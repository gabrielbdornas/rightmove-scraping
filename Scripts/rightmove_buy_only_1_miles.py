import requests
import csv
from datetime import datetime, timedelta
import re, time
import json
import os.path
import random, signal, sys


class ProgramKilled(Exception):
    pass
def signal_handler(signum, frame):
    raise ProgramKilled

class Handler:



  def __init__(self):

    global date
    standartdate = datetime.now()
    date = standartdate.strftime('%Y%m%d %H%M')
    self.filename = 'Scrapes/rightmove_{}.csv'.format(date)
    self.log_names = ['City', 'Buy', 'Rent', 'Status']

    self.fieldnames = ['Ref No.', 'URL', 'Price', 'No. Bedrooms', 'Prop Type', 'Date Listed', 'Address', 'Latitude', 'Longitude', 'Channel', 'airDNA City']
    self.useragent_lists = [
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
      'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Trident/5.0)',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
      'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.64',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 OPR/50.0.2762.58',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
      'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
      'Mozilla/5.0 (Windows NT 6.1; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
      'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
      'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
      'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    ]
    self.session = requests.Session()
    self.base_link = 'https://www.rightmove.co.uk'
    self.ref_buf = []

  def main(self, logger):
    # Read location from csv
    with open('Scripts/unique cities.csv', encoding='utf-8-sig') as csvfile:
      url_list = [line.strip() for line in csvfile.readlines()]
      for i, row in enumerate(url_list):

        log = {}
        num_for_sale = 0
        num_for_rent = 0
        flag_for_sale = True
        flag_for_rent = True

        user_agent = self.useragent_lists[random.randrange(0, len(self.useragent_lists))]
        link = self.make_link(row)
       
        region_id = self.get_locationIdentifier(link, user_agent)
        
        if region_id == None:
          print("ERROR WITH RegionID - " + row)
          continue

        print('Starting: {}, {}, {}, {}'.format(i+1,row, region_id, link))
                
        num_for_sale, flag_for_sale = self.parse_sale_data(region_id, user_agent, row)
#        num_for_rent, flag_for_rent = self.parse_rent_data(region_id, user_agent, row)
        

        print('Finishing: {}, {}, for sale: {}, for rent: {}'.format(i+1, row, num_for_sale, num_for_rent))
        print("")
        # print('* INFO: no: {}, city: {}, region: {} for sale: {}, for rent: {}'.format(i+1, row, region_id, num_for_sale, num_for_rent))
        # break
        log['City'] = row
        log['Buy'] = num_for_sale
        log['Rent'] = num_for_rent
        log['Status'] = 'Ok'
        if flag_for_rent == False or flag_for_sale == False:
          log['Status'] = 'Interrupted'

        #file_exists = os.path.isfile("/home/User/rightmove/Scrapers/Logs/log_{}.csv".format(date))
        #with open("/home/User/rightmove/Scrapers/Logs/log_{}.csv".format(date), "a", newline='') as csvfile:
        file_exists = os.path.isfile("Scrapes/Logs/log_{}.csv".format(date))
        with open("Scrapes/Logs/log_{}.csv".format(date), "a", newline='') as csvfile:

          writer = csv.DictWriter(csvfile, fieldnames=self.log_names)
          if not file_exists:
            writer.writeheader()
          writer.writerow(log)



  def parse_sale_data(self, region_id, user_agent, row):
    
    print('* Getting for sale data ...')
    try:
      num = 0
      headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
      }

      r = self.session.get('https://www.rightmove.co.uk/', headers=headers)

      params = (
          ('locationIdentifier', region_id),
          ('numberOfPropertiesPerPage', '24'),
          ('radius', '1.0'),
          ('sortType', '2'),
          ('index', '0'),
          ('includeSSTC', 'false'),
          ('viewType', 'LIST'),
          ('channel', 'BUY'),
          ('areaSizeUnit', 'sqft'),
          ('currencyCode', 'GBP'),
          ('isFetching', 'false'),
      )

      json_headers = {
        'Accept': 'application/json, text/javascript',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': user_agent
      }
      response = requests.get('https://www.rightmove.co.uk/api/_search', headers=json_headers, params=params)
      jsonD = json.loads(response.text)


      for p in jsonD['properties']:
        buf = {}
        ref_no = p['id']
        url = p['propertyUrl']
        price = p['price']['amount']
        bedrooms = p['bedrooms']
        prop_type = p['propertySubType']
        date_listed = p['firstVisibleDate'].split('T')[0]
        try:
          postcode = p['displayAddress'].split(',')[-1].strip()
        except:
          postcode = ''
        latitude = p['location']['latitude']
        longitude = p['location']['longitude']
        full_address = p['displayAddress'].replace('\r\n', '')

        if ref_no not in self.ref_buf:
          num = num + 1
          buf['Ref No.'] = ref_no
          buf['URL'] = self.base_link + url
          buf['Price'] = price
          buf['No. Bedrooms'] = bedrooms
          buf['Prop Type'] = prop_type
          buf['Date Listed'] = date_listed
          buf['Latitude'] = latitude
          buf['Longitude'] = longitude
          buf['Address'] = full_address
          buf['Channel'] = "For sale"
          buf['airDNA City'] = row



          file_exists = os.path.isfile("{}".format(self.filename))
          
          with open("{}".format(self.filename), "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if not file_exists:
              writer.writeheader()
            writer.writerow(buf)

          self.ref_buf.append(ref_no)
      try:
        total = int(jsonD['pagination']['total'])
      except:
        total = 0

      for page_cnt in range(1, total):
        params = (
            ('locationIdentifier', region_id),
            ('numberOfPropertiesPerPage', '24'),
            ('radius', '1.0'),
            ('sortType', '2'),
            ('index', '{}'.format(24*page_cnt)),
            ('includeSSTC', 'false'),
            ('viewType', 'LIST'),
            ('channel', 'BUY'),
            ('areaSizeUnit', 'sqft'),
            ('currencyCode', 'GBP'),
            ('isFetching', 'false'),
        )

        response = requests.get('https://www.rightmove.co.uk/api/_search', headers=json_headers, params=params)
        try:
          jsonD = json.loads(response.text)
        except:
          break

        for p in jsonD['properties']:
          buf = {}
          ref_no = p['id']
          url = p['propertyUrl']
          price = p['price']['amount']
          bedrooms = p['bedrooms']
          prop_type = p['propertySubType']
          date_listed = p['firstVisibleDate'].split('T')[0]
          try:
            postcode = p['displayAddress'].split(',')[-1].strip()
          except:
            postcode = ''
          latitude = p['location']['latitude']
          longitude = p['location']['longitude']
          full_address = p['displayAddress'].replace('\r\n', '')

          if ref_no not in self.ref_buf:
            num = num + 1
            buf['Ref No.'] = ref_no
            buf['URL'] = self.base_link + url
            buf['Price'] = price
            buf['No. Bedrooms'] = bedrooms
            buf['Prop Type'] = prop_type
            buf['Date Listed'] = date_listed
            buf['Latitude'] = latitude
            buf['Longitude'] = longitude
            buf['Address'] = full_address
            buf['Channel'] = "For sale"
            buf['airDNA City'] = row


            file_exists = os.path.isfile("{}".format(self.filename))
            
            with open("{}".format(self.filename), "a", newline='') as csvfile:
              writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
              if not file_exists:
                writer.writeheader()
              writer.writerow(buf)

            self.ref_buf.append(ref_no)
      return num, True
    except:
      return num, False


  def parse_rent_data(self, region_id, user_agent, row):
    print('* Getting to rent data ...')
    try:
      num = 0
      headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
      }

      r = self.session.get('https://www.rightmove.co.uk/', headers=headers)

      params = (
          ('locationIdentifier', region_id),
          ('numberOfPropertiesPerPage', '24'),
          ('radius', '1.0'),
          ('sortType', '2'),
          ('index', '0'),
          ('includeSSTC', 'false'),
          ('viewType', 'LIST'),
          ('channel', 'RENT'),
          ('areaSizeUnit', 'sqft'),
          ('currencyCode', 'GBP'),
          ('isFetching', 'false'),
      )
      json_headers = {
        'Accept': 'application/json, text/javascript',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': user_agent
      }
      response = requests.get('https://www.rightmove.co.uk/api/_search', headers=json_headers, params=params)
      jsonD = json.loads(response.text)


      for p in jsonD['properties']:
        buf = {}
        ref_no = p['id']
        url = p['propertyUrl']
        price = p['price']['amount']
        frequency = p['price']['frequency']
        bedrooms = p['bedrooms']
        prop_type = p['propertySubType']
        date_listed = p['firstVisibleDate'].split('T')[0]
        try:
          postcode = p['displayAddress'].split(',')[-1].strip()
        except:
          postcode = ''
        latitude = p['location']['latitude']
        longitude = p['location']['longitude']
        full_address = p['displayAddress'].replace('\r\n', '')

        if ref_no not in self.ref_buf:
          num = num + 1
          buf['Ref No.'] = ref_no
          buf['URL'] = self.base_link + url
          buf['Price'] = '{} {}'.format(price, frequency)
          buf['No. Bedrooms'] = bedrooms
          buf['Prop Type'] = prop_type
          buf['Date Listed'] = date_listed
          buf['Latitude'] = latitude
          buf['Longitude'] = longitude
          buf['Address'] = full_address
          buf['Channel'] = "To rent"
          buf['airDNA City'] = row

          file_exists = os.path.isfile("{}".format(self.filename))
          
          with open("{}".format(self.filename), "a", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if not file_exists:
              writer.writeheader()
            writer.writerow(buf)

          self.ref_buf.append(ref_no)
      try:
        total = int(jsonD['pagination']['total'])
      except:
        total = 0

      for page_cnt in range(1, total):
        params = (
            ('locationIdentifier', region_id),
            ('numberOfPropertiesPerPage', '24'),
            ('radius', '1.0'),
            ('sortType', '2'),
            ('index', '{}'.format(24*page_cnt)),
            ('includeSSTC', 'false'),
            ('viewType', 'LIST'),
            ('channel', 'RENT'),
            ('areaSizeUnit', 'sqft'),
            ('currencyCode', 'GBP'),
            ('isFetching', 'false'),
        )

        response = requests.get('https://www.rightmove.co.uk/api/_search', headers=json_headers, params=params)
        try:
          jsonD = json.loads(response.text)
        except:
          break

        for p in jsonD['properties']:
          buf = {}
          ref_no = p['id']
          url = p['propertyUrl']
          price = p['price']['amount']
          frequency = p['price']['frequency']
          bedrooms = p['bedrooms']
          prop_type = p['propertySubType']
          date_listed = p['firstVisibleDate'].split('T')[0]
          try:
            postcode = p['displayAddress'].split(',')[-1].strip()
          except:
            postcode = ''
          latitude = p['location']['latitude']
          longitude = p['location']['longitude']
          full_address = p['displayAddress'].replace('\r\n', '')

          if ref_no not in self.ref_buf:
            num = num + 1
            buf['Ref No.'] = ref_no
            buf['URL'] = self.base_link + url
            buf['Price'] = '{} {}'.format(price, frequency)
            buf['No. Bedrooms'] = bedrooms
            buf['Prop Type'] = prop_type
            buf['Date Listed'] = date_listed
            buf['Latitude'] = latitude
            buf['Longitude'] = longitude
            buf['Address'] = full_address
            buf['Channel'] = "To rent"
            buf['airDNA City'] = row


            file_exists = os.path.isfile("{}".format(self.filename))
            
            with open("{}".format(self.filename), "a", newline='') as csvfile:
              writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
              if not file_exists:
                writer.writeheader()
              writer.writerow(buf)

            self.ref_buf.append(ref_no)
      return num, True
    except:
      return num, False

  def make_link(self, loc):
    buf = []
    loc = loc.replace('-', '')
    for i in range(0, len(loc), 2):
      buf.append(loc.upper()[i:i+2])
    param = '/'.join(buf)
    link = "https://www.rightmove.co.uk/typeAhead/uknostreet/{}".format(param)
    return link

  def get_locationIdentifier(self, link, user_agent):
    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'User-Agent': user_agent,
      'X-Requested-With': 'XMLHttpRequest',
    }

    try:
      r = self.session.get(link, headers=headers)
      jsonD = json.loads(r.text)
      region_id = jsonD['typeAheadLocations'][0]['locationIdentifier']
    except:
      region_id = None
    return region_id

class MockLogger:
  @staticmethod
  def info(message):
    print(message)

  
def log_scraping_start(company, logger):
  start_time = datetime.now()
  logger.info('* Starting: {}'.format(company))
  logger.info('-------------------- Processing starting at: {} --------------------'.format(start_time))
  return start_time


def log_scraping_end(logger):
  end_time = datetime.now()
  logger.info('* Processing ended at: {} ------------------------------'.format(end_time))
  return end_time


if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  
  print_logger = MockLogger()

  log_scraping_start("Rightmove", print_logger)

  C = Handler()
  cont = C.main(print_logger)

  log_scraping_end(print_logger)



###### Move log to ~/Scrapes/Logs/
#standartdate = datetime.now()
#date = standartdate.strftime('%Y%m%d %H%M')

#os.rename('_log.csv','Scrapes/Logs/log_{}.csv'.format(date))
######


#input('Press Enter to Exit...')
