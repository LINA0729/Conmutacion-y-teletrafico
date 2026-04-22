Fundamentos de Redes Cisco: Módulos 8 - 17
Este repositorio contiene el resumen técnico y los conceptos fundamentales abordados en la certificación de redes, centrándose en la comunicación lógica, el direccionamiento y la seguridad de dispositivos.

Módulo 1: Comunicación entre Redes (Capítulos 8 - 10)
1.1 Protocolo IP y Enrutamiento
El protocolo IP es el responsable de identificar los dispositivos y determinar la mejor ruta para los datos.

Características: No orientado a la conexión, máximo esfuerzo (sin garantía de entrega) e independiente de los medios físicos.

Encapsulamiento: Proceso de añadir información de dirección IP a los datos para su transporte.

1.2 Resolución de Direcciones (ARP y ND)
Para que los datos lleguen al hardware correcto en una red local, se requiere vincular la dirección lógica con la física.

ARP (IPv4): Utiliza mensajes de solicitud y respuesta para encontrar la dirección MAC asociada a una IP.

Neighbor Discovery (IPv6): Reemplaza a ARP en IPv6, utilizando mensajes ICMPv6 para localizar dispositivos vecinos.

1.3 Resumen
Los routers toman decisiones de envío basadas en su tabla de enrutamiento.

ARP es esencial para la comunicación en la misma red local (Capa 2).

ICMP permite verificar la conectividad y reportar errores de red.

Módulo 2: Direccionamiento IP (Capítulos 11 - 13)
2.1 IPv4 e IPv6
IPv4: Direcciones de 32 bits. Utiliza máscaras de subred para separar la parte de red de la de host.

IPv6: Direcciones de 128 bits. Elimina la necesidad de NAT y Broadcast, mejorando la eficiencia y escalabilidad.

2.2 Subredes y VLSM
La segmentación de red mejora el rendimiento y la seguridad.

Subnetting: División de una red grande en redes más pequeñas para reducir el tráfico de difusión.

VLSM: Uso de máscaras de longitud variable para asignar direcciones de forma exacta según la necesidad de cada subred, evitando el desperdicio de IPs.

2.3 Resumen
El diseño de direccionamiento debe ser jerárquico y escalable.

IPv6 utiliza prefijos (comúnmente /64) para identificar subredes de forma estándar.

Módulo 3: Protocolos de Aplicación (Capítulos 14 - 15)
3.1 Servicios Fundamentales
Los protocolos de aplicación permiten que el software del usuario interactúe con la red.

DNS: Servicio de resolución de nombres que traduce URLs en direcciones IP.

DHCP: Protocolo de configuración dinámica que asigna IPs automáticamente a los dispositivos.

HTTP/HTTPS: Estándares para la transferencia de datos en la web.

3.2 Intercambio de Datos
Cliente-Servidor: Un dispositivo central provee servicios a múltiples clientes.

P2P: Los dispositivos comparten recursos directamente sin necesidad de un servidor centralizado.

3.3 Resumen
La capa de aplicación es la interfaz directa entre el usuario y la infraestructura de red.

Los servicios como DHCP y DNS son críticos para la operatividad automática de una red moderna.

Módulo 4: Seguridad y Configuración (Capítulos 16 - 17)
4.1 Administración de Cisco IOS
La configuración de dispositivos se realiza mediante la interfaz de línea de comandos (CLI).

Archivos de sistema: Running-config (RAM) y Startup-config (NVRAM).

Verificación: Uso de comandos show para inspeccionar el estado de interfaces y configuraciones.

4.2 Aseguramiento de Dispositivos (Hardening)
Implementación de medidas para proteger el acceso administrativo.

Cifrado: Uso de passwords encriptados y el comando service password-encryption.

Acceso Remoto: Migración de Telnet hacia SSH para garantizar que las sesiones de administración estén cifradas.

Seguridad de Puertos: Protección básica contra accesos físicos no autorizados.

4.3 Resumen
La seguridad inicial comienza con credenciales fuertes y la desactivación de servicios no utilizados.

SSH es el estándar obligatorio para la gestión remota segura en equipos de infraestructura.

