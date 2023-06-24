import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from google_play_scraper import app
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import spacy
import pandas as pd
from nltk import ngrams
import re

def kelimecevir(kelime):
    kelime = kelime.split()
    a = len(kelime)
    b = ""
    if a == 1:
        kelime = kelime[0]
        return str(kelime)
    elif a == 2:
        kelime.insert(1, "%20")
        kelime = "".join(kelime)
        return kelime
    elif a == 3:
        kelime.insert(1, "%20")
        kelime.insert(3, "%20")
        kelime = "".join(kelime)
        return kelime
    elif a == 4:
        kelime.insert(1, "%20")
        kelime.insert(3, "%20")
        kelime.insert(5, "%20")
        kelime = "".join(kelime)
        return kelime

def sembolkaldır(k):
    symbols = "!–\"#$%&()*”+✓-./“:$;<=>😊?@[\]^_😉`-{|·}~\n,.‘'🥰’➡️&🏆💎🎉📱📝🎨🖼🏷📌💯📷🌈⭐☆👍🎊✅🔥✔📣★•—◆®❤●"
    for i in symbols:
        k = k.replace(i, '').replace("  ", " ")
    return k

def ngram(text):
    ngram_tek=[]
    for i in range(1,4):
        if i == 1:    
            n_grams = ngrams((text).split(), i)
            for a in n_grams:
                ngram_tek.append((a))
        if i == 2:    
            n_grams = ngrams((text).split(), i)
            for a in n_grams:
                ngram_tek.append(" ".join((a)))
        if i == 3:    
            n_grams = ngrams((text).split(), i)
            for a in n_grams:
                ngram_tek.append(" ".join((a)))

    return ngram_tek

