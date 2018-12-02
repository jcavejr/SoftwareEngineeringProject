# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:34:27 2018

@author: John Carter and Dominic Scola
"""

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
    
    def closeConnection(self):
        self.cursor.close()
        self.connection.close()
