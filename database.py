 #!/usr/bin/python

import csv
import sqlite3

conn = sqlite3.connect('AskBronco.db')
cur = conn.cursor()


# USER details table creation
cur.execute("DROP TABLE IF EXISTS USER")
cur.execute("CREATE TABLE USER( USER_ID INT UNIQUE, USER_NAME TEXT PRIMARY KEY, FIRST_NAME TEXT, LAST_NAME TEXT, EMAIL TEXT, PASSWORD TEXT NOT NULL)")

cur.execute("INSERT INTO USER VALUES (1, 'rdeshpande','Rucha','Deshpande','rdeshpande@scu.edu','qwe@123')")
cur.execute("INSERT INTO USER VALUES (2, 'drajagopal','Divya','Rajagopal','drajagopal@scu.edu','abc@123')")
cur.execute("INSERT INTO USER VALUES (3, 'vramu','Vidhyasree','Ramu','vramu@scu.edu','asd@123')")
cur.execute("INSERT INTO USER VALUES (4, 'mchintalapati','Meghna','chintalapati','mchintalapati@scu.edu','xyz@123')")
cur.execute("INSERT INTO USER VALUES (5, 'nkurian','Nora','Kurian','nkurian@scu.edu','zxc@123')")
cur.execute("INSERT INTO USER VALUES (6, 'jsmith','John','Smith','jsmith@scu.edu','abc@123')")
cur.execute("INSERT INTO USER VALUES (7, 'adhal','Amarjit','dhal','adhal@scu.edu','abc@123')")
cur.execute("INSERT INTO USER VALUES (8, 'akumar4','Abinav','Kumar','akumar4@scu.edu','abc@123')")
cur.execute("INSERT INTO USER VALUES (9, 'ysun','Yixin','Sun','ysun@scu.edu','abc@123')")
cur.execute("INSERT INTO USER VALUES (10, 'fwang2','Fei','Wang','fwang@scu.edu','abc@123')")

# DEPARTMENT list table creation
cur.execute("DROP TABLE IF EXISTS DEPARTMENT")
cur.execute("CREATE TABLE DEPARTMENT( DEPARTMENT_ID INT PRIMARY KEY, DEPARTMENT_NAME TEXT)")
cur.execute("INSERT INTO DEPARTMENT VALUES (1, 'GBP')")
cur.execute("INSERT INTO DEPARTMENT VALUES (2, 'ISS')")
cur.execute("INSERT INTO DEPARTMENT VALUES (3, 'IT')")

# STAFF details table creation
cur.execute("DROP TABLE IF EXISTS STAFF")
cur.execute("CREATE TABLE STAFF( DEPT_ID TEXT, STAFF_NAME TEXT PRIMARY KEY, FIRST_NAME TEXT, LAST_NAME TEXT, EMAIL TEXT, PASSWORD TEXT NOT NULL, FOREIGN KEY(DEPT_ID) REFERENCES DEPARTMENT(DEPARTMENT_NAME))")
'''GBP Staff'''
cur.execute("INSERT INTO STAFF VALUES ('GBP', 'mvirasak','Minh','Vrasak','mvirasak@scu.edu','abc@123')")
cur.execute("INSERT INTO STAFF VALUES ('GBP', 'rfernandez','Ramie','Fernandez','rfernandez@scu.edu','abc@123')")
'''ISS Staff'''
cur.execute("INSERT INTO STAFF VALUES ('ISS', 'speters','Susan','Peters','speters@scu.edu','abc@123')")
cur.execute("INSERT INTO STAFF VALUES ('ISS', 'sbonnel','Sarah','Bonnel','sbonnel@scu.edu','abc@123')")
'''IT Staff'''
cur.execute("INSERT INTO STAFF VALUES ('IT', 'sjane','Susan','Jane','sjane@scu.edu','abc@123')")
cur.execute("INSERT INTO STAFF VALUES ('IT', 'randrew','Robert','Andrew','randrew@scu.edu','abc@123')")
'''Admin Staff'''
cur.execute("INSERT INTO STAFF VALUES ('ADMIN', 'admin','admin','admin','admin@scu.edu','abc@123')")

