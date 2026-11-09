import json,tempfile,unittest,zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import engine
class WorkflowTests(unittest.TestCase):
 def setUp(self):
  self.sample=json.loads((Path(__file__).parent/'original-results.json').read_text(encoding='utf-8'))
  self.clip=self.sample['ranked'][0]
 def test_valid_saved_results(self):self.assertIs(engine.validate_results(self.sample),self.sample)
 def test_unrelated_json_rejected(self):
  with self.assertRaises(ValueError):engine.validate_results({'hello':'world'})
 def test_missing_nested_field(self):
  del self.clip['critique']['weakness']
  with self.assertRaises(ValueError):engine.validate_results(self.sample)
 def test_score_range(self):
  self.clip['score']=101
  with self.assertRaises(ValueError):engine.validate_results(self.sample)
 def test_large_input(self):
  with self.assertRaisesRegex(ValueError,'20MB'):engine.parse('large',b'x'*20_000_001)
 def test_empty_zip(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.zip'
   with zipfile.ZipFile(p,'w') as z:z.writestr('note.md','irrelevant')
   with self.assertRaisesRegex(ValueError,'No text'):engine.load(p)
 def test_corrupt_zip(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.zip';p.write_bytes(b'not a zip')
   with self.assertRaises(zipfile.BadZipFile):engine.load(p)
 def test_retry_preserves_attempts(self):
  response=lambda text:SimpleNamespace(output_text=text,model_dump_json=lambda:json.dumps({'output_text':text}))
  with tempfile.TemporaryDirectory() as d,patch('google.genai.Client') as client,patch('engine.time.sleep'):
   client.return_value.interactions.create.side_effect=[response('invalid'),response('{"candidates":[]}')]
   self.assertEqual(engine.call_ai('test',engine.Proposals,'fake',Path(d),'test','fake-key'),{'candidates':[]})
   self.assertTrue((Path(d)/'test.attempt-0.response.json').exists());self.assertTrue((Path(d)/'test.attempt-1.response.json').exists())
 def test_retry_limit(self):
  with tempfile.TemporaryDirectory() as d,patch('google.genai.Client') as client,patch('engine.time.sleep'):
   client.return_value.interactions.create.side_effect=RuntimeError('network unavailable')
   with self.assertRaises(RuntimeError):engine.call_ai('test',engine.Proposals,'fake',Path(d),'test','fake-key')
   self.assertEqual(client.return_value.interactions.create.call_count,3)
 def test_pipeline_cache_and_exports(self):
  with tempfile.TemporaryDirectory() as d,patch('engine.call_ai',side_effect=[{'candidates':[self.clip]},self.clip['critique']]) as ai:
   r=engine.run(Path(__file__).parent/'original.txt',d,'fake');self.assertTrue(r['complete']);self.assertEqual(len(r['ranked']),1)
   engine.run(Path(__file__).parent/'original.txt',d,'fake');self.assertEqual(ai.call_count,2)
   self.assertTrue((Path(d)/'ranked.csv').read_text().startswith('rank,episode'))
 def test_provider_failure_visible(self):
  with tempfile.TemporaryDirectory() as d,patch('engine.call_ai',side_effect=RuntimeError('provider unavailable')):
   r=engine.run(Path(__file__).parent/'original.txt',d,'fake');self.assertFalse(r['complete']);self.assertEqual(r['episodes'][0]['state'],'failed');self.assertEqual(r['ranked'],[])
 def test_invalid_proposal_rejected(self):
  self.clip['start_id']=999
  with tempfile.TemporaryDirectory() as d,patch('engine.call_ai',return_value={'candidates':[self.clip]}):
   r=engine.run(Path(__file__).parent/'original.txt',d,'fake');self.assertEqual(len(r['rejected']),1);self.assertFalse(r['ranked'])
 def test_duplicates_preserved(self):
  with tempfile.TemporaryDirectory() as d,patch('engine.call_ai',side_effect=[{'candidates':[self.clip,self.clip]},self.clip['critique'],self.clip['critique']]):
   r=engine.run(Path(__file__).parent/'original.txt',d,'fake');self.assertEqual(len(r['ranked']),1);self.assertEqual(len(r['duplicates']),1)
 def test_zero_candidates(self):
  with tempfile.TemporaryDirectory() as d,patch('engine.call_ai',return_value={'candidates':[]}):
   r=engine.run(Path(__file__).parent/'original.txt',d,'fake');self.assertTrue(r['complete']);self.assertFalse(r['ranked'])
if __name__=='__main__':unittest.main()
