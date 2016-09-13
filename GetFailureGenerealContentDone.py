__author__ = 'admin'

import urllib2;
from bs4 import BeautifulSoup;
import csv;
import re;
import time;
from numpy import random;


def getGeneralInformation(url_id, writer, content):

	info_dic = {}.fromkeys(fieldnames);

	info_dic["shop_id"] = url_id;


	soup = BeautifulSoup(content);

	# Get General Information

	avg_star = soup.find("div",class_="info-name");
	print avg_star.h2.a.contents[0]
	info_dic['shop_name'] = avg_star.h2.a.contents[0].encode('utf-8'); # Shop Name

	avgStarString = avg_star.div.span["class"][1];
	print float(avgStarString[-2:])/10.0
	info_dic['avg_stars'] = float(avgStarString[-2:])/10.0 # Average Star Number

	price = str(avg_star.div.strong.contents[0].encode('utf-8'))

	pattern = re.compile(r"\D*(\d*)\D*");
	match = pattern.match(price);
	try:
		price_res = int(match.groups()[0]);
		info_dic['avg_price'] = price_res; # Average Price
	except:
		info_dic['avg_price'] = -1;

	shop_info_list = soup.find("div",class_="info-list");
	for li in shop_info_list.findAll("li"):
		if li.em and li.a:
			#address
			print li.em.contents[0]
			print li.a.contents[0]
			info_dic['address'] = li.a.contents[0].encode('utf-8'); #Address
		elif li.em:
			#telephone
			print li.em.contents[0]
			print li.contents[1]
			info_dic['telephone'] = li.contents[1].encode('utf-8'); #Telephone
		else:
			pass;
	# Get Comments Count
	comment_star = soup.findAll("div",class_="comment-star");
	res = comment_star.pop().dl;
	for dd in res.findAll("dd"):
		if dd.span.a:
			name = dd.span.a.contents[0]
			info_dic[projection[name]] = int(dd.span.em.contents[0][1:-1]);
		else:
			name = dd.span.contents[0]
			print name;
			info_dic[projection[name]] = 0;

	print info_dic

	writer.writerow(info_dic);
	csvfile.flush()


#Main

fieldnames= ['shop_id', 'shop_name', 'avg_stars', 'avg_price', 'address', 'telephone', 'all_comments_count', '5_star_comments_count', '4_star_comments_count', '3_star_comments_count', '2_star_comments_count', '1_star_comments_count'];

projection = {u'\u5168\u90e8':'all_comments_count',
        u'5\u661f':'5_star_comments_count',
        u'4\u661f':'4_star_comments_count',
		u'3\u661f':'3_star_comments_count',
		u'2\u661f':'2_star_comments_count',
		u'1\u661f':'1_star_comments_count'}


csvfile = open('shop.csv','a');
writer = csv.DictWriter(csvfile, fieldnames = fieldnames);
writer.writeheader();




url_base = "http://www.dianping.com";

f = open("failurelist.txt");
shoplist = f.readlines();
f.close();
i_headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5", "Referer":'http://www.dianping.com/'}


# proxy website: http://ip.zdaye.com/
proxylist = ["211.51.90.211:8080","218.24.94.74:80"]
proxy_pointer = 0;

failure_list = [];
try:
	for ind, shopurl in enumerate(shoplist):
		url_id = shopurl[29:-13];
		url = shopurl
		print url_id
		print url
		proxy = 'http://115.182.15.27:8080'
		opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), urllib2.HTTPHandler(debuglevel=0 ))
		urllib2.install_opener(opener)

		req = urllib2.Request(url, headers=i_headers)
		content = urllib2.urlopen(req, timeout=2).read();
		f = open('something.html','w')
		f.write(content);
		f.close();
		try:
			getGeneralInformation(url_id, writer, content);

		except:
			print "Fail"
			failure_list.append(url);
		sleeptime = 0.5 * random.randn() + 0.5;
		if sleeptime<0:
			sleeptime = 0.5;
		print "SLEEP For %s" % str(sleeptime);
		time.sleep(sleeptime);
except Exception,e:
	print e;
	for i in range(ind,len(shoplist)):
		failure_list.append(shoplist[i])

csvfile.close();


f = open('failurelist.txt','w');
for url in failure_list:
	f.write(url)
f.close()