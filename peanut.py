import pandas as pd
import streamlit as st
import openpyxl
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Storage", layout='wide')

file_01="data/xwh_romo.xlsx"

#wb=openpyxl.load_workbook(file_01)
romox = pd.read_excel("data/22agustus.xlsx")


lst = []
for each in romox["lotno"]:
    lst.append(str(each).split('.')[0])
  
# all values converting to integer data type
final_list = [i for i in lst]
romox["lotno"]=final_list






warna_bag = {'WMS_n.a.':'#64B5F6',
        'good stock':'#EF9A9A',
        'damage':'#FF8A80',
        'empty':'#1DE9B6'}


ticktext=['WMS_n.a.', 'good stock', 'damage', 'empty']




y_loc=[
"1A","1B","1C","1D","1E","1F","1G",
"1H","1I","1J","1K","1L","1M","1N"]





dpn=["AA","AB", "AC", "AD", "AE", "AF",
     "AG", "AH", "BA","BB","BC","BD","BE","BF",
    "CA","CB","CC","CD","CE","CF"]



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



romox_join=pd.merge(lokasi,romox, left_on="set_loc", right_on='loc', how='outer')
romox_join= romox_join.fillna(value=np.nan)
romox_join["qtybag"] = romox_join["qtybag"].fillna(0)
romox_join["lotno"] = romox_join["lotno"].fillna("-").astype(str)



for i, row in romox_join.iterrows():
        hasil = ''
        if row['loc'] != row['set_loc']:
            hasil = 'WMS_n.a.'
        elif (row['loc'] == row['set_loc'] and  row['typedesc'] =="GOOD STOCK" and row['qtybag']!=0):
            hasil = 'good stock'
        elif (row['loc'] == row['set_loc'] and  row['typedesc'] =="BLOCKED STOCK" and row['qtybag']!=0):
            hasil = 'damage'
        else:
             hasil = "empty"
        
        romox_join.at[i, 'grup'] = hasil
        
romox_join["warna"]=[warna_bag[x] for x in romox_join["grup"]]


for i, row in romox_join.iterrows():
        hasil1 = ''
        if row['loc'] != row['set_loc']:
            hasil1 = 0
        elif (row['loc'] == row['set_loc'] and  row['typedesc'] =="GOOD STOCK" and row['qtybag']!=0):
            hasil1 = 10
        elif (row['loc'] == row['set_loc'] and  row['typedesc'] =="BLOCKED STOCK" and row['qtybag']!=0):
            hasil1 = 5
        else:
             hasil1 = 3
        
        romox_join.at[i, 'Z_value'] = hasil1

romox_join["con"] = romox_join['grup'].astype(str)+" : " +romox_join['lotno'].astype(str)



new_title = '<p style="font-family:sans-serif; font-size: 20px;">Storage Location Control</p>'
st.markdown(new_title, unsafe_allow_html=True)



pilih_zona=romox_join['zona'].drop_duplicates().sort_index(ascending=True)
pilihan=st.radio("", key="visibility", options= pilih_zona, label_visibility= "collapsed",
                 horizontal=True, disabled=False,)

romox_join_zona=romox_join[romox_join.zona == pilihan].reset_index(drop=True)


        
hm_zona = go.Figure(go.Heatmap(x=romox_join_zona["x_loc"], y = romox_join_zona["y_loc"], z=romox_join_zona["Z_value"],
                           customdata=romox_join_zona["con"], xgap=1.5, ygap=1.5,text=romox_join_zona["qtybag"],texttemplate="%{text}",
                           textfont={"size":10},
                           colorscale=romox_join["warna"], showscale=False,
                           hovertemplate="%{x}.%{y} : %{customdata} <extra></extra>"))


hm_zona.update_layout(width=1250, height=500, yaxis_autorange=True, xaxis_autorange=True, title= '',
                 title_y=0.85)



st.plotly_chart(hm_zona)

st.text("Sumber Data: WMS Romokalisari 22 Agustus 2023")