# Universal Window Monitor 👁️

Una herramienta de escritorio para Windows que monitorea el título de cualquier aplicación seleccionada y lo guarda en un archivo de texto (`ventana_actual.txt`). Ideal para mostrar "Música Actual" o "Proyecto Actual" en OBS o Streamlabs.

## 🚀 Características
- **Selector GUI:** Elige visualmente qué ventana monitorear.
- **System Tray:** Se minimiza a la bandeja del sistema (al lado del reloj) sin estorbar.
- **Limpieza de Texto:** Elimina sufijos molestos (ej: " - Google Chrome", " - Notepad").
- **Instancia Única:** Previene abrir el programa múltiples veces por error.
- **Ligero:** Escrito en Python nativo con `ctypes`.

## 🛠️ Instalación y Uso

No es necesario instalar Python. Solo descarga el ejecutable:

1.  Ve a la sección de **[Releases](https://github.com/wazazky/Universal-Window-Monitor/releases/latest)**.
2.  Descarga el archivo `UniversalMonitor.exe` (bajo la sección "Assets").
3.  Ejecútalo (Windows puede preguntar si confías en el archivo, dale a "Más información" > "Ejecutar de todas formas").
4.  Selecciona la ventana que quieras monitorear.

## 💻 Desarrollo
Requisitos: Python 3.12+