# CATEGORY list table creation
cur.execute("DROP TABLE IF EXISTS CATEGORY")
cur.execute("CREATE TABLE CATEGORY( DEPARTMENT TEXT, CATEGORY_ID INT PRIMARY KEY, CATEGORY_NAME TEXT, FOREIGN KEY(DEPARTMENT) REFERENCES DEPARTMENT(DEPARTMENT_NAME))")
'''GBP'''
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 1, 'Add Course')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 2, 'Drop Course')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 3, 'Swap Course')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 4, 'Petition form')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 5, 'Other request related to petition form')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 6, 'Careers Chat')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 7, 'Alumini Panel')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 8, 'Request classroom change')")
cur.execute("INSERT INTO CATEGORY VALUES ('GBP', 9, 'Others')")
'''ISS'''
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 10, 'CPT Appointment')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 11, 'OPT Appointment')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 12, 'Immigration')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 13, 'On Campus Employment - SSN')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 14, 'Reduced Course Load')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 15, 'I20')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 16, 'Visa and Travel')")
cur.execute("INSERT INTO CATEGORY VALUES ('ISS', 17, 'Others')")
'''IT'''
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 18, 'Campus Network')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 19, 'eCampus')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 20, 'Gmail')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 21, 'Login/Acccounts')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 22, 'Campus Wireless')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 23, 'Software')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 24, 'Registering a device')")
cur.execute("INSERT INTO CATEGORY VALUES ('IT', 25, 'Others')")


# STATUS list table creation
cur.execute("DROP TABLE IF EXISTS STATUS")
cur.execute("CREATE TABLE STATUS( STATUS_ID INT PRIMARY KEY, STATUS_TYPE TEXT)")
cur.execute("INSERT INTO  STATUS VALUES (1 , 'Open')")
cur.execute("INSERT INTO  STATUS VALUES (2 , 'In Progress')")
cur.execute("INSERT INTO  STATUS VALUES (3 , 'Closed')")


# PRIORITY list table creation
cur.execute("DROP TABLE IF EXISTS PRIORITY")
cur.execute("CREATE TABLE PRIORITY( PRIORITY_ID INT PRIMARY KEY, PRIORITY_TYPE TEXT)")

cur.execute("INSERT INTO PRIORITY VALUES(1,'Urgent')")
cur.execute("INSERT INTO PRIORITY VALUES(2,'High')")
cur.execute("INSERT INTO PRIORITY VALUES(3,'Medium')")
cur.execute("INSERT INTO PRIORITY VALUES(4,'Low')")

# TICKETS table creation
cur.execute("DROP TABLE IF EXISTS TICKETS")
cur.execute("CREATE TABLE TICKETS (TICKET_ID INTEGER PRIMARY KEY AUTOINCREMENT, CREATED_BY TEXT, CREATION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, CLOSED_TIME TIMESTAMP DEFAULT NULL, STATUS TEXT DEFAULT Open, PRIORITY TEXT, DEPARTMENT TEXT, CATEGORY TEXT, SUMMARY TEXT, DESCRIPTION TEXT, FILE_NAME TEXT DEFAULT NULL, STAFF_NAME TEXT DEFAULT NULL, FOREIGN KEY(CREATED_BY) REFERENCES USER(USER_NAME),FOREIGN KEY(STATUS) REFERENCES STATUS(STATUS_TYPE), FOREIGN KEY(PRIORITY) REFERENCES PRIORITY(PRIORITY_TYPE), FOREIGN KEY(DEPARTMENT) REFERENCES DEPARTMENT(DEPARTMENT_NAME), FOREIGN KEY(CATEGORY) REFERENCES CATEGORY(CATEGORY_NAME), FOREIGN KEY(STAFF_NAME) REFERENCES STAFF(STAFF_NAME))")

