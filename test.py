from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QLineEdit,QGridLayout,QMainWindow,QMessageBox,QTextEdit, QDialog,QTableWidget, QHeaderView
from PyQt5.QtGui import QFont, QGuiApplication
from PyQt5.uic import loadUi
import mysql.connector
import bcrypt
import datetime

#CHANGE THE LOCATION OF ADDING TO THE TOP OF type

#DATABASE CONFIGURATION
connection = mysql.connector.connect(host="localhost",database="cc15",user="root",password="root")
cursor = connection.cursor(prepared=True)

class ElistaCalendarOperation(QDialog):
    #FEATURE TO DO LIST SHOULD BE BY MONTH
    
    def __init__(self,session):
        super().__init__()
        self.session = session
        loadUi("elistaCalendar.ui",self)
        self.authenticatedNameLabel.setText(Database.getUsername(session))
        #create updating buttons
        self.firstAuthenticatedButton.clicked.connect(self.dynamicButton)
        #self.secondAuthenticatedButton.clicked.connect(self.dynamicButton) DECOMISSIONED
        self.thirdAuthenticatedButton.clicked.connect(self.dynamicButton)
        self.fourthAuthenticatedButton.clicked.connect(self.dynamicButton)

        self.calendarBox.currentTextChanged.connect(self.calendarDynamicComboBox) 
        self.calendarDynamicComboBox(self.calendarBox.currentText()) 

        self.calendarData.clicked.connect(self.calendarPressEvent)

        self.calendarTable.cellDoubleClicked.connect(self.rowClickEvent)
        self.calendarTable.verticalHeader().setVisible(False)
        self.calendarTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.calendarTable.setSelectionMode(QTableWidget.SingleSelection)

    def rowClickEvent(self, row, column):
        row_data = []
        for col in range(self.calendarTable.columnCount()):
            item = self.calendarTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        #GO BACK HERE
        edit = ElistaEditOperation(self.session,row_data[-1],row_data[2],Database.sanitizedGetPriorityName(row_data[-1]),Database.sanitizedGetStatusName(row_data[-1]),False)

        widget.setFixedWidth(480)
        widget.setFixedHeight(600)
        widget.addWidget(edit)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

        print("Row clicked:", row_data)
    
    #DESIGN THIS FUNCTIONALITY
    def calendarPressEvent(self, date: QDate):
        year = date.year()
        month = date.month()
        day = date.day()

        calendarData = Database.getSanitizedCalendarDayData(year,month,day,self.session)
        self.calendarTable.setRowCount(len(calendarData))
        self.calendarTable.setColumnCount(5)

        self.calendarTable.setHorizontalHeaderLabels(["Task","Priority","Status","Type","TaskID"])
        self.calendarTable.setColumnHidden(3, False)
        self.calendarTable.setColumnHidden(4, True)

        self.calendarTable.clearContents()

        tableRow = 0
        for i in calendarData:
            print(i)
            self.calendarTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.calendarTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
            self.calendarTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
            self.calendarTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(i[3])))
            self.calendarTable.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(i[4])))

            tableRow += 1


       #IMPORTANT EVENT 
        print(f"Clicked date: {year}-{month:02d}-{day:02d}")

        
        #calendarData = Database.getSanitizedDayData(year,month,day,self.session)

        #print(calendarData)

    def editTable(self,typeTable):
        tableRow = 0
        for i in typeTable:
            print(i)
            self.calendarTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
            self.calendarTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
            self.calendarTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
            self.calendarTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(i[3])))
            tableRow += 1
            

    #SORT BY MONTH FEATURE. 
    def calendarDynamicComboBox(self,sortBy):

        #8756523
        if sortBy == "Priority":
            self.calendarTable.resizeRowsToContents()
            self.calendarTable.setColumnCount(4)
            self.calendarTable.setHorizontalHeaderLabels(["Task","Priority","Type","TaskID"])


            priorityData = Database.getSanitizedCalendarPriorityData(self.session)
            print(self.calendarData.selectedDate().year()) 
            self.calendarData.selectedDate().month()
            self.calendarTable.setRowCount(len(priorityData))
            

            self.editTable(priorityData)

        if sortBy == "Deadline":
            self.calendarTable.resizeRowsToContents()
            self.calendarTable.setColumnCount(4)

            self.calendarTable.setHorizontalHeaderLabels(["Task","Deadline","Type","TaskID"])

            deadlineData = Database.getSanitizedCalendarDeadlineData(self.session)
            self.calendarTable.setRowCount(len(deadlineData))


            tableRow = 0

            self.editTable(deadlineData)

            
        if sortBy == "Status":
            self.calendarTable.resizeRowsToContents()
            self.calendarTable.setColumnCount(4)

            self.calendarTable.setHorizontalHeaderLabels(["Task","Status","Type","TaskID"])

            statusData = Database.getSanitizedCalendarStatusData(self.session)
            self.calendarTable.setRowCount(len(statusData))


            self.editTable(statusData)

    
    
    def dynamicButton(self):
        pressed = self.sender()

        if pressed == self.firstAuthenticatedButton:
            loggedIn = ElistaMainPage(self.session)
            widget.addWidget(loggedIn)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)
            
        elif pressed == self.thirdAuthenticatedButton:
            calendar = ElistaCalendarOperation(self.session) 
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1) 


        elif pressed == self.fourthAuthenticatedButton:
            Utilities.confirmLogout()
            

