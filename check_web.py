from __future__ import print_function

import urllib2
import re
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

TESTING = False # use for testing and do not retrieve webpages

site_dir = {"CLP" : "https://www.xoom.com/chile/fees-fx",
			"CAD" : "https://www.xoom.com/canada/fees-fx"}
			
yahoo_url = "http://download.finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=USD%s=X"

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]


sample = """TEXTEXTEXTE FDAEFADFFEAF DFAFDA<span>1 USD = 333.3333 CLP</span>DFAEGDAEFAFDADAEFA 
	GDAA<span>1 USD = 3.3333 CAD</span> fdafjeofaldkfjewoifajdlfkjads"""


for cur,url in site_dir.iteritems():

	TS = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	if TESTING:
		page = sample
	else:
		raw = opener.open(url)
		page = raw.read()

	pat = re.compile("(?!<span>1 USD = )\d+.\d+(?= %s</span>)"%cur)
	
	l = pat.findall(page)
	
	rate = float(l[0])
	print(cur + '\n' + str(rate) + " Xoom")
	
	yrate = pd.read_csv(yahoo_url%cur,header = None)
	yrate = float(yrate[1])
	print (str(yrate) + " Yahoo")
	
	f = open(cur + '.txt' , 'a')
	f.write(TS + ',' + str(rate) + ',' + str(yrate) + '\n')
	f.close()
	
	#Update plots
	df = pd.read_csv(cur+'.txt',parse_dates = [0], index_col = 0)
	ax = df.plot(marker = 'o')
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d   %H'))
	
	plt.savefig(cur + '.png')
	
	time.sleep(1) #wait to avoid raising flags, might not be necesary
	
	
	
	
	
	
	
