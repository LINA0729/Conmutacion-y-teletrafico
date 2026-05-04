# Ejercicio 12 

## Descripción del proyecto

**ASISTENTE DE SEGURIDAD DE REDES** es una aplicación modular que simula las capacidades de un orquestador de seguridad y gestión de infraestructura de redes empresariales convergentes (voz, video, datos e IoT).

El sistema actúa como asistente para ingenieros de infraestructura, cubriendo desde la generación de configuraciones multi-vendor hasta la respuesta automática ante incidentes de seguridad.

---

## Objetivo general

Diseñar e implementar, a partir de un prompt base, un software extensible que permita:

1. Generar plantillas de configuración para dispositivos Cisco, Fortinet y Huawei.
2. Visualizar dashboards de disponibilidad, rendimiento y eventos en tiempo real.
3. Analizar tráfico de voz, video e IoT con métricas de QoS (jitter, latencia, MOS).
4. Gestionar VLAN Voice y segmentos de red con tráfico sensible al retardo.
5. Aplicar ACLs dinámicas como respuesta automática ante tráfico anómalo.

---

## Módulos operativos

### Módulo 1 — Configuración Multi-Vendor
Generador automático de comandos para **Fortinet FortiOS**, **Cisco IOS/IOS-XE** y **Huawei VRP**.

Genera configuraciones reales para:
- Reglas de firewall y políticas de acceso
- Túneles IPsec / SSL-VPN
- Hardening de interfaces (deshabilitar servicios inseguros)
- VLAN voice con CoS/DSCP
- ACLs estándar y extendidas
- QoS: DSCP marking, traffic policing

**Uso:**
```bash
python -m modules.config_generator --vendor cisco --feature vlan_voice --vlan-id 10 --ip-range 192.168.10.0/24
```

---

### Módulo 2 — Dashboard de Postura de Seguridad
Interfaz visual (web o CLI) con actualización en tiempo real cada 5-30 segundos.

Métricas mostradas:
- Disponibilidad de nodos (ICMP/ping simulado): latencia y pérdida de paquetes
- Recursos de dispositivos (SNMP simulado): CPU %, memoria %, tráfico de interfaces
- Estado de túneles VPN: activo/inactivo, uptime, bytes transferidos
- Registro de eventos con nivel de severidad (INFO / WARNING / CRITICAL)

**Uso:**
```bash
python -m modules.dashboard --mode web --port 8080
# o en modo CLI:
python -m modules.dashboard --mode cli
```

---

### Módulo 3 — Analizador de Tráfico Crítico (IoT/Edge)
Captura y analiza paquetes sintéticos generados con Scapy.

Tipos de tráfico simulados:
- **VoIP:** SIP + RTP (codec G.711)
- **Video:** RTSP/RTP
- **IoT industrial:** Modbus TCP, MQTT
- **Administrativo:** SSH, HTTPS

Métricas calculadas:
- Latencia (ms), Jitter (ms), Pérdida de paquetes (%)
- **MOS estimado** para VoIP mediante E-Model simplificado
- Alertas automáticas si latencia VoIP > 150 ms o pérdida > 1%

**Uso:**
```bash
python -m modules.traffic_analyzer --type voip --duration 60 --report json
```

---

### Módulo 4 — Gestión de Segmentación Dinámica
Crea y gestiona VLANs segmentadas con políticas de aislamiento automáticas.

Perfiles preconfigurados:
| VLAN | ID | Política | Prioridad |
|------|----|----------|-----------|
| Voice | 10 | Solo PBX y PSTN GW | CoS 5 / DSCP EF (46) |
| Corporativa | 20 | Acceso completo + ACLs | DSCP CS2 |
| IoT | 30 | Solo servidores autorizados | DSCP EF (46) |
| Invitados | 40 | Solo internet, aislada | DSCP CS0 |

Genera comandos de puertos acceso/trunk para Cisco y Huawei listos para copiar.

**Uso:**
```bash
python -m modules.vlan_manager --create voice --vlan-id 10 --vendor cisco
```

---

### Módulo 5 — Respuesta ante Incidentes (ACLs Dinámicas)
Sistema de detección y bloqueo automático ante tráfico anómalo simulado.

Ataques simulados:
- Escaneo de puertos (tipo Nmap sintético)
- Flood UDP/ICMP (DoS simulado)
- SYN flood / conexiones repetidas

Flujo de respuesta:
1. Detección por umbral (paquetes/segundo por IP origen)
2. Generación automática de ACL extendida de bloqueo
3. Aplicación en la interfaz simulada afectada
4. Registro en base de datos (IP, protocolo, timestamps, evidencia)
5. Opción de revisión manual, aprobación o reversión

**Uso:**
```bash
python -m modules.incident_response --simulate dos --target 192.168.1.100 --auto-block
```

---

## Criterios de evaluación

- [x] Comandos válidos generados para Cisco y Fortinet/Huawei
- [x] Dashboard con métricas en tiempo real (datos sintéticos)
- [x] Análisis de latencia/jitter/MOS en flujo RTP simulado
- [x] VLANs Voice, IoT y Corporativa con comandos generados
- [x] Detección de DoS simulado con ACL de bloqueo automática
- [x] Todos los eventos registrados en BD con timestamps
