"""
Converter from an RDF serialized text to a neo4j property graph.
(python3 supports)

Parameters:

-i (--input): pass the input of an RDF text
"""
import argparse
from neo4j import GraphDatabase

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

"""
Import a specified RDF input to the neo4j PG format.
TODO should allow users to specify configurations of the construction.
     For example, representing multi-valued properties as an array.
TODO get and print the returned exception statements from the CALL.
     The current action is to happen nothing. (Should check the browser inter
     -face in this case.)
"""
def import_RDF_to_PG(session, input):
  print("Import the input RDF.. :"+input)
  session.run("CALL n10s.graphconfig.init({handleRDFTypes: 'LABELS_AND_NODES'});")
#session.run("CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE")
  session.run("CALL n10s.rdf.import.fetch('file:///"+input+"', 'N-Triples')")
  print("Importing done.")

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
                         dest='inputRDFFile', required=True)

  args = optParser.parse_args()
  inputRDFFile = args.inputRDFFile

  driver = GraphDatabase.driver(uri, auth=("neo4j", "1"))
  with driver.session() as session:
    delete_existing_db(session)
    import_RDF_to_PG(session, inputRDFFile)
    get_num_nodes_edges(session)

if __name__ == "__main__":
  main()
