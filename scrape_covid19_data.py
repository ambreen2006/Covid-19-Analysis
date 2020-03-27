from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import requests
import csv

class DataScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def parse(self, in_memory = False):
        self.fetchData()
        a1 = self.soup.find(id='a1')
        a1.findNext('caption')
        token = 'as of '

        caption_info_table = str(a1.findNext('caption').string).strip()
        pub_date = caption_info_table[caption_info_table.find(token)+len(token):]

        head = a1.find_next('thead')
        column_names_tr = head.tr
        column_names_th = column_names_tr.find_all('th')

        columns = [str(th.string).strip() for th in column_names_th]
        
        prov_body = a1.find_next('tbody')
        values_parsed = []
        
        for row in prov_body.find_all('tr'):
            values = []
            for data in row.find_all('td'):
                values.append(str(data.string).strip())
            values_parsed.append([values[0], int(values[1].replace(',','')), int(values[2].replace(',','')), int(values[3].replace(',',''))])
        
        if not in_memory:
            self.write('canada_covid19.csv', 'canada_covid19_meta.csv', values_parsed, columns, pub_date)

        cdata = pd.DataFrame(values_parsed, columns = columns)
        return cdata, pub_date

    def write(self, filename, meta_filename, values_parsed, columns, pub_date):
        writer = csv.writer(open(filename, 'w'))
        writer_metadata = csv.writer(open(meta_filename, 'w'))
        writer_metadata.writerow(['Publication Date', pub_date])
        writer.writerow(columns)
        writer.writerow(values_parsed)    
    
    def fetchData(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, "html.parser")

if __name__ == "__main__":
    url = "https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html"
    scraper = DataScraper(url)
    data, current = scraper.parse(in_memory = False)
    print("Publication Date ", current)
    print(data)
