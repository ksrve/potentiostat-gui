#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

class Test ():

	def __init__(self, root, obj):
		self.root = root
		self.obj = obj

		# Высота и длина таблицы значений
		self.height = 10
		self.width = 2

		self.entry_list = list()
		self.entry_list_status = list()
		self.voltage_list = list()

		_frame = tk.Frame(self.root,background='#ffffff')
		_frame.grid(row=0,column=0, columnspan=6, sticky="NSEW")

		top_label = tk.Label(_frame, text="TEST & PARAMETERS", font=("Roboto", 14),
		background='#ffffff', foreground='#1990ea')
		top_label.grid(row=0, column=0, sticky="W", padx = 10, pady = 10)

		# Создаем надпись select test
		select_test_label = tk.Label(_frame, text="Select Test", font=("Roboto", 12),
		background='#ffffff', foreground='#212121')
		select_test_label.grid(row=1, column=0, sticky="W", padx = 10, pady = 10)

		self.select_test_box = Combobox(_frame, values=["Zn test","Cyclic"], font=("Roboto", 12),
		background='#666d76', foreground='#666d76', height=2, width=27, state='readonly')
		self.select_test_box.grid(row=2, column=0, sticky="W", padx = 12, pady = 5)
		self.select_test_box.bind("<<ComboboxSelected>>", lambda event: self.select_test(event))
		self.select_test_box.current(0)

		self.select_test(None)

	def destroy_frames(self, frame):
		list = frame.grid_slaves()
		for l in list:
			l.destroy()

	def line_drawing(self, parent, row_begin, column_begin, text_label, entry_var, text_label_, separate, delta_label=0, status=False):
		delta = 0
		if separate:
			delta = 90
		if not status:
			label = tk.Label(parent, text=text_label+" ("+text_label_+")", font=("Roboto", 12),
			background='#ffffff', foreground='#666d76')
		else:
			label = tk.Label(parent, text=text_label, font=("Roboto", 12),
			background='#ffffff', foreground='#666d76')
		label.grid(row=row_begin,column=column_begin, sticky="W", padx=(0,delta_label), pady=(10,0))

		entry = tk.Entry(parent, font=("Roboto", 12), background = '#ffffff',
		foreground='#666d76', textvariable=entry_var, highlightthickness=0, width=12)
		entry.grid(row=row_begin,column=column_begin+1, sticky="W", padx= (0,delta), pady=(10,0))

	def checkbutton_line(self, parent, row, column, text_label, text_var, delta_x=0):

		label = tk.Label(parent, text=text_label, font=("Roboto", 12),
		background='#ffffff', foreground='#666d76')
		label.grid(row=row,column=column, sticky="W", padx=delta_x, pady=(10,0))

		check = tk.Checkbutton(parent, background='#ffffff', highlightthickness=0,
		activebackground="#1990ea", variable=text_var, offvalue=0, onvalue=1, padx=2)
		check.grid(row=row,column=column+1, sticky="W", padx=delta_x, pady=(10,0))

	def data_settings(self, parent, row, column):

		self.output_format_txt = tk.IntVar()
		self.output_format_csv = tk.IntVar()
		self.output_format_csv.set(1)

		self.graphs_save = tk.IntVar()
		self.graphs_drw = tk.IntVar()
		self.graphs_save.set(1)

		self.compound = tk.StringVar()
		self.compound.set("TEST1")

		self.except_first = tk.IntVar()
		self.except_first.set(1)

		self.cycles = tk.IntVar()
		self.cycles.set(1)

		data_set_label = tk.Label(parent, text="Data Output Settings", font=("Roboto", 12),
		background='#ffffff', foreground='#212121')
		data_set_label.grid(row=row,column=column, sticky="W", pady=(20,0))

		data_setting = tk.Frame(parent, background='#ffffff')
		data_setting.grid(row=row+1,column=column, columnspan=7, sticky="NSEW")

		output_format_label = tk.Label(data_setting, text="output format", font=("Roboto", 12, 'underline'),
		background='#ffffff', foreground='#666d76')
		output_format_label.grid(row=0,column=0, sticky="W")

		self.checkbutton_line(data_setting, 1, 0, "txt", self.output_format_txt)
		self.checkbutton_line(data_setting, 2, 0, "csv", self.output_format_csv)

		graphs_label = tk.Label(data_setting, text="graphs", font=("Roboto", 12, 'underline'),
		background='#ffffff', foreground='#666d76')
		graphs_label.grid(row=0,column=2, sticky="W", padx=30)

		self.checkbutton_line(data_setting, 1, 2, "save graphs", self.graphs_save, 30)
		self.checkbutton_line(data_setting, 2, 2, "drawing graphs", self.graphs_drw, 30)

		graphs_label = tk.Label(data_setting, text="test", font=("Roboto", 12, 'underline'),
		background='#ffffff', foreground='#666d76')
		graphs_label.grid(row=0,column=4, sticky="W")

		self.checkbutton_line(data_setting, 1, 4, "except first", self.except_first, 0)
		self.line_drawing(data_setting, 2, 4, "test count",self.cycles, "", False, 0, True)
		self.line_drawing(data_setting, 3, 4, "compound", self.compound, "", True, 50, True)

		check_button = tk.Button(data_setting, text="Run Test !", font=("Roboto", 12),
		background = '#1990ea', foreground='#ffffff', relief = 'flat', width=12, command=self.run_test)
		check_button.grid(row=4,column=5, sticky="W", pady=(20,0))

	def base_settings(self, parent, row, column):
		self.current_range = tk.StringVar()
		self.current_range.set(100)
		self.sample_rate = tk.IntVar()
		self.sample_rate.set(100)
		self.quiet_time = tk.IntVar()
		self.quiet_time.set(0)
		self.quiet_value = tk.IntVar()
		self.quiet_value.set(0)
		base_settings_label = tk.Label(parent, text="Base Settings",
		font=("Roboto", 12), background='#ffffff', foreground='#212121')
		base_settings_label.grid(row=row,column=column, sticky="W")

		base_settings_frame = tk.Frame(parent, background='#ffffff')
		base_settings_frame.grid(row=row+1, column=column, columnspan=7, pady = 10, sticky="W")

		current_range_label = tk.Label(base_settings_frame,  text ="current range (uA)",
									   font=("Roboto", 12), foreground="#666d76" ,background="#ffffff")
		current_range_label.grid(row=row+1, column=column, sticky="W")

		self.current_range_box = Combobox(base_settings_frame, values=["1","10","100","1000"],
										takefocus=False, state="readonly", font=("Roboto", 12) ,background="#ffffff",
										foreground="#666d76", textvariable=self.current_range, width=11)
		self.current_range_box.grid(row=row+1, column=column+1, padx = 30, sticky="W")
		self.current_range_box.current(2)

		rate_label = tk.Label(base_settings_frame,  text ="sample rate (Hz) ",
							font=("Roboto", 12), foreground="#666d76",background="#ffffff")
		rate_label.grid(row=row+2, column=column, pady = 10, sticky="W")

		rate_entry = tk.Entry(base_settings_frame, textvariable=self.sample_rate,
						font=("Roboto", 12), foreground="#666d76",background="#ffffff", width=12, highlightthickness=0)
		rate_entry.grid(row=row+2, column=column+1, padx = 30, sticky="W")
		rate_entry.bind("<FocusIn>", lambda event, f=base_settings_frame: self.callback_rate(event, f))

		time_label = tk.Label(base_settings_frame, text ="quiet time (s)", font=("Roboto", 12),
							foreground="#666d76" ,background="#ffffff")
		time_label.grid(row=row+1, column=column+2, padx = (55,0), sticky="W")
		time_entry = tk.Entry(base_settings_frame, textvariable=self.quiet_time,
							font=("Roboto", 12), foreground="#666d76",background="#ffffff", width=12, highlightthickness=0)
		time_entry.grid(row=row+1, column=column+3, padx = 50, sticky="W")
		time_entry.bind("<FocusIn>", lambda event, f=base_settings_frame: self.callback_time(event, f))

		q_value_label = tk.Label(base_settings_frame,  text ="quiet value (V)",
								font=("Roboto", 12), foreground="#666d76" ,background="#ffffff")
		q_value_label.grid(row=row+2, column=column+2, padx = (55,0), sticky="W")

		q_value_entry = tk.Entry(base_settings_frame, textvariable=self.quiet_value,font=("Roboto", 12),
						foreground="#666d76",background="#ffffff", width=12, highlightthickness=0)
		q_value_entry.grid(row=row+2, column=column+3, padx = 50, sticky="W")
		q_value_entry.bind("<FocusIn>", lambda event, f=base_settings_frame: self.callback_q_value(event, f))

	def pretreat_settings(self, parent, row, column):
		self.e_condition_var = tk.DoubleVar()
		self.t_condition_var = tk.IntVar()
		self.t_condition_var.set(10)
		self.e_depostion_var = tk.DoubleVar()
		self.t_depostition_var = tk.IntVar()
		self.t_depostition_var.set(10)

		pretreat_set_label = tk.Label(parent, text="Pretreatment settings", font=("Roboto", 12),
		background='#ffffff', foreground='#212121')
		pretreat_set_label.grid(row=row,column=column, sticky="W")

		pretreatment_setting = tk.Frame(parent, background='#ffffff')
		pretreatment_setting.grid(row=row+1,column=column, columnspan=7, sticky="NSEW")

		self.line_drawing(pretreatment_setting, 0, 0, "E condition", self.e_condition_var, "V", True, 50)
		self.line_drawing(pretreatment_setting, 1, 0, "t   condition", self.t_condition_var, "s", True)
		self.line_drawing(pretreatment_setting, 0, 3, "E depostion", self.e_depostion_var, "V", True, 40)
		self.line_drawing(pretreatment_setting, 1, 3, "t   depostion", self.t_depostition_var, "s", True)

	def square_wave_settings(self, parent, row, column):

		self.e_begin = tk.DoubleVar()
		self.e_begin.set(-0.5)
		self.e_end = tk.DoubleVar()
		self.e_end.set(0.5)
		self.e_step = tk.DoubleVar()
		self.e_step.set(0.02)
		self.amplitude = tk.DoubleVar()
		self.amplitude.set(0.05)
		self.window = tk.DoubleVar()
		self.window.set(0.2)
		square_wave_set_label = tk.Label(parent, text="Square Wave Voltammetry Settings", font=("Roboto", 12),
		background='#ffffff', foreground='#212121')
		square_wave_set_label.grid(row=row,column=column, sticky="W", pady=(20,0))

		square_wave_setting = tk.Frame(parent, background='#ffffff')
		square_wave_setting.grid(row=row+1,column=column, columnspan=7, sticky="NSEW")

		self.line_drawing(square_wave_setting, 0, 0, "start value", self.e_begin, "V", True, 40)
		self.line_drawing(square_wave_setting, 0, 3, "final value", self.e_end, "V", True, 50)
		self.line_drawing(square_wave_setting, 1, 0, "step value", self.e_step, "V", True, 50)
		self.line_drawing(square_wave_setting, 1, 3, "amplitude", self.amplitude, "V", True, 50)
		self.line_drawing(square_wave_setting, 2, 0, "sample window", self.window, "V", True, 50)

	def make_scrollable_frame(self, parent, height=210, width=670):
		canvas_table = tk.Canvas(parent, background='#ffffff',
		height=height, width=width, borderwidth=0, highlightthickness=0)
		canvas_table.grid(row=0,column=0, sticky='NEWS')
		canvas_table.configure(scrollregion=canvas_table.bbox("all"))

		scroll_vertical = tk.Scrollbar(parent,orient="vertical",command=canvas_table.yview,
		background='#ffffff', activebackground="#ffffff", troughcolor="#1990ea", width=10)
		scroll_vertical.grid(row=0,column=1,sticky=("NEWS"))

		scrollable_frame = tk.Frame(canvas_table, borderwidth=0,
		highlightthickness=0, background='#ffffff')
		scrollable_frame.grid(row=1,column=0,sticky='NEWS')

		scrollable_frame.bind("<Configure>",
		lambda e: canvas_table.configure(
		scrollregion=canvas_table.bbox("all")))
		canvas_table.create_window((0, 0), window=scrollable_frame, anchor="nw")
		canvas_table.configure(yscrollcommand=scroll_vertical.set)

		return scrollable_frame

	def cyclic_settings(self, parent, row, column):
		self.scan_rate = tk.DoubleVar()
		self.scan_rate.set(0.5)

		cyclic_set_label = tk.Label(parent, text="Cyclic Voltammetry Settings", font=("Roboto", 12),
		background='#ffffff', foreground='#212121')
		cyclic_set_label.grid(row=row,column=column, sticky="W", pady=(20,0))

		cyclic_setting = tk.Frame(parent, background='#ffffff')
		cyclic_setting.grid(row=row+1,column=column, columnspan=7, sticky="NSEW")

		self.line_drawing(cyclic_setting, 0, 0, "scan rate", self.scan_rate, "V/s", True, 40)

		names_frame = tk.Frame(cyclic_setting, background='#ffffff')
		names_frame.grid(row=0,column=2, columnspan=2, sticky="NSEW")

		self.nametable(names_frame,["E min","E max"])

		voltage_setting = tk.Frame(cyclic_setting, background='#ffffff')
		voltage_setting.grid(row=1,column=2, columnspan=2, rowspan=3, sticky="NSEW")

		scroll_frame = self.make_scrollable_frame(voltage_setting, 100, 170)
		self.table(scroll_frame)

	def select_test(self, event):

		self.setting_frame = tk.Frame(self.root,background='#ffffff')
		self.setting_frame.grid(row=3,column=0, columnspan=6, sticky="NSEW", padx = 10, pady = 10)
		if self.select_test_box.get() == "Zn test":

			self.destroy_frames(self.setting_frame)
			scroll_frame = self.make_scrollable_frame(self.setting_frame)
			self.base_settings(scroll_frame, 0, 0)
			self.pretreat_settings(scroll_frame, 2, 0)
			self.square_wave_settings(scroll_frame, 4, 0)
			self.data_settings(self.setting_frame, 2, 0)

		elif self.select_test_box.get() == "Cyclic":
			self.destroy_frames(self.setting_frame)
			scroll_frame = self.make_scrollable_frame(self.setting_frame)
			self.base_settings(scroll_frame, 0, 0)
			self.cyclic_settings(scroll_frame, 2, 0)
			self.data_settings(self.setting_frame, 4, 0)

	def check_range(self):
		h = 0
		p = 2
		is_out_of_range = False
		for i in range(self.height):
			if self.entry_list[h:p][0].get() != "":
				if (float(self.entry_list[h:p][0].get()) >= -10.0 and float(self.entry_list[h:p][0].get()) <= 10.0):
					is_out_of_range = False
				else:
					is_out_of_range = True
			if self.entry_list[h:p][1].get() != "":
				if (float(self.entry_list[h:p][1].get()) >= -10 and float(self.entry_list[h:p][1].get()) <= 10):
					is_out_of_range = False
				else:
					is_out_of_range = True

			h+=2
			p+=2
		if is_out_of_range == True:
			messagebox.showerror("Ошибка",
			"Значение напряжения находятся не в диапазоне [-10, 10]!")
			return False
		else:
			return True

	def run_test(self):
		if self.select_test_box.get() == 'Zn test':
			self.obj.constant_voltage_square_wave(self)
		if self.select_test_box.get() == 'Cyclic':
			if self.check_range() == True:
				self.voltage_list.clear()
				h = 0
				p = 2
				for i in range(self.height):
					if (self.entry_list[h:p][0].get() == "" and self.entry_list[h:p][0].get() == ""):
						pass
					else:
						self.voltage_list.append((float(self.entry_list[h:p][0].get()), float(self.entry_list[h:p][1].get())))
					h+=2
					p+=2
				self.obj.set_voltage(self.voltage_list)
			self.obj.cyclic_test(self)

	def callback_focus(self, event, selected_entry):
		"""
		Функция отвечает за фокус на линии в таблице.
		"""
		self.selected_entry = selected_entry
		self.check_empty()

	def check_empty(self):
		if not self.entry_list_status[self.selected_entry] == True:
			h = 0
			p = 2
			is_empty = True
			for i in range(self.height):
				if (self.entry_list[h:p][0].get() != "" and self.entry_list[h:p][1].get() != ""):
					is_empty = False
				h+=2
				p+=2
			if is_empty == False:
				self.listbox = tk.Listbox(self.scrollable_frame, background='#ffffff', borderwidth=0, highlightthickness=0)
				self.listbox.grid(row=self.height, column=0)
				for j in range(self.width):
					## Создание полей в строках
					self.entry = tk.Entry(self.listbox, text="", background="#ffffff", foreground='#1990ea', font=("Roboto", 16),
					width = 15, highlightbackground="#ffffff",  borderwidth=0, highlightthickness=0)
					self.entry.grid(row=self.height, column=j, padx = 5, pady = 5,  sticky='NEWS')
					self.entry_list.append(self.entry)
					self.entry.bind("<FocusIn>", lambda event, f=int(self.width/self.width): self.callback_focus(event, f))
				self.height+=1
				self.entry_list_status[self.selected_entry] = True
				self.entry_list_status.append(False)
			else:
				num_delete = self.height - 10
				if not num_delete == 0:
					for i in (self.height-num_delete, self.height):
						#self.entry_list[i].destroy()
						self.height = 10

	def nametable(self, root, names):
		"""
		Функция отвечает за создание таблицы наименований.
		"""
		b = tk.Frame(root, background='#ffffff')
		b.grid(row = 0, column = 0)
		for j in range(self.width):
			x = tk.Label(root, background='#ffffff',text=str(names[j]),font=("Roboto", 12), foreground='#666d76',
			highlightbackground="#ffffff", borderwidth=0, highlightthickness=0)
			x.grid(row = 0, column = j, padx = (0,21), sticky='NEWS')

	def error_connection(self):
		messagebox.showerror("Ошибка",
		"Устройство не подключено!")

	def table(self, parent):
		"""
		Функция отвечает за создание таблицы
		с заданной высотой.
		"""
		self.height = 10
		background_color="#ffffff"
		for i in range(self.height):
			self.listbox = tk.Listbox(parent, background='#ffffff', borderwidth=0, highlightthickness=0)
			self.listbox.grid(row=i, column=0)
			for j in range(self.width):
				## Создание полей в строках
				self.entry = tk.Entry(self.listbox, text="", background="#ffffff", foreground='#666d76', font=("Roboto", 12),
				width = 6,  highlightbackground="#ffffff", highlightthickness=1)
				self.entry.grid(row=i, column=j, padx = (0,6), pady = 2,  sticky='NEWS')
				self.entry_list.append(self.entry)
		for k in range(len(self.entry_list)):
			## Добавление фокуса в каждую строку
			self.entry_list[k].bind("<FocusIn>", lambda event, f=int(k/self.width): self.callback_focus(event, f))
			self.entry_list_status.append(False)
