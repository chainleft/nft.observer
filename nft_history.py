import streamlit as st
st.set_page_config(layout="wide")

import numpy as np
import pandas as pd
import datetime
import sys
import csv
#from load_css import local_css
#local_css("style.css")


st.title('NFT Collection History')

df = pd.read_csv('nfts.csv')
df = df.replace(np.nan, '', regex=True)

df['address'] = df['Contract'].str.split("https://etherscan.io/address/").str[1]

onoff_options = ["","Off-chain","On-chain"]
gen_options = ["","Manual","Generative"]

cat_options = list(set(df['Category']))
cat_options.append('')
cat_options.sort()

format_options = list(set(df['Format']))
format_options.append('')
format_options.sort()

type_options = list(set(df['Type']))
type_options.append('')
type_options.sort()

interact_options = ["","Interactive","Non-interactive"]

#detail_options = list(set(df['Detail']))
#detail_options.append("")
#detail_options.sort()
#https://api.opensea.io/api/v1/collection/curiocardswrapper

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
    format_options = list(set(df2['Format']))
    format_options.append('')
    format_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()
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
    format_options = list(set(df2['Format']))
    format_options.append('')
    format_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()

  elif onoff == "Off-chain":
    df2 = df2[df2["Generated on chain?"] == False]
    cat_options = list(set(df2['Category']))
    cat_options.append('')
    cat_options.sort()
    format_options = list(set(df2['Format']))
    format_options.append('')
    format_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()

  #Category
  cat = st.sidebar.selectbox(
      'Category',
       cat_options)
  #Filter based on sidebar selection
  if cat != "":
    df2 = df2[df2["Category"] == cat]
    format_options = list(set(df2['Format']))
    format_options.append('')
    format_options.sort()
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()

  #Format
  fileformat = st.sidebar.selectbox(
      'Format',
       format_options)
  #Filter based on sidebar selection
  if fileformat != "":
    df2 = df2[df2["Format"] == fileformat]
    type_options = list(set(df2['Type']))
    type_options.append('')
    type_options.sort()

  #Subtype
  type_selected = st.sidebar.selectbox(
      'Type',
       type_options)
  #Filter based on sidebar selection
  if type_selected != "":
    df2 = df2[df2["Type"] == type_selected]

  #Interactive
  interact = st.sidebar.selectbox(
    'Interactive?',
     interact_options)
  #Filter based on sidebar selection
  if interact == "Interactive":
    df2 = df2[df2["Interactive"] == True]
  elif interact == "Non-interactive":
    df2 = df2[df2["Interactive"] == False]

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

  text_interactive = interact.lower()

  text_cat = cat.lower()
  text_format = fileformat.lower()

  if type_selected!="": text_type = "based on " + type_selected.lower()
  else: text_type = ""


  #if ==True: cat_type = 'interactive ' + cat.lower()
  #elif interact==False: cat_type = 'non-interactive ' cat.lower()
  #else: cat_type = filetype.lower() + " based " + cat.lower()

  #if interact==True: cat_type = 'interactive ' + cat.lower()
  #elif interact==False: cat_type = 'non-interactive ' cat.lower()
  #else: cat_type = filetype.lower() + " based " + cat.lower()
  text_alltypes = text_format + ' ' + text_cat + ' NFT collection ' + text_type
  if text_type == "based on meta":
    text_alltypes = text_format + ' meta NFT collection'
  st.write('On Ethereum network, the first ', text_onoff_gen, text_interactive, text_alltypes, 'was:')
  st.subheader(df2['Title'].iloc[0])
  st.text("")
  st.write(df2['Title'].iloc[0],'was created on',df2['Date'].iloc[0],'.')
  
  text_web = "[Website]("+df2['Website'].iloc[0]+")"
  if df2['Website'].iloc[0]=='':
    text_web = "Website isn't available for this project"

  text_opensea = "[OpenSea]("+df2['OpenSea'].iloc[0]+")"
  if df2['OpenSea'].iloc[0]=='':
    text_opensea = "OpenSea link isn't available for this project"
  
  text_contract = "[Contract]("+df2['Contract'].iloc[0]+")"
  if df2['Contract'].iloc[0]=='':
    text_contract = "Contract link isn't available for this project"
  
  text_twitter = "[Twitter]("+df2['Twitter'].iloc[0]+")"
  if df2['Twitter'].iloc[0]=='':
    text_twitter = "Twitter link isn't available for this project"

  st.write(text_web)
  st.write(text_opensea)
  st.write(text_contract)
  st.write(text_twitter)
  #st.image("https://ipfs.io/ipfs/QmZH7MZK6XGELZNhHre2LJiBcXFpsi1wzhmx1MGcApahnD",width=400, # Manually Adjust the width of the image as per requirement)

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
expander.write("- Categorization was the hardest part of this project. If you have any feedback, we are open")
expander.write("- In fact, we are open to any feedback!")

#expander = st.expander("Roadmap for NFT Archive")
#expander.write("- Second, third projects in NFT history")
#expander.write("- Firsts in networks other than Ethereum")
#expander.write("- Event more categories!")
#expander.write("- A floor tracker method that's more reliable than what you've seen before. The method is already built, I'm working on API setup")
#expander.write("- Data science approach to art: What makes an art piece more iconic?")