"""
Konfigürasyon Yöneticisi
"""

import json
import os
from typing import Optional
from pathlib import Path
from utils.console import Console

class Config:
    """Uygulamanın tüm ayarlarını yönetir"""
    
    # Proxy Ayarları
    LOCAL_IP: str = "127.0.0.1"
    LOCAL_PORT: int = 8080
    REMOTE_HOST: str = "mc.sonoyuncu.network"
    REMOTE_PORT: int = 25565
    
    # Lag Ayarları
    LAG_ENABLED: bool = True
    LAG_AMOUNT: int = 500  # millisecond
    
    # Adaptif Lag
    ADAPTIVE_LAG_ENABLED: bool = True
    ADAPTIVE_LAG_AMOUNT: int = 200
    
    # Değişken Lag
    VARIABLE_LAG_ENABLED: bool = True
    VARIABLE_LAG_MIN: int = 100
    VARIABLE_LAG_MAX: int = 300
    
    # Spam Koruma
    ANTI_SPAM_ENABLED: bool = True
    
    # Filtreleme
    FILTER_ENABLED: bool = False
    BLOCK_PACKETS: list = []
    
    # Otomatik Yönetim
    AUTO_ADJUST_LAG: bool = True
    
    # Diğer
    DEBUG_MODE: bool = True
    LOG_PACKETS: bool = False
    
    @classmethod
    def load_config(cls) -> 'Config':
        """Config dosyasından yükle veya varsayılanları kullan"""
        config_path = Path("config.json")
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Ayarları güncelle
                for key, value in data.items():
                    if hasattr(cls, key):
                        setattr(cls, key, value)
                
                Console.log("✅ Config dosyası yüklendi", "SUCCESS")
            except Exception as e:
                Console.log(f"⚠️ Config yükleme hatası: {e}", "WARNING")
        else:
            cls._create_default_config()
        
        return cls
    
    @classmethod
    def _create_default_config(cls):
        """Varsayılan config dosyası oluştur"""
        config_data = {
            "LOCAL_IP": cls.LOCAL_IP,
            "LOCAL_PORT": cls.LOCAL_PORT,
            "REMOTE_HOST": cls.REMOTE_HOST,
            "REMOTE_PORT": cls.REMOTE_PORT,
            "LAG_ENABLED": cls.LAG_ENABLED,
            "LAG_AMOUNT": cls.LAG_AMOUNT,
            "ADAPTIVE_LAG_ENABLED": cls.ADAPTIVE_LAG_ENABLED,
            "ADAPTIVE_LAG_AMOUNT": cls.ADAPTIVE_LAG_AMOUNT,
            "VARIABLE_LAG_ENABLED": cls.VARIABLE_LAG_ENABLED,
            "VARIABLE_LAG_MIN": cls.VARIABLE_LAG_MIN,
            "VARIABLE_LAG_MAX": cls.VARIABLE_LAG_MAX,
            "ANTI_SPAM_ENABLED": cls.ANTI_SPAM_ENABLED,
            "FILTER_ENABLED": cls.FILTER_ENABLED,
            "AUTO_ADJUST_LAG": cls.AUTO_ADJUST_LAG,
            "DEBUG_MODE": cls.DEBUG_MODE,
        }
        
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            Console.log("✅ Varsayılan config dosyası oluşturuldu", "SUCCESS")
        except Exception as e:
            Console.log(f"❌ Config oluşturma hatası: {e}", "ERROR")