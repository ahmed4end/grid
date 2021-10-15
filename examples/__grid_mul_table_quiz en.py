from grid.grid import Grid
from typer import Typer
import sys
sys.path.append(r'F:\Python\mathar\grid')

typer = Typer()
typer.debug = 0
typer.font_size=70
typer.mode='EN'

def paste(pil, xy, xalign='left', yalign='center'):
	# DEV: complete aligns
	pil = typer.fit_image(image=pil, width=grid.cell_width, height=grid.cell_height)
	if xalign=='right':
		x = grid.cell_width-pil['w']
	if xalign=='left':
		x = 0
	if xalign=='center':
		x = grid.cell_width//2-pil['w']//2
	if yalign=='center':
		y = grid.cell_height//2-pil['h']//2
	grid_image.paste(pil['p'], (xy[0]+x,xy[1]+y), mask=pil['p'])

import random
def gen():
	while True:
		for i in range(1,13):
			for j in range(1,13):
				pop = [1,1,0]
				random.shuffle(pop)
				f,s,t = pop
				yield f'{i if f else "h(2)"}×{j if s else "h(2)"}={i*j if t else f"h(2)"}'

gen = gen()

for k in range(10):
	res = []
	grid = Grid(24,6, width=3508//2, height=2480, 
		border_width=3, 
		border_color='grey', 
		margin=100, 
		cell_margin=25, 
		bgcolor='white',
		header = 'Multiplication table worksheet',
		footer = 'Grade (5A) — A.S.A')
	#grid.color_cells()
	grid_image = grid.image
	cells = grid.cells
	random.shuffle(cells)
	for i, row in enumerate(cells):
		for j, col in enumerate(row):
			pil = typer.robot(next(gen))
			paste(pil, col)
			res.append(grid_image)
	
	#grid.image.show()
	#im.p.show()
	grid_image.save(f'{k}.png')

