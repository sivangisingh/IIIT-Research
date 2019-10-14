from flask import render_template
from flask import url_for,redirect,session
from flask import request,flash
from datetime import datetime
import sqlite3
import os.path
import flask
from werkzeug import secure_filename
from app import app

app.secret_key = "Ramukaka"
 
app.config['UPLOAD_FOLDER']="research_paper"


def upload_file(post_id):
	if request.method == 'POST':
		try:
			f = request.files['file']
			f.filename=str(post_id)+".pdf"
			f.save("app/research_paper/"+secure_filename(f.filename))
    # return redirect(url_for('index'))
		except:
			return "No file inserted"
def file(filename):
    try:
    	return flask.send_file(
    	'research_paper/'+filename,  
    	'application/pdf',
    	as_attachment=True,
    	attachment_filename=filename
    	)
    except:
    	# flash("No File inserted!!!")
    	return redirect(url_for('index',id=session['userID']))

@app.route('/show_file/<filename>')
def file_show(filename):
	if session['user_logged_in']==True:
	    return file(filename)
	return redirect(url_for('login'))


@app.route('/insert_post',methods=['POST'])
def insert_post():
	if request.method=='POST' :
		researcharea=request.form['research_area']
		lab_id=request.form.get('lab')
		prof_id=request.form.get('prof')
		post_text=request.form.get('post_content')
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(BASE_DIR, "project.db")
		conn = sqlite3.connect(db_path)
		try : 
			if not request.files['file']=='':
				file_present="yes"
		except:
			file_present="no"

	 	conn.text_factory = str
		if session['type'][0]=="professor":
			prof_id=session['userID']
			student_id=""
			post_person_id=prof_id
		else:
			post_person_id=session['userID']
			student_id=session['userID']
		t =(student_id,researcharea,lab_id,prof_id,post_text,datetime.now(),post_person_id,0,file_present)
		c=conn.cursor()
		try :
			c.execute("INSERT into post (student_id,researcharea,lab,prof_id,post_text,time,post_person_id,vote_count,file_present) values(?,?,?,?,?,?,?,?,?) ", t )
			conn.commit()
			li=c.execute("SELECT post_id from post ORDER BY post_id DESC limit 1")
			li=c.fetchall()
			# post_id=li[0]
			# f = request.files['file']
   #    		f.filename=post_id+".pdf"
   #    		f.save("app/research_paper"+secure_filename(f.filename))
			upload_file(li[0])
			conn.close()
			return redirect(url_for('index'))
		except sqlite3.IntegrityError:
			conn.close()
			return "Post can't be inserted "



@app.route('/lab_info/<name>')
def lab_info(name):
    if session['user_logged_in']==True:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "project.db")
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        t=(name,)
        c=conn.cursor()
        li=c.execute("SELECT id,name,native From login where name like ? ",t)
        li=c.fetchall()
        lab_posts=lab_p(name)
        prof=list_prof(name)
        conn.close()
        return render_template('lab_page.html',id=session['userID'],lab=li[0],prof=prof,lab_posts=lab_posts)
    return redirect(url_for('login'))

def lab_p(name):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t=(name,)
	c=conn.cursor()
 	li=c.execute("SELECT * From post where lab like ? ORDER BY time desc",t)
	li=c.fetchall()
	conn.close()
	return li	


@app.route('/index')
def index():
	if session['user_logged_in']==True:	
		lis=list_following()
		posts=show_post()
		lab_list = list_lab()
		all_prof=all_professor()
		vote_result=[]
		for post in posts:
			check=[]
			check.append(post)
			check.append(liked(post[0]))
			vote_result.append(check)
		return render_template('index.html',id=session['userID'],lis=lis,lab_list = lab_list,all_prof=all_prof,vote_result=vote_result)
	return	redirect(url_for('login'))

@app.route('/timeline')
def timeline():
	if session['user_logged_in']==True:
		if session['type'][0]=="student":
			posts=show_timeline(session['userID'])
		else:
			posts=student_under_me(session['userID'])
		if len(posts)==0:
			return render_template('timeline_noPost.html',id=session['userID'])
		return render_template('timeline.html',id=session['userID'],posts=posts)
	return	redirect(url_for('login'))
	
@app.route('/update')
def update():
    if session['user_logged_in']==True:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "project.db")
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        t=(session['userID'],)
        c=conn.cursor()
        li=c.execute("SELECT * From login where id = ? ",t)
        li=c.fetchall()
        conn.close()
        return render_template('update.html',id=session['userID'],li=li[0])
    return    redirect(url_for('login'))
   
@app.route('/update_info', methods=['POST','GET'])
def update_info():
    if request.method=='POST' or request.method=='GET':
        id=session['userID']
        name=request.form.get('name')
        password=request.form.get('pass')
        native=request.form.get('native')
        dob=request.form.get('dob')
        update_login(id,name,password,native,dob)
        return redirect(url_for('about',id=id))


