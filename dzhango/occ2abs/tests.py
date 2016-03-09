from django.test import TestCase
from .views import OccQueryForm, url_to_display_string, query_for_people
from django.http import HttpRequest

class OccQueryFormTest(TestCase):

    def setUp(self):
        self.oqf = OccQueryForm()

    def test_getting_occupations(self):
        """
        Ensure response non-empty
        """
        results = self.oqf.query_for_occupations()
        self.assertGreater(len(results), 1, 'Empty response') # empty set still with header info, hence 1

    def test_occupations_well_formed(self):
        """
        Response should be a list of tuples, the first element of which must be a URI
        """
        results = self.oqf.query_for_occupations()
        self.assertEquals(len(results[0]), 2, 'Occupation tuples must have length 2')
        self.assertRegex(results[1][0], '^http:', 'Occupation identifiers must be URIs')

    def test_occupations_have_all_info_types(self):
        """
        Occupation labels should be of the form Simplified Character text, English text, hit count
        """
        results = self.oqf.query_for_occupations()
        test_string = results[1][1]
        self.assertRegex(test_string, '^[\u4e00-\u9fff]+ \([\w\s]+\) \[[\d]+ hits\]', 'Occupation labels must be of the form Simplified Character text, English text, hit count')

class ViewsTest(TestCase):

    def test_url_to_display_string(self):
        """
        Should do nothing more than lop the final path element from a URL and swap in spaces for underscores
        """
        self.assertEquals(url_to_display_string('http://dbpedia.org/ontology/Record_producer'), 'Record producer')
        self.assertEquals(url_to_display_string('http://dbpedia.org/ontology/Animator'), 'Animator')

    def test_query_for_people(self):
        """
        Ensure response non-empty
        """
        testparams = HttpRequest()
        setattr(testparams, 'GET', {})
        testparams.GET['occ'] = 'http://dbpedia.org/resource/Philosopher'
        testparams.GET['sort_by'] = 'zh'
        self.assertGreater(len(query_for_people(testparams).content), 1, 'People query should return at least one result')