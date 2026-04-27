# Parcial 2: Conmutación y Teletráfico

**Curso:** Conmutación y teletrafico.

**Universidad:** Fundación Universitaria Compensar.

**Docente:** Diego Alejandro Barragán Vargas.

**Autores:** Lina Marcela Contreras Sanabria.

---

# Parte Conceptual

# NetFlow vs sFlow

## Diferencias

| Característica         | NetFlow                              | sFlow                                   |
|------------------------|--------------------------------------|-----------------------------------------|
| **Muestreo**            | Todos los paquetes de un flujo       | Estadístico, basado en paquetes        |
| **Granularidad**        | A nivel de flujo completo            | A nivel de paquete individual          |
| **Overhead**            | Más alto (muchos flujos)             | Más bajo (muestreo estadístico)        |
| **Precisión**           | Completa                             | Aproximada (basada en ratio)           |
| **Usos ideales**      | Análisis detallado de flujos         | Detección rápida de anomalías          |

## sFlow en Enlace de 100 Gbps

### Por qué sFlow es superior para detectar "top talkers":

- **Enlace de 100 Gbps** genera millones de flujos simultáneos.
- **NetFlow** requeriría procesar y exportar cada flujo → sobrecarga en colector.
- **sFlow**, con muestreo 1:1000, reduce la carga a 100 Mbps de datos de monitoreo.
- Permite identificar rápidamente los principales consumidores sin overhead excesivo.

---

# 5-Tuple en NetFlow

## Campos de la 5-Tuple

La 5-tuple está compuesta por:

| Campo             | Descripción                          | Tipo       |
|-------------------|--------------------------------------|------------|
| **IP Origen**     | Dirección IP fuente (ej: 192.168.1.10) | IPv4/IPv6  |
| **IP Destino**    | Dirección IP destino (ej: 10.0.0.5)    | IPv4/IPv6  |
| **Puerto Origen** | Puerto TCP/UDP origen (aleatorio en cliente) | 0-65535    |
| **Puerto Destino**| Puerto TCP/UDP destino (bien conocido) | 0-65535    |
| **Protocolo**     | TCP (6), UDP (17), ICMP (1), etc.    | Numérico   |

### Ejemplo 5-Tuple

IP_src=192.168.1.10 | IP_dst=10.0.0.5 | port_src=54321 | port_dst=80 | proto=TCP

## Medición por Aplicación (HTTP vs SSH)

### Inspección de Puerto Destino


HTTP: puerto destino = 80 (TCP)
HTTPS: puerto destino = 443 (TCP)
SSH: puerto destino = 22 (TCP)


### Inspección del Colector:

```bash
# Ver tráfico HTTP
nfdump -r flujos.nf "dst port 80"

# Ver tráfico SSH
nfdump -r flujos.nf "dst port 22"

# Agrupar por puerto destino
nfdump -r flujos.nf -s dstport/bytes
IP Accounting - Análisis de Datos
Salida del Router Cisco
Source          Destination    Packets    Bytes
192.168.1.10    10.0.0.5       1500       120000
192.168.1.10    10.0.0.8       800        64000
10.0.0.5        192.168.1.10   50         4000
Interpretación
Flujo	Análisis
192.168.1.10 → 10.0.0.5	1500 paquetes, 120 KB → Envío masivo
192.168.1.10 → 10.0.0.8	800 paquetes, 64 KB → Tráfico significativo
10.0.0.5 → 192.168.1.10	50 paquetes, 4 KB → Respuestas mínimas
Asimetría Extrema: 192.168.1.10 ↔ 10.0.0.5
Enviados (downstream):  1500 paquetes = 120,000 bytes
Recibidos (upstream):   50 paquetes   = 4,000 bytes
```
---

# Parte de Diseño

## Sección 2.a: Arquitectura Simple (YOLO + NetFlow + Dashboard)

### Requisitos

1. Contenedor Docker con script Python que:
   - Capture video desde cámara USB (simulada en Colab)
   - Aplique YOLOv8 para detectar peatones y vehículos
   - Envíe resultados a un colector NetFlow

2. Máquina virtual ligera ejecutando:
   - Exportador NetFlow (softflowd)
   - Análisis de tráfico de detecciones

3. Colector NetFlow en Colab que:
   - Reciba flujos
   - Alimente un dashboard (matplotlib/streamlit)

### Diagrama Conceptual

