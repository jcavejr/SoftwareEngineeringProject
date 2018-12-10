# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:34:27 2018

@author: John Carter and Dominic Scola
(John's copy)
"""
import re
import mysql.connector
from mysql.connector import errorcode

class se_db:

    config = {
    'user': 'debian-sys-maint',
    'password': 'pR5hJsvCW37Z4Ude',
    'host': '127.0.0.1',
    'database': 'test',
    }

    def __init__(self):
        self.connection =  mysql.connector.connect(**se_db.config)
        self.cursor = self.connection.cursor()

    '''
    Class Functions
    '''

    def listClasses(self):
        '''
        Lists all classes in the class table
        @return: a list of class names
        '''
        query = """SELECT class_name FROM test.class"""
        try:
            self.cursor.execute(query)
        except:
            return "Error: Unable to list classes"
        classList = []
        for (class_name) in self.cursor:
            names = len(class_name)
            for (i) in range(names):
                classList.append(class_name[i])
        return classList

    def addClass(self, name, subject, color, userList, school = "Rutgers Camden"):
        '''
        Adds a class to the class table
        @params: name of class, field of study, color, and list of users (a string)
        @return: Error/Success message
        '''
        query = """SELECT COUNT(*) FROM test.class WHERE class_name = '%s'""" % (name)
        try:
            self.cursor.execute(query)
            for (count) in self.cursor:
                if count[0] > 0:
                    return "Error: Class already exists in database"
        except:
            return "Error: Unable to execute query"
        queryInsert = """INSERT INTO test.class (class_name, subject, color, school, list_of_users) VALUES ('%s','%s','%s','%s','%s')""" % (name, subject, color, school, userList)
        try:
            self.cursor.execute(queryInsert)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(err)
            return "Error: Unable to insert class into database"
        return "Successfully added class to database"

    def checkClassColor(self, className):
        '''
        Finds the class color for the class name passed in
        @param 'className': class name to check color
        @return: the class' color
        '''
        querySelect = """SELECT color FROM test.class WHERE class_name = '%s'""" % (className)
        try:
            self.cursor.execute(querySelect)
        except:
            return "Error: Unable to execute query"
        for (color) in self.cursor:
            return color

    def listClassesInSubject(self, subject):
        '''
        Lists all classes in a specific field of study
        @param 'subject': a field of study to list classes
        @return: a list of class names
        '''
        query = """SELECT class_name FROM test.class WHERE subject = '%s'""" % (subject)
        try:
            self.cursor.execute(query)
        except:
            return "Error: Unable to list classes"
        classList = []
        for (class_name) in self.cursor:
            names = len(class_name)
            for (i) in range(names):
                classList.append(class_name[i])
        return classList

    def classList(self, className):
        '''
        Lists all users in a specific class
        @param 'className': name of class to list roster
        @return: a list of users 
        '''
        query = """SELECT list_of_users FROM test.class WHERE class_name = '%s'""" % (className)
        try:
            self.cursor.execute(query)
        except:
            return "Error: Unable to list users"
        for (list_of_users) in self.cursor:
            return list_of_users
        
    def classCount(self, className):
        '''
        Returns the number of users in a class
        @param 'className': name of class to find number of students
        @return: number of students in the class
        '''
        query = """SELECT list_of_users FROM test.class WHERE class_name = '%s'""" % (className)
        try:
            self.cursor.execute(query)
        except:
            return "Error: Unable to list users"
        for (list_of_users) in self.cursor:
            userList = str(list_of_users)
            userList = userList.strip(',')
            userList = userList.split(' ')
        return len(userList)        

    def addUserToClass(self, email, className):
        '''
        Adds another user to an existing class
        @params: email of new user, class to add user to
        @return: updated list of users in class
        '''
        query = """SELECT list_of_users FROM test.class WHERE class_name = '%s'""" % (className)
        try:
            self.cursor.execute(query)
        except:
            return "Error: Unable to list users"
        for (list_of_users) in self.cursor:
            list_of_users = str(list_of_users)
            list_of_users = re.sub("[()']","", list_of_users)
            userList = list_of_users + email
            self.cursor.execute("""UPDATE test.class SET list_of_users = %s WHERE class_name = %s""", 
                    (userList, className))
            self.connection.commit()
        query1 = """SELECT list_of_classes FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(query1)
        except errorcode.Error as err:
            print(err)
            return "Error: Unable to list users"
        for (list_of_classes) in self.cursor:
            list_of_classes = str(list_of_classes)
            list_of_classes = re.sub("[()']","", list_of_classes)
            classList = list_of_classes+className
            self.cursor.execute("""UPDATE test.profiles SET list_of_classes = %s WHERE email = %s""",
                    (classList, email))
            self.connection.commit()
        return userList, classList 

    '''
    Profile functions below
    '''

    def addProfile(self, email, password, first, last, school = "Rutgers Camden"):
        queryCheck = """SELECT COUNT(*) FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(queryCheck)
            for (count) in self.cursor:
                if count[0] > 0:
                    return "Error: Email already exists in database"
        except:
            return "Error: Unable to execute query"
        queryInsert = """INSERT INTO test.profiles (email, password, first, last, school, upvotes, active_flag) VALUES ('%s','%s','%s','%s','%s', 0, 1)""" % (email, password, first, last, school)
        try:
            self.cursor.execute(queryInsert)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(err)
            return "Error: Unable to insert user into database"
        return "Successfully added user to database"

    def checkProfileCredentials(self, email, password):
        queryCheck = """SELECT COUNT(*) FROM test.profiles WHERE email = '%s' AND password = '%s'""" % (email, password)
        try:
            self.cursor.execute(queryCheck)
        except:
            return "Error: Incorrect credentials"
        for (count) in self.cursor:
            if count[0] == 1:
                return "Successful credentials"
            else:
                return "Error: Incorrect credentials"
    def getProfileName(self, email):
        querySelect = """SELECT first, last FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(querySelect)
        except:
            return "Error: Unable to execute query"
        for (first, last) in self.cursor:
            return first+" "+last

    def getProfileSchool(self, email):
        querySelect = """SELECT school FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(querySelect)
        except:
            return "Error: Unable to execute query"
        for (school) in self.cursor:
            return school[0]

    def getProfileUpvotes(self, email):
        querySelect = """SELECT upvotes FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(querySelect)
        except:
            return "Error: Unable to execute query"
        for (upvotes) in self.cursor:
            return upvotes[0]

#    def addThread(self, email, thread_title, post):
#        queryCheck = """SELECT COUNT(*) FROM se_database.threads WHERE email = '%s' AND thread_title = '%s' AND post = '%s'""" % (email, thread_title, post)
#        try:
#            self.cursor.execute(queryCheck)
#            for (count) in self.cursor:
#                if count[0] > 0:
#                    thread_title = "[DUPLICATE " + count[0] + "] - " + thread_title
#        except:
#            return "Error: Unable to execute query"
#        queryInsert = """INSERT INTO se_database.threads (email, date, thread_title, post, upvotes) VALUES ('%s', SYSDATE(), '%s', '%s', 0)""" % (email, thread_title, post)
#        try:
#            self.cursor.execute(queryInsert)
#            self.connection.commit()
#        except:
#            return "Error: Unable to execute query"
#        return "Successfully added thread to database"
#
#    def getThreadTitlesByUser(self, email):
#        query = """SELECT thread_title FROM se_database.threads WHERE email = '%s'""" % (email)
#        try:
#            self.cursor.execute(query)
#        except:
#            return "Error: Unable to execute query"
#        threadResults = []
#        for (thread_title) in self.cursor:
#            threads = len(thread_title)
#            for (temp) in range(threads):
#                threadResults.append(thread_title[temp])
#   def getThreadId(self, email, thread_title):
#        querySelect = """SELECT thread_id FROM se_database.threads WHERE email = '%s' AND thread_title = '%s'""" % (email, thread_title)
#        try:
#            self.cursor.execute(querySelect)
#        except:
#            return "Error: Unable to execute query"
#        for (thread_id) in self.cursor:
#            return thread_id[0]
#
#    def getThreadPost(self, thread_id):
#        querySelect = """SELECT post FROM se_database.threads WHERE thread_id = '%d'""" % (thread_id)
#        try:
#            self.cursor.execute(querySelect)
#        except:
#            return "Error: Unable to execute query"
#        for (post) in self.cursor:
#            return post[0]
#
#    def getThreadUpvotes(self, thread_id):
#        querySelect = """SELECT upvotes FROM se_database.threads"""
#        try:
    def closeConnection(self):
        self.cursor.close()
        self.connection.close()
