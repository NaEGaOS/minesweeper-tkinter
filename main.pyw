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
	def __init__(self, button: tk.Button, position: tuple[int, int], value: int | str = 0) -> None:
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
		self.first_pressed = True
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
	
	def create_grid(self, dimentions: tuple[int, int]) -> None:
		self.square_reference = {}
		for row in range(dimentions[0]):
			for column in range(dimentions[1]):
				square = Square(tk.Button(self.grid_frame, text="", width=2, height=1, bg=button_colours["raised"],
				    					  command=lambda row=row, column=column: self.leftclick(row, column)),
								(row, column))
				square.button.bind("<Button-3>", lambda event, row=row, column=column: self.rightclick(row, column))
				square.button.grid(row=row, column=column)
				self.square_reference[(row, column)] = square
	
	def apply_pattern(self, dimentions: tuple[int, int], total_bombs: int, clicked_square: Square) -> None:
		bombs_remaining = total_bombs
		while bombs_remaining > 0:
			row, column = (random.randint(0, dimentions[0] - 1), random.randint(0, dimentions[1] - 1))
			current_square = self.square_reference[(row, column)]
			# first square must be blank
			if abs(row - clicked_square.position[0]) <= 1 and abs(column - clicked_square.position[1]) <= 1:
				continue
			if current_square.value == "b":
				continue
			current_square.value = "b"
			bombs_remaining -= 1
			# increment surrounding squares
			for row_offset in range(-1, 2):
				for column_offset in range(-1, 2):
					if row_offset == column_offset == 0:  # skips center square
						continue
					if not (0 <= row + row_offset < dimentions[0] and 0 <= column + column_offset < dimentions[1]):
						continue
					increment_square = self.square_reference[(row+row_offset, column+column_offset)]
					if increment_square.value != "b":
						increment_square.value += 1

	def leftclick(self, row: int, column: int) -> None:

		def clear_zeros(triggered_square: Square) -> None:
			queue = [triggered_square]
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

		if self.first_pressed:
			self.apply_pattern(settings["grid size"], settings["total bombs"], self.square_reference[(row, column)])
			self.first_pressed = False
		square = self.square_reference[(row, column)]
		if square.button["relief"] == "sunken" or square.flag or self.game_over:  # won't press if already pressed, flagged, or game over
			return
		if square.value == "b":
			self.game_over = True
			self.remaining_bombs_label.config(text="losser :( :( :(")
			# reveal all bombs
			for current_square in self.square_reference.values():
				if current_square.value == "b" and not current_square.flag:  # unflagged bomb
					current_square.button.config(text=None, image=self.image_bomb, width=18, height=20)
				elif current_square.flag and current_square.value != "b":  # wrong flag
					current_square.button.config(text=None, image=self.image_bomb_crossed, width=18, height=20)
			return
		square.button.config(text=square.value if square.value != 0 else "", relief="sunken", fg=number_colours[str(square.value)],
								 bg=button_colours["sunken"])
		if square.value == 0:
			clear_zeros(square)
		self.check_win()

	def rightclick(self, row: int, column: int) -> None:
		square = self.square_reference[(row, column)]
		square.flag = not square.flag
		if square.flag:
			square.button.config(text=None, image=self.image_flag, width=18, height=20)
			self.remaining_bombs -= 1
		else:
			square.button.config(text=None, image="", fg=number_colours[str(square.value)], width=2, height=1)
			self.remaining_bombs += 1
		self.remaining_bombs_label.config(text=f"Remaining Bombs: {self.remaining_bombs}")
		self.check_win()
	
	def check_win(self) -> None:
		# check if all bombs are flagged
		all_bombs_flagged = all(square.flag for square in self.square_reference.values() if square.value == "b")
		# check if all non-bombs are pressed
		all_pressed = all(square.button["relief"] == "sunken" for square in self.square_reference.values() if square.value != "b")
		if (all_bombs_flagged and self.remaining_bombs == 0) or all_pressed:
			self.game_over = True
			self.remaining_bombs_label.config(text="you win :) :) :)")

	def reset(self) -> None:
		self.game_over = False
		self.first_pressed = True
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
