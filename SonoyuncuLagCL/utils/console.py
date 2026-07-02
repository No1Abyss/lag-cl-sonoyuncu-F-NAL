"""
Konsol Yöneticisi - Renkli çıktı ve logo
"""

from colorama import Fore, Back, Style, init

init(autoreset=True)

class Console:
    """Konsol operasyonlarını yönetir"""
    
    @staticmethod
    def banner():
        """Başlangıç banner'ını göster"""
        banner = f"""
{Fore.RED}╔════════════════════════════════════════════════════════════╗
║         {Fore.WHITE}SonOyuncu Lag Client v2.0{Fore.RED}                      ║
║         {Fore.WHITE}Proxy + Lag Mekanizması{Fore.RED}                         ║
║         {Fore.WHITE}Modern Python Sürümü{Fore.RED}                           ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.CYAN}⚙️  Ayarlar:{Style.RESET_ALL}
  • H tuşu: Lag aç/kapat
  • P tuşu: Statistikler
  • Q tuşu: Çık

{Fore.YELLOW}⚠️  Dikkat:{Style.RESET_ALL}
  • Sunucu: 127.0.0.1:8080
  • Remote: mc.sonoyuncu.network:25565
  
{Fore.GREEN}✅ Hazırlanıyor...{Style.RESET_ALL}
"""
        print(banner)
    
    @staticmethod
    def log(message: str, level: str = "INFO"):
        """Log mesajı yazdır"""
        colors = {
            "INFO": Fore.CYAN,
            "SUCCESS": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "DEBUG": Fore.MAGENTA,
        }
        
        color = colors.get(level, Fore.WHITE)
        timestamp = __import__('datetime').datetime.now().strftime("%H:%M:%S")
        
        print(f"{Fore.BLUE}[{timestamp}]{Style.RESET_ALL} {color}[{level}]{Style.RESET_ALL} {message}")