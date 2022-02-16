from pym import readAllUsers
import json

users = readAllUsers()

for row in (users):
    print(row[0])
#print(json.dumps(users,indent=3))