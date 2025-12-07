import os
import sys
import time
import threading
import ctypes
import tkinter as tk
from tkinter import messagebox
from ctypes import wintypes
from pystray import Icon, MenuItem as item, Menu
from PIL import Image, ImageDraw

# --- CONFIGURACIÓN ---
FILENAME = "ventana_actual.txt"
CHECK_INTERVAL = 1
TEXTO_VENTANA_CERRADA = "Ventana cerrada"
TEXTO_SELECCIONANDO = "Seleccionando..."
MUTEX_NAME = "Global\\UniversalMonitor_Wazazky_Unique_ID" # ID Único en memoria

SUFIJOS_LIMPIEZA = [
    " - Google Chrome", " - YouTube", " - Mozilla Firefox", 
    " - Opera", " - Brave", " - Edge", " - Notepad", " - Bloc de notas"
]

# --- VARIABLES GLOBALES ---
selected_hwnd = None
stop_event = threading.Event()
current_display = "Iniciando..."
root = None
listbox = None
app_mutex = None # Necesario para mantener el candado vivo

# --- RUTAS ---
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, FILENAME)

# --- API WINDOWS ---
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def enforce_single_instance():
    """Intenta crear un Mutex nombrado. Si falla, ya existe otra instancia."""
    global app_mutex
    # Intentamos crear el mutex
    app_mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    last_error = kernel32.GetLastError()
    
    # ERROR_ALREADY_EXISTS = 183
    if last_error == 183:
        return False
    return True

def get_window_text(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value
    return ""

def get_visible_windows():
    windows = []
    def enum_callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            title = get_window_text(hwnd)
            if title and title not in ["Program Manager", "Settings", "Microsoft Text Input Application"]:
                windows.append((hwnd, title))
        return True
    user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)(enum_callback), 0)
    return sorted(windows, key=lambda x: x[1])

# --- LÓGICA GUI (TKINTER) ---
windows_map = []

def refresh_list():
    global listbox, windows_map
    listbox.delete(0, tk.END)
    windows_map.clear()
    current_windows = get_visible_windows()
    for hwnd, title in current_windows:
        windows_map.append((hwnd, title))
        listbox.insert(tk.END, f"{title}")

def on_select():
    global selected_hwnd, root
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Atención", "Selecciona una ventana.")
        return
    index = selection[0]
    selected_hwnd = windows_map[index][0]
    root.withdraw()

def show_gui_threadsafe():
    refresh_list()
    root.deiconify()
    root.lift()
    root.focus_force()

def setup_gui():
    global root, listbox
    root = tk.Tk()
    root.title("Selector Universal")
    root.geometry("400x500")

    lbl = tk.Label(root, text="Selecciona la ventana a monitorear:", font=("Arial", 10, "bold"))
    lbl.pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Consolas", 9))
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    btn_refresh = tk.Button(btn_frame, text="Actualizar Lista", command=refresh_list)
    btn_refresh.pack(side="left", padx=5)

    btn_ok = tk.Button(btn_frame, text="MONITOREAR ESTA", command=on_select, bg="#1ed760", fg="white", font=("Arial", 9, "bold"))
    btn_ok.pack(side="left", padx=5)

    def on_close_window():
        if selected_hwnd:
            root.withdraw()
        else:
            sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_close_window)
    refresh_list()

# --- LÓGICA MONITOR ---
def clean_title(title):
    for suffix in SUFIJOS_LIMPIEZA:
        if title.endswith(suffix):
            return title[:-len(suffix)]
    return title

def monitor_loop(icon):
    global current_display, selected_hwnd
    last_wrote = None

    while not stop_event.is_set():
        try:
            if not selected_hwnd:
                current_display = TEXTO_SELECCIONANDO
                time.sleep(1)
                continue

            if not user32.IsWindow(selected_hwnd):
                current_text = TEXTO_VENTANA_CERRADA
            else:
                raw_title = get_window_text(selected_hwnd)
                current_text = clean_title(raw_title) if raw_title else "..."

            if current_text != last_wrote:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(current_text)
                last_wrote = current_text
                current_display = current_text
                
                safe_tooltip = f"Monitor: {current_text}"[:63]
                icon.title = safe_tooltip
                try: icon.update_menu()
                except: pass

        except Exception as e:
            print(e)
        time.sleep(CHECK_INTERVAL)

# --- TRAY ICON ---
def create_image():
    img = Image.new('RGB', (64, 64), (255, 87, 34)) 
    dc = ImageDraw.Draw(img)
    dc.ellipse((16, 16, 48, 48), fill=(255, 255, 255))
    return img

def on_reselect(icon, item):
    root.after(0, show_gui_threadsafe)

def on_exit_app(icon, item):
    stop_event.set()
    icon.stop()
    root.quit()
    sys.exit()

def get_label(item):
    return f"👁️ {current_display}"[:50]

def start_tray():
    menu = Menu(
        item(get_label, action=None),
        item("Cambiar App / Ventana", on_reselect),
        item("Abrir carpeta", lambda i, It: os.startfile(script_dir)),
        item("Salir", on_exit_app)
    )
    icon = Icon("WindowMonitor", create_image(), title="Monitor Activo", menu=menu)
    t_monitor = threading.Thread(target=monitor_loop, args=(icon,), daemon=True)
    t_monitor.start()
    icon.run()

# --- MAIN (CON CHECK DE INSTANCIA ÚNICA) ---
if __name__ == "__main__":
    # 1. VERIFICAR INSTANCIA ÚNICA
    if not enforce_single_instance():
        # Opcional: Mostrar alerta visual
        ctypes.windll.user32.MessageBoxW(0, "El Monitor Universal ya se está ejecutando.\nRevisa la bandeja del sistema (cerca del reloj).", "Error", 0x10)
        sys.exit()

    # 2. INICIAR APP NORMALMENTE
    setup_gui() 
    t_tray = threading.Thread(target=start_tray, daemon=True)
    t_tray.start()
    root.mainloop()