"""
Converter from an RDF serialized text to a visualized .png graph.
(python3 supports)

Parameters:

-i (--input): pass the input of an RDF text
-o (--output): pass the output of a generated visualized RDF graph
-s (--source): pass an input RDF format
               (N3: 0, Turtle: 1, NTriple: 2, RDF/XML: 3, default=RDF/XML)
-d (--destination): pass a target RDF format converted from the source
               (N3: 0, Turtle: 1, NTriple: 2, RDF/XML: 3, default=RDF/XML)
"""
import io
import sys
import os
import rdflib
import argparse
#from io import BytesIO as StringIO # for Python 2.4
import pydotplus
from IPython.display import display, Image
from rdflib.tools.rdf2dot import rdf2dot

# rdflib supports N3, XML, NTriples, Turtle, and Trix.

N3     = 0
TURTLE = 1
NT     = 2
RDFXML = 3

RDFString = [ "n3", "turtle", "nt", "application/rdf+xml" ] 
outputDir = os.getcwd()

"""
Get a RDF/XML formatted RDF graph, and
convert it to a visualized graph.
Target image extension is '.png'
"""
def visualize(g, ofname):
  stream = io.StringIO()
  rdf2dot(g, stream, opts = {display})
  dg = pydotplus.graph_from_dot_data(stream.getvalue())
  png = dg.create_png()
  img = Image(data=png) # generate .png object.
  open(outputDir+'/'+ofname+'.png', 'wb').write(img.data)

#------------------------------- Main Starts -----------------------------------
def main():
  optParser = argparse.ArgumentParser()
  optParser.add_argument('-i', '--input', type=str,
                         help='Specify an input file name having'
                               'RDF formmated texts.',
                         dest='inputRDFFile', required=True)
  optParser.add_argument('-o', '--output', type=str,
                         help='Specify an output file name for'
                               'the visualized RDF graph.',
                         dest='outputImgFname', required=True)
  optParser.add_argument('-s', '--source', type=int,
                         help='Specify an input RDF format to be converted:'
                              '(N3: 0, Turtle: 1, NTriple: 2, RDF/XML: 3, '
                              'default=RDF/XML)')
  optParser.add_argument('-d', '--destination', type=int,
                         help='Specify an output RDF format to be converted:'
                              '(N3: 0, Turtle: 1, NTriple: 2, RDF/XML: 3, '
                              'default=RDF/XML)\n'
                              'Note that only RDF/XML format can produce a '
                              'visualized RDF graph.')
  args = optParser.parse_args()

  inputRDFFile   = args.inputRDFFile
  outputImgFname = args.outputImgFname

  srcRDFFormat  = RDFXML
  destRDFFormat = RDFXML

  # If the I/O RDF formats are passed by an user.
  if args.source is not None:
    srcRDFFormat = args.source
  if args.destination is not None:
    destRDFFormat = args.destination

  print("\n** Passed arguments *************************** ")
  print()
  print("\tInput file name: "+inputRDFFile)
  print("\tOutput file name: "+outputImgFname)
  print("\tInput RDF format: "+RDFString[srcRDFFormat])
  print("\tOutput RDF format: "+RDFString[destRDFFormat])
  print()
  print("*********************************************** ")
  print()


  # create a Graph.
  g = rdflib.Graph()

  # open a file.
  f = open(inputRDFFile)

  # parse in an RDF file hosted on the Internet
  # result = g.parse("http://www.w3.org/People/Berners-Lee/card")

  # consider the file as the N3 format and parse it.
  result = g.parse(file=f, format=RDFString[srcRDFFormat])

  for subj, pred, obj in g:
    if (subj, pred, obj) not in g:
      raise Exception("It better be!")

  print ("** Graph has {} statements.".format(len(g)))

  destRDFFormatStr = RDFString[destRDFFormat]
  result = g.serialize(format=destRDFFormatStr).decode("utf-8")

  print("** Converted "+RDFString[srcRDFFormat]+" to "+destRDFFormatStr)
  print(result)
  print("")

  if destRDFFormat == RDFXML:
    visualize(g, outputImgFname)
    print("The visualized graph is successfully generated:"+
          outputImgFname+".png")
  else:
    print("This RDF output format does not generate a visualized graph.")
#------------------------------- Main Ends -------------------------------------

if __name__ == "__main__":
  main()
