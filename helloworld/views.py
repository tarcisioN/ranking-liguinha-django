#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import xmltodict, json

from helloworld.wer.graphUtil import Graph
from helloworld.wer.scoreUtils import Score
import glob


class WerToGraph:


    def __init__(self, docs):
        self.docs = docs


    def run(self):

        score_factor = 3
        score_factor2 = 0

        score_utils = Score(score_factor, score_factor2)

        werReportGraph = Graph()
        personIdName = {}

        # self.files = glob.glob('helloworld/reports/*.wer')

        for werReportJsonData in self.docs:

            # doc = open(f, 'rb')
            # werReportDict = xmltodict.parse(doc)
            # werReportJsonString = json.dumps(werReportDict, ensure_ascii=False).encode('utf8')
            # werReportJsonData = json.loads(werReportJsonString)

            participation = werReportJsonData['event']['participation']

            for person in participation['person']:
                personIdName[person['@id']] = person['@first'] + ' ' + person['@last']

            matches = werReportJsonData['event']['matches']

            for round in matches['round']:
                for match in round['match']:
                    if '@opponent' in match:
                        if match['@win'] > match['@loss']:
                            werReportGraph.add_directed_edge(match['@person'], match['@opponent'], 1)

            # doc.close()

        score_to_concede = {}

        for v in werReportGraph:

            vn_scoreToConcede = 0

            for w in v.get_connections():

                vw_score = 0

                if w in v.adjacent:
                    if v in w.adjacent:
                        vw_score = v.get_weight(w) - w.get_weight(v)
                    else:
                        vw_score = v.get_weight(w)

                if vw_score < 1:
                    continue

                vn_scoreToConcede += vw_score

            score_to_concede[v.get_id()] = vn_scoreToConcede

        total_score = {}

        for v in werReportGraph:

            v_total_score = 0

            for w in v.get_connections():

                v_simple_score = score_to_concede[w.get_id()]

                vw_score = 0

                if w in v.adjacent:

                    if v in w.adjacent:
                        vw_score = v.get_weight(w) - w.get_weight(v)
                    else:
                        vw_score = v.get_weight(w)

                if vw_score < 1:
                    vw_score = 0

                v_total_score += v_simple_score * score_utils.score(vw_score)

            str_v_total_score = "{0:.2f}".format(v_total_score)
            #total_score[v.get_id()] = str_v_total_score
            total_score[v.get_id()] = v_total_score

        list = sorted_x = sorted(total_score.items(), key=operator.itemgetter(1), reverse=True)


        jsonList = []

        for i in list:
            jsonC = {}
            jsonC['pontos'] = str(i[1])
            jsonC['pontosDerrota'] = str(score_to_concede[i[0]])
            jsonC['nome'] = personIdName[i[0]]

            jsonList.append(jsonC)

        jsonR = {}
        jsonR['records'] = len(list)
        jsonR['rows'] = jsonList

        return json.dumps(jsonR, ensure_ascii=False).encode('utf8')

if __name__ == '__main__':

    docs = glob.glob('reports/*.wer')

    wtg = WerToGraph(docs)

    print(wtg.run())
