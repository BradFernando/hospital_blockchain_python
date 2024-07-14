from flask import Flask, jsonify, request
from time import time
from blockchain import Blockchain, Block

app = Flask(__name__)
blockchain = Blockchain()


@app.route('/chain', methods=['GET'])
def full_chain():
    serialized_chain = [block.serialize() for block in blockchain.chain]
    response = {
        'chain': serialized_chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/add_block', methods=['POST'])
def add_block():
    values = request.get_json()
    required = ['data']
    if not all(k in values for k in required):
        return 'Missing values', 400

    data = values['data']
    new_block = Block(index=len(blockchain.chain), timestamp=time(), data=data,
                      previous_hash=blockchain.get_latest_block().hash)
    blockchain.add_block(new_block)

    response = {
        'message': f'New block has been added to the blockchain at index {new_block.index}.',
        'block': new_block.serialize(),
    }
    return jsonify(response), 201


@app.route('/validate_chain', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    response = {'is_valid': is_valid}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
