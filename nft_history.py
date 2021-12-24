
import streamlit as st
st.set_page_config(layout="wide")

import numpy as np
import pandas as pd
import datetime
import sys
import csv
#from load_css import local_css
#local_css("style.css")

def pull_organize():
  df = pd.read_csv('nfts_edit.csv')
  df = df.replace(np.nan, '', regex=True)
  df = df[df["Network"] == "Ethereum"]
  df['address'] = df['Contract'].str.split("https://etherscan.io/address/").str[1]
  df['opensea_coll_slug'] = df['OpenSea'].str.split("https://opensea.io/collection/").str[1]
  return df

def build_choices(df,column):
  choices = list(set(df[column]))
  choices.append('')
  choices.sort()
  return choices


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


st.title('NFT Collection History')

df = pull_organize()

onoff_options = ["","Off-chain","On-chain"]
gen_options = ["","Curated","Generative"]
sft_options = ["Included","Excluded"]
interact_options = ["","Interactive","Non-interactive"]

cat_options = build_choices(df,'Category')
format_options = build_choices(df,'Format')
type_options = build_choices(df,'Type')


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
  #Non-fungible or semi-fungible
  sft = st.sidebar.checkbox('Include SFTs (editions)?', value=True)
  #Filter based on sidebar selection
  if sft == False:
    df2 = df2[df2["nonfungibleness"] == "Fully nonfungible"]
    cat_options = build_choices(df2,'Category')
    format_options = build_choices(df2,'Format')
    type_options = build_choices(df2,'Type')

  #Tokenness
  nontokens = st.sidebar.checkbox('Include non-tokens?', value=False)
  #Filter based on sidebar selection
  if nontokens == False:
    df2 = df2[df2["transferrable"] == True]

  #Generative or curated production
  gen = st.sidebar.selectbox(
      'Generative or curated?',
       gen_options)
  #Filter based on sidebar selection
  if gen == "Curated":
    df2 = df2[df2["Generative"] == False]
    onoff_options = ["","Off-chain"]
    cat_options = build_choices(df2,'Category')
    format_options = build_choices(df2,'Format')
    type_options = build_choices(df2,'Type')
  elif gen == "Generative":
    df2 = df2[df2["Generative"] == True]

  #Generated on or off chain
  onoff = st.sidebar.selectbox(
      'Generated on-chain or off-chain?',
       onoff_options)
  #Filter based on sidebar selection
  if onoff == "On-chain":
    df2 = df2[df2["OnChain"] == True]
    cat_options = build_choices(df2,'Category')
    format_options = build_choices(df2,'Format')
    type_options = build_choices(df2,'Type')

  elif onoff == "Off-chain":
    df2 = df2[df2["OnChain"] == False]
    cat_options = build_choices(df2,'Category')
    format_options = build_choices(df2,'Format')
    type_options = build_choices(df2,'Type')

  #Category
  cat = st.sidebar.selectbox(
      'Category',
       cat_options)
  #Filter based on sidebar selection
  if cat != "":
    df2 = df2[df2["Category"] == cat]
    format_options = build_choices(df2,'Format')
    type_options = build_choices(df2,'Type')

  #Format
  fileformat = st.sidebar.selectbox(
      'Format',
       format_options)
  #Filter based on sidebar selection
  if fileformat != "":
    df2 = df2[df2["Format"] == fileformat]
    type_options = build_choices(df2,'Type')

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

  text_sft = ""
  if sft == False: text_sft = " (excluding editioned SFTs)"

  text_nontokens = ""
  if nontokens == True: text_nontokens = " (including non-transferrable entities)"

  if onoff=="On-chain": text_onoff_gen = "on-chain generated"
  elif onoff=="Off-chain": text_onoff_gen = "off-chain generated"
  elif gen=="Curated": text_onoff_gen = "curated"
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
  st.write('On Ethereum network, the first ', text_onoff_gen, text_interactive, text_alltypes, text_sft, text_nontokens, 'was:')
  st.subheader(df2['Title'].iloc[0])
  st.text("")
  st.write(df2['Title'].iloc[0],'was created on',df2['Date'].iloc[0],'.')
  
  text_web = "[Website]("+df2['Website'].iloc[0]+")"
  if df2['Website'].iloc[0]=='':
    text_web = "Website isn't available for this project"

  text_opensea = "[Marketplace]("+df2['OpenSea'].iloc[0]+")"
  if df2['OpenSea'].iloc[0]=='':
    text_opensea = "Marketplace link isn't available for this project"
  
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
  # Manually adjust the width of the image as per requirement
  if df2['image'].iloc[0]!='':
    st.image(df2['image'].iloc[0],width=200, )
  
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
expander.write("- Categorization is determined almost arbitrarily. If you have any feedback, we are open")
expander.write("- In fact, we are open to any feedback!")

#expander = st.expander("Roadmap for NFT Archive")
#expander.write("- Second, third projects in NFT history")
#expander.write("- Firsts in networks other than Ethereum")
#expander.write("- Event more categories!")
#expander.write("- A floor tracker method that's more reliable than what you've seen before. The method is already built, I'm working on API setup")
#expander.write("- Data science approach to art: What makes an art piece more iconic?")