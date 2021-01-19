### Get birthdate of fictional characters

```
SELECT ?person ?birthDate ?label
WHERE
{
 ?person rdf:type uner:Fictional .
 ?person rdfs:label ?label .
 ?person sem:hasBeginTimeStamp ?birthDate
}
```

### Get all holidays 
```
SELECT ?event ?eventDate ?label
WHERE
{
  
 ?event rdf:type uner:Holiday .
 ?event rdfs:label ?label .
 ?event sem:hasBeginTimeStamp ?eventDate
        
}
```

### Get all earthquakes with date and location
```
SELECT DISTINCT ?eq ?label ?eventDate ?place ?loclabel
WHERE
{
  ?eq rdf:type uner:Earthquake .
  ?eq sem:hasPlace ?place .
  ?eq rdfs:label ?label .
  ?place rdfs:label ?loclabel .
  ?eq sem:hasBeginTimeStamp ?eventDate
} 


```
