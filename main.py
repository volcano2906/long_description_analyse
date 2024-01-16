import streamlit as st
import re
import pandas as pd

# Streamlit app header
st.title("Keyword Usage Analyzer")
st.write("Analyze keyword usage in your data")

# Get user input for data and keywords
you_long = st.text_area("Please write app long description data:", "", height=400)  # Increase the height
# Add a placeholder to suggest keywords
placeholder_text = "ai, ai generator, ai art generator, generate art"
girilen_kelimeler = st.text_input("Please write your keywords (comma-separated):", placeholder=placeholder_text)

# Remove spaces and split keywords by commas
girilen_kelimeler = girilen_kelimeler.replace(" ", "").split(",")



if you_long and girilen_kelimeler:
    # Split and sort the keywords
    girilen_kelimeler_sorted = sorted(girilen_kelimeler.split(","), key=lambda x: len(x), reverse=True)

    # Analyze keyword usage
    hedef_keliemler_adet = {}

    def kontrol_keyword_usage(long_description, kontrol_kelimeleri):
        long_description_2 = long_description
        long_description_nonsembol = re.sub(r'\W+', ' ', long_description_2)
        long_description_leng = len(long_description_nonsembol.split())
        longdescriptionLower = long_description.lower()

        for av in kontrol_kelimeleri:
            sayı = 0
            if re.findall('\\b' + av + '\\b', longdescriptionLower):
                sayı = len([*re.finditer('\\b' + av + '\\b', longdescriptionLower)])
                longdescriptionLower = re.sub('\\b' + av + '\\b', "", longdescriptionLower)
            hedef_keliemler_adet[av] = sayı

        return hedef_keliemler_adet

    # Analyze keyword usage
    hedef_keliemler_adet = kontrol_keyword_usage(you_long, girilen_kelimeler_sorted)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(list(hedef_keliemler_adet.items()), columns=["Keyword", "Count"])

    # Calculate the percentage of keyword usage
    df["Percentage"] = round((df["Count"] / len(you_long.split(","))) * 100)

    # Sort the DataFrame by Count in descending order
    df = df.sort_values(by="Count", ascending=False)

    # Display the DataFrame
    st.header("Keyword Usage Analysis")
    st.dataframe(df)
