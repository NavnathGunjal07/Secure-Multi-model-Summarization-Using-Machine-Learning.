import json
from watson_developer_cloud import SpeechToTextV1
import objectpath
import requests
global temppath1

iam_apikey_v = "i4aEpD1RkuiOXHGKQULGyFMT4eMv20dDNQX8bVHpSBDd"
url_v = "https://gateway-lon.watsonplatform.net/speech-to-text/api"

temppath1="C:\\Users\\smart\\Desktop\\upload"

def convert_Audio():

	try:
		stt = SpeechToTextV1(iam_apikey=iam_apikey_v, url=url_v)
		audio_file = open(temppath1+"\\data1.wav", "rb")

		print("ng\n")

		with open(temppath1+"\\data1.json", 'w') as fp:
			result = stt.recognize(audio_file, content_type="audio/wav",continuous=True,timestamps=False,max_alternatives=1,smart_formatting=True)
			print(json.dump(result.get_result(),fp,indent=2))

		print("R\n")
		with open(temppath1+"\\data1.json") as datafile:
			data = json.load(datafile)

		jsonnn_tree = objectpath.Tree(data['results'])
		result_tuple = tuple(jsonnn_tree.execute('$..transcript'))

		print("A\n")

		f=open(temppath1+"\\audiodata.txt","w")
		f.write(" ".join(result_tuple))
		f.close()
				
		print("\nK")

		f = open(temppath1+'\\audiodata.txt','r')
		u=f.read()
		data = {
			'text': u
		}
		
		
		print("S")
		response = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
		print(response.text)
		x=response.text
		print("customized text:"+x)

		file = open(temppath1+'\\audiodata.txt','w')
		file.write(x)
		file.close()

		
		return x

	except:
		file = open(temppath1+'\\audiodata.txt','w')
		file.write("something went wrong")
		file.close()
		return "something went wrong"
		