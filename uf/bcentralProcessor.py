# This class provides all the business logic related to managing data from the BCentral website
# The idea is to keep the logic end of stuff separate form the functionality that Django demands
# This class implements a Web Scraper that uses Selenium and has a 1 second delay while refreshing pages to avoid looking like a bot
#     For sake of performance, it does incremental updates - the assumption is that only newer records need to be added
# There is also a clearDB method which empties the table so you can see how the selenium integration works from scratch


from bs4 import BeautifulSoup

from selenium import webdriver
import time
import datetime

from .models import ufHistory
from .globalConstants import globalConstants

class bcentralProcessor():
    # This needs to be called only once (per day) to update the database
    def retrieveUFDataWithSelenium(self):
        browser = webdriver.Chrome(executable_path = globalConstants.chromeDriverLocation)
        browser.get(globalConstants.startUrls[0])

        htmlDoc = browser.page_source
        soup = BeautifulSoup(htmlDoc, 'lxml')
        
        allYearsTags = soup.find_all("option")

        latestKnownUfDate = datetime.date(1900, 1, 1)
        if ufHistory.objects.all().count() > 0: # handling case when DB is empty
            latestKnownUfDate = ufHistory.objects.latest('publishedDate').publishedDate # Picking latest data to perform imcremental updates

        for yearTag in allYearsTags:
            year = yearTag.string

            if int(year) < latestKnownUfDate.year:
                continue    # Support incremental updates
            
            time.sleep(1)   # Set a delay to avoid being kicked out by server for being a bot
            
            browser.find_element_by_xpath('//*[@id="DrDwnFechas"]/option[contains(text(), %s)]' % year).click()
            
            htmlDoc = browser.page_source
            soup = BeautifulSoup(htmlDoc, 'lxml')
            
            for tag in soup.find_all("span", class_="obs"): 
                #tag['id'] has details on date and month
                #tag.string has the UF Value
                ufValue = 0
                if  tag.string != None:
                    ufValue = self.extractUfValue(tag.string)
                
                if(ufValue != 0):   # Keeping it simple. Not checking for invalid dates
                    ufDate = self.extractUfDate(tag['id'], int(year))
                    if ufDate > latestKnownUfDate:  # Perform only incremental updates
                        uf = ufHistory(publishedDate=ufDate, ufValue = ufValue)
                        uf.save();
        
        browser.quit()
        return 1

    # This call will clear DB. Make sure to call retrieveUFDataWithSelenium to populate DB again
    def clearDB(self):
        ufHistory.objects.all().delete()
        return
    
    # These are helper methods to keep things clean
    def extractUfValue(self, ufValueAsString):
        return float(ufValueAsString.replace('.','').replace(',', '.'))
    
    def extractUfDate(self, tagDayMonthId, year):
        day = int(tagDayMonthId[6:8]) - 1       # because Day 01 starts on row 2
        month = globalConstants.monthdict[tagDayMonthId[9:]]
        ufDate = datetime.date(year, month, day)
        return ufDate

    # These static methods provide functionality to retrieve data from the DB
    @staticmethod
    def convertYyyyMmDdStringToDate(yyyyMmDdString):
        try:
            if len(yyyyMmDdString) == 8:
                ufYear = int(yyyyMmDdString[0:4])
                ufMonth = int(yyyyMmDdString[4:6])
                ufDay = int(yyyyMmDdString[6:8])
                ufDate = datetime.date(ufYear, ufMonth, ufDay)
            else:
                return None
        except:
            return None

        return ufDate
    
    @staticmethod
    def convertvalueStringToFloat(valueString):
        try:
            return float(valueString)
        except:
            return None
        
    # This returns a dictionary with inputs and computed output.
    @staticmethod
    def computeUfFromQueryString(queryString):
        ufDate = bcentralProcessor.convertYyyyMmDdStringToDate(queryString.get('date'))
        inputValue = bcentralProcessor.convertvalueStringToFloat(queryString.get('value'))
        
        params = {'ufDate': ufDate,
                  'inputValue': inputValue,
                  'ufHistoricalValue': None,
                  'ufEquivalent': 0
                  }
        
        if params['ufDate'] and params['inputValue']:   # Both are not None
            ufHistoricalValue = ufHistory.objects.filter(publishedDate=ufDate)
            if ufHistoricalValue.exists():
                params['ufHistoricalValue'] = ufHistoricalValue.first().ufValue
                params['ufEquivalent'] = params['ufHistoricalValue'] * params['inputValue']
        
        return params














