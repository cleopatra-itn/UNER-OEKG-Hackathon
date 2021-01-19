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
### All broadcast programs in Greece
```
SELECT DISTINCT ?eq ?label ?eventDate ?place ?loclabel
WHERE
{
  ?eq rdf:type uner:Broadcast_Program .
  ?eq sem:hasBeginTimeStamp ?eventDate .
  ?eq rdfs:label ?label .
  ?eq sem:hasPlace ?place .
  ?place rdfs:label ?loclabel .
  ?place so:containedInPlace ?y .
  ?y owl:sameAs dbr:Greece .
 
} 
```
