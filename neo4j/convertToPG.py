"""
Converter from an RDF serialized text to a neo4j property graph.
(python3 supports)

Parameters:

-i (--input): pass the input of an RDF text
"""
import argparse
import os
import sys
from neo4j import GraphDatabase

TURTLE = 0
NT     = 1
RDFXML = 2

# TODO n3 is not the target.
RDFString = [ "Turtle", "N-Triples", "RDF/XML" ] 

uri = "neo4j://localhost:7687"
usrID = "neo4j"
usrPW = "1" # NOTE: You should use your own account.
            # Default account of the neo4j would be
            # ID: neo4j and PW: neo4j.

"""
Remove all the existing data whenver the script starts.
Note that it would be better to remove data taking too much memory manually. 
DB is located on /var/lib/neo4j/data/databases/*.
"""
def delete_existing_db(session):
  print("Delete existing data..")
  session.run("MATCH (resource) DETACH DELETE resource;")
  print("Deletion done.")

def init_env(session):
  delete_existing_db(session)
  session.run("CALL n10s.graphconfig.init({handleRDFTypes: 'LABELS_AND_NODES', handleMultival: 'ARRAY'});")

  #session.run("DROP CONSTRAINT n10s_unique_uri")
  uniqConstExt = False
  for constraint in session.run("call db.constraints()"):
    if (constraint[0] == "n10s_unique_uri"):
      uniqConstExt = True

  if uniqConstExt:
    print("Unique URI constraint is already enabled.")
  else:
    print("Enable an unique URI constraint.")
    session.run("CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE")

"""
Import a specified RDF input to the neo4j PG format.
TODO should allow users to specify configurations of the construction.
     For example, representing multi-valued properties as an array.
TODO get and print the returned exception statements from the CALL.
     The current action is to happen nothing. (Should check the browser inter
     -face in this case.)
"""
def import_RDF_to_PG(session, input, rdfFormatIdx):
  print("Import the input RDF.. :"+input)
  #session.run("CALL n10s.rdf.import.fetch('file:///"+input+"', '"+RDFString[rdfFormatIdx]+"')")
  importCypher = "CALL n10s.rdf.import.fetch('file:///"+input+"', '"+RDFString[rdfFormatIdx]+"') \
                  YIELD terminationStatus, triplesLoaded, triplesParsed, extraInfo \
                  RETURN extraInfo"
  with session.begin_transaction() as tx:
    res = tx.run(importCypher)
    # printout the result of the query.
    for r in res:
      print(r["extraInfo"]);
      continue;
    print("Importing done.")

def import_DIR_to_PG(session, inputDir, rdfFormatIdx):
  session.run("CALL n10s.graphconfig.init({handleRDFTypes: 'LABELS_AND_NODES', handleMultival: 'ARRAY'});")
  uniqConstExt = False
  for constraint in session.run("call db.constraints()"):
    if (constraint[0] == "n10s_unique_uri"):
      uniqConstExt = True

  if uniqConstExt:
    print("Unique URI constraint is already enabled.")
  else:
    print("Enable an unique URI constraint.")
    session.run("CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE")

  for fname in os.listdir(inputDir): 
    print(">>>>>>>"+inputDir+"/"+fname);
    #session.run("CALL n10s.rdf.import.fetch('file:///"+input+"', '"+RDFString[rdfFormatIdx]+"')")
    importCypher = "CALL n10s.rdf.import.fetch('file:///"+inputDir+"/"+fname+"', '"+RDFString[rdfFormatIdx]+"') "
    importCypher +="YIELD terminationStatus, triplesLoaded, triplesParsed, extraInfo "
    importCypher +="RETURN extraInfo"
    print(importCypher)
    with session.begin_transaction() as tx:
      res = tx.run(importCypher)
      # printout the result of the query.
      for r in res:
        print("\t"+r["extraInfo"]);
        continue;
  print("Importing done.")

#def dumpNeo4j(output):
#  print("Dump the DB..")
#  os.system("neo4j-admin dump --database=neo4j --to="+output)

def exportToCypher(session, output):
	session.run("CALL apoc.export.cypher.all('"+output+".cypher')");

