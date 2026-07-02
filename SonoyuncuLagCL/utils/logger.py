"""
Logger - Dosyaya ve konsola loglama
"""

import logging
from pathlib import Path
from datetime import datetime

class Logger:
    """Sınıf bazlı logger"""
    
    _loggers = {}
    
    def __new__(cls, name: str):
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            
            # Log dosyasını oluştur
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # Handler'ları ekle
            fh = logging.FileHandler(
                log_dir / f"{datetime.now().strftime('%Y%m%d')}.log",
                encoding='utf-8'
            )
            ch = logging.StreamHandler()
            
            # Format
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            logger.addHandler(fh)
            logger.addHandler(ch)
            logger.setLevel(logging.DEBUG)
            
            cls._loggers[name] = logger
        
        return cls._loggers[name]
    
    @staticmethod
    def debug(msg): logging.debug(msg)
    @staticmethod
    def info(msg): logging.info(msg)
    @staticmethod
    def warning(msg): logging.warning(msg)
    @staticmethod
    def error(msg): logging.error(msg)