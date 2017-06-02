import re
from bs4 import BeautifulSoup
#from selenium import webdriver
import urllib2

def loginRequired(address):

    #Case 1: For example, Facebook
    searched_word = 'login'
    source = urllib2.urlopen('http://'+address).read()
    soup = BeautifulSoup(source,'html.parser')
    result = soup.body.find_all(text=re.compile('.*{0}.*'.format(searched_word)),recursive=True)
    #print'Found the word "{0}" {1} times\n'.format(searched_word,len(result))
    #print result
    #Case 2: For example, 128.46.66.246
    form = soup.find('body')
    input = form.find_all('input',{"name":"login"})

    #case 3: For example, 128.46.75.31:88
    body = soup.find('body')
    div = body.find_all('div', {"id": "login"})

    #Case 4: For example, 128.46.117.111
    content = soup.find_all('meta', {"content": "1;url=html/login.html"})

    #Case 1 check
    if result:
        #print("Case 1 returned 1")
        return 1

    #Case 2 check
    if input:
        #print("Login was found in source")
        #print("Case 2 returned 1")
        return 1

    #Case 3 check
    if div:
        #print("Login was found in source")
        #print("Case 3 returned 1")
        return 1

    #Case 4 check
    if content:
         #print("Login was found in source")
         #print("Case 4 returned 1")
         return 1

    return 0
'''
if __name__ == '__main__':
    #loginRequired('128.46.66.246')
    loginRequired('128.46.117.111')
    #loginRequired('128.46.75.31:88')
    #loginRequired('www.facebook.com')
'''