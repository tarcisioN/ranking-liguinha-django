#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import xmltodict, json
from graphUtil import Graph
from scoreUtils import Score
import glob

score_factor = 3
score_factor2 = 0

score_utils = Score(score_factor, score_factor2)

docs = []

score = {}

for f in glob.glob('reportsXML/*.xml'):

    doc = open(f, 'rb')

    werReportDict = xmltodict.parse(doc)
    werReportJsonString = json.dumps(werReportDict, ensure_ascii=False).encode('utf8')
    werReportJsonData = json.loads(werReportJsonString)

    for team in werReportJsonData['Standings']['Team']:

        if team['@Name'] in score:
            score[team['@Name']] += int(team['@MatchPoints'])
        else:
            score[team['@Name']] = int(team['@MatchPoints'])

    doc.close()

list = sorted_x = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

for i in list:
    print(i[0] + ' -> ' + str(i[1]))