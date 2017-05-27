from random import randint
from random import shuffle
import time

def DNA_reverse(string):
	dna_rep = ''
	for i in string:
		if i == 'A':
			dna_rep = dna_rep + 'T'
		elif i == 'T':
			dna_rep = dna_rep + 'A'
		elif i == 'C':
			dna_rep = dna_rep + 'G'
		elif i == 'G':
			dna_rep = dna_rep + 'C'

	return dna_rep

def DNA_to_binary(string):
	binary = ''
	for i in string:
		if i == 'A':
			binary = binary + '01'
		elif i == 'T':
			binary = binary + '10'
		elif i == 'C':
			binary = binary + '00'
		elif i == 'G':
			binary = binary + '11'

	return binary

def binary_to_DNA(string):
	dna_message = ''
	for i in range(0, len(string), 2):
		if string[i:i+2] == '01':
			dna_message = dna_message + 'A'
		elif string[i:i+2] == '10':
			dna_message = dna_message + 'T'
		elif string[i:i+2] == '00':
			dna_message = dna_message + 'C'
		elif string[i:i+2] == '11':
			dna_message = dna_message + 'G'

	return dna_message

def main():
	file1 = open("plaintext.txt", "r")

	plaintext = file1.readline()
	plaintext = plaintext.rstrip('\n')

	message = [] 																	#binary rep of every char of message
	all_strands = []

	for i in plaintext:																#converts plaintext to binary
		x = ord(i)																	#convert to ASCII value
		binary = str(bin(x))

		binary = binary[2:]															#omit 0b
		
		while len(binary) % 8 != 0:													#should be divisible by 8 because ASCII has 256 chars 
			binary = '0' + binary

		message.append(binary)

	binary_message = ''.join(message)

	dna_message = binary_to_DNA(binary_message)										#converting binary message to DNA strand

	start_primer = DNA_to_binary(DNA_reverse(dna_message[:len(dna_message)/5]))		#length of primer = 1/5 of length of DNA message
	end_primer = ''

	i = len(dna_message)-1

	while len(end_primer) != len(start_primer):										#end primer has same length as start primer
		if dna_message[i] == 'A':
			end_primer = '01' + end_primer
		elif dna_message[i] == 'T':
			end_primer = '10' + end_primer
		elif dna_message[i] == 'C':
			end_primer = '00' + end_primer
		elif dna_message[i] == 'G':
			end_primer = '11' + end_primer

		i = i-1

	print "\nPlaintext message expressed in DNA form: \n" + dna_message
	print "Plaintext in binary format: \n" + binary_message
	print "Start Primer: " + binary_to_DNA(start_primer)
	print "End Primer: " + binary_to_DNA(end_primer)

	result = start_primer + binary_message + end_primer

	print "\nDNA Binary Strand with primers: \n" + binary_to_DNA(result) + '\n'

	#Encryption; five dummy strands

	#print "\nDummy Strands:\n"

	#generate dummy strands
	for i in range(0, 99):
		dummy = ''																
		while len(dummy) != len(result):
			for j in range(0, len(result)):						
				bit = str(randint(0,1))
				dummy = dummy + bit
#
			if dummy == result or dummy in all_strands:
				dummy = ''															#reset if equal, there should be no dummy equal to the actual message

		all_strands.append(dummy)

	all_strands.append(result)
	shuffle(all_strands)			

	#Save to ciphertext
	file2 = open("ciphertext.txt", "w")

	file2.write(start_primer + '\n')
	file2.write(end_primer + '\n')	

	for i in all_strands:
		file2.write(i + '|' + DNA_to_binary(DNA_reverse(binary_to_DNA(i))) + '\n')	#DOUBLE STRANDED DNA - MESSAGE | COMPLEMENT

	file1.close()
	file2.close()

start_time = time.clock()
main()
print "Running Time: %s seconds" % round(time.clock() - start_time, 10)