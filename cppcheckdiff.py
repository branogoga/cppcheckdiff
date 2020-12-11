import argparse
import copy
import xml.etree.ElementTree as ElementTree

parser = argparse.ArgumentParser("Difference between two CppCheck XML output files. Writes errors, that are present in observerFilename, but not in expectedFilename.")
parser.add_argument('observed', help="Observed CppCheck .xml result file.")
parser.add_argument('expected', help="Expected CppCheck .xml result file.")
parser.add_argument('output', help="Output filename.")
parser.add_argument('-v', '--verbose', help='Show verbose output', action='store_true')

args = parser.parse_args()

expectedFilename: str = args.expected
observedFilename: str = args.observed
outputFilename: str = args.output

expectedTree = ElementTree.parse(expectedFilename).getroot()
observedTree = ElementTree.parse(observedFilename)
observedTreeRoot = observedTree.getroot()

def getNumberOfErrors(errors):
    numberOfErrors = 0
    for error in errors:
        numberOfErrors = numberOfErrors + 1
    return numberOfErrors

def isSame(error1, error2):
    location1 = error1.find('location')
    location2 = error2.find('location')
    return (error1.attrib['id'] == error2.attrib['id'] and error1.attrib['verbose'] == error2.attrib['verbose'] and location1.attrib['file'] == location2.attrib['file'])

def findError(errors, searchedError):
    for error in errors:
        if isSame(error, searchedError):
            return error
    return None

if args.verbose:
    print("Expected errors: " + str(getNumberOfErrors(expectedTree.iter('error'))))
    print("Observed errors: " + str(getNumberOfErrors(observedTreeRoot.iter('error'))))
    print("New errors:")
    for error in observedTreeRoot.iter('error'):
        if findError(expectedTree.iter('error'), error) is None:
            print(error.find('location').attrib)
            print(error.attrib)
    print("Fixed errors:")
    for error in expectedTree.iter('error'):
        if findError(observedTreeRoot.iter('error'), error) is None:
            print(error.find('location').attrib)
            print(error.attrib)   

    print("Filter new errors:")

newErrorsTree = copy.deepcopy(observedTree)
newErrorsTreeRoot = newErrorsTree.getroot()
newErrors = newErrorsTreeRoot.find('errors')
numberOfRemoved = 0
numberOfPreserved = 0
totalProcessed = 0
toRemove = []
for error in newErrors.iter('error'):
    totalProcessed = totalProcessed + 1
    result = findError(expectedTree.iter('error'), error)
    if result is None:
        numberOfPreserved = numberOfPreserved + 1
    else:
        toRemove.append(error)
        numberOfRemoved = numberOfRemoved + 1

for error in toRemove:
    newErrors.remove(error)

if args.verbose:
    print("New errors:" + str(getNumberOfErrors(newErrorsTreeRoot.iter('error'))))
    print("Observed errors: " + str(getNumberOfErrors(observedTreeRoot.iter('error'))))
    for error in newErrorsTree.iter('error'):
        print(error.find('location').attrib)
        print(error.attrib)

    print("numberOfRemoved: " + str(numberOfRemoved))
    print("numberOfPreserved: " + str(numberOfPreserved))
    print("totalProcessed: " + str(totalProcessed))

newErrorsTree.write(outputFilename)

if args.verbose:
    print("Done!")