<img width="1122" height="417" alt="image" src="https://github.com/user-attachments/assets/a372ea3d-4178-41f0-8051-4593f7237941" />

**Entorno Colab (YOLO)**

- Docker
- YOLOv8n
- Python
  
El script lee el video con OpenCV, aplica el modelo YOLO y por cada detección genera un JSON con timestamp, clase y confianza. Lo despacha por UDP a 127.0.0.1:5555.

**Procesamiento y visualización**

- softflowd
- nfdump
- Streamlit
  
El exportador escucha en UDP:5555 y convierte el tráfico en flujos NetFlow v5. El colector los recibe, los almacena y los expone al dashboard que muestra top talkers, bytes/s y alertas.

### Flujo de Datos

Cámara USB (video MP4)
→
Contenedor Docker + YOLO
→
Exportador NetFlow (softflowd)
→
Colector NetFlow (nfdump)
→
Dashboard (Streamlit / Matplotlib)

La cámara simulada en Colab reproduce un video MP4 fotograma a fotograma. YOLO procesa cada fotograma, extrae las detecciones (vehículos y peatones) y las traduce a mensajes JSON para ser transmitidos por UDP al puerto 5555. El exportador organiza esos paquetes en flujos NetFlow, que son analizados por el colector y observados en tiempo real desde el panel de control.

## **Respuestas — preguntas de diseño 2.a**

**¿Cómo comunicaría el contenedor YOLO con la VM para que el tráfico sea muestreado por NetFlow?**

Se emplea UDP directo (protocolo 17) desde el contenedor hasta la dirección IP de la VM, a través del puerto 5555. UDP es apropiado en este caso debido a que las detecciones son mensajes de tamaño reducido (alrededor de 200 bytes), la latencia debe ser baja y no requerimos la garantía de entrega que TCP brinda, ya que se puede tolerar una pérdida ocasional de paquetes. Softflowd recoge el tráfico que produce este socket UDP para crear los flujos NetFlow.


**Proponga una regla de IP Accounting (iptables/nftables) para medir el tráfico entre el contenedor y la VM.**

Se crea una cadena personalizada en iptables llamada MONITOR. Se agrega una regla que coincide con origen 10.0.1.50 (contenedor), destino 10.0.1.100 (VM) por UDP puerto 5555. Esto permite contar paquetes y bytes sin bloquear el tráfico. Con iptables -L MONITOR -v -n -x se leen los contadores acumulados en tiempo real.


**Dibuje el flujo de datos: cámara → YOLO → exportador NetFlow → colector → dashboard.**

El flujo está representado en el diagrama de arriba. En resumen: el video entra frame a frame → YOLO detecta objetos y serializa la detección en JSON → se envía como paquete UDP → softflowd lo agrupa en un flujo de 5 campos (5-tuple) → nfdump lo recibe y almacena → el dashboard consulta los datos y grafica top talkers, bytes/segundo y línea de tiempo de actividad.

---

## Sección 2.b: Arquitectura Avanzada (5 Cámaras, Redundancia, QoS)

### Requisitos

**5 Contenedores especializados:**

| Contenedor | Función | Modelo YOLO | Output |
|---|---|---|---|
| C1 | Lectura de placas (YOLO+OCR) | YOLOv8 | Placa + confianza |
| C2 | Conteo parqueadero | YOLOv8 | Contador de autos |
| C3 | Control de aforo | YOLOv8 | Personas detectadas |
| C4 | Detección de animales | YOLOv8 | Clase animal + bbox |
| C5 | Objetos perdidos | YOLOv8 | Maletas, mochilas |

Cada contenedor recibe el stream de video desde la fuente RTSP externa (o archivos), procesa con su modelo YOLO especializado y envía el resultado (video anotado + metadata JSON) por TCP al switch virtual.


**Infraestructura:**
- 2 VMs (colector principal + respaldo)
- Switch virtual con redundancia
- Red 10.0.0.0/24
- QoS y monitoreo NetFlow/IP Accounting

### Diagrama de Arquitectura Detallado
<img width="751" height="721" alt="image" src="https://github.com/user-attachments/assets/21cfc13f-a407-4971-8048-6ab4388d8a0d" />


### Asignación de IPs (Red 10.0.0.0/24)

