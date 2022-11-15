from pygooglenews import GoogleNews

urls = []
gn = GoogleNews(lang = 'en', country = 'US')
results = gn.search('mindree')
newsitems = results['entries']
for item in newsitems[0:5]:
    urls.append(item.link)

print(urls)

