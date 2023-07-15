import socket
import time
import threading
import sys

def check_internet_connection():
    # Verbindung zu einem zuverlässigen Server herstellen (z. B. Google DNS)
    host = '8.8.8.8'
    port = 53
    timeout = 5  # in Sekunden

    try:
        # Socket erstellen
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
        return True
    except socket.error:
        return False

def calculate_uptime(start_time, end_time, downtime):
    total_time = end_time - start_time
    uptime = total_time - downtime
    uptime_percent = (uptime / total_time) * 100
    return uptime_percent

def print_live_uptime(start_time, downtime):
    while not exit_event.is_set():
        current_time = time.time()
        uptime_percent = calculate_uptime(start_time, current_time, downtime)
        sys.stdout.write("\rUptime: {:.2f}% | Laufzeit: {:.2f}s".format(uptime_percent, current_time - start_time))
        sys.stdout.flush()
        time.sleep(1)

def main():
    interval = 1  # Intervall zwischen den Überprüfungen in Sekunden
    runtime = 3600  # Gesamtdauer der Überwachung in Sekunden
    start_time = time.time()
    end_time = start_time + runtime

    successful_checks = 0
    failed_checks = 0

    global exit_event
    exit_event = threading.Event()

    # Thread für die Live-Uptime-Anzeige starten
    uptime_thread = threading.Thread(target=print_live_uptime, args=(start_time, failed_checks * interval))
    uptime_thread.start()

    while time.time() < end_time:
        if check_internet_connection():
            successful_checks += 1
        else:
            failed_checks += 1

        time.sleep(interval)

    # Live-Uptime-Thread beenden
    exit_event.set()
    uptime_thread.join()

    uptime_percent = calculate_uptime(start_time, end_time, failed_checks * interval)
    sys.stdout.write("\rGesamte Uptime: {:.2f}% | Laufzeit: {:.2f}s\n".format(uptime_percent, runtime))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
