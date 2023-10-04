import pandas as pd
import streamlit as st

import plotly.graph_objects as go
import numpy as np
from bokeh.plotting import figure
from bokeh.transform import cumsum


import pandas_bokeh 
pandas_bokeh.output_notebook()

from math import pi

        


st.set_page_config(page_title="Romokalisari", layout='wide')




romox = pd.read_excel("data/29_09_23_goodstock.xlsx")
romox['c3'] = romox["c3"].apply(str)
romox['c3'] = romox['c3'].str.replace('.0','')


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
lokasi['x_loc_new'] = lokasi['set_loc'].str[:5]
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
        

color_continuous_scale=[(0.00, "#64B5F6"), (0.25, "#64B5F6"),
                        (0.25, "#BDBDBD"), (0.50, "#BDBDBD"),                   
                        (0.50, "#1DE9B6"),  (0.75, "#1DE9B6"),
                        (0.75, "#FF8A80"), (1, "#FF8A80")]



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
        
        romox_join.at[i, 'Z_value'] = hasil1






romox_join["con"] = romox_join['grup'].astype(str)+" : " +romox_join['lotno'].astype(str)


pilih_zona=romox_join['zona'].drop_duplicates().sort_index(ascending=True)


gs=int(romox_join['qtybag'].sum())

tot_bag = [['good_stock', gs, '#90caf9' ], ['bad_stock', 318,  '#ef9a9a' ]]
rkp_bag = pd.DataFrame(tot_bag, columns=['item', 'qty', 'color'])
rkp_bag['angle'] = rkp_bag['qty']/rkp_bag['qty'].sum() * 2*pi

rkp_bag['value']=100*(rkp_bag['qty']/rkp_bag['qty'].sum())



p = figure(plot_height=300, plot_width=400, title="Detail Komposisi Resin Romokalisari 26 Sept 2023", toolbar_location="above",
           tools="hover", tooltips="@item: @qty", x_range=(-.5, .5))

p.annular_wedge(x=0, y=1,  inner_radius=0.19, outer_radius=0.4, direction="anticlock", 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color=None, fill_color='color', legend='item', source=rkp_bag)

       
        
       

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None
p.legend.location = "center"
p.add_layout(p.legend[0], 'right')

st.bokeh_chart(p)



#st.dataframe(rkp_bag)

col1, col2 = st.columns([1, 12], gap="small")

with col1:
    
    pilihan=st.selectbox(label="**Location:**",options= pilih_zona)

    romox_join_zona=romox_join[romox_join.zona == pilihan].reset_index(drop=True)


    x_sum = int(romox_join_zona['qtybag'].sum())

    
   
    test= f"""<p style=' color: #262730; text-align: center;
                        font-size: 18px; 
                        border-radius: 8px; 
                        background-color: #f0f2f6;
                        border: 1px solid #ff2b2b;
                        padding-left: 0px; 
                        padding-top: 25px; 
                        padding-bottom: 25px;
                        line-height:3px;'>
                        {x_sum} Bag
                        """

    st.markdown(test, unsafe_allow_html=True)

 #border: 2px solid #3288bd;


with col2:
   
            
    hm_zona = go.Figure(go.Heatmap(x=romox_join_zona["x_loc_new"], y = romox_join_zona["y_loc"], z=romox_join_zona["Z_value"],
                           customdata=romox_join_zona["con"], xgap=1.5, ygap=1.5,text=romox_join_zona["qtybag"],texttemplate="%{text}",
                           textfont={"size":10},
                           colorscale=color_continuous_scale, showscale=False,
                           hovertemplate="%{x}.%{y} : %{customdata} <extra></extra>"))


    hm_zona.update_layout(width=1200, height=500, yaxis_autorange=True, xaxis_autorange=True, title= f"Storage Location Control - {pilihan}",
                 title_y=0.99, title_font_size=20, title_yanchor="top", margin_t=50)


    
    st.plotly_chart(hm_zona)


    st.text("Sumber Data: WMS Romokalisari 26 September 2023")