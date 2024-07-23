# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 22:51:27 2024

@author: Emmanuel J Perez
"""

# Mod 1 - How to create a blockchain
#import lybraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

#1-create a blockchain
class Blockchain:  #the class Blockchain is created 
    
    def __init__(self): #the constructor must be created
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0') #the genesis block must be initialized
   
    def create_block(self, proof, previous_hash):
        #the block is created
        block = {'index' : len(self.chain)+1,    
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}  
        #the block is added to the chain
        self.chain.append(block)
        #the block info is returned
        return block              
        
    def get_previous_block(self):
        return self.chain[-1] #-1 is the position of the first block backwards
        
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #the puzzle could become more difficult 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            #we could increase the number of zeros to increase the dificulty 
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #the funtion of sort_keys is organice the keys of the block
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block): #the previous hash is verified
                return False
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':  #the proof is verified
                return False
            previous_block = current_block
            block_index += 1
        return True #return true if the chain is valid
    
#2-mine a block

#the web app must be created
app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
#the objet block chain must be created
blockchain = Blockchain()

#mine a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof) #the proof must be obtained 
    previous_hash = blockchain.hash(previous_block) #the previous hash must be obtained
    block = blockchain.create_block(proof, previous_hash) #the new block is created
    response = {'message' : 'you has mined a new block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']} #is the response of the server 
    
    return jsonify(response), 200  #is necesary jasonify the response and the status code is 200(Ok) 

#obtain the blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200

#verify if the chain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    validation = blockchain.is_chain_valid(blockchain.chain)
    if validation == True:
        response = {'message' : 'The chain is valid',
                    'chain' : blockchain.chain}
    else:
        response = {'message' : 'The chain is not valid'}
        
    return jsonify(response), 200  

#execute the flask app
app.run(host = '0.0.0.0', port = 5000)
