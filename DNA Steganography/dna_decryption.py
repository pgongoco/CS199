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

def remove_start_primer(dna_message, start_primer):			#returns complement of dna_message - start primer
	new_strand = start_primer		
	for j in range(len(binary_to_DNA(start_primer))*2, len(dna_message)):
		if dna_message[j] == 'A':
			new_strand = new_strand + '10'
		elif dna_message[j] == 'T':
			new_strand = new_strand + '01'
		elif dna_message[j] == 'C':
			new_strand = new_strand + '11'
		elif dna_message[j] == 'G':
			new_strand = new_strand + '00'

	return new_strand

def remove_end_primer(dna_message, end_primer):			#returns complement of dna_message - end_primer
	new_strand = end_primer
	for j in range((len(dna_message)-(len(binary_to_DNA(end_primer)))*2)-1, -1, -1):
		if dna_message[j] == 'A':
			new_strand = '10' + new_strand
		elif dna_message[j] == 'T':
			new_strand = '01' + new_strand
		elif dna_message[j] == 'C':
			new_strand = '11' + new_strand
		elif dna_message[j] == 'G':
			new_strand = '00' + new_strand

	return new_strand

def replicate(strand, altered_strand, number):
	new_strand = []
	if number == 0:
		new_strand.append(strand)
		new_strand.append(altered_strand)
	else:
		new_strand.append(altered_strand)
		new_strand.append(strand)
	
	return new_strand

def main():
	file = open("ciphertext.txt", "r")
	start_primer = file.readline()
	end_primer = file.readline()

	start_primer = start_primer.rstrip('\n')
	end_primer = end_primer.rstrip('\n')

	start_DNA_length = len(binary_to_DNA(start_primer))
	end_DNA_length = len(binary_to_DNA(end_primer))

	#all_strands = [line.rstrip('\n') for line in file]
	all_strands = []
	for line in file:												#EACH ELEMENT OF ALL_STRANDS IS A PAIR REPRESENTING A DOUBLE STRANDED DNA
		line = line.rstrip('\n')
		strand = line.split("|")
		all_strands.append(strand)

	#dna_message uses start primer for replication (directionality)
	#complement uses end primer for replication (directionality)

	#10 cycles
	modified_all_strands = []
	for i in range(0, 10):
		print "Entering cycle", str(i+1), "..."
		new_strands = []
		for strand in all_strands:			#checks if the pair is the message strand
		#while all_strands != []:
		#	strand = all_strands[0]
			if binary_to_DNA(strand[0][:len(start_primer)]) == binary_to_DNA(start_primer) or binary_to_DNA(strand[0][len(binary_to_DNA(strand))-len(end_primer):]) == binary_to_DNA(end_primer):
				
				dna_message = binary_to_DNA(strand[0])				#Splitting of DNA
				complement = binary_to_DNA(strand[1])
				for i in range(0,2):						
					if i == 0:								#message strand
						#strand still has both primers
						if strand[i][len(start_primer):len(start_primer)*2] == DNA_to_binary(DNA_reverse(binary_to_DNA(start_primer))) and strand[i][len(binary_to_DNA(strand))-len(end_primer)*2:len(binary_to_DNA(strand))-len(end_primer)] == end_primer:
							new_strand = replicate(strand[i], remove_start_primer(dna_message, start_primer), i)
							new_strands.append(new_strand)

						elif strand[i][len(start_primer):len(start_primer)*2] == DNA_to_binary(DNA_reverse(binary_to_DNA(start_primer))):
							new_strand = replicate(strand[i], remove_start_primer(dna_message, start_primer), i)
							new_strands.append(new_strand)
						else:
							new_strand = replicate(strand[i], DNA_to_binary(DNA_reverse(binary_to_DNA(strand[i]))), i)
							new_strands.append(new_strand)

					else:										#complement
						if strand[i][len(start_primer):len(start_primer)*2] == start_primer and strand[i][len(binary_to_DNA(strand))-len(end_primer)*2:len(binary_to_DNA(strand))-len(end_primer)] == DNA_to_binary(DNA_reverse(binary_to_DNA(end_primer))):
							new_strand = replicate(strand[i], remove_end_primer(complement, end_primer), i)
							new_strands.append(new_strand)
						elif strand[i][len(binary_to_DNA(strand))-len(end_primer)*2:len(binary_to_DNA(strand))-len(end_primer)] == DNA_to_binary(DNA_reverse(binary_to_DNA(end_primer))):
							new_strand = replicate(strand[i], remove_end_primer(complement, end_primer), i)
							new_strands.append(new_strand)
						else:
							new_strand = replicate(strand[i], DNA_to_binary(DNA_reverse(binary_to_DNA(strand[i]))), i)
							new_strands.append(new_strand)
				
			all_strands = []
			#all_strands.remove(strand)
			#after a cycle, strands are added
			for i in new_strands:
				all_strands.append(i)		
		print "Cycle time:",time.clock()-start_time
	#for i in modified_all_strands:
	#	all_strands.append(i)
	#shuffle(all_strands)	#randomize strands
	#print
	#for i in all_strands:
	#	print binary_to_DNA(i)

	picked_strand = all_strands[randint(0, len(all_strands)-1)]		#random strand

	print len(all_strands)
	print all_strands.count(picked_strand)

	message = ''
	for i in range(0, len(picked_strand[0]), 8):
		binary = picked_strand[0][i:i+8]
		x = int(binary, 2)
		char = chr(x)
		message = message + char
	print "Message: ", message

start_time = time.clock()
main()
print "Running Time: %s seconds" % round(time.clock() - start_time, 10)