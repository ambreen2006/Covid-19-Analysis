from bs4 import BeautifulSoup
import urllib.request
import requests
import csv

url = "https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

writer = csv.writer(open('canada_covid19.csv', 'w'))
writer_metadata = csv.writer(open('canada_covid19_meta.csv', 'w'))

a1 = soup.find(id='a1')
a1.findNext('caption')
token = 'as of '

caption_info_table = str(a1.findNext('caption').string).strip()
pub_date = caption_info_table[caption_info_table.find(token)+len(token):]
print(pub_date)

writer_metadata.writerow(['Publication Date', pub_date])

head = a1.find_next('thead')

column_names_tr = head.tr

column_names_th = column_names_tr.find_all('th')

print(column_names_th)

columns = [str(th.string).strip() for th in column_names_th]
writer.writerow(columns)

prov_body = a1.find_next('tbody')

for row in prov_body.find_all('tr'):
    values = []
    for data in row.find_all('td'):
        values.append(str(data.string).strip())

    values_parsed = [values[0], int(values[1].replace(',','')), int(values[2].replace(',','')), int(values[3].replace(',',''))]
    writer.writerow(values_parsed)
