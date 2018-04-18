import re
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.display.max_colwidth = 8000

# TR: �rnek T�rk�e dok�manlar 
# EN: Sample documents in Turkish
docs = ['A��klama projenin ortaklar�ndan Rus enerji devi Gazprom dan geldi. Y�ll�k 63 milyar metrek�p enerji',
        'ilk g�n�ndeki 20 yar�� heyecanl�yd�, 109 puan toplayan T�rkiye, 12 �lke aras�nda 9. oldu ve yar�� tamamland�',
        'Cortanan�n yeni i�letim sistemi Windows 10 un �nemli bir par�as� oldu�unu belirten Microsoft ; Google Android ve iOS cihazlar�ndaki Dijital',
        'Teknoloji devi Google, Android in MMM s�r�m�yle birlikte bir �ok sistemsel hatas�n�n d�zeltilece�ini',
        'Siroz hastal��� ile ilgili detaylara dikkat �ekerek, sa�l�kl� bir karaci�ere sahip olmak hastal�k i�in',
        'Hastal�k �o�u kez y�llarca do�ru tan� konmamas� veya ciddiye al�nmamas� sebebi ile k�s�rla�t�r�c� etki yapabiliyor, kronik a�r�,',
        '�lk 4 etaptan galibiyetle ayr�lan 18 ya��ndaki Razgatl�o�lu, �talya daki yar��ta 3. s�ray� alarak ',
        'Helal g�da pazar� sanki 860 milyar dolar�n �zerinde'    
]
# TR: Dok�manlara ait s�n�flar 
# EN: Classes of documents
classes = ['ekonomi', 'spor', 'teknoloji', 'teknoloji', 'saglik', 'saglik', 'spor', 'ekonomi']

# TR: �zel karakterlerin d�n���m� 
# EN: Conversion of special Turkish characters to Latin forms
coding = {'�': 'c', '�': 'i', '�': 'u', '�': 's', '�': 'g', '�': 'o', '�': 'I' }
for i in range(len(docs)):
    for k, v in coding.items():
        docs[i] = docs[i].replace(k, v)

docs = np.array(docs)
df_docs = pd.DataFrame({'Dokuman': docs, 
                        'Sinif': classes})
df_docs = df_docs[['Dokuman', 'Sinif']]
#print (df_docs)

WPT = nltk.WordPunctTokenizer()
stop_word_list = nltk.corpus.stopwords.words('turkish')

def norm_doc(single_doc):
    # TR: Dok�mandan �zel karakterleri ve say�lar� at
    # EN: Remove special characters and numbers
    single_doc = re.sub(r'[^a-zA-Z\s]', '', single_doc, re.I|re.A)
    # TR: Dok�man� k���k harflere �evir
    # EN: Convert document to lowercase
    single_doc = single_doc.lower()
    single_doc = single_doc.strip()
    # TR: Dok�man� token'lar�na ay�r
    # EN: Tokenize documents
    tokens = WPT.tokenize(single_doc)
    # TR: Stop-word listesindeki kelimeler hari� al
    # EN: Filter out the stop-words 
    filtered_tokens = [token for token in tokens if token not in stop_word_list]
    # TR: Dok�man� tekrar olu�tur
    # EN: Reconstruct the document
    single_doc = ' '.join(filtered_tokens)
    return single_doc

norm_docs = np.vectorize(norm_doc) #like magic :)
normalized_documents = norm_docs(docs)
#print(normalized_documents)


# TR: 1.Terim Sayma Ad�mlar�
# EN: 1.Term Counting Steps
from sklearn.feature_extraction.text import CountVectorizer
BoW_Vector = CountVectorizer(min_df = 0., max_df = 1.)
BoW_Matrix = BoW_Vector.fit_transform(normalized_documents)
print (BoW_Matrix)

# TR: BoW_Vector i�erisindeki t�m �znitelikleri al
# EN: Fetch al features in BoW_Vector
features = BoW_Vector.get_feature_names()
print ("features[50]:" + features[50])
print ("features[52]:" +features[52])

BoW_Matrix = BoW_Matrix.toarray()
print(BoW_Matrix)
# TR: Dok�man - �znitelik matrisini g�ster
# EN: Print document by term matrice
BoW_df = pd.DataFrame(BoW_Matrix, columns = features)
#print(BoW_df)
#print(BoW_df.info())



# TR: 2.TFxIdf Hesaplama Ad�mlar�
# EN: 2.TFxIdf Calculation Steps
from sklearn.feature_extraction.text import TfidfVectorizer
Tfidf_Vector = TfidfVectorizer(min_df = 0., max_df = 1., use_idf = True)
Tfidf_Matrix = Tfidf_Vector.fit_transform(normalized_documents)
Tfidf_Matrix = Tfidf_Matrix.toarray()
print(np.round(Tfidf_Matrix, 3))
# TR: Tfidf_Vector i�erisindeki t�m �znitelikleri al
# EN: Fetch al features in Tfidf_Vector
features = Tfidf_Vector.get_feature_names()
# TR: Dok�man - �znitelik matrisini g�ster
# EN: Print document by term matrice
print(pd.DataFrame(np.round(Tfidf_Matrix, 3), columns = features))