from flask import *
from flask import Flask, flash, redirect, render_template, \
     request, url_for
from text_summarize import *
from audio_summarize import *
from user import *
from video_summarize import *
import os
global temppath,temppath1

app = Flask(__name__)
temppath="C:\\Users\\Smart\\Desktop\\Project\\pro\\summ\\app\\static"
temppath1="C:\\Users\\Smart\\Desktop\\upload"

def removefiles():
	if(os.path.isfile(temppath1+'\\data1.txt')):
		os.remove(temppath1+"\\data1.txt")
		print("dtrs")
	
	if(os.path.isfile(temppath1+'\\data1.wav')):
		os.remove(temppath1+'\\data1.wav')

	if(os.path.isfile(temppath1+'\\data1.json')):
		os.remove(temppath1+'\\data1.json')

	if(os.path.isfile(temppath1+'\\audiodata.txt')):	
		os.remove(temppath1+'\\audiodata.txt')

	if(os.path.isfile(temppath1+'\\sumdata.txt')):	
		os.remove(temppath1+'\\summdata.txt')


	if(os.path.isfile(temppath1+'\\sumdata.txt')):	
					os.remove(temppath1+'\\summdata.txt')


@app.route('/')
def index():
	
	removefiles()
	return render_template('about.html')
	
	
@app.route("/storedata" , methods=['GET', 'POST'])
def storedata():
	global email
	global pwd
	login=request.form.get('login')
	signup=request.form.get('signup')
	email=request.form.get('email') 
	pwd=request.form.get('psw')
	forget=request.form.get('forgetpass')

	page=user_login(login,signup,email,pwd)
	print(page)
	if(page=="login.html"):
		removefiles()
		return render_template("login.html",error="Enter valid data either email or password wrong")

	elif(page=="Please Verify your email"):
		print("unverified")
		removefiles()
		return render_template("login.html",error="Verify your email")

	elif str(forget)=="FORGETPASS":
		print("You are in forgot")
		return render_template('forgot.html')

	else:
		return render_template(page)
	#elif(page==s)


@app.route("/forgotfunction" , methods=['GET','POST'])
def forgotfunction():

	print(url_for('forgotfunction'))

	forgotpass=request.form.get('forgotpass')
	login=request.form.get('login')
	print(forgotpass)

	if login=='Login':
		print("login")
		return render_template('login.html')

	else:
		if forgotpass!= None:
			if request.method=='POST':
				try:
					print("succ")
					auth.send_password_reset_email(forgotpass)
					return render_template('forgot.html',error="Password reset successfully")
				except:
					error="Enter valid E-MAIL"
					print("er")
					return render_template('forgot.html',error=error)

		else:
			return render_template('forgot.html')


@app.route("/verifyfunction" , methods=['GET','POST'])
def verifyfunction():
	print("verifyfunction")
	email=request.form.get('forgotpass')
	pwd=request.form.get('pass')
	print(email)
	print(pwd)
	login=request.form.get('login')
	#print(forgotpass)

	if login=='Login':
		print("login")
		return render_template('login.html')

	
	else:
		if email!= None:
			if pwd!=None:
				try:
					print("succ")

					user=auth.sign_in_with_email_and_password(email,pwd)
					auth.send_email_verification(user['idToken'])
					return render_template('verification.html',error="Password reset successfully")
				
				except Exception as er:
					error="Enter valid E-MAIL"
					print(er)
					return render_template('verification.html',error=error)

		else:
			return render_template('verification.html')




@app.route("/navi" , methods=['GET','POST'])
def navi():
		if request.method=='POST':

				removefiles()

				home=request.form.get('home')
				his=request.form.get('history')
				logout=request.form.get('logout')
				if str(home)=="HOME":
							return render_template('select_type.html')
				elif str(his)=="HISTORY":
					return render_template('list.html')
				elif str(logout)=="LOGOUT":
					return render_template('about.html')
				else:
					return render_template('about.html')


