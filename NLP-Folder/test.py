import json
import requests
from nltk.metrics import jaccard_distance
from nltk.tokenize import word_tokenize

# Wikipedia API'sinden metin verisi çekme

def wikiTest(metin):
    url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{metin}" # apiye istek yap
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
#Kullanıcıdan bir konu adı girmesini iste
#Wikipedia'dan metin verisi çekme

metin = input("Bir konu adi girin: ")
fromWiki = wikiTest(metin)

if fromWiki:
    user_text = input("Bir metin girin: ")   #Kullanciidan bir metin girmesini iste
        
    similarity = benzerlik(fromWiki, user_text) #metinler arasındaki benzerliği hesapla
    
    result = {                              #Sonuclari json olarak döndür
        "metin": metin,
        "wikipedia_text": fromWiki,
        "user_text": user_text,
        "similarity": similarity
    }
  
    with open("DB.json", "w") as f:                             #sonuclari kaydet DB olarak
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print("Sonuçlar 'DB.json' dosyasina kaydedildi.")

    
else:
    print("Belirtilen konu için Wikipedia'dan metin verisi bulunamadi.")
