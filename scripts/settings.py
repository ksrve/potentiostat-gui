#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

from tkinter import messagebox
from tkinter import filedialog

class Settings():

	def directory_focus(self, event):
		folder_selected = filedialog.askdirectory()
		self.dir.set(folder_selected)

	def __init__(self, root):
		self.root = root
		self.dir = tk.StringVar()
		# Создаем надпись ElectroSense
		select_device_label = tk.Label(self.root, text="Settings for the potentiostat", font=("Roboto", 14),
		bg='#ffffff', fg='#1990ea')
		select_device_label.grid(row=0, column=0, sticky="W", padx = 10, pady = 10)

		select_device_label = tk.Label(self.root, text="Select saving directory", font=("Roboto", 12),
		bg='#ffffff', fg='#666d76')
		select_device_label.grid(row=1, column=0, sticky="W", padx = 10, pady = 10)

		self.en_1 = tk.Entry(self.root, font=("Roboto", 12), background='#ffffff',
		foreground='#666d76', textvariable=self.dir, width=15)
		self.en_1.grid(row=1,column=1,sticky='W',padx = 50, pady = 20)
		self.en_1.bind("<1>", lambda event: self.directory_focus(event))

		select_device_label = tk.Label(self.root, text="Settings for the program", font=("Roboto", 14),
		bg='#ffffff', fg='#1990ea')
		select_device_label.grid(row=2, column=0, sticky="W", padx = 10, pady = (70,10))

		select_device_label = tk.Label(self.root, text="Update software", font=("Roboto", 12),
		bg='#ffffff', fg='#666d76')
		select_device_label.grid(row=3, column=0, sticky="W", padx = 10, pady = 10)

		test_button = tk.Button(self.root, text="run update", font=("Roboto", 14), background = '#1990ea',
		foreground='#ffffff', relief = 'flat', height=1, width=12, command=self.run_update, highlightthickness=1)
		test_button.grid(row=3,column=1, sticky="W", padx = 50, pady = 10)

		select_device_label = tk.Label(self.root, text="Update hardware", font=("Roboto", 12),
		bg='#ffffff', fg='#666d76')
		select_device_label.grid(row=4, column=0, sticky="W", padx = 10, pady = 10)

		test_button = tk.Button(self.root, text="run update", font=("Roboto", 14), background = '#1990ea',
		foreground='#ffffff', relief = 'flat', height=1, width=12, command=self.run_update, highlightthickness=1)
		test_button.grid(row=4,column=1, sticky="W", padx = 50, pady = 10)

	def run_update(self):
		print("Update")
