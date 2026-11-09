# Three-minute walkthrough

Record this in your own voice after inspecting the actual output.

**0:00–0:25** “I am Surya Dev Vinod, Engineering Physics, roll number 230121059. I chose Find the Promos because an editor needs precise usable cuts, not just a summary of dramatic scenes. My tool is called Cut Before the Answer.”

**0:25–0:55** Open the workbench and upload the original sample. Explain the first three seconds, standalone stakes and unanswered ending. Show the model selector and explain it can change without changing timing rules.

**0:55–1:35** Open the saved full-pack results. State the actual coverage and shortlist count. Show the strongest recommendation: episode, timestamps, duration, hook, cliffhanger, and unanswered question. Read the warning as well as the recommendation.

**1:35–2:15** Expand source evidence. Explain that IDs refer to real timed entries and overlapping camera/dialogue descriptions do not add to clip duration. Show a rejected cut and its reason. Mention that footage can still require editorial adjustment.

**2:15–2:45** Show raw responses and exported CSV. Explain caching, retries, provider replacement and the observed model-availability failure. State one actual editorial failure found in review, if available; never invent one.

**2:45–3:00** “AI judges story appeal; code enforces timing; a human approves the edit. I would measure editor acceptance and time saved before claiming business impact.”

# Interview notes
- Why option 1? Real input, checkable output, direct operational value.
- Why continuous clips? Fewer continuity errors and easy editor handoff.
- Why two passes? Selection sees context; critique sees only what a stranger sees. Same-model bias remains.
- Why IDs? The model cannot invent timestamps; deterministic validation catches invalid references and spoken-line cuts.
- Why these weights? An explicit editorial starting assumption, not learned performance data. Tune with editor feedback.
- Scale? Cache by input hash/model/version, process episodes independently, add bounded workers within quotas, human-review top candidates. Log actual tokens/latency from responses; do not invent costs.
- What would improve it? Human labels, a second-model critique, footage-level boundary checks and measured ad experiments.
