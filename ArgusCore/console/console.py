import time
import threading

import config.settings as settings
from scripts.monitor import run_monitor, stop_monitor


# =========================
# GLOBAL STATES
# =========================

monitor_thread = None
monitor_active = False
failed_attempts = 0


class Colors:
    RED   = "\033[91m"
    GREEN = "\033[92m"
    RESET = "\033[0m"


# =========================
# BANNER / MENU
# =========================

def show_banner():
    print("\n========================")
    print(" ARGUSCORE CONSOLE")
    print(f" Version: {settings.APP_VERSION}")
    print("========================\n")


def show_menu():
    monitoring_status = "ON"  if monitor_active      else "OFF"
    monitoring_color  = Colors.GREEN if monitor_active      else Colors.RED
    debug_status      = "ON"  if settings.DEBUG_MODE else "OFF"
    debug_color       = Colors.GREEN if settings.DEBUG_MODE else Colors.RED

    print(f"1. Scan Engine {monitoring_color}[{monitoring_status}]{Colors.RESET}")
    print("2. System Status")
    print(f"3. Debug Mode {debug_color}[{debug_status}]{Colors.RESET}")
    print("4. Recent Errors")
    print("5. Recent Detections")
    print("6. Metrics")
    print("7. Change Scan Interval")
    print("8. Exit\n")


# =========================
# AUTH
# =========================

def verify_admin_password():
    global failed_attempts

    password = input("\nAdministrator Password: ")

    if password == settings.ADMIN_PASSWORD:
        failed_attempts = 0
        return True

    failed_attempts += 1
    remaining = settings.MAX_LOGIN_ATTEMPTS - failed_attempts

    print(f"\n[SECURITY] Invalid password")
    print(f"Attempts remaining: {remaining}\n")

    if failed_attempts >= settings.MAX_LOGIN_ATTEMPTS:
        settings.LOCKDOWN_MODE = True
        print("\n[SECURITY] LOCKDOWN ACTIVATED")
        print("ArgusCore has been locked.\n")
        exit()

    return False


# =========================
# STATUS
# =========================

def show_system_status():
    print("\n========================")
    print(" ARGUSCORE STATUS ")
    print("========================\n")
    print(f"Version:          {settings.APP_VERSION}")
    print(f"Scan Engine:      {'ONLINE' if monitor_active else 'OFFLINE'}")
    print(f"Debug Mode:       {'ON' if settings.DEBUG_MODE else 'OFF'}")
    print(f"Monitor Interval: {settings.MONITOR_INTERVAL}s")
    print(f"Lockdown Mode:    {'ENABLED' if settings.LOCKDOWN_MODE else 'DISABLED'}")
    print("Security Logger:  ACTIVE")
    print("Incident Manager: ACTIVE")
    print("Detectors Loaded: 7")
    print()


# =========================
# LOGS
# =========================

def show_errors():
    """Opción 4: muestra errors.log y security incidents."""
    print("\n===== ERRORES RECIENTES =====\n")
    _read_log("logs/errors.log", label="errors")
    show_security_incidents()


def show_detections():
    """Opción 5: muestra detections.log y error.log."""
    print("\n===== DETECCIONES RECIENTES =====\n")
    _read_log("logs/detections.log", label="detections")
    show_error_log()


def _read_log(path, label="log"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print(f"No hay entradas en {label}.\n")
        else:
            for line in lines[-10:]:
                print(line.strip())
    except FileNotFoundError:
        print(f"Archivo {path} no encontrado.\n")
    except Exception as err:
        print(f"[ERROR] {err}")


def show_security_incidents():
    print("\n=== SECURITY INCIDENTS ===\n")
    _read_log("logs/security.log", label="security incidents")
    print()


def show_error_log():
    print("\n=== ERROR LOG ===\n")
    _read_log("logs/error.log", label="error log")
    print()

# =========================
# METRICS
# =========================

def show_metrics():
    print("\n===== METRICAS =====\n")
    print("Módulo de métricas en desarrollo.")
    print("Tip: visita http://127.0.0.1:8000 para el dashboard en tiempo real.\n")


# =========================
# MONITORING
# =========================

def start_monitor():
    global monitor_thread, monitor_active

    if monitor_active:
        print("\n[!] Monitoring already active\n")
        return

    print("\n[SCAN ENGINE] Initializing...\n")

    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()
    monitor_active = True


def toggle_monitoring():
    global monitor_active

    if monitor_active:
        if verify_admin_password():
            stop_monitor()
            monitor_active = False
            print("\n[-] Scan Engine OFF\n")
    else:
        start_monitor()
        print("\n[+] Scan Engine ON\n")


# =========================
# SETTINGS
# =========================

def toggle_debug():
    settings.DEBUG_MODE = not settings.DEBUG_MODE
    status = "enabled" if settings.DEBUG_MODE else "disabled"
    print(f"\n[+] Debug mode {status}\n")


def change_scan_interval():
    try:
        interval = int(input("\nNew interval (seconds): "))
        settings.MONITOR_INTERVAL = interval
        print(f"\n[+] Scan interval updated to {interval} seconds\n")
    except ValueError:
        print("\n[!] Invalid value\n")


# =========================
# MAIN LOOP
# =========================

def start_console():
    while True:
        show_banner()
        show_menu()
        option = input("Select option: ").strip()

        if option == "1":
            toggle_monitoring()

        elif option == "2":
            show_system_status()

        elif option == "3":
            toggle_debug()

        elif option == "4":
            # Muestra errores + incidentes de seguridad
            show_errors()

        elif option == "5":
            # Muestra detecciones + error log
            show_detections()

        elif option == "6":
            show_metrics()

        elif option == "7":
            change_scan_interval()

        elif option == "8":
            if verify_admin_password():
                print("\n[+] Shutting down ArgusCore...\n")
                break

        else:
            print("\n[!] Invalid option\n")
