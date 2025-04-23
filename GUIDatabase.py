"""====================================================================================================


File                     :  GUIDatabase.py

date                     :  4/3/2025

Author                   :  Benedict Ward

Description              :  this will interface from pgadmin allowing for GUI to be made with customtkinter

History                  :  4/3/2025 v1.0 - added code given in the lecture
                                            added basic GUI (tabs(frames),buttons)
                            
                            10/4/2025 v1.1 - added Selecting, Inserting, Updating, Tools tab fully working

                            20/4/2025 v2 - will redo alot of the frames here to better fit with the project
===================================================================================================="""
import psycopg2
import customtkinter as CTk
import tkinter as Tk  # only needed for labelFrames
import json


attempt_connection = True
if attempt_connection:
    with open("../secret.json", "r") as f:
        secretData = json.load(f)

    try:
        conn = psycopg2.connect(user=secretData["user"],
                                password=secretData["password"],
                                host=secretData["host"],
                                port=secretData["port"],
                                database=secretData["database"]
                                )
        #  the summative db is selected in the __init__
        print(f"successfully connected to the db named '{secretData["database"]}'!")
        secretData = {}

    except psycopg2.OperationalError as e:
        print("connection error, turn on the 'BIG-IP edge client' vpn.")
        print("running GUI but commands won't execute.")
#conn = None


