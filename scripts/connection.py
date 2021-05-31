#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import *

class Connection():

	def __init__(self, root, main_object):
		self.root = root
		self.main_object = main_object

		self.root.option_add('*TCombobox*Listbox.font', ("Roboto", "12"))
		self.root.option_add('*TCombobox.font', ("Roboto", "12"))
		self.root.option_add('*TCombobox*Listbox.selectbackground', '#ffffff')
		self.root.option_add('*TCombobox.selectbackground', '#ffffff')
		self.root.option_add('*TCombobox.insertbackground', '#ffffff')
		self.root.option_add("*TCombobox*Listbox*Background", '#ffffff')
		self.root.option_add('*TCombobox*Listbox.fieldbackground', '#ffffff')
		self.root.option_add('*TCombobox*Listbox.highlightthickness ', '0')
		self.root.option_add('*TCombobox*Listbox.height', '4')

		self.text = tk.StringVar()
		self.text_id = tk.StringVar()
		self.text_fw = tk.StringVar()
		self.text_hw = tk.StringVar()

		# Создаем надпись ElectroSense
		top_label = tk.Label(self.root, text="DEVICE CONNECTION", font=("Roboto", 14),
		background='#ffffff', foreground='#1990ea')
		top_label.grid(row=0, column=0, sticky="W", padx = 10, pady = 10)

		# Создаем надпись SELECT YOUR DEVICE
		select_device_label = tk.Label(self.root, text="select your device", font=("Roboto", 14), bg='#ffffff', fg='#1990ea')
		select_device_label.grid(row=2, column=0, sticky="W", padx = 10, pady = (50,10))

		# Создаем выпадающий список
		self.combo = Combobox(self.root,postcommand=self.change_ports, values=["None"], state='readonly',
		background='#666d76', foreground='#666d76')
		self.combo.bind("<<ComboboxSelected>>", self.callback_focus)
		self.combo.grid(row=3, column=0, sticky="W", padx = 10, pady = 10)
		self.combo.current(0)

		# Создаем кнопку BUTTON
		connect_button = tk.Button(self.root, text="connect", font=("Roboto", 14),
		command= lambda: self.main_object.potentiostat_connect(self), width=20, bg = '#1990ea', fg='#ffffff', relief = 'flat')
		connect_button.grid(row=4, column=0, sticky="W", padx = 10, pady = 10)

		self.label_stat= tk.Label(self.root, font=("Roboto", 14),bg="#ffffff", textvariable=self.text)
		self.label_stat.grid(row=1, column=0, sticky="W", padx = 10, pady = 20)

		self.label_id = tk.Label(self.root, textvariable=self.text_id, font=("Roboto", 12),bg="#ffffff",fg="#666d76")
		self.label_id.grid(row=5, column=0, sticky="W", padx = 10, pady = (70,10))

		self.label_fw = tk.Label(self.root, textvariable=self.text_fw, font=("Roboto", 12),bg="#ffffff",fg="#666d76")
		self.label_fw.grid(row=6, column=0, sticky="W", padx = 10, pady = 10)

		self.label_hw = tk.Label(self.root, textvariable=self.text_hw, font=("Roboto", 12),bg="#ffffff",fg="#666d76")
		self.label_hw.grid(row=7, column=0, sticky="W", padx = 10, pady = 10)

		self.update_status()

	def update_status(self):
		flag = False
		if self.main_object.status_connection.get() == False:
			self.text.set("status: disconnected")
			self.text_id.set("Device id:            " )
			self.text_fw.set("Firmware version:     " )
			self.text_hw.set("Hardware version:     ")
			self.label_stat.config(fg='#ea6b66')
		elif self.main_object.status_connection.get() == True:
			self.text.set("status: connected")
			self.text_id.set("Device id:                   " + str(self.main_object.pstat.get_device_id()))
			self.text_fw.set("Firmware version:      " + str(self.main_object.pstat.get_firmware_version()))
			self.text_hw.set("Hardware version:     " + str(self.main_object.pstat.get_hardware_variant()))
			flag = True
			self.label_stat.config(fg='#6dcf95')
		if flag == False:
			self.root.after(2000, self.update_status)

	def serial_ports(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		else:
			raise EnvironmentError('Unsupported platform')
		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result

	def change_ports(self):
		result = self.serial_ports()
		if len(result) > 0:
			self.combo["values"] =  ("None", result)
		else:
			self.combo["values"] =  ("None")
		self.combo.current(0)

	def callback_focus(self, event):
		self.event = self.combo.get()
