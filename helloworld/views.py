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

client = Minio('www.bolsadoinfinito.com.br:9000',
               access_key='AWWT0FQLOGA327RAVNMG',
               secret_key='9h5eWe5NwnbQkyumAXDtUA9Wfo36HueocsRhmybA', http_client=http)


def index(request, edition='current', pivot=None):

    wtg = WerToGraph(get_reports(edition))

    ranking = wtg.run(pivot)

    return HttpResponse(ranking)


def get_reports(edition):

    objects = client.list_objects(edition)

    reports = []

    for object in objects:

        if '.wer' in object.object_name:
            report = client.get_object(edition, object.object_name)

            file_data = report.read()

            werReportDict = xmltodict.parse(file_data)
            werReportJsonString = json.dumps(werReportDict)
            werReportJsonData = json.loads(werReportJsonString)

            reports.append(werReportJsonData)

    return reports
