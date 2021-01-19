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