''' OCT 2016 All tickets CLOSED ''' 
cur.execute("INSERT INTO TICKETS  VALUES (100,'jsmith', '2016-10-29 02:27:12' ,'2016-10-30 22:27:12', 'Closed','Medium', 'GBP','Add Course', 'Need to add capstone Courses', 'Kindly add the Capstone Course to me', 'null', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  VALUES (101,'jsmith', '2016-10-29 02:27:12' ,'2016-10-30 20:27:12', 'Closed','Medium', 'ISS','Reduced Course Load', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'null', 'speters')")
cur.execute("INSERT INTO TICKETS  VALUES (102,'jsmith', '2016-10-29 02:27:12' ,'2016-10-30 20:27:12', 'Closed','Medium', 'GBP','Drop Course', 'Drop course MSIS 2604', 'Drop course MSIS 2604', 'null', 'speters')")
cur.execute("INSERT INTO TICKETS  VALUES (103,'jsmith', '2016-10-29 02:27:12' ,'2016-10-30 20:27:12', 'Closed','Medium', 'IT','eCampus', 'Unable to update the address', 'Unable to update the address', 'null', 'sjane')")
cur.execute("INSERT INTO TICKETS  VALUES (104,'rdeshpande', '2016-10-29 02:27:12' ,'2016-10-30 22:27:12', 'Closed','Medium', 'GBP','Add Course', 'Need to add capstone Courses', 'Kindly add the Capstone Course to me', 'null', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  VALUES (105,'drajagopal', '2016-10-30 02:27:12' ,'2016-10-30 20:27:12', 'Closed','Medium', 'ISS','Reduced Course Load', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'null', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  VALUES (106,'nkurian', '2016-10-29 02:27:12' ,'2016-10-30 20:27:12', 'Closed','Medium', 'IT','eCampus', 'Unable to update the address', 'Unable to update the address', 'null', 'randrew')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('nkurian', '2017-10-30 03:27:12' , '2017-10-31 22:27:12', 'Closed','Medium', 'GBP', 'Swap Course', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-10-30 03:27:12' , '2016-11-01 22:27:12', 'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MGMT2501', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-10-30 02:27:12' , '2016-10-30 22:27:12', 'Closed','Medium', 'ISS', 'CPT Appointment', 'Need CPT appointment', 'Need CPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-10-30 02:27:12' , '2016-10-30 22:27:12', 'Closed','Medium', 'ISS', 'CPT Appointment', 'Need CPT appointment', 'Need CPT appointment in coming week', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-10-30 02:27:12' , '2016-10-30 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2016-10-30 02:27:12' , '2016-10-30 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'randrew')")


''' Nov 2016 All tickets CLOSED'''
'''ISS'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-11-03 22:27:12', 'Closed','Medium', 'ISS', 'Reduced Course Load', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-05-12 22:27:12' , '2016-11-06 22:27:12', 'Closed','Medium', 'ISS', 'CPT Appointment', 'Need CPT appointment', 'Need CPT appointment in coming week', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2016-11-11 22:27:12' , '2016-11-13 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'sbonnel')")  
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-11-12 22:27:12' , '2017-11-13 22:27:12','Open','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
'''GBP'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2016-11-12 22:27:12' ,'2016-12-14 22:27:12', 'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-11-14 22:27:12' , '2016-11-16 22:27:12',  'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-11-16 22:27:12' , '2016-11-17 22:27:12' ,'Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2016-11-16 22:27:12' , '2016-11-17 22:27:12' ,'Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
'''IT'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-11-24 02:27:12' , '2016-11-25 22:27:12', 'Closed','Medium', 'IT', 'Software', 'Error While Installing a software', 'Software installation is blocked', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2016-11-26 02:27:12' , '2016-11-27 22:27:12', 'Closed','Medium', 'IT', 'Campus Network', 'Campus network not working', 'Unable to connect to Campus Network', 'randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2016-11-25 02:27:12' , '2016-11-27 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-11-27 02:27:12' , '2016-11-30 22:27:12', 'Closed','Medium', 'IT', 'Software','Error While Installing a software', 'Software installation is blocked', 'randrew')")


''' Dec 2016 All Closed Tickets '''
'''ISS'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-12-02 22:27:12' , '2016-12-04 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2017-12-04 22:27:12' , '2017-12-07 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-12-05 03:27:12' , '2017-11-07 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
'''GBP'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2016-12-09 22:27:12' , '2016-12-10 22:27:12',  'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2016-12-12 22:27:12' , '2016-12-14 22:27:12','Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2016-12-15 22:27:12' , '2016-12-16 22:27:12', 'Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
'''IT'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2016-12-18 22:27:12' , '2016-12-19 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-12-20 22:27:12' , '2016-12-21 22:27:12', 'Closed','Medium', 'IT', 'Software','Error While Installing a software', 'Software installation is blocked', 'randrew')")


