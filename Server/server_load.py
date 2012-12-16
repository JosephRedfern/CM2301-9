import threading
import psutil
import datetime
#adding some randomdfshg
class ServerLoad(object):
    server_load = []
    cpu_usage = []
    mem_usage = 0.0
    last_update = 0.0
    updating = False

    def __init__(self):
        self.start_updating()

    def persist_load(self):
        """Saves the current server load to the database"""
        #Use the database class to update it

    def update_load(self):
        """Updates the historical load list, capped to 60 and is a blocking method"""
        if (len(self.cpu_usage) >= 60):
            self.cpu_usage.pop(60-1)
        self.cpu_usage.insert(0, psutil.cpu_percent(interval=1))
        self.last_update = datetime.datetime.now()

    def calculate_load(self, interval=10):
        """Returns the actual useful load!"""
        if (len(self.cpu_usage) < interval):
            raise Exception("Not long enough fuck tard")
            return
        total = 0
        for i in range(0, interval):
            total += self.cpu_usage[i]
        return (total/interval) / float(psutil.virtual_memory().available)

    def start_updating(self):
        """Stards the object logging load"""
        self.updating = True
        t = threading.Thread(target=self.__update)
        t.start()

    def stop_updating(self):
        """Stops the object logging load"""
        self.updating = False

    def __update(self):
        while self.updating:
            self.update_load()
        

    
