# **PARCIAL**

## **PRIMER PUNTO**

### A. Explicar la diferencia fundamental entre la latencia y el jitter ¿cual de estas 2 metricas tendria un impacto mas negativo en una llamada de VoIP y porque?

Latencia:
Es el tiempo que tarda un paquete en viajar desde el origen hasta el destino en la red.

Jitter: 
Es el cambio en el tiempo que tardan los paquetes en llegar.

Impacto en la VoIP:
El jitter tiene un impacto más negativo, ya que la voz se oye distorsionada o entrecortada si los paquetes arriban en tiempos distintos.

### B. Una aplicación envía datos usando protocolo TCP, mientras que otra usa UDP para la misma tarea de transmisión de video. ¿Cuál es más eficiente en términos de throughput y cuál ofrece mayor control de la pérdida de paquetes? Justifique su respuesta basándose en la “anatomía” de sus cabeceras.

En términos de throughput, UDP es más eficiente porque tiene una cabecera más pequeña (8 bytes) y no realiza control de conexión ni retransmisiones, lo que reduce la sobrecarga. En cuanto al control de pérdida de paquetes, TCP es superior, ya que incluye números de secuencia, confirmaciones (ACK) y retransmisiones, lo que garantiza una entrega confiable de los datos.

### C. Al ejecutar el comando “arp -a” en la CMD de Windows, se obtiene una lista de direcciones IP y direcciones físicas.
<img width="783" height="902" alt="image" src="https://github.com/user-attachments/assets/379f1cd9-c25a-4fc7-9d1c-0b6669cca92b" />

¿Qué protocolo de la suite TCP/IP llena esta tabla y cuál es su función principal dentro de una red local? Relacionar la respuesta con la estructura de una trama Ethernet.

ARP (Address Resolution Protocol) es el protocolo que completa esa tabla. Su propósito fundamental es asociar una dirección IP con una dirección MAC en el ámbito de una red local.

Permite determinar la MAC de destino que se necesita para construir una trama Ethernet.

### D. Mencionar dos diferencias clave entre las arquitecturas SNMPv2c y SNMPv3. Enfocarse en los aspectos de seguridad y el tipo de mensajes que manejan.

Seguridad:

SNMPv2c usa "community strings" como contraseña en texto plano, lo que proporciona una seguridad baja.

SNMPv3 tiene autenticación, cifrado y control de acceso, lo que lo hace muy seguro.

Mensajes:

SNMPv2c tiene la capacidad de manejar mensajes como Get, Set, GetBulk y Trap.

SNMPv3 utiliza la misma clase de mensajes, pero añade seguridad mediante la autenticación y la confidencialidad en la transmisión.

Se evidencia una mejoria sobre todo en lo relacionado con seguridad.

### E. Define que es un OID y cual es su relación con MIB. ¿Si un administrador quiere saber la cantidad de bytes que ha recibido una interface de red, ¿Que operación SNMP (Get,set,trap) debe utilizar y por qué no sería adecuado usar un Trap para esto?

OID:
Es un identificador único que representa un objeto dentro del sistema SNMP.

MIB:
Es una base de datos estructurada como un árbol que incluye todos los elementos consultables.

La operación adecuado es:
GET, ya que facilita la consulta de información del dispositivo.

Ya que los Trap se utilizan para informar automáticamente sobre eventos, no para hacer consultas de datos.


## **SEGUNDO PUNTO**
