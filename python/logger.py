#!/usr/bin/env python


"""
This is a class that can be imported as a module. It implements the logging functionality.
Works with Python 2.7+
								
"""

import os, signal
import sys
import logging
from os.path import isfile





class Logger(object):
	"""
	This class implements the logging functionality.
	"""
	
	def __init__(self, logfile, environment, log_file_dir, log_title):
		self.logfile = logfile
		self.environment = environment
		self.log_file_dir = log_file_dir
		self.log_title = log_title
	
	
	def create_logging_directory(self):
		print("[INFO] Creating logging directory")
		try:
			if not os.path.exists("%s" % (self.log_file_dir)):
				os.mkdir("%s" % (self.log_file_dir))
			if not os.path.exists(self.log_file_dir + self.environment):
				os.mkdir("%s" % (self.log_file_dir + self.environment))
			print("[INFO] Logging directory created")
		except Exception as e:
				print("[ERROR] Unable to create logging directory or log file. Error is: %s" % str(sys.exc_info()[1]))
				raise
	
	
	def create_logger_instance(self):
		logger_inst = None
		file_handler = None
		try:
			logger_inst = logging.getLogger(self.log_title)
			logger_inst.setLevel(logging.INFO)
			
			lg_f = self.log_file_dir + self.environment + "/" + self.logfile
			# create the logging file handler
			file_handler = logging.FileHandler(lg_f)
			
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			file_handler.setFormatter(formatter)
			
			# add handler to logger_inst object
			logger_inst.addHandler(file_handler)
			
		except Exception as e:
			print("[ERROR] Error with creating a logger instance for logging.", sys.exc_info()[1])
			print("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise 
		else:
			return (logger_inst, file_handler)
	
	
	def add_logstash_handler(self, logger, logstash_handler=None):
		"""
		This method adds a logstash handler to the logger object that is passed to it. 
		It requires that the logger object is successfully created before by instatiating this class and calling the create_logger_instance() method after.
		"""
		try:
			if logstash_handler != None:
				# Adding a logstash handler to send logs to logstash
				logger.addHandler(logstash_handler)
				logger.info("Added logstash handler to the logger instance")
		except Exception as e:
			print("Unable to add logstash handler to the logger instance. Shipping script activity logs to logstash will not work.")
			logger.error("Unable to add logstash handler to the logger instance. Shipping script activity logs to logstash will not work.")
			logger.error(sys.exc_info()[1])
			# The script can do without the logstash handler so no reason to stop the execution if it fails adding it.
			pass
		# No need to return a value here as the 'logger' object is being passed by reference, not by value.
	
	
	def clear_log_file(self):
		"""
		This method removes the log file that this script creates.
		"""
		try:
			lg_f = lg_f = self.log_file_dir + self.environment + "/" + self.logfile
			print("[INFO] Removing log file %s from the previous run" % (lg_f))
			if os.path.isfile(lg_f):
				os.remove(lg_f)
				print("[INFO] Log file from previous run removed successfully. Another one will be created in this run")
			else:
				print("[INFO] No such file %s, so not removing anything" % (lg_f))
		except OSError as e:
			print ("[ERROR] Failed to remove logfile %s" % (lg_f))
			raise
		except Exception as e:
			print("[ERROR] An error occurred: %s" % str(sys.exc_info()[1]))
			raise

