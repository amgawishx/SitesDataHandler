from AES256 import AESCipher as AES
from hashlib import sha512
import time, os, re
import numpy as np
class Database:
    '''
    A class for creating and handling database objects and associated files
    \nkey <====> a string for encrypting/decrypting database information
    '''
    def __init__(self, key):
        if key==None: # enforcing key necessity
            print("\nError: A register key must be supplied")
            exit()
        self.keys = open("keys.db","r").read() # reading registered keys database
        if not sha512(key.encode()).hexdigest() in self.keys: # asserting the validation of the supllied key
            print("\nError: Incorrect/Unregistered key.")
            exit()
        else:
            self.key = key
        self.dbtemp = """website: {site}
key: {key}
datestamp: {date}
username: {username}
password: {password}
------------------------
""" # a template for a database object
        self.datetemp = "{hour}:{min}:{sec} {day}/{month}/{year}" # a template for timestamp
        self.charlib = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
        'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
        '2', '3', '4', '5', '6', '7', '8', '9', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '/'] # characters' set
        self.cipher = AES(self.key) # the encrypting/decrypting cipher
    def registerSite(self, site, username, password=None, randPass=False, N=False): # a method for registering a new site data
        if randPass: # creating a random characters password
            password = self.__generatePass(N)
        try: # ensuring the existance of a database file and creating a new one if not
            assert "<DirEntry 'sitesdata.db'>" in [str(entry) for entry in os.scandir()]
        except AssertionError:
            decision = input("Database file not found. Do you want to create a new one? (y/n) ")
            if decision=="y": pass
            elif decision=="n": exit()
            else: print("Error: unknown option."); exit()
        with open("sitesdata.db","a") as file: # writing to the database file
            data = self.dbtemp.format(
                site = site, date = self.__getDate(), username = self.__encrypt(username), password = self.__encrypt(password), key = sha512(self.key.encode()).hexdigest()
            )
            file.write(data)
            file.close()
            print("\nSuccessful data site register!")
    def registerKey(self, key): # a method for registering a new encryption key in the keys data base
        try: # ensuring the existance of a keys file and creating a new one if not
            assert "<DirEntry 'keys.db'>" in [str(entry) for entry in os.scandir()]
        except AssertionError:
            decision = input("\nKeys file not found. Do you want to create a new one? (y/n) ")
            if decision=="y": pass
            elif decision=="n": exit()
            else: print("\nError: unknown option."); exit()
        with open("keys.db","a") as file: # writing to the keys file
            key = sha512(key.encode()).hexdigest()
            file.write(key)
            file.close()
            print("\nSuccessful key register!")
    def retrieve(self, site): # a method for retrieving site's data
        with open("sitesdata.db","r") as file: # reading the database file
            file.seek(0)
            reader = file.read()
            file.close()
        try: # asserting the existance of the requested site
            siteSpan = self.__find("{site}".format(site = site))(reader).span()
        except:
            print("\nError: site not found in the database.")
            exit()
        data = ''; Data=[]
        for i in range(siteSpan[0],len(reader)):
            if str(reader[i])!="-": data+=str(reader[i])
            else: break
        data = data.splitlines()
        for line in data:
            nwline=line.replace("website: ","").replace("username: ","").replace("datestamp: ","").replace("password: ","").replace("key: ","")
            Data.append(nwline)
        site = Data[0]
        key = Data[1]
        if key != sha512(self.key.encode()).hexdigest():
            print("\nERROR: YOU HAVE USED THE WRONG REGISTER KEY FOR THIS DATABASE ENTRY.")
        date = Data[2]
        username = self.__decrypt(Data[3])
        password = self.__decrypt(Data[4])
        printable = self.dbtemp.format(
                site = site, date = date, username = username, password = password, key = key
            )
        return printable
    def __getDate(self): # a utility method for creating timestamp
        l = time.localtime()
        date = self.datetemp.format(
            year = l.tm_year, month = l.tm_mon, day = l.tm_mday,
            hour = l.tm_hour, min = l.tm_min, sec = l.tm_sec
        )
        return date
    def __find(self, word): # a utility method for searching for the requested site within the database
        match = re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search
        return match
    def __encrypt(self, string): # a utility method for encrypting data
        return self.cipher.enc(string).decode()
    def __decrypt(self, cipher): # a utility method for decrypting data
        return self.cipher.dec(cipher)
    def __generatePass(self, length): # a utility method for generating random characters string
        password = ''
        for i in range(length):
            password += np.random.choice(self.charlib)
        return password
