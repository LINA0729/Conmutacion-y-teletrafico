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

**Infraestructura:**
- 2 VMs (colector principal + respaldo)
- Switch virtual con redundancia
- Red 10.0.0.0/24
- QoS y monitoreo NetFlow/IP Accounting

### Diagrama de Arquitectura Detallado
<img width="305" height="826" alt="image" src="https://github.com/user-attachments/assets/abd257a8-f99b-4567-a07e-3c73a789d902" />


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

### Configuración de QoS

```bash
# En Open vSwitch - Garantizar ancho de banda mínimo
ovs-vsctl set Port eth0 qos=@newqos \
  -- --id=@newqos create QoS \
     type=linux-htb \
     other-config:max-rate=1000000000

# Limitar tráfico por contenedor
ovs-vsctl -- \
  set queue @newqueue \
  other-config:max-rate=100000000 \
  -- add qos @newqos queues

# Prioridad para tráfico crítico (video)
# Prioridad baja para monitoreo
```

### Configuración de IP Accounting para Contenedores

```bash
# Crear cadena para medir tráfico por contenedor
sudo iptables -N CONTAINER_STATS

# C1: Placas
sudo iptables -A CONTAINER_STATS -s 10.0.0.11 -j ACCEPT

# C2: Parqueadero
sudo iptables -A CONTAINER_STATS -s 10.0.0.12 -j ACCEPT

# C3: Aforo
sudo iptables -A CONTAINER_STATS -s 10.0.0.13 -j ACCEPT

# C4: Animales
sudo iptables -A CONTAINER_STATS -s 10.0.0.14 -j ACCEPT

# C5: Objetos perdidos
sudo iptables -A CONTAINER_STATS -s 10.0.0.15 -j ACCEPT

# Aplicar a OUTPUT
sudo iptables -A OUTPUT -j CONTAINER_STATS

# Ver estadísticas por contenedor
sudo iptables -L CONTAINER_STATS -v -n -x

# Limpiar cada 5 minutos (con cron)
# */5 * * * * iptables -Z CONTAINER_STATS && logger "Estadísticas reseteadas"
```

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

#### Protocolo Adecuado: UDP vs TCP

**Condiciones de red:**
```
Latencia base: 2 ms
Jitter: ±1 ms (rango 1-3 ms)
```

**Análisis:**

| Aspecto | UDP | TCP |
|---|---|---|
| **Latencia** | 2ms (mínima) | 2ms + handshake (más) |
| **Retransmisión** | No | Sí (resincroniza) |
| **Overhead** | Mínimo | Secuencias, ACKs |
| **Para Video** | ✅ Óptimo | ❌ Excesivo |
| **Tolerancia pérdida** | Sí | No (busca perfección) |

**Decisión: UDP es más adecuado**

Justificación:
- Pérdida ocasional de frames es tolerable (video 30fps)
- TCP añadiría latencia por retransmisiones
- Jitter es pequeño (±1ms) → UDP lo maneja bien

**Mitigación de Jitter en Receptor:**

```python
from collections import deque
import time

class JitterBuffer:
    def __init__(self, buffer_size=3):
        """Buffer circular para absorber jitter"""
        self.buffer = deque(maxlen=buffer_size)
        self.target_delay = 0.033  # 33ms para 30fps
        
    def add_frame(self, frame, timestamp):
        """Añade frame al buffer"""
        self.buffer.append((frame, timestamp))
    
    def get_frame(self):
        """Retorna frame cuando está listo"""
        if len(self.buffer) >= self.target_delay / 0.033:
            return self.buffer.popleft()[0]
        return None

# Uso
jitter_buf = JitterBuffer(buffer_size=3)

while True:
    frame, ts = receive_udp_frame()
    jitter_buf.add_frame(frame, ts)
    
    display_frame = jitter_buf.get_frame()
    if display_frame:
        process_and_display(display_frame)
    
    time.sleep(0.033)  # 30fps
```

**Técnicas adicionales:**
1. **Interpolación de frames**: llenar gaps con frames intermedios
2. **Reordenamiento**: buffer secuencial por timestamp
3. **PLC (Packet Loss Concealment)**: duplicar últimos datos válidos

#### Regla NetFlow para Medir Tráfico por Contenedor

**Configuración en softflowd:**

