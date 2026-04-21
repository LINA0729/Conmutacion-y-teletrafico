
---

# Ejercicio en Clase: Análisis de Tráfico de Red (TCP vs. UDP)

Este repositorio contiene el desarrollo del ejercicio práctico de captura y análisis de protocolos de transporte utilizando el modelo de visión artificial **YOLOv8**. El objetivo es contrastar el comportamiento de los protocolos **TCP** y **UDP** en diferentes escenarios de red.

---

## Desarrollo del Ejercicio

El ejercicio se realizó utilizando **Google Colab** como servidor en la nube basado en Linux.

### 1. Preparación del Entorno
Se instalaron las herramientas necesarias para la ejecución de modelos de IA y la captura de paquetes de red:
* **YOLOv8 (Ultralytics)**: Para la lógica de visión artificial.
* **tcpdump**: Capturador de tráfico de red por línea de comandos.
<img width="1342" height="728" alt="image" src="https://github.com/user-attachments/assets/2774fcb0-936d-412a-81c9-7bf8f5d20341" />

### 2. Fase 1: Análisis de la Descarga (Tráfico TCP)
Se capturó el tráfico generado durante la descarga de los componentes del modelo pre-entrenado.
* **Comando de captura**: `!sudo tcpdump -i eth0 -s 1500 -w descarga_tcp.pcap &`.
* **Acción**: Se cargó el modelo `yolov8n.pt`, lo que activó una conexión **TCP**.
* **Resultado**: Captura exitosa del tráfico fiable orientado a la conexión.
<img width="1197" height="402" alt="image" src="https://github.com/user-attachments/assets/2b1a1e79-a476-4df7-b2ed-ab21fd224ae7" />
<img width="926" height="747" alt="image" src="https://github.com/user-attachments/assets/6bdc0c84-2ddb-451b-ae2f-ac398037f53f" />


### 3. Fase 2: Transmisión de Video (Tráfico UDP)
Se simuló la transmisión de datos de una cámara web para analizar el tráfico en tiempo real.
* **Comando de captura**: `!sudo tcpdump -i eth0 -s 1500 -w video_udp.pcap udp and port 12345 &`.
* **Acción**: Script en Python enviando 100 paquetes de datos simulando fotogramas.
<img width="697" height="567" alt="image" src="https://github.com/user-attachments/assets/17d0c2bb-9b28-40a0-86c7-bd0e0f834a2f" />

* **Incidencia Técnica**: En esta fase, la captura en la interfaz `eth0` no registró el tráfico debido a que el script enviaba datos a la dirección de **loopback** (`127.0.0.1`). El tráfico local no atraviesa la interfaz de red principal `eth0`, lo que explica por qué el archivo resultante no contenía los datagramas esperados.

* **Problemas encontrados:** A pesar de cambiar la interfaz de captura a lo0 (loopback), tcpdump no logró capturar el tráfico UDP correctamente en Google Colab. El tráfico generado fue capturado en el archivo .pcap, pero el archivo solo contenía paquetes vacíos de 24 bytes, lo que sugiere que tcpdump no pudo captar el tráfico generado.

<img width="680" height="212" alt="image" src="https://github.com/user-attachments/assets/e3bb81ef-f233-43ab-86cb-54867765109d" />
---

## Cuestionario de Análisis

### **1. ¿Qué es YOLO, sus características y arquitectura?**
* **Definición**: YOLO es un modelo potente de visión por computadora.
* **Características**: Capacidad de realizar inferencia en tiempo real y alta eficiencia en la detección de objetos.
* **Arquitectura**: Se basa en una red neuronal que procesa la imagen completa en una sola pasada, prediciendo cajas delimitadoras y probabilidades de clase simultáneamente.

### **2. Protocolo vs. Aplicación: ¿Por qué TCP y UDP?**
* **Descarga (TCP)**: Se utiliza TCP porque es un protocolo **fiable** y orientado a la conexión. La descarga del modelo requiere que no se pierda ni un solo bit para que el archivo funcione correctamente.
* **Video (UDP)**: Se utiliza UDP para minimizar la **latencia**. En una transmisión en vivo, es preferible perder un paquete ocasional que retrasar todo el video esperando una retransmisión.

### **3. Fiabilidad vs. Velocidad**
* **Retransmisiones**: El filtro `tcp.analysis.retransmission` en Wireshark muestra paquetes perdidos que debieron enviarse de nuevo.
* **Crucial vs. Perjudicial**: Este mecanismo es crucial para descargar archivos (garantiza integridad) pero sería **perjudicial** para un video en vivo, ya que causaría congelamientos y retrasos acumulados en la imagen.

### **4. Identificación del Origen**
Para aislar el tráfico específico del servidor en Wireshark, se pueden utilizar los filtros de visualización de direcciones IP:
* `ip.src == [IP_Servidor]`: Para ver los paquetes que el servidor envía al equipo.
<img width="630" height="402" alt="image" src="https://github.com/user-attachments/assets/486a0a88-5fbe-4e13-a241-3b5989a63f31" />

* [cite_start`ip.dst == [IP_Servidor]`: Para ver los paquetes enviados desde el equipo hacia el servidor.
<img width="637" height="295" alt="image" src="https://github.com/user-attachments/assets/89d2599d-0f2d-405c-ab88-b5f3e27afd01" />

---

**Estudiante:** Lina Marcela Contreras 
**Docente:** Diego Alejandro Barragán Vargas
**Institución:** Fundación Universitaria Compensar
**Materia:** Conmutación y Teletráfico