def update_login(id,name,password,native,dob):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "project.db")
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    t =(name,password,native,dob,id)
    c=conn.cursor()
    try :
        c.execute("update login set name=?, password=?,native=?,dob=? where id=?", t)
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return "User id doesn't exists"


@app.route('/lab')
def lab():
	if session['user_logged_in']==True:
		li=list_lab()
		return render_template('lab.html',id=session['userID'],li=li)
	return	redirect(url_for('login'))

@app.route('/about/<id>')
def about(id):
	if session['user_logged_in']==True:
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(BASE_DIR, "project.db")
		conn = sqlite3.connect(db_path)
		conn.text_factory = str
		c=conn.cursor()
		names=(id,)
		t=(session['userID'],id,)
		li=c.execute("SELECT * FROM follow WHERE follower = ? and following=?" , t )
		li=c.fetchall()
		followed=1
		if len(li) == 0 :
			followed=0
		lin=c.execute("SELECT name,type,native,dob,id FROM login WHERE id= ?",names)
		lin=c.fetchall()
		lis=list_follower(id)
		posts=show_timeline(id)
		for li in lin:
			return render_template('about.html',id=session['userID'],li=li,followed=followed,lis=lis,posts=posts)
	return	redirect(url_for('login'))


@app.route('/about_lab/<lab_name>')
def about_lab(lab_name):
	if session['user_logged_in']==True:
		prof_li=list_prof(lab_name)
		return render_template('professor.html',id=session['userID'],prof_li=prof_li)
	return	redirect(url_for('login'))


@app.route('/trending')
def trending():
    if session['user_logged_in']==True:
        profs=most_followed_prof()
        posts=most_voted_post()
        labs=most_publications_labs()
        vote_result=[]
        for post in posts:
        	check=[]
        	check.append(post)
        	check.append(liked(post[0]))
        	vote_result.append(check)
    	return render_template('trending.html',id=session['userID'],vote_result=vote_result,profs=profs,labs=labs)
    return    redirect(url_for('login'))
# def trending():
# 	if session['user_logged_in']==True:
# 		return render_template('trending.html',id=session['userID'])
# 	return	redirect(url_for('login'))


@app.route('/professor')
def professor():
    if session['user_logged_in']==True:
        prof_li = all_professor()
        return render_template('professor.html',id=session['userID'],prof_li= prof_li)
    return    redirect(url_for('login'))

@app.route('/')	
@app.route('/login')
def login():
	if 'user_logged_in' in session and session['user_logged_in']==True:
		return redirect(url_for('index',id=session['userID']))
	# flash("invalid credentials")
	return render_template('login.html')

@app.route('/registration')
def registration():
	return render_template('registration.html',li=list_lab())

@app.route('/follow/<id2>')
def follow(id2):
	if session['user_logged_in']==True:
		return insert_follow(id2=id2,id1=session['userID'])
	return render_template('login.html')


def list_following():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(session['userID'],)
 	li=c.execute("SELECT name,id from login where id IN (SELECT following FROM follow where follower=?)",t)
	li=c.fetchall()
	conn.close()
	return li

def list_follower(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(id,)
 	li=c.execute("SELECT name,id from login where id IN (SELECT follower FROM follow where following=?)",t)
	li=c.fetchall()
	conn.close()
	return li 
	
def insert_login(id,name,password,type,lab):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t =(id,name,password,type,lab)
	c=conn.cursor()
	try :
		c.execute("INSERT into login (id,name,password,type,lab) values(?,?,?,?,?) ", t )
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "User id already exists"
	#li=c.execute("SELECT * FROM login" )
	#print [l for l in li]






def insert_follow(id2,id1):
 	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
 	conn.text_factory = str
	t =(id2,id1)
	l=(id2,)
	c=conn.cursor()
	print id1,id2
	try :
		c.execute("INSERT into follow (following,follower) values(?,?) ", t )
		c.execute("UPDATE login set no_of_followers=no_of_followers+1 where id=?",l)
		conn.commit()
		conn.close()
		return redirect(url_for('about',id=id2))
	except sqlite3.IntegrityError:
		conn.close()
		return redirect(url_for('about',id=id2))


def check_user(id,password):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "project.db")
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    t =(id,password)
    c=conn.cursor()
    li=c.execute("SELECT * FROM login WHERE id = ? and password=?" , t )
    li=c.fetchall()
    if len(li) == 0 :
        return "Invaild credentials!"
    else :
        return True
    conn.close()

def show_post():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t=(session['userID'],session['userID'],)
	c=conn.cursor()
 	li=c.execute("SELECT * From post where post_person_id in (SELECT following FROM follow WHERE follower = ?) OR post_person_id==? ORDER BY time desc",t)
	li=c.fetchall()
	conn.close()
	return li

