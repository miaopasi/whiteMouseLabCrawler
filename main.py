__author__ = 'Ninespring'

from bs4 import BeautifulSoup;
import re;
import urllib,urllib2;


'''
import urllib
def url_proxies():
proxylist = (  '211.167.112.14:80',  '210.32.34.115:8080',  '115.47.8.39:80',  '211.151.181.41:80',  '219.239.26.23:80',  )
for proxy in proxylist:
proxies = {'': proxy}
opener = urllib.FancyURLopener(proxies)
f = opener.open("http://www.dianping.com/shanghai")
print f.read()


import urllib2
def url_user_agent(url):
# proxy = 'http://211.167.112.14:80'
# opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), urllib2.HTTPHandler(debuglevel=1))
# urllib2.install_opener(opener)
i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",\  "Referer": 'http://www.dianping.com/'}
req = urllib2.Request(url, headers=i_headers)
return urllib2.urlopen(req).read()
#print url_user_agent('http://www.dianping.com/shanghai')


'''




url_base = "http://www.dianping.com/search/keyword/2/10_%E6%9C%9B%E4%BA%AC/p";


i_headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5", "Referer":'http://www.dianping.com/'}

f = open("shoplist.txt","w");

for i in range(1,51):
	url = url_base + str(i);
	req = urllib2.Request(url, headers=i_headers)
	content = urllib2.urlopen(req).read()
	print "Page %s" % str(i);

	# #
	# f = open('something.html','w');
	# f.write(content);
	# f.close();
	# #
	soup = BeautifulSoup(content);
	shop_list_html = soup.findAll('div',class_="pic");
	for shop in shop_list_html:
		print shop.a["href"]
		f.write(shop.a["href"]);
		f.write("\n");
	f.flush();
f.close();