import threading
import subprocess
import socket
import argparse
import os

# Configuración de argumentos de línea de comandos 
def configurar_argumentos():
    parser = argparse.ArgumentParser(description="Escáner de Red - INACAP")
    parser.add_argument("-t", "--target", help="Red base (ej: 192.168.1.)", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = configurar_argumentos()
    print(f"--- INICIANDO ESCÁNER EN LA RED: {args.target} ---")

def ping_host(ip):
    # Ajuste de comando según el Sistema Operativo del escáner [cite: 43]
    param = "-n" if os.name == "nt" else "-c"
    comando = ["ping", param, "1", "-w", "500", ip]
    
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Lógica de detección de SO (Puntos Extra) 
    so = "Desconocido"
    if resultado.returncode == 0:
        if "ttl=64" in resultado.stdout.lower():
            so = "Linux/Unix"
        elif "ttl=128" in resultado.stdout.lower():
            so = "Windows"
        return True, so
    return False, so

def ejecutar_ping_sweep(red_base):
    hosts_activos = []
    threads = []

    def escaneo_rapido(ip):
        activo, so = ping_host(ip)
        if activo:
            print(f"[✔] Host activo: {ip} | Posible SO: {so}")
            hosts_activos.append((ip, so))

    for i in range(1, 255):
        ip_actual = f"{red_base}{i}" if red_base.endswith(".") else f"{red_base}.{i}"
        t = threading.Thread(target=escaneo_rapido, args=(ip_actual,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    return hosts_activos

def obtener_banner(s, puerto):
    # Intento de comunicación para obtener el banner del servicio [cite: 55]
    try:
        if puerto == 80:
            s.send(b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        return banner.split("\n")[0] if banner else "Sin respuesta"
    except:
        return "No disponible"

def escanear_puertos(ip, lista_puertos):
    puertos_abiertos = []
    
    def conectar(p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((ip, p)) == 0:
            servicio = obtener_banner(s, p)
            print(f"    [+] Puerto {p} ABIERTO | Servicio: {servicio}")
            puertos_abiertos.append({"puerto": p, "servicio": servicio})
        s.close()

    threads = []
    for p in lista_puertos:
        t = threading.Thread(target=conectar, args=(p,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    return puertos_abiertos

def guardar_reporte(datos):
    with open("resultados.txt", "w", encoding="utf-8") as f:
        f.write("REPORTE FINAL DE ESCANEO - INACAP\n")
        f.write("="*40 + "\n")
        for host in datos:
            f.write(f"IP: {host['ip']} | SO: {host['so']}\n")
            if host['puertos']:
                for p in host['puertos']:
                    f.write(f"  [+] Puerto {p['puerto']} ({p['servicio']})\n")
            else:
                f.write("  [-] No se detectaron puertos abiertos en la lista común.\n")
            f.write("-" * 40 + "\n")
# Integración en el bloque principal
import time # Añadir al inicio del archivo

if __name__ == "__main__":
    args = configurar_argumentos()
    
    # Asegurar que la red termine en punto
    red_objetivo = args.target if args.target.endswith(".") else f"{args.target}."
    
    activos = ejecutar_ping_sweep(red_objetivo)
    
    if activos:
        # Lista de puertos sugerida por la guía [cite: 57]
        puertos_test = [21, 22, 23, 80, 443, 445, 3389]
        resultados_finales = []
        
        print(f"\n--- Iniciando escaneo de puertos para {len(activos)} equipos ---")
        
        for ip, so in activos:
            print(f"\n🔍 Analizando: {ip} ({so})")
            # Escanear puertos para CADA host detectado [cite: 26]
            p_encontrados = escanear_puertos(ip, puertos_test)
            
            resultados_finales.append({
                "ip": ip, 
                "so": so, 
                "puertos": p_encontrados
            })
            
            # Pequeña pausa para no saturar el socket de red
            time.sleep(0.5)
        
        # Guardar todo el reporte final [cite: 59]
        guardar_reporte(resultados_finales)
        print(f"\n✅ Proceso terminado. Resultados de {len(activos)} equipos guardados.")
    else:
        print("\n❌ No se encontraron hosts activos en esa red.")