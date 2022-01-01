from selenium import webdriver
from RepositoryForWObject import ObjectRepository
from selenium.webdriver.common.by import By
import requests
from mongoDBOperations import MongoDBManagement
from summaryBot import Summarizer

class WikiScrapper:

    def __init__(self, executable_path, chrome_options):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

    def findElementByClass(self, classpath):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.driver.find_element(By.CLASS_NAME, value=classpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByClass) - ClassPath provided was not found.\n" + str(e))

    def findElementByXpath(self, xpath):
        """
        This function finds the web element using xpath passed
        """
        try:
            element = self.driver.find_element(By.XPATH, value=xpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByXpath) - XPATH provided was not found.\n" + str(e))

    def findElementByTag(self, tag_name):
        """
        This function finds web element using tag_name provided
        """
        try:
            element = self.driver.find_elements(By.TAG_NAME, tag_name)

            return element
        except Exception as e:
            raise Exception(f"(findElementByTag) - ClassPath provided was not found.\n" + str(e))


    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorsObject) - Could not find locators\n" + str(e))

    def checkVisibilityOfElement(self, element_to_be_checked):
        """
        This function check the visibility of element on the webpage
        """
        try:
            if element_to_be_checked in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkVisibilityOfElement) - Not able to check for the element.\n" + str(e))

    def openUrl(self,url):
        """
                This function open the particular url passed.
                :param url: URL to be opened.
                """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))


    def searchArticle(self, searchString):
        """
        This function helps to search using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            search_box_path = self.findElementByXpath(xpath=locator.getInputSearchArea())
            search_box_path.send_keys(searchString)
            search_button = self.findElementByXpath(xpath=locator.getSearchButton())
            search_button.click()
            return True
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(searchArticle) - Something went wrong on searching.\n" + str(e))

    def getSummary(self):
        """
                This function makes the summary.
                """
        try:
            locator = self.getLocatorsObject()
            print("making summary")
            elements=self.findElementByTag("p")
            data=""
            for i in elements:
                data+=i.text
            sum=Summarizer()
            summary=sum.getSummary(data)
            return summary
        except Exception as e:
            raise Exception(f"(summary) - Not able to get the summary.\n" + str(e))

    def getReferences(self):
        """
                This function gets all the references.
                """
        try:
            body=self.findElementByClass("mw-parser-output")

            print("making refs")

            refs = body.find_elements(By.TAG_NAME, "a")
            #refs = self.findElementByTag("a")
            print("list href")
            li=[]
            for i in refs:
                r=i.get_attribute("href")
                li.append(r)
            print("list append start")


            li= [i.split("#")[0] for i in li if (i != "None" and i != None)]
            li=list(set(li))
            #li= [i for i in li if i != None]
            print("list append end")
            return li
        except Exception as e:
            raise Exception(f"(refs) - Not able to get the refs.\n" + str(e))


    def getImages(self):
        """
                This function gets all the images.
                """
        try:
            print("making images")
            body=self.findElementByClass("mw-parser-output")
            imgs = body.find_elements(By.TAG_NAME, "img")
            #imgs = self.findElementByTag("img")

            li=[]
            for i in imgs:
                r=i.get_attribute("src")
                li.append(r)
            return li
        except Exception as e:
            raise Exception(f"(images) - Not able to get the images.\n" + str(e))

    def getInfo(self,searchString):
        try:
            print("inside getinfo")
            summary=self.getSummary()
            refs=self.getReferences()
            images=self.getImages()
            mongoClient = MongoDBManagement(username='mongouser', password='mongouser')
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
            print("downloading images")
            imglist={}
            for i in images:
                if not "data:image" in i:
                    a = requests.get(i, headers=headers)
                    n = i.split('/')[-1].replace("%","p")
                    if "." in n:
                        imglist[n] = {"type": "image", "name": n, "img": a.content}


            result={"type":"textinfo","summary":summary,"refs":refs}
            print("making db entry")
            mongoClient.insertRecord(db_name="Wiki-Scrapper",collection_name=searchString,record=result)
            mongoClient.insertRecords(db_name="Wiki-Scrapper", collection_name=searchString,records=imglist)
            print("done db entry")
            mongoClient.closeMongoDBconnection()
            return searchString

        except Exception as e:
            raise Exception(f"(getinfo) - Not able to scrape from wiki page.\n" + str(e))






