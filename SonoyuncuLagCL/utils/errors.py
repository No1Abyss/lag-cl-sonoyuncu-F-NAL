"""
Custom Exception Sınıfları
"""

class ProxyError(Exception):
    """Proxy hatalarının ana sınıfı"""
    pass

class ProxyConnectionError(ProxyError):
    """Bağlantı hatası"""
    pass

class ProxyConnectionClosed(ProxyError):
    """Bağlantı kapalı"""
    pass

class PipeError(ProxyError):
    """Pipe işlem hatası"""
    pass

class ConfigError(ProxyError):
    """Konfigürasyon hatası"""
    pass

class PacketError(ProxyError):
    """Paket işleme hatası"""
    pass