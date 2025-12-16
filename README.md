# Dilimizin Zenginlikleri - Web Uygulaması

Bu proje, Türkçe kelime ve anlam eşleştirme oyununu web tabanlı bir uygulamaya dönüştürür.

## Özellikler

- 🎮 İnteraktif kelime-anlam eşleştirme oyunu
- 📊 Liderlik tablosu sistemi
- 🎯 Çoktan seçmeli sorular
- ⏱️ Süre takibi
- 📱 Mobil uyumlu tasarım
- 💾 Otomatik skor kaydetme

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
python app.py
```

3. Tarayıcınızda `http://localhost:5000` adresine gidin.

## Kullanım

1. Ana sayfada öğrenci adınızı ve okulunuzu girin
2. Soru sayısını seçin (5-25 arası)
3. Oyunu başlatın
4. Her soruda doğru anlamı seçin
5. Oyun sonunda skorunuz liderlik tablosuna eklenir

## Dosya Yapısı

```
├── app.py              # Ana Flask uygulaması
├── templates/          # HTML şablonları
│   ├── base.html      # Temel şablon
│   ├── index.html     # Ana sayfa
│   └── leaderboard.html # Liderlik tablosu
├── requirements.txt    # Python bağımlılıkları
├── kelime_havuzu.json # Kelime veritabanı (otomatik oluşur)
└── liderlik_tablosu.json # Skor veritabanı (otomatik oluşur)
```

## Özelleştirme

- `DEFAULT_WORDS` listesini düzenleyerek kelime havuzunu genişletebilirsiniz
- CSS stillerini değiştirerek görünümü özelleştirebilirsiniz
- Soru sayısı seçeneklerini `index.html` dosyasından değiştirebilirsiniz

## Teknik Detaylar

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Veri Depolama**: JSON dosyaları
- **Session Yönetimi**: Flask Sessions

## Geliştirme

Geliştirme modunda çalıştırmak için:
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python app.py
```