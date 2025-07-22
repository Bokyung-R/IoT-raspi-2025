from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def helloworld():
	return "hello world"

@app.route('/name')
def name():
	return "<h1>My name is Hong Kil-dong</h1>"

@app.route('/age')
def age():
	return "<h1>my age is 30 yesr's old</h1>"

if __name__=="__main__":
	app.run(host='0.0.0.0', debug=True)
