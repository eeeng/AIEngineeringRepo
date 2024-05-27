import requests
import spacy
import json

#nlp modelini googledan cekiyoruz ve yüklüyoruz
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"]) #spacy metin isleme icin altlik gibi davransin
    nlp = spacy.load("en_core_web_sm")  #webden veri alma 

# Anahtar kelimelerle genel konuyu belirleme
def genelTarama(text):
    fizikTerimleri = ['Kuantum mekanigi', 'Parcacik fizigi', 'Dalga kilavuzlama', 'Schrodinger']
    teknolojiTerimleri = ['Kuantum Bilgisayarlar', 'Kuantum Kriptografisi', 'Kuantum İletisimleri']
    
    fizikSkor        = sum(1 for word in fizikTerimleri if word in text.lower())
    teknolojiSkor    = sum(1 for word in teknolojiTerimleri if word in text.lower())
    
    if fizikSkor > teknolojiSkor:
        return 'fizik'
    
    elif teknolojiSkor > fizikSkor:
        return 'teknoloji'
    
    else:
        return 'None'

# Alt konuları belirleme
def spesifikTara(text):
    if 'Kuantum Bilgisayarlar' in text.lower():
        return 'Kuantum Bilgisayarlar'
    
    elif 'Kuantum mekanigi' in text.lower():
        return 'Kuantum mekanigi'
    
    elif 'Kuantum Kriptografisi' in text.lower():
        return 'Kuantum Kriptografisi'
    
    elif 'Kuantum İletisimleri' in text.lower():
        return 'Kuantum İletisimleri'
    

    else:
        return 'OTHER'

# İnternetten bilgi toplama (örneğin Wikipedia API kullanımı)
def bilgiAl(topic):
    search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        return data.get('extract', 'No information found')
    else:
        return 'Failed to retrieve information'

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    results = {}
    
    text = input("Bir metin girin (örneğin kuantum hakkinda): ")
    genelKonu = genelTarama(text)
    results['genelKonu'] = genelKonu

    spesifikKonu = spesifikTara(text)
    results['spesifikKonu'] = spesifikKonu

    information = bilgiAl(spesifikKonu)
    results['information'] = information
    
    save_to_json(results, 'sonuc2.json')
    print("Sonuclar 'sonuc2.json' dosyasina kaydedildi.")

#Kullanicidan metin alsin
#Genel konuyu belirlesin
#Alt konuyu belirlesin
#İnternetten bilgi toplasin
#Sonucları json formatnda kaydetsin

if __name__ == "__main__":
    main()
