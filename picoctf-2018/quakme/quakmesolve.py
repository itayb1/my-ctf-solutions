gretting_message = "You have now entered the Duck Web, and you're in for a honkin' good time.\nCan you figure out my trick?"
flag = ""
secret_key = "6e696c206f4e005d51514d16505747562b5d084b145b1b511e30352b4f160629"
secret_key_list = [secret_key[i]+secret_key[i+1] for i in range(0,len(secret_key),2)]
secret_key_list = secret_key_list[::-1] ..
for i, char in enumerate(gretting_message):
	if i > 24:
		break
	result = ord(char) ^ int("0x"+secret_key_list[i], 16)
	print (chr(result), end="")

