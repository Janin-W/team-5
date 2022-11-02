import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.stats import gaussian_kde
plt.style.use('seaborn')

st.title('Final Team Project by Xinyu Chen and Yanan Wen')
df = pd.read_csv('healthcare-dataset-stroke-data.csv')
df = df.drop(df[df["gender"]=="Other"].index)


st.subheader('1.See the relationship between glucose levels and stroke:')

a = list(df['avg_glucose_level'])
a = sorted(a)
glu_filter = st.select_slider(
    'Glucose levels:', 
    options = a)
num =  df.value_counts('avg_glucose_level')
st.write('When the  glucose levels is',glu_filter,'the number of people is: ',num[glu_filter])


fig, ax= plt.subplots()
df['avg_glucose_level'].plot.kde( color = 'red', ax = ax )
df.query('stroke==1')['avg_glucose_level'].plot.kde( color= 'blue', ax = ax )
st.pyplot(fig)


st.subheader('2.See the relationship between heart disease and stroke:')
fig, ax= plt.subplots()
df_hd_sum = df.groupby('heart_disease').sum()
df_hd_count = df.groupby('heart_disease').count()
df_hd_count['stroke_rate'] = df_hd_sum['stroke'] / df_hd_count['stroke']

df_hd_count0 = df_hd_count.copy()
df_hd_count1 = df_hd_count.copy()
df_hd_count0['stroke_rate'] = 1 - df_hd_count0['stroke_rate']
df_hd_count0['hd'] = [str((i, 0))for i in df_hd_count.index.values]
df_hd_count1['hd'] = [str((i, 1))for i in df_hd_count.index.values]
df_hd_count3 = pd.concat((df_hd_count0, df_hd_count1), axis=0).sort_values('hd')

ax = df_hd_count3.plot.bar( x= 'hd', y = 'stroke_rate', ax = ax)
ax.set_xticks(range(4))
ax.set_xlabel('Heart disease, Stroke')
st.pyplot(fig)


st.subheader('3.See the relationship between work type and stroke based on gender:')


select = st.sidebar.selectbox('Please select gender', ('Female','Male','All'))

if select == 'Female':
    df = df.drop(index = (df.loc[df['gender']=='Male'].index))
if select == 'Male':
    df = df.drop(index = (df.loc[df['gender']=='Female'].index))


total_dataframe = pd.DataFrame({
        'work type': ['Private', 'Self-employed', 'children','Government-work','Never-worked'],
        'number of stroke': (df.work_type.value_counts()['Private'],
                df.work_type.value_counts()['Self-employed'],
                df.work_type.value_counts()['children'],
                df.work_type.value_counts()['Govt_job'],
                df.work_type.value_counts()['Never_worked'])})

 

st.markdown("### %s number of stroke on Private, Self-employed, children, Government-work, Never-worked" % (select))
if not st.checkbox('Hide Graph', False, key=3):
    state_total_graph = px.bar(
        total_dataframe,
        x='work type',
        y='number of stroke',
        labels={'number of stroke': '%s number of stroke' % (select)},
        color='work type')
    st.plotly_chart(state_total_graph)

def get_table():
    df2 = df.drop(index = (df.loc[df['stroke']==0].index))
    datatable = df2.sort_values(by=['work_type'], ascending=False)
    return datatable
 
datatable = get_table()
st.markdown("### The number of stroke in different work type")
st.markdown("The following table provides %s number of stroke on Private, Self-employed, children, Government-work, Never-worked"% (select))
st.dataframe(datatable) # will display the dataframe
st.table(total_dataframe)# will display the table


st.subheader('4.See the relationship between age and stroke:')
age_filter = st.sidebar.radio(
    "choose age range",
    ('Youth','Middle','Elder','All'))

if age_filter == 'Youth' :
    df = df[df.age <= 18]
if age_filter == 'Middle':
    df = df[(df.age < 45) & (df.age > 18)]
if age_filter == 'Elder':
    df = df[df.age >= 45]


fig, ax= plt.subplots()
df_age = df.pivot_table(index='age',columns='stroke',values='id',aggfunc='count')
df_age.head()
df_age = df_age.apply(lambda x:x/x.sum())
df_age.plot.area(ax=ax, figsize=(10,5))
st.pyplot(fig)

