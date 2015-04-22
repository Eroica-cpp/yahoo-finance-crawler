#!/usr/bin/python
"""
==================================================================
File: 	crawler.py
Author: Tao Li (eroicacmcs@gmail.com)
Date: 	Arp. 22, 2015
Desc: 	Crawl data from Yahoo! Finance
==================================================================
"""

import urllib2
import BeautifulSoup
import re
import sys

# parameters
COMPANY = sys.argv[1]
PATTERN = "http://finance.yahoo.com/q/ae?s="
URL = PATTERN + COMPANY

def getHTML(URL):
	"""
	get raw HTML from given URL
	"""
	print "downloading from " + URL
	req = urllib2.Request(URL)
	con = urllib2.urlopen(req)
	HTML = con.read()
	con.close()
	return HTML

def parse(HTML):
	soup = BeautifulSoup.BeautifulSoup(HTML)
	pattern = re.compile(r"t[hd]") # pattern of every post in the collection page
	raw_results = soup.findAll("table", {"class": "yfnc_tableout1"})
	filename = COMPANY + ".csv"
	f = open(filename, "a")
	counter = 0
	for table in raw_results:
		lines = table.findAll("tr")
		write_content = ""
		if counter >= 1: lines = lines[1:]
		for line in lines:
			items = line.findAll(pattern)
			write_content += "\t".join([i.text for i in items]) + "\n"
		f.write(write_content+"\n")
		counter += 1
	f.close()
	print COMPANY + " DONE!"

def main():

	if len(sys.argv) <= 1:
		print "Usage: python crawler <company_name>"
		print "e.g.: python crawler FB"
		return

	HTML = getHTML(URL)
	parse(HTML)

if __name__ == "__main__":
	main()