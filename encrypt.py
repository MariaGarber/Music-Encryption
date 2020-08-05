from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import json
import os

def generate_key():
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator) #generate pub and priv key
    return key

def encrypt(key,msg):
    pubkey=RSA.import_key(key)
    encryptor = PKCS1_OAEP.new(pubkey.publickey())
    encrypted = encryptor.encrypt(bytes(msg, 'utf8'))
    with open("file.txt", "w") as write_file:
        write_file.write(str(encrypted))
    #message to encrypt is in the above line 'encrypt this message'

def get_data():
    if (os.path.exists("./data_file.json")):
        with open("data_file.json") as read_file:
            data = json.load(read_file)
        read_file.close()
    else:
        data = {}
    return data
def register(username,password):
    data = get_data()
    if (dict(data).get(username) != None):
        return False
    else:
        pub=generate_key()
        temp=str(pub.publickey().exportKey().decode())
        data1 = {username: {
            'pass': password,
            'pubkey': temp
            }
        }
        data1.update(data)
        with open("data_file.json", "w") as write_file:
            json.dump(data1, write_file,indent=2)
        write_file.close()
        return pub.exportKey(),pub.publickey().exportKey()
      #  msg="hello word"
       # encrypt(pub,msg)

def login(username,password):
    data = dict(get_data())
    if (data.get(username) != None):
        if(data.get(username)['pass']==password):
            return True
    else:
        return False

def regenerate(username):
    data = dict(get_data())
    pub = generate_key()
    temp = str(pub.publickey().exportKey().decode())
    data[username]['pubkey']=temp
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file, indent=2)
    return pub.exportKey(), pub.publickey().exportKey()
