"""====================================================================================================


File                     :  GUIDatabase.py

date                     :  4/3/2025

Author                   :  Benedict Ward

Description              :  this will interface from pgadmin allowing for GUI to be made with customtkinter

History                  :  4/3/2025 v1.0 - added code given in the lecture
                                            added basic GUI (tabs(frames),buttons)

===================================================================================================="""

# these require pip
# to install these run the command "pip install -r /path/to/requirements.txt"
import psycopg2
import customtkinter as CTk
import json

with open("../secret.json", "r") as f:
    secretData = json.load(f) 

conn = psycopg2.connect(user = secretData["user"],
                        password = secretData["password"],
                        host = secretData["host"],
                        port = secretData["port"],
                        database = secretData["database"]
                        )

# given example of the psycopg2 api:
# cur = conn.cursor()
# cur.execute('SET search_path TO Demo,public;')
# cur.execute('SELECT * FROM emp')
# rows = cur.fetchall()
#
# for row in rows:
#     print(row[0], row[1], row[3])
# conn.close()

class App(CTk.CTk):
    def __init__(self, database_connection:psycopg2.extensions.connection):
        super().__init__()
        self.__DbConnection = database_connection
        self.cursor = self.__DbConnection.cursor()

        self.geometry("400x400")
        self.__tableNameTitles:dict = { "exam": ["excode","extitle","exdate","extime"],
                                        "student": ["sno","sname","semail"],
                                        "entry": ["eno","excode","sno","egrade"],
                                        "cancel": ["eno","excode","sno","cdate","curser"]
                                      }

        self.__tabController = CTk.CTkTabview(self)
        self.__tabController.pack(fill="both", expand=True, padx=10, pady=10)
        self.frames = []

        #following CRUD, Create, Retrieve, update, Delete
        self.frames.append(self.__tabController.add("Selecting"))
        self.frames.append(self.__tabController.add("Inserting"))
        self.frames.append(self.__tabController.add("Update"))
        self.frames.append(self.__tabController.add("Delete"))

        # the default GUI on each of the tabs
        self.initiliseFrame1()
        self.initiliseFrame2()
        self.initiliseFrame3()
        self.initiliseFrame4()


    def initiliseFrame1(self):
        tableName = self.__tableNameTitles.keys()
        tableTitles = self.__tableNameTitles["exam"]
        button = CTk.CTkButton(self.frames[0], text="fetch exam", command=lambda:self.displayDateFromTable("exam"))
        button.grid(column=0, row= 0,padx=20, pady=20)
        button = CTk.CTkButton(self.frames[0], text="fetch student", command=lambda:self.displayDateFromTable("student"))
        button.grid(column=0, row= 1,padx=20, pady=20)
        button = CTk.CTkButton(self.frames[0], text="fetch entry", command=lambda:self.displayDateFromTable("entry"))
        button.grid(column=0, row= 2,padx=20, pady=20)
        button = CTk.CTkButton(self.frames[0], text="fetch cancel", command=lambda:self.displayDateFromTable("cancel"))
        button.grid(column=0, row= 3,padx=20, pady=20)

    def initiliseFrame2(self):
        pass
    def initiliseFrame3(self):
        pass
    def initiliseFrame4(self):
        pass
    
    def displayDateFromTable(self, tableName:str )-> None:
        allColumns = self.__tableNameTitles[tableName]

        self.cursor.execute('SET search_path TO Demo,public;')
        self.cursor.execute('SELECT * FROM emp')
        rows = self.cursor.fetchall()

        for row in rows:
            print(row[0], row[1], row[3])

    def button_callback(self):
        print("button clicked")

try:
    app = App(conn)
    app.mainloop()
except Exception as e:
    print("[ERROR]" + str(e))
finally:
    if conn:
        conn.close()
