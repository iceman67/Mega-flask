##
#
# This entire file is simply a set of examples. The most basic is to
# simply create a custom server by inheriting tserver.ThreadedServer
# as shown below in MyServer.
#
import jsocket
import logging
import DS1820

logger = logging.getLogger("localhost")

##
#       This is an example factory thread, which the server factory will
#               instantiate for each new connection.
#
class Networkerror(RuntimeError):
   def __init__(self, arg):
      self.args = arg

def error():
    print ("error")
    raise Networkerror('oops!')


class MyFactoryThread(jsocket.ServerFactoryThread):
    def __init__(self):
        super(MyFactoryThread, self).__init__()
        self.timeout = 2.0

    ##
    #  virtual method - Implementer must define protocol
    def _process_message(self, obj):
        print ("received a request")
        if obj != '':
            if obj['MEGA'] == "temp":
                temperature_dev = DS1820()
                print(temperature_dev.get_temp_list())
                #self.send_obj({"TEMP":  temperature_dev.get_temp_list()})
                self.send_obj({"TEMP":  1})
                logger.info("new connection.")
            else:
                val = obj['message']
                if val == "exit":
                    error()
                else:
                   print (type(val))
                   self.send_obj({"reply": val["t1"]})

                logger.info(obj)


def startServer():
    #   MyFactoryThread 실행
    server = jsocket.ServerFactory(MyFactoryThread)
    server.timeout = 2.0
    server.start()
    
    # take your time
    time.sleep(4)
    try:
        raise Networkerror("oops!")
    except Networkerror:
       print ("second error occurred")
       server.stop()
       server.join()



if __name__ == "__main__":
    import time
    import jsocket
    import threading

    t = threading.Timer(1.0, startServer)
    t.start()

    time.sleep(5)

    logger.debug("starting JsonClient")
    cPids = []
    for j in range(10):
        client = jsocket.JsonClient()
        cPids.append(client)
        client.connect()
        print("connected ")
        client.send_obj({"MEGA": "temp"})
        #client.send_obj({"message": {"t1": j}})
        obj = client.read_obj()
        print("received", obj)
        client.send_obj({"message": "exit"})

    time.sleep(2)

    for c in cPids:
        c.close()
