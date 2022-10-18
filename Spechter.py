import streamlit as st

from psaw import PushshiftAPI
import pandas as pd
import waybackpy
import urllib.request
import random
import string
import requests
import hashlib
import ipyplot
from waybackpy import WaybackMachineCDXServerAPI

api = PushshiftAPI()
st.set_page_config(layout='wide')

st.selectbox('Pick secret', st.secrets["secretlist"])

with open('user.txt','r') as f:
    stored_users = f.readlines()
    stored_users = list(map(lambda x:x.strip(),stored_users))
f.close()

@st.cache(suppress_st_warning=True)
def bake(url_collection):
	link = ""
	filetype = ""
	user_agent = "ua.chrome"
	user_agent = "my new app's user agent"
	# df = df[:15]
	d = 0
	waybacked = []
	title = []
	for i, reddit_url in enumerate(url_collection):

		d += 1

		try:

			cdx_api = WaybackMachineCDXServerAPI(reddit_url, user_agent)
			link = cdx_api.oldest().archive_url
			index = link.find("/" + reddit_url)
			link = link[:index] + 'if_' + link[index:]
			waybacked.append(link)
		except:
			st.write("failed")

	st.write("Waybacking finished. " +str(len(waybacked))+ "/" +str(len(url_collection))+" waybacked.")
	st.write("Baked!")
	st.snow()
	return waybacked

@st.cache
def search_SFW(author_name, limit):

	gen = api.search_submissions(author = author_name , over_18 = False, filter=['selftext','author', 'title', 'subreddit','url'], limit = limit)
	df = pd.DataFrame([thing.d_ for thing in gen])

	return df
@st.cache
def search_NSFW(author_name, limit):

	gen = api.search_submissions(author = author_name , over_18 = True, filter=['selftext','author', 'title', 'subreddit','url'] , limit = limit)
	df = pd.DataFrame([thing.d_ for thing in gen])

	return df

st.header('Spechter')

tab1, tab2 = st.tabs(["New users", "Stores users"])

author_text = tab1.text_input('User')
author_db = tab2.selectbox('Choose User', stored_users)

col1,col2,col3, col4,col5 = st.columns(5)

sfw = col1.checkbox("SFW")
nsfw = col2.checkbox("NSFW")
sfw_WB = col3.checkbox("Bake SFW")
nsfw_WB = col4.checkbox("Bake NSFW")
limit = col5.number_input("Limit", min_value= 0, value=2000, step= 1, label_visibility = "collapsed" )



if st.button('Raw', key="Starte"):

	if author_text:
		df_sfw = search_SFW(author_text, limit)
		df_nsfw = search_NSFW(author_text, limit)
		with open('user.txt', 'a') as f:
			if author_text not in stored_users:
				f.write(str(author_text) + '\n')
		f.close()

	elif author_db:
		df_sfw = search_SFW(author_db, limit)
		df_nsfw = search_NSFW(author_db, limit)



	tab1, tab2, tab3, tab4 = st.tabs(["SFW", "NSFW", "Backed SFW","Backed NSFW"])

	if sfw:

		with tab1.expander("Activity", expanded=False):

			st.table(df_sfw["subreddit"].value_counts())
			st.dataframe(df_sfw[["created_utc", 'selftext', 'author', 'title', 'subreddit', 'url']], use_container_width=True)

		with tab1.expander("Pictures", expanded=True):
			st.image(list(df_sfw[df_sfw['url'].str.contains('i.redd.it')]["url"]), caption = list(df_sfw[df_sfw['url'].str.contains('i.redd.it')]["title"]), width=150)
	else:
		tab1.info("Unchecked!")


	if nsfw:
		with tab2.expander("Activity", expanded=False):
			st.dataframe(df_nsfw[["created_utc", 'selftext', 'author', 'title', 'subreddit', 'url']], use_container_width=True)
			st.table(df_nsfw["subreddit"].value_counts())

		with tab2.expander("Pictures", expanded=True):
			st.image(list(df_nsfw[df_nsfw['url'].str.contains('i.redd.it')]["url"]), caption = list(df_nsfw[df_nsfw['url'].str.contains('i.redd.it')]["title"]), width=150)
	else:
		tab2.info("Unchecked!")


	if sfw_WB:
		tab3.write("backing SFW")
		baked_sfw = bake(list(df_sfw[df_sfw['url'].str.contains('i.redd.it')]["url"]))
		tab3.write("backing SFW done")
		tab3.image(baked_sfw, width=150)
	else:
		tab3.info("Unchecked!")

	if nsfw_WB:
		tab4.write("backing NSFW")
		baked_nsfw = bake(list(df_nsfw[df_nsfw['url'].str.contains('i.redd.it')]["url"]))
		tab4.write("backing NSFW done")
		tab4.image(baked_nsfw, width=150)

	else:
		tab4.info("Unchecked!")
