from sys import argv
import numpy as np
from numpy.lib.stride_tricks import as_strided
import math

script, filename = argv


def factorization(k):
    s = 2
    fs = []
    for j in range(s, int(k ** (1 / 2)) + 1):
        while (k % j == 0):
            fs.append(j)
            k = k // j
    if (k != 1):
        fs.append(k)
    # Para calcular matrices rectangulares
    if len(fs) > 2:
        fy = []
        for x in range(len(fs)):
            if fs[x] in fy:
                fy[x - 1] *= fs[x]
            else:
                fy.append(fs[x])
        fs = fy
    return fs


class Complex:
    def __init__(self):
        self.search = False
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
            self.data_points = [[0 for x in range(self.columns)] for y in range(self.rows)]
            self.dataWrong = [[0 for x in range(self.columns)] for y in range(self.rows)]
            for row in range(self.rows):
                self.data.append(tuple(lines[row]))

            for row in range(self.rows):
                ntomatoes = self.data[row].count("T")
                self.tomatoes += ntomatoes
                self.mushrooms += self.columns - ntomatoes

    def calculateslices(self):
        max_slices = math.ceil((self.rows * self.columns) / self.max)
        print('Minimo numero de trozos: ', max_slices)
        if self.tomatoes < self.mushrooms:
            self.search = True
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

        if self.search:
            for column in range(self.columns):
                for row in range(self.rows):
                    if self.data[row][column] == 'T':
                        self.data_points[row][column] = 1
        else:
            for column in range(self.columns):
                for row in range(self.rows):
                    if self.data[row][column] == 'M':
                        self.data_points[row][column] = 1

    def find_valid_position(self):
        if pow(-1, self.max) == 1:
            print("PAR")
            idx = np.argwhere(np.matrix(self.data_points) == 1)
            for row in range(self.rows):
                for column in range(self.columns):
                    # print("Neighbors for position [", row, "][", column, "]  ==  ", self.neighbors(row, column))
                    pass

            print()
            print("Ubicación del ingrediente con menos probabilidades de aparecer: ")
            print(idx)
        else:
            print("IMPAR")

    def neighbors(self, fil, col):
        list_neighbors = []
        for i in range(fil - 1, fil + 2, 1):
            for j in range(col - 1, col + 2, 1):
                if i == fil and j == col:
                    continue
                if i == len(self.data_points) or j == len(self.data_points[i]):
                    break
                if i >= 0 and j >= 0:
                    list_neighbors.append(self.data_points[i][j])
        return list_neighbors

    def calculatewrongmatrix(self):
        # Lista en la que guardamos todas las posibles matrices
        list_posibilities = []
        listFactors = []
        # Nueva forma de submatriz colocada para revisar
        submatrix = np.reshape(x.data_points, (self.rows, self.columns))
        # Calculamos el factorial del máximo para ver los posibles tamaños de submatrices
        maximum = self.max
        while (maximum > 3):
            if (maximum % 2) == 1:
                maximum -= 1
            factors = factorization(maximum)
            listFactors.append(factors)
            maximum -= 1
        print("Factorizacion: ", listFactors)
        for row in range(self.rows):
            for column in range(self.columns):
                list_posibilities = []
                for rigth in range(self.columns - column):
                    subMatrixSplit = submatrix[row:row + 1, column:int(column + rigth + 1)]
                    # print(submatrix_split)
                    # print("submatrix[", row, ", ", row + 1, "][", column, ", ", int(column + rigth + 1), "]")
                    num_elem = subMatrixSplit.size
                    if (2 * self.min) <= num_elem <= self.max:
                        list_posibilities.append(subMatrixSplit)
                for scroll_left in range(column):
                    for rigth in range(self.columns - column):
                        subMatrixSplit = submatrix[row:row + 1, column - (scroll_left + 1):int(column + rigth + 1)]
                        num_elem = subMatrixSplit.size
                        if (2 * self.min) <= num_elem <= self.max:
                            list_posibilities.append(subMatrixSplit)
                            # print(subMatrixSplit)
                            # print("submatrix[", row, ", ", row + 1, "][", column - (scroll_left + 1), ", ", int(column + rigth + 1), "]")
                for down in range(self.rows - row):
                    subMatrixSplit = submatrix[row:int(row + down + 1), column:column + 1]
                    num_elem = subMatrixSplit.size
                    if (2 * self.min) <= num_elem <= self.max:
                        list_posibilities.append(subMatrixSplit)
                for scroll_up in range(row):
                    for down in range(self.rows - row):
                        subMatrixSplit = submatrix[row - (scroll_up + 1):int(row + down + 1), column:column + 1]
                        num_elem = subMatrixSplit.size
                        if (2 * self.min) <= num_elem <= self.max:
                            list_posibilities.append(subMatrixSplit)
                            # print(subMatrixSplit)
                            # print("submatrix[", row - (scroll_up + 1), ", ", int(row + down + 1), "][", column, ", ", column + 1, "]")
                if self.max > 3:
                    for numOperations in range(len(listFactors)):
                        if listFactors[numOperations][1] <= self.columns - column and listFactors[numOperations][
                            0] <= self.rows - row:
                            horizontal = \
                                self.get_im2col_indices(submatrix, self.rows, self.columns,
                                                        listFactors[numOperations][0],
                                                        listFactors[numOperations][1])[row, column]
                            if (not (
                                            0 < np.sum(horizontal) < listFactors[numOperations][0] *
                                        listFactors[numOperations][
                                            1])):
                                # print(horizontal)
                                for rowAux in range(listFactors[numOperations][0]):
                                    for columnAux in range(listFactors[numOperations][1]):
                                        self.dataWrong[rowAux + row][columnAux + column] += 1
                        if listFactors[numOperations][0] != listFactors[numOperations][1]:
                            if listFactors[numOperations][0] <= self.columns - column and listFactors[numOperations][
                                1] <= self.rows - row:
                                vertical = self.get_im2col_indices(submatrix, self.rows, self.columns,
                                                                   listFactors[numOperations][1],
                                                                   listFactors[numOperations][0])[row, column]
                                if (not (0 < np.sum(vertical) < listFactors[numOperations][1] *
                                    listFactors[numOperations][0])):
                                    # print(vertical)
                                    for rowAux in range(listFactors[numOperations][1]):
                                        for columnAux in range(listFactors[numOperations][0]):
                                            self.dataWrong[rowAux + row][columnAux + column] += 1
                # print("finisehd matrix of point  [", row, "][", column, "]  ==> ", list_posibilities)
                result = 0
                for num in range(len(list_posibilities)):
                    # print("Sum: ", np.sum(list_posibilities[num]), " len: ", list_posibilities[num].size)
                    if not (0 < np.sum(list_posibilities[num]) < list_posibilities[num].size):
                        result += 1
                self.dataWrong[row][column] += result
                # print("Matrix[", row, ",", column, "] => ", self.dataWrong[row][column])
        pass

    def get_im2col_indices(self, x, H, W, HH, WW, stride=1):
        # Perform an im2col operation on x
        OH = (H - HH) / stride + 1  # output height
        OW = (W - WW) / stride + 1  # output width
        shape = (int(OH), int(OW), HH, WW)  # define the shape of output matrix
        strides = (stride * W, stride, 1 * W, 1)  # define the strides(offset) according to shape
        strides = x.itemsize * np.array(strides)  # turn unit of the strides into byte
        # print("strides:", shape)
        x_stride = as_strided(x, shape=shape, strides=strides)
        x_cols = np.ascontiguousarray(x_stride)  # put our convenience matrix together im memory

        return x_cols

    def calculateSlides(self):
        print(np.reshape(self.dataWrong, (self.rows, self.columns)))
        sumPerRow = np.sum(self.dataWrong, axis=1)
        sumPerColumn = np.sum(self.dataWrong, axis=0)
        max = -1
        while (max != 0):
            row = -1
            column = -1
            for x in range(sumPerRow.size):
                if max < sumPerRow[x]:
                    max = sumPerRow[x]
                    row = x
            for y in range(sumPerColumn.size):
                if max < sumPerColumn[y]:
                    max = sumPerColumn[y]
                    column = y
            print(max)
            print(row, column)
            for row in range(self.rows):
                for column in range(self.columns):
                    pass
            max = 0
        pass


txt = open(filename)
# print("Here's your file %r:" % filename)
x = Complex()
x.readfile(txt)
x.calculateslices()
# x.find_valid_position()
print()
print(np.matrix(x.data_points))
x.calculatewrongmatrix()
x.calculateSlides()
