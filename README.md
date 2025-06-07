# Film Öneri Chatbotu (Gemini)

## Proje Özeti
Bu proje, yapay zekâ destekli bir chatbot geliştirme sürecini kapsamaktadır. Kullanıcıların film önerisi almak için doğal dilde sorularını anlayan ve yanıtlayan bir chatbot tasarlanmıştır. Projede Google Gemini LLM modeli kullanılarak chatbot eğitilmiş ve intent sınıflandırması SVM modeli ile gerçekleştirilmiştir.

---

## Proje Konusu ve Gerekçe
Film öneri chatbotu seçilmesinin nedeni, kullanıcıların tercih ettikleri film türleri, oyuncular veya duygulara göre hızlı ve doğru öneriler alabilmeleridir. Böylece kullanıcı deneyimi artırılmış ve kişiselleştirilmiş öneri sağlanmıştır.

---

## Chatbot Akışı
Chatbot, kullanıcının aşağıdaki gibi niyetlerine göre yanıt vermektedir:
- Selamlama (Greeting)
- Vedalaşma (Goodbye)
- Film Öner 
- Film Puanı Sor
- Film Süresi Sor
- Platforma Göre Öner
- ...

Kullanıcı mesajı alındıktan sonra:
1. Kullanıcının isteği intent sınıflandırma modeliyle analiz edilir.
2. Benzer geçmiş sorgular vektör veritabanından çekilir.
3. Google Gemini LLM modeli, sorgu ve bağlamı kullanarak öneriyi oluşturur.
4. Kullanıcıya öneri metni olarak iletilir.

---

## Veri Seti
- Veri formatı: Excel (.xlsx)
- Satır sayısı: 1000 örnek (intent ve text içeren)
- Örnek yapı:

| intent   | text                          |
| -------- | ----------------------------------- |
| Greeting | Merhaba, size nasıl yardımcı olabilirim? |
| Goodbye  | Görüşmek üzere, iyi günler!         |
| Film_Type| Aksiyon türünde film önerir misin?  |

- Veri, kullanıcı niyetlerini temsil edecek şekilde etiketlenmiştir.

---

## Model Seçimi ve Eğitim
- **Intent Sınıflandırma:** SVM (Support Vector Classifier) kullanıldı. TF-IDF ile metinler sayısallaştırıldı.
- **Neden SVM?** Basit, etkili ve küçük/orta büyüklükte veri setlerinde iyi sonuç verir.
- **Chatbot LLM Modeli:** Google Gemini (models/gemini-1.5-flash-latest)
- **Embedding Modeli:** GoogleGenerativeAIEmbeddings (models/embedding-001)
- **Neden Google Gemini?** Proje kapsamına uygun, güçlü, Türkçe dil desteği ve gelişmiş bağlamsal anlama yeteneği sunar.
- API anahtarı `.env` dosyasından güvenli şekilde yüklendi.

---

## Performans Değerlendirmesi
Intent sınıflandırma modeli test setinde aşağıdaki performans değerlerini almıştır:

| Metrik    | Değer  |
| --------- | ------ |
| Accuracy  | 0.910   |
| Precision | 0.841   |
| Recall    | 0.910   |
| F1-Score  | 0.874   | 

Metrikler, scikit-learn kütüphanesi kullanılarak hesaplanmıştır.

---

## Uygulama Arayüzü
- Streamlit kullanılarak basit ve kullanıcı dostu bir web arayüzü hazırlanmıştır.
- Kullanıcı, arayüz üzerinden film tercihini doğal dilde girer.
- Chatbot, Gemini modeli ile öneriyi oluşturur ve ekranda gösterir.
- Arayüz akıcı ve hızlıdır, kullanıcı deneyimini ön planda tutar.

---

## Kurulum ve Çalıştırma
1. Proje dosyalarını indiriniz.
2. `.env` dosyasına Google Gemini API anahtarınızı ekleyiniz.
3. Gerekli paketleri yükleyiniz.
4. Streamlit uygulamasını çalıştırınız: streamlit run app.py
5. Tarayıcıda açılan sayfadan chatbot ile etkileşime geçebilirsiniz.
   
