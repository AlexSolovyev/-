import re
import urllib.request
import json

articles = open('lj_articles.txt', 'r')
for article in articles:
    response = urllib.request.urlopen(article)
    text = response.read().decode("utf-8")
    users = re.findall('"username":"([A-Za-z0-9_]*)","user_alias"', text)
    ids = re.findall('"dtalkid":([A-Za-z0-9_]*)', text)
    commentators = dict()
    i = 0
    for elem in ids:
        commentators[elem] = users[i]
        i += 1
    
    parents_id = re.findall('"parent":([0-9_]*)', text)
    parents = list()
    for elem in parents_id:
        if (commentators.get(elem)):
            parents.append(commentators.get(elem))
        else:
            parents.append('root')
    information = dict()
    i = 0
    for elem in ids:
        information[elem] = (parents[i], "suit", users[i])
        i += 1
    links = list()
    for elem in information:
        if information[elem][0] != 'root':
            links.append({"source" : information[elem][2], "target" : information[elem][0], "type": '0'})
    for elem in links:
        print(elem,",")
    print('\n')

articles.close()
