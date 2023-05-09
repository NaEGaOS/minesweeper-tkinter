import tkinter as tk
import json
import random


class Global:
	global settings
	with open(r"game_files\settings.json", "r") as settings_file:
		settings = json.load(settings_file)
	global square_colours
	with open(r"game_files\square_colours.json", "r") as square_colours_file:
		square_colours = json.load(square_colours_file)

class Square:
	def __init__(self, button: tk.Button, position: tuple[int, int], value: int | str) -> None:
		self.bomb = False
		self.button = button
		self.position = position
		self.value = value


class GUI:
	def __init__(self) -> None:
		self.root = tk.Tk()
		self.root.title("Minesweeper")
		# frames
		self.grid_frame = tk.Frame(self.root)
		# widgets
		# variables
		
		# code
		self.create_pattern(settings["grid size"], settings["total bombs"])
		self.create_grid(settings["grid size"])
	
	def create_pattern(self, dimentions: tuple[int, int], total_bombs: int) -> None:
		self.pattern = [[0 for _ in range(dimentions[1])] for _ in range(dimentions[0])]  # 2d list based on dimentions
		bombs_remaining = total_bombs
		while bombs_remaining > 0:
			row, column = (random.randint(0, dimentions[0] - 1), random.randint(0, dimentions[1] - 1))
			if self.pattern[row][column] != "b":  # turns square to bomb
				self.pattern[row][column] = "b"
				bombs_remaining -= 1
				# increment surrounding squares
				for row_offset in range(-1, 2):
					for column_offset in range(-1, 2):
						if row_offset == column_offset == 0:  # skips center square
							continue
						if 0 <= row + row_offset < dimentions[0] and 0 <= column + column_offset < dimentions[1]:
							if self.pattern[row+row_offset][column+column_offset] != "b":
								self.pattern[row+row_offset][column+column_offset] += 1
	
	def create_grid(self, dimentions: tuple[int, int]) -> None:
		self.square_reference = {}
		width, height = settings["square size"]
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				pattern = self.pattern[row][column]
				square = Square(tk.Button(self.grid_frame, text="", width=width, height=height,
				    					  command=lambda row=row, column=column: self.button_pressed(row, column)),
								(row, column), pattern)
				square.button.grid(row=row, column=column)
				self.square_reference[(row, column)] = square
	
	def button_pressed(self, row, column) -> None:
		queue = []
		square = self.square_reference[(row, column)]
		square.button.config(text=square.value if square.value != 0 else "", relief="sunken",
							 fg=square_colours[str(square.value)])
		if square.value == 0:
			queue.append(square)
		# press all connecting 
		for current_square in queue:
			current_square.button.config(text=current_square.value if current_square.value != 0 else "", relief="sunken")
			direct_neighbors = []
			row, column = current_square.position
			direct_neighbors.append(self.square_reference[row-1, column]) if row != 0 else None
			direct_neighbors.append(self.square_reference[row+1, column]) if row != settings["grid size"][0] - 1 else None
			direct_neighbors.append(self.square_reference[row, column-1]) if column != 0 else None
			direct_neighbors.append(self.square_reference[row, column+1]) if column != settings["grid size"][1] - 1 else None
			for neighbor in direct_neighbors:
				if neighbor.value == 0:
					queue.append(neighbor) if neighbor not in queue else None

	def mainloop(self) -> None:
		self.grid_frame.pack()
		self.root.mainloop()


def main() -> None:
	GUI().mainloop()


if __name__ in "__main__":
	main()
