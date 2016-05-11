from config_reader import ConfigReader
from data_manipulation import readData
import numpy as np
import sys

assert(len(sys.argv) >= 4 and len(sys.argv) <= 6)

if len(sys.argv) == 4:
    _, docType, measure, minNumCitationsString = sys.argv
    minAgeString = "0"
    minBase = None
elif len(sys.argv) == 5:
    _, docType, measure, minNumCitationsString, minAgeString = sys.argv
    minBase = None
else:
    _, docType, measure, minNumCitationsString, minAgeString, minBaseString = sys.argv
    minBase = int(minBaseString)

minNumCitations = int(minNumCitationsString)
minAge = int(minAgeString)

cr = ConfigReader("config.ini", docType, measure, minNumCitations, minAge, minBase)

X = readData(cr.featuresPath)

if minBase != None:
    allInds = np.where(
        (X[[cr.citationFeature]].values[:, 0] >= cr.minNumCitations) & (X[[cr.ageFeature]].values[:, 0] >= cr.minAge) & \
        (X[[cr.baseFeature]].values[:, 0] >= cr.minBase)
    )[0]
else:
    allInds = np.where(
        (X[[cr.citationFeature]].values[:, 0] >= cr.minNumCitations) & (X[[cr.ageFeature]].values[:, 0] >= cr.minAge)
    )[0]
sampleSize = len(allInds)
testSize = min(int(.2 * sampleSize), 10000)
validSize = min(int(.1 * sampleSize), 10000)
trainSize =  sampleSize - testSize - validSize

np.random.seed(12)
np.random.shuffle(allInds)
trainInds = sorted(allInds[0:trainSize])
validInds = sorted(allInds[trainSize:(trainSize + validSize)])
testInds = sorted(allInds[(trainSize + validSize):len(allInds)])

np.array(trainInds).tofile(cr.trainIndsPath, sep = "\t", format = '%d')
np.array(validInds).tofile(cr.validIndsPath, sep = "\t", format = '%d')
np.array(testInds).tofile(cr.testIndsPath, sep = "\t", format = '%d')