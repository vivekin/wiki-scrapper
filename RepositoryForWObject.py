class ObjectRepository:

    def __init__(self):
        print()

    def getInputSearchArea(self):
        search_inputarea = "/html/body/div[5]/div[1]/div[2]/div/div/form/div/input[1]"
        return search_inputarea


    def getSearchButton(self):
        #search_button = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/button[1]"

        search_button = "/html/body/div[5]/div[1]/div[2]/div/div/form/div/input[4]"
        return search_button

    def getFirstpara(self):

        fp = "/html/body/div[3]/div[3]/div[5]/div[1]"
        return fp
