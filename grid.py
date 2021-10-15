from PIL import Image, ImageDraw, ImageFont
import random 

import sys
sys.path.append(r'F:/Python/mathar/assets/fonts/')

class Grid:

	A4 = (2480, 3508)

	def __init__(self,  rows:int, cols:int, width:int=2480, height:int=3508, *args, **kwargs):
		'''
			:kwargs:
				bgcolor: image background color
				border_color: border color
				border_width: border width
				hlines: horizontal lines drawing bool
				vlines: vertical lines drawing bool
				border: border bool
				margin: (top,right,bottom,left) or integer
				cell_margin: cell margin to all sides.
		'''
		self.size = (width, height)
		self.cols = cols
		self.rows = rows
		self.width = width
		self.height = height
		self.image = Image.new(mode='RGBA', size=(width, height), color=kwargs.get('bgcolor',(0,0,0,0)))
		self.draw = ImageDraw.Draw(self.image)
		self.kwargs = kwargs
		self.border_width = kwargs.get('border_width',1)
		self.cell_margin = kwargs.get('cell_margin',1)
		self.margin = self._margin()
		self.grid_metrics = self._grid_metrics()
		self.cell_width = self.grid_metrics['col_height']-kwargs['cell_margin']*2-kwargs['border_width'] #-self.margin[1]
		self.cell_height = self.grid_metrics['row_height']-kwargs['cell_margin']*2-kwargs['border_width']#-self.margin[0]

		self.header = self.kwargs.get('header','')
		self.footer = self.kwargs.get('footer','')
		#init
		self.draw_lines()
		self.draw_headers()

	def _grid_metrics(self,):
		row_piece_val = (self.height-self.margin[0]-self.margin[2])//self.rows
		col_piece_val = (self.width-self.margin[1]-self.margin[3])//self.cols
		return {
			'row_height': row_piece_val,
			'col_height': col_piece_val
		}

	def _margin(self):
		margin = self.kwargs.get('margin')
		if isinstance(margin,tuple) and len(margin)==4 and all(map(int,margin)):
			return tuple(map(lambda x: x+self.border_width//2,margin))
		elif isinstance(margin,int):
			return tuple(map(lambda x: x+self.border_width//2,(margin,)*4))
		else:
			return (self.border_width//2,)*4

	def draw_lines(self):
		_h, _w = self.margin[0], self.margin[1]
		if self.kwargs.get('hlines') or 'hlines' not in self.kwargs:
			for row in range(self.rows-1):
				_h += self.grid_metrics['row_height']
				self.draw.line(
					xy=[self.width-self.margin[1], _h, self.margin[3], _h], 
					fill=self.kwargs.get('border_color','black'), 
					width=self.border_width
				)	
		
		if self.kwargs.get('vlines') or 'vlines' not in self.kwargs:
			for col in range(self.cols-1):
				_w += self.grid_metrics['col_height']
				self.draw.line(xy=[self.width-_w, self.margin[0], self.width-_w, self.height-self.margin[2]], 
					fill=self.kwargs.get('border_color','black'), 
					width=self.border_width
				)
		
		if self.kwargs.get('border') or 'border' not in self.kwargs:
			self.draw.rectangle(
				xy=(self.margin[3]-self.border_width//2, 
					self.margin[0]-self.border_width//2, 
					self.size[0]-self.margin[2]+self.border_width//2, 
					self.size[1]-self.margin[1]+self.border_width//2),
				fill=None,
				outline=self.kwargs.get('border_color','black'), 
				width=self.border_width)

	@property
	def cells(self):
		_cells = []
		_col_height = self.grid_metrics['row_height']
		_col_width = self.grid_metrics['col_height']
		for row in range(self.rows):
			_row = []
			for col in range(self.cols):

				# cell xy
				_cell = (_col_width*col+self.margin[3]+self.border_width//2+self.cell_margin,
					_col_height*row+self.margin[0]+self.border_width//2+self.cell_margin,
					_col_width*(col+1)+self.margin[3]-self.border_width//2-self.cell_margin,
					_col_height*(row+1)+self.margin[0]-self.border_width//2-self.cell_margin
				)

				_row.append(_cell)

			_cells.append(_row)

		# reverse row order to RTL
		_cells = list(map(lambda x: x[::-1], _cells)) 	

		return _cells

	def rndcolor(self):
		return (random.randint(50,200), random.randint(50,200), random.randint(50,200))

	def color_cells(self):
		for row in self.cells:
			for col in row:
				self.draw.rectangle(xy=col,fill=self.rndcolor())

	def draw_headers(self):
		''' draw header and footer '''
		font = ImageFont.truetype('assets/fonts/Sans.ttf', 50)
		# draw header
		(width, height), (_, offset_y) = font.font.getsize(self.header)
		self.draw.text( (self.width//2-width//2, self.margin[0]//2-height//2), text=self.header, fill='black', font=font)
		# draw footer
		(width, height), (_, offset_y) = font.font.getsize(self.footer)
		self.draw.text( (self.width//2-width//2, self.height-self.margin[3]//2-height//2), text=self.footer, fill='black', font=font)

if __name__=='__main__':
	from pprint import pprint
	obj = Grid(15,4, border_width=25, cell_margin=25, margin=50, bgcolor='lightgrey')
	details = obj.grid_metrics
	print(details)
	obj.color_cells()
	pprint(obj.cells)
	obj.image.show()
	#obj.image.save('example.png')
	