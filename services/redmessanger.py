from pwn import *
from random import randint
import sys

def get_flag(host, port, flag_id, token):
        c = remote(host,port)
        c.sendline("LOGIN " + flag_id + " " + token)
        c.recvline()
        c.recvline()
        c.sendline("READ " + flag_id + "_0")
        c.recvline()
        c.recvline()
        c.recvline()
        c.recvline()
        c.recvline()
        data = c.recvline()
        c.sendline("EXIT")
        c.close()
        data = data[:-1]
        return data
        
def set_flag(host, port, flag):
        #print("flag set: " + flag)
        flag_id = genFlagID()
        password = genPasswd()
        c = remote(host,port)
        c.sendline("NEW " + flag_id + " " + password)
        c.recvline()
        c.recvline()
        c.sendline("LOGIN " + flag_id + " " + password)
        c.recvline()
        c.recvline()
        c.sendline("SEND " + flag_id)
        c.recvline()
        c.recv(9)
        c.sendline("flag")
        data = c.recvline()
        c.sendline(flag + "\n.\n")
        c.sendline("EXIT")
        c.close()
        return {"flag_id": flag_id, "token":password}

def genFlagID():
        rang = randint(4,8)
        flag_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return flag_id

def genPasswd():
        rang = randint(8,16)
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rang))
        return password
