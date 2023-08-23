import pandas as pd
import streamlit as st

df=pd.read_csv('intracity_jan_jul_2022.csv')
df=pd.read_csv('https://github.com/widiantoko/upload/blob/main/intracity_jan_jul_2022.csv')

st.dataframe(df.head(10))

