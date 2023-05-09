import tkinter as tk
import json
import random


class Square:
	def __init__(self, button: tk.Button, position: tuple[int, int]) -> None:
		self.bomb = False
		self.button = button
		self.position = position
		self.value = self.button["text"]


class GUI:
	def __init__(self) -> None:
		with open(r"game_files\settings.json", "r") as settings_file:
			self.settings = json.load(settings_file)
		self.root = tk.Tk()
		self.root.title("Minesweeper")
		# frames
		self.grid_frame = tk.Frame(self.root)
		# widgets
		# variables
		
		# code
		self.create_pattern(self.settings["grid size"], self.settings["total bombs"])
		self.create_grid(self.settings["grid size"])
	
	def create_pattern(self, dimentions: tuple[int, int], total_bombs: int) -> None:
		self.pattern = [[0 for _ in range(dimentions[1])] for _ in range(dimentions[0])] # 2d list based on dimentions
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
							if self.pattern[row + row_offset][column+column_offset] != "b":
								self.pattern[row + row_offset][column+column_offset] += 1
	
	def create_grid(self, dimentions: tuple[int, int]) -> None:
		self.square_reference = {}
		width, height = self.settings["square size"]
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				pattern = self.pattern[row][column]
				square = Square(tk.Button(self.grid_frame, text=pattern, width=width, height=height,
				    							  command=lambda row=row, column=column: self.button_pressed(row, column)), (row, column))
				square.button.grid(row=row, column=column)
				self.square_reference[(row, column)] = square
	
	def button_pressed(self, row, column) -> None:
		# if corner or edge
		if row in (0, self.settings["grid size"][0] - 1) or column in (0, self.settings["grid size"][1] - 1):
			print("poop")
		else:
			square = self.square_reference[(row, column)]
			square.button.config(relief="sunken")
	
	def mainloop(self) -> None:
		self.grid_frame.pack()
		self.root.mainloop()


def main() -> None:
	GUI().mainloop()


if __name__ in "__main__":
	main()
