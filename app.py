#html related
from flask import Flask,render_template,request,redirect,session
app=Flask(__name__)
app.secret_key='mpes'

@app.route('/')
def Homepage():
    return render_template('homepage.html')
#db related
from pymongo import MongoClient as mc
client=mc('127.0.0.1',27017)
db=client['bloodmanagement'] #for storing user details during the registration process
ucollection=db['ucollection']
bdcollection=db['bdcollection']
#for registration page


@app.route('/registerpage')
def registerpage():
    return render_template('register.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/searchpage')
def searchpage():
    return render_template('search.html')

@app.route('/homepage')
def homepage():
    return render_template('loginuserpage.html')
#to print the user details after login
@app.route('/userdetails')
def userdetailspage():
    data=[]
    for i in ucollection.find({'email':session['username']}):
        dummy=[]
        dummy.append(i['name'])
        dummy.append(i['email'])
        dummy.append(i['Mob'])
        dummy.append(i['Aadhar'])
        dummy.append(i['Password'])
        data.append(dummy)

    return render_template('userdetails.html',data=data,l=len(data))
#Register page
@app.route('/register',methods=['POST'])
def Register():
    name=request.form['uname']
    email=request.form['email']
    Mob=request.form['Mob']
    Aadhar=request.form['Aadhar']
    Password=request.form['Password']
    CPassword=request.form['CPassword']
    #print(name,email,Mob,Aadhar,Password,CPassword)
    if Password!=CPassword:    #checking the passwords entered
        return render_template('register.html',err='Please enter correct password')
    for i in ucollection.find({'email':email}):
        if i['email']==email:   #checking if the user is already registered
            return render_template('login.html',res='You are already registered')
    #check for existing email
    u={}
    print(name,email,Mob,Aadhar,Password,CPassword)
    u['name']=name
    u['email']=email
    u['Mob']=Mob
    u['Aadhar']=Aadhar
    u['Password']=Password
    ucollection.insert_one(u)   #adding it the user collection 
    return render_template('login.html',res='Registered Successfully')
            
#for login page
@app.route('/login',methods=['POST'])
def Login():
    email=request.form['email']
    Password=request.form['Password']
    for i in ucollection.find({'email':email}):   #check if the user details are correct
        print(i)
        if i['Password']!=Password:
            return render_template('login.html',err='Enter correct Password')

    session['username']=email        
    #return redirect('/userdetails')
    return render_template('loginuserpage.html',res='Log in Successful')
        
    #for i in ucollection.find():
        #if i in ucollection ['email']==email:
            #return render_template('login.html',res='you already registered')
        #else:
            #return render_template('loginuserpage.html')
    
#for search page
@app.route('/search',methods=['POST'])
def search():
    Bgroup=request.form['Bgroup']
    data=[]
    for i in bdcollection.find({'BGroup':Bgroup}):
        print(i)
        if i['BGroup']==Bgroup:
            dummy=[]
            dummy.append(i['name'])
            dummy.append(i[' address'])
            try:
                dummy.append(i['number'])
            except:
                dummy.append('No')
            try:
                dummy.append(i['Availability'])
            except:
                dummy.append('No')
            try:
                dummy.append(i['BGroup'])
            except:
                dummy.append('No')
            data.append(dummy)
    return (render_template('displayavail.html',data=data,l=len(data)))
#for home page after login
@app.route('/userdetails',methods=['POST'])
def userdetails():
    print(ucollection.find())

@app.route('/logout')
def logoutPage():
    session['username']=None
    return redirect('/')

if (__name__)=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)


