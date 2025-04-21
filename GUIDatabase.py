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

with open("../secret.json", "r") as f:
    secretData = json.load(f)

# try:
#     conn = psycopg2.connect(user=secretData["user"],
#                             password=secretData["password"],
#                             host=secretData["host"],
#                             port=secretData["port"],
#                             database=secretData["database"]
#                             )
#     print(f"successfully connected to the db named '{secretData["database"]}'!")
#     secretData = {}
#
# except psycopg2.OperationalError as e:
#     print("connection error, turn on the 'BIG-IP edge client' vpn.")
#     print("running GUI but commands won't execute.")
conn = None


class App:
    def __init__(self, database_connection: psycopg2.extensions.connection) -> None:
        """uses the connection to generate a database cursor and initialises the GUI"""
        self.CTK = CTk.CTk()
        self.__DbConnection = database_connection
        if self.__DbConnection is not None:
            self.cursor = self.__DbConnection.cursor()
            self.cursor.execute('SET search_path to summative,public;')

        self.CTK.geometry("550x450")
        self.__title = "SQL summative project"
        self.CTK.title(self.__title)

        self.__tableNameTitles: dict = {"exam": ["excode", "extitle", "exdate", "extime"],
                                        "student": ["sno", "sname", "semail"],
                                        "entry": ["eno", "excode", "sno", "egrade"],
                                        "cancel": ["eno", "excode", "sno", "cdate", "curser"]
                                        }

        # self.__tabController = CTk.CTkTabview(self.CTK)
        # self.__tabController.pack(fill="both", expand=True, padx=10, pady=10)
        self.frames: list[CTk.CTkFrame] = []
        self.frame1totalbuttons = 0
        self.mostRecentQuery = ""
        self.init_buttons()
        self.CTK.mainloop()

    def custom_func(self):
        print("custom function!")


    #    A B C
    #    0 0 0
    #    0 0 0
    def task_A(self):
        """A. Insert a new student member of the society."""

        task_A_tab = CTk.CTk()
        task_A_tab.title(self.__title + ": Task A")
        tablename = "student"

        totalQueryVar2 = CTk.StringVar(task_A_tab)
        totalQueryVar2.set("total query: ")

        required = ', '.join(self.__tableNameTitles[tablename])

        label = CTk.CTkLabel(task_A_tab, text="required columns:  " + required)
        label.grid(column=0, row=0, columnspan=2)

        requirements = CTk.StringVar(task_A_tab)
        requirements.set("Requirements: " + required)

        label = CTk.CTkLabel(task_A_tab, text="type in the parameters\nin a CSV format")
        label.grid(column=0, row=1, padx=20, pady=20)

        entryTextVarA = CTk.StringVar(task_A_tab)
        textEntry = CTk.CTkEntry(task_A_tab,width=200,height=40, textvariable=entryTextVarA)
        textEntry.grid(column=1, row=1, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_A_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"INSERT INTO {tablename}({required}) VALUES ({textEntry.get()})\n"),
                print(totalTextVar.get() + textEntry.get())
            )
        )
        updateButton.grid(column=0, row=2, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_A_tab)
        totallabelA = CTk.CTkLabel(task_A_tab, textvariable=totalTextVar)
        totallabelA.grid(column=1, row=2, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_A_tab, text="submit command", command=
            lambda: (
                print("submitting: " + totalTextVar.get())
            )
        )
        updateButton.grid(column=0, row=3, columnspan=2, padx=20, pady=20)


        task_A_tab.mainloop()

    def task_B(self):
        """B. Insert a new examination for the coming year."""
        task_B_tab = CTk.CTk()
        task_B_tab.title(self.__title + ": Task B")
        tablename = "exam"

        totalQueryVar2 = CTk.StringVar(task_B_tab)
        totalQueryVar2.set("total query: ")

        required = ', '.join(self.__tableNameTitles[tablename])

        label = CTk.CTkLabel(task_B_tab, text="required columns:  " + required)
        label.grid(column=0, row=0, columnspan=2)

        requirements = CTk.StringVar(task_B_tab)
        requirements.set("Requirements: " + required)

        label = CTk.CTkLabel(task_B_tab, text="type in the parameters\nin a CSV format")
        label.grid(column=0, row=1, padx=20, pady=20)

        entryTextVarA = CTk.StringVar(task_B_tab)
        textEntry = CTk.CTkEntry(task_B_tab,width=200,height=40, textvariable=entryTextVarA)
        textEntry.grid(column=1, row=1, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_B_tab, text="Update 'total query'", command=
            lambda: (
                totalTextVar.set(f"INSERT INTO {tablename}({required}) VALUES ({textEntry.get()})\n"),
                print(totalTextVar.get() + textEntry.get())
            )
        )
        updateButton.grid(column=0, row=2, padx=20, pady=20)

        totalTextVar = CTk.StringVar(task_B_tab)
        totallabelB = CTk.CTkLabel(task_B_tab, textvariable=totalTextVar)
        totallabelB.grid(column=1, row=2, padx=20, pady=20)

        updateButton = CTk.CTkButton(task_B_tab, text="submit command", command=
            lambda: (
                print("submitting: " + totalTextVar.get())
            )
        )
        updateButton.grid(column=0, row=3, columnspan=2, padx=20, pady=20)


        task_B_tab.mainloop()

    def task_C(self):
        """C. Delete a student. This happens if a student withdraws from the society. All the
examination entries for the student must be cancelled. The cancelled entries must
retain their student reference number even though there is no longer a matching row
in the student table."""
        print("task_c")

    #    0 0 0
    #    D E F
    #    0 0 0
    def task_D(self):
        """D. Delete an examination. Examinations that have no entries may be deleted from
the database. The examination must not have any current (not cancelled) entries."""
        print("task_D")

    def task_E(self):
        """E. Insert an examination entry. A student can only enter a specific examination once
in a year. The student cannot take more than one examination on the same day.

        so i would guess this would be the user selecting a student then saying what exam they have when?
        cant use a drop down menu for selecting a student"""

        #INSERT INTO entry (eno,excode,sno,egrade) VALUES (int,char,int,decimal)
        task_E_tab = CTk.CTk()
        task_E_tab.title(self.__title + ": Task E")

        label = CTk.CTkLabel(task_E_tab, text="what is the exam's eno:")
        label.grid(column=0, row=0, padx=20, pady=20)

        enoentryTextVar = CTk.StringVar(task_E_tab)
        enotextEntry = CTk.CTkEntry(task_E_tab,width=70,height=40, textvariable=enoentryTextVar)
        enotextEntry.grid(column=1, row=0, padx=20, pady=20)

        # -0-
        # X X
        # 0 0
        # 0 0
        # 0 0
        # 0 0
        label = CTk.CTkLabel(task_E_tab, text="what is the exam's excode:")
        label.grid(column=0, row=1, padx=20, pady=20)

        excodeentryTextVar = CTk.StringVar(task_E_tab)
        excodetextEntry = CTk.CTkEntry(task_E_tab,width=70,height=40, textvariable=excodeentryTextVar)
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
        snotextEntry = CTk.CTkEntry(task_E_tab,width=70,height=40, textvariable=snoTextVar)
        snotextEntry.grid(column=1, row=2, padx=20, pady=20)

        # -0-
        # 0 0
        # 0 0
        # X X
        # 0 0
        # 0 0
        label = CTk.CTkLabel(task_E_tab, text="what is the student's egrade:")
        label.grid(column=0, row=3, padx=20, pady=20)

        egradeEntryTextVar = CTk.StringVar(task_E_tab)
        egradeTextEntry = CTk.CTkEntry(task_E_tab,width=70,height=40, textvariable=egradeEntryTextVar)
        egradeTextEntry.grid(column=1, row=3, padx=20, pady=20)

        submitButton = CTk.CTkButton(task_E_tab, text="submit command", command=
            lambda: (
                #INSERT INTO entry (eno,excode,sno,egrade) VALUES (int,char,int,decimal)
                values := enotextEntry.get() +", "+ excodetextEntry.get() +", "+ snotextEntry.get() +", "+ egradeTextEntry.get(),
                toSub := f"INSERT INTO entry (eno,excode,sno,egrade) VALUES ({values});",
                print("submitting: " + toSub)
            )
        )
        submitButton.grid(column=0, row=4, columnspan=2, padx=20, pady=20)


        task_E_tab.mainloop()

    def task_F(self):
        """F. Update an entry. This records the grade awarded by the examiners to an entry
made by a student for an examination. The entry is specified by entry reference
number."""
        print("task_F")

    #    0 0 0
    #    0 0 0
    #    G H I
    def task_G(self):
        print("task_G")

    def task_H(self):
        print("task_H")

    def task_I(self):
        print("task_I")
    def init_buttons(self):

        #    A B C
        #    0 0 0
        #    0 0 0
        button = CTk.CTkButton(self.CTK, text="my buttonA", command=self.task_A)
        button.grid(column=0 , row=0 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonB", command=self.task_B)
        button.grid(column=1 , row=0 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonC", command=self.task_C)
        button.grid(column=2 , row=0 ,padx=20, pady=20)

        #    0 0 0
        #    D E F
        #    0 0 0
        button = CTk.CTkButton(self.CTK, text="my buttonD", command=self.task_D)
        button.grid(column=0 , row=1 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonE", command=self.task_E)
        button.grid(column=1 , row=1 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my buttonF", command=self.task_F)
        button.grid(column=2 , row=1 ,padx=20, pady=20)

        #    0 0 0
        #    0 0 0
        #    G H I
        button = CTk.CTkButton(self.CTK, text="my button", command=self.task_G)
        button.grid(column=0 , row=2 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my button", command=self.task_H)
        button.grid(column=1 , row=2 ,padx=20, pady=20)

        button = CTk.CTkButton(self.CTK, text="my button", command=self.task_I)
        button.grid(column=2 , row=2 ,padx=20, pady=20)

        # # following CRUD, Create, Retrieve, update, Delete
        # self.frames.append(self.__tabController.add("Selecting"))
        # self.frames.append(self.__tabController.add("Inserting"))
        # self.frames.append(self.__tabController.add("Update"))
        # self.frames.append(self.__tabController.add("Delete"))
        # self.frames.append(self.__tabController.add("Tools"))
        # self.frames.append(self.__tabController.add("Results"))
        #
        # # the default GUI on each of the tabs
        # self.initiliseFrame1()
        # self.initiliseFrame2()
        # self.initiliseFrame3()
        # self.initiliseFrame4()
        # self.initiliseFrame5()
        # self.initiliseFrame6()
        #
        # # updating the title of the tab to show what tab the user is on for more responsiveness
        # self.frames[0].bind('<Enter>', lambda _: self.title(self.__title + " - Selecting Data"))
        # self.frames[1].bind('<Enter>', lambda _: self.title(self.__title + " - Inserting Data"))
        # self.frames[2].bind('<Enter>', lambda _: self.title(self.__title + " - Updating Data"))
        # self.frames[3].bind('<Enter>', lambda _: self.title(self.__title + " - Deleting Data"))
        # self.frames[4].bind('<Enter>', lambda _: self.title(self.__title + " - Running any Command"))
        # self.frames[5].bind('<Enter>', lambda _: self.title(self.__title + " - Looking at Data"))

    def initiliseFrame1(self) -> None:
        """The Gui for the Selecting Tab"""

        label = CTk.CTkLabel(self.frames[0], text="Chose from a table")
        label.grid(column=0, row=0)

        dropDownOptionValue = CTk.StringVar()
        totalQueryVar = CTk.StringVar()

        dropDownOptions = list(self.__tableNameTitles.keys())
        dropDownTableOptions = CTk.CTkOptionMenu(self.frames[0], variable=dropDownOptionValue, values=dropDownOptions)
        dropDownTableOptions.set(dropDownOptions[0])
        dropDownTableOptions.grid(column=1, row=0, padx=20, pady=20)

        Checkbutton1 = CTk.IntVar()
        Checkbutton2 = CTk.IntVar()
        Checkbutton3 = CTk.IntVar()
        Checkbutton4 = CTk.IntVar()

        checkButtonText1 = CTk.StringVar()
        checkButtonText2 = CTk.StringVar()
        checkButtonText3 = CTk.StringVar()
        checkButtonText4 = CTk.StringVar()

        labelFrame = Tk.LabelFrame(self.frames[0], text="Columns", bg="gray")

        Button1 = CTk.CTkCheckBox(labelFrame, textvariable=checkButtonText1,
                                  variable=Checkbutton1,
                                  onvalue=True,
                                  offvalue=False)

        Button2 = CTk.CTkCheckBox(labelFrame, textvariable=checkButtonText2,
                                  variable=Checkbutton2,
                                  onvalue=True,
                                  offvalue=False)

        Button3 = CTk.CTkCheckBox(labelFrame, textvariable=checkButtonText3,
                                  variable=Checkbutton3,
                                  onvalue=True,
                                  offvalue=False)

        Button4 = CTk.CTkCheckBox(labelFrame, textvariable=checkButtonText4,
                                  variable=Checkbutton4,
                                  onvalue=True,
                                  offvalue=False)
        allButtons = [Button1, Button2, Button3, Button4]
        allButtonsText = [checkButtonText1, checkButtonText2, checkButtonText3, checkButtonText4]

        labelFrame.grid(column=1, row=2, columnspan=3, padx=0, pady=0)

        label = CTk.CTkLabel(self.frames[0], text="type in the WHERE clause")
        label.grid(column=0, row=5, padx=20, pady=20)

        entryTextVar = CTk.StringVar()
        textEntry = CTk.CTkEntry(self.frames[0], textvariable=entryTextVar)
        textEntry.grid(column=1, row=5, padx=20, pady=20)

        updateButton = CTk.CTkButton(self.frames[0], text="Update 'total query'", command=
        lambda: (
            self.updateTotalQueryFrame1(totalQueryVar, dropDownOptionValue, entryTextVar, allButtons, allButtonsText)))
        updateButton.grid(column=0, row=6, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[0], textvariable=totalQueryVar)
        label.grid(column=1, row=6, padx=20, pady=20)

        self.updateTotalQueryFrame1(totalQueryVar, dropDownOptionValue, entryTextVar, allButtons, allButtonsText)

    def updateTotalQueryFrame1(self, totalQueryVar: CTk.StringVar, dropDownOptionValue: CTk.StringVar,
                               WHERETextVar: CTk.StringVar, allButtons: list[CTk.CTkCheckBox],
                               allButtonsText: list[CTk.StringVar]):
        try:
            self.__tableNameTitles[dropDownOptionValue.get()]
        except KeyError:  # when the user hasnt selected a table
            return

        tableName = dropDownOptionValue.get()
        self.frame1totalbuttons = len(self.__tableNameTitles[tableName])

        for i in range(len(allButtons)):
            allButtonsText[i].set("_________")
            allButtons[i].lower()
            allButtons[i].configure(state=CTk.DISABLED)

        totalQueryColumns = []

        for i in range(self.frame1totalbuttons):
            allButtons[i].forget()  # I have forgotten what this even does ong
            allButtons[i].configure(state=CTk.NORMAL)

            allButtons[i].grid(column=2, row=i, padx=5, pady=5)
            allButtonsText[i].set(self.__tableNameTitles[tableName][i])
            if allButtons[i].get():
                totalQueryColumns.append(allButtonsText[i].get())

        if len(totalQueryColumns) == self.frame1totalbuttons:
            totalQueryColumns = ["*"]

        if WHERETextVar.get() == "":
            self.mostRecentQuery = f"SELECT {(", ".join(totalQueryColumns))}\n FROM {tableName};"
            totalQueryVar.set(f"total query: {self.mostRecentQuery}")

        else:
            self.mostRecentQuery = f"SELECT {(", ".join(totalQueryColumns))}\n FROM {tableName} WHERE \n{WHERETextVar.get()};"
            totalQueryVar.set(f"total query:\n{self.mostRecentQuery}")

        print("executing: " + self.mostRecentQuery)
        if self.__DbConnection != None:
            self.cursor.execute(self.mostRecentQuery)
            print(self.cursor.fetchall())
        # self.__DbConnection.commit()

    def initiliseFrame2(self):
        """The Gui for the 2nd Tab, Inserting data."""

        totalQueryVar = CTk.StringVar()
        totalQueryVar.set("total query: ")

        label = CTk.CTkLabel(self.frames[1], text="Chose from a table")
        label.grid(column=0, row=0)

        requirements = CTk.StringVar()
        requirements.set("Requirements")

        dropDownOptionValue = CTk.StringVar()

        dropDownOptions = list(self.__tableNameTitles.keys())
        dropDownTableOptions = CTk.CTkOptionMenu(self.frames[1], variable=dropDownOptionValue, values=dropDownOptions)
        dropDownTableOptions.set(dropDownOptions[0])
        dropDownTableOptions.grid(column=1, row=0, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[1], text="type in the parameters\nin a CSV format")
        label.grid(column=0, row=1, padx=20, pady=20)

        entryTextVar = CTk.StringVar()
        textEntry = CTk.CTkEntry(self.frames[1], textvariable=entryTextVar)
        textEntry.grid(column=1, row=1, padx=20, pady=20)

        updateButton = CTk.CTkButton(self.frames[1], text="Update 'total query'", command=
        lambda: (
            totalQueryVar.set("total query:\nINSERT INTO " + dropDownOptionValue.get() + "(" + (", ".join(self.__tableNameTitles[dropDownOptionValue.get()])) + ")" + "VALUES\n(" + entryTextVar.get() + ")"),requirements.set("Requirements\n" + (", ".join(self.__tableNameTitles[dropDownOptionValue.get()])))))
        updateButton.grid(column=0, row=2, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[1], textvariable=totalQueryVar)
        label.grid(column=1, row=2, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[1], textvariable=requirements)
        label.grid(column=1, row=3, padx=20, pady=20)

        insertButton = CTk.CTkButton(self.frames[1], text="insert into database",
                                     command=lambda: self.__insertIntoDb(dropDownOptionValue.get(), entryTextVar.get().replace('"',"'")))
        insertButton.grid(column=0, row=3, padx=20, pady=20) 

    def __insertIntoDb(self, tableName: str, values: str):
        command = f"INSERT INTO {tableName}({', '.join(self.__tableNameTitles[tableName])}) VALUES ({values});"
        print(command),
        if self.__DbConnection is not None:
            self.cursor.execute(command),
            self.__DbConnection.commit()

    def __updateDb(self):
        pass

    def initiliseFrame3(self):
        """the Frame for the update GUI"""
        entryTextVar = CTk.StringVar()
        requirements = CTk.StringVar()
        totalQueryVar = CTk.StringVar()
        totalQueryVar.set("total query: ")

        label = CTk.CTkLabel(self.frames[2], text="Chose from a table")
        label.grid(column=0, row=0, padx=20, pady=20)

        dropDownOptionValue = CTk.StringVar()

        dropDownOptions = list(self.__tableNameTitles.keys())
        dropDownTableOptions = CTk.CTkOptionMenu(self.frames[2], variable=dropDownOptionValue, values=dropDownOptions)
        dropDownTableOptions.set(dropDownOptions[0])
        dropDownTableOptions.grid(column=1, row=0, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[2], text="Set the new values:")
        label.grid(column=0, row=1, padx=20, pady=20)
        label = CTk.CTkLabel(self.frames[2], text="WHERE:")
        label.grid(column=0, row=2, padx=20, pady=20)

        entryTextVar1 = CTk.StringVar()
        entryTextVar2 = CTk.StringVar()

        textEntry1 = CTk.CTkEntry(self.frames[2], textvariable=entryTextVar1)
        textEntry2 = CTk.CTkEntry(self.frames[2], textvariable=entryTextVar2)
        textEntry1.grid(column=1, row=1, padx=20, pady=20)
        textEntry2.grid(column=1, row=2, padx=20, pady=20)

        updateButton = CTk.CTkButton(self.frames[2], text="Update 'total query'", command=
        lambda: (totalQueryVar.set(f"total query:\nUPDATE {dropDownTableOptions.get()} SET{(", ".join(
            self.__tableNameTitles[dropDownOptionValue.get()]))} VALUES\n(" + entryTextVar.get() + ")"),
                 requirements.set("Requirements\n" + (", ".join(self.__tableNameTitles[dropDownOptionValue.get()])))))

        updateButton.grid(column=0, row=3, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[2], textvariable=totalQueryVar)
        label.grid(column=1, row=3, padx=20, pady=20)

    def initiliseFrame4(self):
        """the Frame for the Delete GUI"""
        pass

    def initiliseFrame5(self):
        """the Frame for the Tools GUI"""
        commandInp = CTk.StringVar()
        requirements = CTk.StringVar()
        totalQueryVar = CTk.StringVar()
        totalQueryVar.set("total query: ")

        text_tables = f"Chose from a table: {', '.join(list(self.__tableNameTitles.keys()))}"

        label = CTk.CTkLabel(self.frames[4], text=text_tables)
        label.grid(column=0, row=0, padx=20, pady=20)

        label = CTk.CTkLabel(self.frames[4], text="what command to run:")
        label.grid(column=0, row=1, padx=20, pady=20)
        textEntry1 = CTk.CTkEntry(self.frames[4], textvariable=commandInp)
        textEntry1.grid(column=1, row=1)

        updateButton = CTk.CTkButton(self.frames[4], text="execute command", command=
        lambda: self.__runAnyCommand(commandInp.get()))
        updateButton.grid(column=0, row=2, padx=20, pady=20)

    def __runAnyCommand(self, command: str):
        """runs ANY sql command onto the database without any checks
        SQL injection who?"""
        if self.__DbConnection is not None:
            self.cursor.execute(command)
            self.__DbConnection.commit()

    def initiliseFrame6(self):
        """the Frame for the Results GUI"""
        pass

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
