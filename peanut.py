import pandas as pd
import streamlit as st
import openpyxl

#df=pd.read_csv('intracity_jan_jul_2022.csv')
#df=pd.read_csv('https://github.com/widiantoko/upload/blob/main/intracity_jan_jul_2022.csv')

file_01="https://github.com/widiantoko/upload/blob/main/data/xwh_romo.xlsx"

wb=openpyxl.load_workbook(file_01)
df = pd.read_excel(file_01)


x_loc=[
"AA.01","AA.02","AA.03","AA.04","AA.05","AA.06","AA.07","AA.08","AA.09",
"AA.10","AA.11","AA.12","AA.13","AA.14","AA.15","AA.16","AA.17","AA.18","AA.19",
"AA.20","AA.21","AA.22","AA.23","AA.24","AA.25","AA.26","AA.27","AA.28","AA.29",
"AA.30","AA.31","AA.32","AA.33","AA.34","AA.35","AA.36","AA.37","AA.38","AA.39",
"AA.40","AA.41","AA.42","AA.43","AA.44","AA.45","AA.46","AA.47","AA.48","AA.49",
"AA.50","AA.51","AA.52","AA.53","AA.54","AA.55","AA.56","AA.57","AA.58","AA.59"]


y_loc=[
"1A","1B","1C","1D","1E","1F","1G",
"1H","1I","1J","1K","1L","1M"]

temp_xy = [(a, b) for a in x_loc for b in y_loc]
xy_cont=[x+"."+y for (x, y) in temp_xy]

dpn=["AA","AB", "AC", "AD", "AE", "AF"]
tgh=["01","02","03", "04","05","06","07","08","09","10","11",
     "12","13","14","15","16","17","18","19","20","21","22","23",
     "24","25","26","27","28","29","30","31","32","33","34","35",
     "36","37","38","39","40","41","42","43","44","45","46","47",
     "48","49","50","51","52","53",'54',"55","56","57","58","59",
     "60","61","62","63"
     ]

dpn_tgh=[(a, b) for a in dpn for b in tgh]
x_loc_new=[x+"."+y for (x, y) in dpn_tgh]


dpn_tgh_blk=[(a, b) for a in x_loc_new for b in y_loc]
loc_all_new=[x+"."+y for (x, y) in dpn_tgh_blk]


lokasi=pd.DataFrame(loc_all_new, columns=["set_loc"])
lokasi['zona'] = lokasi['set_loc'].str[:2]
lokasi['x_loc'] = lokasi['set_loc'].str[:5]
lokasi['y_loc'] = lokasi['set_loc'].str[6:8]

st.dataframe(lokasi)