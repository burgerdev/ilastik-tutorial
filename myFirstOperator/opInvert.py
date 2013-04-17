

from lazyflow.graph import InputSlot, OutputSlot, Operator
import numpy

class OpInvert(Operator):
    """
    This example operator class inverts images with dtypes float32, float64, uint8, uint16. 
    We assume that it's a normal image, i.e. 2d with no fancy dimensions.
    """

    name = "OpInvert"

    # this slot will provide the image input
    inputslot = InputSlot()

    # at this slot the inverted image can be queried
    outputslot = OutputSlot()

    def setupOutputs(self):
        # we will pass for now
        pass

    def execute(self, slot, subindex, roi, result):
        # this is the worker method, it gets called when the output slot is queried

        # collect corresponding input data
        data = self.inputslot.get(roi).wait()
        # invert the data
        # to invert it, we subtract from the maximum value
        if data.dtype == numpy.dtype('uint8'):
            m = 2**8-1
        elif data.dtype == numpy.dtype('uint16'):
            m = 2**16-1
        else:
            m = 1

        result[:] = m-data

        # reassign the original data type
        result = result.astype(data.dtype,copy=False)

        return result

    def propagateDirty(self, slot, subindex, roi):
        # also being passed for now
        pass

