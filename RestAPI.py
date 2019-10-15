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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
