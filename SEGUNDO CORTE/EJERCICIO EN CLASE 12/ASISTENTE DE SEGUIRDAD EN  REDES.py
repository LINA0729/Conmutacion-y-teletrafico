#!/usr/bin/env python3
"""
NetOps Security Orchestrator - Ejercicio en clase
Implementa 5 módulos de seguridad y configuración de redes
"""

import json
import random
import datetime
import math
from typing import List, Dict, Tuple

# ============================================================================
# MÓDULO 1: CONFIGURACIÓN MULTI-VENDOR
# ============================================================================

class ConfigGenerator:
    """Genera comandos de configuración para Cisco, Fortinet y Huawei"""
    
    @staticmethod
    def validate_vlan(vlan_id: int) -> bool:
        """Valida que VLAN esté en rango 1-4094"""
        return 1 <= vlan_id <= 4094
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Valida formato IP básico"""
        try:
            parts = ip.split('.')
            return len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts)
        except:
            return False
    
    @staticmethod
    def cisco_config(vlan_id: int, vlan_name: str, interface: str, ip: str, mask: str) -> str:
        """Genera comandos Cisco IOS para crear VLAN y configurar interfaz"""
        if not ConfigGenerator.validate_vlan(vlan_id):
            return f"ERROR: VLAN {vlan_id} fuera de rango 1-4094"
        if not ConfigGenerator.validate_ip(ip):
            return f"ERROR: IP {ip} inválida"
        
        config = f"""
! ===== CISCO IOS - VLAN {vlan_id} =====
configure terminal
vlan {vlan_id}
  name {vlan_name}
  exit
interface {interface}
  switchport mode access
  switchport access vlan {vlan_id}
  no shutdown
  exit
interface vlan {vlan_id}
  ip address {ip} {mask}
  no shutdown
  exit
ip access-list extended ACL_{vlan_name}
  permit ip 10.0.0.0 0.0.255.255 any
  deny ip any any log
  exit
end
"""
        return config
    
    @staticmethod
    def fortinet_config(policy_id: int, srcintf: str, dstintf: str, srcip: str, dstip: str, action: str = "accept") -> str:
        """Genera comandos FortiOS para reglas de firewall"""
        config = f"""
! ===== FORTINET FortiOS - Policy {policy_id} =====
config firewall policy
  edit {policy_id}
    set name "Policy_{policy_id}"
    set srcintf "{srcintf}"
    set dstintf "{dstintf}"
    set srcaddr "all"
    set dstaddr "all"
    set action {action}
    set schedule "always"
    set service "ALL"
    set nat enable
    set logtraffic all
  next
end
config system interface
  edit "port1"
    set ip {srcip} 255.255.255.0
    set allowaccess ping http https ssh
  next
end
"""
        return config
    
    @staticmethod
    def huawei_config(vlan_id: int, vlan_name: str, ip: str) -> str:
        """Genera comandos Huawei VRP para VLAN"""
        if not ConfigGenerator.validate_vlan(vlan_id):
            return f"ERROR: VLAN {vlan_id} fuera de rango 1-4094"
        
        config = f"""
! ===== HUAWEI VRP - VLAN {vlan_id} =====
system-view
vlan {vlan_id}
  name {vlan_name}
  quit
interface vlanif {vlan_id}
  ip address {ip} 255.255.255.0
  quit
acl number 3000
  rule 5 permit ip source 10.0.0.0 0.0.255.255
  rule 10 deny ip source any
  quit