''' Jan 2017 All Closed Tickets '''
'''ISS'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-01-03 22:27:12' , '2017-01-04 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2017-01-03 22:27:12' , '2017-01-05 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2017-01-04 22:27:12' , '2017-01-05 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'sbonnel')")  
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-01-04 22:27:12' , '2017-01-05 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2017-01-06 22:27:12' , '2017-01-07 22:27:12','Closed','Medium', 'ISS', 'CPT Appointment','Need CPT Appointment', 'Need CPT appointment in coming week', 'sbonnel')")  
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-01-07 22:27:12' , '2017-01-08 22:27:12','Closed','Medium', 'ISS', 'CPT Appointment','Need CPT Appointment', 'Need CPT appointment in coming week', 'speters')")
'''GBP'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2017-01-10 22:27:12' , '2017-01-11 22:27:12', 'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-01-10 22:27:12' , '2017-01-12 22:27:12', 'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-01-11 22:27:12' , '2017-01-12 22:27:12','Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-01-13 22:27:12' , '2017-01-14 22:27:12','Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
'''IT'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-01-13 22:27:12' , '2017-01-13 22:27:12', 'Closed','Medium', 'IT', 'Software', 'Error While Installing a software', 'Software installation is blocked', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2017-01-13 22:27:12' , '2017-01-14 22:27:12', 'Closed','Medium', 'IT', 'Campus Network', 'Campus network not working', 'Unable to connect to Campus Network', 'randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2017-01-15 22:27:12' , '2017-01-16 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-01-17 22:27:12' , '2017-01-18 22:27:12', 'Closed','Medium', 'IT', 'Software','Error While Installing a software', 'Software installation is blocked', 'randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('adhal', '2017-01-17 22:27:12' , '2017-01-19 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-01-20 22:27:12' , '2017-01-23 22:27:12', 'Closed','Medium', 'IT', 'Registering a device','Registering a device', 'Registering a device', 'randrew')")


''' Feb 2017 All Tickets '''
'''ISS'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-02-03 22:27:12' , '2017-02-03 22:27:12','Closed','Medium', 'ISS', 'Reduced Course Load','Reduced Course Load for spring quater', 'Reduced Course Load for spring quater', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2017-02-03 22:27:12' , '2017-02-10 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-02-13 22:27:12' , '2017-02-14 22:27:12','Closed','Medium', 'ISS', 'Visa and Travel','Travel to home country', 'Travel to home country', 'speters')")
'''GBP'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-02-13 22:27:12' , '2017-02-14 22:27:12',  'Closed','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-02-13 22:27:12' , '2017-02-14 22:27:12','Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-02-13 22:27:12' , '2017-02-16 22:27:12','Closed','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
'''IT'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2016-11-25 02:27:12' , '2016-11-27 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Campus wireless not working', 'Campus wireless not working', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-11-27 02:27:12' , '2016-11-30 22:27:12', 'Closed','Medium', 'IT', 'Software','Error While Installing a software', 'Software installation is blocked', 'randrew')")


''' Inprogress Ticket '''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME,  STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-02-25 22:27:12' , 'In Progress','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME,  STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('nkurian', '2017-02-26 22:27:12' , 'In Progress','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME,  STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-02-26 22:27:12' , 'In Progress','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME,  STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-02-27 22:27:12' ,  'In Progress','Medium', 'GBP', 'Drop Course', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME,  STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-02-27 22:27:12' , 'In Progress','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-02-27 22:27:12' , 'In Progress','Medium','GBP', 'Petition form', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'mvirasak')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('vramu', '2017-02-27 22:27:12' , 'In Progress','Medium', 'IT', 'Login/Acccounts', 'Issue with Login', 'Issue with Login', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME,  STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2017-02-27 22:27:12' , 'In Progress','Medium', 'IT','Login/Acccounts', 'Unable to Login', 'Issue with Login', 'randrew')")

