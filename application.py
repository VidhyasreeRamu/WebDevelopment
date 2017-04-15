'''
Capstone Design Project - Ask Bronco

Created by : Ask Bronco Team members on February 2017

'''

from collections import Counter

import csv
import sqlite3
import json
import sys
import uuid
import boto3
import re

from flask import Flask, render_template, request, g, redirect, url_for,session,jsonify,request, redirect,send_from_directory
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from werkzeug import secure_filename
import os
DATABASE = '/var/www/html/flaskapp/AskBronco.db'
UPLOADS ='/var/www/html/uploads/'

app = Flask('application')

app.config.from_object('application')

app.secret_key = 'secretkey'
app.config['UPLOAD_FOLDER'] = UPLOADS

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
	 db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def createTicket_query(query, args=()):
    cur = get_db().execute(query, args)
    cur.close()
    

# View db function to check on the DB 
@app.route('/viewdb')
def viewdb():
    rows = execute_query("""SELECT * FROM Tickets""")
    return '<br>'.join(str(row) for row in rows)



''' Start User/Staff Login and Signup related '''

# Rendering the templates to login, register new user and forgot password functionality
@app.route('/')
def webprint():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgotpassword.html')
def forgotpassword():
    return render_template('forgotpassword.html')

@app.route('/thankuregistration')
def thankuregistration():
    return render_template('thankuregistration.html')


# User Signup
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    username = request.form['username']
    password = request.form['Password']
    confirmedPassword = request.form['password_confirmation']
    if password!=confirmedPassword:
            return render_template('register.html',error='Passwords do not match')
    match = re.match('^[a-zA-Z0-9]+@',email)
    if match == None:
        return render_template('register.html',error='Please enter a valid email address')
 

    rows = get_db().execute('SELECT * FROM User WHERE USER_NAME="%s"' %(username))
    if rows.fetchone() is None:        
        get_db().execute('INSERT INTO USER(USER_NAME,FIRST_NAME,LAST_NAME,EMAIL,PASSWORD) VALUES("%s","%s","%s","%s","%s")' %(username,firstname,lastname,email,password ))
        get_db().commit();
        return render_template('login.html', success='Thank you for registering, please sign in!')
    else:
        return render_template('register.html',error='Username already exists')
   
# Forgot Password Functionality
@app.route('/forgotpwd',methods=['POST','GET'])
def forgotpwd():
        username = request.args.get('name')
        rows = get_db().execute('SELECT EMAIL FROM User WHERE USER_NAME="%s"' %(username))
        email = ""
        for row in rows:
            email = row[0];  #We will only fetch 1st email id 

        if not email:
            return render_template('wrongusername.html')
        else:    

            s = Serializer(app.secret_key, 1800)
            token  = s.dumps({'user': username}).decode('utf-8')
            url = "http://"+request.host+"/resetpwd?token="+token
            invoke_ses_email(url, email)
            return render_template('afterforgot.html')
            
# Reset Password
@app.route('/resetpwd',methods=['POST','GET'])
def resetpwd():
    if request.method == 'GET':
        return render_template('passwordchange.html')
    else:    
        token  = request.args.get('token')
        password = request.form['password']
        username =  verify_token(token)
        if username is None:
            return render_template('login.html')
        else:
            print "I was here"
            get_db().execute('UPDATE User SET PASSWORD = "%s" WHERE USER_NAME="%s"' %(password,username))
            get_db().commit();

            return render_template('login.html')


# Email to User    
def verify_token(token):
    s = Serializer(app.secret_key)
    try:
        data = s.loads(token)
    except:
        return None
    id = data.get('user')
    if id:
        return id
    return None

def invoke_ses_email(url,email):
 client = boto3.client('ses',region_name='us-west-2',aws_access_key_id='AKIAJ5VG6QVSX3SRDTMA',aws_secret_access_key='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')
 response = client.send_email(
    Destination={
        
        'ToAddresses': [
            email
        ],
    },
    Message={
        'Body': {
            
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'Please click on this link to reset your password '+url,
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Password reset by Askbronco',
        },
    },
    ReplyToAddresses=[
    ],
    
    Source='askbronco@outlook.com',
   
)

# User/Staff Login
@app.route('/login',methods=['POST','GET'])
def login():
        username = request.form['name']
        password = request.form['password']
        rows = get_db().execute('SELECT * FROM User WHERE USER_NAME="%s" AND password="%s"' %(username, password))
        if rows.fetchone() is None:
           rows = get_db().execute('SELECT * FROM STAFF WHERE STAFF_NAME="%s" AND PASSWORD="%s"' %(username, password))
           if rows.fetchone() is None:
            return render_template('login.html', error='Invalid Credentials')
           else:
            session['username'] = username
            session['level'] = "staff"
            return redirect(url_for('staff'))
        else:
          session['username'] = username
          session['level'] = "student"
          return redirect(url_for('home'))

