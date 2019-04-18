__author__ = '1ka'

import os
import sys
import time
import json
import numpy
import epics
import queue
import threading
import zerorpc


class PV(object):
    def __init__(self,pv_json,callback):
        self.name = pv_json["Name"]
        self.pvname = pv_json["Pv"]
        pv_queue.put(self.pvname,epics.caget(self.pvname))
        self.pv = epics.pv.PV(
            self.pvname,
            callback = callback,
            auto_monitor = epics.dbr.DBE_VALUE
        )
        self.datatype = "int"
        if hasattr(pv_json,"Datatype"):
            self.datatype = pv_json["Datatype"]


def subscribePvObjects(list):
    for pvobj in list:
        pvobj.subscription()


def createPvObjects(list,publisher):
    pv_objects = []
    for pv in list:
        pvobj = PV(pv,publisher)
        pv_objects.append(pvobj)
    return pv_objects


def shotFromList(list):
    shot = []
    for item in list:
        if "Name" in item:
            shot.append({"Name":item["Name"],"Value":None})
    return shot


def openConfigFile(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

def putPvQueue(*args, **kwargs):
    pv_queue.put([str(kwargs["pvname"]),kwargs["value"]])

def sendData(pvname,value):
    try:
        if(type(value) is numpy.ndarray):
            value = value.tolist()
        publisher.__call__(u'testing', pvname,value)
    except Exception as e:
        print("myerr",e)

def runserver():
    #server = zerorpc.Server(ServerRPC())
    server = zerorpc.Publisher()
    server.bind("tcp://0.0.0.0:4243")
    return server
    #client = zerorpc.Client()
    #client.connect("tcp://127.0.0.1:4242")


publisher = runserver()

script_dir = os.path.dirname(__file__)
pv_list = openConfigFile(os.path.join(script_dir,"pv_list.json"))
pv_queue = queue.Queue()
pv_objects = createPvObjects(pv_list,putPvQueue)

while True:
    item = pv_queue.get()
    sendData(item[0],item[1])


#app = QtCore.QCoreApplication(sys.argv)

#thread1 = threading.Thread(target=testsubscriber)
#thread1.start()

#cothread.WaitForQuit()

#sys.exit(app.exec_())


