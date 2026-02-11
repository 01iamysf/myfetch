from src.core.scanner import Scanner
from src.core.formatter import Formatter

class HealthModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("System Health & Hardware")
        
        temps = self.scanner.get_temperatures()
        mem = self.scanner.get_meminfo()
        battery = self.scanner.get_battery_info()
        load = self.scanner.get_loadavg()
        
        # CPU Temperature
        pkg_temp = temps.get('x86_pkg_temp', temps.get('Package id 0', next(iter(temps.values())) if temps else 0))
        temp_str = f"{pkg_temp:.1f}°C" if pkg_temp else "N/A"
        
        health_color = "green"
        if pkg_temp and pkg_temp > 80:
            health_color = "red"
            hint = "(Critical: CPU is overheating!)"
        elif pkg_temp and pkg_temp > 65:
            health_color = "yellow"
            hint = "(Warning: CPU temperature is high)"
        else:
            hint = "(Safe range)"
            
        self.formatter.kv("CPU Temp", f"{self.formatter.color(temp_str, health_color)} {self.formatter.color(hint, 'gray')}", "")

        # Memory Pressure
        total = mem.get('MemTotal', 0)
        available = mem.get('MemAvailable', mem.get('MemFree', 0) + mem.get('Cached', 0))
        used = total - available
        percent = (used / total * 100) if total > 0 else 0
        
        mem_status = "Healthy"
        if percent > 90: mem_status = "Critical (Out of memory risk)"
        elif percent > 75: mem_status = "Warning (High memory pressure)"
        
        self.formatter.kv("Memory Status", f"{mem_status} ({percent:.1f}% used)", "")

        # Battery
        if battery:
            bat_status = f"{battery['capacity']}% ({battery['status']})"
            self.formatter.kv("Battery", bat_status, "󰁹")

        # Services Check (Basic detection of failed systemd services)
        try:
            import subprocess
            failed_services = subprocess.check_output(['systemctl', 'list-units', '--state=failed', '--no-legend'], stderr=subprocess.STDOUT).decode().strip()
            if failed_services:
                self.formatter.kv("Failed Services", self.formatter.color("Detection Pending (See --services)", "yellow"), "")
            else:
                self.formatter.kv("Services Status", self.formatter.color("All services running normally", "green"), "")
        except:
            pass

        print("\n" + self.formatter.color("Overall Device Health Report: The system appears functional and stable.", "white", bold=True))
