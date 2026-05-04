# Ejercicio 12 

# ASISTENTE DE SEGURIDAD EN REDES

## ¿QUÉ ES?

Un programa en Python que simula 5 módulos de seguridad e infraestructura de redes empresariales.

## CÓMO USAR

### Requisitos
- Python 3.7 o superior
- Nada más (solo librerías estándar)

## QUÉ HACE

El programa ejecuta automáticamente estos 5 módulos:

### 1️. Generador de Comandos
- Crea comandos reales para Cisco, Fortinet y Huawei
- Valida IPs y VLANs (1-4094)
- Listo para copiar-pegar en un router

### 2️. Dashboard de Seguridad
- Muestra disponibilidad de nodos (UP/DOWN)
- CPU, memoria e interfaces de red
- Estado de túneles VPN
- Alertas de seguridad

### 3️. Análisis de Tráfico
- Simula flujos VoIP (SIP/RTP)
- Simula tráfico IoT (MQTT/Modbus)
- Calcula latencia, jitter y pérdida
- Calcula MOS (calidad de voz)

### 4️. Segmentación de VLANs
- Crea VLAN de Invitados (aislada)
- VLAN Corporativa (acceso total)
- VLAN IoT (restringida)
- VLAN Voice (prioridad alta)

### 5️. Detección de Ataques
- Simula ataques (port scan, DoS, SYN flood)
- Genera ACLs de bloqueo automático
- Registra todo en logs

## EJEMPLO DE SALIDA

Cuando ejecutas el programa, verás:

```
MÓDULO 1: CONFIGURACIÓN MULTI-VENDOR
✓ Comandos Cisco IOS generados
✓ Comandos Fortinet FortiOS generados
✓ Comandos Huawei VRP generados

MÓDULO 2: DASHBOARD DE POSTURA DE SEGURIDAD
✓ Router-Core       | 10.0.1.1      | Latencia: 15ms | Pérdida: 0%
✓ Switch-Main      | 10.0.1.5      | Latencia: 10ms | Pérdida: 0%
...

MÓDULO 3: ANALIZADOR DE TRÁFICO CRÍTICO
[FLUJO VoIP - RTP]
MOS Score: 4.25 (Excelente)
Latencia: 45ms | Jitter: 12ms | Pérdida: 0.5%

[FLUJO IoT - MQTT/Modbus]
Latencia: 25ms | Jitter: 8ms | Pérdida: 0.1%
...
```

## ESTRUCTURA DEL CÓDIGO

```
netops_orchestrator.py
│
├── ConfigGenerator()        → Genera comandos
├── SecurityDashboard()      → Muestra métricas
├── TrafficAnalyzer()        → Analiza tráfico
├── DynamicSegmentation()    → Crea VLANs
├── IncidentResponse()       → Detecta ataques
└── main()                   → Ejecuta todo
```

## VALIDACIÓN

* Genera comandos válidos para Cisco, Fortinet, Huawei
* Dashboard muestra métricas simuladas en tiempo real
* Analizador calcula latencia, jitter y MOS
* Crea 4 perfiles de VLAN con comandos de configuración
* Detecta ataques y genera ACLs de bloqueo
* Todos los eventos tienen timestamp y severidad  

## CLASES PRINCIPALES

- **ConfigGenerator:** Valida IPs/VLANs y genera comandos
- **SecurityDashboard:** Simula métricas de red
- **TrafficAnalyzer:** Calcula QoS (MOS, latencia, jitter)
- **DynamicSegmentation:** Crea perfiles de VLAN
- **IncidentResponse:** Detecta ataques y bloquea

## EJEMPLO RÁPIDO

```python
# Generar configuración Cisco
from netops_orchestrator import ConfigGenerator

gen = ConfigGenerator()
config = gen.cisco_config(10, "Corporativa", "Gi0/0/1", "10.10.1.1", "255.255.255.0")
print(config)
```