class ElistaAddOperation(QDialog):
    def __init__(self,session,typeName):
        super().__init__()
        self.session = session
        self.typeName = typeName
        loadUi("elistaAdd.ui",self)

        #task adder functionality here
        self.addTaskSubmitBox.clicked.connect(self.addTask)
        self.taskAdderReturn.clicked.connect(self.returnToMainPage)

        self.addTaskDeadlineBox.setDate(QDate.currentDate())


        #STRUCTURAL CODE. dont remove.
        aliases = {"Personal": "Personal","Assign": "Academics","Plan": "Miscs..."}

        self.addToLabel.setText("ADDING TO " + str(aliases[self.typeName]).upper())

        meanings = {

        }

    def returnToMainPage(self):
        loggedIn = ElistaMainPage(self.session)
        widget.addWidget(loggedIn)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1400)
        widget.setFixedHeight(800)

    def addTask(self):
        print(self.typeName)
        taskOwner = self.session
        taskPriority = self.addTaskPriorityBox.currentText()
        taskType = self.typeName
        taskStatus = "Pending"
        taskName = self.taskNameField.toPlainText()
        taskDeadline = self.addTaskDeadlineBox.date().toString("yyyy-MM-dd")

        #TASK NAME MUST NOT BE EMPTY

        Database.sanitizedInsertTask(taskOwner,taskPriority,taskType,taskStatus,taskName,taskDeadline)

        Utilities.successfulAction()

class ElistaEditOperation(QDialog):
    def __init__(self,session,taskId,typeName,priority,status,isFromMain):
        super().__init__()
        self.session = session
        self.taskId = taskId
        self.typeName = typeName
        self.priority = priority
        self.status = status
        self.isFromMain = isFromMain

        loadUi("elistaUpdate.ui",self)
        self.reviseTypeBox.setCurrentText(self.typeName)
        self.revisePriorityBox.setCurrentText(self.priority)
        self.reviseStatusBox.setCurrentText(self.status)

        self.reviseTaskId.setText(str(taskId))  
        self.reviseNameBox.setText(Database.getSanitizedTaskName(self.taskId))
        
        self.reviseCancelButton.clicked.connect(self.returnToMainPage)
        self.reviseDiscardButton.clicked.connect(self.removeTask)

        self.reviseUpdateButton.clicked.connect(self.updateTask)
        self.reviseDeadlineBox.setDate(QDate.currentDate())




    def updateTask(self):
        updateName = self.reviseNameBox.text()
        updatePriority = self.revisePriorityBox.currentText()
        updateStatus = self.reviseStatusBox.currentText()
        updateType = self.reviseTypeBox.currentText()
        updateDeadline = self.reviseDeadlineBox.date().toString("yyyy-MM-dd")

        Database.sanitizedUpdateTask(updateName,updatePriority,updateStatus,updateType,updateDeadline,self.taskId)

        Utilities.successfulAction()

        if self.isFromMain:
            loggedIn = ElistaMainPage(self.session)
            widget.addWidget(loggedIn)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)
        else:
            calendar = ElistaCalendarOperation(self.session) 
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)



    def returnToMainPage(self):
        if self.isFromMain:
            loggedIn = ElistaMainPage(self.session)
            widget.addWidget(loggedIn)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)
        else:
            calendar = ElistaCalendarOperation(self.session) 
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)

    def removeTask(self):
        Database.sanitizedDeleteTask(self.taskId)
        self.returnToMainPage()

   
