from src.core.scanner import Scanner
from src.core.formatter import Formatter

class NetworkModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("Network Analysis")
        
        ips = self.scanner.get_ip_addresses()
        net_stats = self.scanner.get_net_stats()
        
        self.formatter.kv("Primary IP", ips.get('primary', 'Unknown'), "󰩟")
        
        if not net_stats:
            print(self.formatter.color("No active network interfaces detected.", "yellow"))
            return

        print(f"\n{self.formatter.color('INTERFACE STATUS', 'white', bold=True)}")
        print(f"{'IFACE':<12} {'RECEIVED':<15} {'SENT':<15}")
        print("─" * 45)
        
        for iface, stats in net_stats.items():
            rx = self.formatter.format_size(stats['rx'] / 1024)
            tx = self.formatter.format_size(stats['tx'] / 1024)
            print(f"{iface:<12} {rx:<15} {tx:<15}")

        status = "Healthy" if ips.get('primary') != "Disconnected" else "Disconnected"
        color = "green" if status == "Healthy" else "red"
        
        print("\n" + self.formatter.color(f"Connectivity Status: {status}", color, bold=True))
        print(self.formatter.color("Recommendation: Use --network for detailed routing and port scan (future update).", "gray"))