# Routing to Staff Login         
@app.route('/staff')
def staff():
        if 'username' in session:
            username = session['username']
            department = 'GBP';
            rows = get_db().execute('SELECT DEPT_ID FROM STAFF WHERE STAFF_NAME="%s"' %(username))
            for row in rows:
                department = row[0];

            if department == 'GBP':
                return render_template('Staff_Home_GBP.html', username = session['username'])
            elif department == "ISS":
                return render_template('Staff_Home_ISS.html', username = session['username'])
            elif department == "IT": 
                return render_template('Staff_Home_IT.html', username = session['username'])
            elif department == "ADMIN": 
                return render_template('manager_home.html', username = session['username'])    
        else:
         return render_template('login.html')
         
# Routing to User login
@app.route('/home')
def home():
        if 'username' in session:
         return render_template('user_home.html', username = session['username'])
        else:
         return render_template('login.html')

''' End of Login and Sign up related '''

''' ISS Details'''

# Rendering MyISS template 
@app.route('/MyISS.html')
def MYISS():
	return render_template('MyISS.html',username = session['username'])

# Display top 3 tickets for the user in MyISS	
@app.route('/tickets', methods=['GET'])
def get_tickets():
    try: 
    	username = session['username']
        rows = execute_query("""SELECT * FROM TICKETS WHERE DEPARTMENT = 'ISS' AND CREATED_BY like "%s" ORDER BY creation_time DESC Limit 3"""%(username))
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['ticket_id']=row[0]
            ticket['created_by']=row[1]
            ticket['creation_time']=row[2] 
            ticket['status']=row[4]
            ticket['priority']=row[5]
            ticket['category']=row[7]
            ticket['sub_category']=row[6]
            ticket['summary']=row[8]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
            
            tickets.append(ticket)    
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString	
        #return jsonify(tickets=tickets)		
    except:
            e = sys.exc_info()[0]
            return e	
            
#Rendering GBP template 
@app.route('/MyGBP.html')
def MYGBP():
	return render_template('MyGBP.html',username = session['username'])

# Display top 3 tickets for the user in individual dept	
@app.route('/GBPtickets', methods=['GET'])
def get_GBPtickets():
    try: 
    	username = session['username']
        rows = execute_query("""SELECT * FROM TICKETS WHERE DEPARTMENT="GBP" AND CREATED_BY like "%s" ORDER BY creation_time DESC Limit 3"""%(username))
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['ticket_id']=row[0]
            ticket['created_by']=row[1]
            ticket['creation_time']=row[2] 
            ticket['status']=row[4]
            ticket['priority']=row[4]
            ticket['category']=row[7]
            ticket['sub_category']=row[6]
            ticket['summary']=row[8]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
            
            tickets.append(ticket)    
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString	
        #return jsonify(tickets=tickets)		
    except:
            e = sys.exc_info()[0]
            return e	
# Rendering MyISS template 
@app.route('/MyIT.html')
def MYIT():
	return render_template('MyIT.html',username = session['username'])

# Display top 3 tickets for the user in individual dept	
@app.route('/ITtickets', methods=['GET'])
def get_ITtickets():
    try: 
    	username = session['username']
        rows = execute_query("""SELECT * FROM TICKETS WHERE DEPARTMENT="IT" AND CREATED_BY like "%s" ORDER BY creation_time DESC Limit 3"""%(username))
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['ticket_id']=row[0]
            ticket['created_by']=row[1]
            ticket['creation_time']=row[2] 
            ticket['status']=row[4]
            ticket['priority']=row[4]
            ticket['category']=row[7]
            ticket['sub_category']=row[6]
            ticket['summary']=row[8]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
            
            tickets.append(ticket)    
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString	
        #return jsonify(tickets=tickets)		
    except:
            e = sys.exc_info()[0]
            return e	
            
# ISS User Ticket Summary
@app.route('/ticketsummary.html')
def loadtickets():
        return render_template('ticketsummary.html', username = session['username'])
        
@app.route('/ticketsummaryGBP.html')
def loadticketsGBP():
        return render_template('ticketsummaryGBP.html', username = session['username'])  
        
@app.route('/ticketsummaryIT.html')
def loadticketsIT():
        return render_template('ticketsummaryIT.html', username = session['username'])                

