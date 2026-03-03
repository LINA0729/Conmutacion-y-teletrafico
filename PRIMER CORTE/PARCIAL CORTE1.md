# **PARCIAL**

## **PRIMER PUNTO**

A. Explicar la diferencia fundamental entre la latencia y el jitter ¿cual de estas 2 metricas tendria un impacto mas negativo en una llamada de VoIP y porque?

La latencia es el tiempo que un paquete demora en desplazarse desde el emisor hasta el receptor.
El jitter es la fluctuación en el tiempo entre paquetes.

El jitter influye de manera más negativa en una llamada VoIP, ya que genera que la voz suene distorsionada o entrecortada como resultado de la llegada irregular de los paquetes.

Un pequeño retraso puede ser ocasionado por una latencia constante, pero la claridad de la conversación se ve afectada directamente por el jitter.

B. Una aplicación envía datos usando protocolo TCP, mientras que otra usa UDP para la misma tarea de transmisión de video. ¿Cuál es más eficiente en términos de throughput y cuál ofrece mayor control de la pérdida de paquetes? Justifique su respuesta basándose en la “anatomía” de sus cabeceras.

En términos de throughput, UDP es más eficiente porque tiene una cabecera más pequeña (8 bytes) y no realiza control de conexión ni retransmisiones, lo que reduce la sobrecarga. En cuanto al control de pérdida de paquetes, TCP es superior, ya que incluye números de secuencia, confirmaciones (ACK) y retransmisiones, lo que garantiza una entrega confiable de los datos.

C. Al ejecutar el comando “arp -a” en la CMD de Windows, se obtiene una lista de direcciones IP y direcciones físicas.
¿Qué protocolo de la suite TCP/IP llena esta tabla y cuál es su función principal dentro de una red local? Relacionar la respuesta con la estructura de una trama Ethernet.

ARP (Address Resolution Protocol) es el protocolo que completa esa tabla.

Su objetivo principal es vincular una dirección IP con una dirección MAC en el interior de una red local.

Conexión con la trama Ethernet:
La trama Ethernet requiere la dirección MAC de destino para transmitir datos en una red LAN. ARP posibilita que la trama se entregue correctamente en la capa de enlace, descubriendo esa dirección MAC a través de la IP.

D. Mencionar dos diferencias clave entre las arquitecturas SNMPv2c y SNMPv3. Enfocarse en los aspectos de seguridad y el tipo de mensajes que manejan.

Seguridad:

SNMPv2c emplea "community strings" como contraseña en texto plano, lo que le otorga una seguridad baja.

SNMPv3 tiene autenticación, cifrado y control de acceso, lo que lo hace muy seguro.

Mensajes:

SNMPv2c tiene la capacidad de manejar mensajes como Get, Set, GetBulk y Trap.

SNMPv3 utiliza la misma clase de mensajes, pero incorpora seguridad a través de la autenticación y confidencialidad en la transmisión.

La mejora significativa de la seguridad es el principal cambio.


## **SEGUNDO PUNTO**
