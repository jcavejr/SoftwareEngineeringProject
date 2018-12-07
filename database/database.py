# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:34:27 2018

@author: John Carter and Dominic Scola
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
        except:
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
    
    def addMessage(self, new_thread_ind, reply_message_id, creator, title, post, class_name):
        if (new_thread_ind == 0):
            queryCheck = """SELECT COUNT(*) FROM test.message"""
            try:
                self.cursor.execute(queryCheck)
                for (count) in self.cursor:
                    if count[0] == 0:
                        queryInsert = """INSERT INTO test.message (message_id, date_time, creator, title, post, class, upvotes) VALUES (0, SYSDATE(), '%s', '%s', '%s', '%s', 0)""" % (creator, title, post, class_name)
                        try:
                            self.cursor.execute(queryInsert)
                            self.connection.commit()
                        except:
                            return "Error: Unable to insert message into database (1)"
                        return "Successfully added message into database"
                    else:
                        queryCheckNumber = """SELECT MAX(message_id) FROM test.message"""
                        try:
                            self.cursor.execute(queryCheckNumber)
                            for (message_id_new) in self.cursor:
                                queryInsertNewThread = """INSERT INTO test.message (message_id, date_time, creator, title, post, class, upvotes) VALUES ('%d', SYSDATE(), '%s', '%s', '%s', '%s', 0)""" % (message_id_new[0] + 1, creator, title, post, class_name)
                                try:
                                    self.cursor.execute(queryInsertNewThread)
                                    self.connection.commit()
                                except:
                                    return "Error: Unable to insert message into database (2)"
                                return "Successfully added message into database"
                        except:
                            return "Error: Unable to insert message into database (3)"
            except:
                return "Error: Unable to execute query"

        else:
            queryInsertNewMessage = """INSERT INTO test.message (message_id, date_time, creator, title, post, class, upvotes) VALUES ('%f', SYSDATE(), '%s', '%s', '%s', '%s', 0)""" % (reply_message_id +.001, creator, title, post, class_name)
            try:
                self.cursor.execute(queryInsertNewMessage)
                self.connection.commit()
            except:
                return "Error: Unable to insert message into database (4)"
            return "Successfully added message into database"

    def messagesByUser(self, creator):
        querySelect = """SELECT post FROM test.message WHERE creator = '%s'""" % (creator)
        try:
            messages_list = []
            self.cursor.execute(querySelect)
            for (messages) in self.cursor:
                messages_list.append(messages[0])
        except:
            return "Error: Unable to execute query"
        return messages_list

    def getRepliesToThread(self, thread_message_id):
        querySelect = """SELECT post FROM test.message WHERE message_id > '%d' AND message_id < '%d'""" % (thread_message_id, thread_message_id + 1)
        try:
            replies_list = []
            self.cursor.execute(querySelect)
            for (replies) in self.cursor:
                replies_list.append(replies[0])
        except:
            return "Error: Unable to execute query"
        return replies_list

    def messagesByClass(self, class_name):
        querySelect = """SELECT DISTINCT title FROM test.message WHERE class = '%s'""" % (class_name) 
        try:
            threads_by_class = []
            self.cursor.execute(querySelect)
            for (threads) in self.cursor:
                threads_by_class.append(threads[0])
        except:
            return "Error: Unable to execute query"
        return threads_by_class



#        
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
#        return threadResults
#    
#    def getThreadId(self, email, thread_title):
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
#            self.cursor.execute(querySelect)
#        except:
#            return "Error: Unable to execute query"
#        for (upvotes) in self.cursor:
#            return upvotes[0]
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        
#            
#    def addPost(self, email, thread_id, post):
#        query = """INSERT INTO se_database.posts (email, date, thread_id, post) VALUES ('%s', SYSDATE(), '%s', '%s')""" % (email, thread_id, post)
#        try:
#            self.cursor.execute(query)
#            self.connection.commit()
#        except:
#            return False
#        finally:
#            return True
#        
#    def upvoteThread(self, email, thread_id):
#        query = """SELECT upvotes FROM se_database.threads WHERE thread_id = '%d'""" % (thread_id)
#        query1 = """SELECT upvotes FROM se_database.profiles WHERE email = '%s'""" % (email)
#        try:
#            self.cursor.execute(query)
#            for (upvote_thread) in self.cursor:
#                upvote_thread = upvote_thread[0]
#            self.cursor.execute(query1)
#            for (upvote_profile) in self.cursor:
#                upvote_profile= upvote_profile[0]
#        except:
#            return False
#        finally:
#            query2 = """UPDATE se_database.threads SET upvotes = '%d' + 1 WHERE thread_id='%d'""" % (upvote_thread, thread_id)
#            query3 = """UPDATE se_database.profiles SET upvotes = '%d' + 1 WHERE email='%s'""" % (upvote_profile, email)
#            try:
#                self.cursor.execute(query2)
#                self.connection.commit()
#                self.cursor.execute(query3)
#                self.connection.commit()
#            except:
#                return False
#            finally:
#                return True
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
            self.cursor.execute("""UPDATE test.class SET list_of_users = %s WHERE class_name = %s""",(userList, className))
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
            self.cursor.execute("""UPDATE test.profiles SET list_of_classes = %s WHERE email = %s""",(classList, email))
            self.connection.commit()
        return userList, classList

    def closeConnection(self):
        self.cursor.close()
        self.connection.close()
