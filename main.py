import streamlit as st
import re
import pandas as pd

st.set_page_config(layout="wide")
# Streamlit app header
st.title("Keyword Usage Analyzer")
st.write("Analyze keyword usage in your data")

# Get user input for data and keywords
you_long = st.text_area("Please write your data:", "", height=400) # Increase the height
st.write("Total number of keywords:", len(you_long.split()), "Number of chracters:",len(you_long))
# Add a placeholder to suggest keywords
placeholder_text = "ai, ai generator, ai art generator, generate art"
girilen_kelimeler = st.text_input("Please write your keywords (comma-separated):", placeholder=placeholder_text)
girilen_kelimeler_temiz = ",".join([keyword.strip() for keyword in girilen_kelimeler.split(",") if keyword.strip()])


if you_long and girilen_kelimeler_temiz:
    # Split and sort the keywords
    girilen_kelimeler_sorted = sorted(girilen_kelimeler_temiz.split(","), key=lambda x: len(x), reverse=True)

    # Analyze keyword usage
    hedef_keliemler_adet = {}

    def kontrol_keyword_usage(long_description, kontrol_kelimeleri):
        long_lower=long_description.lower()
        for av in kontrol_kelimeleri:
            sayı = 0
            if re.findall('\\b' + av + '\\b', long_lower):
                sayı = len([*re.finditer('\\b' + av + '\\b', long_lower)])
                long_lower = re.sub('\\b' + av + '\\b', "", long_lower)
            hedef_keliemler_adet[av] = sayı
        return hedef_keliemler_adet

    # Analyze keyword usage
    hedef_keliemler_adet = kontrol_keyword_usage(you_long, girilen_kelimeler_sorted)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(hedef_keliemler_adet.items()), columns=["Keyword", "Count"])

    # Calculate the percentage of keyword usage
    df["Percentage"] = round(((df["Count"] / len(you_long.split())) * 100),1)

    # Sort the DataFrame by Count in descending order
    df = df.sort_values(by="Count", ascending=False)

    # Display the DataFrame
    st.header("Keyword Usage Analysis")
    st.dataframe(df.set_index(df.columns[0]),height=300, width=1000)
