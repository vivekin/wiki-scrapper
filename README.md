# wiki-scrapper

This is a web scrapper buit to scrape wikipedia. This app uses Flask,Selenium,Chrome webdriver,NLTK.
- This app is hosted on heroku, giving the link below.

https://pacific-temple-77915.herokuapp.com/

- app.py -- is the main python file where flask appication is written
- WikiScrapping.py -- module to scrape text,references and images from wikipedia page and store it in mongo db
- imageHandler.py -- module to encode and decode images into base64
- mongoDBOperations.py -- module to perform mongo db operations
- summaryBot.py -- module to summarise long text into a short summary using nltk
- RepositoryForWObject.py
- logger_class.py

