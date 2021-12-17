import hashlib
import cryptocode
import rsa
from Crypto.Cipher import AES

file  = open("data.txt","r")
lines = file.readlines()
line_pass = [""]*160
line_user = [""]*160
count_pass = 1
count_user = 0
z_f = 0
for line in lines:
    if count_pass > 110:
        break
    if z_f%2 == 0:
        line_user[count_user] = line.strip()
        count_user+= 1
        z_f+=1
    elif z_f % 2 != 0 :
        line_pass[count_pass] = line.strip()
        count_pass += 1
        z_f+=1
string2 = "ahmad2"
encoded = cryptocode.encrypt(string2,"8585")
## And then to decode it:
decoded = cryptocode.decrypt(line_pass[1], "8585")
print(encoded)
print(decoded)