# Display all the ISS ticket list to user        
@app.route('/ticketsummaryselection', methods=['GET'])
def get_ticketsummaryselection():
    try: 
        category = request.args.get('category')
        status = request.args.get('status')
        username = session['username']
        rows = get_db().execute("""SELECT * FROM TICKETS WHERE  CATEGORY LIKE "%s" AND STATUS LIKE "%s" AND CREATED_BY ="%s" AND DEPARTMENT = 'ISS'""" %(category,status,username))
        ticketssummary=[]
        for row in rows:
            ticketsummary = {}
            ticketsummary['TICKET_ID']=row[0]
            ticketsummary['CREATED_BY']=row[1]
            ticketsummary['STATUS']=row[4]
            ticketsummary['PRIORITY']=row[5]
            ticketsummary['CATEGORY']=row[7]
            ticketsummary['SUMMARY']=row[8]
            
            
            ticketssummary.append(ticketsummary)    
        jsonString = json.dumps(ticketssummary)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)    
    except:
            e = sys.exc_info()[0]
            return e         

# Display all the GBP ticket list to user
@app.route('/ticketsummaryselectionGBP', methods=['GET'])
def get_ticketsummaryselectionGBP():
    try: 
        category = request.args.get('category')
        status = request.args.get('status')
        username = session['username']
        rows = get_db().execute("""SELECT * FROM TICKETS WHERE  CATEGORY LIKE "%s" AND STATUS LIKE "%s" AND CREATED_BY ="%s" AND DEPARTMENT = 'GBP'""" %(category,status,username))
        ticketssummary=[]
        for row in rows:
            ticketsummary = {}
            ticketsummary['TICKET_ID']=row[0]
            ticketsummary['CREATED_BY']=row[1]
            ticketsummary['STATUS']=row[4]
            ticketsummary['CATEGORY']=row[7]
            ticketsummary['PRIORITY']=row[5]
            ticketsummary['SUMMARY']=row[8]
            
            
            ticketssummary.append(ticketsummary)    
        jsonString = json.dumps(ticketssummary)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)    
    except:
            e = sys.exc_info()[0]
            return e 

# Display all the GBP ticket list to user
@app.route('/ticketsummaryselectionIT', methods=['GET'])
def get_ticketsummaryselectionIT():
    try: 
        category = request.args.get('category')
        status = request.args.get('status')
        username = session['username']
        rows = get_db().execute("""SELECT * FROM TICKETS WHERE  CATEGORY LIKE "%s" AND STATUS LIKE "%s" AND CREATED_BY ="%s" AND DEPARTMENT = 'IT'""" %(category,status,username))
        ticketssummary=[]
        for row in rows:
            ticketsummary = {}
            ticketsummary['TICKET_ID']=row[0]
            ticketsummary['CREATED_BY']=row[1]
            ticketsummary['STATUS']=row[4]
            ticketsummary['CATEGORY']=row[7]
            ticketsummary['PRIORITY']=row[5]
            ticketsummary['SUMMARY']=row[8]
            
            
            ticketssummary.append(ticketsummary)    
        jsonString = json.dumps(ticketssummary)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)    
    except:
            e = sys.exc_info()[0]
            return e 
                        
# Render ISS Staff and User individual ticket view        	
@app.route('/TicketDetails_StaffView.html')
def ticketdetail_staff():
     return render_template('TicketDetails_StaffView.html')

@app.route('/TicketDetails_UserView.html')
def ticketdetail_user():
	return render_template('TicketDetails_UserView.html')

# Display ISS Ticket Details	
@app.route('/tickets/<ticket_id>', methods=['GET'])
def get_ticketdetail(ticket_id):
    try: 
        rows = execute_query("SELECT ticket_id, created_by, creation_time, status, department, priority,category, summary,description, staff_name, closed_time, file_name  FROM TICKETS WHERE ticket_id="+ticket_id)
    
        ticket={}
        row=rows[0]
        ticket['ticket_id']=row[0]
        ticket['created_by']=row[1]
        ticket['creation_time']=row[2]
        ticket['status']=row[3]
        ticket['department']=row[4]
        ticket['priority']=row[5]
        ticket['category']=row[6]
        ticket['summary']=row[7]
        ticket['description']=row[8] 
        ticket['staff_name']=row[9]   
        ticket['closed_time']=row[10]  
        ticket['file_name'] = row[11]
        ticket['all_categories'] = []
        catRows = execute_query("SELECT CATEGORY_NAME FROM CATEGORY WHERE DEPARTMENT='"+ticket['department']+"'")
        for cat in catRows:
            ticket['all_categories'].append(cat[0]) 
        
        jsonString = json.dumps(ticket)
        
        print jsonString
        return jsonString	
        #return jsonify(tickets=tickets)		
    except:
            e = sys.exc_info()[0]
            return e
