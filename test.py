from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QVBoxLayout,QHBoxLayout,QLineEdit,QGridLayout,QMainWindow,QMessageBox,QTextEdit, QDialog
from PyQt5.QtGui import QFont
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
        loadUi("elistaDbOperationsAdd.ui",self)
        self.cNameOperationsLabel.setText(Database.getUsername(self.session))
        self.addAuthenticatedButton.clicked.connect(self.dbOperations)
        self.updateAuthenticatedButton.clicked.connect(self.dbOperations)
        self.returnAuthenticatedButton.clicked.connect(self.dbOperations)

        #task adder functionality here
        self.addTaskSubmitBox.clicked.connect(self.addTask)

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



    def dbOperations(self):
        pressed = self.sender()

        if pressed == self.addAuthenticatedButton:
            print("it works!")
            add = ElistaAddOperation(self.session)
            widget.addWidget(add)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        
        elif pressed == self.updateAuthenticatedButton:
            pass #ELISTA UPDATE PAGE
                
        elif pressed == self.returnAuthenticatedButton:
            print("it works!")
            EmainPage = ElistaMainPage(self.session)
            widget.addWidget(EmainPage)
            widget.setCurrentIndex(widget.currentIndex() + 1)

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
        #JUST COPY FOR ALL        

    #MAKE TABLE HERE
    def personalDynamicComboBoxes(self,sortBy):
        if sortBy == "Priority":
            self.personalTable.resizeRowsToContents()
            self.personalTable.setColumnCount(3)
            
            self.personalTable.setHorizontalHeaderLabels(["Task","Status","Priority"])

            priorityData = Database.getSanitizedPriorityData(self.session,1) 
            self.personalTable.setRowCount(len(priorityData))

            tableRow = 0

            for i in priorityData:
                print(i)
                self.personalTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
                self.personalTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
                self.personalTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
                tableRow += 1

        if sortBy == "Deadline":
            self.personalTable.resizeRowsToContents()
            self.personalTable.setColumnCount(3)
       
            self.personalTable.setHorizontalHeaderLabels(["Task","Deadline","Status"])

            deadlineData = Database.getSanitizedDeadlineData(self.session,1) 
            self.personalTable.setRowCount(len(deadlineData))

            tableRow = 0

            for j in deadlineData:
                print(j)
                self.personalTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.personalTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.personalTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                tableRow += 1
        
    def academicDynamicComboBoxes(self,sortBy):
        if sortBy == "Priority":
            self.academicTable.resizeRowsToContents()
            self.academicTable.setColumnCount(3)
            
            self.academicTable.setHorizontalHeaderLabels(["Task","Status","Priority"])

            priorityData = Database.getSanitizedPriorityData(self.session,2) 
            print(priorityData)
            self.academicTable.setRowCount(len(priorityData))

            tableRow = 0

            for i in priorityData:
                print(i)
                self.academicTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
                self.academicTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
                self.academicTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
                tableRow += 1
        
        if sortBy == "Deadline":
            self.academicTable.resizeRowsToContents()
            self.academicTable.setColumnCount(3)
       
            self.academicTable.setHorizontalHeaderLabels(["Task","Deadline","Status"])

            deadlineData = Database.getSanitizedDeadlineData(self.session,2) 
            self.academicTable.setRowCount(len(deadlineData))

            tableRow = 0

            for j in deadlineData:
                print(j)
                self.academicTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.academicTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.academicTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                tableRow += 1

    def miscDynamicComboBoxes(self,sortBy):
        if sortBy == "Priority":
            self.miscTable.resizeRowsToContents()
            self.miscTable.setColumnCount(3)
            
            self.miscTable.setHorizontalHeaderLabels(["Task","Status","Priority"])

            priorityData = Database.getSanitizedPriorityData(self.session,3) 
            print(priorityData)
            self.miscTable.setRowCount(len(priorityData))

            tableRow = 0

            for i in priorityData:
                print(i)
                self.miscTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(i[0])))
                self.miscTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(i[1])))
                self.miscTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(i[2])))
                tableRow += 1

        if sortBy == "Deadline":
            self.miscTable.resizeRowsToContents()
            self.miscTable.setColumnCount(3)
       
            self.miscTable.setHorizontalHeaderLabels(["Task","Deadline","Status"])

            deadlineData = Database.getSanitizedDeadlineData(self.session,2) 
            self.miscTable.setRowCount(len(deadlineData))

            tableRow = 0

            for j in deadlineData:
                print(j)
                self.miscTable.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(j[0])))
                self.miscTable.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(j[1])))
                self.miscTable.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(j[2])))
                tableRow += 1
            
            
            

          


        








    def dynamicButton(self):
        pressed = self.sender()

        if pressed == self.firstAuthenticatedButton:
            #DEFAULT SCREEN, VIEW ALL DATA
            print("first")
            


        elif pressed == self.secondAuthenticatedButton: #GOBACK HERE

            #make a CREATE READ UPDATE CLASS. MAKE THIS ONE FIRST
            crud = ElistaAddOperation(self.session)
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


class Database():
    @staticmethod
    def getSanitizedPriorityData(session,typeId):
        data = (session,typeId)
        query = """SELECT taskname,priorityname,statusname FROM tasks INNER JOIN taskstatus ON tasks.statusid = taskstatus.statusid INNER JOIN taskpriority ON tasks.priorityid = taskpriority.priorityid WHERE userid = %s AND typeId = %s ORDER BY taskpriority.priorityid ASC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def getSanitizedDeadlineData(session,typeId):
        data = (session,typeId)
        query = """SELECT TaskName,deadline,statusname FROM Tasks LEFT JOIN TaskStatus ON Tasks.statusId = TaskStatus.statusId WHERE userId = %s AND typeId = %s ORDER BY deadline ASC"""
        cursor.execute(query,data)
        result = cursor.fetchall()
        print(result)
        return result

    @staticmethod
    def sanitizedInsertTask(taskOwner,taskPriority,taskType,taskStatus,taskName,taskDeadline):
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
            "In progress": 3,
            "Pending": 4,
        }

        data = (taskOwner,priorityDict[taskPriority],typeDict[taskType],statusDict[taskStatus],taskName,taskDeadline,)
        query = """INSERT INTO Tasks(userId,priorityId,typeId,statusId,taskName,deadline) VALUES (%s,%s,%s,%s,%s,%s)"""

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

