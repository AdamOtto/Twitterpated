'''
Meant to handle the 'display 5 at a time requirement'. Stores a table of rows, 
a start index, a global selection index and a length.

When printed, it will display the (length) number of rows, starting at the
row of the start index. If the selection index is within the printed rows, that
row will be marked by a (To be determined). The class can return the selected row
if asked.

The class should handle all of the bounds checks here.
'''

class ScrollDisplay(object):
	
	def __init__(self):
		pass
	
	def toString(self):
		return 'This is my print function'