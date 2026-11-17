import unittest
from unittest.mock import patch
from engine import Agent
from research_challenger import research, validate_claims, validate_sources
SOURCES=[{'id':'s1','title':'Example','text':'Synthetic observation.'}]
class Tests(unittest.TestCase):
    def test_research_flow(self):
        a=Agent()
        self.assertEqual(research('Question',SOURCES,a)['claims'][0]['citations'],['s1'])
        self.assertEqual(len(a.trace),3)
    def test_bad_citation(self):
        with self.assertRaises(ValueError): validate_claims({'claims':[{'text':'Claim','citations':['invented']}]},{'s1'})
    def test_duplicates(self):
        with self.assertRaises(ValueError): validate_sources(SOURCES*2)
    def test_empty_sources(self):
        with self.assertRaises(ValueError): research('Question',[],Agent())
    def test_missing_key(self):
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaisesRegex(ValueError,'OPENAI_API_KEY'): Agent(True).run('role',{}, {})
