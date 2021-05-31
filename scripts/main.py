#!/usr/bin/python
# -*- coding: utf-8 -*-

from potentiostatapp import *
from utils import *
import connection
import maketest
import history
import settings

class GUI (Frame):

	def __init__(self, root):
		Frame.__init__(self, root)
		self.root = root
		self.root.title("Potentiostat")
		## Описание стиля графического окна
		style = ttk.Style(root)
		style.theme_create( "theme", parent="classic", settings={
		"TNotebook": {"configure": {"background": '#f5f6fa', "tabposition": "wn", "borderwidth": "0"}},
		"TCombobox": {"configure": {'selectbackground': 'white',
		"height": "10", "font":("Roboto", "12"), 'selectforeground': '#666d76', 'relief':'flat',"borderwidth": "1"}},
		"TNotebook.Tab": {
			"configure": {"padding": [25, 20],"height": "15","width": "20", "background": '#f5f6fa',"borderwidth": "0",
			"foreground": '#1990ea',"font":("Roboto", "14")},
			"map":       {"background": [("selected", '#1990ea')],
						  "foreground": [("selected", '#ffffff')],
						  "expand": [("selected", "#1990ea")] } },
		"TCheckButton": {"configure": {"background": '#ffffff', "tabposition": "wn"}}})
		style.configure("theme", focuscolor=style.configure(".")["background"])
		style.theme_use("theme")

		self.pw_top = tk.Frame(self.root, background='#ffffff')
		self.pw_top.grid(row=0,column=0, sticky="NSEW",
		padx = 10, pady = 10)

		electroSense_label = tk.Label(self.pw_top, text="\t\t\t\t\t\tElectroSense",
		font=("Roboto", 22), background='#ffffff', foreground='#1990ea')
		electroSense_label.grid(row=0, column=0, sticky="E")
		# Создаем левую панель для размещения элементов
		self.pw_left = tk.Frame(self.root, background='#ffffff')
		self.pw_left.grid(row=1, column=0, sticky="NSEW", padx = 10, pady = 10)

		# Создаем закладки
		n = ttk.Notebook(self.pw_left, width=710, height=640)
		n.grid(row=1,column=0, sticky="NEWS")
		self.main_object = PotentiostatAPP(self.pw_left)

		Connect             = tk.Frame(n, background='#ffffff')
		Test                = tk.Frame(n, background='#ffffff')
		History             = tk.Frame(n, background='#ffffff')
		Settings            = tk.Frame(n, background='#ffffff')

		self.connection_obj = connection.Connection(Connect, self.main_object)
		self.maketest_obj   = maketest.Test(Test, self.main_object)
		self.history_obj    = history.History(History)
		self.settings_obj   = settings.Settings(Settings)

		n.add(Connect  ,text='DEVICE CONNECTION')
		n.add(Test     ,text='TEST & PARAMETERS')
		#n.add(History  ,text='History')
		#n.add(Settings ,text='Settings')

def main():
	try:
		mainwindow = tk.Tk()
	except:
		logging.error("Error initializing Tkinter!\n\nShutting down\n\nPress any key" )
		sytem.exit(0)

	# Размеры главного окна
	req_width = 1000
	req_height = 650
	# Настройка открытия окна на центре экрана
	positionRight = int(mainwindow.winfo_screenwidth()/2 - req_width/2)
	positionDown = int(mainwindow.winfo_screenheight()/2.2 - req_height/2)
	mainwindow.geometry('+{}+{}'.format(positionRight, positionDown))
	mainwindow.geometry('{}x{}'.format(req_width,req_height))
	# Запретить изменять размеры приложения
	mainwindow.resizable(width=False, height=False)
	## Создаем экземпляр класса PotentiostatAPP
	app = GUI(mainwindow)
	# Запуск цикла главного окна графического интерфейса
	try:
		mainwindow.mainloop()
	except KeyboardInterrupt:
		logging.error('Exiting program...')  # will not print anything
		sys.exit(0)

if __name__ == '__main__':
	main()
