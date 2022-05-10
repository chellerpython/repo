"""
Name: Cameron Heller
CS230 Section 2
Data: Boston Crime
URL:

Description: This program contains data related to Boston 2022 crime. The user can filter out
offenses from the data table or choose to display offenses that happened a range of times.
Using the select box, the user can then learn information about crime data in January, February, March, or April.
A pie chart is displayed that shows the top 10 crimes of that month and the related percentages.
A bar chart is also displayed that shows the districts and the number of offenses within that
district for the month. Lastly, there is a map that shows the reported incidents in Boston
in January.
"""
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

image = Image.open('boston-massachusetts-BOSTONTG0221.jpg')
st.image(image)
st.title("2022 Boston Crime Data")
st.write("By Cameron Heller")

dfOriginal = pd.read_csv('BostonCrime2022_8000_sample.csv')
Boston_Crime = dfOriginal
st.sidebar.header('Select what to display')
offense = Boston_Crime['OFFENSE_DESCRIPTION'].unique().tolist()
offense_select = st.sidebar.multiselect('Offenses', offense, offense)

nb_offenses = Boston_Crime['OFFENSE_DESCRIPTION'].value_counts()
nb_crimes = st.sidebar.slider("Number of Offenses",int(nb_offenses.min()),int(nb_offenses.max()),(int(nb_offenses.min()), int(nb_offenses.max())), 1)
mask_offense = Boston_Crime['OFFENSE_DESCRIPTION'].isin(offense_select)

mask_crimes = Boston_Crime['OFFENSE_DESCRIPTION'].value_counts().between(nb_crimes[0],nb_crimes[1]).to_frame()
mask_crimes = mask_crimes[mask_crimes['OFFENSE_DESCRIPTION'] == 1].index.to_list()
mask_crimes = Boston_Crime['OFFENSE_DESCRIPTION'].isin(mask_crimes)

df_offense_filtered = Boston_Crime[mask_offense & mask_crimes]
st.write(df_offense_filtered)

show_crime = df_offense_filtered['OFFENSE_DESCRIPTION'].value_counts()
st.subheader('Monthly Crime Data')
month = st.selectbox('Select 1-4 for January - April', [1, 2, 3, 4]) # show selector with options
df = dfOriginal[['OFFENSE_DESCRIPTION', 'MONTH']]
df.index = df['MONTH']
df = df.loc[[month]]
df = df['OFFENSE_DESCRIPTION'].value_counts()[0:10] # choose top 10 values
df = df.to_frame()
df = df.reset_index()
crimes = []
amounts = []

for index, row in df.iterrows():
    crime = row['index']
    amount = row['OFFENSE_DESCRIPTION']
    crimes.append(crime)
    amounts.append(amount)

fig, ax = plt.subplots()
ax.pie(amounts, autopct='%.0f%%')
ax.set_title('Top 10 Crimes for Month') #title
ax.legend(crimes, loc='upper left', bbox_to_anchor=(1,1)) # Move chart legend over
st.pyplot(fig)

df = dfOriginal['DISTRICT'].value_counts()[0:10] # Top 10 districts
df = df.to_frame()
df = df.reset_index()
districts = []
amounts2 = []

for index, row in df.iterrows():
    district = row['index']
    amount2 = row['DISTRICT']
    districts.append(district)
    amounts2.append(amount2)
print(amounts2)
print(districts)


fig, ax = plt.subplots() # Bar Chart
ax.bar(districts, amounts2)
ax.set_title('Districts In Boston With Most Offenses ')
ax.set_xlabel('District')
ax.set_ylabel('Number of Offenses for Month')
st.pyplot(fig)

st.title("Map of Incidents in January")
df = dfOriginal[["Lat", "Long", "MONTH"]]
df.columns = ['lat', "lon", 'MONTH']
df = df[df.MONTH == 1] # Show data for January
st.map(df)
