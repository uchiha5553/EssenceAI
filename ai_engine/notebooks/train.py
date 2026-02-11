import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. VERİYİ YÜKLE
# Terminalde 'Parfum_AI_Project' klasöründe olduğun için yol bu şekilde olmalı
try:
    dataFrame = pd.read_excel("ai_engine/data/egitim.xlsx")
    # print("egitim.xlsx başarıyla okundu.")
except FileNotFoundError:
    print("HATA: Dosya bulunamadı! Lütfen terminalde 'Parfum_AI_Project' klasöründe olduğundan emin ol.")

# 2. ÖZELLİKLERİ BİRLEŞTİR
# Boş hücreleri (NaN) boş metinle dolduruyoruz ki toplama işlemi hata vermesin
dataFrame['birlesik_ozellikler'] = (
    dataFrame['Ust_Nota'].fillna('') + " " + 
    dataFrame['Orta_Nota'].fillna('') + " " + 
    dataFrame['Alt_Nota'].fillna('') + " " + 
    dataFrame['Genel_Karakter'].fillna('')
)

# 3. YAPAY ZEKA MODELİNİ OLUŞTUR
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(dataFrame['birlesik_ozellikler'])
similarity = cosine_similarity(tfidf_matrix)

print("--- Benzerlik Matrisi Oluşturuldu ---")

# 4. KAYIT İŞLEMLERİ
export_yolu = "ai_engine/exports/"

# Klasör yoksa oluştur
if not os.path.exists(export_yolu):
    os.makedirs(export_yolu)

# Benzerlik matrisini (pkl) kaydet
with open(export_yolu + "similarity_model.pkl", "wb") as dosya:
    pickle.dump(similarity, dosya)

# Parfüm listesini (xlsx) kaydet
dataFrame.to_excel(export_yolu + "parfum_listesi.xlsx", index=False)

# print("İşlem Tamam! Modeller 'ai_engine/exports' klasörüne kaydedildi.")