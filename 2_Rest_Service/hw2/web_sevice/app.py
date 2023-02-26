from flask import Flask, jsonify, abort, make_response, request


from products import Products

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': Products})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = list(filter(lambda pr: pr['id'] == product_id, Products))
    if len(product) == 0:
        abort(404)
    return jsonify({'Products': product[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/products', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    product = {
        'id': Products[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
    }
    Products.append(product)

    return jsonify({'products': product}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_task(product_id):
    product = list(filter(lambda pr: pr['id'] == product_id, Products))
    if len(product) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        abort(400)
    if 'description' not in request.json:
        abort(400)
    
    product[0]['name'] = request.json.get('name', product[0]['name'])
    product[0]['description'] = request.json.get('description', product[0]['description'])
    
    return jsonify({'products': product[0]})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_task(product_id):
    product = list(filter(lambda pr: pr['id'] == product_id, Products))
    if len(product) == 0:
        abort(404)
    Products.remove(product[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)