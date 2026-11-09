from pathlib import Path
import unittest
from engine import load,boundary_menu,validate
class MenuTests(unittest.TestCase):
 def test_menu_boundaries(self):
  ep=load(Path(__file__).parent/'original.txt')[0]
  menu=boundary_menu(ep)
  self.assertTrue(menu)
  for w in menu:
   by={e['id']:e for e in ep['entries']}; a=by[w['start_id']]['start'];b=by[w['end_id']]['end']
   self.assertTrue(20<=b-a<=60)
   self.assertFalse(any(e['dialogue'] and (e['start']<a<e['end'] or e['start']<b<e['end']) for e in ep['entries']))