# Update the ISS ticket with Staff details
@app.route('/tickets/<ticket_id>/action',methods = ['POST'])
def actionForTicket(ticket_id):
    status = request.form['status']
    staff_name = session['username']
    if status == 'Closed':
        print 'closing ticket'
        conn = get_db()
        conn.execute("UPDATE TICKETS SET STAFF_NAME= \'%s\', STATUS = \'%s\', CLOSED_TIME=(DateTime('now')) where ticket_id = %s" %(staff_name, status, ticket_id))
        conn.commit()
    else:
        print 'action on ticket '+ticket_id+' is '+status;
        conn = get_db()
        conn.execute("UPDATE TICKETS SET STAFF_NAME= \'%s\', STATUS = \'%s\' where ticket_id = %s" %(staff_name, status, ticket_id))
        conn.commit()
    return ticket_id + "is in status "+ status    

# Inserting new ISS User and Staff comments
@app.route('/tickets/<ticket_id>/comments',methods = ['POST', 'GET'])
def commentForTicket(ticket_id):
    if request.method == 'POST': 
        comment = request.form['comment']
        createdBy = session['username']#request.form['createdBy'] #replace with session user
        conn = get_db()
        conn.execute("INSERT INTO COMMENTS(TICKET_ID, CREATED_BY, COMMENT) VALUES( %s, \'%s\', \'%s\' )" %(ticket_id,createdBy,comment))
        conn.commit()
        return "Comment inserted"
    else:
        comments = []
        commentRows = execute_query("select C.CREATION_TIME, C.COMMENT, C.CREATED_BY,case when t.created_by == c.created_by then 'USER' else 'STAFF' end as 'TYPE' from COMMENTS C, TICKETS t where c.ticket_id = t.ticket_id and t.ticket_id = "+ticket_id+" order by c.creation_time desc")
        for cmt in commentRows:
            comment = {}
            comment['creation_time'] = cmt[0]
            comment['comment'] = cmt[1]
            comment['created_by'] = cmt[2]
            comment['type'] = cmt[3]
            comments.append(comment) 
        jsonString = json.dumps(comments)
        
        print jsonString
        return jsonString

# Adding Work notes by ISS Staff
@app.route('/tickets/<ticket_id>/notes',methods = ['POST', 'GET'])
def noteForTicket(ticket_id):
    if request.method == 'POST': 
        note = request.form['note']
        createdBy = session['username']#request.form['createdBy'] #replace with session user
        conn = get_db()
        conn.execute("INSERT INTO NOTES(TICKET_ID, CREATED_BY, NOTE) VALUES( %s, \'%s\', \'%s\' )" %(ticket_id,createdBy,note))
        conn.commit()
        return "Work note inserted"
    else:
        notes = []
        noteRows = execute_query("select N.CREATION_TIME, N.NOTE, N.CREATED_BY,case when T.staff_name == N.created_by then 'WORKER' else 'OTHER' end as 'TYPE' from NOTES N, TICKETS T  where T.TICKET_ID=N.TICKET_ID and T.ticket_id = "+ticket_id+" order by N.creation_time desc")
        print noteRows
        for note in noteRows:
            workNote = {}
            workNote['creation_time'] = note[0]
            workNote['note'] = note[1]
            workNote['created_by'] = note[2]
            workNote['type'] = note[3]
            notes.append(workNote) 
        jsonString = json.dumps(notes)
        
        print jsonString
        return jsonString
# Displaying the file in the Staff and User view
@app.route('/download/<filename>',methods = ['GET'])
def downloadFile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Rendering ISS Create Ticket template
@app.route('/createTicket.html')
def createTicket():
	return render_template('createTicket.html',username = session['username'])

@app.route('/createTicket_GBP.html')
def createTicketGBP():
	return render_template('createTicket_GBP.html',username = session['username'])
	
@app.route('/createTicket_IT.html')
def createTicketIT():
	return render_template('createTicket_IT.html',username = session['username'])
	


# ISS CreateTicket form
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
                nm = request.form['CreatedBy']
                summ = request.form['Summary']
                cat = request.form['Category']
                pri = request.form['Priority']
                Dept = request.form['Department']
                desc = request.form['Description']
                oldFiles = request.form['OldFiles']
		filename=""
		files = request.files.getlist('file')
		#print files
		uniqueid =str(uuid.uuid4())
		for file in files:
			if file.filename != '':
                        	f = file
                        	filename = filename+(uniqueid+"_"+f.filename+",")
                        	fname = uniqueid+"_"+f.filename
				f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(fname)))
				
                	else:
   				filename=None
   			
   			if oldFiles != '':
				filename=oldFiles+filename
            
            	conn = sqlite3.connect('/var/www/html/flaskapp/AskBronco.db')
            	cur = conn.cursor()
            	cur.execute("""INSERT INTO TICKETS(CREATED_BY, PRIORITY, DEPARTMENT, CATEGORY, SUMMARY, DESCRIPTION,FILE_NAME) VALUES("%s","%s","%s","%s","%s","%s","%s")""" %(nm,pri,Dept,cat,summ,desc,filename))
            	conn.commit()
		rows = execute_query("""SELECT *  FROM TICKETS WHERE CREATED_BY ="%s" ORDER BY TICKET_ID DESC Limit 1"""%(nm))
            	for row in rows:
                       ticketNo=row[0]
            	return render_template ("result.html", msg = ticketNo)
	    	 

