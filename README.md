# Cut Before the Answer
Surya Dev Vinod | 230121059 | Engineering Physics | Kuku Problem 1

A screenplay-to-promo editor workbench. AI proposes; code validates; an editor approves.

## Run
Python 3.11 or later recommended.

```powershell
python -m pip install -r requirements.txt
$env:GEMINI_API_KEY = "your-local-key"
python -m streamlit run app.py
```

Upload the original sample TXT, a screenplay TXT, or a ZIP containing TXT scripts. To batch-process:

```powershell
python engine.py "path-to-input.zip" --output runs/full-pack --model gemini-3.1-flash-lite
```

Use any available Gemini model name in the Model field or `--model`. Replace `call_ai` to connect another provider. No keys are committed. Runs contain confidential excerpts; never publish them.

## What it checks
20–60 seconds from actual timeline boundaries; source IDs must exist; no spoken line may straddle a cut. Hook must begin within three seconds, cliffhanger evidence must finish within five seconds of the end. Quality scores: hook 30%, cliffhanger 30%, standalone clarity 25%, pacing 15%. Flags rank below unflagged candidates. Same-episode clips overlapping more than 70% of the shorter clip are retained as duplicates in the audit, excluded from shortlist.

## Outputs and recovery
Each episode folder preserves prompts, full SDK responses and validated results. `results.json` includes coverage, failures, duplicates and rankings; `ranked.csv` is editor-ready. Rerun the same command to resume completed episodes. Source hashes, model and version determine cache identity. Three bounded attempts handle API failures. Failed episodes remain explicit, not silently skipped.

Manual fallback: provide `--manual folder` with `episode-001.json` etc. Each file contains a `candidates` array matching Candidate in engine.py and a matching `critiques` array. This import is labeled manual, never described as an API run. Change output directory when changing imported responses.

## Limits
Scripts cannot prove visual delivery or ad performance. Rubric judgments may share the selecting model's biases. Continuous clips only. Uploaded script content is sent to the configured Gemini API. The public sample is original fiction; Kuku scripts and results belong in the private reviewer package.

## Verification
`python -m unittest test_engine test_menu -v`

AI assistance: Codex helped implement and inspect the tool. Final decisions and interview explanation must be understood by the submitter.

Original sample: `original.txt`. It contains no supplied Kuku content.

## No-key demonstration
Open the workbench and load `original-results.json` in **Open saved results**. It is an actual Gemini result on the original sample. New generation requires your own API key. Tested with streamlit 1.67.0, google-genai 3.0.0 and pydantic 2.14.3.
