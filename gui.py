import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
from scanner import ping_sweep, port_scan, guardar_resultados

# 1. HERRAMIENTA PARA REDIRIGIR LA CONSOLA (Igual que antes)
class RedirigirConsola:
    def __init__(self, widget_texto):
        self.widget_texto = widget_texto
    def write(self, texto):
        self.widget_texto.insert(tk.END, texto)
        self.widget_texto.see(tk.END)
    def flush(self):
        pass

# 2. FUNCIÓN PARA INICIAR EL ESCANEO
def iniciar_escaneo():
    red = entrada_target.get()
    if not red.endswith("."):
        messagebox.showwarning("Error", "La red debe terminar en punto (ej: 192.168.1.)")
        return

    # Actualizar la caja de comando para que se vea como en Nmap
    entrada_comando.config(state=tk.NORMAL)
    entrada_comando.delete(0, tk.END)
    entrada_comando.insert(0, f"python scanner.py -t {red}")
    entrada_comando.config(state="readonly")

    # Limpiar paneles antes del nuevo escaneo
    consola_output.delete(1.0, tk.END)
    lista_hosts.delete(0, tk.END)
    boton_scan.config(state=tk.DISABLED)

    # Iniciar el hilo
    threading.Thread(target=ejecutar_logica, args=(red,)).start()

# 3. LÓGICA DE EJECUCIÓN
def ejecutar_logica(red):
    print(f"Starting Nmap-style scan at {red}0/24")
    print("...")
    open("resultados.txt", "w").close()

    # Ejecutar el barrido de ping
    equipos = ping_sweep(red)

    # Actualizar el Panel Izquierdo con los equipos encontrados
    for eq in equipos:
        # root.after asegura que la interfaz gráfica se actualice de forma segura desde este hilo
        root.after(0, lambda e=eq: lista_hosts.insert(tk.END, e))

    if equipos:
        puertos = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389, 8080]
        for equipo in equipos:
            print(f"\nScanning {equipo}")
            puertos_abiertos = port_scan(equipo, puertos)
            
            if puertos_abiertos:
                print(f"Discovered open ports on {equipo}:")
                for p in puertos_abiertos:
                    print(f" - {p}")
            else:
                print(f"No open ports found on {equipo}")
            
            guardar_resultados(equipo, puertos_abiertos)
    else:
        print("No hosts found.")

    print("\nScan completed. Results saved.")
    root.after(0, lambda: boton_scan.config(state=tk.NORMAL))

# ==========================================
# 4. DISEÑO DE LA INTERFAZ (ESTILO ZENMAP)
# ==========================================
root = tk.Tk()
root.title("Zenmap - Network Scanner (Grupo CHM)")
root.geometry("900x600") # Ventana más grande

# Usar un tema más moderno para los botones y pestañas
style = ttk.Style()
try:
    style.theme_use('clam') # Tema más limpio que el default de Windows
except:
    pass

# --- ZONA SUPERIOR (Target, Profile, Command) ---
frame_top = tk.Frame(root, padx=10, pady=10)
frame_top.pack(fill=tk.X)

# Fila 1: Target y Profile
tk.Label(frame_top, text="Target:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
entrada_target = tk.Entry(frame_top, width=20, font=("Arial", 10))
entrada_target.insert(0, "192.168.1.")
entrada_target.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_top, text="Profile:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky="w", padx=10)
combo_profile = ttk.Combobox(frame_top, values=["Intense scan", "Quick scan", "Ping sweep"], state="readonly", width=25)
combo_profile.current(1) # Seleccionar Quick scan por defecto
combo_profile.grid(row=0, column=3, padx=5, pady=5)

boton_scan = tk.Button(frame_top, text="Scan", font=("Arial", 10, "bold"), width=10, command=iniciar_escaneo)
boton_scan.grid(row=0, column=4, padx=15)

# Fila 2: Command
tk.Label(frame_top, text="Command:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5)
entrada_comando = tk.Entry(frame_top, font=("Consolas", 10), bg="#f0f0f0")
entrada_comando.insert(0, "python scanner.py")
entrada_comando.config(state="readonly")
entrada_comando.grid(row=1, column=1, columnspan=4, sticky="we", padx=5, pady=5)

# --- ZONA PRINCIPAL (Panel dividido) ---
# PanedWindow permite arrastrar el separador entre el panel izquierdo y derecho
paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Panel Izquierdo: Lista de Hosts
frame_left = tk.Frame(paned, relief=tk.SUNKEN, bd=1)
tk.Label(frame_left, text="Hosts", bg="#e0e0e0", anchor="w", font=("Arial", 9, "bold")).pack(fill=tk.X)
lista_hosts = tk.Listbox(frame_left, font=("Arial", 10), borderwidth=0)
lista_hosts.pack(fill=tk.BOTH, expand=True)
paned.add(frame_left, weight=1) # Ocupa 1 parte de la pantalla

# Panel Derecho: Pestañas (Notebook)
notebook = ttk.Notebook(paned)
paned.add(notebook, weight=4) # Ocupa 4 partes de la pantalla

# Pestaña 1: Nmap Output
tab_output = ttk.Frame(notebook)
notebook.add(tab_output, text="Nmap Output")
consola_output = scrolledtext.ScrolledText(tab_output, font=("Consolas", 10), bg="white", fg="black", borderwidth=0)
consola_output.pack(fill=tk.BOTH, expand=True)

# Pestaña 2: Ports / Hosts (Lista para el futuro)
tab_ports = ttk.Frame(notebook)
notebook.add(tab_ports, text="Ports / Hosts")
tk.Label(tab_ports, text="Aquí podrías agregar una tabla con los puertos detallados más adelante.").pack(pady=20)

# Pestaña 3: Topology (Lista para el futuro)
tab_topo = ttk.Frame(notebook)
notebook.add(tab_topo, text="Topology")

# Redirigir la consola a la pestaña principal
sys.stdout = RedirigirConsola(consola_output)

root.mainloop()
