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
    
    '''
    Profile Functions
    '''

    def addProfile(self, email, password, first, last, school = "Rutgers Camden"):
        '''
        Adds a profile to the database
        @param: email, password, first name, last name, school name (defaulted to Rutgers Camden)
        @return: True if successful, False otherwise
        '''
        queryCheck = """SELECT COUNT(*) FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(queryCheck)
            for (count) in self.cursor:
                if count[0] > 0:
                    return False
        except:
            return False
        queryInsert = """INSERT INTO test.profiles (email, password, first, last, school, upvotes, active_flag) VALUES ('%s','%s','%s','%s','%s', 0, 1)""" % (email, password, first, last, school)
        try:
            self.cursor.execute(queryInsert)
            self.connection.commit()
        except:
            return False
        return True
    
    def checkProfileCredentials(self, email, password):
        '''
        Checks that the email and password match
        @param: email, password
        @return: True if credentials correct, False otherwise
        '''
        queryCheck = """SELECT COUNT(*) FROM test.profiles WHERE email = '%s' AND password = '%s'""" % (email, password)
        try:
            self.cursor.execute(queryCheck)
        except:
            return False
        for (count) in self.cursor:
            if count[0] == 1:
                return True
            else:
                return False
                
    def getProfileName(self, email):
        '''
        Gets the name of the user
        @param: email
        @return: the first and last name of the user as a string
        '''
        querySelect = """SELECT first, last FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(querySelect)
        except:
            return False
        for (first, last) in self.cursor:
            return first+" "+last
    
    def getProfileSchool(self, email):
        '''
        Get the school of the user
        @param: email
        @return: the school the user belongs to.
        '''
        querySelect = """SELECT school FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(querySelect)
        except:
            return False
        for (school) in self.cursor:
            return school[0]

    def getProfileUpvotes(self, email):
        '''
        Gets the number of upvotes the user has
        @param: email
        @return: the number of upvotes a user has
        '''
        querySelect = """SELECT upvotes FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(querySelect)
        except:
            return False
        for (upvotes) in self.cursor:
            return upvotes[0]
    

    '''
    Message Functions
    '''

    def addMessage(self, new_thread_ind, reply_message_id, creator, title, post, class_name):
        '''
        Adds a message into the message table
        @param new_thread_id (0 if new thread), the id of the message you are replying to (0 if new thread), creator, title, post, name of class
        @return True if successful, False otherwise
        '''
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
                            return False
                        return True
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
                                    return False
                                return True
                        except:
                            return False
            except:
                return False

        else:
            queryInsertNewMessage = """INSERT INTO test.message (message_id, date_time, creator, title, post, class, upvotes) VALUES ('%f', SYSDATE(), '%s', '%s', '%s', '%s', 0)""" % (reply_message_id +.001, creator, title, post, class_name)
            try:
                self.cursor.execute(queryInsertNewMessage)
                self.connection.commit()
            except:
                return False
            return True

    def messagesByUser(self, creator):
        '''
        Lists all the messages a person has posted
        @param: creator
        @return: List of all messages
        '''
        querySelect = """SELECT post FROM test.message WHERE creator = '%s'""" % (creator)
        try:
            messages_list = []
            self.cursor.execute(querySelect)
            for (messages) in self.cursor:
                messages_list.append(messages[0])
        except:
            return False
        return messages_list

    def getRepliesToThread(self, thread_message_id):
        '''
        Lists all replies to a thread
        @param: id of the thread
        @return: list of all replies
        '''
        querySelect = """SELECT post FROM test.message WHERE message_id > '%d' AND message_id < '%d'""" % (thread_message_id, thread_message_id + 1)
        try:
            replies_list = []
            self.cursor.execute(querySelect)
            for (replies) in self.cursor:
                replies_list.append(replies[0])
        except:
            return False
        return replies_list

    def messagesByClass(self, class_name):
        '''
        Lists all the post titles by class
        @param: name of the class
        @return: a list of titles
        '''
        querySelect = """SELECT DISTINCT title FROM test.message WHERE class = '%s'""" % (class_name) 
        try:
            threads_by_class = []
            self.cursor.execute(querySelect)
            for (threads) in self.cursor:
                threads_by_class.append(threads[0])
        except:
            return False
        return threads_by_class

    def upvoteMessage(self, email, message_id):
        query = """SELECT upvotes FROM test.message WHERE message_id = '%d'""" % (message_id)
        query1 = """SELECT upvotes FROM test.profiles WHERE email = '%s'""" % (email)
        try:
            self.cursor.execute(query)
            for (upvote_message) in self.cursor:
                upvote_message = upvote_message[0]
            self.cursor.execute(query1)
            for (upvote_profile) in self.cursor:
                upvote_profile= upvote_profile[0]
        except:
            return False
        finally:
            query2 = """UPDATE test.message SET upvotes = '%d' + 1 WHERE message_id='%d'""" % (upvote_message, message_id)
            query3 = """UPDATE test.profiles SET upvotes = '%d' + 1 WHERE email='%s'""" % (upvote_profile, email)
            try:
                self.cursor.execute(query2)
                self.connection.commit()
                self.cursor.execute(query3)
                self.connection.commit()
            except:
                return False
            finally:
                return True


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
            return False
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
                    return False
        except:
            return False
        queryInsert = """INSERT INTO test.class (class_name, subject, color, school, list_of_users) VALUES ('%s','%s','%s','%s','%s')""" % (name, subject, color, school, userList)
        try:
            self.cursor.execute(queryInsert)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(err)
            return False
        return True

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
            return False
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
            return False
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
            return False
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
            return False
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
            return False
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
            return False
        classList = ''
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
