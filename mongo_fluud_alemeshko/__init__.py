__author__ = 'nmarchenko'

from pymongo import MongoClient
import dateutil.parser
import copy
import sys
import argparse
import urllib
from gevent import monkey, spawn, sleep
from gevent.queue import JoinableQueue

monkey.patch_all()


def start_fluud():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='mongo host')
    parser.add_argument('port', help='mongo port')
    parser.add_argument('--login', help='mongo login')
    parser.add_argument('--password', help='mongo password')
    args = parser.parse_args()

    if args.login and args.password:
        login = urllib.quote_plus(args.login)
        password = urllib.quote_plus(args.password)
        uri = 'mongodb://{}:{}@{}:{}/'.format(login, password, args.host, args.port)
    else:
        uri = 'mongodb://{}:{}/'.format(args.host, args.port)

    client = MongoClient(uri)

    template = {
        "first_sample_timestamp": dateutil.parser.parse("2015-09-02T13:08:20.314Z"),
        "last_sample_timestamp":  dateutil.parser.parse("2015-09-02T13:08:20.314Z"),
        "metadata": {
            "typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event",
            "initiator": {
                "typeURI": "service/security/account/user",
                "host": {
                    "address": "192.168.0.2"
                },
                "id": "openstack:610e7d74-16af-4358-9b77-5275194fa6e4",
                "name": "8b07b49216d243d2b49561759bd104f4"
            },
            "target": {
                "typeURI": "service/security/account/user",
                "id": "openstack:fc43ddcf-d147-466c-adfe-d60bd2b773ba"
            },
            "observer": {
                "typeURI": "service/security",
                "id": "openstack:a256def4-0a36-472e-95e5-e456db4e0681"
            },
            "eventType": "activity",
            "eventTime": "2015-09-02T13:08:20.256770+0000",
            "host": "identity.node-1",
            "action": "authenticate",
            "outcome": "success",
            "id": "openstack:00244b9a-1a43-48a5-b75e-9d68dd647487",
            "event_type": "identity.authenticate"
        },
        "meter": [
            {
                "counter_name": "identity.authenticate.success",
                "counter_unit": "user",
                "counter_type": "delta"
            }
        ],
        "project_id": None,
        "source": "openstack",
        "user_id": "openstack:610e7d74-16af-4358-9b77-5275194fa6e4"
    }

    data = [copy.deepcopy(template) for _ in range(10000)]

    def progress():
        while True:
            print client.ceilometer.resource.count()
            sys.stdout.flush()
            sleep(2)

    spawn(progress)

    def worker():
        while True:
            q.get()
            try:
                client.ceilometer.resource.insert_many(copy.deepcopy(data), False)
            finally:
                q.task_done()

    q = JoinableQueue()
    for i in range(10):
        spawn(worker)

    for i in range(100):
        q.put(0)

    q.join()