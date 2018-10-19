import string
import random


def key_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

key = key_generator()
key_length = 16
CON = 0x38e38e39
n = 0

def ordinary(char):
	if ord(char) > 47 and ord(char) <= 57:
		return ord(char) - ord('0')
	elif ord(char) > 64 and ord(char) <= 90: 
		return ord(char)-55

def unordinary(num):
	if num >= 0 and num <= 9:
		return num + ord('0')
	else:
		return num + 55

for i in range(key_length-1):
	c = ordinary(key[i]) + 1 
	mul = i + 1
	mul *= c
	n += mul

temp = n * 0x38e38e39
upper_bytes = hex(temp).replace(hex(temp)[2:][3:], "")
t1 = int(upper_bytes,16) / 8
t2 = (t1 * 8) + t1
t2 = t2 * 4
n = n - t2
t1 = n


final = key+chr(unordinary(t1))


print final
