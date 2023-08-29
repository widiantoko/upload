import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np



st.set_page_config(page_title="Storage", layout='wide')


romox_a = pd.read_excel("data/23_08_23.xlsx")

grup_bag1=romox_a.groupby(['typedesc'], as_index =False)['qtybag'].sum()
#grup_bag2=romox_a.groupby(['typedesc', 'c2'], as_index =False)['qtybag'].sum()

with open('style.css') as f:
  st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


col_a, col_b, col_c = st.columns(3)
col_b.metric("Good Stock", int(grup_bag1.loc[1,'qtybag']))
col_c.metric("Damage", int(grup_bag1.loc[0,'qtybag']))


romox=romox_a[romox_a.c2!="QI"]
romox["c3"]=romox["c3"].astype(str)


for i, row in romox.iterrows():
        hasil2 = ''
        if len(row['c3']) == 1:
            hasil2 = "0"+row["c3"]
        else:
             hasil2 = row["c3"]
        
        romox.at[i, 'c3'] = hasil2


lst = []
for each in romox["lotno"]:
    lst.append(str(each).split('.')[0])
  
# all values converting to integer data type
final_list = [i for i in lst]
romox["lotno"]=final_list


ticktext=['WMS_n.a.', 'good stock', 'damage', 'empty']


dpn=sorted(set(romox["c2"]))
tgh=sorted(set(romox["c3"]))
y_loc=sorted(set(romox["c4"]))


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
        


color_scale= [(0.00, "#64B5F6"), (0.25, "#64B5F6"),
                        (0.25, "#BDBDBD"), (0.50, "#BDBDBD"),
                        (0.50, "#FF8A80"), (0.75, "#FF8A80"),
                        (0.75, "#1DE9B6"),  (1.00, "#1DE9B6")] 




color_new=[
        [0, "#64B5F6"],
        [0.25, "#64B5F6"],
        [0.25, "#EF9A9A"],
        [0.5, "#EF9A9A"],
        [0.5, "#1DE9B6"],
        [0.75, "#1DE9B6"],
        [0.75, "#FFCC80"],
        [1, "#FFCC80"]]


     





for i, row in romox_join.iterrows():
        hasil1 = ''
        if row['loc'] != row['set_loc']:
            hasil1 = 2
        elif (row['loc'] == row['set_loc'] and  row['typedesc'] =="GOOD STOCK" and row['qtybag']!=0):
            hasil1 = 0
        elif (row['loc'] == row['set_loc'] and  row['typedesc'] =="BLOCKED STOCK" and row['qtybag']!=0):
            hasil1 = 3
        else:
             hasil1 = 1
        
        romox_join.at[i, 'z'] = hasil1

romox_join["con"] = romox_join['grup'].astype(str)+" : " +romox_join['lotno'].astype(str)



 
pilih_zona=romox_join['zona'].drop_duplicates().sort_index(ascending=True)



col1, col2 = st.columns([1, 12], gap="small")

with col1:
    
    pilihan=st.selectbox(label="**Location:**",options= pilih_zona)
    romox_join_zona=romox_join[romox_join.zona == pilihan].reset_index(drop=True)

    x_sum = int(romox_join_zona['qtybag'].sum())

    
   
    test= f"""<p style=' color: #3288bd; text-align: center;
                        font-size: 18px; 
                        border-radius: 8px; 
                        border: 1.5px solid #3288bd;
                        padding-left: 0px; 
                        padding-top: 25px; 
                        padding-bottom: 25px;
                        line-height:3px;'>
                        {x_sum} Bag
                        """

    st.markdown(test, unsafe_allow_html=True)



with col2:
   
            
    hm_zona = go.Figure(go.Heatmap(x=romox_join_zona["x_loc"], y = romox_join_zona["y_loc"], z=romox_join_zona["z"],
                           customdata=romox_join_zona["con"], xgap=1.5, ygap=1.5,text=romox_join_zona["qtybag"],texttemplate="%{text}",
                           textfont={"size":10},
                           colorscale=color_scale, showscale=False, 
                           hovertemplate="%{x}.%{y} : %{customdata} <extra></extra>"))


    hm_zona.update_layout(width=1200, height=500, yaxis_autorange=True, xaxis_autorange=True, title= f"Storage Location Control - {pilihan}",
                 title_y=0.99, title_font_size=20, title_yanchor="top", margin_t=50, showlegend=True)







    
    st.plotly_chart(hm_zona)

    st.text("Sumber Data: WMS Romokalisari 22 Agustus 2023")


aging=romox_join[romox_join.grup=="good stock"]

zona_fd=romox_join[romox_join.grup=="WMS_n.a."]

import datetime 

today = pd.Timestamp(datetime.date.today())

aging['today']=today
aging['diff_days'] = (aging['expired_new'] - aging['today']) / np.timedelta64(1, 'D')
aging_sort = aging.sort_values(by=['diff_days']).head(50)

st.dataframe(zona_fd)


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




#st.text(dpn)
#st.text(c3_sort)



