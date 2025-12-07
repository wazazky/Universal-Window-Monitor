# Universal Window Monitor 👁️

Una herramienta de escritorio para Windows que monitorea el título de cualquier aplicación seleccionada y lo guarda en un archivo de texto (`ventana_actual.txt`). Ideal para mostrar "Música Actual" o "Proyecto Actual" en OBS o Streamlabs.

## 🚀 Características
- **Selector GUI:** Elige visualmente qué ventana monitorear.
- **System Tray:** Se minimiza a la bandeja del sistema (al lado del reloj) sin estorbar.
- **Limpieza de Texto:** Elimina sufijos molestos (ej: " - Google Chrome", " - Notepad").
- **Instancia Única:** Previene abrir el programa múltiples veces por error.
- **Ligero:** Escrito en Python nativo con `ctypes`.

## 🛠️ Instalación y Uso
1. Ve a la sección de [Releases](link-a-tus-releases) y descarga el `.exe`.
2. Ejecuta `UniversalMonitor.exe`.
3. Selecciona la ventana de la lista (ej: Spotify, YouTube en Chrome, etc.).
4. En OBS, agrega una fuente de texto (GDI+) y selecciona la opción "Leer desde archivo".
5. Apunta al archivo `ventana_actual.txt` generado.

## 💻 Desarrollo
Requisitos: Python 3.12+
