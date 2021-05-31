#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging

import sys
import glob
import serial
import csv

import pathlib

import datetime
import numpy as np

## Импорт библиотеки tkinter
try:
	import Tkinter as tk	# Python 2.X
except ImportError:
	import tkinter as tk	# Python 3.X
try:
	import 	ttk
	from 		ttk import *
except ImportError:
	from		tkinter import ttk
	from 		tkinter.ttk import *
## Импорт библиотеки PIL
try:
	from PIL import ImageTk, Image, ExifTags
except ImportError:
	raise ("ImageTk not installed. If running Python 3.x\n" \
			 "Use: sudo apt-get install python3-pil.imagetk")
from tkinter import messagebox

ROOT_DIR = pathlib.Path.home()
INSTALL_DIR = "/Desktop/potentiostat-gui/"
DATA_DIR = pathlib.Path.home().joinpath("Desktop","potentiostat-gui", "data")


def generate_dir(compound, data):
	directory = DATA_DIR.joinpath(compound)
	directory = directory.joinpath(data)
	directory.mkdir(parents=True, exist_ok=True)
	return directory

def generate_file_names(compound, data, adding=''):
	filenames_data = list()
	filenames_graphs = list()
	if compound != "":
		filename = compound + "_"+ adding + "_" + data
	dir = generate_dir(compound, data)
	filename_txt   = dir.joinpath(adding + "_" + "data_output.txt")
	filename_csv_1 = dir.joinpath(adding + "_" + "current_compound.csv")
	filename_csv_2 = dir.joinpath(adding + "_" + "current_voltage.csv")

	filenames_data.append(filename_txt)
	filenames_data.append(filename_csv_1)
	filenames_data.append(filename_csv_2)

	filename_graphs_1 = dir.joinpath(adding + "_" + "img_output_1.png")
	filename_graphs_2 = dir.joinpath(adding + "_" + "img_output_2.png")

	filenames_graphs.append(filename_graphs_1)
	filenames_graphs.append(filename_graphs_2)
	return filenames_data, filenames_graphs
