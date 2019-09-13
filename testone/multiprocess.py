# -*- coding: utf-8 -*-
import sys
import csv
from collections import namedtuple
import queue
from multiprocessing import Queue,Process

IncomeLookup = namedtuple('IncomeLookup',
	['start','tax_rate','quick_sub'])
Income_Point = 5000
Income_Table = [
		IncomeLookup(80000,0.45,15160),
		IncomeLookup(55000,0.35,7160),
		IncomeLookup(35000,0.30,4410),
<<<<<<< HEAD
		IncomeLookup(25000,0.25,2660),
		IncomeLookup(12000,0.2,1410),
		IncomeLookup(3000,0.1,210),
		IncomeLookup(0,0.03,0)
]


=======
		IncomeLookup(80000,0.45,15160),
		IncomeLookup(80000,0.45,15160),
		IncomeLookup(80000,0.45,15160),
		IncomeLookup(80000,0.45,15160),
		IncomeLookup(80000,0.45,15160),
]
>>>>>>> d3d606d1b741a84ae446d4d00f2ccfc9d3c0a6ee
