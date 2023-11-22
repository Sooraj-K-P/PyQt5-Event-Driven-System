import os
import re
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTime
from pynput import keyboard
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QTimeEdit
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QTimeEdit

if os.path.exists("tracker.txt"):
    f = open("tracker.txt", "a")
else:
    f = open("tracker.txt", "x")
print(os)

class WelcomeScreen(QDialog):
    close_window_signal = pyqtSignal()

    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)
        self.exit.clicked.connect(sys.exit)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goBack(self):
        create = WelcomeScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui", self)

        # Set the echo mode for the password fields to password mode
        self.passwordfield.setEchoMode(QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QLineEdit.Password)

        # Connect the buttons to the respective functions
        self.signup.clicked.connect(self.signupfunction)
        self.back.clicked.connect(self.goBack)
        self.show_pass_1.clicked.connect(self.show_pass)
        self.show_pass_2.clicked.connect(self.show_pass)

    def signupfunction(self):
        username = self.username.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
        email = self.email.text()
        phone = self.phone.text()

        # Define regular expressions for the username and password rules
        username_pattern = re.compile("[A-Z][a-z]+")
        password_pattern = re.compile("^(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$")

        if len(username) == 0 or len(password) == 0 or len(confirmpassword) == 0 or len(email) == 0 or len(phone) == 0:
            message = QMessageBox()
            message.setText("Please fill in all inputs.")
            message.exec_()
        elif password != confirmpassword:
            message = QMessageBox()
            message.setText("Passwords do not match.")
            message.exec_()
        elif not username_pattern.match(username):
            message = QMessageBox()
            message.setText("Username must begin with a capital letter followed by lowercase letters.")
            message.exec_()
        elif not password_pattern.match(password):
            message = QMessageBox()
            message.setText("Password must contain at least one uppercase letter, one number, and one special character, and be at least 8 characters long.")
            message.exec_()
        else:
            # Add the user information to the database
            conn = mysql.connector.connect(
                host="localhost",
                user="trackeradmin",
                password="trackpass",
                database="trackerrose",
            )
            cur = conn.cursor()
            user_info = [username, password, email, phone]
            cur.execute('INSERT INTO UserDetails (username, password , email , phone ) VALUES (%s, %s, %s , %s )', user_info)
            conn.commit()
            conn.close()

            # Show a message box indicating that the user was created successfully
            message = QMessageBox()
            message.setText("Created Successfully Kindly log in")
            message.exec_()

            # Navigate to the login screen
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def goBack(self):
        # Navigate back to the welcome screen
        create = WelcomeScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_pass(self):
        if self.show_pass_1.isChecked():
            self.passwordfield.setEchoMode(QLineEdit.Normal)
        elif self.show_pass_2.isChecked():
            self.confirmpasswordfield.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordfield.setEchoMode(QLineEdit.Password)
            self.confirmpasswordfield.setEchoMode(QLineEdit.Password)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui", self)
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.back.clicked.connect(self.goBack)
        self.show_password.clicked.connect(self.show_pass)

        # mysql db connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose",
        )

        self.current_username = None

    def loadscreen(self):
        create = TrackingScreen(current_username=self.current_username, login_screen=self, parent=self)
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def loginfunction(self):
        user = self.emailfield.text()
        password = self.password_field.text()

        if len(user) == 0 or len(password) == 0:
            message = QMessageBox()
            message.setText("Please fill in all inputs.")
            message.exec_()
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="trackeradmin",
                password="trackpass",
                database="trackerrose",
            )
            cur = conn.cursor()
            query = 'SELECT password FROM UserDetails WHERE username =\'' + user + "\'"
            cur.execute(query)
            result = cur.fetchone()
            if result is not None:
                result_pass = result[0]
                if result_pass == password:
                    print("Successfully logged in.")
                    self.loadscreen()
                    self.current_username = user
                else:
                    print('error')
                    message = QMessageBox()
                    message.setText("Invalid inputs.")
                    message.exec_()
            else:
                print('error')
                message = QMessageBox()
                message.setText("Invalid username.")
                message.exec_()

    def goBack(self):
        create = WelcomeScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_pass(self):
        if self.show_password.isChecked():
            self.password_field.setEchoMode(QLineEdit.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.Password)

