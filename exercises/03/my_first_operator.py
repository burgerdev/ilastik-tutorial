#!/usr/bin/env python

"""
Exercise 3 is all about writing operators. We will construct an operator
that takes an input float array, applies a threshold and outputs a bool
array.
"""

from lazyflow.operators import OpArrayPiper


"""
Operator classes usually start with "Op". We want to get started
quickly, so we just inherit from OpArrayPiper because the operator is
(at least to some extent) similar.
"""
class OpThreshold(OpArrayPiper):
    # it is always good to give operators a name
    name = "OpThreshold_First_Try"

    # we will replace the hard-coded value in a later version of this
    # operator
    _threshold = 0.5

    """
    We override the execute method of OpArrayPiper. Execute is called
    whenever an OutputSlot of this operator is called (except when the
    OutputSlot is connected to some other slot). 

    Let's take a look at the arguments:
        slot      This is the slot object from which data was requested
                  (in our case self.Output, because that's the only one
                  we have). If we had multiple OutputSlots we could use
                  it to distinguish between our operation modes. For
                  now, we ignore it.
        subindex  Another one for the ignore list. This is used for
                  higher level slots, more about them later.
        roi       The region of interest that was requested. For slots
                  that handle arrays, this is a lazyflow.rtype.SubRegion
                  object. We can use this to request data from upstream.
        result    This is a preallocated numpy array which we fill with
                  our computation results. Its shape fits the region
                  described by 'roi'.
    """
    def execute(self, slot, subindex, roi, result):
        """
        So, what was it that we wanted to do? Right, threshold the data.
        We need to things for this.
        1. threshold value
        """
        threshold = self._threshold

        """
        2. upstream data
        In the last exercise, we requested data using the slicing
        syntax:
        data = self.Input[x_1:x:2, y_1:y_2].wait()
        We could do this here, too, but we would have to extract a
        slicing from the roi object. However, we are lucky and there is
        an alternative method for creating requests that takes our roi
        object.
        """
        upstream_data = self.Input.get(roi).wait()
        assert upstream_data.shape == result.shape

        """
        Notice that Slot.get() also constructs a request, which we have
        to wait for. Now that we have the data and the threshold value,
        we can start our work.
        """

        """
        EXERCISE: 
        Apply the threshold to upstream_data such that all values
        strictly less than the threshold are set to 0 and all values
        greater or equal to the threshold are set to 1. Store the
        result in array result.
        Hint: Don't overwrite the result array (result = my_new_array)
        but fill it (result[:] = my_new_array).
        """
        # ____________________

        """
        We don't have to return a value (in fact, we shouldn't), filling
        result is enough.
        """


"""
Ok, ready to test your implementation?
"""

import numpy
from lazyflow.graph import Graph

input_array = numpy.asarray([[.20, .60, .30],
                             [.10, .55, .99]])

expected_output_array = numpy.asarray([[0.0, 1.0, 0.0],
                                       [0.0, 1.0, 1.0]])

op = OpThreshold(graph=Graph())
op.Input.setValue(input_array)


"""
Test whether requesting the whole array works ...
"""
output_array = op.Output[...].wait()
numpy.testing.assert_array_equal(output_array, expected_output_array)

"""
Test whether requesting a slice works ... Why do we need the squeeze()?
Hint: see last exercise.
"""

output_slice = op.Output[0, :].wait().squeeze()
expected_output_slice = expected_output_array[0, :]
numpy.testing.assert_array_equal(output_array, expected_output_slice)

"""
That was not too hard. However, we used a fair amount of existent code,
which limits us in some ways.
"""

assert output_array.dtype == input_array.dtype

"""
Wouldn't it be nice if the output was a bool array rather than float64?
We will accomplish that in the next exercise.
"""
