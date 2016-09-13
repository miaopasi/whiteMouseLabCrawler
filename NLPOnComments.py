# coding=utf-8
__author__ = 'Ninespring'

import shelve;
import pandas as pd;
import os;
import csv;


class NLPModule:
	def __init__(self):
		self.vocabulary = ["拉肚子", "腹泄", "闹肚子","胃疼","肚子疼","肚子痛"];
		self.csvdata = pd.read_csv("shop.csv");
		self.fieldname = ["shop_id"]+self.vocabulary;

	def get_vocabulary(self, rec):
		res = {}
		lastauthor = None;
		for word in self.vocabulary:
			res[word] = 0;
		for key in rec.keys():
			comments = rec[key];
			for author in comments:
				comm = comments[author];
				for word in self.vocabulary:
					if word in comm:
						if lastauthor!= None and int(author)== int(lastauthor):
							lastauthor = author;
						else:
							lastauthor = author;
							print "%s : %s" % (author, comm);
						res[word] += 1;
		return res;

	def get_csv_writer(self):
		self.csvfile = open("shop_comment.csv","w");
		self.csvWriter = csv.DictWriter(self.csvfile, fieldnames=self.fieldname);
		self.csvWriter.writeheader();

	def close_csv_writer(self):
		self.csvfile.flush();
		self.csvfile.close();

	def write_to_csv(self, res, url_id):
		temp = {}.fromkeys(self.fieldname);
		temp["shop_id"] = url_id;
		for word in self.vocabulary:
			temp[word] = res[word];
		self.csvWriter.writerow(temp);
		self.csvfile.flush();

	def main_function(self):
		self.get_csv_writer();

		for ind in self.csvdata.index:
			url_id = self.csvdata["shop_id"][ind];
			filepath = "./comments_NLP/" + str(url_id) + ".dat.db";
			if os.path.exists(filepath):
				print "Shop %s" % url_id;
				print "=============================================="
				rec = shelve.open(filepath);
				res = self.get_vocabulary(rec);
				self.write_to_csv(res, url_id);
				print "=============================================="

		self.close_csv_writer();

nlp = NLPModule();
nlp.main_function();
