from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QLineEdit,QGridLayout,QMainWindow,QMessageBox,QTextEdit, QDialog,QTableWidget
from PyQt5.QtGui import QFont, QGuiApplication
from PyQt5.uic import loadUi
import mysql.connector
import bcrypt

#DATABASE CONFIGURATION
connection = mysql.connector.connect(host="localhost",database="cc15",user="root",password="root")
cursor = connection.cursor(prepared=True)

#CREATE ELISTA ADD PAGE
class ElistaAddOperation(QDialog):
    def __init__(self,session):
        super().__init__()
        self.session = session
        loadUi("elistaAdd.ui",self)

        #task adder functionality here
        self.addTaskSubmitBox.clicked.connect(self.addTask)
        self.taskAdderReturn.clicked.connect(self.returnToMainPage)

    def returnToMainPage(self):
        loggedIn = ElistaMainPage(self.session)
        widget.addWidget(loggedIn)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1400)
        widget.setFixedHeight(800)

    def addTask(self):
        taskOwner = self.session
        taskPriority = self.addTaskPriorityBox.currentText()
        taskType = self.addTaskTypeBox.currentText()
        taskStatus = "Pending"
        taskName = self.taskNameField.toPlainText()
        taskDeadline = self.addTaskDeadlineBox.date().toString("yyyy-MM-dd")

        #TASK NAME MUST NOT BE EMPTY

        Database.sanitizedInsertTask(taskOwner,taskPriority,taskType,taskStatus,taskName,taskDeadline)

        Utilities.successfulAction()

class ElistaEditOperation(QDialog):
    def __init__(self,session,taskId):
        super().__init__()
        self.session = session
        self.taskId = taskId
        loadUi("elistaUpdate.ui",self)

        self.reviseTaskId.setText(str(taskId))
        self.reviseNameBox.setText(Database.getSanitizedTaskName(self.taskId))
        
        self.reviseCancelButton.clicked.connect(self.returnToMainPage)
        self.reviseDiscardButton.clicked.connect(self.removeTask)

        self.reviseUpdateButton.clicked.connect(self.updateTask)



    #MAKE UPDATE
    def updateTask(self):
        updateName = self.reviseNameBox.text()
        updatePriority = self.revisePriorityBox.currentText()
        updateStatus = self.reviseStatusBox.currentText()
        updateType = self.reviseTypeBox.currentText()
        updateDeadline = self.reviseDeadlineBox.date().toString("yyyy-MM-dd")

        Database.sanitizedUpdateTask(updateName,updatePriority,updateStatus,updateType,updateDeadline,self.taskId)

        Utilities.successfulAction()

        loggedIn = ElistaMainPage(self.session)
        widget.addWidget(loggedIn)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1400)
        widget.setFixedHeight(800)



    def returnToMainPage(self):
        loggedIn = ElistaMainPage(self.session)
        widget.addWidget(loggedIn)
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
        self.secondAuthenticatedButton.clicked.connect(self.dynamicButton)
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

        self.academicTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.academicTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.academicTable.verticalHeader().setVisible(False)

        self.miscTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.miscTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.miscTable.verticalHeader().setVisible(False)

        #CREATE CLICK TABLE ROW EVENT

        self.personalTable.cellDoubleClicked.connect(self.rowClickEventOne)
        self.academicTable.cellDoubleClicked.connect(self.rowClickEventTwo)
        self.miscTable.cellDoubleClicked.connect(self.rowClickEventThree)


    def rowClickEventOne(self, row, column):
        row_data = []
        for col in range(self.personalTable.columnCount()):
            item = self.personalTable.item(row, col)
            row_data.append(item.text() if item else "")
        #CREATE A DELETER AND UPDATER HERE


        #(self,session,taskId)
        
        edit = ElistaEditOperation(self.session,row_data[3]) 
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
        
        edit = ElistaEditOperation(self.session,row_data[3]) 
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
        
        edit = ElistaEditOperation(self.session,row_data[3]) 
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
            
            
            

          


        








    def dynamicButton(self):
        pressed = self.sender()

        if pressed == self.firstAuthenticatedButton:
            #DEFAULT SCREEN, VIEW ALL DATA
            print("first")
            


        elif pressed == self.secondAuthenticatedButton: #GOBACK HERE

            #make a CREATE READ UPDATE CLASS. MAKE THIS ONE FIRST
            crud = ElistaAddOperation(self.session)
            widget.setFixedWidth(480)
            widget.setFixedHeight(600)
            widget.addWidget(crud)
            widget.setCurrentIndex(widget.currentIndex() + 1) 


        elif pressed == self.thirdAuthenticatedButton:
            print("third") #CALENDAR HERE

        elif pressed == self.fourthAuthenticatedButton:
            #TO-DO LIST, MAKE A PROMPT THAT ASKS A YES OR NO QUESTION TO CONTINUE LOG OUT OR NOT

            loginPage = Login()
            widget.addWidget(loginPage)
            widget.setFixedWidth(480)
            widget.setFixedHeight(600)
            widget.setCurrentIndex(widget.currentIndex() + 1) 
























class Login(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui",self)
        self.LoginSubmitButton.clicked.connect(self.authenticate)
        self.LoginPasswordForm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createAccountButton.clicked.connect(self.visitSignupPage)
    
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
    "Academic": 2,
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
        query = """SELECT TaskName,deadline,statusname,taskid FROM Tasks LEFT JOIN TaskStatus ON Tasks.statusId = TaskStatus.statusId WHERE userId = %s AND typeId = %s ORDER BY deadline ASC,taskstatus.statusid DESC"""
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

