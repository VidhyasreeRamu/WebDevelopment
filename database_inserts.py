import sqlite3

conn = sqlite3.connect('AskBronco.db')
cur = conn.cursor()

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES ('nkurian', '2017-10-30 22:27:12' , '2017-10-31 22:27:12', 'Open','Medium', 'GBP', 'Swap Course', 'Need to swap a Courses', 'Kindly drop the Course MGMT2501 and add MSIS2604', 'rfernandez')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-11-22 22:27:12' , '2017-11-23 22:27:12','Open','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-11-22 22:27:12' , '2017-11-23 22:27:12','In Progress','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")

cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-11-22 22:27:12' , '2017-11-23 22:27:12','Closed','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-11-22 22:27:12' , '2016-11-23 22:27:12','In Progress','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2016-11-22 22:27:12' , '2016-11-23 22:27:12','Open','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'speters')")
cur.execute("INSERT INTO TICKETS  (CREATED_BY, CREATION_TIME, CLOSED_TIME, STATUS, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION, STAFF_NAME) VALUES  ('mchintalapati', '2017-11-22 22:27:12' , '2017-11-23 22:27:12','Open','Medium', 'ISS', 'OPT Appointment','Need OPT Appointment', 'Need OPT appointment in coming week', 'sbonnel')")

