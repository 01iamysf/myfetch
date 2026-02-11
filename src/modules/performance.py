from typing import Dict, Any
from src.core.scanner import Scanner
from src.core.formatter import Formatter

class PerformanceModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("Performance Monitoring")
        
        load = self.scanner.get_loadavg()
        mem = self.scanner.get_meminfo()
        
        # CPU Load
        load_str = f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
        explanation = ""
        if load[0] < 1.0:
            explanation = "(System is idle)"
        elif load[0] < 4.0:
            explanation = "(Normal operating load)"
        else:
            explanation = "(Heavy load detected, performance may be impacted)"
        
        self.formatter.kv("Load Average", f"{load_str} {self.formatter.color(explanation, 'gray')}", "󰓅")

        # Memory Detailed
        total = mem.get('MemTotal', 0)
        available = mem.get('MemAvailable', mem.get('MemFree', 0) + mem.get('Cached', 0))
        free = mem.get('MemFree', 0)
        cached = mem.get('Cached', 0)
        buffers = mem.get('Buffers', 0)
        slab = mem.get('Slab', 0)
        shared = mem.get('Shmem', 0)
        
        used = total - available
        percent = (used / total * 100) if total > 0 else 0
        
        mem_str = f"{self.formatter.format_size(used)} used of {self.formatter.format_size(total)}"
        self.formatter.kv("Memory Pressure", f"{self.formatter.get_progress_bar(percent)} {percent:.1f}%", "")
        
        # Honest Breakdown
        print(f"\n{self.formatter.color('HONEST MEMORY BREAKDOWN', 'white', bold=True)}")
        self.formatter.kv("  Used (Apps/System)", self.formatter.format_size(used))
        self.formatter.kv("  Cached/Buffers", self.formatter.color(self.formatter.format_size(cached + buffers), "gray"))
        self.formatter.kv("  Kernel (Slab)", self.formatter.color(self.formatter.format_size(slab), "gray"))
        self.formatter.kv("  Shared", self.formatter.color(self.formatter.format_size(shared), "gray"))
        self.formatter.kv("  Truly Free", self.formatter.color(self.formatter.format_size(free), "green"))

        # Top Processes
        is_root = self.scanner.is_root()
        root_tag = self.formatter.color(" [ROOT MODE]", "red", bold=True) if is_root else ""
        print(f"\n{self.formatter.color('TOP PROCESSES', 'white', bold=True)}{root_tag}")
        header = f"{'PID':<8} {'NAME':<20} {'MEMORY':<15}"
        if is_root:
            header = f"{'PID':<8} {'OWNER':<10} {'NAME':<20} {'MEMORY':<15}"
        print(header)
        print("─" * (len(header) + 5))
        
        processes = self.scanner.get_top_processes(limit=5)
        total_p_mem = 0
        for p in processes:
            mem_readable = self.formatter.format_size(p['mem_bytes'] / 1024)
            if is_root:
                owner = "root" if p['owner'] == 0 else str(p['owner'])
                print(f"{p['pid']:<8} {owner:<10} {p['name']:<20} {mem_readable:<15}")
            else:
                print(f"{p['pid']:<8} {p['name']:<20} {mem_readable:<15}")
            total_p_mem += p['mem_bytes']
        
        print("─" * (len(header) + 5))
        total_readable = self.formatter.format_size(total_p_mem / 1024)
        total_label_width = 18 if is_root else 8
        print(f"{'TOTAL (Top 5)':<29} {self.formatter.color(total_readable, 'yellow', bold=True):<15}")
        
        print("\n" + self.formatter.color("Note: Total system usage includes kernel, many small processes, and reserved memory.", "gray"))
        print(self.formatter.color("Recommendation: Check high memory processes if system feels slow.", "cyan"))