#CREATE ELISTA UPDATE PAGE
#CREATE ELISTA DELETE PAGE



class ElistaMainPage(QDialog):
    def __init__(self,session): #SESSION IS VERY IMPORTANT
        super().__init__()
        self.session = session
        loadUi("elistaMain.ui",self)
        self.authenticatedNameLabel.setText(Database.getUsername(session))
        #create updating buttons
        self.firstAuthenticatedButton.clicked.connect(self.dynamicButton)
        


        #---------------------------------------------------------------------

        self.personalizeAuthenticatedButton.clicked.connect(self.dynamicAdderButton) #TEMPORARY MAINTENANCE
        self.AssignAuthenticatedButton.clicked.connect(self.dynamicAdderButton)
        self.MiscAuthenticatedButton.clicked.connect(self.dynamicAdderButton)


        #-------------------------------------------------------------


        self.thirdAuthenticatedButton.clicked.connect(self.dynamicButton)
        self.fourthAuthenticatedButton.clicked.connect(self.dynamicButton)

        self.personalBox.currentTextChanged.connect(self.personalDynamicComboBoxes) 
        self.personalDynamicComboBoxes(self.personalBox.currentText()) 
        
        self.academicBox.currentTextChanged.connect(self.academicDynamicComboBoxes)
        self.academicDynamicComboBoxes(self.academicBox.currentText())

        self.miscBox.currentTextChanged.connect(self.miscDynamicComboBoxes)
        self.miscDynamicComboBoxes(self.miscBox.currentText())

        #table configurations
        self.personalTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.personalTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.personalTable.verticalHeader().setVisible(False)
        self.personalTable.setColumnHidden(3, True)


        self.academicTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.academicTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.academicTable.verticalHeader().setVisible(False)
        self.academicTable.setColumnHidden(3, True)

        self.miscTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.miscTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.miscTable.verticalHeader().setVisible(False)
        self.miscTable.setColumnHidden(3, True)

        #CREATE CLICK TABLE ROW EVENT

        self.personalTable.cellDoubleClicked.connect(self.rowClickEventOne)
        self.academicTable.cellDoubleClicked.connect(self.rowClickEventTwo)
        self.miscTable.cellDoubleClicked.connect(self.rowClickEventThree)
    
    def addMenu(self,location):
        crud = ElistaAddOperation(self.session,location)
        widget.setFixedWidth(480)
        widget.setFixedHeight(600)
        widget.addWidget(crud)
        widget.setCurrentIndex(widget.currentIndex() + 1) 
    
    def dynamicAdderButton(self):
        #sanitizedInsertTask(taskOwner,taskPriority,taskType,taskStatus,taskName,taskDeadline):
        #data = (taskOwner,priorityDict[taskPriority],typeDict[taskType],statusDict[taskStatus],taskName,taskDeadline,)

        sender = self.sender()
        pressed = sender.text()

        if pressed == "Personalize":
            print("it works!")
            self.addMenu("Personal")
        
        if pressed == "Assign":
            print("Assign works!")
            self.addMenu("Assign")

        if pressed == "Plan":
            print("Plan works!")
            self.addMenu("Plan")

    def rowClickEventOne(self, row, column):
        row_data = []
        for col in range(self.personalTable.columnCount()):
            item = self.personalTable.item(row, col)
            row_data.append(item.text() if item else "")
        #CREATE A DELETER AND UPDATER HERE


        #(self,session,taskId)
        
        edit = ElistaEditOperation(self.session,row_data[3],"Personal",row_data[1],row_data[2],True) 
        widget.setFixedWidth(480)
        widget.setFixedHeight(600)
        widget.addWidget(edit)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

        print("Row clicked:", row_data)
    
    def rowClickEventTwo(self,row,column):
        row_data = []
        for col in range(self.academicTable.columnCount()):
            item = self.academicTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        edit = ElistaEditOperation(self.session,row_data[3],"Academic",row_data[1],row_data[2],True) 
        widget.setFixedWidth(480)
        widget.setFixedHeight(600)
        widget.addWidget(edit)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

        print("Row clicked:", row_data)
    
    def rowClickEventThree(self,row,column):
        row_data = []
        for col in range(self.miscTable.columnCount()):
            item = self.miscTable.item(row, col)
            row_data.append(item.text() if item else "")
        
        edit = ElistaEditOperation(self.session,row_data[3],"Miscellaneous",row_data[1],row_data[2],True) 
        widget.setFixedWidth(480)
        widget.setFixedHeight(600)
        widget.addWidget(edit)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

        print("Row clicked:", row_data)


    #MAKE TABLE HERE
    def personalDynamicComboBoxes(self,sortBy):
        if sortBy == "Priority":
            self.personalTable.resizeRowsToContents()
            self.personalTable.setColumnCount(4)
            
            self.personalTable.setHorizontalHeaderLabels(["Task","Priority","Status","Task ID"])

            priorityData = Database.getSanitizedPriorityData(self.session,1) 
            self.personalTable.setRowCount(len(priorityData))

            tableRow = 0

            for i in priorityData:
                print(i)
                self.personalTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
                self.personalTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
                self.personalTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
                self.personalTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(i[3])))
                tableRow += 1

        if sortBy == "Deadline":
            self.personalTable.resizeRowsToContents()
            self.personalTable.setColumnCount(4)
       
            self.personalTable.setHorizontalHeaderLabels(["Task","Deadline","Status", "Task ID"])

            deadlineData = Database.getSanitizedDeadlineData(self.session,1) 
            self.personalTable.setRowCount(len(deadlineData))

            tableRow = 0

            for j in deadlineData:
                print(j)
                self.personalTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.personalTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.personalTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                self.personalTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(j[3])))
                tableRow += 1
        
        if sortBy == "Status":
            self.personalTable.resizeRowsToContents()
            self.personalTable.setColumnCount(4)

            self.personalTable.setHorizontalHeaderLabels(["Task","Status","Deadline","Task ID"])

            statusData = Database.getSanitizedStatusData(self.session,1)
            self.personalTable.setRowCount(len(statusData))

            tableRow = 0

            for j in statusData:
                print(j)
                self.personalTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.personalTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.personalTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                self.personalTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(j[3])))
                tableRow += 1

        
    def academicDynamicComboBoxes(self,sortBy):
        if sortBy == "Priority":
            self.academicTable.resizeRowsToContents()
            self.academicTable.setColumnCount(4)
            
            self.academicTable.setHorizontalHeaderLabels(["Task","Priority","Status","Task ID"])

            priorityData = Database.getSanitizedPriorityData(self.session,2) 
            print(priorityData)
            self.academicTable.setRowCount(len(priorityData))

            tableRow = 0

            for i in priorityData:
                print(i)
                self.academicTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
                self.academicTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
                self.academicTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
                self.academicTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(i[3])))
                tableRow += 1
        
        if sortBy == "Deadline":
            self.academicTable.resizeRowsToContents()
            self.academicTable.setColumnCount(4)
       
            self.academicTable.setHorizontalHeaderLabels(["Task","Deadline","Status","Task ID"])

            deadlineData = Database.getSanitizedDeadlineData(self.session,2) 
            self.academicTable.setRowCount(len(deadlineData))

            tableRow = 0

            for j in deadlineData:
                print(j)
                self.academicTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.academicTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.academicTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                self.academicTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(j[3])))
                tableRow += 1
        
        if sortBy == "Status":
            self.academicTable.resizeRowsToContents()
            self.academicTable.setColumnCount(4)

            self.academicTable.setHorizontalHeaderLabels(["Task","Status","Deadline","Task ID"])

            statusData = Database.getSanitizedStatusData(self.session,2)
            self.academicTable.setRowCount(len(statusData))

            tableRow = 0

            for j in statusData:
                print(j)
                self.academicTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.academicTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.academicTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                self.academicTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(j[3])))
                tableRow += 1

    def miscDynamicComboBoxes(self,sortBy):
        if sortBy == "Priority":
            self.miscTable.resizeRowsToContents()
            self.miscTable.setColumnCount(4)
            
            self.miscTable.setHorizontalHeaderLabels(["Task","Priority","Status","Task ID"])

            priorityData = Database.getSanitizedPriorityData(self.session,3) 
            print(priorityData)
            self.miscTable.setRowCount(len(priorityData))

            tableRow = 0

            for i in priorityData:
                print(i)
                self.miscTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
                self.miscTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
                self.miscTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
                self.miscTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(i[3])))
                tableRow += 1

        if sortBy == "Deadline":
            self.miscTable.resizeRowsToContents()
            self.miscTable.setColumnCount(4)
       
            self.miscTable.setHorizontalHeaderLabels(["Task","Deadline","Status","Task ID"])

            deadlineData = Database.getSanitizedDeadlineData(self.session,3) 
            self.miscTable.setRowCount(len(deadlineData))

            tableRow = 0

            for j in deadlineData:
                print(j)
                self.miscTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.miscTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.miscTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                self.miscTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(j[3])))
                tableRow += 1
        
        if sortBy == "Status":
            self.miscTable.resizeRowsToContents()
            self.miscTable.setColumnCount(4)

            self.miscTable.setHorizontalHeaderLabels(["Task","Status","Deadline","Task ID"])

            statusData = Database.getSanitizedStatusData(self.session,2)
            self.miscTable.setRowCount(len(statusData))

            tableRow = 0

            for j in statusData:
                print(j)
                self.miscTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.miscTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.miscTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                self.miscTable.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(j[3])))
                tableRow += 1
            
            
            

          


        








    def dynamicButton(self):
        pressed = self.sender()

        if pressed == self.firstAuthenticatedButton:
            loggedIn = ElistaMainPage(self.session)
            widget.addWidget(loggedIn)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)
            

        #DECOMISSIONED!!!!!!!
        #elif pressed == self.secondAuthenticatedButton: 

            #make a CREATE READ UPDATE CLASS. MAKE THIS ONE FIRST
            #crud = ElistaAddOperation(self.session)
            #widget.setFixedWidth(480)
            #widget.setFixedHeight(600)
            #widget.addWidget(crud)
            #widget.setCurrentIndex(widget.currentIndex() + 1) 


        elif pressed == self.thirdAuthenticatedButton:
            calendar = ElistaCalendarOperation(self.session) 
            widget.addWidget(calendar)
            widget.setCurrentIndex(widget.currentIndex() + 1) 


        elif pressed == self.fourthAuthenticatedButton:
            Utilities.confirmLogout()
            























