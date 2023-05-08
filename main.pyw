import tkinter as tk
import json
import random


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
		# 2d list based on dimentions
		self.pattern = [[0 for _ in range(dimentions[1])] for _ in range(dimentions[0])]
		bombs_remaining = total_bombs
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				if random.randint(0, bombs_remaining) == 0:
					bombs_remaining -= 1
					self.pattern[row][column] = "b"

				else:
					pass  # to be edited by placed bomb
	
	def create_grid(self, dimentions: tuple[int, int]) -> None:
		self.square_reference = {}
		width, height = self.settings["square size"]
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				current_square = tk.Button(self.grid_frame, text=self.pattern[row][column], width=width, height=height,
										   command=lambda row=row, column=column: self.button_pressed(row, column))
				current_square.grid(row=row, column=column)
				self.square_reference[(row, column)] = current_square
	
	def button_pressed(self, row, column) -> None:
		# if corner or edge
		if row in (0, self.settings["grid size"][0] - 1) or column in (0, self.settings["grid size"][1] - 1):
			print("poop")
		else:
			square = self.square_reference[(row, column)]
			square.config(relief="sunken")

	
	def mainloop(self) -> None:
		self.grid_frame.pack()
		self.root.mainloop()


def main() -> None:
	GUI().mainloop()


if __name__ in "__main__":
	main()
