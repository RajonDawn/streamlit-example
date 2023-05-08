from datetime import time, date, datetime, timedelta

import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

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
  climate = st.multiselect(label='气候特征', options = ['高温', '高寒']) 
  st.image('climate.jpg', use_column_width='always')
  road = st.multiselect(label='道路/地形', options = ['高速', '国道', '城市', '非铺路面']) 
  st.image('./road.jpg', use_column_width='always')
with col2:
  landform = st.multiselect(label='地貌特征', options = ['平原', '丘陵', '山区', '高原']) 
  st.image('./landform.jpg', use_column_width='always')
  grade = st.multiselect(label='坡度', options = ['上坡', '下坡', '平路']) 
  st.image('./grade.jpg', use_column_width='always')

l1 = ['怠速', '起步', '低速跟车', '超车', '稳定车速行驶（30,40,50,60,70,80,90km/h)', '倒车', '空挡滑行', '带档滑行', '巡航', '加速', '换挡', '制动', '怠速+开空调', '熄火']
sit = st.multiselect(label='细分工况', options = l1, default=l1) 

specEnv = st.radio(label='特殊环境', options=[], horizontal=True)
specLeg = st.radio(label='特殊法规', options=['排放', '油耗', '限速', '限重', '噪声'], horizontal=True)

st.write(f'输出文件行数为: {len(climate)*len(road)*len(landform)*len(grade)*len(sit)}')

output = pd.DataFrame(columns=['一级细分市场',	'二级细分市场',	'三级细分市场',	'气候特征',	'道路/地形', '地貌特征',	'坡度',	'载重',	'特殊环境',	'特殊法规',	'关注度',	'细分工况'])

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

# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(index=False, encoding='utf-8')

# csv = convert_df(output)



def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
  
st.download_button(label='📥 Download Current Result',
                                data=to_excel(output) ,
                                file_name= 'VOC Collection Table.xlsx')


# st.download_button(
#     label="Download data",
#     data=csv,
#     file_name='VOC Collection Table.csv',
#     mime='text/csv',

# )


# if st.button('Download'):
#   st.success( lev1 +' - '+ lev2 +' - ' + lev3 + '- voc collection table finished!', icon="✅")
