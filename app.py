import csv, io, json, os, tempfile
from pathlib import Path
import streamlit as st
from engine import run
st.set_page_config(page_title='Cut Before the Answer',page_icon='✂',layout='wide')
st.markdown('<style>.stApp{background:#10141c}h1{letter-spacing:-2px}.stMetric{background:#1b2230;padding:16px;border-radius:12px}</style>',unsafe_allow_html=True)
st.caption('SURYA DEV VINOD · 230121059 · ENGINEERING PHYSICS')
st.title('Cut Before the Answer')
st.write('Find the moment that makes a stranger stop—and the question that makes them stay.')
with st.sidebar:
 st.header('Editor workbench')
 key=st.text_input('Gemini API key',type='password',help='Used for this session; never included in downloads.')
 model=st.text_input('Model',value='gemini-3.1-flash-lite')
 uploaded=st.file_uploader('Screenplay ZIP or TXT',type=['zip','txt'])
 imported=st.file_uploader('Open saved results',type=['json'])
 st.caption('Continuous clips · 20–60 seconds · Script evidence only')
if imported:
 try: st.session_state['result']=json.load(imported)
 except Exception as e: st.error(str(e))
if st.button('Find promos',type='primary',disabled=not uploaded):
 if not (key or os.getenv('GEMINI_API_KEY')): st.error('Enter a Gemini API key first.')
 else:
  try:
   with tempfile.TemporaryDirectory() as d:
    path=Path(d)/('input.zip' if uploaded.name.lower().endswith('.zip') else 'input.txt'); path.write_bytes(uploaded.getvalue())
    with st.spinner('Reading, selecting, checking and ranking…'):
     st.session_state['result']=run(path,Path(d)/'run',model,api_key=key or None)
  except Exception as e: st.error(str(e))
r=st.session_state.get('result')
if r:
 a,b,c=st.columns(3); a.metric('Episodes processed',len(r['episodes'])); b.metric('Ranked promos',len(r['ranked'])); c.metric('Run status','Complete' if r['complete'] else 'Incomplete')
 st.caption('Editorial scores are judgments, not predictions of views or conversions. Review flags sort after candidates that pass the quality rubric.')
 st.download_button('Download results JSON',json.dumps(r,indent=2),file_name='promo-results.json')
 csv_buffer=io.StringIO(); fields=['rank','episode','start','end','duration','score','needs_review','title','hook','cliffhanger','unanswered_question','why_it_works']; writer=csv.DictWriter(csv_buffer,fieldnames=fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(r['ranked'])
 st.download_button('Download ranked CSV',csv_buffer.getvalue(),file_name='ranked-promos.csv')
 limit=st.slider('Recommendations to show',1,len(r['ranked']),min(10,len(r['ranked']))) if len(r['ranked'])>1 else len(r['ranked'])
 for c in r['ranked'][:limit]:
  with st.container(border=True):
   st.subheader(f"#{c['rank']}  {c['title']}")
   st.caption(f"{c['episode']} · {c['start']} → {c['end']} · {c['duration']}s · {c['score']}/100 · {'REVIEW' if c['needs_review'] else 'SHORTLIST'}")
   left,right=st.columns(2)
   left.markdown('**Hook**'); left.write(c['hook']); right.markdown('**Cliffhanger**'); right.write(c['cliffhanger'])
   st.info(c['unanswered_question']); st.write(c['why_it_works']); st.warning(c['critique']['weakness'])
   with st.expander('Inspect source evidence and rubric'):
    st.json(c['critique'])
    for e in c['excerpt']: st.text(f"[{e['id']}] {e['start']:.2f}–{e['end']:.2f} {e['kind']}: {e['text']}")
 with st.expander('Coverage and rejected proposals'): st.json({'episodes':r['episodes'],'rejected':r['rejected']})
else:
 st.info('Upload scripts to find promos, or open results.json from a saved run. The public sample is original fiction; the assignment pack stays private.')
 st.markdown('### Three checks before a cut\n1. **Stop:** Is the hook visible in the first three seconds?\n2. **Understand:** Can a new viewer follow the stakes?\n3. **Need the answer:** Does the cut leave a specific question unresolved?')
