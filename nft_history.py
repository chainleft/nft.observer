import streamlit as st
st.set_page_config(layout="wide")

import numpy as np
import pandas as pd
import datetime
import sys
import csv


etherscan_APIkey = 'M6WGR7AGDKQ5KUPRWJF1T9Q13JSCD6DUZ3'
etherscan_API1 = 'https://api.etherscan.io/api?module=account&action=txlist&address='
etherscan_API2 = '&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey='

st.title('NFT Collection History')

df = pd.read_csv('nfts.csv')
df = df.replace(np.nan, '', regex=True)

df['address'] = df['Original contract address'].str.split("https://etherscan.io/address/").str[1]

onoff_options = ["","Off-chain","On-chain"]
gen_options = ["","Manual","Generative"]

cat_options = list(set(df['Category']))
cat_options.append('')
cat_options.sort()

type_options = list(set(df['Type']))
type_options.append('')
type_options.sort()

subtype_options = list(set(df['Subtype']))
subtype_options.append('')
subtype_options.sort()

#detail_options = list(set(df['Detail']))
#detail_options.append("")
#detail_options.sort()

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
  #Filter based on sidebar selection
  if gen == "Manual":
    df2 = df2[df2["Generative?"] == False]
    onoff_options = ["","Off-chain"]
    cat_options = list(set(df2['Category']))
    cat_options.append('')
    cat_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()
    subtype_options = list(set(df2['Subtype']))
    subtype_options.append('')
    subtype_options.sort()
  elif gen == "Generative":
    df2 = df2[df2["Generative?"] == True]

  #Generated on or off chain
  onoff = st.sidebar.selectbox(
      'Generated on-chain or off-chain?',
       onoff_options)
  #Filter based on sidebar selection
  if onoff == "On-chain":
    df2 = df2[df2["Generated on chain?"] == True]
    cat_options = list(set(df2['Category']))
    cat_options.append('')
    cat_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()
    subtype_options = list(set(df2['Subtype']))
    subtype_options.append('')
    subtype_options.sort()

  elif onoff == "Off-chain":
    df2 = df2[df2["Generated on chain?"] == False]
    cat_options = list(set(df2['Category']))
    cat_options.append('')
    cat_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()
    subtype_options = list(set(df2['Subtype']))
    subtype_options.append('')
    subtype_options.sort()

  #Category
  cat = st.sidebar.selectbox(
      'Category',
       cat_options)
  #Filter based on sidebar selection
  if cat != "":
    df2 = df2[df2["Category"] == cat]
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()
    subtype_options = list(set(df2['Subtype']))
    subtype_options.append('')
    subtype_options.sort()


  #Type
  filetype = st.sidebar.selectbox(
      'Type',
       type_options)
  #Filter based on sidebar selection
  if filetype != "":
    df2 = df2[df2["Type"] == filetype]
    subtype_options = list(set(df2['Subtype']))
    subtype_options.append('')
    subtype_options.sort()

  #Subtype
  subtype = st.sidebar.selectbox(
      'Sub-type',
       subtype_options)
  #Filter based on sidebar selection
  if subtype != "":
    df2 = df2[df2["Subtype"] == subtype]

  #Interactive
  interact = st.sidebar.checkbox("Interactive?", value=False);
  #Filter based on sidebar selection
  if interact == True:
    df2 = df2[df2["Interactive"] == interact]

  #Details
  #details = st.sidebar.selectbox(
  #    'Details',
  #     detail_options)
  #if details != "":
  #  df2 = df2[df2["Detail"] == details]

  df2 = df2.sort_values(by=['timestamp'])

  if onoff=="On-chain": text_onoff_gen = "on-chain generated"
  elif onoff=="Off-chain": text_onoff_gen = "off-chain generated"
  elif gen=="Manual": text_onoff_gen = "manually created"
  else: text_onoff_gen = onoff.lower() + " " + gen.lower()

  if interact==True: text_interactive = "interactive "
  #elif interact==False: text_interactive = "non-interactive"
  else: text_interactive = ""

  text_cat = cat.lower()
  text_type = filetype.lower()

  if subtype!="": text_subtype = "based on " + subtype.lower()
  else: text_subtype = ""


  #if ==True: cat_type = 'interactive ' + cat.lower()
  #elif interact==False: cat_type = 'non-interactive ' cat.lower()
  #else: cat_type = filetype.lower() + " based " + cat.lower()

  #if interact==True: cat_type = 'interactive ' + cat.lower()
  #elif interact==False: cat_type = 'non-interactive ' cat.lower()
  #else: cat_type = filetype.lower() + " based " + cat.lower()

  st.write('On Ethereum network, the first ', text_onoff_gen, text_interactive, text_type, text_cat, ' NFT collection', text_subtype, 'was:')
  st.subheader(df2['Title'].iloc[0])
  st.text("")
  st.write(df2['Title'].iloc[0],'was created on',df2['Date'].iloc[0],'. The link to OpenSea:',df2['OpenSea link'].iloc[0])
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

expander = st.expander("Notes")

expander.write("- Interactive means the viewer can change the way the NFT output looks")
expander.write("- For more explanations for each category, see the Types of NFTs page")
#expander.write("- Dynamic image means the viewer sees a different image every time they refresh the image")
#expander.write("- Unigrids or Audioglphys are categorized under 'audio beats'. Audio beats are when there's a single beat or melody that lasts in an infinite loop. Songs are differentiated as being a limited music piece where there are multiple beats/melodies")
expander.write("- Categorization was the hardest part of this project. If you have any feedback, we are open")
expander.write("- In fact, we are open to any feedback!")

#expander = st.expander("Roadmap for NFT Archive")
#expander.write("- Second, third projects in NFT history")
#expander.write("- Firsts in networks other than Ethereum")
#expander.write("- Event more categories!")
#expander.write("- A floor tracker method that's more reliable than what you've seen before. The method is already built, I'm working on API setup")
#expander.write("- Data science approach to art: What makes an art piece more iconic?")