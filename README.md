## Screenshots
<table>
  <tr>
    <td>Graf Görselleştirme Ekranı</td>
    <td>Kuyruk & BST İşlemleri</td>
    <td>Analiz Sonuçları</td>
  </tr>
  <tr>
    <td><img src="screenshots/ss1.jpeg" alt="Graf Görselleştirme Ekranı" width="300px"></td>
    <td><img src="screenshots/ss2.jpeg" alt="Kuyruk & BST İşlemleri" width="300px"></td>
    <td><img src="screenshots/ss3.jpeg" alt="Analiz Sonuçları" width="300px"></td>
  </tr>
</table>

# Yazarlar ve İşbirliği Analizi Projesi

Bu proje, akademik makalelerdeki yazarlar arasındaki işbirliği ilişkilerini graf veri yapısı ile modelleyip, analiz etmeyi amaçlamaktadır. Python'da pandas ile veri çekimi ve işlenmesi, Pyvis ile graf görselleştirmesi, HTML/JavaScript ile etkileşimli arayüz geliştirilmiştir. Proje boyunca, veri modelleme, algoritma geliştirme ve görselleştirme konularında kendimi geliştirdim.

## Proje Özeti

- **Tema:** Akademik işbirliği ağını graf modeliyle analiz ve görselleştirme
- **Temel İşlevler:**
  - Pandas ile Excel dosyasından yazar/makale verisi çekimi ve nesne oluşturma
  - Yazarlar arası ortak makale ilişkilerinden ağırlıklı, tıklanabilir ve dinamik bir graf oluşturma (Pyvis)
  - Düğümlerin (yazarların) makale sayısına göre boyut ve renk ile ayırt edilmesi
  - Kenarların, ortak makale sayısına göre ağırlıklandırılması
  - Zoom/kaydırma ve düğüme tıklayınca makale bilgisi gösterme
  - İsterlere (analiz adımlarına) göre:
    - En kısa yol bulma (iki yazar arasında)
    - İşbirliği yapılan yazarlar için kuyruk oluşturma
    - Kuyruktan BST (Binary Search Tree) oluşturma ve silme işlemleri
    - En çok işbirliği yapan yazarın bulunması
    - En uzun yol analizi
    - Tüm adımlar ve sonuçlar arayüzde görsel olarak gösteriliyor

## Kullanılan Teknolojiler ve Yöntemler

- **Python:** Veri çekimi ve işlenmesi (pandas), graf nesnelerinin oluşturulması
- **Pyvis:** Graf görselleştirmesi, HTML dosyasına etkileşimli çıktı alma
- **HTML / JavaScript:** Butonlar, textbox, arayüz dinamikliği, görsel analiz ve navigasyon
- **Veri Yapıları & Algoritmalar:** 
  - Graf (node/edge)
  - Kuyruk ve BST (ikili arama ağacı)
  - En kısa yol ve en uzun yol algoritması
  - Dinamik ağırlıklandırma ve görsel vurgulama

## Kazanımlarım

- Gerçek veriyle, graf veri yapısı kurma ve işbirliği ilişkilerini analiz etme yeteneği kazandım.
- Pandas ile veri çekme, işleme ve nesneye dönüştürme pratiği yaptım.
- Pyvis ve HTML/JS ile etkileşimli ve kullanıcı dostu bir görsel arayüz geliştirdim.
- Algoritma tasarımı (en kısa yol, en uzun yol, BST, kuyruk) ve adım adım analiz sunumu konularında ilerledim.
- Görselleştirme ile teknik sunum ve raporlama becerimi güçlendirdim.
- Tıklanabilir düğümler, makale detayları, dinamik kuyruk ve BST işlemleriyle, veri yapılarının gerçek kullanımını deneyimledim.

## Sonuç

Bu projede, akademik işbirliği verilerini graf olarak modelleyip, algoritmik analizlerle görselleştirdim. Veri işleme, graf ve veri yapısı algoritmaları, ve görsel arayüz geliştirme konularında hem teknik hem analitik yönden kendimi ileriye taşıdım.

---

*Not: Bu proje teknik kazanımlarımı ve veri analizi yaklaşımımı göstermek amacıyla hazırlanmıştır. Kurulum ve kullanım talimatı yerine, yapılan işin genel yapısı ve teknik altyapısı öne çıkarılmıştır.*
