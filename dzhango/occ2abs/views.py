from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import EndPointNotFound, EndPointInternalError
from django import forms
from json import dumps

class OccQueryForm(forms.Form):

    def __init__(self, language, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        lang_to_label = {"zh":"Chinese Simplified Characters", "ar":"Arabic", "ja":"Japanese"}
        self.fields['language_options'] = forms.ChoiceField(label="Language options", choices=[('zh', 'Chinese Simplified Characters'), ('ar', 'Arabic'), ('ja', 'Japanese')], initial=language, widget=forms.RadioSelect(attrs={ 'id' : 'lang-selector'}))
        self.fields['sort_options'] = forms.ChoiceField(label="Sort options", choices=[('other', lang_to_label[language]), ('en', 'English')], initial='other', widget=forms.RadioSelect(attrs={ 'id' : 'sort-selector'}))
        self.occ_options = self.query_for_occupations(language)
        self.fields['occupations'] = forms.ChoiceField(label="Occupation", choices=self.occ_options, widget=forms.Select(attrs={ 'id' : 'occ-selector'}), initial='')

    def query_for_occupations(self, lang):
        """
         Queries to retrieve all occupations (i) with both en and lang labels (ii) fulfilled by more than
         10 individuals who (iii) have both en and lang abstracts available.
         :param lang: 2-letter language code (ar|zh|ja)
        :return: A JSON serialization of the response
        """
        endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
        occsQuery = """
            select distinct ?occupation ?occtag count(?person) as ?count {
                ?person <http://dbpedia.org/ontology/occupation> ?occupation.
                ?occupation <http://www.w3.org/2000/01/rdf-schema#label> ?occtag .
                FILTER(LANG(?occtag) = '"""  + lang + """')
                FILTER(EXISTS { ?occupation <http://www.w3.org/2000/01/rdf-schema#label> ?occtag_en . FILTER(LANG(?occtag_en) = 'en') })
                ?person <http://dbpedia.org/ontology/abstract> ?abstract .
                FILTER(LANG(?abstract) = '"""  + lang + """')
                FILTER(EXISTS { ?person <http://dbpedia.org/ontology/abstract> ?abstract_en . FILTER(LANG(?abstract_en) = 'en') })
                ?person <http://www.w3.org/2000/01/rdf-schema#label> ?name .
                ?person a <http://dbpedia.org/ontology/Person> .
                FILTER(LANG(?name) = '"""  + lang + """') .
                FILTER(EXISTS { ?person <http://www.w3.org/2000/01/rdf-schema#label> ?name_en . FILTER(LANG(?name_en) = 'en') })
            }
            GROUP BY ?occupation ?occtag
            HAVING (COUNT(?person) >=10)
            ORDER BY ?occtag
            """
        endpoint.setQuery(occsQuery)
        endpoint.setReturnFormat(JSON)
        results = endpoint.queryAndConvert()
        # we need to eliminate gibberish values
        nonsense_occs = ['http://dbpedia.org/resource/Invention', 'http://dbpedia.org/resource/Violin', 'http://dbpedia.org/resource/Arrangement', 'http://dbpedia.org/resource/Anime', 'http://dbpedia.org/resource/Short_story', 'http://dbpedia.org/resource/Legislative_council', 'http://dbpedia.org/resource/Voice_acting_in_Japan', 'http://dbpedia.org/resource/Linguistics']
        occ_options = [('', '--------------------------')]
        for result in results["results"]["bindings"]:
            occupation_url = result["occupation"]["value"]
            if(occupation_url not in nonsense_occs):
                occupation_label = result["occtag"]["value"]
                occupation_label_en = url_to_display_string(occupation_url)
                occupation_count = result["count"]["value"]
                occupation_display_string = occupation_label + " (" + occupation_label_en + ") [" + str(occupation_count) + " hits]"
                occ_options.append((occupation_url, occupation_display_string))
        return occ_options

def query(request, lang):
    lang = lang.lower() if(lang.lower() in ['zh', 'ar', 'ja']) else 'zh'
    try:
        oqf = OccQueryForm(language=lang)
        return render(request, 'occ2abs/queryform.html', {'form':oqf })
    except (EndPointNotFound, EndPointInternalError) as e:
        return render(request, 'occ2abs/queryform.html', context={'error_msg' : str(e)})

def url_to_display_string(url):
    """
    A crude hack to generate readable en-labels from URLs
    :param url: The dbpedia URL from which the label is to be derived
    :return: The human readable label

    TODO: Replace this with the rdfs:label

    """
    raw_label = url.split('/')[-1]
    label = raw_label.replace('_', ' ')
    return label

def query_for_people(search_params):
    """
    Queries the dbpedia sparql endpoint for all persons matching the occupation passed in the
    searchparam object, providing that they have both other-language and en names and abstracts available

    :param search_params: Request object holding a dbpedia url resolving to an occupation and a preferred sort order
    :return: the name and abstract, in other-language and en, of all persons holding that occupation with the requisite dataa
    """
    qry = build_query_people(search_params)
    try:
        endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
        endpoint.setQuery(qry)
        endpoint.setReturnFormat(JSON)
        results = endpoint.queryAndConvert()
        return HttpResponse(dumps(results['results']['bindings']))
    except (EndPointNotFound, EndPointInternalError) as e:
        return HttpResponse(dumps({'err_msg' : str(e)}))

def build_query_people(search_params):
    """
    Builds a query to retrieve the names and abstracts of all persons (i) practicing an occupation and
    (ii) who have these attributes available in both en and the target language, ordered by either of
    these language orderings.
    :param search_params: Request object holding a dbpedia url resolving to an occupation, a preferred
    sort order, and the language of the query
    :return: the relevant SPARQL query as a string
    """
    occupation = search_params.GET['occ']
    sort_by = search_params.GET['sort_by']
    language = search_params.GET['language']
    sort_field = "?name" if(sort_by == 'other') else "?name_en"
    people_qry = """
    select distinct ?person ?name ?abstract ?name_en ?abstract_en
        where{
            ?person <http://dbpedia.org/ontology/abstract> ?abstract_en .
            ?person <http://www.w3.org/2000/01/rdf-schema#label> ?name_en .
            FILTER(LANG(?abstract_en) = 'en')
            FILTER(LANG(?name_en) = 'en')
            {select distinct ?person ?name ?abstract  {
            ?person <http://dbpedia.org/ontology/occupation> <""" + occupation + """> .
            ?person <http://dbpedia.org/ontology/abstract> ?abstract .
            ?person <http://www.w3.org/2000/01/rdf-schema#label> ?name .
            ?person a <http://dbpedia.org/ontology/Person> .
            FILTER(LANG(?abstract) = '""" + language + """')
            FILTER(LANG(?name) = '""" + language + """')
        }}} ORDER BY """ + sort_field
    return people_qry
