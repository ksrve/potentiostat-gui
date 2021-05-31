#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

class History():

	def __init__(self, root):
		self.root = root
		self.dir = ""

		self.width = 4
		self.height = 3
		self.entry_list = []
		self.entry_list_status = []
		self.list_array = []
		self.list_status = []
		self.entry_old = -1

		# Создаем надпись ElectroSense
		select_device_label = tk.Label(self.root, text="History of experiments", font=("Roboto", 14),
		bg='#ffffff', fg='#1990ea')
		select_device_label.grid(row=0, column=0, sticky="W", padx = 10, pady = 10)

		## Определение таблицы таблицы значений
		frame_table = tk.Frame(self.root, background='#ffffff',
		height=500, width=540, highlightthickness=0)
		frame_table.grid(row=1,column=0, rowspan=6, sticky="W", padx = 10, pady = 5)

		## Определение таблицы названий переменных
		frame_table_1 = tk.Frame(frame_table, background='#ffffff')
		frame_table_1.grid(row=0, column=0, sticky='W')

		## Создание таблицы названий переменных
		self.nametable(frame_table_1,["Date","Compound","Parameters", "Data"])

		canvas_table = tk.Canvas(frame_table, background='#ffffff', highlightbackground="#1990ea",
		height=500, width=540, borderwidth=0, highlightthickness=0)
		canvas_table.grid(row=1,column=0, sticky='NEWS')
		canvas_table.configure(scrollregion=canvas_table.bbox("all"))

		scroll_vertical = tk.Scrollbar(frame_table,orient="vertical",command=canvas_table.yview,
		background='#ffffff',activebackground="#ffffff",troughcolor="#1990ea", width=20)
		scroll_vertical.grid(row=1,column=1,sticky=("NEWS"))

		self.scrollable_frame = tk.Frame(canvas_table, borderwidth=0, highlightthickness=0)
		self.scrollable_frame.grid(row=1,column=0,sticky='NEWS')

		self.scrollable_frame.bind(
			 "<Configure>",
			 lambda e: canvas_table.configure(
				 scrollregion=canvas_table.bbox("all")
			 )
		 )
		self.tableframe = self.scrollable_frame
		## Возможность пролистывания данных
		canvas_table.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		canvas_table.configure(yscrollcommand=scroll_vertical.set)
		self.table()

	def callback_focus(self, event, selected_entry):
		self.selected_entry = selected_entry
		self.list_array[self.selected_entry].config(background='#ebe8e8')
		if self.entry_old != self.selected_entry:
			self.list_array[self.entry_old].config(background='#ffffff')
		self.entry_old = self.selected_entry

	def nametable(self, root, names):
		b = tk.Frame(root, background='#ffffff')
		b.grid(row = 0, column = 0)
		for j in range(self.width):
			x = tk.Label(root, background='#ffffff',text=str(names[j]),font=("Roboto", 12), foreground='#666d76',
			width=14, highlightbackground="#ffffff",  borderwidth=0, highlightthickness=0)
			x.grid(row = 0, column = j,padx = 5, sticky='NEWS')

	def table(self):
		self.height = 14
		for i in range(self.height):
			self.listbox = tk.Listbox(self.scrollable_frame, background='#ffffff', borderwidth=0, highlightthickness=0)
			self.listbox.grid(row=i, column=0)
			self.list_array.append(self.listbox)
			for j in range(self.width):
				## Создание полей в строках
				self.entry = tk.Entry(self.listbox, text="", background="#ffffff",
				foreground='#666d76', font=("Roboto", 12),
				width = 14, highlightbackground="#ffffff", highlightthickness=1)
				self.entry.grid(row=i, column=j, padx = 5,
				pady = 5, sticky='NEWS')
				self.entry_list.append(self.entry)
		for k in range(len(self.entry_list)):
			## Добавление фокуса в каждую строку
			self.entry_list[k].bind("<FocusIn>", lambda event, f=int(k/self.width): self.callback_focus(event, f))
