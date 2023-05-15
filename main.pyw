import tkinter as tk
import json
import random


class Global:
	global settings
	with open(r"game files\json files\settings.json", "r") as settings_file:
		settings = json.load(settings_file)
	global number_colours
	with open(r"game files\json files\number_colours.json", "r") as number_colours_file:
		number_colours = json.load(number_colours_file)
	global button_colours
	with open(r"game files\json files\button_colours.json", "r") as button_colours_file:
		button_colours = json.load(button_colours_file)
	

class Square:
	def __init__(self, button: tk.Button, position: tuple[int, int], value: int | str) -> None:
		self.flag = False
		self.button = button
		self.position = position
		self.value = value


class GUI:
	def __init__(self) -> None:
		self.root = tk.Tk()
		self.root.title("Minesweeper")
		# binds
		self.root.bind("<Escape>", lambda event: self.reset())
		# variables
		self.remaining_bombs = settings["total bombs"]
		self.game_over = False
		self.image_bomb = tk.PhotoImage(file=r"game files\image files\bomb.png")
		self.image_bomb_crossed = tk.PhotoImage(file=r"game files\image files\bomb crossed.png")
		self.image_flag = tk.PhotoImage(file=r"game files\image files\flag.png")
		# frames
		self.grid_frame = tk.Frame(self.root)
		# widgets
		self.settings_button = tk.Button(self.root, text="settings", command=lambda: self.open_settings())
		self.new_game_button = tk.Button(self.root, text="new game", command=lambda: self.reset())
		self.remaining_bombs_label = tk.Label(self.root, text=f"remaining bombs: {self.remaining_bombs}")
		# code
		self.create_grid(settings["grid size"])
	
	def open_settings(self) -> None:

		def save_settings() -> None:
			try:
				grid_size = (abs(int(rows_entry.get())), abs(int(columns_entry.get())))
				total_bombs = int(bombs_entry.get())
			except ValueError:
				return
			if grid_size[0] * grid_size[1] < total_bombs or total_bombs < 1:
				return
			settings["grid size"] = grid_size
			settings["total bombs"] = total_bombs
			with open(r"game files\json files\settings.json", "w") as settings_file:
				json.dump(settings, settings_file, indent=4)	
			settings_window.destroy()
			self.reset()
		
		settings_window = tk.Toplevel(self.root)
		settings_window.title("settings")
		# widgets
		columns_label = tk.Label(settings_window, text="columns")
		columns_entry = tk.Entry(settings_window, width=3)
		rows_label = tk.Label(settings_window, text="rows")
		rows_entry = tk.Entry(settings_window, width=3)
		bombs_label = tk.Label(settings_window, text="bombs")
		bombs_entry = tk.Entry(settings_window, width=3)
		save_button = tk.Button(settings_window, text="save", command=lambda: save_settings())
		# pack
		columns_label.grid(row=0, column=0)
		columns_entry.grid(row=0, column=1)
		rows_label.grid(row=1, column=0)
		rows_entry.grid(row=1, column=1)
		bombs_label.grid(row=2, column=0)
		bombs_entry.grid(row=2, column=1)
		save_button.grid(row=3, column=0, columnspan=2)
		settings_window.mainloop()
	
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
		self.create_pattern(dimentions, settings["total bombs"])
		self.square_reference = {}
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				pattern = self.pattern[row][column]
				square = Square(tk.Button(self.grid_frame, text="", width=2, height=1, bg=button_colours["raised"],
				    					  command=lambda row=row, column=column: self.button_pressed(row, column, True)),
								(row, column), pattern)
				square.button.bind("<Button-3>", lambda event, row=row, column=column: self.button_pressed(row, column, False))
				square.button.grid(row=row, column=column)
				self.square_reference[(row, column)] = square
	
	def button_pressed(self, row: int, column: int, leftclick: bool) -> None:
		square = self.square_reference[(row, column)]
		if square.button["relief"] == "sunken" or self.game_over:  # already pressed
			return
		if leftclick and not square.flag:
			if square.value == "b":
				self.game_over = True
				self.remaining_bombs_label.config(text="losser :( :( :(")
				for current_square in self.square_reference.values():
					if current_square.value == "b" and not current_square.flag:  # unflagged bomb
						current_square.button.config(text=None, image=self.image_bomb, width=18, height=20)
					elif current_square.flag and current_square.value != "b":  # wrong flag
						current_square.button.config(text=None, image=self.image_bomb_crossed, width=18, height=20)
			square.button.config(text=square.value if square.value != 0 else "", relief="sunken", fg=number_colours[str(square.value)],
								 bg=button_colours["sunken"])
			queue = [square] if square.value == 0 else []
			# press all connecting 
			for current_square in queue:
				current_square.button.config(text=current_square.value if current_square.value != 0 else "", relief="sunken",
											 bg=button_colours["sunken"])
				direct_neighbors = []
				indirect_neighbors = []
				row, column = current_square.position
				direct_neighbors.append(self.square_reference[row-1, column]) if row != 0 else None
				direct_neighbors.append(self.square_reference[row+1, column]) if row != settings["grid size"][0] - 1 else None
				direct_neighbors.append(self.square_reference[row, column-1]) if column != 0 else None
				direct_neighbors.append(self.square_reference[row, column+1]) if column != settings["grid size"][1] - 1 else None
				indirect_neighbors.append(self.square_reference[row-1, column-1]) if row != 0 and column != 0 else None
				indirect_neighbors.append(self.square_reference[row-1, column+1]) if row != 0 and column != settings["grid size"][1] - 1 else None
				indirect_neighbors.append(self.square_reference[row+1, column-1]) if row != settings["grid size"][0] - 1 and column != 0 else None
				indirect_neighbors.append(self.square_reference[row+1, column+1]) if row != settings["grid size"][0] - 1 and column != settings["grid size"][1] - 1 else None
				for neighbor in direct_neighbors:
					if neighbor.value == 0:
						queue.append(neighbor) if neighbor not in queue else None  # gets pressed later
					else:
						neighbor.button.config(text=neighbor.value, relief="sunken", fg=number_colours[str(neighbor.value)],
			     							   bg=button_colours["sunken"])
				for neighbor in indirect_neighbors:
					neighbor.button.config(text=neighbor.value, relief="sunken", fg=number_colours[str(neighbor.value)],
			    						   bg=button_colours["sunken"]) if neighbor.value != 0 else None
		if not leftclick:  # right click on unpressed square
			square.flag = not square.flag
			if square.flag:
				square.button.config(text=None, image=self.image_flag, width=18, height=20)
				self.remaining_bombs -= 1
				self.remaining_bombs_label.config(text=f"remaining bombs: {self.remaining_bombs if self.remaining_bombs >= 0 else 0}")
			else:
				square.button.config(text="", fg=number_colours[str(square.value)], image="", width=2, height=1)
				self.remaining_bombs += 1
				self.remaining_bombs_label.config(text=f"remaining bombs: {self.remaining_bombs}")
		# if all non-bomb squares are pressed or all bombs are flagged
		if all(square.button["relief"] == "sunken" for square in self.square_reference.values() if square.value != "b") or \
		   all(square.flag for square in self.square_reference.values() if square.value == "b"):
			self.game_over = True
			self.remaining_bombs_label.config(text="you win :) :) :)")

	def reset(self) -> None:
		self.game_over = False
		self.remaining_bombs = settings["total bombs"]
		self.remaining_bombs_label.config(text=f"remaining bombs: {self.remaining_bombs}")
		self.grid_frame.destroy()
		self.grid_frame = tk.Frame(self.root)
		self.create_grid(settings["grid size"])
		self.mainloop()

	def mainloop(self) -> None:
		self.settings_button.place(x=5, y=5)
		self.new_game_button.pack(padx=5, pady=5)
		self.remaining_bombs_label.pack(padx=5, pady=5)
		self.grid_frame.pack(padx=5, pady=5)
		self.root.mainloop()


def main() -> None:
	GUI().mainloop()


if __name__ in "__main__":
	main()
