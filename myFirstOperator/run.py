#!/usr/bin/python

from opInvert import OpInvert
from lazyflow.graph import Graph
from vigra.impex import writeImage
import numpy

if __name__ == "__main__":

    # our operator is a lone wolf, but needs some pseudo-graph as parent
    op = OpInvert(graph=Graph())
	
    # simulate an input image
    n = 100
    img = numpy.zeros((n,n), numpy.uint8)
    for i in range(n):
        for j in range(n):
            img[i,j] = 255*i*j/(n**2)

    # write the input to file
    writeImage(img, 'input.jpg')
	
    # propagate to input slot of the operator
    op.inputslot.setValue(img)
	
    # requesting the output causes the operator to process the input 
    req = op.output(start=(0,0),stop=(100,100))

    # we need to wait until the output is ready 
    # (this blocks until calculations are complete)
    result = req.wait()
    
    # write the output to file
    writeImage(result, 'output.jpg')

	
