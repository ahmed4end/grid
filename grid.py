from PIL import Image, ImageDraw
from core import Data

A4 = (2480, 3508)

class Grid:

	def __init__(self, cols:int, rows:int, width:int=2480, height:int=3508, *args, **kwargs):
		'''
			:kwargs:
				bgcolor: image background color
				border_color: border color
				border_width: border width
				hlines: horizontal lines drawing bool
				vlines: vertical lines drawing bool
				margin: (top,right,bottom,left) or integer
		'''
		self.cols = cols
		self.rows = rows
		self.width = width
		self.height = height
		self.image = Image.new(mode='RGBA', size=(width, height), color=kwargs.get('bgcolor',(0,0,0,0)))
		self.draw = ImageDraw.Draw(self.image)
		self.kwargs = kwargs
		self.margin = self._margin()
		self.border_width = kwargs.get('border_width')
		self.grid_metrics = self._grid_metrics()
		

	def _grid_metrics(self,):
		row_piece_val = (self.height-self.margin[0]-self.margin[2]-self.border_width)//self.rows
		col_piece_val = (self.width-self.margin[1]-self.margin[3]-self.border_width)//self.cols
		return Data(
			row_width= row_piece_val, 
			col_width= col_piece_val,
		)

	def _margin(self):
		margin = self.kwargs.get('margin')
		if isinstance(margin,tuple) and len(margin)==4 and all(map(int,margin)):
			return margin
		elif isinstance(margin,int):
			return (margin,)*4
		else:
			return (0,)*4

	def draw_lines(self):
		_h, _w = self.margin[0], self.margin[1]
		if self.kwargs.get('hlines') or 'hlines' not in self.kwargs:
			for row in range(self.rows+1):
				self.draw.line(
					xy=[self.width-self.margin[1], _h, self.margin[3], _h], 
					fill=self.kwargs.get('border_color','black'), 
					width=self.border_width
				)
				_h += self.grid_metrics['row_width']
		
		if self.kwargs.get('vlines') or 'vlines' not in self.kwargs:
			for col in range(self.cols+1):
				self.draw.line(xy=[self.width-_w-self.border_width, self.margin[0], self.width-_w-self.border_width, self.height-self.margin[2]], 
					fill=self.kwargs.get('border_color','black'), 
					width=self.border_width
				)
				_w += self.grid_metrics['col_width']

	def cells(self):
		pass


if __name__=='__main__':
	obj = Grid(4,4, bgcolor='lightgrey', border_color='red', margin=100, border_width=5)
	details = obj.grid_metrics
	print(details)
	obj.draw_lines()
	obj.image.show()