Network Scanner - Grupo CHM
Herramienta de reconocimiento de red local desarrollada en Python para la asignatura de Redes Avanzadas en INACAP.

Descripcion
Este proyecto consiste en crear un escáner de red tipo NMAP. La herramienta permite mapear la red local, identificar servicios activos y generar reportes automatizados mediante una arquitectura basada en la librería estándar de Python.

Funcionalidades clave
Escaneo rapido (Threading): Ejecución en paralelo para procesar múltiples puertos simultáneamente.

Host Discovery: Identificación de equipos activos mediante Ping Sweep (ICMP).

Service Mapping: Análisis de disponibilidad en puertos TCP comunes.

Identificacion de servicios: Banner grabbing para detectar versiones de software y nombres de servicios.

Interfaz Dual: Soporte para línea de comandos (CLI) y entorno gráfico (GUI) basado en Tkinter.

Requisitos y Dependencias
Python 3.8 o superior.

Sistemas Operativos: Windows o Linux.

Permisos: Requiere privilegios de administrador para la correcta ejecución de comandos de red.

Nota sobre dependencias: El proyecto utiliza exclusivamente la librería estándar de Python (socket, subprocess, threading, tkinter, argparse). No es necesario realizar instalaciones externas.

Uso de la Herramienta
Interfaz Grafica (Recomendado)
Para iniciar la versión visual con entorno gráfico:

Bash
python gui.py
Linea de Comandos (CLI)
Para ejecutar el escaneo directamente desde la terminal:

Bash
python scanner.py --network 192.168.1
Estructura del Proyecto
gui.py: Interfaz Gráfica de Usuario y manejo de eventos visuales.

scanner.py: Motor principal, lógica de red y soporte para terminal.

resultados.txt: Archivo de texto autogenerado con el reporte del último escaneo.

README.md: Documentación técnica del proyecto.

Objetivos
Detectar hosts activos mediante un barrido de red acelerado por hilos.

Identificar puertos abiertos y servicios asociados en los equipos detectados.

Asegurar una ejecución fluida mediante el manejo de procesos en segundo plano.

Automatizar la generación de reportes técnicos.

Equipo de Trabajo
Hernán Vera: Líder de Proyecto / Gestión de Git.

Matías Peralta: Desarrollador / Lógica de Sockets.

Claudio Zambra: Documentación Técnica.

2026 | INACAP
