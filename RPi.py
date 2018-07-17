import urllib.request as urllib
class pin:
	number = -1
	direction = "NS"
	state = "NS"
	def __init__(self, numberVal): self.number = numberVal
pins = [ pin(0),  pin(1),  pin(2),  pin(3),  pin(4),  pin(5),  pin(6),
		 pin(7),  pin(8),  pin(9), pin(10), pin(11), pin(12), pin(13),
		pin(14), pin(15), pin(16), pin(17), pin(18), pin(19), pin(20),
		pin(21), pin(22), pin(23), pin(24), pin(25), pin(26), pin(27)]
boardPins = [-1,
			 -1, -1,  2, -1,  3, -1,  4, 14, -1, 15,
			 17, 18, 27, -1, 22, 23, -1, 24, 10, -1,
			  9, 25, 11,  8, -1,  7,  0,  1,  5, -1,
			  6, 12, 13, -1, 19, 16, 26, 20, -1, 21]
class gpio:
	BCM = "BCM"
	BOARD = "BOARD"
	OUT = "Out"
	IN = "In"
	HIGH = "High"
	LOW = "Low"
	mode = "NS"
	def setmode(self, numbering):
		if numbering == self.BCM or numbering == self.BOARD:
			self.mode = numbering
			print("Pin numbering set to: %s" % numbering)
		else:self.cleanup("Invalid pin numbering")
	def setup(self, pinNumber, direction):
		if self.mode != "NS":
			if self.mode == self.BOARD:	number = boardPins[pinNumber]
			else:number = pinNumber
			if number == -1:self.cleanup("Invalid pin number")
			else:
				if direction == self.OUT or direction == self.IN:
					pins[number].direction = direction
					self.__request("setup/pin/" + str(number) + "/dir/" + direction)
					print("Pin %d direction set to: %s" % (pinNumber, direction))
				else:self.cleanup("Invalid pin direction")
		else:self.cleanup("Numbering not set")
	def output(self, pinNumber, state):
		if self.mode == self.BOARD:number = boardPins[pinNumber]
		else:number = pinNumber
		if number == -1:self.cleanup("Invalid pin number")
		else:
			if pins[number].direction == self.OUT:
				if state == self.HIGH or state == self.LOW:
					pins[number].state = state
					self.__request("state/pin/" + str(number) + "/state/" + state)
					print("Pin %d state set to: %s" % (pinNumber, state))
				else:self.cleanup("Invalid pin state")
			else:self.cleanup("Invalid pin direction")
	def input(self, pinNumber):
		if self.mode == self.BOARD:number = boardPins[pinNumber]
		else:number = pinNumber
		if number == -1:self.cleanup("Invalid pin number")
		else:
			if pins[number].direction == self.IN:
				state = self.__request("get/pin/" + str(number))
				if state == b'High':return self.HIGH
				else:return self.LOW
			else:self.cleanup("Invalid pin direction")
	def cleanup(self, error=""):
		if error == "":
			print("Cleaning up")
			self.__request("cleanup")
			for x in range(0, len(pins)):
				pins[x].state = "NS"
				pins[x].direction = "NS"
			exit(0)
		else:raise Exception(error)
	def __request(self, req):
		response = urllib.urlopen("http://localhost:55555/" + req).read()
		if req[0:3] == 'get':return response
		if response != b'Done':raise Exception("An error occured, is your emulator on?")
GPIO = gpio()