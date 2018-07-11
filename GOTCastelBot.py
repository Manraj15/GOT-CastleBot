from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import requests
import re
import bs4

path = "/Users/manrajthind/Documents/GOT_caste_bot/commented.txt"
header = '**Background of this castle:** \n'
footer = "\n*---I am a bot of house Binary | My father is [USERNAME]"

def authenticate():
    print("Authenticating...\n")
    reddit = praw.Reddit(client_id='[CLIENT_ID]',
                client_secret="[CLIENT_SECRET]", password='[PASSWORD]',
                user_agent='web:GOT-castle-bot:v0.1 (by [USERNAME])', username='[USERNAME]')
    print('hi')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def getTitleArray(title):
    titleArray = title.split()
    for word in titleArray:
        if word[0] == "[":
            titleArray.remove(word)

    return titleArray
            

def getCastelList():
    r = requests.get("https://awoiaf.westeros.org/index.php/Category:Castles")
    soup = BeautifulSoup(r.content, 'html.parser')
    tags = soup.findAll("li")
    list_tag = soup.find(id = "mw-pages")
    secondl_tag = soup.find(id = "mw-pages")
    thirdl_tag = soup.find(id = "mw-pages")
    end = False
    castels = []

    for tag in tags:
        if(tag.text == "Acorn Hall"):
            list_tag = tag
        if(tag.text == "Greenfield"):
            secondl_tag = tag
        if(tag.text == "Pyke"):
            thirdl_tag = tag
            

    p_tag = list_tag.parent

    while True:
        if isinstance (p_tag, bs4.element.Tag):
            if (p_tag.name == "ul"):
                for child in p_tag.children:
                    if isinstance(child, bs4.element.Tag):
                        if(child.name == "li"):
                            castels.append(child.text)
                            if (child.text == "Yronwood"):
                                end = True
                                break

        
        if(castels[-1] == "Grassfield Keep"):
            p_tag = secondl_tag.parent

        elif(castels[-1] == "Poddingfield"):
            p_tag = thirdl_tag.parent

        elif(castels[-1] == "Yronwood"):
            break
        
        else:
            p_tag = p_tag.next_sibling
            
    return castels

def fetchData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find('p')

    data = tag.text
    return data

def compareWord(castels, titleArray):
    matchFound = False
    
    for castel in castels:
        castelArray = castel.split()
        for castelElem in castelArray:
            for word in titleArray:
                if castelElem.lower() == word.lower():
                    matchFound = True
                    break
                else:
                    matchFound = False
                    
        if(matchFound == True):
            return castel
                    

def runGotCastelBot(reddit):
    print('getting 30 submissions')
    castels = getCastelList()

    for submission in reddit.subreddit("test").new(limit = 30):
        title = submission.title
        titleArray = getTitleArray(title)
        castel = compareWord(castels, titleArray)
        file_obj_r = open(path, "r")
        
        if(castel and submission.id not in file_obj_r.read().splitlines()):
            url = "https://awoiaf.westeros.org/index.php/" + castel.replace(" ", "_")
            background = fetchData(url)
            submission.reply(header+background+footer)
            
            file_obj_r.close()

            file_obj_w = open(path, 'a+')
            file_obj_w.write(submission.id + '\n')
            file_obj_w.close()
    
    print("Waiting 60 seconds...\n")
    time.sleep(60)
    

def main():
    reddit = authenticate()
    runGotCastelBot(reddit)


if __name__ == '__main__':
    main()










