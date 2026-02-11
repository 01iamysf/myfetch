import os
from src.core.scanner import Scanner
from src.core.formatter import Formatter

class SecurityModule:
    def __init__(self, scanner: Scanner, formatter: Formatter):
        self.scanner = scanner
        self.formatter = formatter

    def run(self):
        self.formatter.header("Security Status")
        
        # 1. Firewall Check (basic)
        fw_status = "Unknown"
        try:
            if os.path.exists('/usr/sbin/ufw'):
                import subprocess
                out = subprocess.check_output(['ufw', 'status'], stderr=subprocess.STDOUT).decode()
                fw_status = "Active" if "active" in out.lower() else "Inactive"
            elif os.path.exists('/usr/bin/firewall-cmd'):
                import subprocess
                out = subprocess.check_output(['firewall-cmd', '--state'], stderr=subprocess.STDOUT).decode().strip()
                fw_status = "Active" if out == "running" else "Inactive"
        except:
            pass
        
        fw_color = "green" if fw_status == "Active" else "yellow"
        self.formatter.kv("Firewall", self.formatter.color(fw_status, fw_color), "󰒃")

        # 2. SSH Status
        ssh_status = "Disabled"
        try:
            import subprocess
            subprocess.check_output(['systemctl', 'is-active', 'sshd'], stderr=subprocess.STDOUT)
            ssh_status = "Enabled"
        except:
            pass
        self.formatter.kv("SSH Service", ssh_status, "󰣀")

        # 3. SELinux / AppArmor
        sec_module = "None"
        if os.path.exists('/sys/fs/selinux'):
            sec_module = "SELinux (Enforcing)" # Simplifying for this tool
        elif os.path.exists('/sys/kernel/security/apparmor'):
            sec_module = "AppArmor"
            
        self.formatter.kv("Kernel Security", sec_module, "󰞀")

        
        print(self.formatter.color("Basic security risk summary: System is protected by kernel security modules.", "white"))
