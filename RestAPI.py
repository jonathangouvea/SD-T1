#!flask/bin/python
from flask import Flask, jsonify, make_response, request, abort
from Wrapper import *

app = Flask(__name__)

tsUser = TSUser()
tsTopico = TSTopico()
tsComentario = TSComentario()

@app.route('/')
def index():
    return "Hello, World!"
    
@app.route('/api/user', methods=['GET'])
def get_users():
    print("## GET_USERS")
    tuplas = tsUser.queryUser(None)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
        'id': t[1][0],
        'username': t[1][1],
        'nome': t[1][2]
        })
    return jsonify({'users': tuplas_json})
    
@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    print("## GET_USER {0}".format(username))
    tuplas = tsUser.queryUser(username)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
                                'id': t[1][0],
                                'username': t[1][1],
                                'nome': t[1][2]
        })
    return jsonify({'users': tuplas_json})
    
@app.route('/api/user', methods=['POST'])
def post_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    print("## POST_USER (id, {0}, {1})".format(request.json['username'], request.json['nome']))
    id = tsUser.addUser(request.json['username'], request.json['nome'])
    novoUser = {
        'id': id,
        'username': request.json['username'],
        'nome': request.json['nome']
    }
    
    return jsonify({'users': novoUser})
    
@app.route('/api/user/<username>', methods=['PUT'])
def put_user(username):
    if not request.json:
        abort(400)

    print("## PUT_USER {0}".format(username))
    tuplas = tsUser.getUser(username)[1]
    
    username = request.json.get('username', tuplas[1])
    nome = request.json.get('nome', tuplas[2])
    print("\t## {0} -> {1}".format(tuplas, (tuplas[0], username, nome)))
    tsUser.addUserId(tuplas[0], username, nome)
        
    tuplas = tsUser.queryUser(username)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
                                'id': t[1][0],
                                'username': t[1][1],
                                'nome': t[1][2]
        })
    return jsonify({'users': tuplas_json})
    
@app.route('/api/user/<username>', methods=['DELETE'])
def delete_user(username):
    print("## DELETE_USER {0}".format(username))    
    tuplas = [tsUser.getUser(username)]
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
                                'id': t[1][0],
                                'username': t[1][1],
                                'nome': t[1][2]
        })
    return jsonify({'users': tuplas_json})
    
###

@app.route('/api/topico', methods=['GET'])
def get_topicos():
    print("## GET_TOPICOS")
    tuplas = tsTopico.queryTopico(None)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
            'id': t[1][0],
            'titulo': t[1][1],
            'autor': t[1][2],
            'descricao': t[1][3],
            'time': t[1][4]
        })
    return jsonify({'topicos': tuplas_json})
    
@app.route('/api/topico/<int:id>', methods=['GET'])
def get_topico(id):
    print("## GET_TOPICO ID#{0}".format(id))
    tuplas = tsTopico.queryTopico(id)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
            'id': t[1][0],
            'titulo': t[1][1],
            'autor': t[1][2],
            'descricao': t[1][3],
            'time': t[1][4]
        })
    return jsonify({'topicos': tuplas_json})
    
@app.route('/api/topico_autor/<autor>', methods=['GET'])
def get_topico_autor(autor):
    print("## GET_TOPICO AUTOR {0}".format(autor))
    tuplas = tsTopico.queryTopicoAutor(autor)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
            'id': t[1][0],
            'titulo': t[1][1],
            'autor': t[1][2],
            'descricao': t[1][3],
            'time': t[1][4]
        })
    return jsonify({'topicos': tuplas_json})
    
@app.route('/api/topico', methods=['POST'])
def post_topico():
    if not request.json or not 'titulo' in request.json:
        abort(400)
    print("## POST_TOPICO (id, {0}, {1}, {2})".format(request.json['titulo'], request.json['autor'], request.json['descricao']))
    id = tsTopico.addTopico(request.json['titulo'], request.json['autor'], request.json['descricao'])
    novoTopico = {
        'id': id,
        'titulo': request.json['titulo'],
        'autor': request.json['autor'],
        'descricao': request.json['descricao'],
        'time': '0'
    }
    
    return jsonify({'topicos': novoTopico})
    
@app.route('/api/topico/<int:id>', methods=['PUT'])
def put_topico(id):
    if not request.json:
        abort(400)

    print("## PUT_TOPICO ID#{0}".format(id))
    tuplas = tsTopico.getTopico(id)[1]
    
    titulo = request.json.get('titulo', tuplas[1])
    autor = request.json.get('autor', tuplas[2])
    descricao = request.json.get('descricao', tuplas[3])
    
    print("\t## {0} -> {1}".format(tuplas, (tuplas[0], titulo, autor, descricao, tuplas[4])))
    tsTopico.addTopicoId(tuplas[0], titulo, autor, descricao)
        
    tuplas = tsTopico.queryTopico(tuplas[0])
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
            'id': t[1][0],
            'titulo': t[1][1],
            'autor': t[1][2],
            'descricao': t[1][3],
            'time': t[1][4]
        })
    return jsonify({'topicos': tuplas_json})
    
@app.route('/api/topico/<int:id>', methods=['DELETE'])
def delete_topico(id):
    print("## DELETE_TOPICO ID#{0}".format(id))    
    tuplas = [tsTopico.getTopico(id)]
    if tuplas == [None]:
        return not_found(404)
    tuplas_json = []
    for t in tuplas:
        tuplas_json.append({
            'id': t[1][0],
            'titulo': t[1][1],
            'autor': t[1][2],
            'descricao': t[1][3],
            'time': t[1][4]
        })
    return jsonify({'topicos': tuplas_json})
    
###

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
