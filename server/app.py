import uuid
from pprint import pprint as pp
from flask import Flask, jsonify, request
from flask_cors import CORS
import docker


DEBUG = True
CONTAINERS = []


app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_container(container_id):
    for c in CONTAINERS:
        if c['id'] == container_id:
            CONTAINERS.remove(c)

            return True

    return False

def start_container(container_id):
    container = client.containers.get(container_id)
    container.start

    return True

@app.route('/containers', methods=['GET', 'POST'])
def all_containers():
    response_object = {'status': 'success'}
    
    if request.method == 'POST':
        post_data = request.get_json()
        input_docker_image = post_data.get('image')
        
        # Validando o input do usuário
        if input_docker_image == None:
            response_object['status'] =  'failure'
            response_object['log'] = 'Empty docker image name.'

            return jsonify(response_object)

        else:
            # Criando e iniciando a imagem no container
            try:
                container = client.containers.create(image=input_docker_image, auto_remove=False)
                container.start()

                CONTAINERS.append({
                    'id': container.short_id,
                    'image': container.image.tags[0]
                })
                response_object['containers'] = CONTAINERS

            except:
                response_object['status'] = 'failure'
                response_object['log'] = 'Wrong image name.'

            return jsonify(response_object)

    else:
        response_object['containers'] = CONTAINERS
    
        return jsonify(response_object)




@app.route('/containers/<container_id>', methods=['POST', 'PUT', 'DELETE'])
def single_book(container_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        start_container(container_id)

    elif request.method == 'PUT':
        stop_container(container_id)

    elif request.method == 'DELETE':
        remove_container(container_id)

        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    # client = docker.DockerClient()
    # client = docker.from_env()
    client = docker.client.from_env()
    app.run()