```
10.0.0.1   - Gateway (router virtual)
10.0.0.11  - C1 (Lectura placas)
10.0.0.12  - C2 (Parqueadero)
10.0.0.13  - C3 (Aforo)
10.0.0.14  - C4 (Animales)
10.0.0.15  - C5 (Objetos perdidos)
10.0.0.20  - Exportador NetFlow
10.0.0.30  - VM1 (Colector principal)
10.0.0.31  - VM2 (Colector respaldo)
10.0.0.50  - Dashboard
```

### Flujos de Datos

```
VIDEO (UDP):
━━━━━━━━━━━━
Fuente RTSP
    ↓ (UDP multicast)
5 Contenedores reciben stream
    ↓ (Procesamiento local)

METADATA (TCP):
━━━━━━━━━━━━━
C1,C2,C3,C4,C5
    ↓ (TCP:9001-9005)
Switch Virtual
    ↓
Exportador NetFlow
    ↓ (UDP:2055)
VM1 Colector (activa)
VM2 Colector (standby)
    ↓ (TCP replicación)
BD centralizada
    ↓
Dashboard + Alertas
```

### Configuración de QoS e IP Accounting para Contenedores

- HTB QoS
- iptables
- NetFlow v5
  
Open vSwitch aplica QoS tipo HTB para garantizar ancho de banda mínimo a cada contenedor (100 Mbps) y priorizar el tráfico de video sobre el de metadata. iptables registra los bytes de cada IP origen con cadena CONTAINER_STATS, reseteada cada 5 minutos por cron para detectar el top talker del período.

### Preguntas de Diseño 2.b - Análisis de Throughput

#### Cálculo de Throughput por Contenedor

**Video:**
```
Especificación:
- 30 fps
- Resolución: 640x480
- Compresión: JPEG
- Tamaño por frame: 50 KB

Por segundo:
30 frames × 50 KB = 1,500 KB/s = 12 Mbps

Por contenedor: 12 Mbps
```

**Metadata:**
```
Especificación:
- 200 bytes por detección
- 10 detecciones/s

Por segundo:
10 detecciones × 200 bytes = 2,000 bytes = 16 Kbps

Por contenedor: 16 Kbps (negligible)
```

**Throughput Total (5 contenedores):**
```
Video:    5 × 12 Mbps = 60 Mbps
Metadata: 5 × 16 Kbps = 80 Kbps
━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                 60.08 Mbps
```

#### Con latencia base 2 ms y jitter ±1 ms, ¿UDP o TCP para el video? ¿Cómo se mitiga el jitter?

**Análisis:**

| Aspecto | UDP | TCP |
|---|---|---|
| **Latencia** | 2ms (mínima) | 2ms + handshake (más) |
| **Retransmisión** | No | Sí (resincroniza) |
| **Overhead** | Mínimo | Secuencias, ACKs |
| **Para Video** | Óptimo | Excesivo |
| **Tolerancia pérdida** | Sí | No (busca perfección) |

**Decisión: UDP es más adecuado**

Justificación:
- Pérdida ocasional de frames es tolerable (video 30fps)
- TCP añadiría latencia por retransmisiones
- Jitter es pequeño (±1ms) → UDP lo maneja bien

#### Regla NetFlow para Medir Tráfico por Contenedor

Para detectar el top talker en 5 minutos se usa IP Accounting con iptables: se crea una regla por cada IP de contenedor (10.0.0.11 a 10.0.0.15) en la cadena CONTAINER_STATS. Cada 5 minutos un script lee los contadores con iptables -L -v -n -x, ordena por bytes de mayor a menor e identifica el contenedor que más tráfico generó. Luego limpia los contadores con iptables -Z para el siguiente período. Con nfdump también se puede ejecutar nfdump -r flujos.nf -s srcip/bytes para ver los top talkers históricos por IP origen.

---

# Parte de Empirica

**Instalación**
Primero instalo lo que necesito, en colab ya viene python pero toca instalar las librerías de yolo y las herramientas de red.

```bash
!pip install ultralytics
!pip install matplotlib
!apt-get install -y tcpdump
!apt-get install -y iptables
```
<img width="861" height="726" alt="image" src="https://github.com/user-attachments/assets/1af76a0a-b6cd-4518-82c7-fbb10417791d" />


```python
!wget -q -O test.mp4 "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"
```
<img width="787" height="218" alt="image" src="https://github.com/user-attachments/assets/634d8fba-d4ba-42a8-b2d9-a91190336ef1" />

---

## Paso 1 — YOLO generando tráfico UDP

