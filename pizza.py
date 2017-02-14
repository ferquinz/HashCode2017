from sys import argv
from numpy import *
import math

script, filename = argv


class Complex:
    def __init__(self):
        # self.data = [["" for x in range(columns)] for y in range(rows)]
        self.data = []
        self.min = 0
        self.max = 0
        self.rows = 0
        self.columns = 0
        self.mushrooms = 0
        self.tomatoes = 0



    def readfile(self, file):
        with file as f:
            lines = f.read().splitlines()
            self.rows, self.columns, self.min, self.max = [int(x) for x in lines.pop(0).split(' ')]
            for row in range(self.rows):
                self.data.append(tuple(lines[row]))
            
            for row in range(self.rows):
                ntomatoes = self.data[row].count("T")
                self.tomatoes += ntomatoes
                self.mushrooms += self.columns - ntomatoes


    def calculateslices(self):
        max_slices = math.ceil((self.rows * self.columns) / self.max)
        print('Maximo numero de conjuntos: ', max_slices)
        if self.tomatoes < self.mushrooms:
            num_tomatoes_slice = self.tomatoes / self.min
            tomatoes_per_context = max_slices / num_tomatoes_slice
            print('Care tomatoes, per slice: ', tomatoes_per_context)
        elif self.tomatoes == self.mushrooms:
            num_per_slice = self.tomatoes / self.min
            per_context = math.ceil(max_slices / num_per_slice)
            print('Are the same, per slice: ', per_context)
        else:
            num_mushrooms_slice = self.mushrooms / self.min
            mushrooms_per_context = math.ceil(max_slices / num_mushrooms_slice)
            print('Care mushrooms, per slice: ', mushrooms_per_context)



txt = open(filename)
print("Here's your file %r:" % filename)
x = Complex()
x.readfile(txt)
print(x.data)
print('min per slice: ', x.min)
print('max per slice: ', x.max)
print('mushroms: ', x.mushrooms)
print('tomatoes: ', x.tomatoes)
x.calculateslices()
