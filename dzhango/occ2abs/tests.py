from django.test import TestCase
from .views import OccQueryForm, url_to_display_string, query_for_people
from django.http import HttpRequest

class OccQueryFormTest(TestCase):

    def setUp(self):
        self.oqf = OccQueryForm("zh")

    def test_getting_occupations(self):
        """
        Ensure response non-empty
        """
        results = self.oqf.query_for_occupations("zh")
        self.assertGreater(len(results), 1, 'Empty response') # empty set still with header info, hence 1

    def test_occupations_well_formed(self):
        """
        Response should be a list of tuples, the first element of which must be a URI
        """
        results = self.oqf.query_for_occupations("zh")
        self.assertEquals(len(results[0]), 2, 'Occupation tuples must have length 2')
        self.assertRegex(results[1][0], '^http:', 'Occupation identifiers must be URIs')

    def test_occupations_have_all_info_types_zh(self):
        """
        Chinese occupation labels should be of the form Simplified Character text, English text, hit count
        """
        results = self.oqf.query_for_occupations("zh")
        test_string = results[1][1]
        self.assertRegex(test_string, '^[\u4e00-\u9fff]+ \([\w\s]+\) \[[\d]+ hits\]', 'Chinese occupation labels must be of the form Simplified Character text, English text, hit count')

    def test_occupations_have_all_info_types_ar(self):
        """
        Arabic occupation labels should be of the form Arabic text, English text, hit count
        """
        results = self.oqf.query_for_occupations("ar")
        test_string = results[1][1]
        self.assertRegex(test_string, '^[\u0600-\u06ff]+ \([\w\s]+\) \[[\d]+ hits\]', 'Arabic occupation labels must be of the form Arabic text, English text, hit count')

    def test_occupations_have_all_info_types_ja(self):
        """
        Japanese occupation labels should be of the form Japanese text, English text, hit count
        """
        results = self.oqf.query_for_occupations("ja")
        test_string = results[2][1]
        # TODO: This regex is too tight and too loose - can't cope with latin alphabet characters appearing
        #  in the text, and covers everything from the katakana block up to the end of the usual
        #  zh range
        self.assertRegex(test_string, '^[\u30A0-\u9fff]+ \([\w\s]+\) \[[\d]+ hits\]', 'Japanese occupation labels must be of the form Japanese text, English text, hit count')

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
        testparams.GET['sort_by'] = 'other'
        testparams.GET['language'] = 'zh'
        self.assertGreater(len(query_for_people(testparams).content), 1, 'People query should return at least one result')