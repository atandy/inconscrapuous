import requests
import bs4
import time
import datetime
from IPython import embed


# Good test URL: https://dcurt.is/

#  blog_url = raw_input('Blog url >> ')
blog_url = 'https://dcurt.is/'

dict_list = []
year_list = []

# get the html
r = requests.get(blog_url)
html = r.content
soup = bs4.BeautifulSoup(html, "html.parser")

# Check if the blog spans multiple pages.
last_one = soup.findAll('span', {'class': 'last'})

# If it doesn't just grab the info from the first page.
if not last_one:
    articles = soup.findAll('article', {'class': 'post user_show'})
    for article in articles:
        try:
            # information for each article
            article_title = article('a')[0].getText().encode('utf-8')
            datestring = article('time')[0].get('datetime').encode('utf-8')
            new = datetime.datetime.strptime(datestring, "%Y-%m-%d")
            month = new.strftime("%B")
            link = 'http:'+article('a')[0].get('href').encode('utf-8')
            mdown_link = '- [%s](%s)' % (article_title, link)
            year = int(datestring.split('-')[0])

            d = {
            'link': mdown_link,
            'date': datestring,
            'year': year
            }
            dict_list.append(d)
            year_list.append(year)

        except Exception as e:
            pass

# TODO: This loop is duplicating page 22, skipping 23, and getting 24.  WHY
else:
    page_count = int(last_one[0]('a')[0].get('href').encode('utf-8').split('/')[2])
    alist = []
    for number in range(1, page_count + 1):  # include the last page
        time.sleep(1)  # don't generate too many requests too quickly
        full_url = blog_url + "/page/{}".format(number)
        r = requests.get(full_url)
        html = r.content
        soup = bs4.BeautifulSoup(html, "html.parser")
        articles = soup.findAll('article', {'class': 'post user_show'})
        alist.append(articles)
    for articles in alist:
        for article in articles:
            try:
                article_title = article('a')[0].getText().encode('utf-8')
                datestring = article('time')[0].get('datetime').encode('utf-8')
                new = datetime.datetime.strptime(datestring, "%Y-%m-%d")
                month = new.strftime("%B")
                link = 'http:'+article('a')[0].get('href').encode('utf-8')
                mdown_link = '- [%s](%s)' % (article_title, link)
                year = int(datestring.split('-')[0])

                d = {
                    'link': mdown_link,
                    'date': datestring,
                    'year': year
                    }
                dict_list.append(d)
                year_list.append(year)
            except Exception as e:
                pass


# Loop for appropriate number of headings  to determine number of year headings


current_year = datetime.datetime.now().year
oldest_post_year = sorted(year_list)[0]
year_count = current_year - oldest_post_year


output = \
"""=============================================================================
|| Here's your archive.  You can copy/paste the output below into a new post:
=============================================================================\n"""
print output
print '#Archive'
for number in range(0, year_count+1):  # need to include the current year, so expand year count...kind of dumb)
    print '\n##Posts from %i' % (current_year - number)
    for d in dict_list:
        if d['year'] == (current_year - number):
            print d['link'] + "  " + "*(" + d['date'] + ")*"



