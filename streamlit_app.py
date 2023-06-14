import pandas as pd
import streamlit as st
from io import BytesIO
from io import StringIO




    
@st.cache_data
def init_data(file = './FFA场景定义 template 20230508.xlsx'):
  inData = pd.read_excel(file, sheet_name=None)
  return inData

dataSet = init_data()

st.header('FFA VOC Collection Template')
st.subheader('CCI CE')

# Silder
with st.sidebar:
  uploaded_file = st.file_uploader("请上传FFA模板文件", accept_multiple_files=False )

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataSet = init_data(uploaded_file, sheet_name=None)
  sheetNames = list(dataSet)

  st.header('Application')
  lev0 = st.selectbox(label='数据表名', options=sheetNames)
  tempSheet = dataSet[lev0]
  lev1 = st.selectbox(label='一级细分市场', options = tempSheet.iloc[:, 0].dropna()) 
  lev2 = st.selectbox(label='二级细分市场', options = tempSheet.iloc[:, 1].dropna()) 
  lev3 = st.selectbox(label='三级细分市场', options = tempSheet.iloc[:, 2].dropna()) 


st.empty()
col1, col2 = st.columns(2)
with col1:
  climate = st.multiselect(label='气候特征', options = tempSheet['气候特征'].dropna()) 
  st.image('./climate.jpg', use_column_width='always')
  road = st.multiselect(label='道路/地形', options = tempSheet['道路/地形'].dropna()) 
  st.image('./road.jpg', use_column_width='always')
with col2:
  landform = st.multiselect(label='地貌特征', options = tempSheet['地貌特征'].dropna()) 
  st.image('./landform.jpg', use_column_width='always')
  grade = st.multiselect(label='坡度', options = tempSheet['坡度'].dropna()) 
  st.image('./grade.jpg', use_column_width='always')
sit = st.multiselect(label='细分工况', options = tempSheet['细分工况'].dropna(), default=tempSheet['细分工况'].dropna()) 

specEnv = st.multiselect(label='特殊环境', options=tempSheet['特殊环境'].dropna())
specWei = st.multiselect(label='载重', options = tempSheet['载重'].dropna())
specLeg = st.multiselect(label='特殊法规', options = tempSheet['特殊法规'].dropna())
specAtt = st.multiselect(label='关注度', options = tempSheet['关注度'].dropna())
rows = 1
for i in [climate, road, landform, grade, sit, specEnv, specWei, specLeg, specAtt]:
  if len(i)>=1:
    rows = rows * len(i)
  else:
    i.append('')
    rows = rows * 1
st.write(f'输出组合数量为: {rows}')

@st.cache_data
def fileGen(specAtt, climate, road, landform, grade, specEnv, specWei, specLeg, sit):
  output = pd.DataFrame(columns=['一级细分市场',	'二级细分市场',	'三级细分市场',	'关注度',	'气候特征',	'道路/地形', '地貌特征',	'坡度',	'载重',	'特殊环境',	'特殊法规',	'细分工况'])

  for att in specAtt:
    for temp_climate in climate:
      for temp_road in road:
        for temp_landform in landform:
          for temp_grade in grade:
            for env in specEnv:
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
                                            '特殊环境':	[env],
                                            '特殊法规': [leg],
                                            '细分工况': [temp_sit]      })
                      output = pd.concat([output,temp])


  return output


if st.download_button('📥下载VOC表格', data=fileGen(specAtt, climate, road, landform, grade, specEnv, specWei, specLeg, sit).to_csv(index=False).encode('utf_8_sig'),file_name='VOC Collection Table.csv',mime='text/csv'):
  st.balloons()
  if lev3:
    st.success( lev1 +' - '+ lev2 +' - ' + lev3 + '- voc collection table completed!', icon="✅")
  else:
    st.success( lev1 +' - '+ lev2 + '- voc collection table completed!', icon="✅")



