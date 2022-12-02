from mysql import connector
from pandas import DataFrame
from exception import SystemError
import os, sys

class app_config():
    def __init__(self):
        try:
            f = open('mysqldata.txt').read()
            read = f.split()
            self.mydb = connector.connect(
                        host = read[0],
                        user = read[1],
                        password = read[2],
                        port = int(read[3]),
                        database = read[4])
            print('MYSQL is connected successfully')
            self.path = os.path.join(os.getcwd(), "static",'BankFAQs.csv')
            self.upath = os.path.join(os.getcwd(), 'static', 'userdata.csv')
        except Exception as e:
            raise SystemError(e, sys)
    
    def convert_data_into_dataframe(self) -> DataFrame:
        try:
            self.cursor = self.mydb.cursor()
            self.cursor.execute('SELECT * FROM bankfaqs')
            data = self.cursor.fetchall()
            qlst = []
            alst = []
            clst = []
            for i in data:
                qlst.append(i[0])
                alst.append(i[1])
                clst.append(i[2])
            df = DataFrame(list(zip(qlst, alst, clst)), columns=['Question', 'Answer', 'Class'])
            df.to_csv(self.path)
            return df
        except Exception as e:
            raise SystemError(e, sys)
        

    def initialise_process(self):
        try:
            # appdata = self.mysql_connect()
            df = self.convert_data_into_dataframe()
            return df
        except Exception as e:
            raise SystemError(e, sys)







