# Desarrollo del Taller HSRP (Implementación en equipos físicos)

## Descripción general

El taller tuvo como fin implementar el protocolo **HSRP (Hot Standby Router Protocol)** a fin de dar redundancia a la puerta de enlace predeterminada de una red LAN. Este protocolo permite que dos routers trabajen juntos compartiendo una **IP virtual**, de forma que los hosts utilicen una única puerta de enlace lógica, independientemente de qué router esté activo.

Los routers **R1 y R3** fueron configurados como gateways redundantes para la red LAN en la topología propuesta, mientras que el router **R2** actuaba como router intermedio hacia otras redes.
---

## Configuración realizada

En todos los routers se hizo la configuración de direccionamiento IP según lo planificado en el laboratorio. Luego, se implementó HSRP en los routers **R1 y R3**, asignando una IP virtual compartida que serviría como puerta de enlace para los dispositivos finales.

La configuración hecha en los routers fue:

- Definir la dirección IP de las interfaces que se conectan a la LAN.
- Creación del grupo HSRP 
- Asignación de la IP virtual
- Prioridad de configuración
- Habilitar la opción `preempt` para poder recuperar el router con mayor prioridad


El mismo procedimiento fue aplicado tanto en **R1 como en R3**, designando a uno como **router activo** y al otro como **router en espera (standby)**.
---
## Funcionamiento esperado

Con HSRP configurado correctamente:

- Los hosts de la red LAN utilizan una **IP virtual** como su puerta de enlace predeterminada
- Uno de los routers pasa a modo **Active**, gestionando el tráfico
- El otro router se queda en modo **Standby** para hacerse cargo en cualquier momento
- En caso de que falle el router activo, el router de respaldo asume el control de forma automática sin que esto afecte a la conectividad de los hosts
---

## Verificación parcial

Se verificó el estado de las interfaces en los routers a través de comandos como:


Verificando que las interfaces estuviesen en estado **up/up**, lo que indica conectividad básica operativa.
---

## Limitaciones encontradas

No se pudieron realizar todas las pruebas del taller por limitaciones del hardware. Los routers físicos disponibles solo disponían de **dos interfaces de red**, pero la topología del laboratorio demandaba al menos **tres interfaces por router** para su correcta implementación.

Esta limitación impedía:

- Replicar completamente la topología planteada en Packet Tracer
- Crear todas las conexiones entre routers que sean necesarias
- Realizar pruebas completas de conmutación por error.
---

## Conclusión

A pesar de no haber completado la validación final, el taller permitió comprender el funcionamiento del protocolo HSRP y su importancia en la implementación de **redundancia de gateway** en redes LAN. Se logró configurar el protocolo en los routers R1 y R3, evidenciando su lógica de operación. Sin embargo, la limitación de interfaces en los equipos físicos impidió realizar pruebas completas de alta disponibilidad, destacando la diferencia entre entornos simulados y escenarios reales.