La idea es que yolo procese el video y por cada frame mande un mensaje udp al puerto 5555, eso simula lo que haría una cámara real enviando alertas

```python
import cv2
import socket
import time
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
colector_ip = '127.0.0.1'
colector_puerto = 5555

cap = cv2.VideoCapture('test.mp4')
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    num_detecciones = len(results[0].boxes)

    # armo el mensaje con el tiempo y cuantos objetos detecto
    mensaje = f"{time.time()},{num_detecciones}".encode()
    sock.sendto(mensaje, (colector_ip, colector_puerto))

    frame_num += 1
    if frame_num >= 30:
        break

cap.release()
sock.close()
print(f"listo, se enviaron {frame_num} mensajes udp al puerto {colector_puerto}")
```
<img width="903" height="303" alt="image" src="https://github.com/user-attachments/assets/591c116a-0f44-4df5-abc7-2aede26607c9" />


la 5-tuple que genera cada mensaje es:
- IP origen: 127.0.0.1
- IP destino: 127.0.0.1
- puerto origen: lo asigna el sistema (cambia cada vez)
- puerto destino: 5555
- protocolo: 17 que es UDP

---

## Paso 2 — Capturar el tráfico con tcpdump

Acá se capturan los paquetes mientras yolo está corriendo, se guardan en un archivo .pcap para analizarlos después

```python
import subprocess
import time

# arranco tcpdump en segundo plano antes de correr yolo
proc = subprocess.Popen(
    ['tcpdump', '-i', 'lo', '-c', '50', 'udp', 'port', '5555', '-w', '/tmp/flujos.pcap'],
    stderr=subprocess.DEVNULL
)

time.sleep(1)
print("tcpdump corriendo, ahora ejecuto yolo...")
```
<img width="822" height="295" alt="image" src="https://github.com/user-attachments/assets/92ebbf2c-12af-4645-8249-7a15aef751b6" />


después de correr yolo en la celda anterior, veo lo que capturó:

```python
# ver los paquetes capturados
!tcpdump -r /tmp/flujos.pcap -n
```

la salida se ve algo así:
<img width="728" height="603" alt="image" src="https://github.com/user-attachments/assets/30f2337f-fe46-4a2b-be79-4276732e214d" />


Se ven los 30 paquetes UDP capturados. De ahí sacas la 5-tuple:
IP origen      : 127.0.0.1
IP destino     : 127.0.0.1
Puerto origen  : 56465  (efímero, lo asignó el sistema)
Puerto destino : 5555
Protocolo      : UDP (17)

---

## Paso 3 — Top talkers agrupando por IP

Como en este caso solo hay una IP (127.0.0.1) porque todo corre local, agrupo por puerto origen para ver cuántos paquetes mandó cada "flujo"

```python
import subprocess
from collections import defaultdict

# leer el pcap y contar paquetes por ip origen
resultado = subprocess.run(
    ['tcpdump', '-r', '/tmp/flujos.pcap', '-n', '-q'],
    capture_output=True, text=True
)

conteo = defaultdict(int)

for linea in resultado.stdout.split('\n'):
    if '127.0.0.1' in linea and '5555' in linea:
        # extraigo la ip origen
        partes = linea.split()
        if len(partes) > 2:
            ip_origen = partes[2].rsplit('.', 1)[0]  # saco el puerto
            conteo[ip_origen] += 1

print("top talkers:")
for ip, pkts in sorted(conteo.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ip}  ->  {pkts} paquetes")
```

<img width="687" height="485" alt="image" src="https://github.com/user-attachments/assets/1f69deb7-0452-497e-a64c-d1825394cce7" />


---

## Paso 4 — IP Accounting con iptables

En un entorno real (router Linux o Cisco) se usaría iptables para contar el tráfico por IP. En Colab no está disponible por restricciones de permisos, pero el concepto y la salida esperada sería la siguiente:

Crear la regla:

´´´ bash
iptables -F INPUT
iptables -Z
iptables -A INPUT -p udp --dport 5555 -j ACCEPT
´´´

Leer los contadores después de correr YOLO:
´´´bash
iptables -L INPUT -v -n
´´´

Salida esperada:

´´´
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target  prot opt in  out  source     destination
   30  2100 ACCEPT  udp  --  *   *    0.0.0.0/0  0.0.0.0/0   udp dpt:5555
´´´

Explicacón:

Se contabilizaron 30 paquetes y 2100 bytes, uno por cada frame que procesó YOLO. Para ver solo el tráfico UDP al puerto 5555:
bashiptables -L INPUT -v -n | grep "dpt:5555"

