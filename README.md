Network Scanner - Grupo CHM
Herramienta de reconocimiento de red local desarrollada en Python para la detección de hosts y servicios. Proyecto académico para la asignatura de Redes Avanzadas en INACAP.

Equipo de trabajo
Hernán Vera: Líder de Proyecto / Gestión de Git.

Matías Peralta: Desarrollador / Lógica de Sockets.

Claudio Zambra: Documentación Técnica.

Especificaciones Técnicas
El script opera bajo dos módulos de análisis:

Ping Sweep: Identificación de hosts activos mediante tráfico ICMP en el segmento de red.

Port Scan: Verificación de disponibilidad en servicios críticos (21, 22, 80, 443) mediante conexiones TCP.

Requisitos
Python 3.x

Privilegios de administrador para la gestión de sockets y comandos de red.

Instrucciones de Ejecución
Escaneo de red predeterminado (192.168.1.0/24):

Bash
python escaneoredes.py
Escaneo de host específico:

Bash
python escaneoredes.py -t <IP_OBJETIVO>
Nota sobre control de versiones: Antes de ejecutar, verifique que el archivo no contenga marcas de conflicto (<<<<<<<, =======).

Aviso Legal
Software con fines educativos. El uso de esta herramienta en redes sin autorización es responsabilidad exclusiva del usuario.

2026 | INACAP