def student_under_me(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t=(id,)
	c=conn.cursor()
 	li=c.execute("SELECT * From post where prof_id = ? ORDER BY time desc",t)
	li=c.fetchall()
	conn.close()
	return li


def show_timeline(id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	t=(id,)
	c=conn.cursor()
 	li=c.execute("SELECT * From post where post_person_id = ? ORDER BY time desc",t)
	li=c.fetchall()
	conn.close()
	return li

@app.errorhandler(404)
def http_404_handler(error):
    return render_template('404.html')

def list_lab():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT DISTINCT lab FROM login where lab!='None'")
	li=c.fetchall()
	conn.close()
	return li

def list_prof(lab):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(lab,)
 	li=c.execute("SELECT name,id FROM login where lab like ? and type='professor'",t)
	li=c.fetchall()
	conn.close()
	return li


def most_voted_post():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT * FROM post ORDER BY vote_count DESC limit 10")
	li=c.fetchall()
	
	conn.close()
	return li


def most_followed_prof():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT name,id,no_of_followers FROM login where type='professor' ORDER BY no_of_followers DESC limit 10")
	li=c.fetchall()
	conn.close()
	return li

def most_publications_labs():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT lab ,COUNT(*) FROM post GROUP BY lab ORDER BY COUNT(*) DESC limit 10  ")
	li=c.fetchall()
	conn.close()
	return li

@app.route('/vote_count_increment/<post_id>')
def vote_count_increment(post_id):
	if session['user_logged_in']==True:
		increase_vote_count(session['userID'],post_id)
		return redirect(url_for('login'))
	return redirect(url_for('login'))


def increase_vote_count(id,post_id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(post_id,)
	t1=(post_id,id)
	try:
		c.execute("UPDATE post set vote_count=vote_count+1 where post_id=?",t)
		c.execute("INSERT into vote_table (post_id,voted_person_id) values (?,?) ", t1 )
	except:
		return "Error"	
	conn.commit()
	conn.close()
	
def liked (post_id):
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	id=session['userID']
	t1=(post_id,id)
	li=c.execute("SELECT * from vote_table where post_id=? and voted_person_id=?", t1 )
	li=c.fetchall()
		# conn.commit()
	conn.close()
	if len(li)==1:
		return str('T')
	else:
		return str('F')

@app.route('/registrationNext',methods=['POST'])
def registrationNext():
	if request.method=='POST' :
		id=request.form["id"]
		name=request.form["name"]
		password=request.form["password"]
		type=request.form["type"]
		if type=="student":
			lab=""
		elif type=="professor":
			lab=request.form["lab"]
		if insert_login(id,name,password,type,lab)==True:
			return redirect(url_for('login'))
		else:	
			# flash("User id already Exits!!")
			return redirect(url_for('registration'))

def type_find():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	t=(session['userID'],)
	li=c.execute("SELECT type from login where id=? ",t)
	li=c.fetchall()
	# print li
	conn.close()
	return li[0]

@app.route('/loginNext',methods=['POST'])
def loginNext():
    if request.method=='POST':
        id=request.form["id"]
        password=request.form["password"]
        if check_user(id,password)==True:
            session['user_logged_in']=True
            session['userID']=id
            session['type']=type_find()
            return redirect(url_for('index',id=session['userID']))
        else :
            # flash( "Invaild credentials!")
            return redirect(url_for('login'))			

@app.route('/logout')
def logout():
	session['user_logged_in']=False
	session.pop('userID',None)
	return render_template('login.html')

@app.route('/read_search',methods=['POST','GET'])
def read_search():
    if request.method=='POST' or request.method=='GET':
        search_name = request.form.get("search_box")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "project.db")
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        t = (search_name,)
        c = conn.cursor()
        student_list = c.execute("SELECT * FROM login WHERE name like ? and type='student'",t)
        student_list = c.fetchall()
        prof_list=c.execute("SELECT * FROM login WHERE name like ? and type='professor'",t)
        prof_list=c.fetchall()
        lab_list = c.execute("SELECT DISTINCT  lab FROM login WHERE lab like ?",t)
        lab_list=c.fetchall()
        i_list = c.execute("SELECT * FROM post WHERE researcharea like ? ",t)
        i_list = c.fetchall()
        return render_template('search.html',id=session['userID'],prof_list=prof_list,student_list=student_list,i_list=i_list,lab_list=lab_list)
        conn.close()    

def all_professor():
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect(db_path)
	conn.text_factory = str
	c=conn.cursor()
	li=c.execute("SELECT name,id from login where type='professor'")
	li=c.fetchall()
	# print li
	conn.close()
	return li
