__author__ = '1ka'

import os
import sys
import time
import json
import epics
import queue
import threading
import zerorpc




class PV(object):
    def __init__(self,pv_json,callback):
        self.name = pv_json["Name"]
        self.pvname = pv_json["Pv"]
        self.pv = epics.pv.PV(
            self.pvname,
            callback = callback,
            auto_monitor = epics.dbr.DBE_VALUE
        )
        self.datatype = "int"
        if hasattr(pv_json,"Datatype"):
            self.datatype = pv_json["Datatype"]
    """def subscription(self):
        def sendData(value):#pvname,char_value,value,status,ftype,chid,host,type,cb_info,typefull,nelm,lower_ctrl_limit,count,upper_ctrl_limit,upper_warning_limit,lower_warning_limit,access,lower_alarm_limit,upper_alarm_limit,lower_disp_limit,  upper_disp_limit,write_access,read_access,enum_strs,units,precision,nanoseconds,posixseconds,severity,timestamp):
            #print(value)
            self.callback(self.pvname,value)
        try:
            None
            #camonitor(str(self.pvname),sendData)
        except Exception as e:
            print(self.pvname+" "+str(e))
    def sendData(self, *args, **kwargs):
        value = str(kwargs["value"])
        print(self.pvname+" "+value)
        self.callback(self.pvname,value)"""


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
        print(pvname+str(value))
        publisher.testing(pvname,value)
    except Exception as e:
        print(e)

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