@app.route('/updateRec',methods = ['POST'])
def updateRec():
    print request.method
    if request.method == 'POST':   	 
        nm = request.form['CreatedBy']
        summ = request.form['Summary']
        cat = request.form['Category']
        pri = request.form['Priority']
        Dept = request.form['Department']
        desc = request.form['Description']
        oldFiles = request.form['OldFiles']
        ticketId=request.form['TicketId']

        
        filename=""
	files = request.files.getlist('file')
	uniqueid =str(uuid.uuid4())
	for file in files:
		if file.filename != '':
                        f = file
                        filename = filename+(uniqueid+"_"+f.filename+",")
                        fname = uniqueid+"_"+f.filename
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(fname)))
				
                else:
   			filename=filename.append(None)
   	
   	
        

        if oldFiles is not None:
            filename=oldFiles+filename
        
        conn = get_db()
        query = "UPDATE TICKETS SET PRIORITY=\'%s\', DEPARTMENT=\'%s\', CATEGORY=\'%s\', SUMMARY=\'%s\', DESCRIPTION=\'%s\',FILE_NAME=\'%s\' WHERE TICKET_ID=\'%s\'  " %(pri,Dept,cat,summ,desc,filename,ticketId)
        print query
        conn.execute(query)
        conn.commit()
        
        print 'after commit'
        
        return "Success"                          
	    	 
# ISS File upload from form	             
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = str(uuid.uuid4())+f.filename
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(filename)))

# Routing to results template from ISS Create Ticket
@app.route('/result')
def get_ticketnumber():
        tno = execute_query("""SELECT TICKET_ID  FROM (SELECT *  TICKETS WHERE USERNAME = session['username'] ORDER BY date(creation_time) DESC Limit 1""")
        return render_template('result.html', msg = tno)	

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

''' ISS Staff '''

# Staff my team ticket summary list    
@app.route('/ISSticketsummary.html')
def  loadISStickets():
        return render_template('ISSticketsummary.html', username = session['username'])
        
@app.route('/GBPticketsummary.html')
def  loadGBPtickets():
        return render_template('GBPticketsummary.html', username = session['username'])
        
@app.route('/ITticketsummary.html')
def  loadITtickets():
        return render_template('ITticketsummary.html', username = session['username'])

@app.route('/ticketsummaryselectionstaff', methods=['GET'])
def get_staffticketsummaryselection():
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        username = session['username']
        dept = get_db().execute('SELECT DEPT_ID FROM STAFF  WHERE STAFF_NAME="%s"' %(username))
        print dept
        #rows = get_db().execute("""SELECT * FROM TICKETS WHERE  CATEGORY LIKE "%s" AND PRIORITY LIKE "%s" AND DEPARTMENT = '%s'""" %(category,status,dept))
        rows = get_db().execute("""SELECT * FROM TICKETS T, STAFF S WHERE  T.CATEGORY LIKE "%s" AND T.STATUS LIKE "%s"  AND S.STAFF_NAME LIKE "%s" AND T.DEPARTMENT = S.DEPT_ID ORDER BY CREATION_TIME DESC""" %(category,status,username))
        ticketssummary=[]

        for row in rows:
            ticketsummary = {}
            ticketsummary['TICKET_ID']=row[0]
            ticketsummary['CREATION_TIME']=row[2]
            ticketsummary['STATUS']=row[4]
            ticketsummary['PRIORITY']=row[5]
            ticketsummary['CATEGORY']=row[7]
            ticketsummary['SUMMARY']=row[8]


            ticketssummary.append(ticketsummary)
        jsonString = json.dumps(ticketssummary)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)
    except:
            e = sys.exc_info()[0]
            return e  
                  
# Staff my ticket  list    
@app.route('/Staffticket.html')
def  loadstafftickets():
        return render_template('Staffticket.html', username = session['username'])    
        
