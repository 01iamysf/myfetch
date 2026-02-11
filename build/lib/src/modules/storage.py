from src.core.scanner import Scanner
from src.core.formatter import Formatter

class StorageModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("Storage & Filesystems")
        
        storage = self.scanner.get_storage_info()
        
        if not storage:
            print(self.formatter.color("No physical storage devices detected.", "yellow"))
            return

        print(f"{'DEVICE':<15} {'MOUNT':<20} {'TYPE':<10} {'USAGE':<25}")
        print("─" * 70)
        
        total_cap = 0
        total_used = 0
        seen_devices = set()
        
        for s in storage:
            # For total calculation, we only count each physical device once to avoid overcounting (e.g. BTRFS subvolumes)
            if s['device'] not in seen_devices:
                total_cap += s['total']
                total_used += s['used']
                seen_devices.add(s['device'])
            
            usage_str = f"{self.formatter.format_size(s['used'] / 1024)} / {self.formatter.format_size(s['total'] / 1024)}"
            bar = self.formatter.get_progress_bar(s['percent'], width=10)
            
            # Warning logic
            status_tag = ""
            if s['percent'] > 90:
                status_tag = self.formatter.color(" [CRITICAL]", "red", bold=True)
            elif s['percent'] > 80:
                status_tag = self.formatter.color(" [WARNING]", "yellow", bold=True)
                
            print(f"{s['device']:<15} {s['mount']:<20} {s['type']:<10} {bar} {s['percent']:>5.1f}%{status_tag}")

        print("─" * 70)
        total_gb = total_cap / (1024**3)
        used_gb = total_used / (1024**3)
        total_percent = (total_used / total_cap * 100) if total_cap > 0 else 0
        
        summary_str = f"TOTAL SYSTEM STORAGE: {used_gb:.1f} GB / {total_gb:.1f} GB ({total_percent:.1f}% Used)"
        print(self.formatter.color(summary_str, "white", bold=True))

        if any(s['percent'] > 80 for s in storage):
            print(self.formatter.color("\nWarning: Some partitions are near capacity. Consider cleaning up old logs or temp files.", "yellow"))
        
        print("\n" + self.formatter.color("Performance Hint: Use 'noatime' mount option for better SSD performance.", "cyan"))
