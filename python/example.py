#!/usr/bin/env python



import os
import os.path
import sys

try:
	# from python-logstash module
	import logstash
	from logger import Logger
	from send_email import SendEmail
except ImportError as e:
	print("Failed to import module python-logstash or Logger or SendEmail! This script requires these module to be installed and imported.")
	sys.exit(1)


def main():
	"""
	Execution entry point
	"""

	try:
		environment = "test"
		logdir = "/var/tmp/program/"
		logfile = "%s.log" % (environment)
		# First, get a logger object for logging - without that the script can't execute cause we need to keep activity log. 
		# (OPTIONAL) We also pass a logstash handler to ship logs to a logstash instance on UDP_IP:UDP_PORT - otherwise don't pass a handler.
		logger, file_handler = create_logger(environment, logfile, logdir, logstash.UDPLogstashHandler(UDP_IP, UDP_PORT, message_type="test-ops", version=1))
		# At this point the logger has been created successfully so we can continue
	except OSError as e:
		print("\n\n[ERROR] An error occurred. Error:\n\t (%s)\n" % (str(sys.exc_info()[1])))
		sys.exit(1)
	except Exception as e:
		print("\n\n[ERROR] An error occurred. Error:\n\t (%s)\n" % (str(sys.exc_info()[1])))
		sys.exit(1)


def create_logger(environment, logfile, logdir, logstash_handler=None):
	"""
	This method creates a logger to log into a logfile by calling the class from the module.
	"""

	lgr = None
	logger = None
	file_handler = None
	try:
		# If the logger does not get created successfully, we must exit the script.
		lgr = Logger(logfile, environment, logdir, "test-ops")
		lgr.clear_log_file()
		lgr.create_logging_directory()
		logger, file_handler = lgr.create_logger_instance()
		logger.info("Logger created successfully")
		# No need to assign value to a variable below as the 'logger' object is being passed by reference, not by value.
		lgr.add_logstash_handler(logger, logstash_handler)
	except Exception as e:
		# If the logger does not get created successfully, exit the script
		print("[ERROR] Unable to create a logging handler which is required by the script. Exiting the script...")
		print(str(sys.exc_info()[1]))
		sys.exit(1)
	return (logger, file_handler)


if __name__ == '__main__':
	main()