@app.route('/Staffticketselection', methods=['GET'])
def get_Staffticketselection():
    try: 
        
        username = session['username']
        print username
        rows = get_db().execute("""SELECT * FROM TICKETS T, STAFF S WHERE  T.STATUS like 'In Progress'  AND S.STAFF_NAME LIKE "%s" AND S.DEPT_ID = T.DEPARTMENT""" %(username))
        Stafftickets=[]
        for row in rows:
            Staffticket = {}
            Staffticket['TICKET_ID']=row[0]
            Staffticket['CREATION_TIME']=row[2]
            Staffticket['STATUS']=row[4]
            Staffticket['PRIORITY']=row[5]
            Staffticket['CATEGORY']=row[7]
            Staffticket['SUMMARY']=row[8]
            
            
            Stafftickets.append(Staffticket)    
        jsonString = json.dumps(Stafftickets)
        print jsonString
        return jsonString  
    except:
            e = sys.exc_info()[0]
            return e                  

@app.route('/dash_tickets', methods=['GET'])
def getOpen_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='Open' AND DEPARTMENT='ISS'""")
        for row in rows:
            ticket_open = {}
            ticket_open['open']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString              
    except:
            e = sys.exc_info()[0]
            return e
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'''' ISS Dashboard '''

@app.route('/student_dash.html')
def student_dash():
        return render_template('student_dash.html')

@app.route('/manager_home.html')
def manager_home():
     return render_template('manager_home.html')
     
@app.route('/wip_tickets', methods=['GET'])
def getWIP_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='In Progress'AND DEPARTMENT='ISS'""")
        for row in rows:
            ticket_open = {}
            ticket_open['wip']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/area_ticket1234', methods=['GET'])
def getAreae_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE DEPARTMENT='ISS'""")
        tickets1=[]
        for row in rows:
            ticket1 = {}
            ticket1['Year']=row[0]
            ticket1['Status']=row[1]
            ticket1['count']=row[2]
            tickets1.append(ticket1)
        jsonString = json.dumps(tickets1)
        print jsonString
        return jsonString                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/total', methods=['GET'])
def getTotal_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS""")
        for row in rows:
            ticket_total = {}
            ticket_total['total']=row[0]
        jsonString = json.dumps(ticket_total)
        print jsonString
        return jsonString              
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/close_tickets', methods=['GET'])
def getClosed_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='Closed' AND DEPARTMENT='ISS'""")
        for row in rows:
            ticket_open = {}
            ticket_open['closed']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/dept', methods=['GET'])
def getDept_tickets():
    try:
        rows=  execute_query("""SELECT STAFF_NAME,count(TICKET_ID) FROM TICKETS WHERE DEPARTMENT="ISS" AND STATUS="Closed" AND STAFF_NAME IS NOT NULL GROUP BY STAFF_NAME""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['STAFF']=row[0]
            ticket['Count']=row[1]
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/bar_open', methods=['GET'])
def getBar_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE STATUS='Open' AND DEPARTMENT= 'ISS' GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/bar_close', methods=['GET'])
def getBarClose_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE STATUS='Closed' AND DEPARTMENT='ISS' GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
                    
    except:
            e = sys.exc_info()[0]
            return e

               
@app.route('/bar_open1', methods=['GET'])
def getBar1_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE DEPARTMENT="ISS" GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
'''extra
@app.route('/comments', methods=['GET'])
def getcomments():
    try:
        rows = execute_query("""select count (*) FROM TICKETS INNER JOIN COMMENTS ON TICKETS.TICKET_ID=COMMENTS.TICKET_ID WHERE DEPARTMENT='ISS'""")
        for row in rows:
            ticket_open = {}
            ticket_open['comments']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
'''
@app.route('/turnaround', methods=['GET'])
def getturnaround():
    try:
        rows = execute_query("""select  (julianday (CLOSED_TIME) - julianday (CREATION_TIME) ) * 24 AS Turnaround,CATEGORY from tickets where DEPARTMENT= "ISS"  GROUP BY CATEGORY """)
 	tickets=[]
        for row in rows:
            ticket = {}
            ticket['Turnaround']=row[0]
            ticket['Category']=row[1]
           # ticket['count']=row[2]
	    tickets.append(ticket)
        #print jsonString
	jsonString = json.dumps(tickets)
        return jsonString                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/total_dept', methods=['GET'])
