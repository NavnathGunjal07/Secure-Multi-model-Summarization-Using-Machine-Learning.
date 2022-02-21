from flask import *
from flask import Flask, flash, redirect, render_template, \
     request, url_for
     
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('image.html')
    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)