class App:
    def __init__(self, database_connection: psycopg2.extensions.connection) -> None:
        """uses the connection to generate a database cursor and initialises the GUI"""
        self.CTK = CTk.CTk()
        self.__DbConnection = database_connection
        if self.__DbConnection is not None:
            print("connected!")
            self.__cursor = self.__DbConnection.cursor()
            self.__cursor.execute('SET search_path to summative,public;')

        #self.CTK.geometry("")  # if i dont set the geometry then it auto fits better then i can
        self.__title = "SQL summative project"

        self.CTK.title(self.__title)

        self.__tableNameTitles: dict = {"exam": ["excode", "extitle", "exlocation", "exdate", "extime"],
                                        "student": ["sno", "sname", "semail"],
                                        "entry": ["eno", "excode", "sno", "egrade"],
                                        "cancel": ["eno", "excode", "sno", "cdate", "curser"]
                                        }

        self.mostRecentQuery = ""

        self.init_buttons()

        self.CTK.mainloop()

    def __run_sql_command(self, query: str):
        self.mostRecentQuery = query
        print("running command: " + query)
        if self.__DbConnection is not None:

            self.__cursor.execute(query)
            print("fetching results:")
            self.display_results()

    def display_results(self):
        print("results: ", self.__cursor.fetchall())

    def custom_func(self):
        print("custom function!")


    #    A B C
    #    0 0 0
    #    0 0 0
    def task_A(self):
        """A. Insert a new student member of the society."""

        task_A_tab = CTk.CTk()
        task_A_tab.title(self.__title + ": Task A - adding student")


        label = CTk.CTkLabel(task_A_tab, text="what is the students's name:")
        label.grid(column=0, row=0, padx=20, pady=20)

        nameEntryTextVar = CTk.StringVar(task_A_tab)
        nametextEntry = CTk.CTkEntry(task_A_tab,width=120,height=40, textvariable=nameEntryTextVar)
        nametextEntry.grid(column=1, row=0, padx=20, pady=20)


        label = CTk.CTkLabel(task_A_tab, text="what is the students's email:")
        label.grid(column=0, row=1, padx=20, pady=20)

        emailEntryTextVar = CTk.StringVar(task_A_tab)
        emailtextEntry = CTk.CTkEntry(task_A_tab,width=120,height=40, textvariable=emailEntryTextVar)
        emailtextEntry.grid(column=1, row=1, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_A_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"INSERT INTO student(sname,semail) VALUES ('{nametextEntry.get()}','{emailtextEntry.get()}');"),
            )
        )
        updateButton.grid(column=0, row=2, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_A_tab)
        totallabelA = CTk.CTkLabel(task_A_tab, textvariable=totalTextVar)
        totallabelA.grid(column=1, row=2, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_A_tab, text="submit command", command=
            lambda: (
                self.__run_sql_command(totalTextVar.get())
            )
        )
        updateButton.grid(column=0, row=3, columnspan=2, padx=20, pady=20)

        totalTextVar.set(f"INSERT INTO student(sname,semail) VALUES ('{nametextEntry.get()}','{emailtextEntry.get()}');"),
        task_A_tab.mainloop()

    def task_B(self):
        """B. Insert a new examination for the coming year."""
        task_B_tab = CTk.CTk()
        task_B_tab.title(self.__title + ": Task B - adding exam")

        label = CTk.CTkLabel(task_B_tab, text="what is the exams excode:")
        label.grid(column=0, row=0, padx=20, pady=20)

        excodeEntryTextVar = CTk.StringVar(task_B_tab)
        excodeTextEntry = CTk.CTkEntry(task_B_tab,width=120,height=40, textvariable=excodeEntryTextVar)
        excodeTextEntry.grid(column=1, row=0, padx=20, pady=20)


        label = CTk.CTkLabel(task_B_tab, text="what is the exams extitle:")
        label.grid(column=0, row=1, padx=20, pady=20)

        extitleEntryTextVar = CTk.StringVar(task_B_tab)
        extitleTextEntry = CTk.CTkEntry(task_B_tab,width=120,height=40, textvariable=extitleEntryTextVar)
        extitleTextEntry.grid(column=1, row=1, padx=20, pady=20)


        label = CTk.CTkLabel(task_B_tab, text="what is the exams exlocation:")
        label.grid(column=0, row=2, padx=20, pady=20)

        exlocationEntryTextVar = CTk.StringVar(task_B_tab)
        exlocationTextEntry = CTk.CTkEntry(task_B_tab,width=120,height=40, textvariable=exlocationEntryTextVar)
        exlocationTextEntry.grid(column=1, row=2, padx=20, pady=20)


        label = CTk.CTkLabel(task_B_tab, text="what is the exams exdate:")
        label.grid(column=0, row=3, padx=20, pady=20)

        exdateEntryTextVar = CTk.StringVar(task_B_tab)
        exdateTextEntry = CTk.CTkEntry(task_B_tab,width=120,height=40, textvariable=exdateEntryTextVar)
        exdateTextEntry.grid(column=1, row=3, padx=20, pady=20)


        label = CTk.CTkLabel(task_B_tab, text="what is the exams extime:")
        label.grid(column=0, row=4, padx=20, pady=20)

        extimeEntryTextVar = CTk.StringVar(task_B_tab)
        extimeTextEntry = CTk.CTkEntry(task_B_tab,width=120,height=40, textvariable=extimeEntryTextVar)
        extimeTextEntry.grid(column=1, row=4, padx=20, pady=20)


        updateButton = CTk.CTkButton(task_B_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"INSERT INTO exam(excode,extitle,exlocation,exdate,extime) VALUES ('{excodeTextEntry.get()}','{extitleTextEntry.get()}','{exlocationTextEntry.get()}','{exdateTextEntry.get()}','{extimeTextEntry.get()}');")
            )
        )
        updateButton.grid(column=0, row=5, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_B_tab)
        totallabelB = CTk.CTkLabel(task_B_tab, textvariable=totalTextVar)
        totallabelB.grid(column=1, row=5, padx=20, pady=20)

        submitButton = CTk.CTkButton(task_B_tab, text="submit command", command=
            lambda: (
                self.__run_sql_command(totalTextVar.get())
            )
        )
        submitButton.grid(column=0, row=6, columnspan=2, padx=20, pady=20)

        # making this be displayed with this text sowhen it appears its not a shock to the user
        totalTextVar.set(f"INSERT INTO exam(excode,extitle,exlocation,exdate,extime) VALUES ('{excodeTextEntry.get()}','{extitleTextEntry.get()}','{exlocationTextEntry.get()}','{exdateTextEntry.get()}','{extimeTextEntry.get()}');")
        task_B_tab.mainloop()

    def task_C(self):
        """C. Delete a student. This happens if a student withdraws from the society. All the
examination entries for the student must be cancelled. The cancelled entries must
retain their student reference number even though there is no longer a matching row
in the student table."""
        task_C_tab = CTk.CTk()
        task_C_tab.title(self.__title + ": Task B - adding exam")

        label = CTk.CTkLabel(task_C_tab, text="what is the students sno:")
        label.grid(column=0, row=0, padx=20, pady=20)

        snoEntryTextVar = CTk.StringVar(task_C_tab)
        snoTextEntry = CTk.CTkEntry(task_C_tab,width=120,height=40, textvariable=snoEntryTextVar)
        snoTextEntry.grid(column=1, row=0, padx=20, pady=20)

        label = CTk.CTkLabel(task_C_tab, text="what is the exams excode:")
        label.grid(column=0, row=1, padx=20, pady=20)

        excodeEntryTextVar = CTk.StringVar(task_C_tab)
        excodeTextEntry = CTk.CTkEntry(task_C_tab,width=120,height=40, textvariable=excodeEntryTextVar)
        excodeTextEntry.grid(column=1, row=1, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_C_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"SELECT student_withdraw({snoTextEntry.get()},'{excodeTextEntry.get()}');")
            )
        )
        updateButton.grid(column=0, row=2, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_C_tab)
        totallabelB = CTk.CTkLabel(task_C_tab, textvariable=totalTextVar)
        totallabelB.grid(column=1, row=2, padx=20, pady=20)

        submitButton = CTk.CTkButton(task_C_tab, text="submit command", command=
            lambda: (
                self.__run_sql_command(totalTextVar.get())
            )
        )
        submitButton.grid(column=0, row=3, columnspan=2, padx=20, pady=20)

        # making this be displayed with this text sowhen it appears its not a shock to the user
        totalTextVar.set(f"SELECT student_withdraw(,'');")
        task_C_tab.mainloop()

        #SELECT student_withdraw(1,'db01')


    #    0 0 0
    #    D E F
    #    0 0 0
    def task_D(self):
        """D. Delete an examination. Examinations that have no entries may be deleted from
the database. The examination must not have any current (not cancelled) entries."""
        task_D_tab = CTk.CTk()
        task_D_tab.title(self.__title + ": Task B - adding exam")

        label = CTk.CTkLabel(task_D_tab, text="what is the exams excode:")
        label.grid(column=0, row=0, padx=20, pady=20)

        excodeEntryTextVar = CTk.StringVar(task_D_tab)
        excodeTextEntry = CTk.CTkEntry(task_D_tab,width=120,height=40, textvariable=excodeEntryTextVar)
        excodeTextEntry.grid(column=1, row=0, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_D_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"SELECT delete_exam('{excodeTextEntry.get()}');")
            )
        )
        updateButton.grid(column=0, row=1, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_D_tab)
        totallabelB = CTk.CTkLabel(task_D_tab, textvariable=totalTextVar)
        totallabelB.grid(column=1, row=1, padx=20, pady=20)

        submitButton = CTk.CTkButton(task_D_tab, text="submit command", command=
            lambda: (
                self.__run_sql_command(totalTextVar.get())
            )
        )
        submitButton.grid(column=0, row=3, columnspan=2, padx=20, pady=20)

        # making this be displayed with this text sowhen it appears its not a shock to the user
        totalTextVar.set(f"SELECT delete_exam('');")
        task_D_tab.mainloop()

    def task_E(self):
        """E. Insert an examination entry. A student can only enter a specific examination once
in a year. The student cannot take more than one examination on the same day.

        so i would guess this would be the user selecting a student then saying what exam they have when?
        cant use a drop down menu for selecting a student"""

        #INSERT INTO entry (eno,excode,sno,egrade) VALUES (int,char,int,decimal)
        task_E_tab = CTk.CTk()
        task_E_tab.title(self.__title + ": Task E - add examination")


        # -0-
        # X X
        # 0 0
        # 0 0
        # 0 0
        # 0 0
        label = CTk.CTkLabel(task_E_tab, text="what is the exam's excode:")
        label.grid(column=0, row=1, padx=20, pady=20)

        excodeentryTextVar = CTk.StringVar(task_E_tab)
        excodetextEntry = CTk.CTkEntry(task_E_tab,width=120,height=40, textvariable=excodeentryTextVar)
        excodetextEntry.grid(column=1, row=1, padx=20, pady=20)

        # -0-
        # 0 0
        # X X
        # 0 0
        # 0 0
        # 0 0
        label = CTk.CTkLabel(task_E_tab, text="what is the student's sno:")
        label.grid(column=0, row=2, padx=20, pady=20)

        snoTextVar = CTk.StringVar(task_E_tab)
        snotextEntry = CTk.CTkEntry(task_E_tab,width=120,height=40, textvariable=snoTextVar)
        snotextEntry.grid(column=1, row=2, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_E_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"INSERT INTO entry (excode,sno) VALUES ('{excodetextEntry.get()}','{snotextEntry.get()}');")
            )
        )
        updateButton.grid(column=0, row=4, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_E_tab)
        totallabelB = CTk.CTkLabel(task_E_tab, textvariable=totalTextVar)
        totallabelB.grid(column=1, row=4, padx=20, pady=20)

        submitButton = CTk.CTkButton(task_E_tab, text="submit command", command=
            lambda: (

                self.__run_sql_command(totalTextVar.get())
            )
        )
        submitButton.grid(column=0, row=5, columnspan=2, padx=20, pady=20)

        totalTextVar.set(f"INSERT INTO entry (excode,sno) VALUES ('{excodetextEntry.get()}','{snotextEntry.get()}');")
        task_E_tab.mainloop()

    def task_F(self):
        """F. Update an entry. This records the grade awarded by the examiners to an entry
made by a student for an examination. The entry is specified by entry reference
number."""
        task_F_tab = CTk.CTk()
        task_F_tab.title(self.__title + ": Task B - adding exam")

        label = CTk.CTkLabel(task_F_tab, text="what is the students sno:")
        label.grid(column=0, row=0, padx=20, pady=20)

        snoEntryTextVar = CTk.StringVar(task_F_tab)
        snoTextEntry = CTk.CTkEntry(task_F_tab,width=120, height=40, textvariable=snoEntryTextVar)
        snoTextEntry.grid(column=1, row=0, padx=20, pady=20)

        label = CTk.CTkLabel(task_F_tab, text="what is the exams excode:")
        label.grid(column=0, row=1, padx=20, pady=20)

        excodeEntryTextVar = CTk.StringVar(task_F_tab)
        excodeTextEntry = CTk.CTkEntry(task_F_tab,width=120, height=40, textvariable=excodeEntryTextVar)
        excodeTextEntry.grid(column=1, row=1, padx=20, pady=20)

        label = CTk.CTkLabel(task_F_tab, text="what is the students egrade:")
        label.grid(column=0, row=2, padx=20, pady=20)

        egradeEntryTextVar = CTk.StringVar(task_F_tab)
        egradeTextEntry = CTk.CTkEntry(task_F_tab,width=120, height=40, textvariable=egradeEntryTextVar)
        egradeTextEntry.grid(column=1, row=2, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_F_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"SELECT give_egrade({snoTextEntry.get()},'{excodeTextEntry.get()}',{egradeTextEntry.get()});")
            )
        )
        updateButton.grid(column=0, row=3, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_F_tab)
        totallabelB = CTk.CTkLabel(task_F_tab, textvariable=totalTextVar)
        totallabelB.grid(column=1, row=3, padx=20, pady=20)

        submitButton = CTk.CTkButton(task_F_tab, text="submit command", command=
            lambda: (
                self.__run_sql_command(totalTextVar.get())
            )
        )
        submitButton.grid(column=0, row=4, columnspan=2, padx=20, pady=20)

        # making this be displayed with this text sowhen it appears its not a shock to the user
        totalTextVar.set(f"SELECT give_egrade(,'',);")
        task_F_tab.mainloop()

    #    0 0 0
    #    0 0 0
    #    G H I
    def task_G(self):
        print("task_G")

    def task_H(self):
        print("task_H")

    def task_I(self):
        self.__run_sql_command("SELECT * FROM student;")
        print("task_I")


    def init_buttons(self):

        #    A B C
        #    0 0 0
        #    0 0 0
        button = CTk.CTkButton(self.CTK, text="my buttonA", height=50, command=self.task_A)
        button.grid(column=0 , row=0, padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonB", height=50, command=self.task_B)
        button.grid(column=1 , row=0, padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonC", height=50, command=self.task_C)
        button.grid(column=2 , row=0, padx=20, pady=20)

        #    0 0 0
        #    D E F
        #    0 0 0
        button = CTk.CTkButton(self.CTK, text="my buttonD", height=50,command=self.task_D)
        button.grid(column=0 , row=1 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonE", height=50,command=self.task_E)
        button.grid(column=1 , row=1 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonF", height=50,command=self.task_F)
        button.grid(column=2 , row=1 ,padx=20, pady=20)

        #    0 0 0
        #    0 0 0
        #    G H I
        button = CTk.CTkButton(self.CTK, text="my button", height=50, command=self.task_G)
        button.grid(column=0 , row=2 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my button", height=50, command=self.task_H)
        button.grid(column=1 , row=2 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my button", height=50, command=self.task_I)
        button.grid(column=2 , row=2 ,padx=20, pady=20)


    def displayDataFromTable(self, tableName: str) -> None:
        allColumns = self.__tableNameTitles[tableName]
        if self.__DbConnection is not None:
            self.cursor.execute(f'SELECT * FROM {tableName}')
            rows = self.cursor.fetchall()

            print(rows)


app = App(conn)
#
# try:
#     app = App(conn)
#     app.mainloop()
# except Exception as e:
#     print("[ERROR]" + str(e))
# finally:
#     if conn:
#         conn.close()