"""
        return config


# ============================================================================
# MÓDULO 2: DASHBOARD DE POSTURA DE SEGURIDAD
# ============================================================================

class SecurityDashboard:
    """Genera métricas de seguridad en tiempo real (simuladas)"""
    
    @staticmethod
    def simulate_node_availability() -> Dict:
        """Simula disponibilidad de nodos (ping, latencia)"""
        nodes = {
            "Router-Core": {"ip": "10.0.1.1", "status": "UP", "latency_ms": random.randint(5, 25), "loss_pct": random.randint(0, 2)},
            "Switch-Main": {"ip": "10.0.1.5", "status": "UP", "latency_ms": random.randint(3, 15), "loss_pct": 0},
            "FW-Fortinet": {"ip": "192.168.1.1", "status": "UP", "latency_ms": random.randint(10, 30), "loss_pct": random.randint(0, 1)},
            "Server-IoT": {"ip": "10.50.1.10", "status": random.choice(["UP", "UP", "UP", "DOWN"]), "latency_ms": random.randint(20, 50), "loss_pct": random.randint(0, 5)},
        }
        return nodes
    
    @staticmethod
    def simulate_resource_usage() -> Dict:
        """Simula uso de CPU, memoria e interfaces (SNMP)"""
        resources = {
            "Router-Core": {"cpu_pct": random.randint(15, 45), "mem_pct": random.randint(30, 60), "tx_bps": random.randint(1000000, 5000000), "rx_bps": random.randint(1000000, 5000000)},
            "Switch-Main": {"cpu_pct": random.randint(5, 25), "mem_pct": random.randint(20, 50), "tx_bps": random.randint(5000000, 15000000), "rx_bps": random.randint(5000000, 15000000)},
            "FW-Fortinet": {"cpu_pct": random.randint(25, 65), "mem_pct": random.randint(40, 75), "tx_bps": random.randint(2000000, 8000000), "rx_bps": random.randint(2000000, 8000000)},
        }
        return resources
    
    @staticmethod
    def simulate_vpn_tunnels() -> Dict:
        """Simula estado de túneles VPN"""
        tunnels = {
            "VPN-Datacenter": {"status": "active", "bytes_tx": random.randint(1000000, 10000000), "uptime_hours": random.randint(10, 500)},
            "VPN-Remote-Office": {"status": "active", "bytes_tx": random.randint(500000, 5000000), "uptime_hours": random.randint(5, 200)},
            "VPN-Partner": {"status": "inactive", "bytes_tx": 0, "uptime_hours": 0},
        }
        return tunnels
    
    @staticmethod
    def simulate_alerts() -> List[Dict]:
        """Genera alertas y eventos de seguridad"""
        alerts = [
            {"timestamp": datetime.datetime.now().isoformat(), "severity": "INFO", "message": "Interfaz eth0 UP", "source": "Router-Core"},
            {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat(), "severity": "WARNING", "message": "CPU > 60% en FW-Fortinet", "source": "FW-Fortinet"},
            {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=15)).isoformat(), "severity": "CRITICAL", "message": "Pérdida de paquetes > 5% en Server-IoT", "source": "Server-IoT"},
            {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=30)).isoformat(), "severity": "INFO", "message": "VPN-Datacenter restablecida", "source": "VPN-Datacenter"},
        ]
        return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)
    
    @staticmethod
    def display_dashboard():
        """Muestra el dashboard completo"""
        print("\n" + "="*80)
        print("MÓDULO 2: DASHBOARD DE POSTURA DE SEGURIDAD".center(80))
        print("="*80)
        
        # Disponibilidad de nodos
        print("\n[DISPONIBILIDAD DE NODOS]")
        nodes = SecurityDashboard.simulate_node_availability()
        for node, data in nodes.items():
            status_icon = "✓" if data["status"] == "UP" else "✗"
            print(f"  {status_icon} {node:20s} | IP: {data['ip']:15s} | Latencia: {data['latency_ms']:3d}ms | Pérdida: {data['loss_pct']}%")
        
        # Uso de recursos
        print("\n[CONSUMO DE RECURSOS (SNMP)]")
        resources = SecurityDashboard.simulate_resource_usage()
        for device, data in resources.items():
            print(f"  {device:20s} | CPU: {data['cpu_pct']:2d}% | MEM: {data['mem_pct']:2d}% | TX: {data['tx_bps']:>10d} bps | RX: {data['rx_bps']:>10d} bps")
        
        # VPN
        print("\n[ESTADO DE TÚNELES VPN]")
        vpns = SecurityDashboard.simulate_vpn_tunnels()
        for tunnel, data in vpns.items():
            status_icon = "🔒" if data["status"] == "active" else "❌"
            print(f"  {status_icon} {tunnel:25s} | Estado: {data['status']:8s} | Uptime: {data['uptime_hours']:3d}h | Bytes TX: {data['bytes_tx']:>10d}")
        
        # Alertas
        print("\n[EVENTOS Y ALERTAS]")
        alerts = SecurityDashboard.simulate_alerts()
        for alert in alerts[:5]:
            severity_symbol = {"INFO": "ℹ", "WARNING": "⚠", "CRITICAL": "🔴"}
            print(f"  {severity_symbol.get(alert['severity'], '?')} [{alert['severity']:8s}] {alert['timestamp']} | {alert['message']}")


# ============================================================================
# MÓDULO 3: ANALIZADOR DE TRÁFICO CRÍTICO
# ============================================================================

class TrafficAnalyzer:
    """Analiza tráfico de IoT, VoIP y calcula QoS"""
    
    @staticmethod
    def calculate_mos(latency_ms: float, jitter_ms: float, loss_pct: float) -> float:
        """
        Calcula MOS (Mean Opinion Score) usando E-Model simplificado
        Rango: 1.0 (peor) a 5.0 (mejor)
        """
        R = 93.2 - (latency_ms / 10) - (jitter_ms * 2) - (loss_pct * 2.5)
        R = max(0, min(100, R))
        if R < 0:
            mos = 1
        elif R < 6.5:
            mos = 1
        else:
            mos = 4.45 - (R - 60) * 0.007
        return round(max(1, min(5, mos)), 2)
    
    @staticmethod
    def simulate_voip_stream() -> Dict:
        """Simula un flujo RTP de VoIP"""
        latency = random.randint(30, 150)
        jitter = random.randint(5, 50)
        loss = random.uniform(0, 5)
        mos = TrafficAnalyzer.calculate_mos(latency, jitter, loss)
        
        return {
            "stream_type": "VoIP (SIP/RTP)",
            "source_ip": "10.20.1.50",
            "dest_ip": "10.30.1.100",
            "latency_ms": latency,
            "jitter_ms": jitter,
            "loss_pct": round(loss, 2),
            "mos": mos,
            "mos_quality": "Excelente" if mos >= 4 else "Buena" if mos >= 3.5 else "Aceptable" if mos >= 3 else "Pobre"
        }
    
    @staticmethod
    def simulate_iot_traffic() -> Dict:
        """Simula tráfico IoT (Modbus/MQTT)"""
        latency = random.randint(10, 50)
        jitter = random.randint(2, 20)
        loss = random.uniform(0, 2)
        
        return {
            "stream_type": "IoT (MQTT/Modbus)",
            "source_ip": "10.50.1.20",
            "dest_ip": "10.50.10.1",
            "latency_ms": latency,
            "jitter_ms": jitter,
            "loss_pct": round(loss, 2),
            "dscp": "EF (46) - VoIP/IoT Priority",
            "note": "Tráfico industrial prioritario"
        }
    
    @staticmethod
    def display_traffic_analysis():
        """Muestra análisis de tráfico"""
        print("\n" + "="*80)
        print("MÓDULO 3: ANALIZADOR DE TRÁFICO CRÍTICO".center(80))
        print("="*80)
        
        # VoIP
        print("\n[FLUJO VoIP - RTP]")
        voip = TrafficAnalyzer.simulate_voip_stream()
        print(f"  Tipo: {voip['stream_type']}")
        print(f"  Origen → Destino: {voip['source_ip']} → {voip['dest_ip']}")
        print(f"  Latencia: {voip['latency_ms']}ms | Jitter: {voip['jitter_ms']}ms | Pérdida: {voip['loss_pct']}%")
        print(f"  MOS Score: {voip['mos']} ({voip['mos_quality']})")
        
        if voip['latency_ms'] > 150:
            print(f"  ⚠️  ALERTA: Latencia > 150ms (umbral VoIP)")
        if voip['loss_pct'] > 1:
            print(f"  ⚠️  ALERTA: Pérdida > 1%")
        
        # IoT
        print("\n[FLUJO IoT - MQTT/Modbus]")
        iot = TrafficAnalyzer.simulate_iot_traffic()
        print(f"  Tipo: {iot['stream_type']}")
        print(f"  Origen → Destino: {iot['source_ip']} → {iot['dest_ip']}")
        print(f"  Latencia: {iot['latency_ms']}ms | Jitter: {iot['jitter_ms']}ms | Pérdida: {iot['loss_pct']}%")
        print(f"  DSCP: {iot['dscp']}")
        print(f"  Nota: {iot['note']}")
        
        # Priorización
        print("\n[PRIORIZACIÓN DE TRÁFICO]")
        print(f"  EF (46):  VoIP/IoT Priority      ← {voip['stream_type']}")
        print(f"  CS0 (0):  Best-effort/Admin      ← Tráfico general")
        print(f"  Decisión: Se prioriza IoT y VoIP sobre tráfico administrativo")


# ============================================================================
# MÓDULO 4: GESTIÓN DE SEGMENTACIÓN DINÁMICA (VLANs)
# ============================================================================

class DynamicSegmentation:
    """Crea y gestiona perfiles de VLAN"""
    
    @staticmethod
    def create_vlan_profile(name: str, vlan_id: int, vlan_type: str, description: str) -> Dict:
        """Crea un perfil de VLAN"""
        profiles = {
            "Invitados": {
                "vlan_id": 100,
                "name": "Guest-VLAN",
                "access": ["Internet only"],
                "deny": ["LAN access", "Server access"],
                "cos": 0,
                "dscp": "CS0",
            },
            "Corporativa": {
                "vlan_id": 10,
                "name": "Corp-VLAN",
                "access": ["All corporate resources", "File servers", "Email", "Applications"],
                "deny": ["Guest networks"],
                "cos": 3,
                "dscp": "AF31",
            },
            "IoT": {
                "vlan_id": 50,
                "name": "IoT-VLAN",
                "access": ["IoT Gateway", "MQTT Broker", "Data collector"],
                "deny": ["User workstations", "Admin networks"],
                "cos": 5,
                "dscp": "EF",
            },
            "Voice": {
                "vlan_id": 20,
                "name": "Voice-VLAN",
                "access": ["PBX system", "PSTN gateway", "VoIP phones"],
                "deny": ["Data traffic", "Best-effort"],
                "cos": 5,
                "dscp": "EF (46)",
            },
        }
        return profiles.get(vlan_type, {})
    
    @staticmethod
    def generate_port_config(vlan_type: str, port: str = "Gi0/0/1", vendor: str = "cisco") -> str:
        """Genera configuración de puerto para acceso/trunk"""
        profile = DynamicSegmentation.create_vlan_profile(vlan_type, 1, vlan_type, "")
        vlan_id = profile.get("vlan_id", 1)
        
        if vendor.lower() == "cisco":
            config = f"""
