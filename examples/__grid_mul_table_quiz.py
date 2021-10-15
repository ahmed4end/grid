from grid import Grid
from typer import Typer

typer = Typer()
typer.debug = 0
typer.font_size=70

def paste(pil, xy, xalign='right', yalign='center'):
	# DEV: complete aligns
	pil = typer.fit_image(image=pil, width=grid.cell_width, height=grid.cell_height)
	if xalign=='right':
		x = grid.cell_width-pil['w']
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
				yield f'{i if f else "h(1)"}×{j if s else "h(1)"}={i*j if t else f"h(2)"}'

gen = gen()

for k in range(10):
	res = []
	for l in range(2):
		grid = Grid(24,6, width=3508//2, height=2480, border_width=5, border_color='grey', margin=100, cell_margin=25, bgcolor='white')
		grid_image = grid.image
		cells = grid.cells
		random.shuffle(cells)
		for i, row in enumerate(cells):
			for j, col in enumerate(row):
				pil = typer.robot(next(gen))
				paste(pil, col)
				res.append(grid_image)
	res = [res[0].rotate(90, expand=True), res[1].rotate(90, expand=True)]
	im = typer.vstack(res[0], res[1])
	im.p.save(f'{k}.png')

