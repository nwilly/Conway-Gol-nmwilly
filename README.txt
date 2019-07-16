This small app allows the user to play Conway's game of life and some of its variations.

Author: Nathan Willy
Contact: nmwilly123abc@gmail.com but remove the "123abc"

REQUIREMENTS:
	python 3.X (The code was written and tested for 3.7 but should work for any python 3 version)
	any modern OS (The code was written and tested for windows 10 but should be cross platform)

RUN THE APP:
	
	If python is in the OS path:

	1) double clicking the gol.py
		--or--
	2) cd project directory
	   python gol.py

RUN THE TESTS:

	cd project_directory
	python -m unittest discover

USE DOCUMENTATION:

Upon launch the app will bring up the title screen, which is itself a small Game of Life (gol).

The slider at the bottom of the main window will move the gol through its generation.

file -> new
	Brings up a new window where you can specify details about a new random gol.
	Width: the x extent of the sim
	Height: the y extent of the sim
	Probability: the probability that a given cell will be alive
	Generations: the number of time steps to be calculated
	Seed: a seed value for the random numbers

	Hitting OK will run the new gol.

file -> open
	Bring up a file browser which will let you select a .gif image. This image will be used
	as the starting state of a new gol.

	I have included some fun images in the /.maps folder.

file -> exit
	Closes the app (as you might expect)

view -> settings
	Bring up a new window which will let you specify detail about the current gol.  

	Boundary Condition:
		Torus: the edges of the board warp
		Dead: cells outside the board are considered dead
	Born numbers: If a cell is currently dead and has a number of neighbors which is in this list,
		the cell is "born" is is alive the following time step.
	Survive numbers: If a cell is currently alive and has a number of neighbors which is in this
		list, the cell "survives" and remains alive.
	Generations: the number of time steps to be calculated
	Neighborhood Radius: how far the simulation searchs for neighboring alive cells

	Standard gol has 
		born numbers: 3
		survive numbers: 2, 3
		Neighborhood radius: 1

	Clicking OK will re-run the gol with these new settings.


NOTES:

	Running the gol is quite slow.  I use an O(n^2) alogrithm to run the sim, where is is the size of the 		board.  There are better ways to do this; however, the way I render imaging is by far the limiting 		factor.  My top priority was the smooth animation of the gol.  To achieve this, states of the gol are 		pre-rendered and saved as images.  Without the use of modules such as PIL or numpy, creating these 		images is slow.  As a result, it wasn't worth the effort to write a more efficient gol algroithm.

	Specifically, the algorithm makes a "neighbors_map" which is the number of living cells around a given 	cell.  To do this, the program initializes the n_map as a 2d list of 0s with the same dimensions 		as the board.  It then loops through the cells on the board and, if it is alive, adds 1 to all of the 		adjacent locations in the n_map.  It then loops through the board again, this time looking up in a 		table 	whether the cell is alive or dead in the next step.  The table is generated from born numbers 		and survive numbers ie the number(s) of neighbors which results in a dead cell becoming alive and the 		number(s) of neighbors which results in an alive cell staying alive.  For true gol, birth number is 3 		and the survive numbers are 2 and three (annotated B3/A23).  From this a table can be made giving the 		result of every alive/number-of-neighbors combination.  For gol it looks like this:
				
						number of neighbors
				0	1	2	3	4	5	6	7	8
				_	_	_	_	_	_	_	_	_
	is_alive	0   |	0	0	0	1	0	0	0	0	0
			1   |	0	0	1	1	0	0	0	0	0

	Doing this allows for easy generalization to many gol-like games, even non-binary ones where there are 	more possible states than just alive and dead.

	True gol is played on an infinite board.  That ends up being more trouble than I wanted to put into
	this, so I only implemented boundary conditions where the edges wrap or are dead.

