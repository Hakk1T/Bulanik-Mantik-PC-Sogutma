# Bulanık Mantık - Akıllı Performans PC Soğutma Kontrolcüsü 🖥️❄️

Bu proje, Bulanık Mantık (Fuzzy Logic) dersi dönem projesi kapsamında geliştirilmiş, yüksek performanslı bilgisayarlar için akıllı bir soğutma kontrol sistemidir. Klasik eşik değerli (threshold) soğutma sistemlerinin aksine, işlemci (CPU), ekran kartı (GPU) ve kasa içi sıcaklıklarını eş zamanlı değerlendirerek fan hızını yumuşak ve optimum düzeyde ayarlar.

## 🚀 Özellikler
* **Çoklu Giriş Parametreleri:** CPU Sıcaklığı, GPU Sıcaklığı ve Kasa İçi Sıcaklık.
* **Bulanık Çıkarım Sistemi:** 15 farklı kuraldan oluşan kapsamlı kural tabanı.
* **Durulaştırma:** Ağırlık Merkezi (Centroid) metodu ile hassas fan hızı (% RPM) hesaplama.
* **Etkileşimli Arayüz:** Streamlit tabanlı, anlık hesaplama yapabilen ve üyelik fonksiyonlarını / kural aktivasyonlarını grafiksel olarak sunan web arayüzü.

## 🛠️ Kullanılan Teknolojiler
* Python 3.x
* `scikit-fuzzy` (Bulanık mantık motoru)
* `Streamlit` (Web arayüzü)
* `NumPy` & `Matplotlib` (Hesaplama ve görselleştirme)

## ⚙️ Kurulum ve Çalıştırma

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/Hakk1T/Bulanik-Mantik-PC-Sogutma.git](https://github.com/Hakk1T/Bulanik-Mantik-PC-Sogutma.git)
   cd Bulanik-Mantik-PC-Sogutma