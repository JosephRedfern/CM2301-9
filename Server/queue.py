import MySQLdb, datetime
#hghghg
class Database(object):

    host = '127.0.0.1'
    db = 'learn'
    user = 'root'
    psswd = ''

    con = None
    cur = None

    def __init__(self):
        self.con = MySQLdb.connect(self.host, self.user,
                                   self.psswd, self.db)
        self.cur = self.con.cursor()

    def close(self):
        if self.cur != None:
            self.cur.close()
        if self.con != None:
            self.con.close()
            

class QueueManager(list):

    __db = None
    
    def __init__(self):
        "QueueManager"
        
    def get_pending_queue(self):
        """Fetches all uncomplete queue items from db"""
        self.__db = Database()
        self.__db.cur.execute("SELECT * FROM queue WHERE waiting=True AND progress<100")
        rs = self.__db.cur.fetchall()
        self.__set_items_from_db(rs)
        self.__db.close()

    def __set_items_from_db(self, result_set):
        for row in result_set:
            qi = QueueItem()
            qi.uuid = row[0]
            qi.submission_time = row[1]
            qi.waiting = row[2]
            qi.progress = row[3]
            self.append(qi)


class QueueItem(object):
    uuid = None
    job_type = None
    submission_time = None
    waiting = False
    progress = 0.0
    completion_time = None

    __db = None

    def __init__(self):
        print " test"

    def save(self):
        """Saves the queue item back to the database"""
        self.__db = Database()        
        self.__db.cur.execute("UPDATE queue SET "
                              + "waiting=" + str(self.waiting)
                              + ", progress=" + str(self.progress)
 #                             + ", completion_time=" + str(self.completion_time)
                              + " WHERE " + "uuid" + "='" + self.uuid + "'")
        self.__db.close()
        self.__db == None


        
        
        
