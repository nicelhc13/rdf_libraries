import rdflib
import sys

# rdflib supports N3, XML, NTriples, Turtle, and Trix.

N3     = 0
TURTLE = 1
NT     = 2
RDFXML = 3

RDFString = [ "n3", "turtle", "nt", "application/rdf+xml" ] 

inputFormat  = RDFXML
targetFormat = TURTLE

# create a Graph.
g = rdflib.Graph()

# open a file.
f = open(sys.argv[1])

# parse in an RDF file hosted on the Internet
# result = g.parse("http://www.w3.org/People/Berners-Lee/card")

# consider the file as the N3 format and parse it.
result = g.parse(file=f, format=RDFString[inputFormat])

for subj, pred, obj in g:
  if (subj, pred, obj) not in g:
    raise Exception("It better be!")

print ("graph has {} statements.".format(len(g)))


if (targetFormat == TURTLE): 
  print (g.serialize(format="turtle").decode("utf-8"))
elif (targetFormat == N3):
  print (g.serialize(format="n3").decode("utf-8"))
elif (targetFormat == NT):
  print (g.serialize(format="nt").decode("utf-8"))
elif (targetFormat == RDFXML):
  print (g.serialize(format="application/rdf+xml").decode("utf-8"))
