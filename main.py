import numpy as np
import csv
import operator

def main():
  data = loadCsvData('ancestry-train.txt')
  trainedMLE = trainMLEData(data)
  trainedMAP = trainMAPData(data)
  real = loadCsvData('ancestry-test.txt')
  print "\n","MLE Accuracy"
  testData(trainedMLE, real)
  print "\n","Laplace Accuracy"
  testData(trainedMAP, real)

#classifies test input and reports classification accuracy
def testData(trained, real):
  numOfInput = real[0][0]
  numOfVec = real[1][0]
  classz = 0
  classo = 0
  classzc = 0
  classoc = 0
  for r in range (2, 2 + numOfVec):
   probs = []
   for y in range (0, 2):
     proby = 1
     for xi in range (0, numOfInput):
       if real[r][xi] == 0:
        proby *= trained[xi][2*y]
       elif (real[r][xi] == 1):
        proby *= trained[xi][2*y+1]
     eproby = trained[len(trained)-1][y]
     proby *= eproby
     probs.append(proby)
   if real[r][numOfInput] == 0:
     classz += 1
     if probs[0] > probs [1] :
       classzc += 1
   if (real[r][numOfInput] == 1): 
     classo += 1
     if probs [1] > probs [0]:
       classoc += 1
  print "Class 0: correctly classified", classzc, "out of", classz, "tested"
  print "Class 1: correctly classified", classoc, "out of", classo, "tested"
  print "Overall: correctly classified", (classzc + classoc), "out of", (classz + classo), "tested"
  print "Accuracy =", (float(classzc + classoc)/(classz + classo))

#creates matrix of Laplace estimates
def trainMAPData(matrix):
  results = []
  countyz = 2
  countyo = 2
  numOfInput = matrix[0][0]
  numOfVec = matrix[1][0]
  for r in range (2, 2 + numOfVec):
    if (matrix[r][numOfInput] == 0):
       countyz += 1
    else:
       countyo += 1
  for x in range (numOfInput):
    row = []
    for y in range (0,2):
      countxz = 0
      countxo = 0
      for r in range (2, 2 + numOfVec):
        if matrix[r][x] == 0:
           if matrix[r][numOfInput] == y:
             countxz += 1
        if matrix[r][x] == 1:
          if matrix[r][numOfInput] == y:
            countxo += 1
      if (y == 0):
        countxz = float(countxz+1)/countyz
        countxo = float(countxo+1)/countyz
      else:
        countxz = float(countxz+1)/countyo
        countxo = float(countxo+1)/countyo
      row.append(countxz)
      row.append(countxo)
    results.append(row)
  row = []
  row.append(float(countyz-2)/numOfVec)
  row.append(float(countyo-2)/numOfVec)
  results.append(row)
  return results

#creates matrix of Maximum Likelihood Estimates
def trainMLEData(matrix):
  results = []
  countyz = 0
  countyo = 0
  numOfInput = matrix[0][0]
  numOfVec = matrix[1][0]
  for r in range (2, 2 + numOfVec):
    if (matrix[r][numOfInput] == 0):
       countyz += 1
    else:
       countyo += 1
  for x in range (numOfInput):
    row = []
    for y in range (0,2):
      countxz = 0
      countxo = 0
      for r in range (2, 2 + numOfVec):
        if matrix[r][x] == 0:
           if matrix[r][numOfInput] == y:
             countxz += 1
        if matrix[r][x] == 1:
          if matrix[r][numOfInput] == y:
            countxo += 1
      if (y == 0):
        countxz = float(countxz)/countyz
        countxo = float(countxo)/countyz
      else:
        countxz = float(countxz)/countyo
        countxo = float(countxo)/countyo
      row.append(countxz)
      row.append(countxo)
    results.append(row)
  row = []
  row.append(float(countyz)/numOfVec)
  row.append(float(countyo)/numOfVec)
  results.append(row)
  return results

#reads in file, creates matrix of data
def loadCsvData(fileName):
  orig = []
  with open(fileName) as f:
    reader = csv.reader(f)
    for row in reader:
      row = row[0].split()
      orig.append(row)
    numOfInput = orig[0][0]
    for i in range(2, 2+int(orig[1][0])):
      orig[i][int(numOfInput) - 1] = orig[i][int(numOfInput) - 1][0]
    matrix = []
    for row in orig:
      line = []
      for value in row:
        line.append(int(value))
      matrix.append(line)
  return matrix

def printData(matrix):
	for row in matrix:
		print row

# This if statement passes if this
# was the file that was executed
if __name__ == '__main__':
	main()
