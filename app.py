# doing necessary imports
print("App has started yayy!")
import threading
import os
from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
from mongoDBOperations import MongoDBManagement
from WikiScrapping import WikiScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import imageHandler

rows = {}
collection_name = None

logger = getLog('wiki.py')

free_status = True
db_name = 'Wiki-Scrapper'


app = Flask(__name__)  # initialising the flask app with the name 'app'

#For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


#To avoid the time out issue on heroku
class threadClass:

    def __init__(self, searchString, scrapper_object):

        self.searchString = searchString
        self.scrapper_object = scrapper_object

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        global collection_name, free_status
        free_status = False
        collection_name = self.scrapper_object.getInfo(self.searchString)
        #searchString = self.searchString, username = 'mongodb',password = 'mangodb'
        logger.info("Thread run completed")
        free_status = True


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchString = request.form['topic'].replace(" ", "")  # obtaining the search string entered in the form
        searchString = searchString.lower()
        try:
            scrapper_object = WikiScrapper(executable_path=ChromeDriverManager().install(),
                                            chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='mongouser', password='mongouser')
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):

                dtextinfo = mongoClient.findRecordOnQuery(db_name=db_name, collection_name=searchString,query={"type":"textinfo"})
                dimgs = mongoClient.findRecordOnQuery(db_name=db_name, collection_name=searchString,query={"type":"image"})
                summary=dtextinfo[0]["summary"]
                refs=dtextinfo[0]["refs"]
                mongoClient.closeMongoDBconnection()
                imglist = []
                mydir = "static/images"
                clist = [f for f in os.listdir("static/images")]
                for f in clist:
                    os.remove(os.path.join(mydir, f))


                for i in dimgs:
                    imglist.append(i["name"])
                    imageHandler.imagedecode(i["img"],"static/images/{}".format(i["name"]))
                refs.sort()
                searchString=searchString.capitalize()
                result={"name":searchString,"summary":summary,"refs":refs,"images":imglist}
                return render_template('results.html', result=result)  # show the results to user

            else:
                scrapper_object.openUrl("https://en.wikipedia.org/wiki/Main_Page")
                logger.info("Url hitted")
                scrapper_object.searchArticle(searchString=searchString)
                logger.info(f"Search begins for {searchString}")
                print("thread started")
                threadClass( searchString=searchString, scrapper_object=scrapper_object)
                print("thread ended")
                return redirect(url_for('feedback'))

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering .\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    print("in feedbak")
    try:
        global collection_name
        mongoClient = MongoDBManagement(username='mongouser', password='mongouser')
        if collection_name is not None:
            searchString=collection_name
            dtextinfo = mongoClient.findRecordOnQuery(db_name=db_name, collection_name=searchString,
                                                      query={"type": "textinfo"})
            dimgs = mongoClient.findRecordOnQuery(db_name=db_name, collection_name=searchString,
                                                  query={"type": "image"})
            summary = dtextinfo[0]["summary"]
            refs = dtextinfo[0]["refs"]
            mongoClient.closeMongoDBconnection()
            imglist = []
            mydir = "static/images"

            clist = [f for f in os.listdir("static/images")]
            for f in clist:
                os.remove(os.path.join(mydir, f))


            for i in dimgs:
                imglist.append(i["name"])
                imageHandler.imagedecode(i["img"], "static/images/{}".format(i["name"]))
            refs.sort()
            searchString = searchString.capitalize()
            result = {"name": searchString, "summary": summary, "refs": refs, "images": imglist}
            collection_name = None
            return render_template('results.html', result=result)
        else:
            return render_template('results.html', result=None)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))



if __name__ == "__main__":
    app.run()  # running the app on the local machine on port 8000
