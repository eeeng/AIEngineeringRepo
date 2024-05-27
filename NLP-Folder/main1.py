import requests
import spacy
import json

#nlp modelini googledan cekiyoruz ve yüklüyoruz
try:
    nlp = spacy.load("en_core_web_sm")

except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def metin_üret(text):
    dosya = nlp(text)
    topics = [chunk.text for chunk in dosya.noun_chunks]
    return topics

def search_books(topic):
    search_url = f"https://www.googleapis.com/books/v1/volumes?q={topic}"
    response = requests.get(search_url)
    if response.status_code == 200:
        books = response.json().get('items', [])
        return books
    else:
        return []

def cikarim(book):
    info = book.get('volumeInfo', {})
    baslik = info.get('baslik', 'N/A')
    yazar = info.get('yazar', ['N/A'])
    tanimlar = info.get('tanimlar', 'N/A')
    return {
        'baslik'    : baslik,
        'yazar'     : yazar,
        'tanimlar'  : tanimlar
    }

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    results = {}

    # Kullanıcıdan metinler alın
    text1 = input("İlk metni girin (kitaplar hakkinda): ")
    text2 = input("İkinci metni girin (bilim hakkinda): ")

    results['inputs'] = {'text1': text1, 'text2': text2}
    
    
    #Genel konulari belirslein
    topics1 = metin_üret(text1)
    topics2 = metin_üret(text2)
    genel_konular = topics1 + topics2
    
    results['genel_konular'] = genel_konular
    results['general_books'] = []

    
    print("Genel konulara göre bilimsel kitaplar:")     #Genel konulara göre kitapları arasin ve bilgi versin
    for topic in genel_konular:
        books = search_books(topic)
        for book in books:
            book_info = cikarim(book)
            results['general_books'].append(book_info)
            print(book_info)
    
    
    text3 = input("Daha spesifik bir metin girin: ")     #Daha spesifik konu için yeni metin aliyoruz
    results['inputs']['text3'] = text3
    specific_topic = metin_üret(text3)
    
    results['specific_topic'] = specific_topic
    results['specific_books'] = []

    
    print("Biyoloji hakkinda bilimsel kitaplar:")   #Spesifik bi konuya göre kitapları arasin ve bilgi versin
    for topic in specific_topic:
        books = search_books(topic)
        for book in books:
            book_info = cikarim(book)
            results['specific_books'].append(book_info)
            print(book_info)
    
    
    save_to_json(results, 'sonuc.json')     #Sonucları josn formatinda db olarak olustursun
    print("Sonuclar 'sonuc.json' dosyasina yönlendirildi.")

if __name__ == "__main__":
    main()

