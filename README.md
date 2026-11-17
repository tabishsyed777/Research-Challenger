# Research-Challenger

Researcher, challenger, and editor agents review supplied local evidence. Citation validation rejects unknown source IDs. Citation existence does not prove factual support. Bundled sources are fictional; this version does not browse the web.

Requires Python 3.10+. No third-party dependencies.

```bash
python research_challenger.py
python -m unittest discover -s tests -v
```

Default mode uses scripted demo responses, not live AI. Reports and decision traces are saved under `work/`.

For live AI, set `OPENAI_API_KEY` in your environment, optionally `OPENAI_MODEL` (default `gpt-4.1-mini`), then run:

```bash
python research_challenger.py --live
```

Live mode sends supplied code/evidence to OpenAI and incurs API usage. Live API calls have not been verified with credentials. Errors stop the run; there is no silent demo fallback. Never commit credentials. Use `--out` to choose the report directory.

Custom evidence: pass `--question "Your question" --sources path.json`. Sources are JSON arrays with unique `id`, `title`, and `text` strings.

Tests and CI cover the bundled workflow and invalid inputs. Earlier user-specific test steps were unavailable and remain pending.
