import socket
import sys

def format_data(string):
	result = 0
	for c in string:
		result = (result << 8) | ord(c)
	return result

def send_data(sock, b1, b2, b3, b4, time):
	data = [0] * 8

	data[0] = chr(b1)
	data[1] = chr(b2)
	data[2] = chr(b3)
	data[3] = chr(b4)

	data[4] = chr((time >> 24) & 0xff)
	data[5] = chr((time >> 16) & 0xff)
	data[6] = chr((time >> 8) & 0xff)
	data[7] = chr(time & 0xff)

	sock.send(''.join(data))

def connect(port, callback):
	sock = socket.socket()
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # requires nodelay
	sock.connect(("localhost", port))

	send_data(sock, 1, 1, 4, 0, 0) # send version

	try:
		while 1:
			# data packet will be 8 byte long
			raw = format_data(sock.recv(8))
			if raw == 0: continue

			b1 = cmd = raw >> 56
			b2 = (raw >> 48) & 0xff
			b3 = (raw >> 40) & 0xff
			b4 = (raw >> 32) & 0xff
			time = raw & 0xffffffff

			#print "%.2x %.2x %.2x %.2x %.8x" % (b1, b2, b3, b4, time)

			if cmd == 1:
				# handshake (version)
				pass
				#send_data(sock, 0x01, 0x01, 0x04, 0x00, time)
				#send_data(sock, b1, b2, b3, b4, time)

			elif cmd == 101:
				# sync gamepad
				pass

			elif cmd == 104:
				# byte received from master
				result = callback(b2)
				if not result == None:
					# send data
					send_data(sock, 105, result, 0x80, 0, 0)
				else:
					# send ack
					send_data(sock, 106, 1, 00, 0, 0)

			elif cmd == 106:
				send_data(sock, b1, b2, b3, b4, time)

			elif cmd == 108:
				send_data(sock, 108, 1, 0, 0, 0)
	except:
		print sys.exc_info()[0]
		sock.close()
		pass

	print "Connection closed."
