from pymongo import MongoClient
import os

ssh_address = 'ec2-user@ec2-3-19-68-203.us-east-2.compute.amazonaws.com'
ssh_user = 'ec2-user'
ssh_port = 22

private_key = "/home/wmansey/SENG533Official.pem"

mongo_username = 'pythonAccessUser'
mongo_password = 'RhMD!=7wX?FbD@$'


def connect_to_mongo():
   try:
        print('E')
        print(os.getcwd())
        client = MongoClient("mongodb://"+mongo_username+":"+mongo_password+"@" + ssh_address, ssl = True, ssl_keyfile = private_key)
        db = client.myDB
        print('1')
        #Should 'admin' be there or 'myDB'? 'admin' at least get if(auth) passed, while 'myDB' doesn't 
        auth = client.admin.authenticate(mongo_username,mongo_password) 

        if(auth):
                print("MongoDB connection successful")
                col = db.myCollection.count()
        else:
                print("MongoDB authentication failure: Please check the username or password")

        client.close()

   except Exception as e:
        print("MongoDB connection failure: Please check the connection details")
        print(e)

if __name__ == "__main__":
    connect_to_mongo()
