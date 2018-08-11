import urllib.request as urllib

class gpio:
	BCM = "BCM"
	BOARD = "BOARD"
	OUT = "Out"
	IN = "In"
	HIGH = "High"
	LOW = "Low"
	mode = "NS"

	class __pin:
		number = -1
		direction = "NS"
		state = "NS"
		def __init__(self, numberVal): self.number = numberVal

	__pins = [__pin(0), __pin(1), __pin(2), __pin(3), __pin(4), __pin(5), __pin(6),
			  __pin(7), __pin(8), __pin(9), __pin(10), __pin(11), __pin(12), __pin(13),
			  __pin(14), __pin(15), __pin(16), __pin(17), __pin(18), __pin(19), __pin(20),
			  __pin(21), __pin(22), __pin(23), __pin(24), __pin(25), __pin(26), __pin(27)]

	__boardPins = [-1,
				   -1, -1, 2, -1, 3, -1, 4, 14, -1, 15,
				   17, 18, 27, -1, 22, 23, -1, 24, 10, -1,
				   9, 25, 11, 8, -1, 7, 0, 1, 5, -1,
				   6, 12, 13, -1, 19, 16, 26, 20, -1, 21]

	def setmode(self, numbering):
		if numbering == self.BCM or numbering == self.BOARD:
			self.mode = numbering
			print("Pin numbering set to: %s" % numbering)
		else:
			self.__raiser("Invalid pin numbering")

	def setup(self, pinNumber, direction):
		if self.mode != "NS":
			if self.mode == self.BOARD:
				number = self.__boardPins[pinNumber]
			else:
				number = pinNumber
			if number == -1:
				self.__raiser("Invalid pin number")
			else:
				if direction == self.OUT or direction == self.IN:
					self.__pins[number].direction = direction
					self.__request("setup/pin/" + str(number) + "/dir/" + direction)
					print("Pin %d direction set to: %s" % (pinNumber, direction))
				else:
					self.__raiser("Invalid pin direction")
		else:
			self.__raiser("Numbering not set")

	def output(self, pinNumber, state):
		if self.mode == self.BOARD:
			number = self.__boardPins[pinNumber]
		else:
			number = pinNumber
		if number == -1:
			self.__raiser("Invalid pin number")
		else:
			if self.__pins[number].direction == self.OUT:
				if state == self.HIGH or state == self.LOW:
					self.__pins[number].state = state
					self.__request("state/pin/" + str(number) + "/state/" + state)
					print("Pin %d state set to: %s" % (pinNumber, state))
				else:
					self.__raiser("Invalid pin state")
			else:
				self.__raiser("Invalid pin direction")

	def input(self, pinNumber):
		if self.mode == self.BOARD:
			number = self.__boardPins[pinNumber]
		else:
			number = pinNumber
		if number == -1:
			self.__raiser("Invalid pin number")
		else:
			if self.__pins[number].direction == self.IN:
				state = self.__request("get/pin/" + str(number))
				if state == b'High':
					return self.HIGH
				else:
					return self.LOW
			else:
				self.__raiser("Invalid pin direction")

	def cleanup(self):
		print("Cleaning up")
		self.__request("cleanup")
		for x in range(0, len(self.__pins)):
			self.__pins[x].state = "NS"
			self.__pins[x].direction = "NS"
		exit(0)

	def __raiser(self, error):
		self.__request("cleanup")
		for x in range(0, len(self.__pins)):
			self.__pins[x].state = "NS"
			self.__pins[x].direction = "NS"
		raise Exception(error)

	def __request(self, req):
		try:
			response = urllib.urlopen("http://localhost:55555/" + req).read()
			if req[0:3] == 'get': return response
			if response != b'Done': raise Exception("An error occured, is your emulator on?")

		except Exception:
			raise Exception("An error occured, is your emulator on?")

GPIO = gpio()