''' Open Tickets '''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('drajagopal', 'Medium','GBP', 'Swap Course', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2602')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('rdeshpande', 'Medium','ISS', 'OPT Appointment', 'Need OPT Appointment', 'Need OPT appointment in coming week')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('vramu', 'Low','ISS', 'OPT Appointment', 'Need OPT Appointment', 'Need OPT appointment in coming week')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('rdeshpande', 'Medium','ISS', 'OPT Appointment', 'Need OPT Appointment', 'Need OPT appointment in coming week')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('vramu', 'Low','IT', 'Gmail', 'Issues with Gmail', 'Issues with Gmail account')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('drajagopal', 'Medium','IT', 'eCampus', 'The entrollment option is unavailable', 'The entrollment option is unavailable')")

'''Meghana's tickets'''
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-11-01 22:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-11-12 22:27:12' , '2016-11-13 22:27:12' ,'Closed','Medium','IT', 'Gmail', 'Need graduate petition form for spring 2017', 'Need graduate petition form for spring 2017', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('rdeshpande', '2016-11-12 22:27:12' , '2016-11-13 22:27:12', 'Closed','Medium', 'IT', 'Campus Network', 'Need CPT appointment', 'Need CPT appointment in coming week', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-11-21 22:27:12' , '2016-11-22 22:27:12',  'Closed','Medium', 'IT', 'Gmail', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'randrew')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-11-22 22:27:12' , '2016-11-23 22:27:12','Closed','Medium', 'IT', 'Campus Wireless','Need OPT Appointment', 'Need OPT appointment in coming week', 'randrew')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('drajagopal', '2016-12-12 22:27:12' ,'2016-12-14 22:27:12', 'Closed','Medium', 'IT', 'Gmail', 'Need to drop a Courses', 'Kindly drop the Course MSIS2604', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('nkurian', '2016-10-30 22:27:12' , '2016-10-30 22:27:12', 'Closed','Medium', 'IT', 'Gmail', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2604', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('drajagopal', 'Medium','IT', 'Gmail', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2602')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('rdeshpande', 'Medium','IT', 'Campus Wireless', 'Need OPT Appointment', 'Need OPT appointment in coming week','sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', 'Medium','IT', 'Campus Wireless', 'Need OPT Appointment', 'Need OPT appointment in coming week','randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', 'Medium','IT', 'eCampus', 'Need OPT Appointment', 'Need OPT appointment in coming week','sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('nkurian', '2017-10-30 22:27:12' , '2017-10-31 22:27:12', 'Open','Medium', 'IT', 'Gmail', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2604', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('nkurian', '2017-10-28 22:27:12' , '2017-10-29 02:27:12', 'In Progress','Medium', 'IT', 'Gmail', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2604', 'randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION) VALUES ('drajagopal', 'Medium','IT', 'Gmail', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2602')")

#iss

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-01 22:27:12', 'Open','Medium', 'ISS', 'CPT Appointment', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-01 22:27:12', 'In Progress','Medium', 'ISS', 'CPT Appointment', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-04 23:27:12', 'Closed','Medium', 'ISS', 'Reduced Course Load', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'speters')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-01-01 12:27:12' , '2017-01-01 22:27:12', 'Open','Medium', 'ISS', 'CPT Appointment', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-01-01 12:27:12' , '2017-01-06 22:27:12', 'In Progress','Medium', 'ISS', 'OPT Appointment', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sbonnel')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-11-01 12:27:12' , '2017-12-09 22:27:12', 'Closed','Medium', 'ISS', 'Reduced Course Load', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'speters')")

#gbp

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-01 22:27:12', 'Open','Medium', 'GBP', 'Add Course', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-01 22:27:12', 'In Progress','Medium', 'GBP', 'Drop Course', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-04 23:27:12', 'Closed','Medium', 'GBP', 'Add Course', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'mvirasak')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-01-01 12:27:12' , '2017-01-01 22:27:12', 'Open','Medium', 'GBP', 'Add Course', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-01-01 12:27:12' , '2017-01-06 22:27:12', 'In Progress','Medium', 'GBP', 'Add Course', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-11-01 12:27:12' , '2017-12-09 22:27:12', 'Closed','Medium', 'GBP', 'Swap Course', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'mvirasak')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-12-01 12:27:12' , '2017-12-03 22:27:12', 'Closed','Medium', 'GBP', 'Petiton', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'mvirasak')")

