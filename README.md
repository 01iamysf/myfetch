# myfetch - Advanced Linux System Information & Diagnostics

An all-in-one system inspection tool designed for speed, modularity, and human-friendly diagnostics.

## Features
- **Fast**: Reads directly from `/proc` and `/sys` with zero dependencies.
- **Modular**: Separate views for Performance, Network, Storage, Security, and more.
- **Intelligent**: Provides human-readable explanations and health alerts.
- **Honest**: Detailed memory breakdowns and root-level hardware discovery.
- **Modern**: ANSI colors and Nerd Font icon support.

## Installation

### Quick Install (via curl)
Run this one-liner to install `myfetch` globally on any Linux computer:
```bash
curl -sSL https://raw.githubusercontent.com/01iamysf/myfetch/main/curl-install.sh | bash
```

### Uninstallation
To completely remove `myfetch` from your system, run:
```bash
curl -sSL https://raw.githubusercontent.com/01iamysf/myfetch/main/uninstall.sh | bash
```

## Usage
Once installed, simply run:
```bash
myfetch
```
Or for specific modules:
```bash
myfetch --top
myfetch --storage
```
- `myfetch --health`: System health & diagnostics.
- `myfetch --network`: Network analysis.
- `myfetch --security`: Security status and port audit.
- `myfetch --hardware`: Deep hardware info (motherboard, BIOS, CPU, GPU).
- `myfetch --services`: Systemd services & boot performance.

### Sudo Mode (Recommended):
Run with `sudo` to unlock detailed hardware tables, process ownership, and network port mapping:
```bash
sudo myfetch --top
```

## Configuration
Customize the tool at `~/.config/myfetch/config` (JSON):
```json
{
  "icons": true,
  "colors": true
}
```

<<<<<<< HEAD
=======
## Online Distribution

### Hosting on GitHub
1. Create a new repository on GitHub.
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Public release"
   git remote add origin https://github.com/yourusername/myfetch.git
   git push -u origin main
   ```

### Publishing to PyPI
1. Build the package:
   ```bash
   python3 -m pip install --upgrade build
   python3 -m build
   ```
2. Upload to PyPI (requires an account):
   ```bash
   python3 -m pip install --upgrade twine
   python3 -m twine upload dist/*
   ```

### One-liner Installation (GitHub)
Once hosted on GitHub, users can install it instantly:
```bash
curl -sSL https://raw.githubusercontent.com/adminysf/myfetch/main/install.sh | bash
```
>>>>>>> 4241296 (Public release)
