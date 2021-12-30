'''
This script was used to parse the NT file to N3

Authors:
João Ferreira - 80041
João Magalhães - 79923
'''


ns0 = "@prefix ns0: <http://netflix-titles.com/pred/> ."
xsd = "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."

with open('netflix_titles.nt') as ficheiro: 
    entities = []
    for line in ficheiro:
        entity = line.split(" ")[0]
        if entity not in entities:
            entities.append(entity)
        #entities.append( line.split(" ")[0] )


with open('netflix_titles.n3', 'w') as output:
    output.write(ns0+"\n")
    output.write(xsd)


output_str = ""
with open('netflix_titles.n3', 'w') as output:   
    
        for entity in entities:
            #print(entity)
            output_str = entity + "\n"
            
            with open('netflix_titles.nt') as ficheiro:
                for line in ficheiro:
                    if line.startswith(entity) and "http://netflix-titles.com/dir/" not in line:
                        if "pred/type" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/type>", "ns0:type")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(output_str +"|"+ new_line)
                            output_str += new_line
                        elif "pred/title" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/title>", "ns0:title")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(output_str + new_line)
                            output_str += new_line
                        elif "pred/directed_by" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/directed_by>", "ns0:directed_by")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/cast" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/cast>", "ns0:cast")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/country" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/country>", "ns0:country")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/date_added" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/date_added>", "ns0:date_added")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/release_year" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/release_year>", "ns0:release_year")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/duration" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/duration>", "ns0:duration")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/listed_in" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/listed_in>", "ns0:listed_in")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string .")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/name" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/name>", "ns0:name")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string ;")
                            #print(new_line)
                            output_str += new_line
                        elif "pred/acted_in" in line:
                            new_line = line.replace("<http://netflix-titles.com/pred/acted_in>", "ns0:acted_in")
                            new_line = new_line.replace(new_line.split(" ")[0], " ")
                            new_line = new_line.replace("<http://www.w3.org/2001/XMLSchema#string> .","xsd:string .")
                            #print(new_line)
                            output_str += new_line
            print(output_str)
            output.write(output_str+"\n")
