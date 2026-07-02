# 🎮 SonOyuncu Lag Client v2.0

Modern Python sürümü ile yeniden yazılan lag client'i. 

## 📋 Gereksinimler

- Python 3.8+
- pip paket yöneticisi
- Windows/Linux/Mac

## 🚀 Kurulum

### Adım 1: Repository'yi klonla

git clone https://github.com/iAlperenS/sonoyuncu-lag-client.git
cd sonoyuncu-lag-client
Adım 2: Gerekli paketleri kur

pip install -r requirements.txt

Adım 3: SonOyuncu'ya sunucu ekle
SonOyuncu launcher'ı aç
Sunucu ekle: 127.0.0.1:8080
Bağlan
Adım 4: Lag Client'i başlat

python main.py

⌨️ Kontrol Tuşları
Tuş	Fonksiyon
H	Lag Aç/Kapat
P	İstatistikler
Q	Çık
⚙️ Ayarlama
config.json dosyasını düzenle:
{
  "LAG_AMOUNT": 500,        // Temel lag (ms)
  "ADAPTIVE_LAG_ENABLED": true,  // Adaptif lag
  "VARIABLE_LAG_ENABLED": true   // Değişken lag
}

🔧 Hosts Dosyası Düzeltme
Windows'ta hata alırsan hosts dosyasını düzenle:

Notepad'i yönetici olarak aç
Şu dosyayı aç: C:\Windows\System32\drivers\etc\hosts
En sona ekle:
text

Kodu kopyala
127.0.0.1 mc.sonoyuncu.network
127.0.0.1 sonoyuncu.network

Kaydet ve kapat
🐛 Sorun Giderme
Port Hatası
# Port kullanımını kontrol et
netstat -ano | findstr :8080

# Port'u açmaya çalışıyorsan:
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=127.0.0.1 connectport=25565 connectaddress=mc.sonoyuncu.network

Bağlantı Kurulamıyor
Firewall kontrolü: Windows Defender duvarını kapat
İnternet: Stabil bağlantı olduğundan emin ol
SonOyuncu: Server aktif mi kontrol et
📊 Özellikler
✅ Düşük gecikme ile stabil bağlantı

✅ Akıllı lag mekanizması

✅ Anti-spam koruması

✅ Renkli konsol çıktısı

✅ Detaylı loglama