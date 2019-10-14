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
	# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	# db_path = os.path.join(BASE_DIR, "project.db")
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
		return "User id already exists"



if __name__ == '__main__':
	insert_post("kshitij.paliwal@students.iiit.ac.in","AI ","CVIT", "choppela@faculty.iiit.ac.in" ,"This is frist post")	
