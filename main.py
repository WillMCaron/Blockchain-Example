from time import time
from hashlib import sha256
import json

# The Block Chain
class BlockChain:
  def __init__(self):
    # The block chain as a list
    self.chain = []
    # Transactions pending to be added to the blockchain
    self.current_transactions = []
    # Genisis Block
    print("Creating Genesis Block")
    print()
    self.add_block(0,10,0)


  def add_block(self, proof, previous_hash = None, size=2):
    #print("Block Index:",len(self.chain))
    if len(self.current_transactions)>=size:
      block = {
        "index": len(self.chain)+1,
        "timestamp": time(),
        "transactions": self.current_transactions[:size],
        "proof": proof,
        "previous_hash": previous_hash or self.hash(self.chain[-1]),
      }
      self.current_transactions = self.current_transactions[size:]
      self.chain.append(block)
      print("Block Hash:",self.hash(block))
      print()
      print(block)
      print()
      return block  
    else:
      print("There are not enough transactions.")
      return "No"
    
  
  def add_transaction(self, sender, receiver, amount):
    transaction = {
      "sender": sender,
      "receiver": receiver,
      "amount": amount,
      "time": time()
    }
    current_hash = self.hash(transaction)
    self.current_transactions.append(current_hash)
    print("Trasaction added")
    print(transaction)
    print()
     

  def proof_of_work(self, last_proof, difficulty = 2):
    proof = 0
    while self.valid_proof(last_proof, proof, difficulty) is False:
      proof += 1
    return proof

  def mine(self, user, difficulty = 2, size = 6):
    last_block = self.last_block
    last_proof = self.last_block['proof']
    proof = self.proof_of_work(last_proof, difficulty)
    print("Block Index:",len(self.chain))
    print("Proof:",proof)
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = sha256(guess).hexdigest()
    print("Full Proof:", guess_hash)
    print()
    previous_hash = self.hash(self.last_block)
    block = self.add_block(proof,previous_hash,size=size)
    if block != "No":
      print("Rewarding Miner:")
      self.add_transaction("Admin", user, 5)
    
  @staticmethod
  def valid_proof(last_proof, proof, difficulty = 2):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "0"*difficulty
    
  @staticmethod
  def hash(item):
    combString = json.dumps(item, sort_keys=True).encode()
    return sha256(combString).hexdigest()

  @property
  def last_block(self):
    return self.chain[-1]





chain = BlockChain()
chain.add_transaction("ADMIN","Will",500)
chain.add_transaction("Will","Paige",200)
chain.add_transaction("Will","Sarah",200)
chain.add_transaction("Paige","Sarah",50)
chain.add_transaction("Will","Lucas",99.99)
chain.add_transaction("Sarah","GG",150)

#print(len(chain.current_transactions))
for i in range(2):
  chain.mine("Will",difficulty = 6, size=3)
#print(len(chain.current_transactions))
#print(chain.hash(chain.last_block))

#Move not enough transactions to mine function
