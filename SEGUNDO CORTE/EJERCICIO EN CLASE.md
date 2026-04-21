Aquí tienes el contenido completo y estructurado para tu archivo `README.md`. [cite_start]He organizado las secciones para que el desarrollo técnico y el análisis teórico queden separados, facilitando la lectura y cumpliendo con todos los puntos solicitados en la guía del ejercicio[cite: 102, 109].

---

# Ejercicio en Clase: Análisis de Tráfico de Red (TCP vs. UDP)

[cite_start]Este repositorio contiene el desarrollo del ejercicio práctico de captura y análisis de protocolos de transporte utilizando el modelo de visión artificial **YOLOv8**[cite: 21]. [cite_start]El objetivo es contrastar el comportamiento de los protocolos **TCP** y **UDP** en diferentes escenarios de red[cite: 22].

---

## 🛠️ Desarrollo del Ejercicio

[cite_start]El ejercicio se realizó utilizando **Google Colab** como servidor en la nube basado en Linux[cite: 25].

### 1. Preparación del Entorno
[cite_start]Se instalaron las herramientas necesarias para la ejecución de modelos de IA y la captura de paquetes de red[cite: 29]:
* [cite_start]**YOLOv8 (Ultralytics)**: Para la lógica de visión artificial[cite: 31].
* [cite_start]**tcpdump**: Capturador de tráfico de red por línea de comandos[cite: 33].

### 2. Fase 1: Análisis de la Descarga (Tráfico TCP)
[cite_start]Se capturó el tráfico generado durante la descarga de los componentes del modelo pre-entrenado[cite: 37].
* [cite_start]**Comando de captura**: `!sudo tcpdump -i eth0 -s 1500 -w descarga_tcp.pcap &`[cite: 44].
* [cite_start]**Acción**: Se cargó el modelo `yolov8n.pt`, lo que activó una conexión **TCP**[cite: 51, 54].
* [cite_start]**Resultado**: Captura exitosa del tráfico fiable orientado a la conexión[cite: 38].

### 3. Fase 2: Transmisión de Video (Tráfico UDP)
[cite_start]Se simuló la transmisión de datos de una cámara web para analizar el tráfico en tiempo real[cite: 63].
* [cite_start]**Comando de captura**: `!sudo tcpdump -i eth0 -s 1500 -w video_udp.pcap udp and port 12345 &`[cite: 68].
* [cite_start]**Acción**: Script en Python enviando 100 paquetes de datos simulando fotogramas[cite: 81].
* [cite_start]**Incidencia Técnica**: En esta fase, la captura en la interfaz `eth0` no registró el tráfico debido a que el script enviaba datos a la dirección de **loopback** (`127.0.0.1`)[cite: 75]. El tráfico local no atraviesa la interfaz de red principal `eth0`, lo que explica por qué el archivo resultante no contenía los datagramas esperados.

---

## ❓ Cuestionario de Análisis

### **1. ¿Qué es YOLO, sus características y arquitectura?**
* [cite_start]**Definición**: YOLO (*You Only Look Once*) es un modelo potente de visión por computadora[cite: 21].
* [cite_start]**Características**: Capacidad de realizar inferencia en tiempo real y alta eficiencia en la detección de objetos[cite: 23].
* [cite_start]**Arquitectura**: Se basa en una red neuronal que procesa la imagen completa en una sola pasada, prediciendo cajas delimitadoras y probabilidades de clase simultáneamente[cite: 103].

### **2. Protocolo vs. Aplicación: ¿Por qué TCP y UDP?**
* [cite_start]**Descarga (TCP)**: Se utiliza TCP porque es un protocolo **fiable** y orientado a la conexión[cite: 38, 40]. [cite_start]La descarga del modelo requiere que no se pierda ni un solo bit para que el archivo funcione correctamente[cite: 104].
* [cite_start]**Video (UDP)**: Se utiliza UDP para minimizar la **latencia**[cite: 64]. [cite_start]En una transmisión en vivo, es preferible perder un paquete ocasional que retrasar todo el video esperando una retransmisión[cite: 104].

### **3. Fiabilidad vs. Velocidad**
* [cite_start]**Retransmisiones**: El filtro `tcp.analysis.retransmission` en Wireshark muestra paquetes perdidos que debieron enviarse de nuevo[cite: 99, 105].
* [cite_start]**Crucial vs. Perjudicial**: Este mecanismo es crucial para descargar archivos (garantiza integridad) pero sería **perjudicial** para un video en vivo, ya que causaría congelamientos y retrasos acumulados en la imagen[cite: 106].

### **4. Identificación del Origen**
[cite_start]Para aislar el tráfico específico del servidor en Wireshark, se pueden utilizar los filtros de visualización de direcciones IP[cite: 107]:
* [cite_start]`ip.src == [IP_Servidor]`: Para ver los paquetes que el servidor envía al equipo[cite: 108].
* [cite_start]`ip.dst == [IP_Servidor]`: Para ver los paquetes enviados desde el equipo hacia el servidor[cite: 108].

---

**Presentado por:** [Tu Nombre]  
[cite_start]**Docente:** Diego Alejandro Barragán Vargas [cite: 12]  
[cite_start]**Institución:** Fundación Universitaria Compensar [cite: 1, 8]  
[cite_start]**Materia:** Conmutación y Teletráfico [cite: 2]
