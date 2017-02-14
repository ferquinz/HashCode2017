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
            array = lines[0].split(' ')
            lines.pop(0)
            self.rows = int(array[0])
            self.columns = int(array[1])
            self.min = int(array[2])
            self.max = int(array[3])
            for row in range(self.rows):
                self.data.append(tuple(lines[row]))
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.data[row][column] == 'T':
                        self.tomatoes += 1
                    else:
                        self.mushrooms += 1

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
            print('\nCare mushrooms, per slice: ', mushrooms_per_context)

    def __del__(self):
        print('\n\n\nDestructor Deleting objects')


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
