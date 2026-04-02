import subprocess
import socket
import argparse

parser = argparse.ArgumentParser(description="Escáner de Red - INACAP")
parser.add_argument("-t", "--target", help="Red base (ej: 192.168.1.)")
args = parser.parse_args()

def ping(host):
    comando = ["ping", "-n", "1", "-w", "500", host]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    return resultado.returncode == 0

def ping_sweep(red_base):
    hosts_activos = []
    print(f"\nIniciando escaneo en la red {red_base}X ...")

    for numero in range(1, 255):
        ip_objetivo = f"{red_base}{numero}"
        if ping(ip_objetivo):
            print(f"[+] Equipo activo: {ip_objetivo}")
            hosts_activos.append(ip_objetivo)

    return hosts_activos

def scan_port(host, port, timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        resultado = s.connect_ex((host, port))
        return resultado == 0
    except:
        return False
    finally:
        s.close()

def port_scan(host, ports, timeout=1):
    puertos_abiertos = []
    print(f"\nEscaneando puertos en {host}...")

    for puerto in ports:
        if scan_port(host, puerto, timeout):
            print(f"[+] Puerto {puerto} ABIERTO 🔓")
            puertos_abiertos.append(puerto)

    return puertos_abiertos