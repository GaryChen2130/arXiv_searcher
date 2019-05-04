import urllib.request
import re

author = "Ian+Goodfellow"
url = "https://arxiv.org/search/?query=" + author + "&searchtype=author&size=200"
content = urllib.request.urlopen(url)
html_str = content.read().decode('utf-8')

article_pattern = "arxiv-result[\s\S]*?</li>"
article_list = re.findall(article_pattern, html_str)

pagination_pattern = "pagination-list[\s\S]*?</ul>"
pagination_list = re.findall(pagination_pattern, html_str)

cnt = 0
print("[ Author: " + author + " ]")

for article in article_list:
	date_pattern = "originally announced</span>[\s\S]*?</p>"
	date_list = re.findall(date_pattern, article)
	for announced_date in date_list:
		date = announced_date.split("originally announced</span>")[1].split("</p>")[0].strip()
		print(date)
		cnt = cnt + 1


''' If there are other pages, search those pages with the given author name '''
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
			date_pattern = "originally announced</span>[\s\S]*?</p>"
			date_list = re.findall(date_pattern, article)
			for announced_date in date_list:
				date = announced_date.split("originally announced</span>")[1].split("</p>")[0].strip()
				print(date)
				cnt = cnt + 1
				start_index += 200

print(cnt)