def main():
    st.title("Google Play Scraper")
    d = st.text_input("Write target keyword:")

    if st.button("Scrape Data"):
        c = webdriver.ChromeOptions()
        c.add_argument("--incognito")
        c.add_argument("--headless")

        url = "https://play.google.com/store/search?q=" + kelimecevir(d) + "&c=apps&hl=en&gl=US"
        url2 = "https://play.google.com/store/search?q=" + d.replace(" ", "%20") + "&c=apps&hl=en&gl=US"

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=c)
        driver.get(url)

        links_games = []

        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if "details?id" in elem.get_attribute("href"):
                links_games.append((elem.get_attribute("href")))

        links_games = list(dict.fromkeys(links_games))
        driver.close()

        stop_words = stopwords.words('english')
        stop_words.extend(['we', 'you', 'com', '$', 'from', 'subject', 're', 'edu', 'use', 'best', 'us', "puzzle", "mojo", "unfold", "mojito",
                           "you", "your", "a", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "about", "above", "after", "again", "against"])

        # Rest of the code...

        
        def sembolkaldır(k):
            symbols = "!–\"#$%&()*”+✓-./“:$;<=>😊?@[\]^_😉`-{|·}~\n,.‘'🥰’➡️&🏆💎🎉📱📝🎨🖼🏷📌💯📷🌈⭐☆👍🎊✅🔥✔📣★•—◆®❤●"
            for i in symbols:
                k = k.replace(i, '').replace("  ", " ")
            return k
        
        link_games_2 = [m.split("=")[1] for m in links_games]
        
        list_all_elements = []
        başlıklar = []
        kısabaşlık = []
        uzun_açıklama = []
        links_games_1 = []
        developer_mail = []
        reviews_meta=[]
        comments=[]
        
        def metadadatav2():
            for i in link_games_2:
                result = app(
                    i,
                    lang='en',  # defaults to 'en'
                    country='us'
                )  # defaults to 'us'
                title = (result["title"])
                score = (result["score"])
                ratings = (result["ratings"])
                reviews = (result["reviews"])
                short_desc = (result["summary"])
                install = (result["installs"])
                comment = (result["comments"])
                # description=(BeautifulSoup(result["description"], "lxml").text) #orjinal hali burada
                description = (
                    " ".join((BeautifulSoup(result["description"], "lxml").text).split()))
                long_len = len(description.split())
                developer_mail.append(result["developerEmail"])
                tümveri = [title, short_desc, description,
                           long_len, install, score, ratings, reviews]
                list_all_elements.append(tümveri)
                başlıklar.append(title)
                kısabaşlık.append(short_desc)
                comments.append(comment)
                uzun_açıklama.append(description)
        
        
                metadadatav2()
        
        
        docs = []
        docs = uzun_açıklama[0:10]
        docs_küçük=[]
        docs_küçük = [docs_küçük.append(d.lower()) for d in docs]
        doc_uzun_açıklamalar_tüm = " ".join(docs)
        doc_uzun_açıklamalar_tüm_nonsembol = re.sub(r'\W+', ' ', doc_uzun_açıklamalar_tüm)
        doc_uzun_açıklamalar_tüm_nonsembol_split = doc_uzun_açıklamalar_tüm_nonsembol.split()
        doc_uzun_açıklamalar_tüm_nonsembol_non_stop = [word for word in doc_uzun_açıklamalar_tüm_nonsembol_split if word.lower() not in stop_words]
        doc_uzun_açıklamalar_tüm_nonsembol_non_stop=" ".join(doc_uzun_açıklamalar_tüm_nonsembol_non_stop)
        
        
        def ngram(text):
            ngram_tek=[]
            for i in range(1,4):
                if i == 1:    
                    n_grams = ngrams((text).split(), i)
                    for a in n_grams:
                        ngram_tek.append((a))
                if i == 2:    
                    n_grams = ngrams((text).split(), i)
                    for a in n_grams:
                        ngram_tek.append(" ".join((a)))
                if i == 3:    
                    n_grams = ngrams((text).split(), i)
                    for a in n_grams:
                        ngram_tek.append(" ".join((a)))
        
            return ngram_tek
            
                      
        tüm_data = ngram(doc_uzun_açıklamalar_tüm_nonsembol_non_stop.lower())
        
        # Remove symbols from tuples in the list
        cleaned_tüm_data = []
        
        for item in tüm_data:
            if (str(item).replace("(", "").replace(")", "").replace(",", "").replace("'", "")) not in stop_words:
                cleaned_tüm_data.append((str(item).replace("(", "").replace(")", "").replace(",", "").replace("'", "")))
        
        df = pd.DataFrame({'Keyword': cleaned_tüm_data})
        df = df.drop_duplicates(subset='Keyword')
        
        ngram_tek_kaç=dict((x, cleaned_tüm_data.count(x)) for x in set(cleaned_tüm_data))
        df_2 = pd.DataFrame(list(ngram_tek_kaç.items()),columns = ['Keyword','Count'])
        df = pd.merge(df,df_2, on='Keyword')
        df = df.sort_values('Count', ascending=False)
          
        
        
        keywords_to_remove = ['https', 'privacy', 'www']
        
        # Create new columns
        df['one word'] = df['Keyword'].apply(lambda x: "One word" if len(x.split()) == 1 else '')
        df['two word'] = df['Keyword'].apply(lambda x: "Two word" if len(x.split()) == 2 else '')
        df['three word'] = df['Keyword'].apply(lambda x: "Three word" if len(x.split()) == 3 else '')
        
        
        # Create a new column for count data
        df['Exist in Long Description'] = 0
        
        def kontrol():
            for index, row in df.iterrows():
                ac=0
                av=row["Keyword"]
                for ab in docs:
                    if re.findall('\\b'+av+'\\b', ab.lower()):
                        ac=ac+1
                df.at[index, 'Exist in Long Description'] = ac
        
        kontrol()
        
        
        def kontrol_keyword_usage(gelen_comp_dic):
            for competitor, long_description in gelen_comp_dic.items():
                long_description_2=long_description
                long_description_nonsembol = re.sub(r'\W+', ' ', long_description_2)
                long_description_leng=len(long_description_nonsembol.split())
                for index, row in df.iterrows():
                    sayı=0
                    av=row["Keyword"]
                    if re.findall('\\b'+av+'\\b', long_description.lower()):
                        sayı = len([*re.finditer('\\b'+av+'\\b', long_description.lower())])
                    df.at[index, competitor ] = round((sayı/long_description_leng)*100,1)
        kontrol()
        
        competitor_dic={"Competitor":docs[0],"Competitor-1":docs[1],"Competitor-2":docs[2],"Competitor-3":docs[3],"Competitor-4":docs[4],"Competitor-5":docs[5],"Competitor-6":docs[6],"Competitor-7":docs[7],"Competitor-8":docs[8],"Competitor-9":docs[9]}
        kontrol_keyword_usage(competitor_dic)
        df = df[~df['Keyword'].str.contains('|'.join(keywords_to_remove))]
        df['Average Percentage'] = df[['Competitor', 'Competitor-1', 'Competitor-2','Competitor-3', 'Competitor-4', 'Competitor-5','Competitor-6', 'Competitor-7', 'Competitor-8', 'Competitor-9']].apply(
            lambda row: round((row[row != 0].mean()),1), axis=1)

        you_long = st.text_input("Please write your data")
        competitor_dic["You"]=you_long
        kontrol_keyword_usage(competitor_dic)
        st.dataframe(df)



if __name__ == "__main__":
    main()


