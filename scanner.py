import threading
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
    hilos = []

    def scan(puerto):
        if scan_port(host, puerto, timeout):
            servicio = detectar_servicio(host, puerto)
            print(f"[+] Puerto {puerto} ABIERTO 🔓 | Servicio: {servicio}")
            puertos_abiertos.append(puerto)

    for puerto in ports:
        hilo = threading.Thread(target=scan, args=(puerto,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return puertos_abiertos

def detectar_servicio(host, puerto):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((host, puerto))

        # 🔥 Si es HTTP, enviamos petición
        if puerto == 80:
            s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")

        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()

        if banner:
            return banner.split("\n")[0]  # solo primera línea
        else:
            return "Sin respuesta"

    except:
        return "Desconocido"

if __name__ == "__main__":
    print("--- INICIANDO ESCÁNER DE RED INACAP ---")

    # Valor por defecto seguro
    mi_red = "192.168.1."

    # Si el usuario pasa argumento, lo usa
    if args.target is not None:
        mi_red = args.target

    equipos_activos = ping_sweep(mi_red)

    if equipos_activos:
        primer_equipo = equipos_activos[0]
        puertos = [21, 22, 80, 443]
        port_scan(primer_equipo, puertos)
    else:
        print("No se encontraron equipos activos.")
        