```bash
# Exportar flujos agrupados por IP origen
softflowd -i eth0 \
  -n 10.0.0.30:2055 \
  -v 5 \
  -A auto

# Genera flujos con 5-tuple:
# src_ip=10.0.0.11 | dst_ip=10.0.0.30 | port_src=random | port_dst=9001 | proto=TCP
```

**Análisis con nfdump:**

```bash
# Ver top talkers (contenedores que más envían)
nfdump -r flujos.nf -s srcip/bytes | head -5

# Salida esperada:
# IP_src                Bytes      Packets
# 10.0.0.11            12,000,000  3,000  (C1 - placas)
# 10.0.0.12            11,900,000  2,980  (C2 - parqueadero)
# 10.0.0.13            11,800,000  2,950  (C3 - aforo)
# 10.0.0.14             2,400,000    600  (C4 - animales, menos tráfico)
# 10.0.0.15             2,100,000    525  (C5 - objetos perdidos)
```

**IP Accounting: Detectar Mayor Consumidor en 5 Minutos**

```bash
# Método 1: Con iptables (en tiempo real)
# Crear regla para cada contenedor
for i in {11..15}; do
  sudo iptables -A OUTPUT -s 10.0.0.$i -j ACCEPT
done

# Leer cada 5 minutos
while true; do
  echo "=== Estadísticas ($(date)) ==="
  sudo iptables -L OUTPUT -v -n | grep "10.0.0\." | sort -k2 -rn | head -1
  sleep 300
done

# Método 2: Script Python (más completo)
```

**Script Python para monitoreo IP Accounting:**

```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime
from collections import defaultdict

def get_iptables_stats():
    """Obtiene estadísticas de iptables"""
    result = subprocess.run(
        ['sudo', 'iptables', '-L', 'OUTPUT', '-v', '-n', '-x'],
        capture_output=True,
        text=True
    )
    
    stats = defaultdict(lambda: {'pkts': 0, 'bytes': 0})
    
    for line in result.stdout.split('\n'):
        if '10.0.0.' in line:
            parts = line.split()
            if len(parts) >= 2:
                pkts = int(parts[0])
                bytes_val = int(parts[1])
                # Extraer IP destino
                if 'destination' in line.lower():
                    ip = parts[-1]
                    container = {
                        '10.0.0.11': 'C1-Placas',
                        '10.0.0.12': 'C2-Parqueadero',
                        '10.0.0.13': 'C3-Aforo',
                        '10.0.0.14': 'C4-Animales',
                        '10.0.0.15': 'C5-ObjPerdidos'
                    }.get(ip, ip)
                    stats[container]['bytes'] += bytes_val
                    stats[container]['pkts'] += pkts
    
    return stats

def main():
    print("Monitoreo de IP Accounting (cada 5 minutos)")
    print("=" * 60)
    
    while True:
        stats = get_iptables_stats()
        
        # Ordenar por bytes (descendente)
        sorted_stats = sorted(
            stats.items(),
            key=lambda x: x[1]['bytes'],
            reverse=True
        )
        
        print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'Contenedor':<20} {'Bytes':>15} {'Paquetes':>12}")
        print("-" * 50)
        
        max_bytes_container = None
        max_bytes = 0
        
        for container, data in sorted_stats:
            bytes_val = data['bytes']
            pkts = data['pkts']
            print(f"{container:<20} {bytes_val:>15,} {pkts:>12,}")
            
            if bytes_val > max_bytes:
                max_bytes = bytes_val
                max_bytes_container = container
        
        print("-" * 50)
        print(f"🔴 TOP TALKER: {max_bytes_container} ({max_bytes:,} bytes)")
        
        subprocess.run(['sleep', '300'])

if __name__ == "__main__":
    main()
```

---

## Conclusiones

Este parcial integra:

1. **Conceptos teóricos**: NetFlow, sFlow, 5-tuple, IP Accounting
2. **Arquitectura de redes**: Redundancia, QoS, virtualización
3. **Implementación práctica**: Scripts Python, iptables, tcpdump
4. **Monitoreo real**: Detección de anomalías, análisis de top talkers

La combinación de YOLO (visión por computadora) + NetFlow (monitoreo de red) crea un sistema educativo completo para entender cómo funcionan los colectores de flujos en redes modernas.

---

**Versión**: 1.0  
**Última actualización**: 2026-04-26  
**Autor**: Lina - Fundación Universitaria Compensar
