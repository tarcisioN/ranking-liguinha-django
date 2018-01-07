# -*- coding: utf-8 -*-
import json

import xmltodict
from django.http import HttpResponse
from minio import Minio

from helloworld.wer.werToGraph import WerToGraph

client = Minio('play.minio.io:9000',
               access_key='Q3AM3UQ867SPQQA43P2F',
               secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')

def index(request):

    wtg = WerToGraph(get_reports())

    ranking = wtg.run()

    print(ranking)

    return HttpResponse(ranking)


def get_reports():

    objects = client.list_objects('trcs')

    reports = []

    for object in objects:

        if '.wer' in object.object_name:
            report = client.get_object('trcs', object.object_name)

            file_data = report.read()

            werReportDict = xmltodict.parse(file_data)
            werReportJsonString = json.dumps(werReportDict, ensure_ascii=False).encode('utf8')
            werReportJsonData = json.loads(werReportJsonString)

            reports.append(werReportJsonData)

    return reports