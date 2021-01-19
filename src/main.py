
import requests
import urllib.parse
import numpy as np
import math
from jsonmerge import merge
import pandas as pd
import json

from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
    PROF, PROV, RDF, RDFS, SH, SKOS, SOSA, SSN, TIME, \
    VOID, XMLNS, XSD

SO = Namespace('http://schema.org/')
OEKG_R = Namespace("http://oekg.l3s.uni-hannover.de/resource/")
OEKG_S = Namespace("http://oekg.l3s.uni-hannover.de/schema/")
SEM = Namespace('http://semanticweb.cs.vu.nl/2009/11/sem/')
UNER = Namespace("http://oekg.l3s.uni-hannover.de/uner/")
DBO = Namespace('http://dbpedia.org/ontology/')
url = "http://smldapi.l3s.uni-hannover.de/" 
graph = "uner"

files = ["output/UNER_OEKG_entities.tsv", "output/UNER_OEKG_entities_hr.tsv"]

def insert_schema(file):
    with open(file, "r") as f:
        lines = f.readlines()
    g = Graph()
    for line in lines:
        if len(line.split(" ")) == 4:
            s, p, o, _ = line.split(" ")
        else:
            s, p, o = line.split(" ")
        s = s[5:]
        o = o[4:].strip()
        # add triples of first news article
        if p[:4] == "rdfs":
            g.add((URIRef(UNER)+s, RDFS.subClassOf, URIRef(UNER)+o))
        else:
            g.add((URIRef(UNER)+s, RDF.type, OWL.Class))

    file = open("uner_schema.nt", "w")
    file.write(g.serialize(format='nt').decode("utf-8"))
    file.close()
    # Upload the file into to the OEKG,
    uploadFileToOEKG(graph, "uner_schema.nt")

def insert_triples(files):

    # reset graph
    #clear_graph(graph)
    g = Graph()
    for file in files:
        tsv_read = pd.read_csv(file, sep='\t')
        ids = tsv_read["id"]
        classes = tsv_read["uner-class"]
        classes, ids = list(classes), list(ids)
        for entity_id, entity_class in zip(ids, classes):
            entity_id = entity_id.strip()
            if entity_class == "Name-Person-Name":
                entity_class = "Name-Person-Name_Person"
            oekg_id = entity_id
            #print(oekg_id)
            entity_class = entity_class.split("-")[-1].strip()
            # add triples 
            g.add((URIRef(OEKG_R)+oekg_id, RDF.type, URIRef(UNER)+entity_class))

    # Write triples into a file 
    file = open("uner_triples.nt", "w")
    file.write(g.serialize(format='nt').decode("utf-8"))
    file.close()

    # Upload the file into to the OEKG, using the example graph
    uploadFileToOEKG(graph, "uner_triples.nt")

def correspondences(file):
    g = Graph()
    with open(file) as f:
        c=json.load(f)
    for db_class in c:
        uner_class = c[db_class]
        if  not uner_class:
            continue
        else:
            uner_class = uner_class.split("-")[-1].strip()
            if uner_class == db_class:
                g.add((URIRef(UNER)+uner_class, OWL.equivalentClass, URIRef(DBO)+db_class))
            else:
                g.add((URIRef(UNER)+uner_class, SKOS.narrower, URIRef(DBO)+db_class))

    file = open("correspondences.nt", "w")
    file.write(g.serialize(format='nt').decode("utf-8"))
    file.close()
    # Upload the file into to the OEKG,
    uploadFileToOEKG(graph, "correspondences.nt")



def uploadFileToOEKG(graph, file_name):
    print("uploadFileToOEKG: " + url + "upload/"+graph)
    files = {'upload_file': open(file_name, 'rb')}
    r = requests.post(url + "upload/"+graph, files=files)#, data=data)
    print(r.text)


def getOEKGIdByWikidataId(wikidata_id):
    # Get OEKG ID of an entity via its Wikidata ID
    return requests.get(url + "api/wikidataId/" + wikidata_id).json()


def getOEKGIdsByWikidataIds(*wikidata_ids):
    # Get OEKG IDs of a set of entity via its Wikidata ID
    ids = {}
    for ids_sublist in np.array_split(wikidata_ids, math.ceil(len(wikidata_ids) / 1)):
        res = requests.get(url + "api/wikidataIds/" + ";".join(ids_sublist)).json()
        ids = merge(ids, res)
    return ids


def getOEKGIdByWikipediaId(language, wikipedia_id):
    # Get OEKG ID of an entity via its Wikipedia ID
    return requests.get(url + "api/wikipediaId/" + language + "/" + wikipedia_id).json()


def getOEKGIdsByWikipediaIds(language, *wikipedia_ids):
    # Get OEKG IDs for a set of Wikidata IDs
    ids = {}
    for ids_sublist in np.array_split(wikipedia_ids, math.ceil(len(wikipedia_ids) / 1)):
        res = requests.get(url + "api/wikidataIds/" + ";".join(ids_sublist)).json()
        ids = merge(ids, res)
    return ids


def clear_graph(graph_to_be_cleared):
    # Remove all triples uploaded within the given graph.
    r = requests.get(url + "clear/"+graph_to_be_cleared)
    print(r.text)


def query_oekg(query):
    result1 = requests.get(url + "query/" + urllib.parse.quote_plus(query))
    print(result1)


if __name__ == '__main__':
    print("1")
    #clear_graph(graph)
    print("2")
    #insert_schema("schema.txt")
    print("3")
    #insert_triples(files)
    print("4")
    correspondences("dbpedia_uner_mapping_v1.json")

    #clear_graph(graph)
