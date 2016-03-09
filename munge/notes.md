Query to retrieve all occupations (i) with Chinese labels (ii) fulfilled by more than 10 individuals who (iii) have Chinese abstracts available.

`select distinct ?occupation ?occtag count(?person) {
 ?person <http://dbpedia.org/ontology/occupation> ?occupation.
 ?occupation <http://www.w3.org/2000/01/rdf-schema#label> ?occtag .
 ?person <http://dbpedia.org/ontology/abstract> ?abstract .
 ?person <http://www.w3.org/2000/01/rdf-schema#label> ?name .
 ?person a <http://dbpedia.org/ontology/Person> .
 FILTER(LANG(?occtag) = "zh")
 FILTER(LANG(?abstract) = 'zh')
 FILTER(LANG(?name) = 'zh')
} 
GROUP BY ?occupation ?occtag
HAVING (COUNT(?person) > 9)`


http://dbpedia.org/resource/Short_story
http://dbpedia.org/resource/Legislative_council
http://dbpedia.org/resource/Invention


Query to retrieve the names and abstracts of all persons 
(i) practicing an occupation and 
(ii) who have these attributes available in Chinese

select distinct ?name ?abstract {
 ?person <http://dbpedia.org/ontology/occupation> ?occupation.
 ?person <http://dbpedia.org/ontology/abstract> ?abstract .
 ?person <http://www.w3.org/2000/01/rdf-schema#label> ?name .
 ?person a <http://dbpedia.org/ontology/Person> .
 FILTER(LANG(?abstract) = 'zh')
 FILTER(LANG(?name) = 'zh')
}

APIs for pinyin, traditional characters available: but need to assess