def exportToGraphML(session, output, printType):
  if (printType == 1):
      session.run("CALL apoc.export.graphml.all('"+output+".graphml', {useTypes:true, readLabels:true})")
  else:
      session.run("CALL apoc.export.graphml.all('"+output+".graphml', {readLabels:true})")
	
"""
Get the number of nodes and the relationships.
TODO merge the two queries! (e.g. UNION or return multi values)
"""
def get_num_nodes_edges(session):
  nNodes = session.run("MATCH (n) RETURN count(n)")
  print(str(nNodes.single()[0]) + " nodes exist.")
  nEdges = session.run("MATCH (n)-[r]->() RETURN count(r)")
  print(str(nEdges.single()[0]) + " edge exist.")

def main():
  optParser = argparse.ArgumentParser()
  optParser.add_argument('-i', '--input', type=str,
                         help='Specify an input file name having'
                               'RDF formmated texts.',
                         dest='inputRDFFile', required=False)

  optParser.add_argument('-d', '--directory', type=str,
                         help='Specify an input directory having'
                               'RDF formmated texts.',
                         dest='inputDirectory', required=False)

  optParser.add_argument('-s', '--source', type=int,
                         help='Specify an input RDF format to be converted:'
                              '(N3: 0, Turtle: 1, NTriple: 2, RDF/XML: 3, '
                              'default=RDF/XML)')

  optParser.add_argument('-t', '--type', type=int,
                         help="If you want to print out type information,"
                               "please specify '-t' or '--type' (default: 0)",
                         dest='printType', default=1)

  if not (optParser.parse_args().inputRDFFile or
          optParser.parse_args().inputDirectory):
    print("Either input rdf file or input rdf directory is required\n")
    exit()

  args = optParser.parse_args()
  inputRDFFile = args.inputRDFFile
  inputDirectory = args.inputDirectory
  #output = args.output
  printType = args.printType
  srcRDFFormat  = RDFXML

  # Convert relative to absolute path.
  currPath = os.path.abspath(os.path.dirname(__file__))

  if inputRDFFile:
    inputRDFFile = os.path.join(currPath, inputRDFFile)
  else:
    inputRDFFile = "Not specified"
    print("Input RDF file is not specified")

  if inputDirectory:
    inputDirectory = os.path.join(currPath, inputDirectory)
  else:
    inputDirectory = "Not specified"
    print("Input directory is not specified")
  #output = os.path.join(currPath, output)

  # If the I/O RDF formats are passed by an user.
  if args.source is not None:
    srcRDFFormat = args.source

  print("\n** Passed arguments ***************************\n ")
  print("\tInput file name: "+inputRDFFile)
  print("\tInput Dir: "+inputDirectory)
  #print("\tOutput file name: "+output)
  print("\tInput RDF format: "+RDFString[srcRDFFormat])
  if printType == 1:
    print("\tPrint type to GraphML")
  print("\n*********************************************** ")

  fileList = []
  if inputDirectory != "Not specified":
    for rdfFile in os.listdir(inputDirectory):
      rdfFname = os.fsdecode(rdfFile)
      fileList.append(inputDirectory+"/"+rdfFile)
  if inputRDFFile != "Not specified":
    fileList.append(inputRDFFile)

  driver = GraphDatabase.driver(uri, auth=(usrID, usrPW))
  convertLog = {}
  importSuccess = True
  with driver.session() as session:
    init_env(session)
    for rdfPath in fileList:
      print(rdfPath)
      rdfFile = os.path.basename(rdfPath)
      extraInfo = import_RDF_to_PG(session, rdfPath, srcRDFFormat)
      get_num_nodes_edges(session)
      if extraInfo != "":
        importSuccess = False
      convertLog[rdfFile] = extraInfo
  #exportToCypher(session, outputCypher)

  if importSuccess == True:
    print("Importing succeeded.")
    print("Exporting started.")
    exportToGraphML(session, "graphML/"+rdfFile+".graphML", printType)
  else:
    for fname in fileList:
      fname = os.path.basename(fname)
      print(fname+":"+str(convertLog[fname]))

if __name__ == "__main__":
  main()