#it
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-01 22:27:12', 'Open','Medium', 'IT', 'Campus Network', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-01 22:27:12', 'In Progress','Medium', 'IT', 'Gmail', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sjanes')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2016-11-01 12:27:12' , '2016-12-04 23:27:12', 'Closed','Medium', 'IT', 'Campus Wireless', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sjane')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-01-01 12:27:12' , '2017-01-01 22:27:12', 'Open','Medium', 'IT', 'Campus Wireless', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sjane')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-01-01 12:27:12' , '2017-01-06 22:27:12', 'In Progress','Medium', 'IT', 'Campus Network', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'randrew')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('vramu', '2017-11-01 12:27:12' , '2017-12-09 22:27:12', 'Closed','Medium', 'IT', 'Gmail', 'Reduced Course Load for winter 2017', 'Reduced Course Load for winter 2017', 'sjane')")



# COMMENTS table creation
cur.execute("DROP TABLE IF EXISTS COMMENTS")
cur.execute("CREATE TABLE COMMENTS( TICKET_ID INTEGER, COMMENTS_ID INTEGER PRIMARY KEY AUTOINCREMENT, CREATION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, CREATED_BY TEXT, COMMENT TEXT,FOREIGN KEY(TICKET_ID) REFERENCES TICKETS (TICKET_ID))")
cur.execute("INSERT INTO COMMENTS VALUES(100, 10, '2016-10-29 22:27:12' ,'mvirasak', 'Course added' )")
cur.execute("INSERT INTO COMMENTS VALUES(101, 11, '2016-10-29 22:27:12' ,'speters', 'Please come in for appointment at 10:30 tomorrow')")
cur.execute("INSERT INTO COMMENTS VALUES(102, 12, '2016-11-01 22:27:12' ,'mvirasak', 'Course dropped' )")
cur.execute("INSERT INTO COMMENTS VALUES(104, 13, '2016-10-29 12:27:12' ,'speters', 'Please come in for appointment' )")
cur.execute("INSERT INTO COMMENTS VALUES(104, 14, '2016-10-29 01:27:12' ,'rdeshpande', 'Please let me know the time' )")
cur.execute("INSERT INTO COMMENTS VALUES(104, 15, '2016-10-29 03:27:12' ,'speters', 'Please come at 11:30 AM' )")

# NOTES table creation
cur.execute("DROP TABLE IF EXISTS NOTES")
cur.execute("CREATE TABLE NOTES( TICKET_ID INTEGER, NOTE_ID INTEGER PRIMARY KEY AUTOINCREMENT, CREATION_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, CREATED_BY TEXT, NOTE TEXT, FOREIGN KEY(TICKET_ID) REFERENCES TICKETS (TICKET_ID))")
cur.execute("INSERT INTO NOTES VALUES(100, 10, '2016-11-01 22:27:12' ,'rfernandez', 'Can you please add it' )")
cur.execute("INSERT INTO NOTES VALUES(100, 11, '2016-11-01 22:27:12' ,'mvirasak', 'Added')")
cur.execute("INSERT INTO NOTES VALUES(101, 12, '2016-11-01 22:27:12' ,'speters', 'Can you please add it' )")
cur.execute("INSERT INTO NOTES VALUES(101, 13, '2016-11-01 22:27:12' ,'sbonnel', 'Added')")
cur.execute("INSERT INTO NOTES VALUES(103, 14, '2016-11-01 22:27:12' ,'speters', 'Can you please add it' )")
cur.execute("INSERT INTO NOTES VALUES(103, 15, '2016-11-01 22:27:12' ,'sbonnel', 'Added')")



#with open('USER.csv', 'r') as f:
 #   reader = csv.reader(f.readlines()[1:])  # exclude header line
  #  cur.executemany("""INSERT INTO USER VALUES (?,?,?,?,?)""",
#			 (row for row in reader))

conn.commit()
conn.close()

