#!/usr/bin/python

from opInvert import OpInvert
from lazyflow.graph import Graph
from pprint import pprint
import numpy

if __name__ == "__main__":

	# our operator is a lone wolf, but needs some pseudo-graph as parent
	op = OpInvert(graph=Graph())
	
	# input is a black image 
	img = numpy.zeros((100,100))
	
	# propagate to input slot of the operator
	op.inputslot.setValue(img)
	
	# requesting the output causes the operator to process the input 
	req = op.output(start=(0,0),stop=(4,6))

	# we need to wait until the output is ready 
	# (this blocks until calculations are complete)
	result = req.wait()

	print("Output:")
	pprint(result)


	
