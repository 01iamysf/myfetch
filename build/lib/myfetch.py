#!/usr/bin/env python3
import sys
import argparse
import os
import json
from src.core.scanner import Scanner
from src.core.formatter import Formatter
from src.modules.performance import PerformanceModule
from src.modules.network import NetworkModule
from src.modules.health import HealthModule
from src.modules.storage import StorageModule
from src.modules.security import SecurityModule
from src.modules.services import ServicesModule
from src.modules.hardware import HardwareModule

class MyFetch:
    def __init__(self, use_icons=False, use_colors=True):
        self.scanner = Scanner()
        self.formatter = Formatter(use_icons=use_icons, use_colors=use_colors)
        self.config_path = os.path.expanduser("~/.config/myfetch/config")
        self.load_config()

    def load_config(self):
        """Loads configuration from ~/.config/myfetch/config (simple JSON for now)."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.formatter.use_icons = config.get('icons', self.formatter.use_icons)
                    self.formatter.use_colors = config.get('colors', self.formatter.use_colors)
            except:
                pass

    def get_health_status(self, load, mem_percent):
        reasons = []
        if load > 5.0: reasons.append("Critical system load")
        elif load > 2.0: reasons.append("High system load")
        
        if mem_percent > 90: reasons.append("Critical memory usage")
        elif mem_percent > 75: reasons.append("High memory usage")

        reason_str = f" ({', '.join(reasons)})" if reasons else ""
        
        if load > 5.0 or mem_percent > 90:
            return self.formatter.color("Needs Attention", "red", bold=True) + self.formatter.color(reason_str, "gray")
        elif load > 2.0 or mem_percent > 75:
            return self.formatter.color("Warning", "yellow", bold=True) + self.formatter.color(reason_str, "gray")
        return self.formatter.color("Healthy", "green", bold=True)

    def show_default(self):
        os_info = self.scanner.get_os_release()
        kernel = self.scanner.get_kernel_version()
        hostname = self.scanner.get_hostname()
        uptime = self.scanner.get_uptime()
        cpu = self.scanner.get_cpuinfo()
        mem = self.scanner.get_meminfo()
        battery = self.scanner.get_battery_info()
        load = self.scanner.get_loadavg()
        ips = self.scanner.get_ip_addresses()

        # Calculate memory usage
        total_mem = mem.get('MemTotal', 0)
        free_mem = mem.get('MemFree', 0) + mem.get('Buffers', 0) + mem.get('Cached', 0)
        used_mem = total_mem - free_mem
        mem_percent = (used_mem / total_mem * 100) if total_mem > 0 else 0

        self.formatter.header(f"System Summary: {hostname}")
        
        self.formatter.kv("OS", f"{os_info.get('NAME', 'Linux')} {os_info.get('VERSION', '')}", "")
        self.formatter.kv("Kernel", kernel, "")
        self.formatter.kv("Uptime", self.formatter.format_uptime(uptime), "")
        self.formatter.kv("CPU", cpu.get('model', 'Unknown'), "")
        
        mem_str = f"{self.formatter.format_size(used_mem)} / {self.formatter.format_size(total_mem)} ({mem_percent:.1f}%)"
        self.formatter.kv("RAM", f"{mem_str} {self.formatter.get_progress_bar(mem_percent)}", "")

        self.formatter.kv("Network", f"Connected ({ips.get('primary', 'Disconnected')})", "󰩟")

        if battery:
            self.formatter.kv("Battery", f"{battery['capacity']}% ({battery['status']})", "󰁹")

        # Health
        health = self.get_health_status(load[0], mem_percent)
        self.formatter.kv("System Health", health, "󰓅")
        
        print("\n" + self.formatter.color("Run 'myfetch --help' for detailed modules", "gray"))

def main():
    parser = argparse.ArgumentParser(description="myfetch - Advanced Linux System Information")
    parser.add_argument("--top", action="store_true", help="Real-time performance monitoring")
    parser.add_argument("--network", action="store_true", help="Network analysis and status")
    parser.add_argument("--health", action="store_true", help="System health and diagnostics")
    parser.add_argument("--storage", action="store_true", help="Storage and filesystem details")
    parser.add_argument("--security", action="store_true", help="Security status summary")
    parser.add_argument("--services", action="store_true", help="System services and boot performance")
    parser.add_argument("--hardware", action="store_true", help="Deep hardware information")
    parser.add_argument("--icons", action="store_true", help="Enable Nerd Font icons")
    parser.add_argument("--json", action="store_true", help="Output in JSON format (not all modules support yet)")
    
    args = parser.parse_args()
    
    fetch = MyFetch(use_icons=args.icons)
    
    if args.json:
        # Simple JSON dump of scanner data for now
        data = {
            "uptime": fetch.scanner.get_uptime(),
            "load": fetch.scanner.get_loadavg(),
            "memory": fetch.scanner.get_meminfo(),
            "battery": fetch.scanner.get_battery_info(),
            "storage": fetch.scanner.get_storage_info()
        }
        print(json.dumps(data, indent=2))
        return

    if args.top:
        PerformanceModule(fetch.scanner, fetch.formatter).run()
    elif args.network:
        NetworkModule(fetch.scanner, fetch.formatter).run()
    elif args.health:
        HealthModule(fetch.scanner, fetch.formatter).run()
    elif args.storage:
        StorageModule(fetch.scanner, fetch.formatter).run()
    elif args.security:
        SecurityModule(fetch.scanner, fetch.formatter).run()
    elif args.services:
        ServicesModule(fetch.scanner, fetch.formatter).run()
    elif args.hardware:
        HardwareModule(fetch.scanner, fetch.formatter).run()
    else:
        fetch.show_default()

if __name__ == "__main__":
    main()
