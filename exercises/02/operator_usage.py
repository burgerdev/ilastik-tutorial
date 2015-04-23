#!/usr/bin/env python

"""
Exercise 2 is about lazyflow, the lazy operations framework that lays
the foundation for all ilastik workflows. The main feature of lazyflow
is its laziness, which can be compared to lazy evaluation in functional
languages. In general, data is only processed if it is really needed,
which makes processing of volumes larger than RAM possible.
"""

"""
Lazyflow is a framework for manipulating data (mostly image/volume data
in the form of numpy arrays). When we are talking about image
processing, we often mean 'applying a set of operations to an image'.
Lazyflow organizes these operations in so called 'Operators', which are
connected to a (directed, acyclic) 'Graph'. 
"""

from lazyflow.graph import Graph

"""
The Graph class is used for manipulating the data flow from Operators
to Operators. For now, we just need to know that we need a Graph object
for every workflow we write.
"""

from lazyflow.operator import Operator

"""
A single operation is performed by a specialized operator that inherits
from the Operator class. Operators communicate over 'Slots', which send
data from one operator to another
"""

from lazyflow.slot import InputSlot, OutputSlot

"""
The two slot types are pretty much self explanatory - InputSlots are
used for getting data into an operator, OutputSlots can be queried to
get the computation results of an operator.
"""

import numpy

"""
If not specified, slots expect their data to be numpy arrays [1].

Let's look at an example...
"""

from lazyflow.operators import OpArrayPiper

"""
The array piper class is the most simple operator you can imagine: it
takes an input array and provides the same array as output. Therefore,
the operator has only two slots:
    * OpArrayPiper.Input
    * OpArrayPiper.Output
You will see this naming convention quite often, although some operators
use other names for their slots.
"""

input_array = numpy.asarray([[0, 1],
                             [2, 3]])

op = OpArrayPiper(graph=Graph())
op.Input.setValue(input_array)

"""
We used Slot.setValue() to set our input array to the slot. This does
only make sense at a root node of our graph.
"""

request = op.Output[0:2, 0:2]
output_array = request.wait()
# equivalent:
# output_array = op.Output[:, :].wait()
# output_array = op.Output[...].wait()


"""
Output slots can be queried like arrays with the slicing syntax[2]. But
the return value of the slicing, stored in variable 'request', is not
an array yet. This is where the lazyness comes into play. We just
constructed a request for data, which we can either start right away or
run in the background. For now, we use Request.wait() to gather the
data, which blocks while computing. When wait() returns, the desired
output is in variable 'output_array'.
"""

# as promised, the piper will not manipulate the array
numpy.testing.assert_array_equal(output_array, input_array)

"""
EXERCISE:

Try querying the bottom right element (3) from the output slot. What is
the difference to querying a plain numpy array?
"""

# Fill in the blank
output_array = op.Output[1, 1].wait()

print("Extracted element from bottom right:")
print(output_array)
print("Note that the output is still a 2d array")
print("numpy slicing yields")
print(input_array[1, 1])
numpy.testing.assert_array_equal(output_array, 3)

"""
Every slot has a dictionary of meta information, stored in Slot.meta.
The dictionary can be accessed with attribute notation, and it returns
None for keys that it does not know about.
"""

# these are the same as numpy.ndarray.shape, numpy.ndarray.dtype
data_shape = op.Output.meta.shape
data_dtype = op.Output.meta.dtype

# I made this meta tag up
data_unknown_meta_tag = op.Output.meta.whatsthis

assert data_shape == input_array.shape
assert data_dtype == input_array.dtype
assert data_unknown_meta_tag is None

# we could use dict queries, but it's not that comfortable
assert op.Output.meta.shape is op.Output.meta["shape"]

"""
Now that we know how to query a single operator, it's time for building
a chain of operators.
"""

graph = Graph()
op1 = OpArrayPiper(graph=graph)
op1.name = "OpArrayPiper1"
op2 = OpArrayPiper(graph=graph)
op2.name = "OpArrayPiper2"
op3 = OpArrayPiper(graph=graph)
op3.name = "OpArrayPiper3"

op3.Input.connect(op2.Output)
op2.Input.connect(op1.Output)
op1.Input.setValue(input_array)

"""
We connected three operators to a chain. Three times no operation still
equals no operation, but we just wanted to see how the connections are
done. Operators are always connected from end point to start point
(downstream to upstream). 

 -------------------------------      ---------------------      ---------------------
|         OpArrayPiper1         |    |    OpArrayPiper2    |    |    OpArrayPiper3    |
|                               |    |                     |    |                     |
o Input                  Output o----o Input        Output o----o Input        Output o
| (holds a value)               |    |                     |    |                     |
|                               |    |                     |    |                     |
 -------------------------------      ---------------------      ---------------------

Note that we did not use Slot.setValue() for op2 or op3 - they get
their data from upstream.
"""

output_array = op3.Output[...].wait()
numpy.testing.assert_array_equal(output_array, input_array)

"""
What if we had forgotten to set an input to op1?
"""

# forget about the input array
op1.Input.setValue(None)

try:
    op3.Output[...].wait()
except OutputSlot.SlotNotReadyError as error:
    print("Querying without input failed:")
    print(str(error))

"""
The query fails, blaming op3.Input for not being ready. Which makes
perfect sense: If op1 has no data, how should op2 (or op3) know how to
process the request, or even check whether the slicing is right?

To check our configuration, we can use Slot.ready():
"""

# not configured yet
assert not op1.Output.ready()
assert not op2.Output.ready()
assert not op3.Output.ready()

"""
OutputSlots are considered to be ready when all input slots of their
operator are ready. InputSlots are considered ready when they hold a
value, or when they are connected to another slot which is ready.
"""

# provide an array as input
op1.Input.setValue(input_array)

# op1.Input is ready because it holds a value
assert op1.Input.ready()

# op1.Output is ready because all input slots (i.e., op1.Input) are
# ready
assert op1.Output.ready()

# op2.Input is ready because it is connected to op1.Output, which is
# ready
assert op2.Input.ready()

# disconnect op2 and op3
op3.Input.disconnect()

# op3.Input is not ready because it holds no value and has no partner
assert not op3.Input.ready()

# op3.Output is not ready because op3.Input is not ready
assert not op3.Output.ready()


"""
Material for later exercises:

[1]: there is an additional feature called 'axistags', which tells us
     how we should interpret the data
[2]: there are other query methods (Slot.get(), Slot.__call__(),
     Slot.value), but Slot.__getitem__() (square bracket notation) is
     the obvious choice for handling arrays
"""
