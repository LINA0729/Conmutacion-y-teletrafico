# Primer Taller – Conmutación y Teletráfico

## Uso de Docker para simulación de redes y análisis de protocolos

### Integrantes

* Lina Marcela Contreras Sanabria

# Introducción

Docker permite que aplicaciones se ejecuten en entornos separados, llamados contenedores, lo cual hace más fácil replicar circunstancias complicadas sin la necesidad de instalar numerosas dependencias en el sistema operativo principal.

El uso de Docker en telecomunicaciones y redes es examinado en este taller. Su funcionamiento se analiza mediante la ejecución de un contenedor que reproduce un video en la terminal. Además, se usan Gazebo y ROS para construir un ambiente de simulación de robots móviles. Asimismo, se analizan nociones de redes como ARP, jitter y latencia mediante el uso de herramientas de análisis de tráfico como Wireshark. El propósito principal es entender la forma en que Docker posibilita la creación de ambientes controlados para estudiar cómo se comportan los protocolos de red.los de red y los sistemas robóticos.

# Punto 1 – Instalación y uso de Docker

## Instalación de Docker

Para el desarrollo del taller se utilizó Docker Desktop en un sistema operativo Windows con integración a WSL2.

### Paso 1 – Descargar Docker

Se descargó Docker Desktop desde la página oficial:
[
https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
<img width="1575" height="815" alt="image" src="https://github.com/user-attachments/assets/18d4270d-0965-4b0e-a2f8-97c946312abc" />

### Paso 2 – Instalación

Durante la instalación se habilitó la opción de integración con WSL2, lo que permite ejecutar contenedores Linux directamente desde la terminal de Ubuntu en Windows.

### Paso 3 – Verificación de la instalación

Se verificó el correcto funcionamiento de Docker ejecutando el comando:

```bash
docker --version
```

<img width="483" height="72" alt="image" src="https://github.com/user-attachments/assets/db762b81-30ec-4c20-aa13-80e04e6c1a67" />

Este comando permite confirmar que Docker está instalado correctamente en el sistema.

# Punto 1A – Ejecución de contenedor con reproducción de video

Se ejecutó el siguiente comando en la terminal:

```bash
docker run --rm -it wernight/funbox cvlc --no-audio -V caca /examples/countdown.mp4
```

## Explicación del comando

**docker run:**
Permite ejecutar un contenedor a partir de una imagen de Docker.

**--rm:**
Elimina automáticamente el contenedor una vez finalizada la ejecución.

**-it:**
Permite ejecutar el contenedor en modo interactivo.

**wernight/funbox:**
Es la imagen de Docker utilizada. Contiene diversas herramientas de consola.

**cvlc:**
Es la versión de VLC que funciona en modo terminal.

**--no-audio:**
Desactiva el sonido del video.

**-V caca:**
Especifica el modo de visualización del video.

**/examples/countdown.mp4:**
Es el archivo de video que se reproduce dentro del contenedor.

## Resultado obtenido

Cuando se ejecuta el comando, Docker descarga la imagen de Docker Hub automáticamente y luego inicia un contenedor temporal. En el contenedor, VLC opera en modo consola y reproduce directamente un video de cuenta regresiva en formato ASCII en la terminal.

Con el ejercicio, entendemos cómo funcionan los contenedores Docker a nivel básico y la manera en que se ejecutan aplicaciones sin necesidad de instalarlas en el sistema principal.

Evidencia: https://youtu.be/T7y5Uli4L3E


# Punto 1B – Simulación con ROS y Gazebo

La plataforma de desarrollo para robots conocida como ROS (Robot Operating System) facilita la integración de simuladores, controladores y sensores. Gazebo es un simulador físico que posibilita la visualización de robots en ambientes virtuales.

## Creación del Dockerfile

Se creó el archivo llamado Dockerfile-ros con el siguiente contenido:

```bash
FROM osrf/ros:noetic-desktop-full

RUN apt update && apt install -y 
ros-noetic-gazebo-ros 
ros-noetic-gazebo-ros-pkgs

CMD ["bash"]
```
<img width="548" height="373" alt="image" src="https://github.com/user-attachments/assets/094c4150-d50d-40f0-bda8-7ad3cded6b52" />

## Construcción de la imagen

```bash
docker build -t ros-gazebo -f Dockerfile-ros 
```
<img width="1017" height="265" alt="image" src="https://github.com/user-attachments/assets/d5904dc2-63fb-4c1c-a670-e6f8b6d27600" />

Este comando crea una nueva imagen llamada ros-gazebo.

## Ejecución del contenedor

```bash
docker run -it --net=host ros-gazebo
```
<img width="1255" height="380" alt="image" src="https://github.com/user-attachments/assets/b2617c02-edfa-47d5-a660-4472d62e6fd0" />

Una vez iniciado el contenedor se ejecuta:

roscore

Esto inicia el núcleo de ROS que permite la comunicación entre nodos.
<img width="1212" height="632" alt="image" src="https://github.com/user-attachments/assets/6e70ee0e-789e-4870-8160-3cbec3387f66" />

# Punto 1C – Simulación de robot con LIDAR y SLAM

En este ejercicio se implementa la simulación de un robot TurtleBot3 utilizando sensores LIDAR y el algoritmo SLAM para la construcción de mapas.

SLAM significa Simultaneous Localization and Mapping, y permite a un robot construir un mapa del entorno mientras determina su propia posición.

## Creación del Dockerfile

Se creó un archivo llamado Dockerfile-turtlebot con el siguiente contenido:

```bash
FROM osrf/ros:noetic-desktop-full

RUN apt update && apt install -y 
ros-noetic-turtlebot3 
ros-noetic-turtlebot3-slam 
ros-noetic-turtlebot3-gazebo

ENV TURTLEBOT3_MODEL=burger

CMD ["bash"]
```
<img width="783" height="400" alt="image" src="https://github.com/user-attachments/assets/dc94e5f7-10ff-4a9a-ace5-4107735312fc" />


## Construcción de la imagen

```bash
docker build -t turtlebot3 -f Dockerfile-turtlebot
```
<img width="937" height="502" alt="image" src="https://github.com/user-attachments/assets/85557e44-5551-4046-87eb-4d768786629d" />


## Ejecución de la simulación

Dentro del contenedor se ejecuta:

roslaunch turtlebot3_gazebo turtlebot3_world.launch

Esto inicia la simulación del robot dentro del entorno virtual.

Posteriormente se ejecuta el algoritmo SLAM:

roslaunch turtlebot3_slam turtlebot3_slam.launch

Finalmente se abre RViz para visualizar el mapa generado por el robot a partir de los datos del sensor LIDAR.

Este ejercicio permite observar cómo un robot puede explorar un entorno y construir un mapa en tiempo real.



# Punto 2 – Descubriendo el protocolo ARP

El protocolo ARP (Address Resolution Protocol) se utiliza en redes para traducir direcciones IP en direcciones MAC. Este proceso es necesario para que los dispositivos puedan comunicarse dentro de una misma red local.

## Creación de red Docker

docker network create red_arp

Este comando crea una red virtual tipo bridge donde se conectarán los contenedores.

## Creación de contenedores

docker run -it --name contenedor1 --network red_arp alpine sh

docker run -it --name contenedor2 --network red_arp alpine sh

La imagen Alpine Linux fue utilizada debido a su tamaño reducido.

## Instalación de herramientas

Dentro de los contenedores se instalaron herramientas de red:

apk update
apk add iputils
apk add arping

## Captura de tráfico con Wireshark

Se ejecutó Wireshark en el host y se seleccionó la interfaz docker0. Posteriormente se aplicó el filtro:

arp

Esto permitió visualizar únicamente paquetes ARP.

## Procedimiento

Desde contenedor1 se realizó un ping hacia contenedor2 utilizando su dirección IP.

ping -c 4 IP_DEL_CONTENEDOR2

Durante este proceso Wireshark capturó los paquetes ARP generados.

## Análisis de los paquetes

Primero se envía una solicitud ARP en broadcast preguntando:

"Who has IP_del_contenedor2?"

Este mensaje se envía a la dirección MAC de broadcast FF:FF:FF:FF:FF:FF.

Luego el contenedor2 responde con un mensaje ARP reply indicando su dirección MAC. Esta respuesta es enviada directamente al contenedor que realizó la solicitud.

## Conclusión del análisis

Después del intercambio ARP, el sistema almacena la relación entre dirección IP y dirección MAC en la caché ARP. Esto evita tener que repetir el proceso en futuras comunicaciones.

---

# Punto 3 – Medición de latencia y jitter

La latencia es el tiempo que tarda un paquete de datos en viajar desde un origen hasta un destino y regresar. Este tiempo se conoce como Round Trip Time (RTT).

El jitter representa la variación en la latencia entre diferentes paquetes enviados en una misma comunicación.

## Prueba sin perturbación

Desde contenedor1 se ejecutó:

ping -c 10 IP_DEL_CONTENEDOR2

Esto permitió medir el RTT promedio entre los contenedores.

## Introducción de jitter

Para simular variaciones en la red se utilizó la herramienta tc en el host:

sudo tc qdisc add dev docker0 root netem delay 50ms 20ms distribution normal

Este comando introduce un retardo promedio de 50 ms con una variación de 20 ms.

Posteriormente se ejecutó nuevamente:

ping -c 20 IP_DEL_CONTENEDOR2

Los resultados mostraron una mayor variabilidad en los tiempos de respuesta.

Finalmente se eliminó la configuración de red:

sudo tc qdisc del dev docker0 root

## Análisis

En la segunda prueba se observó que los valores de RTT presentaban mayor variación, lo que indica la presencia de jitter.

## Importancia del jitter

El jitter es especialmente crítico en aplicaciones en tiempo real como:

* Videollamadas
* VoIP
* Juegos en línea
* Streaming en vivo

Cuando el jitter es alto, la calidad de la comunicación puede verse afectada generando cortes o retrasos.

---

# Conclusiones

El uso de Docker permite crear entornos virtuales aislados que facilitan la experimentación con diferentes tecnologías sin afectar el sistema principal. A través de este taller se logró comprender el funcionamiento básico de los contenedores y su aplicación en simulaciones de redes y robótica.

También se analizó el funcionamiento del protocolo ARP, el cual es fundamental para la comunicación dentro de redes locales, ya que permite la resolución de direcciones IP a direcciones MAC.

Finalmente se estudiaron conceptos importantes como la latencia y el jitter, los cuales influyen directamente en la calidad de las comunicaciones en redes modernas.

Estos experimentos demuestran cómo herramientas como Docker y Wireshark pueden utilizarse para estudiar el comportamiento real de los protocolos de red y comprender mejor su funcionamiento.

