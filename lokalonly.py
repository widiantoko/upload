import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas_bokeh
pandas_bokeh.output_notebook()
from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, Range1d, LabelSet



st.set_page_config(page_title="Storage", layout='wide')




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

#warna_bag = {'WMS_n.a.':'#69F0AE',  'good stock':'#EF9A9A','damage':'#CE93D8', 'empty':'#FB8C00'}


#warna_bag = {'good stock':'#FB8C00','WMS_n.a.':'#FFECB3','damage':'#FF8F00','empty':'#69F0AE'}


ticktext=['WMS_n.a.', 'good stock', 'damage', 'empty']

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



y_loc=[
"1A","1B","1C","1D","1E","1F","1G",
"1H","1I","1J","1K","1L","1M","1N"]


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



new_title = '<p style="font-family:sans-serif; font-size: 20px;">Storage Location Control </p>'
#st.markdown(new_title, unsafe_allow_html=True)
 
pilih_zona=romox_join['zona'].drop_duplicates().sort_index(ascending=True)



col1, col2 = st.columns([1, 12], gap="small")

with col1:
    
    pilihan=st.selectbox(label="**Location:**",options= pilih_zona)



with col2:
   
    romox_join_zona=romox_join[romox_join.zona == pilihan].reset_index(drop=True)
        
    hm_zona = go.Figure(go.Heatmap(x=romox_join_zona["x_loc"], y = romox_join_zona["y_loc"], z=romox_join_zona["Z_value"],
                           customdata=romox_join_zona["con"], xgap=1.5, ygap=1.5,text=romox_join_zona["qtybag"],texttemplate="%{text}",
                           textfont={"size":10},
                           colorscale=romox_join["warna"], showscale=False,
                           hovertemplate="%{x}.%{y} : %{customdata} <extra></extra>"))


    hm_zona.update_layout(width=1200, height=500, yaxis_autorange=True, xaxis_autorange=True, title= f"Storage Location Control - {pilihan}",
                 title_y=0.99, title_font_size=20, title_yanchor="top", margin_t=50)


    
    st.plotly_chart(hm_zona)

    st.text("Sumber Data: WMS Romokalisari 22 Agustus 2023")


aging=romox_join[romox_join.grup=="good stock"]


import datetime 


today = pd.Timestamp(datetime.date.today())

aging['today']=today
aging['diff_days'] = (aging['expired_new'] - aging['today']) / np.timedelta64(1, 'D')
aging_sort = aging.sort_values(by=['diff_days']).head(50)

st.dataframe(aging_sort)



color_don=['#ef9a9a','#f48fb1','#ce93d8','#b39ddb','#9fa8da','#90caf9',
'#81d4fa','#80deea','#80cbc4','#a5d6a7','#c5e1a5',
'#e6ee9c','#fff59d','#ffe082','#ffcc80','#ffab91',
'#bcaaa4','#e57373','#f06292','#ba68c8','#9575cd',
'#7986cb','#64b5f6','#4fc3f7','#4dd0e1','#4db6ac',
'#81c784','#aed581','#dce775','#fff176','#ffd54f',
'#ffb74d','#ff8a65','#a1887f','#ef5350','#ec407a',
'#ab47bc','#7e57c2','#5c6bc0','#42a5f5','#29b6f6',
'#26c6da','#26a69a','#66bb6a','#9ccc65','#d4e157',
'#ffee58','#ffca28','#ffa726','#ff7043','#8d6e63']




diff_sort=sorted(set(aging_sort["diff_days"]))
st.text(diff_sort)


