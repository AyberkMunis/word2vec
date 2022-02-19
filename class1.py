import re
import time
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
url ='https://raw.githubusercontent.com/sgsinclair/trombone/master/src/main/resources/org/voyanttools/trombone/keywords/stop.tr.turkish-lucene.txt'
data = pd.read_csv(url)
stpwrds = set(data[2:].iloc[:, 0].values)
word_vectors = KeyedVectors.load_word2vec_format('trmodel', binary=True)
sentences1 = ["Fenerbahçe-Çaykur Rizespor maçına Atilla Szalai damgası! Vitor Pereira'nın o kararı",
             "Fenerbahçe, Süper Lig'in 15. haftasında Çaykur Rizespor'u 4-0 mağlup ederek maç fazlasıyla ikinci sıraya yükseldi",
             'Galatasaray Lazio hazırlıklarına başladı',
             'Son dakika haberi: 5 Aralık corona virüsü tablosu ve vaka sayısı Sağlık Bakanlığı tarafından açıklandı!',
             'Bakan Akar, Katar Savunma Bakanı Atiyye ile görüştü']
class w2v():
    def vectorize(self,cumle,stpwrds=stpwrds):
        nokta = [".", ",", ":", ';', "!", "...", "?", "/", "-","[","]","(",")" ]
        for i in nokta:
            cumle = cumle.replace(i, " ")
        words = cumle.split()
        try:
            for i in words:
                words[i] = int(i)
        except:
            pass
        wrds = []
        for i in words:
            if i in stpwrds or i.isdigit() == True:
                pass
            else:
                if "'" in i:
                    nw = i.split("'")
                    wrd = word_vectors[nw[0].lower()].reshape(1, -1)
                    wrds.append(wrd)
                else:
                    wrd = word_vectors[i.lower()].reshape(1, -1)
                    wrds.append(wrd)
        mean=sum(wrds)/len(wrds)
        return mean
    def sentence(self,sentences):
        sentences=sentences.replace("\n","")
        sentences=sentences.split(",,")
        if len(sentences)==1 and "" in sentences:
            return "Please write something"
        for i in range(len(sentences)):
            sentences[i]=sentences[i].strip()
        vectors=[]
        for i in sentences:
            vectors.append(self.vectorize(i))
        arr=[]
        for x in vectors:
            for y in vectors:
                arr.append(cosine_similarity(x,y))
        arr=np.array(arr)
        arr=arr.reshape(len(sentences),len(sentences))
        normal=list(arr.sum(axis=1))
        maxi=list(arr.sum(axis=1))
        maxi.sort(reverse=True)
        if len(sentences)>1:
            final1=[sentences[normal.index(maxi[0])],sentences[normal.index(maxi[1])]]
        else:
            final1 =[sentences[normal.index(maxi[0])]]
        return final1