! Puerto acceso para {vlan_type}
interface {port}
  switchport mode access
  switchport access vlan {vlan_id}
  no shutdown
  exit
"""
        elif vendor.lower() == "huawei":
            config = f"""
! Puerto acceso para {vlan_type}
interface {port}
  port link-type access
  port default vlan {vlan_id}
  undo shutdown
  quit
"""
        else:
            config = f"# Vendor {vendor} no soportado"
        
        return config
    
    @staticmethod
    def display_segmentation():
        """Muestra perfiles de VLAN y configuración"""
        print("\n" + "="*80)
        print("MÓDULO 4: GESTIÓN DE SEGMENTACIÓN DINÁMICA".center(80))
        print("="*80)
        
        vlan_types = ["Invitados", "Corporativa", "IoT", "Voice"]
        
        for vlan_type in vlan_types:
            profile = DynamicSegmentation.create_vlan_profile(vlan_type, 1, vlan_type, "")
            print(f"\n[VLAN: {vlan_type.upper()}]")
            print(f"  ID: {profile['vlan_id']:4d} | Nombre: {profile['name']:20s} | CoS: {profile['cos']} | DSCP: {profile['dscp']}")
            print(f"  ✓ Acceso permitido: {', '.join(profile['access'])}")
            print(f"  ✗ Acceso denegado: {', '.join(profile['deny'])}")
            
            # Mostrar comandos de configuración
            cisco_cfg = DynamicSegmentation.generate_port_config(vlan_type, "Gi0/0/1", "cisco")
            print(f"  [Cisco] {cisco_cfg.strip().split(chr(10))[1].strip()}")


# ============================================================================
# MÓDULO 5: RESPUESTA ANTE INCIDENTES (ACLs DINÁMICAS)
# ============================================================================

class IncidentResponse:
    """Detecta ataques y genera ACLs de bloqueo automático"""
    
    @staticmethod
    def simulate_attack() -> Dict:
        """Simula diferentes tipos de ataques"""
        attack_types = {
            "port_scan": {
                "type": "Port Scan (Nmap-like)",
                "attacker_ip": "192.168.1.105",
                "target_ips": ["10.0.1.1", "10.0.1.2", "10.0.1.3"],
                "protocol": "TCP",
                "packets_per_sec": 250,
                "threshold": 100,
                "action": "EXCEEDED",
            },
            "dos_udp": {
                "type": "UDP Flood (DoS)",
                "attacker_ip": "203.0.113.50",
                "target_ip": "10.0.1.5",
                "protocol": "UDP",
                "packets_per_sec": 8000,
                "threshold": 1000,
                "action": "EXCEEDED",
            },
            "syn_flood": {
                "type": "SYN Flood (DoS)",
                "attacker_ip": "198.51.100.25",
                "target_ip": "10.0.1.1",
                "protocol": "TCP",
                "packets_per_sec": 5000,
                "threshold": 500,
                "action": "EXCEEDED",
            },
        }
        
        return random.choice(list(attack_types.values()))
    
    @staticmethod
    def generate_blocking_acl(attacker_ip: str, interface: str = "eth0", vendor: str = "cisco") -> str:
        """Genera ACL extendida para bloquear atacante"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if vendor.lower() == "cisco":
            acl = f"""
! ACL de Bloqueo Automático - Incidente {timestamp}
ip access-list extended BLOCK_ATTACK
  deny ip host {attacker_ip} any log
  deny ip any host {attacker_ip} log
  permit ip any any
  exit
interface {interface}
  ip access-group BLOCK_ATTACK in
  exit
"""
        elif vendor.lower() == "huawei":
            acl = f"""
! ACL de Bloqueo Automático - Incidente {timestamp}
acl number 3100
  rule 5 deny ip source {attacker_ip}
  rule 10 deny ip destination {attacker_ip}
  rule 20 permit ip source any
  quit
interface {interface}
  traffic-filter inbound acl 3100
  quit
"""
        elif vendor.lower() == "fortinet":
            acl = f"""
! Bloqueo FortiOS - Incidente {timestamp}
config firewall address
  edit "ATTACKER_BLOCK"
    set subnet {attacker_ip} 255.255.255.255
  next
end
config firewall policy
  edit 1
    set srcaddr "ATTACKER_BLOCK"
    set action deny
    set logtraffic all
  next
end
"""
        else:
            acl = f"# Vendor {vendor} no soportado"
        
        return acl
    
    @staticmethod
    def display_incident_response():
        """Muestra detección de ataque y respuesta automática"""
        print("\n" + "="*80)
        print("MÓDULO 5: RESPUESTA ANTE INCIDENTES".center(80))
        print("="*80)
        
        attack = IncidentResponse.simulate_attack()
        timestamp = datetime.datetime.now().isoformat()
        
        print(f"\n[DETECCIÓN DE ATAQUE]")
        print(f"  Timestamp: {timestamp}")
        print(f"  Tipo: {attack['type']}")
        print(f"  IP Atacante: {attack['attacker_ip']}")
        
        if "target_ips" in attack:
            print(f"  Targets: {', '.join(attack['target_ips'])}")
        elif "target_ip" in attack:
            print(f"  Target: {attack['target_ip']}")
        
        print(f"  Protocolo: {attack['protocol']}")
        print(f"  Paquetes/seg: {attack['packets_per_sec']} (umbral: {attack['threshold']})")
        print(f"  Estado: {attack['action']} ⚠️  ALERTA CRÍTICA")
        
        print(f"\n[RESPUESTA AUTOMÁTICA]")
        print(f"  Acción: Generar ACL de bloqueo")
        print(f"  Estado: EN PROGRESO...")
        
        # Generar ACLs para diferentes vendors
        for vendor in ["cisco", "huawei", "fortinet"]:
            acl = IncidentResponse.generate_blocking_acl(attack['attacker_ip'], "eth0", vendor)
            print(f"\n[ACL - {vendor.upper()}]")
            print(acl)
        
        print(f"\n[LOG DE INCIDENTE]")
        print(f"  Evento: Attack detected from {attack['attacker_ip']}")
        print(f"  Severidad: CRITICAL")
        print(f"  Acción: ACL aplicada y registrada")
        print(f"  Status: IP {attack['attacker_ip']} bloqueada en todas las interfaces")


