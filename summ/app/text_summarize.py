import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np
import math

encoded=''
decoded=''
text=''
stop_words=''
split_sentence=''
a=''
x=''

def token_lower(sentence):
    global stop_words
    #print("r")
    return [word.lower() for word in word_tokenize(sentence) if (word not in stop_words and word.isalpha())]

#inverse document frequency
def idf(tok_fil_sent):
	word_idf = {}
	sent_set = []
	words = set()
	num_sent = len(tok_fil_sent)
	for i in range(num_sent):
		sent_set += [set(tok_fil_sent[i])]
		words |= sent_set[i]
	words = list(words)
	for word in words:
		word_idf[word] = math.log(float(num_sent)/sum([1 for i in range(num_sent) if word in sent_set[i]]))
	return word_idf

def idf_mod_cos(sent1,sent2,word_idf):
	sent1_dict = {}
	sent2_dict = {}
	for word in sent1:
		if word in sent1_dict:
			sent1_dict[word] += 1
		else:
			sent1_dict[word] = 1
	for word in sent2:
		if word in sent2_dict:
			sent2_dict[word] += 1
		else:
			sent2_dict[word] = 1
	
	similarity = 0.0
	for word in sent1_dict:
		if word in sent2_dict:
			similarity += sent1_dict[word]*sent2_dict[word]*word_idf[word]*word_idf[word]
	similarity /= sum([(sent1_dict[word]*word_idf[word])**2 for word in sent1_dict])**-2
	similarity /= sum([(sent2_dict[word]*word_idf[word])**2 for word in sent2_dict])**-2

	return similarity

def text_rank_sent(graph,node_weights,d=.85,iter=20):
	weight_sum = np.sum(graph,axis=0)
	while iter >0:
		for i in range(len(node_weights)):
			temp = 0.0
			for j in range(len(node_weights)):
				temp += graph[i,j]*node_weights[j]/weight_sum[j]
			node_weights[i] = 1-d+(d*temp)
		iter-=1

    
def view_summary(data):
    
    print("textsumma"+data)
    top_k=2
    global sentences
    global stop_words
    global decoded
    global encoded
    global split_sentence
    global a
    global x
    
    data = data.strip().replace('\n', ' ')	

    
    sentences = sent_tokenize(data)
    
    stop_words = set(stopwords.words('english'))
    
    
    tok_fil_sent = list(map(token_lower,sentences)) 
    num_nodes = len(tok_fil_sent)
    
    word_idf = idf(tok_fil_sent)
     
    graph = np.zeros((num_nodes,num_nodes)) 
    for i in range(num_nodes):
    	for j in range(i+1,num_nodes):
    		graph[i,j] = idf_mod_cos(tok_fil_sent[i],tok_fil_sent[j],word_idf)
    		graph[j,i] = graph[i,j]
   
    node_weights = np.ones(num_nodes)
   
    text_rank_sent(graph,node_weights)
    
    
    top_index = [i for i,j in sorted(enumerate(node_weights), key=lambda x: x[1],reverse=True)[:top_k]]
    top_sentences = [sentences[i] for i in top_index]
    x=''.join(top_sentences)
    split_sentence = x.split()
    a=x.split()
    
    
    summarized_data=x.splitlines()

    return summarized_data
        


    



