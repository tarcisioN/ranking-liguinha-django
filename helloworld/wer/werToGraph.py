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


    def run(self, pivot = None):

        score_factor = 3
        score_factor2 = 0

        score_utils = Score(score_factor, score_factor2)

        werReportGraph = Graph()
        personIdName = {}
        total_pauper_events = {}
        total_standard_events = {}

        for werReportJsonData in self.docs:

            participation = werReportJsonData['event']['participation']
            event_format = werReportJsonData['event']['@format']
            for person in participation['person']:
                person_id = person['@id']
                personIdName[person_id] = person['@first'] + ' ' + person['@last']
				
                if person_id not in total_pauper_events:
                    total_pauper_events[person_id] = 0
					
                if person_id not in total_standard_events:
                    total_standard_events[person_id] = 0
				
                if event_format == 'CASL':
                    total_pauper_events[person_id] = total_pauper_events[person_id] + 1
                
                if event_format == 'STANDARD':
                    total_standard_events[person_id] = total_standard_events[person_id] + 1

            matches = werReportJsonData['event']['matches']

            for round in matches['round']:
                for match in round['match']:
                    if '@opponent' in match:
                        if match['@win'] > match['@loss']:
                            werReportGraph.add_directed_edge(match['@person'], match['@opponent'], 1)

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

        simulated_plus_one_score_dict = dict()
        total_wins = dict()

        for v in werReportGraph:

            v_total_score = 0

            #for w in v.get_connections():
            for w in werReportGraph:

                if w == v:
                    continue

                v_simple_score = score_to_concede[w.get_id()]

                vw_score = 0

                if v.get_id() not in total_wins:
                    total_wins[v.get_id()] = 0
                
                if w in v.adjacent: # sempre verdade?

                    total_wins[v.get_id()] += v.get_weight(w)

                    if v in w.adjacent:
                        vw_score = v.get_weight(w) - w.get_weight(v)
                    else:
                        vw_score = v.get_weight(w)

                #soh para simulacao
                if v in w.adjacent:
                    vw_score_simulacao = 0 - w.get_weight(v)
                    simulated_plus_one_score = vw_score_simulacao + 1
                else:
                    simulated_plus_one_score = vw_score + 1

                if vw_score < 1:
                    vw_score = 0

                this_event_score = v_simple_score * score_utils.score(vw_score)
                v_total_score += this_event_score

                #inicio simulacao de vitoria

                if v.get_id() not in simulated_plus_one_score_dict:
                    simulated_plus_one_score_dict[v.get_id()] = dict()

                if simulated_plus_one_score < 1:
                    #simulated_plus_one_score = 0
                    simulated_plus_one_score_dict[v.get_id()][w.get_id()] = simulated_plus_one_score
                    continue

                simulated_score = v_simple_score * score_utils.score(simulated_plus_one_score)
                simulated_plus_one_score_dict[v.get_id()][w.get_id()] = simulated_score - this_event_score
                # fim simulacao de vitoria

            total_score[v.get_id()] = v_total_score

        def sort_pontos_pontos_derrota(json):
            try:
                pontos = operator.itemgetter(1)(json)
                pontos_derrota = score_to_concede[operator.itemgetter(0)(json)]
                wins = total_wins[operator.itemgetter(0)(json)]

                result = (float(pontos), float(pontos_derrota), int(wins))
                return result
            except KeyError:
                return 0

        list = sorted_x = sorted(total_score.items(), key=sort_pontos_pontos_derrota, reverse=True)


        jsonList = []

        for p, i in enumerate(list):
            jsonC = {}
            jsonC['position'] = p + 1
            jsonC['pontos'] = "{0:.2f}".format(i[1])
            jsonC['totalVitorias'] = total_wins[i[0]]
            jsonC['totalPauperEvents'] = total_pauper_events[i[0]]
            jsonC['totalStandardEvents'] = total_standard_events[i[0]]

            if pivot:
                if pivot == i[0]:
                    jsonC['pontosDerrota'] = '0'
                else:
                    jsonC['pontosDerrota'] = "{0:.2f}".format(simulated_plus_one_score_dict[pivot][i[0]])
            else:
                jsonC['pontosDerrota'] = str(score_to_concede[i[0]])

            jsonC['nome'] = personIdName[i[0]]
            jsonC['id'] = i[0]

            jsonList.append(jsonC)

        jsonR = {}
        jsonR['records'] = len(list)
        jsonR['rows'] = jsonList

        return json.dumps(jsonR, ensure_ascii=False)



if __name__ == '__main__':

    files = glob.glob('reports/*.wer')

    docs = []

    for file in files:
        doc_data = open(file, 'rb')
        werReportDict = xmltodict.parse(doc_data)
        werReportJsonString = json.dumps(werReportDict)
        werReportJsonData = json.loads(werReportJsonString)

        docs.append(werReportJsonData)

        doc_data.close()

    wtg = WerToGraph(docs)

    r = wtg.run('2248758')
    print(json.loads(r)['rows'][5])
