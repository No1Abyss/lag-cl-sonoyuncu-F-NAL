"""
Pipe - Paketleri iletir ve lag uygular
Bu sistem tüm lag mekanizmasının merkezi
"""

import asyncio
import time
from typing import Optional
from utils.logger import Logger
from utils.config import Config
from utils.console import Console

logger = Logger("PIPE")

class Pipe:
    """
    Paketleri iletir ve lag mekanizmasını uygular
    İki yön: SEND (Client -> Server), RECV (Server -> Client)
    """
    
    def __init__(self, reader, writer, direction: str, config: Config):
        self.reader = reader
        self.writer = writer
        self.direction = direction  # "SEND" veya "RECV"
        self.config = config
        self.packet_count = 0
        self.total_bytes = 0
        self.last_packet_time = time.time()
        
    async def start(self):
        """Pipe'ı başlat ve paketleri işle"""
        try:
            while not self.reader.at_eof():
                # Paket oku
                packet_data = await asyncio.wait_for(
                    self.reader.read(4096),
                    timeout=30.0
                )
                
                if not packet_data:
                    break
                
                # Paket istatistikleri
                self.packet_count += 1
                self.total_bytes += len(packet_data)
                
                # Lag uygula
                await self._apply_lag()
                
                # Paket gönder
                self.writer.write(packet_data)
                await self.writer.drain()
                
                # Debug log
                if self.packet_count % 100 == 0:
                    logger.debug(
                        f"{self.direction}: {self.packet_count} paket, "
                        f"{self.total_bytes} bytes"
                    )
                    
        except asyncio.TimeoutError:
            Console.log(f"⚠️ {self.direction} timeout", "WARNING")
        except asyncio.CancelledError:
            logger.debug(f"{self.direction} iptal edildi")
        except Exception as e:
            logger.error(f"{self.direction} hatası: {e}")
        finally:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except:
                pass
    
    async def _apply_lag(self):
        """Lag mekanizmasını uygula"""
        
        # Temel lag
        if self.config.LAG_ENABLED:
            await asyncio.sleep(self.config.LAG_AMOUNT / 1000)
        
        # Adaptif lag (ping değişimine göre)
        if self.config.ADAPTIVE_LAG_ENABLED:
            adaptive_delay = self._calculate_adaptive_lag()
            await asyncio.sleep(adaptive_delay)
        
        # Variable lag (değişken gecikme)
        if self.config.VARIABLE_LAG_ENABLED:
            variable_delay = self._calculate_variable_lag()
            await asyncio.sleep(variable_delay)
        
        # Spam koruma (flood delay)
        if self.config.ANTI_SPAM_ENABLED:
            await self._apply_anti_spam_delay()
    
    def _calculate_adaptive_lag(self) -> float:
        """Adaptif lag hesapla"""
        current_time = time.time()
        time_diff = current_time - self.last_packet_time
        self.last_packet_time = current_time
        
        # Hızlı paket gelmişse daha fazla lag uygula
        if time_diff < 0.05:  # 50ms'den hızlı
            return self.config.ADAPTIVE_LAG_AMOUNT / 1000
        
        return 0
    
    def _calculate_variable_lag(self) -> float:
        """Değişken lag hesapla (rastgele)"""
        import random
        min_lag = self.config.VARIABLE_LAG_MIN / 1000
        max_lag = self.config.VARIABLE_LAG_MAX / 1000
        return random.uniform(min_lag, max_lag)
    
    async def _apply_anti_spam_delay(self):
        """Spam/flood koruması"""
        if self.packet_count % 10 == 0:  # Her 10 pakette bir
            await asyncio.sleep(0.1)  # 100ms delay