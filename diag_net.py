import subprocess
import os

def diag():
    print("--- ID ---")
    print(f"UID: {os.getuid()}")
    
    commands = [
        ['ss', '-tulnp'],
        ['ss', '-tunp'],
        ['ls', '-l', '/proc/net/tcp'],
        ['cat', '/proc/net/tcp'],
        ['ip', 'addr']
    ]
    
    for cmd in commands:
        print(f"\n--- COMMAND: {' '.join(cmd)} ---")
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            print(out)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    diag()
