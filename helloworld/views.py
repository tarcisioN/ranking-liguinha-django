# -*- coding: utf-8 -*-
import json

import xmltodict
from django.http import HttpResponse
from minio import Minio

from helloworld.wer.werToGraph import WerToGraph

client = Minio('35.188.18.243:9000',
               access_key='XHWHNU67FSLL3XVVI3JZ',
               secret_key='zuf+k016QPWOqMrFgb5TjzupjgNGYqb4Vnq2OTVmoMvk')

def index(request):

    wtg = WerToGraph(get_reports())

    ranking = wtg.run()

    print(ranking)

    return HttpResponse(ranking)


def get_reports():

    objects = client.list_objects('liguinha')

    reports = []

    for object in objects:

        if '.wer' in object.object_name:
            report = client.get_object('liguinha', object.object_name)

            file_data = report.read()

            werReportDict = xmltodict.parse(file_data)
            werReportJsonString = json.dumps(werReportDict, ensure_ascii=False).encode('utf8')
            werReportJsonData = json.loads(werReportJsonString)

            reports.append(werReportJsonData)

    return reports
