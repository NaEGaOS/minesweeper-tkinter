import tkinter as tk
import json


class GUI:
	def __init__(self) -> None:
		with open(r"game_files\settings.json", "r") as settings_file:
			self.settings = json.load(settings_file)
		self.root = tk.Tk()
		self.root.title("Minesweeper")
		# frames
		self.grid_frame = tk.Frame(self.root)
	
	def create_grid(self, dimentions: tuple[int, int]) -> None:
		self.square_reference = {}
		width, height = self.settings["square size"]
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				current_square = tk.Button(self.grid_frame, text=" ", width=width, height=height)
				current_square.grid(row=row, column=column)
				self.square_reference[(row, column)] = current_square
	
	def mainloop(self) -> None:
		self.grid_frame.pack()
		self.create_grid(self.settings["grid size"])
		self.root.mainloop()


def main() -> None:
	GUI().mainloop()


if __name__ in "__main__":
	main()
