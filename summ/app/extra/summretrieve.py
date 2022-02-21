""""import requests

response = requests.post('https://firebasestorage.googleapis.com/v0/b/summarization-d8b27.appspot.com/o/anamika123%40gmail.com%2Ffiles%2Ffile.txt?alt=media&token=g123456789')
print(response.text)
x=response.text
print("customized text:"+x)

file = open('C:\\Users\\Rashmi Kabra\\Desktop\\upload\\summdata.txt','w')
file.write(x)
file.close()
"""
#import os
#x=os.system("curl https://firebasestorage.googleapis.com/v0/b/summarization-d8b27.appspot.com/o/anamika123%40gmail.com%2FAUDIO%2Fabc.txt?alt=media&token=g123456789" )
#print(x.read())

"""
import subprocess
MyOut = subprocess.Popen("curl https://firebasestorage.googleapis.com/v0/b/summarization-d8b27.appspot.com/o/anamika123%40gmail.com%2FAUDIO%2Fabc.txt?alt=media&token=g123456789", 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
stdout,stderr = MyOut.communicate()
print(stdout)
x=stdout
y=x.decode("utf-8")
print("\n"+y)

"""

import os
result = os.popen("curl https://firebasestorage.googleapis.com/v0/b/summarization-d8b27.appspot.com/o/anamika123%40gmail.com%2FAUDIO%2Fabc.txt?alt=media&token=g123456789").read()
#print(result)

file = open('C:\\Users\\Rashmi Kabra\\Desktop\\upload\\summdata.txt','w')
file.write(result)
file.close()