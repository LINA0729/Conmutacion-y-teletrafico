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

<img width="1048" height="218" alt="image" src="https://github.com/user-attachments/assets/d0b0c93b-0492-42cc-8d50-b2a9a22721dc" />

### A. Identificar y explicar cada uno de los campos de la cabecera ethernet. ¿Que significa el valor 0x0800 en el campo "Tipo"?.
<img width="1048" height="218" alt="image" src="https://github.com/user-attachments/assets/a16caa4c-edf4-4d45-b8b6-fff531d30d33" />

* MAC destino: dirección física del receptor.
* MAC origen: dirección física del emisor.
* Tipo: indica el protocolo encapsulado.

El valor 0x0800 indica que el protocolo encapsulado es IPv4.

Campos:

MAC destino: dirección física del receptor.

MAC origen: dirección física del emisor.

Tipo: indica el protocolo encapsulado.

El valor 0x0800 indica que el protocolo encapsulado es IPv4.

### B. En la cabecera IPv4, ¿qué significan los campos Protocolo y TTL? ¿Por qué es importante el TTL en red?
<img width="1048" height="218" alt="image" src="https://github.com/user-attachments/assets/2aa024a1-8a60-4554-8078-ccad9cf3a6ca" />

Protocolo:
Señala qué protocolo de transporte está en uso (UDP o TCP, por ejemplo).

TTL (Tiempo de vida):
Señala la cantidad máxima de saltos que un paquete puede realizar antes de ser eliminado. Evita que los paquetes permanezcan indefinidamente en la red.

### C. En la cabecera TCP, explicar la función de los flags ACK y PSH. ¿Qué indica el "Puerto Destino: 80" sobre el servicio al que se intenta acceder?
<img width="1059" height="218" alt="image" src="https://github.com/user-attachments/assets/47f88f6d-57a0-43cb-9e61-020f1ee77fcd" />

ACK:
Confirma que un paquete fue recibido correctamente.

PSH:
Indica que los datos deben enviarse inmediatamente a la aplicación.

Puerto destino 80:
Significa que se está intentando acceder al servicio HTTP.

### D. Si este mismo paquete se enviara usando IPv6, ¿qué cabecera de IPv6 reemplazaría a la cabecera IPv4 mostrada y cuál sería una mejora notable en su procesamiento por parte de los routers?

La cabecera IPv6 reemplaza la cabecera IPv4. Y tendria una cabecera más simple y fija, lo que permite que los routers procesen los paquetes más rápidamente.


## **TERCER PUNTO**

### A. Desde la CMD de Windows, ejecutar el comando pathping.
<img width="667" height="397" alt="image" src="https://github.com/user-attachments/assets/d8e69ea9-a7b9-4d60-a72e-b7b7fe2c1393" />

*Explicar qué información proporciona este comando que no daría un ping o un tracert.**

El comando pathping permite analizar la ruta hacia un destino y además muestra latencia y pérdida de paquetes en cada salto de la red.

A diferencia de ping, que solo mide el tiempo de respuesta con el destino, y de tracert, que solo muestra los routers intermedios, pathping combina ambas funciones y también calcula el porcentaje de pérdida de paquetes en cada nodo.

**Describir el proceso que sigue pathping para obtener sus resultados.**

Proceso de funcionamiento:

1. Primero, averigua la ruta hacia el destino, de manera parecida a lo que hace tracert.

2. Después, manda varios paquetes ICMP a cada uno de los routers en la ruta.

3. Por último, examina los resultados y determina la latencia y el porcentaje de pérdida de paquetes por salto.

Esto hace posible determinar en qué parte de la red hay fallas.

### B. Para monitorear un router de la oficina, decides usar SNMP. El router soporta SNMPv2c con la comunidad "public" de solo lectura.


¿Qué comando de Windows (o herramienta de línea de comandos) podría utilizar para "caminar" por el árbol MIB y obtener todos los valores de la interfaz del router en la IP 192.168.1.1?





















































Si el router envía un mensaje “authenticationFailure” trap al gestor SNMP, ¿Qué evento lo ha provocado y cuál es la ventaja de recibir un Trap en lugar de estar consultando constantemente (polling) el estado del router?
























