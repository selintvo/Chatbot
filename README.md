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
- Oyuncuya Göre Öner
- Film Yılına Göre Öner
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
- **Neden Google Gemini?** Proje kapsamına uygun, güçlü, Türkçe dil desteği ve gelişmiş bağlamsal anlama yeteneği sunar.
- **Intent Sınıflandırma:** SVM (Support Vector Classifier) kullanıldı. TF-IDF ile metinler sayısallaştırıldı.
- **Neden SVM?** Basit, etkili ve küçük/orta büyüklükte veri setlerinde iyi sonuç verir.
- **Chatbot LLM Modeli:** Google Gemini (models/gemini-1.5-flash-latest)
- **Embedding Modeli:** GoogleGenerativeAIEmbeddings (models/embedding-001)
- API anahtarı `.env` dosyasından güvenli şekilde yüklendi.

> Modelle ilgili tüm detaylı açıklamalar ve kod içi yorumlar, `app.py` dosyasında ilgili kod blokları içerisinde açıklanmıştır.

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

Aşağıda birkaç örnekle chatbotun nasıl cevaplar verdiği yer almaktadır:

| Kullanıcı Sorusu | Modelin Cevabı |
|----------|----------|
| ![1](https://github.com/user-attachments/assets/a47a1478-2005-4160-8415-93bac74fbe9b) | ![2](https://github.com/user-attachments/assets/b8f19fa9-d517-4d8d-ac36-fc071d668978) |

| Kullanıcı Sorusu | Modelin Cevabı |
|----------|----------|
| ![3](https://github.com/user-attachments/assets/09399116-7b14-40ba-91ff-6873eb0ac381) | ![4](https://github.com/user-attachments/assets/b0d9e4b9-510b-4f1b-bd26-38992741b552) |

| Kullanıcı Sorusu | Modelin Cevabı |
|----------|----------|
| ![5](https://github.com/user-attachments/assets/acbf5b7d-2d24-4edb-ba19-c741f7bda82b) | ![6](https://github.com/user-attachments/assets/4488f260-fdac-48ff-aeba-3919d086caa1) |

---

## Kurulum ve Çalıştırma
1. Proje dosyalarını indiriniz.
2. `.env` dosyasına Google Gemini API anahtarınızı ekleyiniz.
3. Gerekli paketleri yükleyiniz.
4. Streamlit uygulamasını çalıştırınız: streamlit run app.py
5. Tarayıcıda açılan sayfadan chatbot ile etkileşime geçebilirsiniz.
   
