import os
# print(os.getcwd())
f = open('./template.html', "r")

data = f.read().strip()

f.close()
print(data)