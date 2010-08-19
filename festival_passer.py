#!/usr/bin/python
import sys,os,time,select, getopt, socket

def usage():
	print """Usage:
festival_passer.py [OPTIONS]
  -h, --host=HOST			Festival server host (by default localhost)
  -p, --port=PORT			Festival server port (by default 1314)

Redirect stdin to Festival server, mapping the sentences into a Festival command
(SayText).
"""


if __name__ == '__main__':

	festival_host = 'localhost'
	festival_port = 1314
	
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'h:p:', ['host=', 'port='])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	for o, a in optlist:
		if o in ("-h", "--host"):
			festival_host = a
		elif o in ("-p", "--port"):
			festival_port = int(a)
		else:
			print "Unhandled option " + o
			usage()
			sys.exit(2)
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((festival_host, festival_port))
		festival_server = s.makefile()
		
	except socket.error:
		s.close()
		raise OroServerError('Unable to connect to the Festival server. Check it is running and ' + \
						 'that you provided the right host and port.')
						 
	#Initial Festival configuration
	festival_server.write("(voice_nitech_us_bdl_arctic_hts)\n")
	festival_server.flush()

	try:
		while True:
			msg = sys.stdin.readline().rstrip('\r\n')
			festival_server.write("(SayText \"" + msg + "\")\n")
			festival_server.flush()
			
			sys.stdout.write(msg + "\n")
			sys.stdout.flush()
	
	except KeyboardInterrupt:
		print "Leaving now."
		sys.exit()
