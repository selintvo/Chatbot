import streamlit as st
import pandas as pd
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
    "Aşağıda geçmiş sorgulardan alınan benzer örnekler (context) yer almakta. "
    "Eğer kullanıcı ne tür film istediğini açık belirtmişse buna göre öneride bulun. "
    "Eğer belirli bir oyuncu veya duygu belirtmişse, buna göre film öner. "
    "Sadece bir film öner, kısa ve anlaşılır cümlelerle yanıtla.\n\n"
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