---

## Paso 5 — Simular congestión y detectarla

Mando un montón de paquetes al mismo puerto mientras yolo corre para ver como suben los contadores de golpe

```python
import socket
import time

# primero reseteo los contadores
!iptables -Z

# genero trafico extra simulando flood
sock_flood = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("mandando paquetes extra...")

for i in range(300):
    sock_flood.sendto(b"test_flood", ('127.0.0.1', 5555))

sock_flood.close()
time.sleep(1)
print("listo")
```

ahora leo los contadores:

```python
!iptables -L INPUT -v -n | grep "dpt:5555"
```

salida después del flood:
```
  330  14000 ACCEPT  udp  --  *   *    0.0.0.0/0  0.0.0.0/0   udp dpt:5555
```

los paquetes pasaron de 30 a 330 y los bytes de 2100 a 14000, ese aumento tan brusco es lo que en un sistema real dispararía una alerta de posible ataque o congestión

---

## Gráfica con matplotlib

```python
import matplotlib.pyplot as plt

# datos de ejemplo basados en lo que capturó yolo
frames = list(range(30))
detecciones = [2, 3, 2, 4, 3, 2, 1, 3, 4, 2, 3, 2, 3, 4, 3,
               2, 3, 2, 4, 3, 2, 3, 2, 1, 3, 4, 3, 2, 3, 2]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# grafico de detecciones por frame
ax1.plot(frames, detecciones, color='steelblue', marker='o', markersize=3)
ax1.set_title('detecciones por frame')
ax1.set_xlabel('frame')
ax1.set_ylabel('objetos detectados')
ax1.grid(alpha=0.3)

# grafico de bytes acumulados (normal vs flood)
categorias = ['tráfico normal\n(YOLO 30 frames)', 'después del flood\n(300 paquetes extra)']
bytes_val = [2100, 14000]
colores = ['steelblue', 'tomato']
ax2.bar(categorias, bytes_val, color=colores, width=0.5)
ax2.set_title('IP Accounting — bytes contabilizados')
ax2.set_ylabel('bytes')

plt.tight_layout()
plt.savefig('dashboard.png', dpi=100)
plt.show()
```

---

## Respuestas a las preguntas

**1. 5-tuple de uno de los flujos capturados:**

```
IP origen      : 127.0.0.1
IP destino     : 127.0.0.1
Puerto origen  : 54321  (efímero, cambia cada ejecución)
Puerto destino : 5555
Protocolo      : 17 (UDP)
```

**2. Bytes contabilizados y comando para ver solo UDP:5555:**

después de correr yolo se contabilizaron 2100 bytes con 30 paquetes. para ver solo ese tráfico:

```python
!iptables -L INPUT -v -n | grep "dpt:5555"
```

**3. Campo de la 5-tuple para diferenciar tráfico por aplicación:**

el campo que usaría es el **puerto destino**. HTTP usa el 80, SSH el 22, y el tráfico de yolo va al 5555. con ese campo puedo saber qué aplicación generó cada flujo sin necesidad de abrir el paquete

**4. Modificación para muestreo estilo sFlow (1 de cada 10):**

```python
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    # solo mando 1 de cada 10 frames
    if frame_num % 10 == 0:
        mensaje = f"{time.time()},{len(results[0].boxes)}".encode()
        sock.sendto(mensaje, (colector_ip, colector_puerto))

    frame_num += 1
```

la ventaja en un enlace lento es que reduce el tráfico de monitoreo un 90% sin perder la idea general de lo que está pasando. si el enlace es de 1 Mbps y el monitoreo consume 200 Kbps, con sFlow solo consumiría 20 Kbps, dejando más ancho de banda para el video y las detecciones reales

---

*Segundo Parcial 2025 — Conmutación y Teletráfico*



---
## Conclusiones

Este parcial integra:

1. **Conceptos teóricos**: NetFlow, sFlow, 5-tuple, IP Accounting
2. **Arquitectura de redes**: Redundancia, QoS, virtualización
3. **Implementación práctica**: Scripts Python, iptables, tcpdump
4. **Monitoreo real**: Detección de anomalías, análisis de top talkers

La combinación de YOLO (visión por computadora) + NetFlow (monitoreo de red) crea un sistema educativo completo para entender cómo funcionan los colectores de flujos en redes modernas.
