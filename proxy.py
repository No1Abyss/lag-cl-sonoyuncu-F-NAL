"""
Proxy Server - Bağlantıyı yönetir ve paketleri işler
"""

import asyncio
from typing import Optional, Dict, Tuple
from proxy.client_handler import ClientHandler
from utils.console import Console
from utils.logger import Logger
from utils.config import Config

logger = Logger("PROXY_SERVER")

class ProxyServer:
    """Ana proxy sunucusu"""
    
    def __init__(self, config: Config):
        self.config = config
        self.server = None
        self.active_connections: Dict[str, ClientHandler] = {}
        self.running = False
        
    async def start(self):
        """Proxy sunucusunu başlat"""
        try:
            local_ip = self.config.LOCAL_IP
            local_port = self.config.LOCAL_PORT
            
            self.server = await asyncio.start_server(
                self._handle_client,
                local_ip,
                local_port
            )
            
            self.running = True
            
            addrs = ', '.join(str(sock.getsockname()) for sock in self.server.sockets)
            Console.log(f"🚀 Proxy Sunucusu Başlatıldı: {addrs}", "SUCCESS")
            
            async with self.server:
                await self.server.serve_forever()
                
        except OSError as e:
            Console.log(f"❌ Port hatası: {e}", "ERROR")
            Console.log(f"💡 Port {local_port} zaten kullanımda olabilir", "INFO")
            raise
        except Exception as e:
            Console.log(f"❌ Sunucu başlatma hatası: {e}", "ERROR")
            raise
    
    async def _handle_client(self, client_reader, client_writer):
        """Yeni client bağlantısını yönet"""
        peer = client_writer.get_extra_info('peername')
        Console.log(f"➕ Yeni Client: {peer[0]}:{peer[1]}", "INFO")
        
        client_handler = ClientHandler(
            client_reader,
            client_writer,
            self.config
        )
        
        # Bağlantıyı kaydet
        connection_id = f"{peer[0]}:{peer[1]}"
        self.active_connections[connection_id] = client_handler
        
        try:
            await client_handler.handle()
        except Exception as e:
            Console.log(f"❌ Client handler hatası: {e}", "ERROR")
        finally:
            # Bağlantıyı kaldır
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
            
            Console.log(f"➖ Client Kapandı: {peer[0]}:{peer[1]}", "INFO")
            Console.log(f"📊 Aktif Bağlantılar: {len(self.active_connections)}", "DEBUG")
    
    async def stop(self):
        """Proxy sunucusunu durdur"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        # Tüm aktif bağlantıları kapat
        for handler in self.active_connections.values():
            await handler.close()
        
        self.running = False
        Console.log("✅ Proxy sunucusu kapatıldı", "SUCCESS")
    
    def get_active_connections(self) -> int:
        """Aktif bağlantı sayısını döndür"""
        return len(self.active_connections)
