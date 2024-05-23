import json
import requests
from nltk.metrics import jaccard_distance
from nltk.tokenize import word_tokenize

# Wikipedia API'sinden metin verisi çekme

def wikiTest(metin):
    url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{topic}" # apiye istek yap
    response = requests.get(url)


    # İstek başarılıysa veriyi JSON olarak dön
    if response.status_code == 200:
        data = response.json()
        if 'extract' in data:
            return data['extract']
        

    # İstek başarısız olursa None dön
    return None

# Metinler arasındaki benzerliği hesapla
def benzerlik(text1, text2):
    tokens1 = set(word_tokenize(text1))
    tokens2 = set(word_tokenize(text2))
    similarity = 1 - jaccard_distance(tokens1, tokens2)
    return similarity

# Kullanıcıdan bir konu adı girmesini iste
topic = input("Bir konu adi girin: ")

# Wikipedia'dan metin verisi çekme
fromWiki = wikiTest(topic)

if fromWiki:
    # Kullanıcıdan bir metin girmesini iste
    user_text = input("Bir metin girin: ")
    
    # Metinler arasındaki benzerliği hesapla
    similarity = benzerlik(fromWiki, user_text)
    
    # Sonuçları JSON formatında hazırla
    result = {
        "topic": topic,
        "wikipedia_text": fromWiki,
        "user_text": user_text,
        "similarity": similarity
    }
    
    # Sonucu JSON dosyasına kaydet
    with open("DB.json", "w") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print("Sonuçlar 'DB.json' dosyasina kaydedildi.")

    
else:
    print("Belirtilen konu için Wikipedia'dan metin verisi bulunamadi.")
