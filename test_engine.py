from pathlib import Path
import unittest
from engine import parse,validate,load
class TimingTests(unittest.TestCase):
 def setUp(self):
  self.ep=load(Path(__file__).parent/'original.txt')[0]
  self.c=dict(start_id=1,end_id=10,hook_id=1,cliffhanger_id=10,title='t',hook='h',cliffhanger='c',unanswered_question='q',why_it_works='w')
 def test_sample(self): self.assertEqual(validate(self.ep,self.c)['duration'],42)
 def test_unknown(self):
  with self.assertRaises(ValueError): validate(self.ep,dict(self.c,start_id=999))
 def test_reversed(self):
  with self.assertRaises(ValueError): validate(self.ep,dict(self.c,start_id=10,end_id=1))
 def test_short(self):
  with self.assertRaises(ValueError): validate(self.ep,dict(self.c,end_id=2))
 def test_overlap(self):
  self.ep['entries'].append(dict(id=11,start=40,end=45,dialogue=True,kind='VOICE',text='overlap'))
  with self.assertRaisesRegex(ValueError,'dialogue'): validate(self.ep,self.c)
 def test_invalid_input(self):
  with self.assertRaises(ValueError): parse('bad',b'no timestamps')
 def test_hook_late(self):
  with self.assertRaises(ValueError): validate(self.ep,dict(self.c,hook_id=4))
if __name__=='__main__': unittest.main()