@app.route("/aboutnavi" , methods=['GET','POST'])
def aboutnavi():
		if request.method=='POST':

				removefiles()
				login=request.form.get('login')
				
				if str(login)=="LOGIN":
					return render_template('login.html')
				else:
					return render_template('sign.html')

@app.route("/aboutsendmessage" , methods=['GET', 'POST'])
def aboutsendmessage():
	name=request.form.get('name')
	email=request.form.get('email') 
	message=request.form.get('message')
	print("name"+name)
	print("\nemail"+email)
	print("\nmessage"+message)

	fp=open("file.txt","w+")
	fp.write("Name:"+name)
	fp.write("\nEmail-id:"+email)
	fp.write("\nMessage:"+message)
	fp.close()
	
	#path="TEXT"
	email=email.replace(".com","")
	print(email)
	upload_file=(email+'.txt')
	upload_file_path=str("ADMIN/"+upload_file)
	
	var=storage.child(upload_file_path).put("file.txt")
	
	return render_template('about.html',error="Feedback submitted successfully")

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
	global email
	global pwd
	name=request.form.get('name')
	email=request.form.get('email') 
	pwd=request.form.get('psw')
	cpwd=request.form.get('cpwd')
	
	page=user_signup(email,pwd,cpwd)
	#error="Pwd and cpwd should same"

	print("\nstart:/signup")
	print("page"+page)
	if(page=="sign.html"):
		print("\nif")
		if(pwd==cpwd):
			print("\n inner if")
			if(len(pwd)<6):
				print("\nleng")
				return render_template("sign.html",error="Password length should be 6  or greater than that!")
			else:
				print("\leng else")
				return render_template("sign.html",error="Email id already registered!")
		else:
			print("\nbigger else")
			return render_template("sign.html",error="Password and confirm password should be same")


	
	elif(page=='login.html'):
		print("biggest else")
		return render_template("login.html",error="resend link")


@app.route("/select" , methods=['GET', 'POST'])
def select():
	text=request.form.get('text')
	audio=request.form.get('audio') 
	video=request.form.get('video')
	view=request.form.get('view')
	
	if str(text)=="TEXT":
		text1="TEXT"
		return render_template('browsetext.html',selection=text1)
	elif str(audio)=="AUDIO":
		text2="AUDIO"
		return render_template('browseaudio.html',selection=text2)
	elif str(video)=="VIDEO":
		text2="VIDEO"
		return render_template('video.html',selection=text2)
	elif str(view)=="VIEW":
		text3="VIEW"
		return render_template('list.html',selection=text3)
	
@app.route("/video" , methods=['GET', 'POST'])
def video():
	data=request.form.get('see_data')

	if(os.path.isfile(temppath+'\\data1.mp4')):
		print("abc")
		if(os.path.isfile(temppath+'\\s.srt')):
			print("def")
			get_summary(temppath+'\\data1.mp4', temppath+'\\s.srt')
			return render_template('video.html')

	else:
		print("ghi")
		error='file not found'
		return render_template('video.html',error=error)


@app.route("/video1" , methods=['GET', 'POST'])
def video1():	
	btn1=request.form.get('av')
	btn2=request.form.get('sv')
	print("ARchana")
	print(str(btn1))
	if str(btn1)=="Actual Video":
		selection="/static/data1.mp4"

	else:
		selection="/static/data1_1.mp4"

	return render_template('video.html',selection=selection)

@app.route("/videosummarize" , methods=['GET', 'POST'])
def videosummarize():
	return render_template('video.html')

@app.route("/textsummarize" , methods=['GET', 'POST'])
def textsummarize():
	text4='TEXT'
	return render_template('browsetext.html',selection=text4)


@app.route("/audiosummarize" , methods=['GET', 'POST'])
def audiosummarize():
	text4='AUDIO'
	return render_template('browseaudio.html',selection=text4)