class Login(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui",self)
        self.LoginSubmitButton.clicked.connect(self.authenticate)
        self.LoginPasswordForm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.visitSignupPage)

        #SET FAILS 
        Database.sanitizedEnforceDeadlines(str(datetime.datetime.today()).split()[0])

        #CLEAR COMPLETED TASKS UPON LOGGING OUT
        Database.sanitizedClearCompletedTasks()

    
    def visitSignupPage(self):
        visitPage = Signup()
        widget.addWidget(visitPage)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

    def authenticate(self):
        username = self.LoginEmailForm.text()
        password = self.LoginPasswordForm.text()

        session = Database.sanitizedLogin(username,password) #handles user login system

        print(session)

        if session != None:
            loggedIn = ElistaMainPage(session)
            widget.addWidget(loggedIn)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(1400)
            widget.setFixedHeight(800)



class Signup(QDialog):
    def __init__(self):
        super(Signup,self).__init__()
        loadUi("create.ui",self)
        self.signupSubmitButton.clicked.connect(self.createAccount)
        self.signupReturnButton.clicked.connect(self.goBackToLogin)
        self.SignupPasswordForm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.SignupConfirmPasswordForm.setEchoMode(QtWidgets.QLineEdit.Password)

    def goBackToLogin(self):
        loginPage = Login()
        widget.addWidget(loginPage)
        widget.setCurrentIndex(widget.currentIndex() + 1) 


    def createAccount(self):
        username = self.signupUsernameForm.text()
        
        #MAKE USERNAMES EXTREMELY SHORT

        #ADD FORCED STRONG PASSWORD MECHHANISM
        if (self.SignupPasswordForm.text() == self.SignupConfirmPasswordForm.text()) and (self.SignupPasswordForm.text() != "" and self.SignupConfirmPasswordForm.text() != "") and (self.signupUsernameForm.text() != ""): #note to self. make the signup proccess strict asf. 
            password = self.SignupPasswordForm.text() 
            hashed = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            
            inserted = Database.sanitizedInsertUser(username,hashed)
            
            if inserted:
                print("Account created!",username,hashed) #DEBUGGING PURPOSES. DO NOT DELETE
                goBack = Login()
                widget.addWidget(goBack)
                widget.setCurrentIndex(widget.currentIndex()+1)

