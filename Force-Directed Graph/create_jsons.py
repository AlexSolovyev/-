#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import urllib.request
from lxml import html
import json
articles =  open('lj_articles.txt', 'r')
index = 1
for article in articles:
    response = urllib.request.urlopen(article)
    text = response.read().decode("utf-8")
    nick_names = re.findall('"username":"([A-Za-z0-9_]*)","user_alias"', text)
    ids = re.findall('"dtalkid":([A-Za-z0-9_]*)', text)
    parent_ids = re.findall('"parent":([0-9_]*)', text)
    groups = re.findall('"level":([0-9]*),"dname"', text)
    i = 0
    all_comments = dict()
    for elem in ids:
        all_comments[elem] = (nick_names[i], groups[i], parent_ids[i])
        i += 1
    for elem in all_comments:
        print (elem,' : ', all_comments[elem])


    i = 0
    nodes = list()
    links = list()
    nodes.append({"id" : "0", "rating" : 20, "name" : "Article"})
    for elem in all_comments:
        x = all_comments[elem][1]
        if x[0] == "–":
            x ="0"
        nodes.append({"id" : elem, "rating" : int(x), "name" : all_comments[elem][0]})
        links.append({"target" : elem, "source"  : all_comments[elem][2]})

    graph = {"nodes" : nodes, "links" : links}
    path = 'data' + str(index) + '.json'
    with open(path, 'w') as output_file:
        json.dump(graph, output_file, sort_keys=False)
    index += 1

articles.close()

