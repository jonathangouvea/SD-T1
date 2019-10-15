from flask import Flask, render_template, g, redirect, flash, Blueprint, request, session, url_for
import requests

app = Flask(__name__)

app.config.from_mapping(
		SECRET_KEY='dev'
	)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		username = request.form['username']
		response = requests.get('http://localhost:5000/api/user/' + username).json()
		print(response)
		session['username'] = response['users'][0]['username']
		session['nome'] = response['users'][0]['nome']
		print(session['username'])
		return redirect(url_for('inicio'))
		
	return render_template('signin.html')
	
@app.route('/inicio')
def inicio():
	if not session['username']:
		return render_template('signin.html')
	return render_template('inicial.html')
	
if __name__ == '__main__':
    app.run(port = 5001, debug = True)
