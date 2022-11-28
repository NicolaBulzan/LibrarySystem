from PyQt5.QtWidgets import *
import MySQLdb
from PyQt5.uic import loadUiType
from xlrd import *

ui, _ = loadUiType('library.ui')


class MainApp(QMainWindow, ui):
   def __init__(self):
       QMainWindow.__init__(self)
       self.setupUi(self)
       self.UI_Changes()
       self.Buttons()

       self.ShowAuthor()
       self.ShowCategory()
       self.ShowPublisher()

       self.ShowCategoryCombobox()
       self.ShowAuthorCombobox()
       self.ShowPublisherCombobox()

   def UI_Changes(self):
       self.tabWidget.tabBar().setVisible(False)

   def Buttons(self):

       self.pushButton_5.clicked.connect(self.OpenBooksTab)
       self.pushButton_6.clicked.connect(self.OpenUsersTab)
       self.pushButton_7.clicked.connect(self.OpenSettingsTab)

       self.pushButton_4.clicked.connect(self.AddBook)
       self.pushButton_8.clicked.connect(self.SearchBook)
       self.pushButton_3.clicked.connect(self.EditBook)
       self.pushButton_9.clicked.connect(self.DeleteBook)

       self.pushButton_13.clicked.connect(self.AddCategory)
       self.pushButton_14.clicked.connect(self.AddAuthor)
       self.pushButton_15.clicked.connect(self.AddPublisher)

       self.pushButton_10.clicked.connect(self.AddUser)
       self.pushButton_11.clicked.connect(self.Login)
       self.pushButton_12.clicked.connect(self.EditUser)

   def Open_Day_To_Day_Tab(self):
       self.tabWidget.setCurrentIndex(0)

   def OpenBooksTab(self):
       self.tabWidget.setCurrentIndex(1)

   def OpenUsersTab(self):
       self.tabWidget.setCurrentIndex(2)

   def OpenSettingsTab(self):
       self.tabWidget.setCurrentIndex(3)

   def AddBook(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       bookTitle = self.lineEdit_6.text()
       bookDescription = self.textEdit_2.toPlainText()
       bookCode = self.lineEdit_5.text()
       bookCategory = self.comboBox_7.currentIndex()
       bookAuthor = self.comboBox_6.currentIndex()
       bookPublisher = self.comboBox_8.currentIndex()
       bookPrice = self.lineEdit_7.text()

       self.cur.execute('''
            INSERT INTO book(book_name,bookDescription,bookCode,bookCategory,bookAuthor,bookPublisher,bookPrice)
            VALUES (%s , %s , %s , %s , %s , %s , %s)
        ''', (bookTitle, bookDescription, bookCode, bookCategory, bookAuthor, bookPublisher, bookPrice))

       self.db.commit()
       self.statusBar().showMessage('New Book Added')

       self.lineEdit_6.setText('')
       self.textEdit_2.setPlainText('')
       self.lineEdit_5.setText('')
       self.comboBox_6.setCurrentIndex(0)
       self.comboBox_7.setCurrentIndex(0)
       self.comboBox_8.setCurrentIndex(0)
       self.lineEdit_7.setText('')

   def SearchBook(self):

       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       bookTitle = self.lineEdit_2.text()

       sql = ''' SELECT * FROM book WHERE book_name = %s'''
       self.cur.execute(sql, [(bookTitle)])

       data = self.cur.fetchone()

       self.lineEdit_8.setText(data[1])
       self.textEdit.setPlainText(data[2])
       self.lineEdit_3.setText(data[3])
       self.comboBox_3.setCurrentIndex(data[4])
       self.comboBox_4.setCurrentIndex(data[5])
       self.comboBox_5.setCurrentIndex(data[6])
       self.lineEdit_4.setText(str(data[7]))

   def EditBook(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       bookTitle = self.lineEdit_8.text()
       bookDescription = self.textEdit.toPlainText()
       bookCode = self.lineEdit_3.text()
       bookCategory = self.comboBox_3.currentIndex()
       bookAuthor = self.comboBox_4.currentIndex()
       bookPublisher = self.comboBox_5.currentIndex()
       bookPrice = self.lineEdit_4.text()
       search_bookTitle = self.lineEdit_2.text()

       self.cur.execute('''
           UPDATE book SET book_name=%s ,bookDescription=%s ,bookCode=%s ,bookCategory=%s ,bookAuthor=%s ,bookPublisher=%s ,bookPrice=%s WHERE book_name = %s
       ''', (bookTitle, bookDescription, bookCode, bookCategory, bookAuthor, bookPublisher, bookPrice,
             search_bookTitle))

       self.db.commit()
       self.statusBar().showMessage('book updated')

   def DeleteBook(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       bookTitle = self.lineEdit_2.text()

       warning = QMessageBox.warning(self, 'Delete Book', "are you sure you want to delete this book",
                                     QMessageBox.Yes | QMessageBox.No)
       if warning == QMessageBox.Yes:
           sql = ''' DELETE FROM book WHERE book_name = %s '''
           self.cur.execute(sql, [(bookTitle)])
           self.db.commit()
           self.statusBar().showMessage('Book Deleted')

   def AddUser(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       username = self.lineEdit_9.text()
       email = self.lineEdit_10.text()
       password = self.lineEdit_11.text()
       passwordDuplicate = self.lineEdit_12.text()

       if password == passwordDuplicate:
           self.cur.execute('''
               INSERT INTO users(user_name , user_email , user_password)
               VALUES (%s , %s , %s)
           ''', (username, email, password))

           self.db.commit()
           self.statusBar().showMessage('New User Added')

       else:
           self.label_29.setText('please add a valid password twice')

   def Login(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       username = self.lineEdit_14.text()
       password = self.lineEdit_13.text()

       sql = ''' SELECT * FROM users'''

       self.cur.execute(sql)
       data = self.cur.fetchall()
       for row in data:
           if username == row[1] and password == row[3]:
               print('user match')
               self.statusBar().showMessage('Valid Username & Password')
               self.groupBox_3.setEnabled(True)

               self.lineEdit_16.setText(row[1])
               self.lineEdit_15.setText(row[2])
               self.lineEdit_17.setText(row[3])

   def EditUser(self):

       username = self.lineEdit_16.text()
       email = self.lineEdit_15.text()
       password = self.lineEdit_17.text()
       passwordDuplicate = self.lineEdit_18.text()

       originalName = self.lineEdit_14.text()

       if password == passwordDuplicate:
           self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
           self.cur = self.db.cursor()

           print(username)
           print(email)
           print(password)

           self.cur.execute('''
                UPDATE users SET user_name=%s , user_email=%s , user_password=%s WHERE user_name=%s
            ''', (username, email, password, originalName))

           self.db.commit()
           self.statusBar().showMessage('User Data Updated Successfully')

   def AddCategory(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       category_name = self.lineEdit_19.text()

       self.cur.execute('''
           INSERT INTO category (category_name) VALUES (%s)
       ''', (category_name,))
       self.db.commit()
       self.statusBar().showMessage('New category was added')
       self.lineEdit_19.setText('')
       self.ShowCategory()
       self.ShowCategoryCombobox()

   def AddAuthor(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()
       author_name = self.lineEdit_20.text()
       self.cur.execute('''
            INSERT INTO authors (author_name) VALUES (%s)
        ''', (author_name,))
       self.db.commit()
       self.lineEdit_20.setText('')
       self.statusBar().showMessage('Added')
       self.ShowAuthor()
       self.ShowAuthorCombobox()

   def AddPublisher(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       publisher_name = self.lineEdit_21.text()
       self.cur.execute('''
           INSERT INTO publisher (publisher_name) VALUES (%s)
       ''', (publisher_name,))

       self.db.commit()
       self.lineEdit_21.setText('')
       self.statusBar().showMessage('New publisher was added')
       self.ShowPublisher()
       self.ShowPublisherCombobox()

   def ShowCategory(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       self.cur.execute(''' SELECT category_name FROM category''')
       d = self.cur.fetchall()

       if d:
           self.tableWidget_2.setRowCount(0)
           self.tableWidget_2.insertRow(0)
           for row, form in enumerate(d):
               for column, item in enumerate(form):
                   self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                   column += 1

               row_pos = self.tableWidget_2.rowCount()
               self.tableWidget_2.insertRow(row_pos)

   def ShowAuthor(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       self.cur.execute(''' SELECT author_name FROM authors''')
       d = self.cur.fetchall()

       if d:
           self.tableWidget_3.setRowCount(0)
           self.tableWidget_3.insertRow(0)
           for row, form in enumerate(d):
               for column, item in enumerate(form):
                   self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                   column += 1

               row_pos = self.tableWidget_3.rowCount()
               self.tableWidget_3.insertRow(row_pos)

   def ShowPublisher(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       self.cur.execute(''' SELECT publisher_name FROM publisher''')
       d = self.cur.fetchall()

       if d:
           self.tableWidget_4.setRowCount(0)
           self.tableWidget_4.insertRow(0)
           for row, form in enumerate(d):
               for column, item in enumerate(form):
                   self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                   column += 1

               row_pos = self.tableWidget_4.rowCount()
               self.tableWidget_4.insertRow(row_pos)

   def ShowCategoryCombobox(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       self.cur.execute(''' SELECT category_name FROM category ''')
       d = self.cur.fetchall()

       self.comboBox_3.clear()
       for categ in d:
           self.comboBox_3.addItem(categ[0])
           self.comboBox_7.addItem(categ[0])

   def ShowAuthorCombobox(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       self.cur.execute(''' SELECT author_name FROM authors''')
       d = self.cur.fetchall()

       self.comboBox_4.clear()
       for a in d:
           self.comboBox_4.addItem(a[0])
           self.comboBox_6.addItem(a[0])

   def ShowPublisherCombobox(self):
       self.db = MySQLdb.connect(host='localhost', user='root', password='1234', db='library')
       self.cur = self.db.cursor()

       self.cur.execute(''' SELECT publisher_name FROM publisher''')
       d = self.cur.fetchall()

       self.comboBox_5.clear()
       for publisher in d:
           self.comboBox_5.addItem(publisher[0])
           self.comboBox_8.addItem(publisher[0])


def main():
   app = QApplication(sys.argv)
   window = MainApp()
   window.show()
   app.exec_()


if __name__ == '__main__':
   main()

