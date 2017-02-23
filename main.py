import numpy
import sys
import getopt

class Output:
    name = ''
    values = None

class Input:
    name = ''
    values = None

def compute(iInput):
    res = Output()
    # compute logique
    res.name = iInput.name+' output'
    return res

def parseInput(iInputFilePath):
    with open(iInputFilePath) as f:
        content = f.readlines()
    res = Input()
    res.name = 'toto'
    res.values = []
    res.values.append(1)
    return res

def formatOutput(iOutput, iOutputFilePath):
    f = open(iOutputFilePath, 'w')
    f.write(iOutput.name+'\n')
    f.close()

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   input = parseInput(inputfile)
   output = compute(input)
   formatOutput(output, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
