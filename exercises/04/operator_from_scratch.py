#!/usr/bin/env python

"""
In this exercise, we will write the thresholding operator from exercise
3 without inheriting from OpArrayPiper. Rewriting it from scratch will
give us more control about the output we're producing.
"""

"""
In the last exercise, I mentioned that it would be nice if our output
would be a bool array rather than float64. For this to work, we will
need to tell the output slot (and possibly downstream operators) that it
does produce boolean data. We do this in Operator.setupOutputs().
"""

import numpy
from lazyflow.operator import Operator
from lazyflow.slot import InputSlot, OutputSlot

class OpThreshold(Operator):
    name = "OpThreshold_For_Real"
    _threshold = 0.5

    """
    Define the slots. We will need an input slot and an output slot,
    like OpArrayPiper from exercise 2. We are using the default
    constructors, which means that our slots will handle arrays.
    """
    Input = InputSlot()
    Output = OutputSlot()

    """
    If something about these attributes seems strange to you, jump
    to [1]. If you don't care about the details, just go on :)
    """

    """
    The execute method is the same one that we used before.
    """
    def execute(self, slot, subindex, roi, result):
        threshold = self._threshold
        upstream_data = self.Input.get(roi).wait()
        result[:] = upstream_data >= threshold

    """
    The name tells us everything we need to know: setupOutputs() sets
    up the Output slot. This method is called when all InputSlots are
    ready, and whenever all Input slots were ready and one of them
    changed (got new data, ...). More about the 'when' and 'how' will
    follow in a later exercise.
    """
    def setupOutputs(self):
        """
        I promised that this method will only be called when all inputs
        are ready, so let's check this.
        """
        assert self.Input.ready()

        """
        It is always a good idea to copy the meta dictionary from Input.
        This prevents us writing boilerplate code and there could be
        meta tags that are not interesting to us, but relevant for
        downstream operators. Luckily, there is a method for this.
        """
        self.Output.meta.assignFrom(self.Input.meta)

        """
        Our output slot is now set up like the input slot. However, we
        wanted it to handle boolean data.
        """
        self.Output.meta.dtype = numpy.bool

        """
        That's it. Not even a real exercise in here.
        """

    """
    The next method is required for an Operator implementation, but we
    will deal with its details in a later exercise.
    """
    def propagateDirty(self, slot, subindex, roi):
        pass


from lazyflow.graph import Graph

input_array = numpy.asarray([[.20, .60, .30],
                             [.10, .55, .99]])
expected_output_array = numpy.asarray([[False, True, False],
                                       [False, True, True]],
                                      dtype=numpy.bool)

op = OpThreshold(graph=Graph())
op.Input.setValue(input_array)

"""
setupOutputs was called, and the output data type should be bool by now.
"""

assert op.Output.meta.dtype == numpy.bool

output_array = op.Output[...].wait()
numpy.testing.assert_array_equal(output_array, expected_output_array)

"""
Footnotes:

[1]: Wait a second - does this mean that all operators share the same
     slot instances?
     There is a tricky mechanism that instantiates object attributes
     from the class attributes that we define here. That mechanism is
     well hidden inside Operator, and that for a reason. Just remember
     to *always* call super().__init__().
     Don't know what I am talking about? Consider the following class,
     where all class instances share the same dict.
        >>> class A:
        ...     d = dict()
        ... 
        >>> a1 = A()
        >>> a2 = A()
        >>> a1.d['key'] = "value"
        >>> a1.d
        {'key': 'value'}
        >>> a2.d
        {'key': 'value'}
"""
