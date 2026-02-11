import os
import re
import time
from typing import Dict, Any, List, Optional

class Scanner:
    """Core scanner to read system data directly from /proc and /sys."""

    @staticmethod
    def is_root() -> bool:
        return os.getuid() == 0

    @staticmethod
    def read_file(path: str) -> str:
        try:
            with open(path, 'r') as f:
                return f.read()
        except (IOError, OSError):
            return ""

    def get_meminfo(self) -> Dict[str, int]:
        """Parses /proc/meminfo into a dictionary (values in KB)."""
        data = self.read_file('/proc/meminfo')
        meminfo = {}
        for line in data.splitlines():
            parts = line.split(':')
            if len(parts) == 2:
                name = parts[0].strip()
                match = re.search(r'(\d+)', parts[1])
                if match:
                    meminfo[name] = int(match.group(1))
        return meminfo

    def get_cpuinfo(self) -> Dict[str, Any]:
        """Parses /proc/cpuinfo for basic CPU details."""
        data = self.read_file('/proc/cpuinfo')
        cpuinfo = {}
        for line in data.splitlines():
            if not line.strip():
                break  # Only process the first processor entry for basic info
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip()
                if key == 'model name':
                    cpuinfo['model'] = val
                elif key == 'cpu MHz':
                    cpuinfo['mhz'] = val
                elif key == 'cache size':
                    cpuinfo['cache'] = val
        
        # Count total processors
        cpuinfo['cores'] = data.count('processor\t:')
        return cpuinfo

    def get_loadavg(self) -> List[float]:
        """Reads /proc/loadavg."""
        data = self.read_file('/proc/loadavg')
        parts = data.split()
        if len(parts) >= 3:
            return [float(x) for x in parts[:3]]
        return [0.0, 0.0, 0.0]

    def get_uptime(self) -> float:
        """Reads /proc/uptime (total seconds)."""
        data = self.read_file('/proc/uptime')
        parts = data.split()
        if parts:
            return float(parts[0])
        return 0.0

    def get_os_release(self) -> Dict[str, str]:
        """Parses /etc/os-release."""
        data = self.read_file('/etc/os-release')
        info = {}
        for line in data.splitlines():
            if '=' in line:
                key, val = line.split('=', 1)
                info[key.strip()] = val.strip().strip('"')
        return info

    def get_hostname(self) -> str:
        """Reads /proc/sys/kernel/hostname."""
        return self.read_file('/proc/sys/kernel/hostname').strip()

    def get_kernel_version(self) -> str:
        """Reads /proc/version or /proc/sys/kernel/osrelease."""
        return self.read_file('/proc/sys/kernel/osrelease').strip()

    def get_battery_info(self) -> Optional[Dict[str, Any]]:
        """Reads battery info from /sys/class/power_supply/."""
        base_path = '/sys/class/power_supply'
        if not os.path.exists(base_path):
            return None
        
        for supply in os.listdir(base_path):
            if supply.startswith('BAT'):
                path = os.path.join(base_path, supply)
                status = self.read_file(os.path.join(path, 'status')).strip()
                capacity = self.read_file(os.path.join(path, 'capacity')).strip()
                try:
                    return {
                        'status': status,
                        'capacity': int(capacity) if capacity else 0
                    }
                except ValueError:
                    continue
        return None

    def get_net_stats(self) -> Dict[str, Any]:
        """Basic network status from /proc/net/dev."""
        data = self.read_file('/proc/net/dev')
        stats = {}
        for line in data.splitlines()[2:]:  # Skip headers
            parts = line.split(':')
            if len(parts) == 2:
                iface = parts[0].strip()
                if iface == 'lo': continue
                metrics = parts[1].split()
                stats[iface] = {
                    'rx': int(metrics[0]),
                    'tx': int(metrics[8])
                }
        return stats

    def get_top_processes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Scans /proc/[pid]/stat for top processes."""
        processes = []
        pids = [d for d in os.listdir('/proc') if d.isdigit()]
        try:
            page_size = os.sysconf('SC_PAGE_SIZE')
        except:
            page_size = 4096
        
        for pid in pids:
            try:
                raw_stat = self.read_file(f'/proc/{pid}/stat')
                if not raw_stat: continue
                
                # The name is between the first '(' and the last ')'
                start = raw_stat.find('(')
                end = raw_stat.rfind(')')
                if start == -1 or end == -1: continue
                
                name = raw_stat[start + 1:end]
                # The rest of the fields start AFTER the last ')'
                rest = raw_stat[end + 2:].split()
                
                # rest[0] is state, so indices are shifted by 2 from the start of file
                # Field 24 (RSS) is at index 21 in 'rest'
                # rest indices: 0=state, 1=ppid, ..., 21=rss
                rss_pages = int(rest[21])
                rss_bytes = rss_pages * page_size
                
                processes.append({
                    'pid': pid,
                    'name': name,
                    'mem_bytes': rss_bytes,
                    'owner': os.stat(f'/proc/{pid}').st_uid if self.is_root() else None
                })
            except (IOError, IndexError, ValueError, OSError):
                continue
        
        return sorted(processes, key=lambda x: x['mem_bytes'], reverse=True)[:limit]

    def get_ip_addresses(self) -> Dict[str, str]:
        """Simple IP lookup (avoiding external commands if possible, but reading /proc/net/fib_trie is complex).
        We'll use a small trick with socket to get primary IP if needed, or stick to basic for now.
        """
        import socket
        ips = {}
        try:
            # Get primary IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips['primary'] = s.getsockname()[0]
            s.close()
        except:
            ips['primary'] = "Disconnected"
        return ips

    def get_storage_info(self) -> List[Dict[str, Any]]:
        """Parses /proc/mounts and uses os.statvfs for usage info."""
        storage = []
        data = self.read_file('/proc/mounts')
        
        # We only care about real physical disks usually
        seen_mounts = set()
        for line in data.splitlines():
            parts = line.split()
            if len(parts) < 3: continue
            
            device = parts[0]
            mount_point = parts[1]
            fs_type = parts[2]
            
            if not device.startswith('/dev/'): continue
            if mount_point in seen_mounts: continue
            
            try:
                st = os.statvfs(mount_point)
                total = (st.f_blocks * st.f_frsize)
                free = (st.f_bavail * st.f_frsize)
                used = total - free
                
                storage.append({
                    'device': device,
                    'mount': mount_point,
                    'type': fs_type,
                    'total': total,
                    'used': used,
                    'percent': (used / total * 100) if total > 0 else 0
                })
                seen_mounts.add(mount_point)
            except:
                continue
        return storage

    def get_temperatures(self) -> Dict[str, float]:
        """Reads from /sys/class/thermal/."""
        temps = {}
        base = '/sys/class/thermal'
        if not os.path.exists(base):
            return temps
            
        for d in os.listdir(base):
            if d.startswith('thermal_zone'):
                try:
                    name = self.read_file(os.path.join(base, d, 'type')).strip()
                    temp_raw = self.read_file(os.path.join(base, d, 'temp')).strip()
                    if temp_raw:
                        temps[name] = int(temp_raw) / 1000.0
                except:
                    continue
        return temps
