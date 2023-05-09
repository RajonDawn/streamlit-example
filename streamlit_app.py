import pandas as pd
import streamlit as st
from io import BytesIO

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
  st.image('./climate.jpg', use_column_width='always')
  road = st.multiselect(label='道路/地形', options = ['高速', '国道', '城市', '非铺路面']) 
  st.image('./road.jpg', use_column_width='always')
with col2:
  landform = st.multiselect(label='地貌特征', options = ['平原', '丘陵', '山区', '高原']) 
  st.image('./landform.jpg', use_column_width='always')
  grade = st.multiselect(label='坡度', options = ['上坡', '下坡', '平路']) 
  st.image('./grade.jpg', use_column_width='always')


l1 = ['怠速', '起步', '低速跟车', '超车', '稳定车速行驶(30,40,50,60,70,80,90km/h)', '倒车', '空挡滑行', '带档滑行', '巡航', '加速', '换挡', '制动', '怠速+开空调', '熄火']
sit = st.multiselect(label='细分工况', options = l1, default=l1) 

specEnv = st.radio(label='特殊环境', options=[], horizontal=True)



specWei = st.multiselect(label='载重', options = ['空载', '满载', '半载'])
specLeg = st.multiselect(label='特殊法规', options = ['排放', '油耗', '限速', '限重', '噪声'],)
specAtt = st.multiselect(label='关注度', options = ['可靠性', '动力性', '经济性', '舒适度', '安全性', '通过性'])
rows = 1
for i in [climate, road, landform, grade, sit, specWei, specLeg, specAtt]:
  if len(i)>=1:
    rows = rows * len(i)
  else:
    rows = rows * 1
st.write(f'输出文件行数为: {rows}')

# st.text('载重')
# col11, col21, col31 = st.columns(3)
# specwei_1 = col11.checkbox('空载')
# specwei_2 = col21.checkbox('满载')
# specwei_3 = col31.checkbox('半载')
# variables1 = specwei_1 + specwei_2 + specwei_3
# specwei = []
# for i in [specwei_1, specwei_2, specwei_3]:
#   if i:
#     specwei.append(i.label)
    
# st.text('特殊法规')
# col11, col21, col31, col41, col51 = st.columns(5)
# specLeg_1 = col11.checkbox('排放')
# specLeg_2 = col21.checkbox('油耗')
# specLeg_3 = col31.checkbox('限速')
# specLeg_4 = col41.checkbox('限重')
# specLeg_5 = col51.checkbox('噪声')
# variables2 = specLeg_1 + specLeg_2 + specLeg_3 + specLeg_4 + specLeg_5


# st.text('关注度')
# col11, col21, col31, col41, col51, col61 = st.columns(6)
# specenv_1 = col11.checkbox('可靠性')
# specenv_2 = col21.checkbox('动力性')
# specenv_3 = col31.checkbox('经济性')
# specenv_4 = col41.checkbox('舒适度')
# specenv_5 = col51.checkbox('安全性')
# specenv_6 = col61.checkbox('通过性')
# variables3 = specenv_1 + specenv_2 + specenv_3 + specenv_4 + specenv_5 + specenv_6

# st.write(f'输出文件行数为: {len(climate)*len(road)*len(landform)*len(grade)*len(sit)*max(1, variables1)*max(1, variables2)*max(1, variables3)}')

output = pd.DataFrame(columns=['一级细分市场',	'二级细分市场',	'三级细分市场',	'关注度',	'气候特征',	'道路/地形', '地貌特征',	'坡度',	'载重',	'特殊环境',	'特殊法规',	'细分工况'])

for att in specAtt:
  for temp_climate in climate:
    for temp_road in road:
      for temp_landform in landform:
        for temp_grade in grade:
          for wei in specWei:
            for leg in specLeg:
                for temp_sit in sit:
                  temp = pd.DataFrame({ '一级细分市场': [lev1],
                                        '二级细分市场': [lev2],
                                        '三级细分市场': [lev3],
                                        '关注度':[att],
                                        '气候特征':  [temp_climate],
                                        '道路/地形': [temp_road],
                                        '地貌特征': [temp_landform],
                                        '坡度':   [temp_grade],
                                        '载重':	[wei],
                                        # '特殊环境':	[env],
                                        '特殊法规': [leg],
                                        '细分工况': [temp_sit]      })
                  output = pd.concat([output,temp])
  
if st.download_button('📥下载VOC表格', data=output.to_csv(index=False).encode('utf_8_sig'),file_name='VOC Collection Table.csv',mime='text/csv'):
  st.success( lev1 +' - '+ lev2 +' - ' + lev3 + '- voc collection table finished!', icon="✅")
