from enum import Enum
from sys import exit
from collections import defaultdict
import os
import sys
import time
import bisect, math
import itertools
from prettytable import PrettyTable

# Get a dict of {field string, number} from file of fields
# Need to have fields as first row of Data file instead
def loadFieldsDict(file):
	d = {}
	if file:
		f = open(file).read().strip().split("\n")
		d = {y.lstrip().strip():x for (x,y) in enumerate(f)}
	return d

# Get a list of fields from the fields file
def loadFieldsList(file):
	l = []
	if file:
		l = [x.lstrip().strip() for x in open(file).read().strip().split("\n")]
	return l

fieldsFilename = "FieldsCurated.csv"

f = loadFieldsDict(fieldsFilename) # dict used for an enum
NUMFIELDS = len(f)

def intersect_sorted(a1, a2):
  """Yields the intersection of sorted lists a1 and a2, without deduplication.

  Execution time is O(min(lo + hi, lo * log(hi))), where lo == min(len(a1),
  len(a2)) and hi == max(len(a1), len(a2)). It can be faster depending on
  the data.

  From: http://ptspts.blogspot.ie/2015/11/how-to-compute-intersection-of-two.html
  """
  if a2 == None and a1 != None:
	for x in a1:
		yield x
  elif a1 == None and a2 != None:
	for x in a2:
		yield x
  else: 
	  s1, s2 = len(a1), len(a2)
	  i1 = i2 = 0
	  if s1 and s1 + s2 > min(s1, s2) * math.log(max(s1, s2)) * 1.4426950408889634:
	    bi = bisect.bisect_left
	    while i1 < s1 and i2 < s2:
	      v1, v2 = a1[i1], a2[i2]
	      if v1 == v2:
		yield v1
		i1 += 1
		i2 += 1
	      elif v1 < v2:
		i1 = bi(a1, v2, i1)
	      else:
		i2 = bi(a2, v1, i2)
	  else:  # The linear solution is faster.
	    while i1 < s1 and i2 < s2:
	      v1, v2 = a1[i1], a2[i2]
	      if v1 == v2:
		yield v1
		i1 += 1
		i2 += 1
	      elif v1 < v2:
		i1 += 1
	      else:
		i2 += 1 #a 2d list with each row being a row from the DB

table = PrettyTable()
def createTable():
        TableRows = [
            "Jabref del",
            "Jabref clicked",
            "Jabref ctr",
      
            "Jabref CORE del",
            "Jabref CORE clicked",
            "Jabref CORE ctr",

            "Mr. DLib Jabref del",
            "Mr. DLib Jabref clicked",
            "Mr. DLib Jabref ctr",
            
            "Mr. DLib Jabref CBF Terms del",
            "Mr. DLib Jabref CBF Terms clicked",
            "Mr. DLib Jabref CBF Terms ctr",

            "Mr. DLib Sowiport del",
            "Mr. DLib Sowiport clicked",
            "Mr. DLib Sowiport ctr",
            ]
                
        print TableRows
        table.add_column("",TableRows)

def printTable(Months=None,
               Sowiport=None,
               Jabref=None,
               MrDlib=None,
               Core=None,
               CBF=None,
               Terms=None,
               recIDtoClick=None,
               requestDateTime=None):

        output = []

        # Sorting each list of IDs for fast intersection
        for x,y in enumerate(Months):
                Months[x] = sorted(y)
        CBF = sorted(CBF)	
        algos = {"CBF": CBF}

        cbfFeat = {"Terms": sorted(Terms)}
        applications = {
                        "Client name: Sowiport": sorted(Sowiport),
                        "Client name: Jabref": sorted(Jabref),
                        "Recsys Operator: Mr Dlib": sorted(MrDlib),
                        "Recsys Operator: Core": sorted(Core)
                       }
        cbfFeatCount = 0
        cbfFeatIter = iter(sorted(cbfFeat.iteritems()))
               
        listAlgos = sorted(algos.iterkeys())
        algoIter = iter(sorted(algos.iterkeys()))
        algo = algoIter.next()

        # Core vs Mr DLib
        clicks = reduce(lambda x,y: x+y, [recIDtoClick[z] for z in Jabref], 0)
        try:
            output.extend([len(Jabref), clicks, float(clicks)/len(Jabref)])
        except:
            output.extend([0,0,0])


        # Core vs Mr DLib
        jabrefcore = list(intersect_sorted(applications["Client name: Jabref"], applications["Recsys Operator: Core"]))
        clicks = reduce(lambda x,y: x+y, [recIDtoClick[z] for z in jabrefcore], 0)
        try:
            output.extend([len(jabrefcore), clicks, float(clicks)/len(jabrefcore)])
        except:
            output.extend([0,0,0])
        
        jabrefmdl = list(intersect_sorted(applications["Client name: Jabref"], applications["Recsys Operator: Mr Dlib"]))
        clicks = reduce(lambda x,y: x+y, [recIDtoClick[z] for z in jabrefmdl], 0)
        try:
            output.extend([len(jabrefmdl), clicks, float(clicks)/len(jabrefmdl)])
        except:
            output.extend([0,0,0])

        jabrefmdlterms = list(intersect_sorted(jabrefmdl, cbfFeat["Terms"]))
        clicks = reduce(lambda x,y: x+y, [recIDtoClick[z] for z in jabrefmdlterms], 0)
        try:
            output.extend([len(jabrefmdlterms), clicks, float(clicks)/len(jabrefmdlterms)])
        except:
            output.extend([0,0,0])

        sowiportmdl = list(intersect_sorted(applications["Client name: Sowiport"], applications["Recsys Operator: Mr Dlib"]))
        clicks = reduce(lambda x,y: x+y, [recIDtoClick[z] for z in sowiportmdl], 0)
        try:
            output.extend([len(sowiportmdl), clicks, float(clicks)/len(sowiportmdl)])
        except:
            output.extend([0,0,0])

        table.add_column(str(requestDateTime.tm_mon-1) + "-" + str(requestDateTime.tm_year), output)
        output = []

        print table


