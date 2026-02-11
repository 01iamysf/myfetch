from src.core.scanner import Scanner
from src.core.formatter import Formatter

class HardwareModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("Hardware Deep Info")
        
        cpu = self.scanner.get_cpuinfo()
        mem = self.scanner.get_meminfo()
        
        # CPU Detailed
        self.formatter.kv("CPU Model", cpu.get('model', 'Unknown'), "")
        self.formatter.kv("Cores/Threads", str(cpu.get('cores', 'Unknown')), "󰻠")
        self.formatter.kv("Cache Size", cpu.get('cache', 'Unknown'), "󰍛")
        
        # VGA / GPU (simple lshw or lspci if available, else skip)
        try:
            import subprocess
            gpu_info = subprocess.check_output(['lspci'], stderr=subprocess.DEVNULL).decode()
            vga = [l for l in gpu_info.splitlines() if "VGA" in l or "3D controller" in l]
            if vga:
                self.formatter.kv("GPU", vga[0].split(':')[-1].strip(), "󰾲")
        except:
            pass

        # Memory configuration
        total_mem = self.formatter.format_size(mem.get('MemTotal', 0))
        self.formatter.kv("Total RAM", total_mem, "")
        
        # Motherboard / BIOS (requires root for dmidecode)
        if self.scanner.is_root():
            try:
                import subprocess
                mboard = subprocess.check_output(['dmidecode', '-s', 'baseboard-product-name'], stderr=subprocess.DEVNULL).decode().strip()
                vendor = subprocess.check_output(['dmidecode', '-s', 'baseboard-manufacturer'], stderr=subprocess.DEVNULL).decode().strip()
                if mboard:
                    self.formatter.kv("Motherboard", f"{vendor} {mboard}", "󰟀")
                
                bios = subprocess.check_output(['dmidecode', '-s', 'bios-version'], stderr=subprocess.DEVNULL).decode().strip()
                if bios:
                    self.formatter.kv("BIOS Version", bios, "󰣖")
            except:
                pass
        
        # Virtualization
        try:
            virt = self.scanner.read_file('/proc/cpuinfo')
            if 'hypervisor' in virt:
                self.formatter.kv("Virtualization", "Detected (Running in VM/Container)", "󰖟")
            else:
                self.formatter.kv("Virtualization", "None (Bare Metal)", "󰖟")
        except:
            pass
        
        if self.scanner.is_root():
            print("\n" + self.formatter.color("Honest Hardware Note: Root access used to read DMI tables for full hardware accuracy.", "yellow"))
