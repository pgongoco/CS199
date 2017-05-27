#Simulation of A.P. Thiruthuvadoss's ENCRYPTION algorithm using DNA strands as OTP.

import random
import math

class MOD_DNACRYPT:
	def __init__ (self):
		pass

	# Function to generate pseudo-random single-strand DNA to be used as OTP.
	# An advisable way to generate a random DNA strand for the OTP is Matlab bioinformatics tool.
	def generate_otp(self, length):
		dna_otp = ""
		for c in range(length):
			dna_otp += random.choice("ACTG")
		return dna_otp

	# Get the complement of a DNA strand using this function.
	def dna_complement(self, string):
		cdna = ""
		for i in string:
			if i == "A":
				cdna += "T"
			elif i == "T":
				cdna += "A"
			elif i == "C":
				cdna += "G"
			elif i == "G":
				cdna += "C"
		return cdna

	def encrypt(self, plain_filename):
		file1 = open(plain_filename, "r")

		readtext = file1.readline()
		plaintext = ''
		while readtext != '':
			plaintext += readtext
			readtext = file1.readline()

		# Convert every character in plaintext to their integer ascii values, then to their 8-bit binary values, then store them as one binary string.
		bintext = "".join(['{0:08b}'.format(ord(c)) for c in plaintext])
		# Generate a random DNA strand with bases 10 times the amount of bits in bintext.
		# Each bit is represented by DNA strand of 10-base length
		otp = self.generate_otp(10*len(bintext))
		#otp = otp_generate(10*len(ciphertext), S)

		# Encrypt the binary strand using the generated OTP
		ciphertext = ""
		for i,j in zip(bintext, range(len(otp),0,-10)):		# The OTP is traversed from the last 10 bases.
			if i == "1":
				ciphertext += self.dna_complement(otp[j-10:j])

		key1 = self.generate_otp(20)
		key2 = self.generate_otp(20)
		key3 = str(len(ciphertext))
		ciphertext = key1 + ciphertext + key2
		while len(ciphertext) < 3000000:
			temp = self.generate_otp(10*random.randint(0,len(bintext)))
			if random.randint(0,1) == 0:
				ciphertext = temp + ciphertext
			else:
				ciphertext = ciphertext + temp
		file2 = open("ciphertext.txt", "w")
		file2.write(ciphertext)

		file3 = open("otp.txt","w") # Temporary. OTP is to be shared using Diffie-Hellman Key Exchange
		file3.write(otp)

		file4 = open("keys.txt","w")
		file4.write(key1+'\n'+key2+'\n'+key3)

		file1.close()
		file2.close()
		file3.close()

	def decrypt(self, cipher_filename):
		file_cipher = open("ciphertext.txt","r")
		file_otp = open("otp.txt","r") # Temporary. OTP is to be shared by Diffie-Hellman Key Exchange

		keyfile = open("keys.txt","r")
		key1 = keyfile.readline().rstrip('\n')
		key2 = keyfile.readline().rstrip('\n')
		key3 = int(keyfile.readline())

		ciphertext = file_cipher.readline().rstrip('\n')
		otp = file_otp.readline().rstrip('\n')
		#otp = otp_generate(10*len(ciphertext), S)
		index = -1
		ctr = 0
		for i in range(0,len(ciphertext),10):
			if ciphertext[i:i+20] == key1 and ciphertext[i+key3:i+key3+20]:
				index = i+20
				ctr+=1

		ciphertext = ciphertext[index:index+key3]
		# Group the ciphertext in groups of 10 bases. Every 10 bases represent a bit.
		ten_set_ciphertext = [ciphertext[i:i+10] for i in range(0,len(ciphertext),10)]
		# Group the OTP in groups of 10 as well as it would be compared with the ciphertext during decryption.
		ten_set_otp = [otp[i:i+10] for i in range(0,len(otp),10)]

		# Decrypt the ciphertext by reversing the encryption process.
		bintext = ""
		for i in reversed(ten_set_otp):		# The OTP is traversed from the last 10 bases during encryption.
			if len(ten_set_ciphertext) > 0 and i == self.dna_complement(ten_set_ciphertext[0]):
				bintext += "1"
				del ten_set_ciphertext[0]
			else:
				bintext += "0"

		# Convert every 8 bits in bintext to their decimal values and then to their corresponding ascii characters.
		set_ascii = []
		for i in range(0,len(bintext),8):
			set_ascii.append(chr(int(bintext[i:i+8],2)))

		plaintext = "".join(set_ascii)
		print plaintext
		file_output = open("message.txt","w")
		file_output.write(plaintext)

		file_cipher.close()
		file_otp.close()
		file_output.close()