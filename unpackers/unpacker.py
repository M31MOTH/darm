import sys
import string
import time
import socket
import struct
import binascii
import os
from common import *

class Unpacker:

	def __init__(self):
		self._unpackers = []

	def __str__(self): 
		return "Default unpacker"

	def addUnpacker(self, unpacker):
		self._unpackers += [unpacker]

	def validate(self, packet):
		return True

	def process(self, packet):
		pass

	def getPayload(self, packet):
		return packet

	def relay(self, packet):
		if len(self._unpackers)>0:
			for unpacker in self._unpackers:
				try:
					unpacker.addPacket(packet)
				except Exception as ex:
					print "{0} error, packet #{1}: {2}".format(unpacker, packet['raw']['seq'], ex)
		else:
			# outputs packet information
			s = []
			for key, value in packet[packet['top']].iteritems():
				s += ["{0} {1}".format(key, value)]
			Log.write("#{0} {1} {2}".format(packet['raw']['seq'], packet['path'], ', '.join(s)), 2)
			
	def addPacket(self, packet):
		if self.validate(packet):
			self.process(packet)
			self.relay(packet);

	def close(self):
		for unpacker in self._unpackers:
			unpacker.close()		

