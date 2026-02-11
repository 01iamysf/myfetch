import os

class Formatter:
    """Handles ANSI colors, icons, and layout formatting."""

    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'gray': '\033[90m',
    }

    def __init__(self, use_colors=True, use_icons=False):
        self.use_colors = use_colors
        self.use_icons = use_icons

    def color(self, text: str, color_name: str, bold=False) -> str:
        if not self.use_colors:
            return text
        code = self.COLORS.get(color_name, self.COLORS['reset'])
        if bold:
            code += self.COLORS['bold']
        return f"{code}{text}{self.COLORS['reset']}"

    def get_progress_bar(self, percent: float, width=20) -> str:
        """Returns a color-coded progress bar."""
        filled = int(width * (percent / 100))
        bar = '█' * filled + '░' * (width - filled)
        
        color = 'green'
        if percent > 90:
            color = 'red'
        elif percent > 75:
            color = 'yellow'
        
        return self.color(bar, color)

    def format_size(self, size_kb: float) -> str:
        """Formats size in KB to human readable string."""
        for unit in ['KB', 'MB', 'GB', 'TB']:
            if size_kb < 1024:
                return f"{size_kb:.1f} {unit}"
            size_kb /= 1024
        return f"{size_kb:.1f} PB"

    def format_uptime(self, seconds: float) -> str:
        """Formats uptime seconds to human readable string."""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        parts = []
        if days > 0: parts.append(f"{days}d")
        if hours > 0: parts.append(f"{hours}h")
        if minutes > 0: parts.append(f"{minutes}m")
        
        return " ".join(parts) if parts else "just started"

    def header(self, title: str):
        print(f"\n{self.color('─── ' + title.upper() + ' ' + '─' * (40 - len(title)), 'cyan', bold=True)}")

    def kv(self, key: str, value: str, icon: str = ""):
        icon_str = f"{icon} " if self.use_icons and icon else ""
        print(f"{icon_str}{self.color(key + ':', 'blue', bold=True):<25} {value}")
