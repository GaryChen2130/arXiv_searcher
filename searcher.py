import urllib.request
import re
import matplotlib.pyplot as plt
import numpy as np

author = input("Please input author name for searching.\n")
url = "https://arxiv.org/search/?query=" + author.replace(" ","+") + "&searchtype=author&size=200"
content = urllib.request.urlopen(url)
html_str = content.read().decode('utf-8')

article_pattern = "arxiv-result[\s\S]*?</li>"
article_list = re.findall(article_pattern, html_str)

pagination_pattern = "pagination-list[\s\S]*?</ul>"
pagination_list = re.findall(pagination_pattern, html_str)

cnt = 0
co_author_list = {}
year_list = {}
print("[ Author: " + author + " ]")

"""
Get the list of author names of each article, and judge if it contains the given author name.
If so, record the name of co-authors and announced year of the article.
"""
for article in article_list:

	authors_pattern = "authors\">[\s\S]*?</p>"
	authors_list = re.findall(authors_pattern, article)
	if authors_list[0].find(author) == -1:
		continue

	name_pattern = "<a[\s\S]*?</a>"
	name_list = re.findall(name_pattern, authors_list[0])
	for name in name_list:
		author_name = name.split("\">")[1].split("</a>")[0].strip()
		if author_name == author:
			continue
		if author_name in co_author_list:
			co_author_list[author_name] += 1
		else:
			co_author_list[author_name] = 1
		'''print(author_name)'''

	date_pattern = "originally announced</span>[\s\S]*?</p>"
	date_list = re.findall(date_pattern, article)
	for announced_date in date_list:
		date = announced_date.split("originally announced</span>")[1].split("</p>")[0].strip()
		year = date.split(" ")[1].split(".")[0]
		if year in year_list:
			year_list[year] += 1
		else:
			year_list[year] = 1
		'''print(year)'''
		cnt = cnt + 1


""" 
If there are other pages, search those pages with the given author name 
"""
start_index = 200;
if len(pagination_list) > 0:
	page_pattern = "<li>[\s\S]*?</li>"
	page_list = re.findall(page_pattern, pagination_list[0])
	for i in range(len(page_list) - 1):
		url_nxt = url + "&start=" + str(start_index)
		content = urllib.request.urlopen(url_nxt)
		html_str = content.read().decode('utf-8')

		article_pattern = "arxiv-result[\s\S]*?</li>"
		article_list = re.findall(article_pattern, html_str)
		for article in article_list:
			authors_pattern = "authors\">[\s\S]*?</p>"
			authors_list = re.findall(authors_pattern, article)
			if authors_list[0].find(author) == -1:
				continue

			name_pattern = "<a[\s\S]*?</a>"
			name_list = re.findall(name_pattern, authors_list[0])
			for name in name_list:
				author_name = name.split("\">")[1].split("</a>")[0].strip()
				if author_name == author:
					continue
				if author_name in co_author_list:
					co_author_list[author_name] += 1
				else:
					co_author_list[author_name] = 1
				'''print(author_name)'''

			date_pattern = "originally announced</span>[\s\S]*?</p>"
			date_list = re.findall(date_pattern, article)
			for announced_date in date_list:
				date = announced_date.split("originally announced</span>")[1].split("</p>")[0].strip()
				year = date.split(" ")[1].split(".")[0]
				if year in year_list:
					year_list[year] += 1
				else:
					year_list[year] = 1
				'''print(year)'''
				cnt = cnt + 1
				start_index += 200

sorted_year = sorted(year_list.items(),key = lambda d: d[0])
'''print(sorted_year)'''
x_list = []
y_list = []
for years,times in sorted_year:
	x_list.append(years)
	y_list.append(times)

plt.bar(x_list,y_list)

sorted_co_author = sorted(co_author_list.items(),key = lambda d: d[0])
'''print(sorted_co_author)'''
for co_author,times in sorted_co_author:
	if times > 1:
		print("[" + co_author + "]: " + str(times) + " times")
	else:
		print("[" + co_author + "]: " + str(times) + " time")

plt.show()