typeDict = {
    "Personal": 1,

    "Assign": 2, 
    "Academic": 2,

    "Plan": 3,
    "Miscellaneous": 3
}

priorityDict = {
    "Urgent": 1,
    "High": 2,
    "Average": 3,
    "Low": 4,
    "Optional": 5
}

statusDict = {
    "Completed": 1,
    "Concluding": 2,
    "In Progress": 3,
    "Pending": 4,
}

class Database():
    @staticmethod 
    def sanitizedClearCompletedTasks():
        query = """DELETE FROM tasks WHERE statusid = 1"""
        cursor.execute(query)
        connection.commit()

    @staticmethod
    def sanitizedGetStatusName(taskid):
        data = (taskid,)
        query = """SELECT statusname from tasks INNER JOIN taskstatus ON tasks.statusid = taskstatus.statusid WHERE taskid = %s"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        
        return result[0][0]

    @staticmethod
    def sanitizedGetPriorityName(taskid):
        data = (taskid,)
        query = """SELECT priorityname FROM tasks INNER JOIN taskpriority ON tasks.priorityid = taskpriority.priorityid WHERE taskid = %s"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        
        return result[0][0]

    @staticmethod
    def sanitizedEnforceDeadlines(today):
        data = (today,)
        query = """UPDATE Tasks SET statusid = 5 WHERE deadline < %s AND statusid != 5"""
        cursor.execute(query,data)
        connection.commit()


    #(year,month,day,self.session)
    @staticmethod
    def getSanitizedCalendarDayData(year,month,day,session):
        data = (year,month,day,session)
        query = """SELECT taskname,priorityname,statusname,typename,tasks.taskid FROM tasks INNER JOIN taskpriority ON tasks.priorityid = taskpriority.priorityid INNER JOIN taskstatus on tasks.statusid = taskstatus.statusid INNER JOIN tasktype ON tasks.typeid = tasktype.typeid WHERE YEAR(deadline) = %s AND MONTH(deadline) = %s AND DAY(deadline) = %s AND userid = %s"""
        cursor.execute(query,data)
        result = cursor.fetchall()

        return result

    


    




    @staticmethod #ADD YEAR AND MONTH FEATURE
    def getSanitizedCalendarStatusData(session):
        data = (session,)
        query = """SELECT taskname,statusname,typename,taskid from tasks INNER JOIN taskstatus on tasks.statusid = taskstatus.statusid inner join tasktype on tasks.typeid = tasktype.typeid where userid = %s ORDER BY tasks.statusid"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def getSanitizedCalendarDeadlineData(session):
        data = (session,)
        query = """SELECT taskname,deadline,typename,taskid from tasks inner join tasktype on tasks.typeid = tasktype.typeid where userid = %s ORDER BY deadline ASC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def getSanitizedCalendarPriorityData(session):
        data = (session,)
        query = """SELECT taskname,priorityname,typename,taskid FROM tasks INNER JOIN taskpriority ON tasks.priorityid = taskpriority.priorityid INNER JOIN tasktype on tasks.typeid = tasktype.typeid WHERE userid = %s ORDER BY tasks.priorityid ASC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def sanitizedDeleteTask(taskId):
        data = (taskId,)
        query = """DELETE FROM Tasks where taskid = %s"""
        cursor.execute(query,data)
        connection.commit()
        
    @staticmethod
    def getSanitizedPriorityData(session,typeId):
        data = (session,typeId)
        query = """SELECT taskname,priorityname,statusname,taskid FROM tasks INNER JOIN taskstatus ON tasks.statusid = taskstatus.statusid INNER JOIN taskpriority ON tasks.priorityid = taskpriority.priorityid WHERE userid = %s AND typeId = %s ORDER BY taskpriority.priorityid ASC,taskstatus.statusid DESC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def getSanitizedDeadlineData(session,typeId):
        data = (session,typeId)
        query = """SELECT TaskName,deadline,statusname,taskid FROM Tasks INNER JOIN TaskStatus ON Tasks.statusId = TaskStatus.statusId WHERE userId = %s AND typeId = %s ORDER BY deadline ASC,taskstatus.statusid DESC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def getSanitizedStatusData(session,typeId):
        data = (session,typeId)
        query = """SELECT taskname,statusname,deadline,taskid FROM tasks INNER JOIN taskstatus on tasks.statusid = taskstatus.statusid WHERE userid = %s AND typeid = %s ORDER BY taskstatus.statusid ASC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def sanitizedInsertTask(taskOwner,taskPriority,taskType,taskStatus,taskName,taskDeadline):
        data = (taskOwner,priorityDict[taskPriority],typeDict[taskType],statusDict[taskStatus],taskName,taskDeadline,)
        query = """INSERT INTO Tasks(userId,priorityId,typeId,statusId,taskName,deadline) VALUES (%s,%s,%s,%s,%s,%s)"""

        cursor.execute(query,data)
        connection.commit()

    def sanitizedUpdateTask(taskname,taskpriority,taskstatus,tasktype,taskdeadline,taskid):
        data = (taskname,priorityDict[taskpriority],statusDict[taskstatus],typeDict[tasktype],taskdeadline,taskid)
        query = """UPDATE Tasks SET taskname = %s, priorityid = %s, statusid = %s, typeid = %s, deadline = %s WHERE taskid = %s"""

        cursor.execute(query,data)
        connection.commit()
        

        



    @staticmethod
    def sanitizedInsertUser(username,password):
        data = (username,password)
        query = """INSERT INTO Users(username,HashedPassword) VALUES (%s,%s)""" #PREVENT SQL INJECTION

        try:
            cursor.execute(query,data)
        except mysql.connector.errors.IntegrityError:
            Utilities.duplicateUser()
            return False
        connection.commit()

        return True

    @staticmethod
    def getSanitizedTaskName(taskid):
        data = (taskid,)
        query = """SELECT taskname FROM tasks WHERE taskid = %s"""
        cursor.execute(query,data)
        result = cursor.fetchall()

        return result[0][0]
    
    @staticmethod
    def sanitizedLogin(username,password):
        data = (username,)
        query = """SELECT userId,HashedPassword FROM Users WHERE username=%s"""
        
        cursor.execute(query,data)
        result = cursor.fetchall()
        
        try:
            cookie = result[0][0]
            bcryptPassword = result[0][1]
            print(result[0][0],result[0][1])
        except IndexError:
            Utilities.invalidCredentials()

        try:
            verified = bcrypt.checkpw(password.encode('utf-8'),bcryptPassword.encode('utf-8'))
        
            if verified:
                return cookie
            else:
                Utilities.invalidCredentials()
        except UnboundLocalError:
            pass
        except ValueError:
            pass

    @staticmethod
    def getUsername(uid):
        data = (uid,)
        query = """SELECT username FROM Users WHERE userId = %s"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        
        return result[0][0]

        
        
class Utilities:
    def confirmLogout():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to logout?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        response = msg.exec_()

        if response == QMessageBox.Yes: #goback
            loginPage = Login()
            widget.addWidget(loginPage)
            widget.setFixedWidth(480)
            widget.setFixedHeight(600)
            widget.setCurrentIndex(widget.currentIndex() + 1) 
        else:
            print("User canceled logout.")

    @staticmethod
    def successfulAction():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Action Successful")
        msg.setText("Your action was successful!")
        msg.setInformativeText("Everything was processed correctly.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def duplicateUser():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Account Creation Error")
        msg.setText("Error: User already exists.")
        msg.setInformativeText("Try a different username")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    @staticmethod
    def invalidCredentials():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Invalid Credentials")
        msg.setText("Error: Username Or Password Mismatch")
        msg.setInformativeText("Try Again!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

app = QApplication([])
widget = QtWidgets.QStackedWidget()

gui = Login()

widget.addWidget(gui)
widget.setFixedWidth(480)
widget.setFixedHeight(600)

widget.show()
app.exec_()

