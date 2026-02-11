from django.shortcuts import render
import pandas as pd
import pickle
import os
from django.conf import settings

# Dosya Yolları
BASE_DIR = settings.BASE_DIR
model_path = os.path.join(BASE_DIR, 'ai_models', 'similarity_model.pkl')
list_path = os.path.join(BASE_DIR, 'ai_models', 'parfum_listesi.xlsx')

# Modeli ve Listeyi Yükle
with open(model_path, 'rb') as f:
    similarity = pickle.load(f)

df = pd.read_excel(list_path)

def clean_name(name):
    # İsimdeki çizgileri kaldırır ve fazla boşlukları temizler
    return str(name).replace('-', ' ').strip().replace('  ', ' ')

def index(request):
    # Ana sayfaya ilk girişte veya yenilemede (GET) her şey sıfırlanır
    parfumler = sorted(df['Parfum_Adi'].dropna().apply(clean_name).unique())
    return render(request, 'index.html', {'parfumler': parfumler})

def recommend(request):
    parfumler_sirali = sorted(df['Parfum_Adi'].dropna().apply(clean_name).unique())
    
    # Sayfa yenilenirse (GET isteği) ana sayfaya temiz halini gönder
    if request.method == 'GET':
        return render(request, 'index.html', {'parfumler': parfumler_sirali})

    if request.method == 'POST':
        secilen_parfum = request.POST.get('parfum_adi', '').strip()
        
        try:
            # Geçici temizlenmiş bir DataFrame üzerinden eşleşme bul
            temp_df = df.copy()
            temp_df['Temiz_Ad'] = temp_df['Parfum_Adi'].apply(clean_name)
            
            search_name = clean_name(secilen_parfum)
            match = temp_df[temp_df['Temiz_Ad'] == search_name]
            
            if match.empty:
                return render(request, 'index.html', {'parfumler': parfumler_sirali})

            idx = match.index[0]
            
            # Benzerlik skorlarını hesapla
            distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
            
            oneriler_listesi = []
            for i in distances[1:6]:
                p_adi = df.iloc[i[0]]['Parfum_Adi']
                p_marka = df.iloc[i[0]]['Marka']
                
                oneriler_listesi.append({
                    'ad': clean_name(p_adi),
                    'marka': p_marka
                })
                
            return render(request, 'index.html', {
                'secilen': clean_name(secilen_parfum),
                'oneriler': oneriler_listesi,
                'parfumler': parfumler_sirali
            })
        except Exception as e:
            print(f"Hata: {e}")
            return render(request, 'index.html', {'parfumler': parfumler_sirali})
            
    return render(request, 'index.html', {'parfumler': parfumler_sirali})