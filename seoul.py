import csv

from bs4 import BeautifulSoup

reader = csv.reader(open('data/newData.csv', 'r'), delimiter=",")

svg = open('data/Seoul_districts.svg', 'r').read()

senior_count = {}
counts_only = []
min_value = 100;
max_value = 0;
past_header = False

for row in reader:
    if not past_header:
        past_header = True
        continue

    try:
        unique = row[0]
        count = float(row[1].strip())
        senior_count[unique] = count
        counts_only.append(count)
    except:
        pass

soup = BeautifulSoup(svg,"html.parser")


paths = soup.findAll('path')

colors = ["#190707","#3B0B0B","#8A0808","#DF0101", "#DF3A01", "#DF7401", "#DBA901", "#D7DF01", "#A5DF00", "#74DF00", "#3ADF00", "#088A4B"]

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

print senior_count

for p in paths:
    if p['id']:
        try:
            count = senior_count[p['id']]
        except:
            continue
        print count
        if count > 700:
            color_class = 0
        elif count > 630:
            color_class = 1
        elif count > 560:
            color_class = 2
        elif count > 490:
            color_class = 3
        elif count > 420:
            color_class = 4
        elif count > 350:
            color_class = 5
        elif count > 280:
            color_class = 6
        elif count > 210:
            color_class = 7
        elif count > 140:
            color_class = 8
        elif count > 70:
            color_class = 9
        else:
            color_class = 10

        color = colors[color_class]
        p['style'] = path_style + color

print soup.prettify()
