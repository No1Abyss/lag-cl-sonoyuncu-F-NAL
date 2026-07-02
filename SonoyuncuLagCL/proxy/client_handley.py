"""
Client Handler - Her client için işlem yapar
"""

import asyncio
from proxy.pipe import Pipe
from utils.console import Console
from utils.logger import Logger
from utils.config import Config
from utils.errors import ProxyConnectionError

logger = Logger("CLIENT_HANDLER")

class ClientHandler:
    """Her client bağlantısını işler"""
    
    def __init__(self, client_reader, client_writer, config: Config):
        self.client_reader = client_reader
        self.client_writer = client_writer
        self.config = config
        self.remote_reader = None
        self.remote_writer = None
        self.pipe_send = None
        self.pipe_recv = None
        
    async def handle(self):
        """Client bağlantısını yönet"""
        try:
            # Remote sunucuya bağlan
            await self._connect_to_remote()
            
            # Pipe'ları oluştur
            self.pipe_send = Pipe(
                self.client_reader,
                self.remote_writer,
                "SEND",
                self.config
            )
            
            self.pipe_recv = Pipe(
                self.remote_reader,
                self.client_writer,
                "RECV",
                self.config
            )
            
            # Her iki pipe'ı paralel çalıştır
            await asyncio.gather(
                self.pipe_send.start(),
                self.pipe_recv.start(),
                return_exceptions=True
            )
            
        except ProxyConnectionError as e:
            Console.log(f"❌ Bağlantı hatası: {e}", "ERROR")
        except asyncio.CancelledError:
            Console.log("⚠️ Client işlemi iptal edildi", "WARNING")
        except Exception as e:
            Console.log(f"❌ Beklenmedik hata: {e}", "ERROR")
        finally:
            await self.close()
    
    async def _connect_to_remote(self):
        """Remote sunucuya bağlan"""
        try:
            remote_host = self.config.REMOTE_HOST
            remote_port = self.config.REMOTE_PORT
            
            self.remote_reader, self.remote_writer = await asyncio.wait_for(
                asyncio.open_connection(remote_host, remote_port),
                timeout=10.0
            )
            
            Console.log(
                f"✅ Remote bağlantısı kuruldu: {remote_host}:{remote_port}",
                "SUCCESS"
            )
            
        except asyncio.TimeoutError:
            raise ProxyConnectionError(
                f"Remote sunucuya bağlanma timeout: {remote_host}:{remote_port}"
            )
        except ConnectionRefusedError:
            raise ProxyConnectionError(
                f"Remote sunucu bağlantısı reddedildi: {remote_host}:{remote_port}"
            )
        except Exception as e:
            raise ProxyConnectionError(f"Remote bağlantı hatası: {e}")
    
    async def close(self):
        """Bağlantıları kapat"""
        try:
            if self.remote_writer:
                self.remote_writer.close()
                await self.remote_writer.wait_closed()
        except Exception as e:
            logger.debug(f"Remote writer kapatma hatası: {e}")
        
        try:
            if self.client_writer:
                self.client_writer.close()
                await self.client_writer.wait_closed()
        except Exception as e:
            logger.debug(f"Client writer kapatma hatası: {e}")