# coding=utf-8
__author__ = 'admin'

import urllib2;
from bs4 import BeautifulSoup;
import csv;
import re;
import time;
from numpy import random;
import shelve;
import pandas as pd;
import pickle;
# General Information
# Function

"""
	fieldnames= ['shop_id', 'shop_name', 'avg_stars', 'avg_price', 'address', 'telephone', 'all_comments_count', '5_star_comments_count', '4_star_comments_count', '3_star_comments_count', '2_star_comments_count', '1_star_comments_count'];
"""

class ExtractHtmlContent:
	def __init__(self):
		pass;

	"""
	Comment Module;
	"""
	def extract_single_comment(self, module):
		# author
		# print "============================================================================="
		# print module
		# print "============================================================================="
		auth = module.find("div", class_="pic");
		author = auth.a["user-id"];

		# comment
		comm = module.find("div", class_="comment-txt");
		comment = comm.div.contents[0];

		print "Author %s said something" % (author);

		return author, comment;

	def _inner_function_has_dataid_id(self, tag):
		return tag.name == "li" and tag.has_attr('data-id') and tag.has_attr('id');

	def get_comment(self, content):
		res = {};
		soup = BeautifulSoup(content);
		comment_list = soup.find("div", class_="comment-list");
		for li in comment_list.ul.find_all(self._inner_function_has_dataid_id):
			author, comment = self.extract_single_comment(li);
			res[author.encode('utf-8')] = comment.encode('utf-8');
		print len(res.keys());
		return res;

	"""
	Failure CatchUp
	"""
	def failure_main_page(self, url, url_id):
		print "CatchUp Failure Main Page:\n %s" % url;
		rec = shelve.open("./comments/"+str(url_id) + ".dat");
		if "1star" in url:
			marker = str(1);
		else:
			marker = str(2);
		try:
			content = self.read_url(url);

			f = open('something.html','w')
			f.write(content);
			f.close();

			rec[marker] = self.get_comment_multi_page(content, url, url_id);
			self.random_sleep(self.TIME_BETWEEN_SHOP);
		except Exception,e:
			print e
			if url_id in self.failure_list:
				self.failure_list[url_id].append(url);
			else:
				self.failure_list[url_id] = [url];
		rec.sync();
		rec.close();

	def failure_single_page(self,url, url_id):
		print "CatchUp Failure Single Page:\n %s" % url;
		rec = shelve.open("./comments/"+str(url_id) + ".dat");
		if "1star" in url:
			marker = str(1);
		else:
			marker = str(2);
		try:
			content = self.read_url(url);

			f = open('something.html','w')
			f.write(content);
			f.close();

			rec[marker].update(self.get_comment_multi_page(content, url, url_id));
			self.random_sleep(self.TIME_BETWEEN_SHOP);
		except Exception,e:
			print e
			if url_id in self.failure_list:
				self.failure_list[url_id].append(url);
			else:
				self.failure_list[url_id] = [url];
		rec.sync();
		rec.close();

	def failure_catchup(self):
		f = open('failure.pkl')
		failure = pickle.load(f);
		f.close();
		for url_id in failure:
			urls = failure[url_id];
			for url in urls:
				if "pageno" in url:
					self.failure_single_page(url, url_id);
				else:
					self.failure_main_page(url, url_id);
		self.save_failure_list();

	def failure_disp(self):
		f = open('failure.pkl')
		failure = pickle.load(f);
		f.close();
		for url_id in failure:
			urls = failure[url_id];
			for url in urls:
				print "Fail For %s at %s" %(url_id,url);

	def save_failure_list(self):
		output = open('failure.pkl', 'wb')

		# Pickle dictionary using protocol 0.
		pickle.dump(self.failure_list, output);

		output.close();


