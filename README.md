# Playlist Chaos — Fixed Version

This is a cleaned and debugged version of the CodePath Playlist Chaos Streamlit lab.

## What was fixed

- Song classification now follows the intended Hype, Chill, and Mixed rules.
- Search is case-insensitive and supports partial matching.
- Playlist statistics use unique songs across all categories.
- Lucky Pick only pulls from the selected playlist unless "Any" is selected.
- User input is normalized by trimming whitespace and lowercasing artist/genre fields.
- Repeated normalization logic was refactored into helper functions.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Testing checklist

Try these songs:

| Title | Artist | Genre | Energy | Expected Playlist |
|---|---|---|---:|---|
| Thunderstruck | AC/DC | Rock | 6 | Hype |
| Sleep Waves | Calm Artist | Ambient | 5 | Chill |
| Regular Song | Some Artist | Folk | 5 | Mixed |
| Party Night | DJ Test | Party | 4 | Hype |
| Lofi Rain | Chill Person | Hip Hop | 6 | Chill |
| Loud Song | Random | Jazz | 8 | Hype |

Also test:

- Search artist `ac` should find `AC/DC`.
- Search title `lofi` should find `Lofi Rain`.
- Lucky Pick with `Hype` should only return Hype songs.
- Lucky Pick with `Chill` should only return Chill songs.
- Lucky Pick with `Any` can return Hype, Chill, or Mixed songs.

## Optional unit tests

Install pytest:

```bash
pip install pytest
```

Run tests:

```bash
pytest
```

## Suggested Git commits

```bash
git add app.py playlist_logic.py
git commit -m "fix: resolved incorrect behavior in playlist logic"
```

```bash
git add app.py playlist_logic.py README.md tests/test_playlist_logic.py
git commit -m "refactor: improved structure and readability"
```
