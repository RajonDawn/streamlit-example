from datetime import time, date, datetime, timedelta

import numpy as np
import pandas as pd
import altair as alt
import streamlit as st


file = pd.read_excel(r'./FFA 场景定义 template 20230504.xlsx', sheet_name='Tractor-1', engine='openpyxl')
columnsName = list(file)
output = pd.DataFrame(columns=columnsName)

st.header('FFA VOC Collection Template')
st.subheader('CCI CE')

# Silder
with st.sidebar:
  st.header('Application')
  lev1 = st.selectbox(label='一级细分市场', options = ['N3-Tractor']) 
  lev2 = st.selectbox(label='二级细分市场', options = ['长途车辆']) 
  lev3 = st.selectbox(label='三级细分市场', options = ['零担', '沙石料']) 

st.empty()
col1, col2 = st.columns(2)
with col1:
  climate = st.multiselect(label=columnsName[3], options = file[columnsName[3]].dropna()) 
  st.image('./images/climate.jpg', use_column_width='always')
  road = st.multiselect(label=columnsName[4], options = file[columnsName[4]].dropna()) 
  st.image('./images/road.jpg', use_column_width='always')
with col2:
  landform = st.multiselect(label=columnsName[5], options = file[columnsName[5]].dropna()) 
  st.image('./images/landform.jpg', use_column_width='always')
  grade = st.multiselect(label=columnsName[6], options = file[columnsName[6]].dropna()) 
  st.image('./images/grade.jpg', use_column_width='always')

sit = st.multiselect(label='细分工况', options = file['细分工况'].dropna(), default=file['细分工况'].dropna()) 

specEnv = st.radio(label='特殊环境', options=file['特殊环境'].dropna(), horizontal=True)
specLeg = st.radio(label='特殊法规', options=file['特殊法规'].dropna(), horizontal=True)

st.write(f'输出文件行数为: {len(climate)*len(road)*len(landform)*len(grade)*len(sit)}')


for temp_climate in climate:
  for temp_road in road:
    for temp_landform in landform:
      for temp_grade in grade:
        for temp_sit in sit:
          temp = pd.DataFrame({ '一级细分市场': [lev1],
                                '二级细分市场': [lev2],
                                '三级细分市场': [lev3],
                                '气候特征':  [temp_climate],
                                '道路/地形': [temp_road],
                                '地貌特征': [temp_landform],
                                '坡度':   [temp_grade],
                                '细分场景': [temp_sit]      })
          output = pd.concat([output,temp])

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, encoding='utf-8')

csv = convert_df(output)


st.download_button(
    label="Download data",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',

)


# if st.button('Download'):
#   st.success( lev1 +' - '+ lev2 +' - ' + lev3 + '- voc collection table finished!', icon="✅")
