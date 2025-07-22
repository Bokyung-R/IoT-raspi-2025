from flask import Flask, render_template, request

app = Flask(__name__)

contacts = []

@app.route('/')
def index():
	return render_template('add.html')

@app.route('/submit', methods=['POST'])
def submit():
	name = request.form.get('name')
	phone = request.form.get('phone')
	email = request.form.get('email')
	contacts.append({'name':name, 'phone':phone,'email':email})
	return f"<h3>입력완료 : {name} - {phone} - {email}</h3><br><a href='/'>돌아가기 </a>"

@app.route('/list', methods=['GET'])
def list():
	result = "<h2>회원정보</h2>"
	result += "<table border=1 ><tr><th>이름</th><th>전화번호</th><th>이메일</th>"

	for i in range(len(contacts)):
		result += f"<tr><td>{contacts[i]['name']}</td><td>{contacts[i]['phone']}</td><td>{contacts[i]['email']}</td></tr>"

	result += f"</table>"

	return result

if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
