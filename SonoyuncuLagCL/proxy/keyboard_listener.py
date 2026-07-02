"""
Klavye Dinleyici - Oyun başında H tuşu vs.
"""

import asyncio
import keyboard
from utils.console import Console
from utils.logger import Logger

logger = Logger("KEYBOARD")

class KeyboardListener:
    """Klavye girdilerini dinler"""
    
    def __init__(self):
        self.running = False
        self.lag_enabled = True
        
    async def start(self):
        """Klavye dinlemesini başlat"""
        self.running = True
        
        # Klavye olaylarını arka planda dinle
        loop = asyncio.get_event_loop()
        
        keyboard.on_press_key('h', self._toggle_lag)
        keyboard.on_press_key('p', self._show_stats)
        keyboard.on_press_key('q', self._quit)
        
        Console.log("✅ Klavye dinleyici aktif", "SUCCESS")
        Console.log("  H=Lag Aç/Kapat | P=Statistik | Q=Çık", "INFO")
        
        # Dinlemeyi devam ettir
        while self.running:
            await asyncio.sleep(1)
    
    def _toggle_lag(self, event=None):
        """Lag'i aç/kapat"""
        self.lag_enabled = not self.lag_enabled
        status = "🟢 AÇIK" if self.lag_enabled else "🔴 KAPALI"
        Console.log(f"Lag {status}", "WARNING")
    
    def _show_stats(self, event=None):
        """İstatistikleri göster"""
        Console.log("📊 İstatistikler", "INFO")
        Console.log("  • Paket Sayısı: ...", "DEBUG")
        Console.log("  • Toplam Bytes: ...", "DEBUG")
    
    def _quit(self, event=None):
        """Programı kapat"""
        Console.log("Çıkılıyor...", "WARNING")
        import sys
        sys.exit(0)