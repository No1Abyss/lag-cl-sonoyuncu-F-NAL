"""
SonOyuncu Lag Client Main Entry Point
Geliştirilmiş ve modernize edilmiş versiyon
"""

import asyncio
import signal
import os
import sys
from pathlib import Path

# Proje kütüphaneleri
from proxy.server import ProxyServer
from utils.config import Config
from utils.console import Console
from utils.logger import Logger
from proxy.keyboard_listener import KeyboardListener

# Logger'ı başlat
logger = Logger("MAIN")

class SonOyuncuLagClient:
    """Ana aplikasyon sınıfı"""
    
    def __init__(self):
        self.config = None
        self.proxy_server = None
        self.keyboard_listener = None
        self.loop = None
        
    async def initialize(self):
        """Uygulamayı başlat"""
        try:
            # Config'i yükle
            self.config = Config.load_config()
            Console.log("✅ Konfigürasyon yüklendi", "INFO")
            
            # Proxy sunucusunu oluştur
            self.proxy_server = ProxyServer(self.config)
            Console.log("✅ Proxy sunucusu oluşturuldu", "INFO")
            
            # Keyboard listener'ı başlat
            self.keyboard_listener = KeyboardListener()
            asyncio.create_task(self.keyboard_listener.start())
            Console.log("✅ Klavye dinleyicisi başlatıldı", "INFO")
            
        except Exception as e:
            Console.log(f"❌ Başlatma hatası: {e}", "ERROR")
            sys.exit(1)
    
    async def run(self):
        """Uygulamayı çalıştır"""
        await self.initialize()
        await self.proxy_server.start()
    
    async def shutdown(self):
        """Uygulamayı kapat"""
        Console.log("🔴 Kapatılıyor...", "WARNING")
        
        if self.proxy_server:
            await self.proxy_server.stop()
        
        if self.loop:
            self.loop.stop()


async def main():
    """Async ana fonksiyon"""
    app = SonOyuncuLagClient()
    
    # Signal handlers
    def signal_handler():
        asyncio.create_task(app.shutdown())
    
    loop = asyncio.get_event_loop()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await app.run()
    except KeyboardInterrupt:
        await app.shutdown()


if __name__ == "__main__":
    Console.banner()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Console.log("\n🔴 Program kapatıldı", "WARNING")
    except Exception as e:
        Console.log(f"❌ Kritik hata: {e}", "ERROR")
        sys.exit(1)