@app.route("/display_list_text_audio" , methods=['GET','POST'])
def display_list_text_audio():
	print("clicked")
	if request.method=='POST':
		global email

		btn1=request.form.get('text')
		btn2=request.form.get('audio')

		
		if str(btn1)=="Display_text":
			selection="TEXT"

		else:
			selection="AUDIO"


		list_keys=list()
		list_val=list()
		
		todo=db.child(email.replace(".com","")).child(selection).get()

		print(selection)
		try:
			for l in todo.each() :
				list_keys.append([l.key(),l.val()])
				print(l.key()+"\n")
				print(l.val()+"\n")


			return render_template('list.html',t=list_keys,selection=selection)
		
		except Exception as e:
			print(e)
			return render_template('list.html',error='No files are summarized yet')


@app.route("/decrypt_TEXT" , methods=['GET','POST'])
def decrypt_TEXT():
	global pwd
	#btn=request.form.get('btn')
	btn=request.form.get('myid')
	print("button"+str(btn)+" ")
	print(btn)
	user_pwd=request.form.get('psw')
	print("\npassword"+pwd)
	print("\npassword_user"+user_pwd)
	if request.method=='POST':
		if user_pwd==pwd:

			global email

			list_keys=list()
			list_val=list()
			todo=db.child(email.replace(".com","")).child("TEXT").get()

			for l in todo.each() :
				list_keys.append([l.key(),l.val()])

				print(l.key()+"\n")
				if(btn==l.key()):
					result = os.popen("curl "+l.val()).read()
					decrypted_data=decrypt(result,pwd)
					file = open(temppath1+'\\summdata.txt','w')
					file.write(decrypted_data)
					file.close()
					print("here")
				
			return render_template('list.html',error=decrypted_data)

		else:
			return render_template('list.html',error="Incorrect key entered")

@app.route("/decrypt_AUDIO" , methods=['GET','POST'])
def decrypt_AUDIO():
	global pwd
	btn=request.form.get('btn')
	print("button"+str(btn))
	user_pwd=request.form.get('psw')
	print("\npassword"+pwd)
	print("\npassword_user"+user_pwd)
	if request.method=='POST':
		if user_pwd==pwd:

			global email

			list_keys=list()
			list_val=list()
			todo=db.child(email.replace(".com","")).child("AUDIO").get()

			for l in todo.each() :
				list_keys.append([l.key(),l.val()])



				print(l.key()+"\n")

				if(str(btn)==l.key()):
					result = os.popen("curl "+l.val()).read()
					decrypted_data=decrypt(result,pwd)
					file = open(temppath1+'\\summdata.txt','w')
					file.write(decrypted_data)
					file.close()
					print("here")
				
			return render_template('list.html',error=decrypted_data)

		else:
			return render_template('list.html',error="Incorrect key entered")


@app.route("/upload_data" , methods=['GET','POST'])
def upload_data():

	global email
	global path
	global data2
	global pwd


	if (path=='TEXT'):
		if(os.path.isfile(temppath1+'\\data1.txt')):
			file = open(temppath1+'\\data1.txt', 'r')
			data1 = file.read()
			file.close()

			summarized_data=view_summary(data1)
			data2=''
			for item in summarized_data:
				data2= data2+item

			file=request.form.get('file')
			print("rr :"+file)

			hidden_field=request.form.get('hidden_field')
			path=str(hidden_field)
			
			print("path"+path)


			upload_file=(file+'.txt')
			print("\nupload_file"+upload_file)

			user_upload(data2,upload_file,email,path,pwd)
				
			print("summary"+data2)
			return render_template('browsetext.html',selection=path,error='Data uploaded successfully!!')

		else:
				return render_template('browsetext.html',selection=path,error="File not found")


	else:
		if(os.path.isfile(temppath1+'\\audiodata.txt')):
			file = open(temppath1+'\\audiodata.txt', 'r')
			data1 = file.read()
			file.close()

			summarized_data=view_summary(data1)
			data2=''
			for item in summarized_data:
				data2= data2+item

			file=request.form.get('file')
			print("rr :"+file)

			hidden_field=request.form.get('hidden_field')
			path=str(hidden_field)
			
			print("path"+path)


			upload_file=(file+'.txt')
			print("\nupload_file"+upload_file)

			user_upload(data2,upload_file,email,path,pwd)
				
			print("summary"+data2)
			return render_template('browseaudio.html',selection=path,error='Data uploaded successfully!!')


		elif(os.path.isfile(temppath1+'\\data1.wav')):
			converted_data=convert_Audio()
			file = open(temppath1+'\\audiodata.txt', 'r')
			data1 = file.read()
			file.close()

			summarized_data=view_summary(data1)
			data2=''
			for item in summarized_data:
				data2= data2+item

			file=request.form.get('file')
			print("rr :"+file)

			hidden_field=request.form.get('hidden_field')
			path=str(hidden_field)
			
			print("path"+path)


			upload_file=(file+'.txt')
			print("\nupload_file"+upload_file)

			user_upload(data2,upload_file,email,path,pwd)
				
			print("summary"+data2)
			return render_template('browseaudio.html',selection=path,error='Data uploaded successfully!!')



		else:
				return render_template('browseaudio.html',selection=path,error="File not found")