# Gets the ID of each row according to some criteria (e.g. this row was delivered on a Monday, this row
# was delivered to Jabref) and adds them to a set. Then intersects these sets to get the CTR of any combination of criteria.
def loadData(file):
	
        createTable()
        jabcount = 0
	startTime = time.time()

	data = []
	errors = 0
	cbf = []
	terms = []
	termsSub = defaultdict(list)

	Months = [[] for x in range(12)]
        monthDict = defaultdict(list)
	
	Sowiport = []
	Jabref = []
	Core = []	
	MrDlib = []

        currentMonth = -1
	recIDtoClick = {}
	setIDtoClick = defaultdict(set)

        output = []
        # Defining the rows for the table, to be printed to the terminal

        if not os.path.isfile(file):
            print "%s does not exist"
            sys.exit()
       	d = open(file)
	lineCount = 0

        # CORE recommendations weren't made until ~50 millionth record
        skipToLine = 65000000
        for x in range(skipToLine):
            d.next()

        prevSetId = 0
        setCount = 0

        # for each row in the dataset
	for line in d:
            lineCount += 1
            l = line.lstrip().strip().split("\t")

            if len(l) != NUMFIELDS:
                errors += 1
                continue

            reqRec = time.strptime(l[f["request_received"]], "%Y-%m-%d %H:%M:%S")

            # If the row we're on is in the next month, print data from the previous month
            if reqRec.tm_mon-1 != currentMonth:
                    if currentMonth == -1:
                        currentMonth = reqRec.tm_mon-1
                        continue

                    # Add the current month's data to the table and print
                    printTable(Months=Months,
                            Sowiport=Sowiport,
                            Jabref=Jabref,
                            MrDlib=MrDlib,
                            Core=Core,
                            CBF=cbf,
                            Terms=terms,
                            recIDtoClick=recIDtoClick,
                            requestDateTime=reqRec)

                    currentMonth = reqRec.tm_mon-1

                    data = []
                    errors = 0
                    cbf = []
                    terms = []
                    termsSub = defaultdict(list)
                    random = []
                    Months = [[] for x in range(12)]
                    monthDict = defaultdict(list)
                    Sowiport = []
                    Jabref = []
                    Core = []	
                    MrDlib = []
 
            # Calculating Data for the current month
            try:
                recId = int(l[f["recommendation_id"]])
            except:
                print l

            try:
                setId = int(l[f["recommendation_set_id"]])
            except:
                print l

            sourceDocId = 0
            if l[f["source_document_id"]] != "null":
                sourceDocId = int(l[f["source_document_id"]])
            
            recDocId = 0
            if l[f["recommended_document_id"]] != "null":
                recDocId = int(l[f["recommended_document_id"]])

            if l[f["client_name"]] == "sowiport":
                    Sowiport.append(recId)	
            elif l[f["client_name"]] == "jabref":
                    jabcount += 1
                    Jabref.append(recId)	
            
            # Total stats
            if l[f["recsys_operator"]] == "mdl":
                    MrDlib.append(recId)
            elif l[f["recsys_operator"]] == "core":
                    Core.append(recId)


            if l[f["clicked"]] != "null":
                    recIDtoClick[recId] = 1
            else:
                    recIDtoClick[recId] = 0

            Months[reqRec.tm_mon-1].append(recId)
            monthDict[(reqRec.tm_mon-1, reqRec.tm_year)].append(recId)
                    
            if l[f["algorithm_class"]] == "cbf":
                    cbf.append(recId)		
                    if l[f["cbf-feature_type"]] == "terms":
                            terms.append(recId)
                            termsSub["Terms-" + l[f["cbf-document_field"]]].append(recId)
        return


if __name__ == "__main__":
    
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print "To run:\npython Analyser.py {path to RARDII Dataset}\n\n"
        sys.exit()

    loadData(sys.argv[1])



