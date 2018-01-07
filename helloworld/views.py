# -*- coding: utf-8 -*-
import json

import urllib3
import xmltodict
from django.http import HttpResponse
from minio import Minio

from helloworld.wer.werToGraph import WerToGraph

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager(
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                        cert_reqs='CERT_NONE',
                        retries=urllib3.Retry(
                            total=5,
                            backoff_factor=0.2,
                            status_forcelist=[500, 502, 503, 504]
                        )
            )

client = Minio('35.188.18.243:9000',
               access_key='IMJ789JGQG6RTMPAORBZ',
               secret_key='j0Wi61KT/B6DOKFq1w8xwwAOARvE8fRWbXA63sDy', http_client=http)

def index(request):

    wtg = WerToGraph(get_reports())

    ranking = wtg.run()

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
