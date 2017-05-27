import crypto_thiruthuvadoss
import time
test = crypto_thiruthuvadoss.DEF_DNACRYPT()

ave_enc = 0
ave_dec = 0
file = open("deftest.csv","w")
file.write("test run #, encryption time, decryption time\n")
for i in range(100):
	encstart = time.time()
	test.encrypt("sms.txt") # replace plaintext.txt with sms.txt or email.txt
	encend = time.time()
	print "Time elapsed on encryption:",encend-encstart,"seconds"
	decstart = time.time()
	test.decrypt("ciphertext.txt")
	decend = time.time()
	print "Time elapsed on decryption:",decend-decstart,"seconds"
	ave_enc += encend-encstart
	ave_dec += decend-decstart
	file.write(str(i+1)+","+str(encend-encstart)+","+str(decend-decstart)+"\n")

file.write("average,"+str(ave_enc/100)+","+str(ave_dec/100))