# occ2abs_zh

Toy application accepting occupations in zh, ar, or ja and returning names and abstracts n English and that language from the dbpedia sparql endpoint

## Specification

A small web application (preferably in Python) to extract a number of people (minimum 10) from the DBpedia endpoint with the follow-
ing parameters:

• occupation

• language (input restricted to Chinese (simplified characters in the first instance)

The web page should display the following information, in the specified language

• name

• abstract

Follow best practices (both in your chosen programming language and SPARQL)

## Limitations

TODO: Mediate into Solr index for better functionality (autocomplete rather than dropdown, no network latency)

TODO: Show/hide English translation

TODO: Support pinyin and traditional characters

TODO: Improve filtering of occupations - many values are nonsense

TODO: Evaluate RTL rendering

TODO: Security: tighten screws on AJAX cleaning, accepted URLS.


