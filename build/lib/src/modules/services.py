import subprocess
from src.core.scanner import Scanner
from src.core.formatter import Formatter

class ServicesModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("System Services")
        
        # Debug: Confirming user privileges
        # print(f"DEBUG: Current UID is {os.getuid()}") 
        
        try:
            # Running services count
            running = subprocess.check_output(['systemctl', 'list-units', '--state=running', '--no-legend']).decode().count('\n')
            # Failed services list
            failed = subprocess.check_output(['systemctl', 'list-units', '--state=failed', '--no-legend']).decode().strip()
            
            self.formatter.kv("Running Services", str(running), "󰒲")
            if failed:
                print(f"\n{self.formatter.color('FAILED SERVICES DETECTED', 'red', bold=True)}")
                print(failed)
            else:
                self.formatter.kv("Services Status", self.formatter.color("All services operational", "green"), "")

            # Boot performance (basic systemd-analyze)
            try:
                boot_time = subprocess.check_output(['systemd-analyze', 'time']).decode().strip()
                self.formatter.kv("Boot Time", boot_time.split('=')[-1].strip(), "")
            except:
                pass


                
        except:
            print(self.formatter.color("Systemd not detected or inaccessible.", "yellow"))

        print("\n" + self.formatter.color("Tip: Use 'systemctl status <service>' for deep inspection.", "gray"))