def getTotal_Dept_tickets():
    try:
        rows=  execute_query("""select DEPARTMENT,count(*) from TICKETS GROUP BY DEPARTMENT""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Department']=row[0]
            ticket['Count']=row[1]
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
'''GBP Dashboard'''

@app.route('/gbp_dash.html')
def gbp_dash():
        return render_template('gbp_dash.html')
@app.route('/gbpopendash_tickets', methods=['GET'])
def getgbpOpen_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='Open' AND DEPARTMENT='GBP'""")
        #tickets_open=[]
        for row in rows:
            ticket_open = {}
            ticket_open['open']=row[0]
            #ticket['created_by']=row[1]
           # ticket['creation_time']=row[2]
           # ticket['status']=row[3]
           # ticket['priority']=row[4]
            #ticket['category']=row[5]
           # ticket['sub_category']=row[6]




        #tickets_open.append(ticket_open)
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/gbpwip_tickets', methods=['GET'])
def getgbpWIP_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='In Progress'AND DEPARTMENT='GBP'""")
        #tickets_open=[]
        for row in rows:
            ticket_open = {}
            ticket_open['wip']=row[0]
            #ticket['created_by']=row[1]
           # ticket['creation_time']=row[2]
           # ticket['status']=row[3]
           # ticket['priority']=row[4]
            #ticket['category']=row[5]
           # ticket['sub_category']=row[6]




        #tickets_open.append(ticket_open)
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/gbpclose_tickets', methods=['GET'])
def getgbpClosed_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='Closed' AND DEPARTMENT='GBP'""")
        #tickets_open=[]
        for row in rows:
            ticket_open = {}
            ticket_open['closed']=row[0]
            #ticket['created_by']=row[1]
           # ticket['creation_time']=row[2]
           # ticket['status']=row[3]
           # ticket['priority']=row[4]
            #ticket['category']=row[5]
           # ticket['sub_category']=row[6]




        #tickets_open.append(ticket_open)
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/gbpdept', methods=['GET'])
def getgbpDept_tickets():
    try:
        rows=  execute_query("""SELECT STAFF_NAME,count(TICKET_ID) FROM TICKETS WHERE DEPARTMENT="GBP" AND STAFF_NAME IS NOT NULL GROUP BY STAFF_NAME""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['STAFF']=row[0]
            ticket['Count']=row[1]
            '''ticket['creation_time']=row[2]
            ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/gbpbar_open', methods=['GET'])
def getgbpBar_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE STATUS='Open' AND DEPARTMENT= 'GBP' GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            '''ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/gbpbar_close', methods=['GET'])
def getgbpBarClose_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE STATUS='Closed' AND DEPARTMENT='GBP' GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            '''ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/gbpbar_open1', methods=['GET'])
def getgbpBar1_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE DEPARTMENT="GBP" GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            '''ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/gbpturnaround', methods=['GET'])
def getgbpturnaround():
    try:
        rows = execute_query("""select ( (julianday (CLOSED_TIME) - julianday (CREATION_TIME) ) * 24/count(*)) AS Turnaround,CATEGORY from tickets where DEPARTMENT= "GBP"  GROUP BY CATEGORY ORDER BY Turnaround DESC""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Turnaround']=row[0]
            ticket['Category']=row[1]
           # ticket['count']=row[2]
            tickets.append(ticket)
        #print jsonString
        jsonString = json.dumps(tickets)
        return jsonString
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/it_dash.html')
def it_dash():
        return render_template('it_dash.html')
@app.route('/itopendash_tickets', methods=['GET'])
def getitOpen_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='Open' AND DEPARTMENT='IT'""")
        #tickets_open=[]
        for row in rows:
            ticket_open = {}
            ticket_open['open']=row[0]
            #ticket['created_by']=row[1]
           # ticket['creation_time']=row[2]
           # ticket['status']=row[3]
           # ticket['priority']=row[4]
            #ticket['category']=row[5]
           # ticket['sub_category']=row[6]




        #tickets_open.append(ticket_open)
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/itwip_tickets', methods=['GET'])
def getitWIP_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='In Progress'AND DEPARTMENT='IT'""")
        #tickets_open=[]
        for row in rows:
            ticket_open = {}
            ticket_open['wip']=row[0]
            #ticket['created_by']=row[1]
           # ticket['creation_time']=row[2]
           # ticket['status']=row[3]
           # ticket['priority']=row[4]
            #ticket['category']=row[5]
           # ticket['sub_category']=row[6]




        #tickets_open.append(ticket_open)
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/itclose_tickets', methods=['GET'])
def getitClosed_tickets():
    try:
        rows = execute_query("""SELECT count(*) FROM TICKETS WHERE STATUS='Closed' AND DEPARTMENT='IT'""")
        #tickets_open=[]
        for row in rows:
            ticket_open = {}
            ticket_open['closed']=row[0]
            #ticket['created_by']=row[1]
           # ticket['creation_time']=row[2]
           # ticket['status']=row[3]
           # ticket['priority']=row[4]
            #ticket['category']=row[5]
           # ticket['sub_category']=row[6]




        #tickets_open.append(ticket_open)
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e 
@app.route('/itdept', methods=['GET'])
def getitDept_tickets():
    try:
        rows=  execute_query("""SELECT STAFF_NAME,count(TICKET_ID) FROM TICKETS WHERE DEPARTMENT="IT" AND STAFF_NAME IS NOT NULL GROUP BY STAFF_NAME""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['STAFF']=row[0]
            ticket['Count']=row[1]
            '''ticket['creation_time']=row[2]
            ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/itbar_open', methods=['GET'])
def getitBar_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE STATUS='Open' AND DEPARTMENT= 'IT' GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            '''ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)     
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/itbar_close', methods=['GET'])
def getitBarClose_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE STATUS='Closed' AND DEPARTMENT='IT' GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            '''ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/itbar_open1', methods=['GET'])
def getitBar1_tickets():
    try:
        rows = execute_query("""select CAST(CREATION_TIME AS DATE),STATUS,COUNT(*) from TICKETS WHERE DEPARTMENT="IT" GROUP BY  CAST(CREATION_TIME AS DATE),STATUS""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Year']=row[0]
            ticket['Status']=row[1]
            ticket['count']=row[2]
            '''ticket['status']=row[3]
            ticket['priority']=row[4]
            ticket['category']=row[5]
            ticket['sub_category']=row[6]
            ticket['summary']=row[7]
            ticket['description']=row[8]
            ticket['staff_name']=row[9]
'''
            tickets.append(ticket)
        jsonString = json.dumps(tickets)
        print jsonString
        return jsonString
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/itturnaround', methods=['GET'])
def getitturnaround():
    try:
        rows = execute_query("""select ( (julianday (CLOSED_TIME) - julianday (CREATION_TIME) ) * 24/count(*)) AS Turnaround,CATEGORY from tickets where DEPARTMENT= "IT"  GROUP BY CATEGORY ORDER BY Turnaround DESC""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Turnaround']=row[0]
            ticket['Category']=row[1]
           # ticket['count']=row[2]
            tickets.append(ticket)
        #print jsonString
        jsonString = json.dumps(tickets)
        return jsonString
    except:
            e = sys.exc_info()[0]
            return e


@app.route('/isspopcat', methods=['GET'])
def getisspopcat():
    try:
        rows = execute_query("""select CATEGORY,count(*) from TICKETS where DEPARTMENT= "ISS" GROUP BY CATEGORY""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Category']=row[0]
            ticket['Count']=row[1]
           # ticket['count']=row[2]
            tickets.append(ticket)
        #print jsonString
        jsonString = json.dumps(tickets)
        return jsonString
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/gbppopcat', methods=['GET'])
def getgbppopcat():
    try:
        rows = execute_query("""select CATEGORY,count(*) from TICKETS where DEPARTMENT= "GBP" GROUP BY CATEGORY""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Category']=row[0]
            ticket['Count']=row[1]
           # ticket['count']=row[2]
            tickets.append(ticket)
        #print jsonString
        jsonString = json.dumps(tickets)
        return jsonString
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/itpopcat', methods=['GET'])
def getitpopcat():
    try:
        rows = execute_query("""select CATEGORY,count(*) from TICKETS where DEPARTMENT= "IT" GROUP BY CATEGORY""")
        tickets=[]
        for row in rows:
            ticket = {}
            ticket['Category']=row[0]
            ticket['Count']=row[1]
           # ticket['count']=row[2]
            tickets.append(ticket)
        #print jsonString
        jsonString = json.dumps(tickets)
        return jsonString
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/comments', methods=['GET'])
def getcomments():
    try:
        rows = execute_query("""select count (*) FROM TICKETS INNER JOIN COMMENTS ON TICKETS.TICKET_ID=COMMENTS.TICKET_ID WHERE DEPARTMENT='ISS'""")
        for row in rows:
            ticket_open = {}
            ticket_open['comments']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e    
@app.route('/gbp_comments', methods=['GET'])
def getgbpcomments():
    try:
        rows = execute_query("""select count (*) FROM TICKETS INNER JOIN COMMENTS ON TICKETS.TICKET_ID=COMMENTS.TICKET_ID WHERE DEPARTMENT='GBP'""")
        for row in rows:
            ticket_open = {}
            ticket_open['comments']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e
@app.route('/it_comments', methods=['GET'])
def getitcomments():
    try:
        rows = execute_query("""select count (*) FROM TICKETS INNER JOIN COMMENTS ON TICKETS.TICKET_ID=COMMENTS.TICKET_ID WHERE DEPARTMENT='IT'""")
        for row in rows:
            ticket_open = {}
            ticket_open['comments']=row[0]
        jsonString = json.dumps(ticket_open)
        print jsonString
        return jsonString
        #return jsonify(tickets=tickets)                
    except:
            e = sys.exc_info()[0]
            return e

@app.route('/logout')
def logout():
        session.pop('username' , None) 
        return render_template('login.html')



if __name__ == '__main__':
  app.run() 
