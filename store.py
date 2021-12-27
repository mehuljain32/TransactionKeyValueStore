from collections import defaultdict
import sys

def not_key():
    return None
#global key-value store
global_store = defaultdict(not_key)


#Transaction stack: every entry in here is a transaction(active/suspended)
class TransactionStack:
    def __init__(self) -> None:
        self.transaction_stack = []

    #creates a new transaction
    def pushTransaction(self):
        #push current active transaction onto local stack
        print("INFO: Starting Transaction")
        temp = Transaction()
        self.transaction_stack.append(temp)
        print(self.transaction_stack)

    #deletes a transaction from a stack
    def popTransaction(self):
        if len(self.transaction_stack) == 0:
            print("ERROR: No active transactions")
            return False
        else:
            self.transaction_stack.pop()

    #returns the active transaction
    def peek(self):
        return self.transaction_stack[-1]

    #commit to global store as well as local store
    def commit(self):
        active = self.transaction_stack[-1] if self.check() else None
        if active:
            print("local store: ", active.local_store)  
            for key,value in active.local_store.copy().items():
                global_store[key] = value
                print("global store: ", global_store)
                if active.local_store[key]:
                    print("key: ", key)
                    active.local_store[key] = value
        else:
            print("INFO: Nothing to commit")
            return False

    #rollback deletes all keys from local_store
    def rollback(self):
        if self.transaction_stack[-1] == None:
            print("ERROR: No Active transaction")
            return False
        else:
            del(self.transaction_stack[-1].local_store)

    #counself.transaction_stack all keys
    def count(self):
        active = self.transaction_stack[-1] if self.check() else None

        if not active:
            print(len(global_store))
        else:
            print(len(active.local_store))

    def check(self):
        if len(self.transaction_stack) > 0:
            return True
        else:
            return False


#Every transaction has iself.transaction_stack own store
class Transaction:
    def __init__(self) -> None:
        self.local_store = defaultdict(not_key)

#retrieve a key
def getKey(key, ts: TransactionStack):
    active = ts.transaction_stack[-1] if check(ts) else None
    print(active)
    if not active:
        if global_store[key]:
            print(global_store[key])
        else:
            print("Not set: ", key)
            return False
    else:
        if active.local_store[key]:
            print(active.local_store[key])
        elif global_store[key]:
            print(global_store[key])
        else:
            print("Not set: ", key)
            return False

#set a key value
def setKey(key, value, ts: TransactionStack):
    active = ts.transaction_stack[-1] if check(ts) else None

    if not active:
        print("INFO: saving to global")
        global_store[key] = value
    else:
        print("INFO: saving to local")
        active.local_store[key] = value

#deletes a particular key
def deleteKey(key, ts: TransactionStack):
    active = ts.transaction_stack[-1] if check(ts) else None

    if not active:
        del(global_store[key])
    else:
        del(active.local_store[key])

def check(ts: TransactionStack):
    if len(ts.transaction_stack) > 0:
        return True
    else:
        return False

if __name__ == '__main__':
    
    currTransaction = TransactionStack()

    while True:

        commands = list(input().split())
        if len(commands) == 0:
            continue
        
        if commands[0].lower() == "begin":
            currTransaction.pushTransaction()
            

        elif commands[0].lower() == "rollback":
            currTransaction.popTransaction()

        elif commands[0].lower() == "commit":
            currTransaction.commit()
            currTransaction.popTransaction()

        elif commands[0].lower() == "end":
            currTransaction.popTransaction()

        elif commands[0].lower() == "set":
            if len(commands) < 3:
                print("INFO: Missing parameter")
                continue
            setKey(commands[1], commands[2], currTransaction)

        elif commands[0].lower() == "get":
            getKey(commands[1], currTransaction)

        elif commands[0].lower() == "delete":
            deleteKey(commands[1], currTransaction)

        elif commands[0].lower() == "count":
            currTransaction.count()

        elif commands[0].lower() == "stop":
            sys.exit()

        else:
            print("Invalid Command")

    sys.exit()