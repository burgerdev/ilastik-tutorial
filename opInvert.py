

from lazyflow.graph import InputSlot, OutputSlot, Operator


class OpInvert(Operator):
	"""
	This example operator class inverts images in a range [0,1].
	"""

	name = "OpInvert"

	# this slot is not neccessary, could be named otherwise or even multiple slots
	inputslot = InputSlot()

	# this attribute is required! 
	output = OutputSlot()
	
	def setupOutputs(self):
		# we will pass for now
		pass
	
	def execute(self, slot, subindex, roi, result):
		# this is the worker method, it gets called when the output slot is queried

		# collect corresponding input data
		d = self.inputslot.get(roi).wait()

		# invert the data
		result[:] = 1-d

		return result
	
	def propagateDirty(self, slot, subindex, roi):
		# also being passed for now
		pass
	



