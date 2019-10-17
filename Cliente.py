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
		session['username'] = response['users'][0]['username']
		session['nome'] = response['users'][0]['nome']
		return redirect(url_for('inicio'))
		
	return render_template('signin.html')
	
@app.route('/criar', methods=['GET', 'POST'])
def criar():
	if request.method == 'POST':
		username = request.form['username']
		nome = request.form['nome']
		response = requests.post('http://localhost:5000/api/user', json={'username': username, 'nome': nome}).json()
		session['username'] = response['users']['username']
		session['nome'] = response['users']['nome']		
		return redirect(url_for('inicio'))
		
	return render_template('criar.html')
	
@app.route('/inicio')
def inicio():
	if not session['username']:
		return render_template('signin.html')
		
	response = requests.get('http://localhost:5000/api/topico').json()['topicos']
	
	proprios = requests.get('http://localhost:5000/api/topico/' + session['username']).json()['topicos']
	comentarios = requests.get('http://localhost:5000/api/comentario').json()['comentarios']

	return render_template('inicial.html', topicos=response, proprios=proprios, comentarios = comentarios)
	
@app.route('/apagar/<int:id>')
def apagar(id):
	requests.delete('http://localhost:5000/api/topico/' + str(id))
	return redirect(url_for('inicio'))

@app.route('/comentar/<int:id>', methods=['GET', 'POST'])	
def comentar(id):
	data = {'username': session['username'], 'comentario': request.form['comentario']}
	requests.post('http://localhost:5000/api/comentario/' + str(id), json=data)
	return redirect(url_for('inicio'))
	
@app.route('/postar', methods=['GET', 'POST'])	
def postar():
	data = {'autor': session['username'], 'titulo': request.form['titulo'], 'descricao': request.form['descricao']}
	requests.post('http://localhost:5000/api/topico', json=data)
	return redirect(url_for('inicio'))
	
if __name__ == '__main__':
    app.run(port = 5001, debug = True)
