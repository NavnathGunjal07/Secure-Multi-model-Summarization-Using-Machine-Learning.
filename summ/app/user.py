import pyrebase

import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

config = {
	"apiKey": "AIzaSyD_6KSTLo__ieCYzy9ZmebwkzVPhYVHKxo",
    "authDomain": "summarization-d8b27.firebaseapp.com",
    "databaseURL": "https://summarization-d8b27.firebaseio.com",
    "projectId": "summarization-d8b27",
    "storageBucket": "summarization-d8b27.appspot.com",
    "messagingSenderId": "685549344953"
}

key= hashlib.sha256(b'16-character key').digest()

firebase = pyrebase.initialize_app(config)
email=None
auth= firebase.auth()
storage = firebase.storage()
db=firebase.database()

def user_login(login,signup,email,pwd):
	
	if str(login)=="LOGIN":
		try:
			use=auth.sign_in_with_email_and_password(email,pwd)
			tempo=auth.get_account_info(use['idToken'])
			if tempo['users'][0]['emailVerified']:
				return "select_type.html"
			else:
				error='Please Verify your email'
				return error
			
		except:	
			error="Enter valid data"
			return "login.html"
	

	elif str(signup)=="SIGNUP":
		return "sign.html"


def user_signup(email,pwd,cpwd):

	print("\nsign")
	if (pwd==cpwd):
		print("\nif")
		try:
			print('\ntry')
			user=auth.create_user_with_email_and_password(email,pwd)
			auth.send_email_verification(user['idToken'])
			
			tempo=auth.get_account_info(user['idToken'])
			
			print("\nlogin")
			return 'login.html'
			
		except Exception as e:
			print('\ncatch')
			print("\nsign")
			return 'sign.html'

	else:
		print('else\n')
		print("sign")
		return "sign.html"

def make_key(password, salt = None):
    if salt is None:
        salt = Random.new().read(8)

    key = PBKDF2(password, salt, AES.block_size, 100000)
    return (key, salt)

def encrypt(raw,key):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    raw = base64.b64encode(pad(raw).encode('utf8'))
    iv = get_random_bytes(AES.block_size)
    
    cipher = AES.new(key=key, mode= AES.MODE_CFB,iv= iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc,pwd):
    unpad = lambda s: s[:-ord(s[-1:])]

    enc = base64.b64decode(enc)
   
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))

def user_upload(summary,upload_file,email,path,pwd):

	
	encrypted_data=encrypt(summary,key)

	f= open("file.txt","wb")
	f.write(encrypted_data)
	f.close()
	print(path)
	print(type(path))
		
	upload_file_path=str(email+"/"+path+"/"+upload_file)
	var=storage.child(upload_file_path).put("file.txt")
	upload_file_url=str(storage.child(upload_file_path).get_url('g123456789'))
	print("path:"+upload_file_url)
	db.child(email.replace(".com","")).child(path).child(upload_file.replace(".txt","")).set( upload_file_url)



