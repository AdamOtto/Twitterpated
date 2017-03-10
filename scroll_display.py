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
	
	table = None
	start_idx = None
	select_idx = None
	num_rows = None
	sep = None
	
	def __init__(self, t, rows_to_display = 5, seperator = ' '):
		self.table = t
		self.start_idx = 0
		self.select_idx = 0
		self.num_rows = rows_to_display
		self.sep = seperator
		
	def scroll(self, scroll_amt):
		'''
		moves the view up or down scroll_amt number of rows
		'''
		end_idx = len(self.table) - 1
		if scroll_amt > 0:
			if end_idx - self.start_idx < scroll_amt:
				self.start_idx = end_idx
			self.start_idx = self.start_idx + scroll_amt
			#@TODO not finished yet, needs negative check
		
	
	def __str__(self):
		'''
		This returns the string representation of the object, for use with print(object_instance)
		'''
		output = ''
		end_idx = self.start_idx + self.num_rows
		if end_idx > (len(self.table) - 1):
			end_idx = len(self.table) - 1
		for i in range(self.start_idx, end_idx):
			for col in self.table[i]:
				output = output + str(col) + self.sep
			output = output + '\n'
		return output