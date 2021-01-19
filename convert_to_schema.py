with open("classes.txt", "r") as f:
    lines = f.readlines()

def seperate_dashes_and_write(lines, prefix="uner:", rdf=" rdf:type"):
    unique_classes = []
    relations = []
    file = open("schema.txt", "w")
    for line in lines:
        classes = line.split("-")
        classes[-1] = classes[-1].strip() # deleting "\n" from last class
        print(classes)
        for c in classes:
            if c not in unique_classes:
                unique_classes.append(c)
                file.write(prefix+c+rdf+" owl:Class .\n")
        if len(classes) > 1:
            previous = ''
            for c in classes[::-1]:
                if previous == '':
                    previous = c
                    continue
                else:
                    rel = prefix + previous + " rdfs:subClassOf " + "owl:"+c + "\n"
                    previous = c
                    if rel not in relations:
                        relations.append(rel)
                        file.write(rel)
files = ["output/UNER_OEKG_entities.tsv", "output/UNER_OEKG_entities_hr.tsv"]
def fix_tsv_naming():
    return

seperate_dashes_and_write(lines)