@app.route("/data_or_summary" , methods=['GET','POST'])
def data_or_summary():
	global pwd
	global path
	global data2
	data2 = ""
	tempfile=request.form.get('myfile')

	data=request.form.get('see_data')
	summary=request.form.get('see_summary') 
	hidden_field=request.form.get('hidden_field')
	path=str(hidden_field)

	
	if (str(data)=="view data in the file") and (str(hidden_field)=="TEXT"):
		
		if(os.path.isfile(temppath1+'\\data1.txt')):
			file = open(temppath1+'\\data1.txt', 'r')
			data1 = file.read()
			file.close()
			return render_template('browsetext.html',data1=data1,selection="TEXT")

		else:
			return render_template('browsetext.html',selection="TEXT",error="File not found")


	elif (str(summary)=="View Summary") and (str(hidden_field)=="TEXT"):


		if(os.path.isfile(temppath1+'\\data1.txt')):
			file = open(temppath1+'\\data1.txt', 'r')
			data1 = file.read()
			file.close()

			summarized_data=view_summary(data1)
			data2=''
			for item in summarized_data:
				data2= data2+item
				
			
			return render_template('browsetext.html',data1=data2,data2=data2,selection="TEXT")

		else:
			return render_template('browsetext.html',selection="TEXT",error="File not found")
			
		
	elif(str(data)=="view data in the file") and (str(hidden_field)=="AUDIO"):

		if(os.path.isfile(temppath1+'\\audiodata.txt')):
			file = open(temppath1+'\\audiodata.txt', 'r')
			converted_data = file.read()
			file.close()
			return render_template('browseaudio.html',data1=converted_data,selection="AUDIO")


		elif(os.path.isfile(temppath1+'\\data1.wav')):
			converted_data=convert_Audio()
			return render_template('browseaudio.html',data1=converted_data,selection="AUDIO")

		else:
			return render_template('browseaudio.html',selection="AUDIO",error="File not found")
		

	elif(str(summary)=="View Summary") and (str(hidden_field)=="AUDIO"):
		if(os.path.isfile(temppath1+'\\audiodata.txt')):
			file = open(temppath1+'\\audiodata.txt', 'r')
			data1 = file.read()
			file.close()

			summarized_data=view_summary(data1)
			data2=''
			for item in summarized_data:
				data2= data2+item

			return render_template('browseaudio.html',data1=data2,selection="AUDIO")

		elif(os.path.isfile(temppath1+'\\data1.wav')):
			converted_data=convert_Audio()
			file = open(temppath1+'\\audiodata.txt', 'r')
			data1 = file.read()
			file.close()

			summarized_data=view_summary(data1)
			data2=''
			for item in summarized_data:
				data2= data2+item

			return render_template('browseaudio.html',data1=data2,selection="AUDIO")


		else:
			return render_template('browseaudio.html',selection="AUDIO",error="File not found")
		
	
	else:
		return "Something went wrrong"
	

		
if __name__=='__main__':
    app.run(debug=True)