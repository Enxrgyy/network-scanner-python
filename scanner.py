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
