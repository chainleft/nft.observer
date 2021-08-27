import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import datetime
import sys
import csv

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append({
          
                "title": title, 
                "function": func
            })

    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # run the app function 
        page['function']()


st.title('NFT Collection History')

#columns = 'Title','Generative?','Generated on chain?','Category','File type','Detail','Date'
#entry1 = "Etheria","Manual",""

df = pd.read_csv('nfts.csv')
df = df.replace(np.nan, '', regex=True)

onoff_options = ["","Off-chain","On-chain"]
gen_options = ["","Manual","Generative"]
cat_options = list(set(df['Category']))
cat_options.append("")
cat_options.sort()
type_options = list(set(df['File type']))
type_options.append("")
type_options.sort()
detail_options = list(set(df['Detail']))
detail_options.append("")
detail_options.sort()

df['timestamp'] = pd.to_datetime(df['Date'], format='%B %d, %Y')
df = df.sort_values(by=['timestamp'])
df2 = df

class ParameterError(Exception):
    pass

try:
  #Generative or manual production
  gen = st.sidebar.selectbox(
      'Generative or manually produced?',
       gen_options)

  if gen == "Manual":
    df2 = df2[df2["Generative?"] == False]
    onoff_options = ["","Off-chain"]
  elif gen == "Generative":
    df2 = df2[df2["Generative?"] == True]

  #Generated on or off chain
  onoff = st.sidebar.selectbox(
      'Generated on-chain or off-chain?',
       onoff_options)

  if onoff == "On-chain":
    df2 = df2[df2["Generated on chain?"] == True]
  elif onoff == "Off-chain":
    df2 = df2[df2["Generated on chain?"] == False]

  #Category
  cat = st.sidebar.selectbox(
      'Category',
       cat_options)
  if cat != "":
    df2 = df2[df2["Category"] == cat]

  #Type
  filetype = st.sidebar.selectbox(
      'Type',
       type_options)
  if filetype != "":
    df2 = df2[df2["File type"] == filetype]

  #Details
  #details = st.sidebar.selectbox(
  #    'Details',
  #     detail_options)
  #if details != "":
  #  df2 = df2[df2["Detail"] == details]

  df2 = df2.sort_values(by=['timestamp'])

  if onoff=="On-chain": onoff_gen = "on-chain generated"
  elif onoff=="Off-chain": onoff_gen = "off-chain generated"
  elif gen=="Manual": onoff_gen = "manually created"
  else: onoff_gen = onoff.lower() + " " + gen.lower()

  if filetype=="Interactive": cat_type = "interactive " + cat.lower()
  elif filetype=="": cat_type = cat.lower()
  else: cat_type = filetype.lower() + " based " + cat.lower()

  'First ', onoff_gen, cat_type, ' NFT collection on Ethereum network is ', df2['Title'].iloc[0]

  left_column, right_column = st.columns(2)

#  if st.checkbox('Show the full list'):
#      df
except:
  raise ParameterError("There are no NFTs matching all of these parameters")
sys.tracebacklimit = 0

st.text("")
st.text("")
st.text("")
st.text("")

expander = st.expander("Roadmap")
expander.write("- Second, third projects in NFT history")
expander.write("- A floor tracker method that's more reliable than what you've seen before. The method is already built, I'm working on API setup")
expander.write("- Data science approach to art: What makes an art piece more iconic?")
