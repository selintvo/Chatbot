import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.linear_model import LogisticRegression 
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, classification_report  
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
import os

# Ortam değişkenlerini yükle (.env içindeki API anahtarı için)
load_dotenv()

# Streamlit başlık
st.title("🎬 Film Öneri Chatbotu (Gemini)")

# Excel veri kümesini yükle
df = pd.read_excel("film_chatbot_veri_seti.xlsx")

# Metin ve hedef (intent) sütunlarını al
X = df['text']
y = df['intent']

# Veri setini %80 train %20 test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

# Metinleri sayısal forma çevirmek için TF-IDF vektörleştirici
vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# SVC modeli ile intent sınıflandırma
clf = SVC(kernel='linear', C=1, probability=True, random_state=0)
clf.fit(X_train_tfidf, y_train)

# Test setinde tahmin yap
y_pred = clf.predict(X_test_tfidf)

# Accuracy, Precision, Recall, F1 hesapla
accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)

print("📊 Intent Sınıflandırma Performansı (SVC)")
print(f"Accuracy: {accuracy:.3f}")          
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-Score: {f1:.3f}")

# Excel'deki text-intent verilerini Document yapısına dönüştür
docs = [
    Document(page_content=row['text'], metadata={"intent": row['intent']})
    for _, row in df.iterrows()
]

# Metinleri parçalara ayır
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(docs)

# Embedding modeli (Gemini)
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Vektör veritabanı (Chroma ile)
vectorstore = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    persist_directory="./chroma_db_film"
)

# Retriever
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# LLM (Gemini Pro)
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    temperature=0.1,
    max_tokens=500
)

# Sistem prompt'u
system_prompt = (
    "Sen bir film öneri asistanısın. Kullanıcının niyetine göre ona film önerisinde bulunacaksın. "
    "Eğer kullanıcı ne tür film istediğini açık belirtmişse buna göre öneride bulun. "
    "Eğer belirli bir oyuncu veya duygu belirtmişse, buna göre film öner. "
    "Önerdiğin filmi sadece isim vermekle kalma, filmin konusunu, neden önerdiğini, önemli oyuncuları ve türünü de kısaca açıkla.\n\n"
    "{context}"
)

# Prompt şablonu
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

# RAG zinciri
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Kullanıcıdan giriş al
query = st.chat_input("Nasıl bir film arıyorsun?")

if query:
    with st.spinner("Film aranıyor..."):
        try:
            response = rag_chain.invoke({"input": query})
            st.success("🎥 Film Önerisi:")
            st.write(response["answer"])
        except Exception as e:
            st.error(f"❌ Hata oluştu: {e}")