# ============================================================================
# MAIN: EJECUTA TODOS LOS MÓDULOS
# ============================================================================

def main():
    """Ejecuta demostración de todos los 5 módulos"""
    
    print("\n" + "="*80)
    print("NetOps Security Orchestrator - DEMOSTRACIÓN COMPLETA".center(80))
    print("="*80)
    
    # ────────────────────────────────────────────────────────────────────────
    # MÓDULO 1: CONFIGURACIÓN MULTI-VENDOR
    # ────────────────────────────────────────────────────────────────────────
    print("\n" + "="*80)
    print("MÓDULO 1: CONFIGURACIÓN MULTI-VENDOR".center(80))
    print("="*80)
    
    generator = ConfigGenerator()
    
    # Cisco
    print("\n[CISCO IOS]")
    cisco_cfg = generator.cisco_config(10, "Corporativa", "Gi0/0/1", "10.10.1.1", "255.255.255.0")
    print(cisco_cfg)
    
    # Fortinet
    print("\n[FORTINET FortiOS]")
    fortinet_cfg = generator.fortinet_config(1, "port1", "port2", "192.168.1.1", "10.0.0.0")
    print(fortinet_cfg)
    
    # Huawei
    print("\n[HUAWEI VRP]")
    huawei_cfg = generator.huawei_config(20, "Voice-VLAN", "10.20.1.254")
    print(huawei_cfg)
    
    # ────────────────────────────────────────────────────────────────────────
    # MÓDULO 2: DASHBOARD
    # ────────────────────────────────────────────────────────────────────────
    SecurityDashboard.display_dashboard()
    
    # ────────────────────────────────────────────────────────────────────────
    # MÓDULO 3: ANALIZADOR DE TRÁFICO
    # ────────────────────────────────────────────────────────────────────────
    TrafficAnalyzer.display_traffic_analysis()
    
    # ────────────────────────────────────────────────────────────────────────
    # MÓDULO 4: SEGMENTACIÓN DINÁMICA
    # ────────────────────────────────────────────────────────────────────────
    DynamicSegmentation.display_segmentation()
    
    # ────────────────────────────────────────────────────────────────────────
    # MÓDULO 5: RESPUESTA ANTE INCIDENTES
    # ────────────────────────────────────────────────────────────────────────
    IncidentResponse.display_incident_response()
    
    # ────────────────────────────────────────────────────────────────────────
    # RESUMEN FINAL
    # ────────────────────────────────────────────────────────────────────────
    print("\n" + "="*80)
    print("RESUMEN DE EJECUCIÓN".center(80))
    print("="*80)
    print("""
    ✓ Módulo 1: Comandos multi-vendor generados y validados
    ✓ Módulo 2: Dashboard de postura con métricas simuladas
    ✓ Módulo 3: Análisis de tráfico VoIP/IoT con QoS (MOS)
    ✓ Módulo 4: Segmentación VLAN dinámicas (Guest, Corp, IoT, Voice)
    ✓ Módulo 5: Detección de ataque y ACLs de bloqueo automático
    
    Todos los eventos registrados con timestamps y severidad.
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
