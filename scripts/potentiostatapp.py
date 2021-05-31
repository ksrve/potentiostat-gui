#!/usr/bin/python
# -*- coding: utf-8 -*-

import connection
import maketest
import history
import main
import serial

import matplotlib.pyplot as plt

from utils import *
from potentiostat import Potentiostat

class PotentiostatAPP (object):

	def __init__(self, pw_right=None):

		self.pstat = None
		self.status_connection = tk.BooleanVar()
		self.status_connection.set(0)

		self.circles = 0

		self.queue_sign = []
		self.queue_current = []
		self.queue_volt = []

		self.test_count = 0

		self.now = None

		self.voltage_list = None
		self.pw_right = pw_right

	def set_voltage(self, voltage_list):
		self.voltage_list = voltage_list

	def get_voltage(self):
		return self.voltage_list

	def calculate_amplitude(self, volt_min, volt_max):
		return 0.5*(volt_max - volt_min)

	def calculate_offset(self, volt_min, volt_max):
		return 0.5*(volt_max + volt_min)

	def calculate_period(self, amplitude, scan_rate):
		return int(1000*4*amplitude/scan_rate)

	def make_graphs(self, other, t, volt, curr, filenames_graphs):

		plt.show(block=False)

		# plot results using matplotlib
		plt.figure(1)
		plt.subplot(211)
		plt.plot(t,volt)
		plt.ylabel('potential (V)')
		plt.grid('on')

		plt.subplot(212)
		plt.plot(t,curr)
		plt.ylabel('current (uA)')
		plt.xlabel('time (sec)')
		plt.grid('on')

		self.save_graphs(other, plt, filenames_graphs[0])

		plt.figure(2)
		plt.plot(volt,curr)
		plt.xlabel('potential (V)')
		plt.ylabel('current (uA)')
		plt.grid('on')

		self.save_graphs(other, plt, filenames_graphs[1])

		if other.graphs_drw.get() == 1:
			plt.show(block=False)

	def save_graphs(self, other, plt, filename):
		if other.graphs_save.get() == 1:
			plt.savefig(filename)

	def constant_voltage_square_wave(self, other):
		self.test_count = 0

		self.queue_sign.clear()
		self.queue_current.clear()
		self.queue_volt.clear()
		if True:
			self.now = datetime.datetime.today().strftime("%d_%m_%Y_%H_%M_%S")

			self.pstat.set_curr_range(other.current_range.get()+ 'uA')
			self.pstat.set_sample_rate(other.sample_rate.get())
			params_c_w_1 = {
			'quietValue' : other.quiet_value.get(),
			'quietTime'  : other.quiet_time.get(),
			'value'      : other.e_condition_var.get(),
			'duration'   : other.t_condition_var.get(),
			'numCycles'  : other.cycles.get(),
			}
			params_c_w_2 = {
			'quietValue' : other.quiet_value.get(),
			'quietTime'  : other.quiet_time.get(),
			'value'      : other.e_depostion_var.get(),
			'duration'   : other.t_depostition_var.get(),
			'numCycles'  : other.cycles.get(),
			}
			params_s_w = {
			'quietValue' : other.quiet_value.get(),
			'quietTime'  : other.quiet_time.get(),
			'startValue' : other.e_begin.get(),
			'finalValue' : other.e_end.get(),
			'stepValue'  : other.e_step.get(),
			'amplitde'   : other.amplitude.get(),
			'window'     : other.window.get(),
			}
			print("----------------------------------------")
			print("Output format txt: " + str(other.output_format_txt.get()))
			print("Output format csv: " + str(other.output_format_csv.get()))
			print("Drawing graphs: " + str(other.graphs_drw.get()))
			print("Save graphs: " + str(other.graphs_save.get()))
			print("Compound value: " + str(other.compound.get()))
			print("Except first: " + str(other.except_first.get()))
			print("----------------------------------------")

			filenames_data, filenames_graphs = generate_file_names(other.compound.get(), self.now, adding="constant")
			filenames_data1, filenames_graphs1 = generate_file_names(other.compound.get(), self.now, adding="squarewave")

			print("Params for testing: " + str(params_c_w_1))
			print("Params for testing: " + str(params_c_w_2))
			print("Params for testing: " + str(params_s_w))

			total_voltage = []
			total_current = []
			time = []

			if other.output_format_csv.get() == 1:
				if other.output_format_txt.get() == 1:

					self.pstat.set_param('constant', param=params_c_w_1)
					t,volt,curr = self.pstat.run_test('constant',filename=filenames_data[0])

					total_voltage.append(volt[0])
					total_current.append(curr[0])
					time.append(t)

					self.pstat.set_param('constant', param=params_c_w_2)
					t,volt,curr = self.pstat.run_test('constant',filename=filenames_data[0])

					total_voltage.append(volt[0])
					total_current.append(curr[0])
					time.append(t)
					self.make_graphs(other, time, total_voltage, total_current, filenames_graphs)

					self.pstat.set_param('squareWave', param=params_s_w)
					t,volt,curr = self.pstat.run_test('squareWave',filename=filenames_data1[0])
					self.make_graphs(other, t, volt, curr, filenames_graphs1)
				else:

					self.pstat.set_param('constant', param=params_c_w_1)
					t,volt,curr = self.pstat.run_test('constant')

					total_voltage.append(volt[0])
					total_current.append(curr[0])
					time.append(t)

					self.pstat.set_param('constant', param=params_c_w_2)
					t,volt,curr = self.pstat.run_test('constant')

					total_voltage.append(volt[0])
					total_current.append(curr[0])
					time.append(t)

					self._save_data_csv(total_voltage, total_current, other.compound.get(),
					other.except_first.get(), filenames_data[1], filenames_data[2])
					self.make_graphs(other, time, total_voltage, total_current, filenames_graphs)

					self.queue_sign.clear()
					self.queue_current.clear()
					self.queue_volt.clear()

					self.pstat.set_param('squareWave', param=params_s_w)
					t,volt,curr = self.pstat.run_test('squareWave')
					self._save_data_csv(volt, curr, other.compound.get(),
					other.except_first.get(), filenames_data1[1], filenames_data1[2])

					self.make_graphs(other, t, volt, curr, filenames_graphs1)



	def cyclic_test(self, other):
		self.circles = other.cycles.get()
		self.test_count = 0
		if not len(self.queue_sign) == 0:
			self.queue_sign.clear()
			self.queue_current.clear()
			self.queue_volt.clear()
		if True:
			self.now = datetime.datetime.today().strftime("%d_%m_%Y_%H_%M_%S")
			for i in range(len(self.get_voltage())):
				self.pstat.set_curr_range(other.current_range.get()+ 'uA')
				print(other.current_range.get())
				self.pstat.set_sample_rate(other.sample_rate.get())
				params = {
				'quietValue' : other.quiet_value.get(),
				'quietTime'  : other.quiet_time.get(),
				'amplitude'  : self.calculate_amplitude(self.get_voltage()[i][0], self.get_voltage()[i][1]),
				'offset'     : self.calculate_offset(self.get_voltage()[i][0], self.get_voltage()[i][1]),
				'period'     : self.calculate_period(self.calculate_amplitude(self.get_voltage()[i][0], self.get_voltage()[i][1]), other.scan_rate.get()),
				'numCycles'  : other.cycles.get(),
				'shift'      : 0.0,
				}
				print("Params for testing: " + str(params))
				self.pstat.set_param('cyclic', param=params)

				print("----------------------------------------")
				print("Output format txt: " + str(other.output_format_txt.get()))
				print("Output format csv: " + str(other.output_format_csv.get()))
				print("Drawing graphs: " + str(other.graphs_drw.get()))
				print("Save graphs: " + str(other.graphs_save.get()))
				print("Compound value: " + str(other.compound.get()))
				print("Except first: " + str(other.except_first.get()))
				print("----------------------------------------")

				filenames_data, filenames_graphs = generate_file_names(other.compound.get(), self.now)

				if other.output_format_csv.get() == 1:
					if other.output_format_txt.get() == 1:
						t,volt,curr = self.pstat.run_test('cyclic',filename = filenames_data[0])
						self.make_graphs(other, t, volt, curr, filenames_graphs)
					else:
						t,volt,curr = self.pstat.run_test('cyclic')
						self.save_data_csv(self.get_voltage()[i][1],volt, curr,
						other.compound.get(), other.except_first.get(), filenames_data[1], filenames_data[2])
						self.make_graphs(other, t, volt, curr, filenames_graphs)
		else:
			messagebox.showerror("Ошибка",
			"Не все параметры заполнены!")

	def generate_matrix(self, list_of_values):
		print(list_of_values)
		length = max(map(len , list_of_values))
		array_of_values = np.array([xi+[np.nan]*(length-len(xi)) for xi in list_of_values])
		matrix = array_of_values.transpose()
		return matrix

	def _save_data_csv(self,voltage, current, compound, except_first, filename_1, filename_2):
		self.queue_volt.append(voltage)
		self.queue_current.append(current)
		volt_array_base = self.generate_matrix(self.queue_volt)
		curr_array_base = self.generate_matrix(self.queue_current)

		curr_array  = np.c_[curr_array_base, np.full((curr_array_base.shape[0], 1), compound)]
		curr_volt_array  = np.c_[volt_array_base, curr_array_base]
		with open(filename_1, "w", newline="") as file:
			writer = csv.writer(file)
			for row in curr_array:
				writer.writerow(row)
		with open(filename_2, "w", newline="") as file:
			writer = csv.writer(file)
			for row in curr_volt_array:
				writer.writerow(row)
		messagebox.showinfo("Потенциостат",
		"Тест завершен!")

	def save_data_csv(self, volt_max, voltage, current, compound, except_first, filename_1, filename_2):
		if len(self.get_voltage()) - self.test_count >= 1:
			self.queue_sign.append(volt_max)
			self.queue_volt.append(voltage)
			self.queue_current.append(current)
		if len(self.get_voltage()) - self.test_count == 1:
			if except_first == 1:
				#volt_ex, curr_ex = self.except_first(self.queue_sign, self.queue_volt, self.queue_current)
				volt_array_base = self.generate_matrix(self.queue_volt)
				curr_array_base = self.generate_matrix(self.queue_current)
			else:
				volt_array_base = self.generate_matrix(self.queue_volt)
				curr_array_base = self.generate_matrix(self.queue_current)
			if compound != "":
				self.queue_sign.append(compound)
				curr_array  = np.c_[curr_array_base, np.full((curr_array_base.shape[0], 1), compound)]
			curr_volt_array  = np.c_[volt_array_base, curr_array_base]

			with open(filename_1, "w", newline="") as file:
				writer = csv.writer(file)
				for row in curr_array:
					writer.writerow(row)
			with open(filename_2, "w", newline="") as file:
				writer = csv.writer(file)
				for row in curr_volt_array:
					writer.writerow(row)
		messagebox.showinfo("Потенциостат",
		"Тест завершен!")

		self.test_count += 1

	def potentiostat_connect(self, other):
		port = str(other.event)
		print("PORT: " + port)
		if (self.status_connection.get() == False):
			try:
				self.pstat = Potentiostat(port)
			except serial.serialutil.SerialException or AttributeError:
				print("Wrong port!")
				messagebox.showerror("Ошибка",
				"Не могу подключиться к этому порту!")
			except OSError:
				messagebox.showerror("Ошибка",
				"Не могу подключиться к этому порту!")
			else:
				print("Connected!")
				self.status_connection.set(1)
		else:
			messagebox.showerror("Ошибка",
			"Устройство уже подключено!")