class TrackingScreen(QtWidgets.QDialog):            
    def __init__(self, current_username, login_screen, parent=None):
        super(TrackingScreen, self).__init__(parent=parent)
        self.login_screen = login_screen
        self.current_username = current_username
        self.id = 1 
        
        loadUi("tracking.ui", self)
        self.login_screen = login_screen
        self.current_username = current_username
        self.stoptracker_button.clicked.connect(self.stop_tracking)
        self.startbutton.clicked.connect(self.on_clicked)
        self.refresh_button.clicked.connect(self.refresh)
        self.logout_ext_but.clicked.connect(QtWidgets.qApp.quit)
        self.consecutive_space_count = 0
        self.MAX_CONSECUTIVE_SPACES = 7
        self.listener = None
        

        self.special_keys = {
            keyboard.Key.space: 'Space',
            keyboard.Key.shift: 'Shift',
            # Add more special keys as needed
        }
    

        # current time
        self.set_time.setText("")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        # current date
        self.set_date.setText("")
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.update_date)
        self.timer2.start(1000)  # Update every second

        # mysql db connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose",
        )

        cur = self.conn.cursor()
        cur.execute("SELECT username FROM UserDetails WHERE username = %s", (current_username,))
        result = cur.fetchone()
        user = result
        # ...
        cur.close()
       
        with open('tracker.txt', 'r') as file:
            file_contents = file.read()
        self.TextEdit.setPlainText(file_contents)
        
    def update_time(self):
        # Get the current time and format it as desired
        current_time = datetime.now().strftime('%I:%M:%S %p')
        self.set_time.setText(current_time)

    def update_date(self):
        # Get the current date and format it as desired
        current_date = datetime.now().strftime('%d-%m-%Y')
        self.set_date.setText(current_date)

    def refresh(self):
        self.update_text()
  
    def on_clicked(self):
        if self.listener is None:
            self.db_connections()
            # Define file object to write to
            with open('tracker.txt', 'a') as f:
                self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.date = datetime.now().date()
                print(self.date)
                print(self.start_time)
                self.key_pressed = list()
                self.alphanumeric_key_count = 0
                self.special_key_count = 0

                # Start the keyboard listener
                self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
                self.listener.start()

            # Hide the "Start Tracker" button after it is pressed
            self.startbutton.hide()
            self.stoptracker_button.show()
                  
    def key_to_string(self, key):
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.space:
                return "Space"
            elif key == keyboard.Key.backspace:
                return "Backspace"
            elif key == keyboard.Key.enter:
                return "Enter"
            else:
                key_str = str(key)
                return key_str.split('.')[-1]
        elif isinstance(key, keyboard.KeyCode):
            if hasattr(key, 'char'):
                if key.char == '5':
                    return '5'
                return key.char
            else:
                return key.char  # Return an empty string for cases where key.char is None
        else:
            return ""

    def on_press(self, key):
        # Handle key press event
        with open('tracker.txt', 'a') as f:
            try:
                if key == keyboard.Key.space:
                    self.consecutive_space_count += 1
                    if self.consecutive_space_count >= self.MAX_CONSECUTIVE_SPACES:
                        text = "\n"  # Write a newline character
                        self.consecutive_space_count = 0
                    else:
                        text = " "
                elif key == keyboard.KeyCode.from_char('5'):
                    text = "5"
                    self.consecutive_space_count = 0
                else:
                    text = "{0}".format(self.key_to_string(key))  # Convert key to string without quotes
                    self.consecutive_space_count = 0

                self.alphanumeric_key_count += 1
                f.write(text)  # Use write() instead of writelines() for single strings
                self.key_pressed.append(text)  # Append the entire text
            except AttributeError:
                text = "special key {0}".format(self.key_to_string(key))  # Write the key without the 'pressed' message
                f.write(text)
                self.special_key_count += 1
                f.flush()
                self.key_pressed.append(text)  # Append the entire text
    
    def on_release(self, key):
        # Handle key release event
        with open('tracker.txt', 'a') as f:
            text = "{0}  ".format(key)
            # f.writelines(f'{text}')
            f.flush()
            self.key_pressed.append(text)
            
    def db_connections(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose"
        )
        self.mycursor = self.mydb.cursor()
        
    def db_insertion(self):
        try:
            # Reconnect to the database if the connection is closed
            if not self.mydb.is_connected():
                self.mydb.reconnect()

            # Create a new cursor if it's not already created
            if not self.mycursor:
                self.mycursor = self.mydb.cursor()

            # Execute the insertion query
            sql = """INSERT INTO TrackerSummary (date, start_time, end_time, total_alphanumeric_keys, total_special_keys, user_id) VALUES (%s,%s,%s,%s,%s,%s)"""
            self.mycursor.execute(sql, (
                self.date, self.start_time, self.end_time, self.alphanumeric_key_count, self.special_key_count, self.id))
            self.mydb.commit()

            summery_id = self.mycursor.lastrowid
            details_row = [(keys, summery_id) for keys in self.key_pressed]

            if details_row:
                sql = """INSERT INTO TrackerDetails (Keys_pressed, summary_id) VALUES (%s,%s)"""
                self.mycursor.executemany(sql, details_row)
                self.mydb.commit()

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:
            # Close the cursor after execution
            if self.mycursor:
                self.mycursor.close()

            # Close the database connection after execution
            if self.mydb.is_connected():
                self.mydb.close()
                
    def stop_tracking(self):
        if self.listener is not None:
            # Stop the keyboard listener
            self.listener.stop()
            self.listener.join()  # Wait for the listener to completely stop

            # Continue with the existing code
            self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.db_insertion()

            # Clear the spaces between strings in the key_pressed list
            joined_text = ''.join(self.key_pressed)

            # Open the file and write the concatenated text
            with open('tracker.txt', 'a') as f:
                f.write(joined_text)

        # Clear the key_pressed list for the next tracking session
        self.key_pressed = []

        # Show the "Start Tracker" button and hide the "Stop Tracker" button
        self.startbutton.show()
        self.stoptracker_button.hide()

        # Set the listener to None to be able to start a new one
        self.listener = None
        
    def update_text(self):
        # Open the text file and read its contents
        with open('tracker.txt', 'r') as file:
            file_contents = file.read()

        # Set the contents of the QTextEdit widget to the contents of the text file
        self.TextEdit.setPlainText(file_contents)

    def time(self):
        time_edit = QTimeEdit()

        # Set the time to the current time
        current_time = QTime.currentTime()
        time_edit.setTime(current_time)

        # Show the widget
        time_edit.show()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
