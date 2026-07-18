# 🎵 Music Recommender Simulation

## Project Summary

TBD.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems combine user behavior and item features to predict what listeners will enjoy next. They look at what similar users liked, but they also pay attention to song attributes like genre, mood, energy, and tempo to match the emotional and stylistic vibe of the listener. My version will prioritize a content-based approach using song metadata and audio-style features, scoring tracks by how closely they match the user’s preferred mood and energy profile.

- `Song` features used in this simulation:
  - `genre`
  - `mood`
  - `energy`
  - `tempo_bpm`
  - `valence`
  - `danceability`
  - `acousticness`

- `UserProfile` features used in this simulation:
  - `favorite_genre`
  - `favorite_mood`
  - `target_energy`
  - `likes_acoustic`

### Algorithm Recipe

**Input** → **Process** → **Output**

```
INPUT: User Preferences
  ├─ favorite_genre
  ├─ favorite_mood
  ├─ target_energy
  └─ likes_acoustic

    ↓

PROCESS: Score Each Song in CSV
  For each song:
    1. Genre match?      → +2.0 points
    2. Mood match?       → +1.0 point
    3. Energy similarity → 0.0 to 1.0 points (max when energy == target_energy)
    4. Total Score = sum of all matches
    5. Store (song, score, reasons)

    ↓

OUTPUT: Top K Rankings
  1. Sort all (song, score) pairs by score (descending)
  2. Return top K results with explanations
```

**Potential Biases to Watch:**
- **Genre over-prioritization**: Genre is weighted at +2.0 vs mood (+1.0), so great songs matching mood but in a different genre may be ranked lower
- **Categorical rigidity**: Genre and mood are binary matches (exact match = points, no match = 0), so a similar-but-not-exact genre won't score
- **Ignoring `acousticness` preference**: The `likes_acoustic` field is captured but not used in scoring logic, creating a blind spot
- **Energy dominance edge case**: If the target energy is very different from most songs, energy similarity could overshadow genre/mood matches
- **Small catalog bias**: With only 4 songs, any weighting imbalance creates extreme skew; results won't generalize to larger music libraries

---

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Here's the actual terminal output showing recommendations for two user profiles:

```
Loading songs from data/songs.csv...
  ✓ Loaded 20 songs

============================================================
         PROFILE 1: High-Energy Pop -- Top 5 Results        
============================================================

#1  Sunrise City by Neon Echo
    Genre: pop | Mood: happy | Tempo: 118 BPM
    Match Score: 1.000 / 1.000

    Why this song?
      - Genre match
      - Mood match
      - Energy match (1.00)
------------------------------------------------------------

#2  Gym Hero by Max Pulse
    Genre: pop | Mood: intense | Tempo: 132 BPM
    Match Score: 0.722 / 1.000

    Why this song?
      - Genre match
      - Energy match (0.89)
------------------------------------------------------------

#3  Rooftop Lights by Indigo Parade
    Genre: indie pop | Mood: happy | Tempo: 124 BPM
    Match Score: 0.485 / 1.000

    Why this song?
      - Mood match
      - Energy match (0.94)
------------------------------------------------------------

#4  Electric Dreams by Synth Wave
    Genre: electronic | Mood: uplifting | Tempo: 128 BPM
    Match Score: 0.240 / 1.000

    Why this song?
      - Energy match (0.96)
------------------------------------------------------------

#5  Urban Beats by DJ Nova
    Genre: hip-hop | Mood: energetic | Tempo: 95 BPM
    Match Score: 0.237 / 1.000

    Why this song?
      - Energy match (0.95)
------------------------------------------------------------

============================================================
            PROFILE 2: Chill Lofi -- Top 5 Results          
============================================================

#1  Midnight Coding by LoRoom
    Genre: lofi | Mood: chill | Tempo: 78 BPM
    Match Score: 1.000 / 1.000

    Why this song?
      - Genre match
      - Mood match
      - Energy match (1.00)
------------------------------------------------------------

#2  Library Rain by Paper Lanterns
    Genre: lofi | Mood: chill | Tempo: 72 BPM
    Match Score: 0.982 / 1.000

    Why this song?
      - Genre match
      - Mood match
      - Energy match (0.93)
------------------------------------------------------------

#3  Focus Flow by LoRoom
    Genre: lofi | Mood: focused | Tempo: 80 BPM
    Match Score: 0.745 / 1.000

    Why this song?
      - Genre match
      - Energy match (0.98)
```


---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



