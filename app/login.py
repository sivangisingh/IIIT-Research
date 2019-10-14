import sqlite3
import datetime


# def insert_login(id,name,password,type):
# 	conn = sqlite3.connect('project.db')
# 	conn.text_factory = str
# 	t =(id,name,password,type)
# 	c=conn.cursor()
# 	try :
# 		c.execute("INSERT into login values(?,?,?,?) ", t )
# 		conn.commit()
# 	except sqlite3.IntegrityError:
# 		return "User id already exists"
# 	#li=c.execute("SELECT * FROM login" )
# 	#print [l for l in li]
# 	conn.close()

# def check_user(id,password):
# 	conn = sqlite3.connect('project.db')
# 	conn.text_factory = str
# 	t =(id,password)
# 	c=conn.cursor()
# 	li=c.execute("SELECT * FROM login WHERE id = ? and password=?" , t )
# 	li=c.fetchall()
# 	if len(li) == 0 :
# 		return "No such User exists"
# 	else :
# 		return li
# 	conn.close()

def insert_post(student_id,researcharea,lab_id,prof_id,post_text):
 	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	t =(student_id,researcharea,lab_id,prof_id,post_text,datetime.datetime.now())
	c=conn.cursor()
	try :
		c.execute("INSERT into post (student_id,researcharea,lab,prof_id,post_text,time) values(?,?,?,?,?,?) ", t )
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "Post already exists"

def insert_follow(student_id,id_2):
 	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	t =(student_id,id_2)
	l=(student_id,)
	c=conn.cursor()
	try :
		c.execute("INSERT into follow (following,follower) values(?,?) ", t )
		c.execute("UPDATE login set no_of_followers=no_of_followers+1 where id=?",l)
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "already exists"



def update_login(id,name,type,password,native,dob):
	# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	# db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	t =(name,password,type,native,dob,id)
	c=conn.cursor()
	try :
		c.execute("update login set name=?, password=?,type=?,native=?,dob=? where id=?", t)
		conn.commit()
		conn.close()
		return True
	except sqlite3.IntegrityError:
		conn.close()
		return "User id already exists"
def show_post(id):
	# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	# db_path = os.path.join(BASE_DIR, "project.db")
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	t=(id,id,)
	c=conn.cursor()
	# li=c.execute("SELECT following FROM follow WHERE follower = ? ", t )
	# li=c.fetchall()
	# # t1=(li,)
 	li=c.execute("SELECT * From post where student_id in (SELECT following FROM follow WHERE follower = ?) or prof_id in (SELECT following FROM follow WHERE follower = ?) ORDER BY time desc",t)
	li=c.fetchall()
	print li
	conn.close()

def list_lab():
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT DISTINCT lab FROM login")
	li=c.fetchall()
	print li
	conn.close()

def list_prof(lab):
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	c=conn.cursor()
	t=(lab,)
 	li=c.execute("SELECT id FROM login where lab=?",t)
	li=c.fetchall()
	print li
	conn.close()	



def most_publications_labs():
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	c=conn.cursor()
 	li=c.execute("SELECT lab ,COUNT(*) FROM post GROUP BY lab ORDER BY COUNT(*) DESC limit 10 ")
	li=c.fetchall()
	print li
	conn.close()


def increase_vote_count(id,post_id):
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	c=conn.cursor()
	t=(post_id,)
	t1=(post_id,id)
	c.execute("UPDATE post set vote_count=vote_count+1 where post_id=?",t)
	c.execute("INSERT into vote_table (post_id,voted_person_id) values (?,?) ", t1 )
	conn.commit()
	conn.close()
	
def all_professor():
	conn = sqlite3.connect("project.db")
	conn.text_factory = str
	c=conn.cursor()
	li=c.execute("SELECT name,id from login where type='professor'")
	li=c.fetchall()
	# print li
	conn.close()
	return li
if __name__ == '__main__':
	# insert_post("niharika.khare@students.iiit.ac.in","AI ","SERC", "" ,"This is frist post niharika")	
	# insert_follow("chopella@faculty.iiit.ac.in","sivangi.singh@students.iiit.ac.in")
	# insert_follow("kshitij.paliwal@students.iiit.ac.in","sivangi.singh@students.iiit.ac.in")
	# show_post("sivangi.singh@students.iiit.ac.in")
	# most_publications_labs()
	# update_login("kshitij.paliwal@students.iiit.ac.in","Kshitij","student","kshitij","indore","02/09/1996")
	# increase_vote_count("kshitij.paliwal@students.iiit.ac.in",1)
	print all_professor()