class GetShopComment:

	def __init__(self, file_path="shop.csv"):
		# self.extractor = ExtractHtmlContent();
		self.url_base = "http://www.dianping.com";
		self.failure_list = {};
		self.csvdata = pd.read_csv(file_path);
		self.comment_star_candidate = [1,2];


		self.TIME_BETWEEN_SHOP = 0.8;
		self.TIME_BETWEEN_COMMENT_PAGE = 0.5;
		self.TIME_RECOVERY = 60;
		self.TIME_RECOVERY_MULTIPLIER = 0;

		# Error Code
		self.SUCCESS = 0x00;
		self.FAILURE_VERIFICATION = 0x01;
		self.FAILURE_403FORBIDDEN = 0x02;
		self.FAILURE_MISSSHOP = 0x03;

		self.proxy_flag = False;
		self.failure_count = 0;
		pass;

	# Read From Website
	def read_url(self, url):
		i_headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5", "Referer":'http://www.dianping.com/'}

		if self.proxy_flag:
			proxy = 'http://183.19.40.67:3128'
			print "Set Proxy as: %s" % proxy;
			opener = urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}), urllib2.HTTPHandler(debuglevel=1))
			urllib2.install_opener(opener)

		req = urllib2.Request(url, headers=i_headers)
		content = urllib2.urlopen(req).read();
		return content;

	# Write To Failure List File
	def write_failure_list(self):
		f=open('failurelist.txt','w');
		for url in self.failure_list:
			f.write(url)
			f.write("\n");
		f.close()

	def random_sleep(self, base_time=0.8):
		sleeptime = 0.5 * random.randn() + base_time;
		if sleeptime<0:
			sleeptime = 0.8
		print "SLEEP For %s" % str(sleeptime)
		time.sleep(sleeptime)

	# def save_to_file(self, shop_id, tempdic):
	# 	s = shelve.open("./comments/"+str(shop_id) + ".dat");
	# 	s = tempdic;
	# 	s.close();
	# Extract Comment
	"""
	Comment Module;
	"""
	def extract_single_comment(self, module):
		# author
		auth = module.find("div", class_="pic");
		author = auth.a["user-id"];

		# comment
		comm = module.find("div", class_="comment-txt");
		comment = comm.div.contents[0];

		# print "Author %s said something" % (author);
		return author, comment;

	def _inner_function_has_dataid_id(self, tag):
		return tag.name == "li" and tag.has_attr('data-id') and tag.has_attr('id');

	def get_comment(self, content):
		res = {};
		soup = BeautifulSoup(content);

		# Get This Page Comments
		comment_list = soup.find("div", class_="comment-list");
		for li in comment_list.ul.find_all(self._inner_function_has_dataid_id):
			author, comment = self.extract_single_comment(li);
			res[author.encode('utf-8')] = comment.encode('utf-8');
		print "%s Author made comments!" % (len(res.keys()));

		# Get Next Page

		next_page = soup.find("a", class_="NextPage");
		if next_page:
			next_page_url = next_page["href"];
		else:
			next_page_url = None;
		return res, next_page_url;

	def get_comment_multi_page(self, content, url, url_id):
		res = {};

		# First Page
		try:
			res_single, next_url = self.get_comment(content);
			res.update(res_single);
		except Exception,e:
			print "Multi Page Error %s" % e;
			if url_id in self.failure_list:
				self.failure_list[url_id].append(url);
			else:
				self.failure_list[url_id] = [url];

		while next_url:
			new_url = url + next_url;
			print new_url;
			try:
				self.random_sleep(self.TIME_BETWEEN_COMMENT_PAGE);
				content = self.read_url(new_url);
				res_single, next_url = self.get_comment(content);
				res.update(res_single);
			except Exception,e:
				print "Multi Page Next Page Error %s" % e;
				if url_id in self.failure_list:
					self.failure_list[url_id].append(new_url);
				else:
					self.failure_list[url_id] = [new_url];
				next_url = None;
		return res;



	# Main
	"""
	Data Structure:
		Every Single File For Each Shop; Defined as shop_id.dat and registered with shelve(test if it fits)
		Dict:{
			"1_star":{
					  author : comment,
					  author : comment
					},
			"2_star":{
					  author : comment,
					  author : comment
					}
			}
	"""
	def get_page_content_error_code(self, content):
		try:
			soup = BeautifulSoup(content);
			head_title = soup.head.title.contents[0].encode("utf-8");
			print head_title;
			if '商户不存在' in head_title:
				print "商户不存在"
				return self.FAILURE_MISSSHOP
			else:
				return self.FAILURE_VERIFICATION
		except Exception, e:
			return self.FAILURE_VERIFICATION;

	def get_page_content_for_main_function(self, url, url_id):
		try:
			content = self.read_url(url);
			f = open('something.html','w')
			f.write(content);
			f.close();
		except Exception,e:
			print e;
			return self.FAILURE_403FORBIDDEN , {}

		try:
			res = self.get_comment_multi_page(content, url, url_id);
			self.random_sleep(self.TIME_BETWEEN_SHOP);
			return self.SUCCESS, res;
		except Exception,e:
			print e
			return self.get_page_content_error_code(content), {}

	def get_page_content_failure(self, errorCode):
		self.failure_count += 1;
		print "Failure Times: %s, registerd Recovery Gap: %s" % (self.failure_count, self.TIME_RECOVERY_MULTIPLIER);
		self.random_sleep(60 * (self.failure_count + self.TIME_RECOVERY_MULTIPLIER));
		# self.proxy_flag = (not self.proxy_flag);
		# print "Switch Proxy to %s" % (self.proxy_flag);

	def main_function(self):
		marker = 0;
		for ind in self.csvdata.index:
			url_id = self.csvdata["shop_id"][ind];
			marker = ind;
			temp = {};
			for star_count in self.comment_star_candidate:

				if self.csvdata[str(star_count)+"_star_comments_count"][ind] == 0:
					temp[str(star_count)] = {};
					continue;

				url = self.url_base + "/shop/" + str(url_id) + "/review_more_" + str(star_count) + "star";
				print url
				flag = self.FAILURE_VERIFICATION;
				while (flag != self.SUCCESS):
					flag, res = self.get_page_content_for_main_function(url, url_id);
					if flag == self.SUCCESS:
						temp[str(star_count)] = res;
						if 0 < self.failure_count < 15 :
							self.TIME_RECOVERY_MULTIPLIER = self.failure_count - 1;
						self.failure_count = 0;
					elif flag == self.FAILURE_MISSSHOP:
						break;
					else:
						self.get_page_content_failure(flag);
				if flag == self.FAILURE_MISSSHOP:
					break;
			if flag != self.FAILURE_MISSSHOP:
				rec = shelve.open("./comments/"+str(url_id) + ".dat");
				for key in temp.keys():
					rec[key] = temp[key];
				rec.sync()
				rec.close()
		self.save_failure_list();





gsc = GetShopComment();
# gsc.failure_catchup();
# gsc.failure_disp()
gsc.main_function();