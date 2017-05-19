from __future__ import print_function

import urllib2
import re
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

TESTING = False # use for testing and do not retrieve webpages

xoom_url = {"CLP" : "https://www.xoom.com/chile/fees-fx",
			"CAD" : "https://www.xoom.com/canada/fees-fx"}
			
yahoo_url = "http://download.finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=USD%s=X"

transferwise_url = 'https://transferwise.com/us/currency-converter/usd-to-%s-rate?amount=1'

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0'),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}



sample = """TEXTEXTEXTE FDAEFADFFEAF DFAFDA<span>1 USD = 333.3333 CLP</span>DFAEGDAEFAFDADAEFA 
	GDAA<span>1 USD = 3.3333 CAD</span> fdafjeofaldkfjewoifajdlfkjadstt =<td data-rate-times-amount="CLP" value="1">333.3333 CLP</td>
	dfdjfljdfkltt = '<td data-rate-times-amount="CAD" value="1">3.3333 CAD</td>'fdkfaodjfadjfadls
	dfjldfjaldfjaldfjadlfjadlfeoiei
	"""

#ts_text = {}

for cur,url in xoom_url.iteritems():

	TS = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	#Read Xoom.com
	if TESTING:
		page = sample
	else:
		raw = opener.open(url)
		page = raw.read()
		
	pat = re.compile("(?!<span>1 USD = )\d+.\d+(?= %s</span>)"%cur)
	
	l = pat.findall(page)
	
	rate = float(l[0])
	print(cur + '\n' + str(rate) + " Xoom")

	#Read Transferwise.com
	raw = opener.open(transferwise_url%cur)
	page = raw.read()
	
	pat = re.compile('(?!<td data-rate-times-amount="%s" value="1">)\d*.\d*(?= %s</td>)'%(cur,cur))
	l = pat.findall(page)
	
	twrate = float(l[0])
	print(str(twrate) + " Transferwise")

	
	yrate = pd.read_csv(yahoo_url%cur,header = None)
	yrate = float(yrate[1])
	print (str(yrate) + " Yahoo")
	
	f = open(cur + '.txt' , 'a')
	f.write(TS + ',' + str(rate) + ',' + str(yrate) + ',' + str(twrate) + '\n')
	f.close()
	
	#Update plots
	df = pd.read_csv(cur+'.txt',parse_dates = [0], index_col = 0)
	ax = df.plot(marker = 'o')
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d   %H'))
	
	plt.savefig(cur + '.png')
	
	time.sleep(1) #wait to avoid raising flags, might not be necesary
	
print('bye')

# req = urllib2.Request('https://transferwise.com/us/currency-converter/usd-to-clp-rate?amount=1', headers=hdr)

# page = urllib2.urlopen(req)

# content = page.read()
# print(content)
	

