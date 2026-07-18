# 🎵 Music Recommender Simulation

## Project Summary

**ContentMatch 1.0** is a content-based music recommendation engine that demonstrates how real-world AI recommenders work by scoring songs based on user taste profiles. The system matches songs to user preferences using a weighted scoring formula: **genre match (+2.0 points) → mood match (+1.0 point) → energy similarity (0-1.0 points)**, then ranks and explains the top 5 recommendations.

**What this project does:**
- ✓ Loads a 20-song catalog with 17 genres and 12 mood categories
- ✓ Accepts user preferences (favorite_genre, favorite_mood, target_energy)
- ✓ Scores each song using transparent, rule-based logic
- ✓ Returns top K recommendations with explanations of why each song matched
- ✓ Runs as a command-line simulation with multiple test profiles

**What we discovered:**
- Genre dominance (+2.0 weight) overwhelms other factors—creating a "genre cliff" where perfect mood/energy matches lose to mediocre genre matches
- Niche genres (classical: 1 song) create recommendation deserts—users get perfect 1.000 scores for the only option, then cliff-drop to 0.458 for alternatives
- Silent failures occur when preferences don't co-exist in the dataset (e.g., high-energy + sad mood)—the algorithm falls back without explanation
- The system is fair to mainstream genres (pop, rock) but isolates users of niche genres

**Key insights:**
This project reveals that recommendation algorithms encode **design choices as values**—weighting decisions, feature selection, and data representation all introduce bias. By building and testing ContentMatch across 11 user profiles (5 standard + 6 adversarial edge cases), we identified critical fairness issues that mirror real-world apps like Spotify and Apple Music.

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

## Adversarial / Edge Case Testing

To stress-test the algorithm, I designed profiles with conflicting preferences or non-existent values. Here's what happens when the system encounters adversarial inputs:

### Key Findings:

1. **Genre Dominance**: When genre doesn't match anything (e.g., "reggaeton"), the algorithm falls back entirely to mood/energy. Genre's +2.0 weight creates a cliff: either you get it, or you don't.

2. **Mood Over-reliance**: When mood doesn't exist in the dataset (Edge Case 2), the algorithm *still performs well* because genre match (+2.0) carries the result.

3. **Energy Tie-breaking**: When genre/mood conflict (Edge Case 5: want "lofi" + high energy 0.92), the algorithm correctly prioritizes **genre** and ignores the conflicting energy preference. This shows the weighting hierarchy works.

4. **Extreme Values Work Well**: Extreme energy preferences (0.1 or 0.99) produce sensible results—the algorithm doesn't break.

5. **Single-Song Genres Dominate**: Niche genres like "classical" (only 1 song) get a perfect 1.000 score, showing the algorithm's **genre bias** can exclude diversity.

### Edge Case Results:

**Edge Case 1: Non-existent Genre (Reggaeton)**
```
Loading songs from data/songs.csv...
  ✓ Loaded 20 songs

============================================================
  EDGE CASE 1: Non-existent Genre (Reggaeton) -- Top 5 Results
============================================================

#1  Urban Beats by DJ Nova
    Genre: hip-hop | Mood: energetic | Tempo: 95 BPM
    Match Score: 0.495 / 1.000

    Why this song?
      - Mood match
      - Energy match (0.98)
------------------------------------------------------------

#2  Techno Pulse by Electronic Beats
    Genre: techno | Mood: energetic | Tempo: 135 BPM
    Match Score: 0.485 / 1.000

    Why this song?
      - Mood match
      - Energy match (0.94)
------------------------------------------------------------

#3  Sunrise City by Neon Echo
    Genre: pop | Mood: happy | Tempo: 118 BPM
    Match Score: 0.242 / 1.000

    Why this song?
      - Energy match (0.97)
------------------------------------------------------------

#4  Storm Runner by Voltline
    Genre: rock | Mood: intense | Tempo: 152 BPM
    Match Score: 0.235 / 1.000

    Why this song?
      - Energy match (0.94)
------------------------------------------------------------

#5  Electric Dreams by Synth Wave
    Genre: electronic | Mood: uplifting | Tempo: 128 BPM
    Match Score: 0.233 / 1.000

    Why this song?
      - Energy match (0.93)
```

**Edge Case 2: Non-existent Mood (Transcendent)**
```
============================================================
  EDGE CASE 2: Non-existent Mood (Transcendent) -- Top 5 Results
============================================================

#1  Coffee Shop Stories by Slow Stereo
    Genre: jazz | Mood: relaxed | Tempo: 90 BPM
    Match Score: 0.718 / 1.000

    Why this song?
      - Genre match
      - Energy match (0.87)
------------------------------------------------------------

#2  Misty Mountains by Folk Wanderers
    Genre: folk | Mood: dreamy | Tempo: 85 BPM
    Match Score: 0.237 / 1.000

    Why this song?
      - Energy match (0.95)
------------------------------------------------------------

#3  Island Vibes by Reggae Kings
    Genre: reggae | Mood: relaxed | Tempo: 100 BPM
    Match Score: 0.230 / 1.000

    Why this song?
      - Energy match (0.92)
------------------------------------------------------------

#4  Midnight Coding by LoRoom
    Genre: lofi | Mood: chill | Tempo: 78 BPM
    Match Score: 0.230 / 1.000

    Why this song?
      - Energy match (0.92)
------------------------------------------------------------

#5  Heartbreak Road by Country Soul
    Genre: country | Mood: melancholic | Tempo: 92 BPM
    Match Score: 0.230 / 1.000

    Why this song?
      - Energy match (0.92)
```

**Edge Case 3: Extremely Low Energy (0.1)**
```
============================================================
   EDGE CASE 3: Extremely Low Energy (0.1) -- Top 5 Results 
============================================================

#1  Nocturne in D Minor by Classical Ensemble
    Genre: classical | Mood: melancholic | Tempo: 70 BPM
    Match Score: 0.963 / 1.000

    Why this song?
      - Genre match
      - Mood match
      - Energy match (0.85)
------------------------------------------------------------

#2  Heartbreak Road by Country Soul
    Genre: country | Mood: melancholic | Tempo: 92 BPM
    Match Score: 0.420 / 1.000

    Why this song?
      - Mood match
------------------------------------------------------------

#3  Spacewalk Thoughts by Orbit Bloom
    Genre: ambient | Mood: chill | Tempo: 60 BPM
    Match Score: 0.205 / 1.000

    Why this song?
      - Energy match (0.82)
------------------------------------------------------------

#4  Library Rain by Paper Lanterns
    Genre: lofi | Mood: chill | Tempo: 72 BPM
    Match Score: 0.188 / 1.000

    Why this song?
      - Energy match (0.75)
------------------------------------------------------------

#5  Coffee Shop Stories by Slow Stereo
    Genre: jazz | Mood: relaxed | Tempo: 90 BPM
    Match Score: 0.182 / 1.000

    Why this song?
      - Energy match (0.73)
```

**Edge Case 4: Extremely High Energy (0.99)**
```
============================================================
  EDGE CASE 4: Extremely High Energy (0.99) -- Top 5 Results
============================================================

#1  Raging Inferno by Metal Masters
    Genre: metal | Mood: aggressive | Tempo: 160 BPM
    Match Score: 0.990 / 1.000

    Why this song?
      - Genre match
      - Mood match
      - Energy match (0.96)
------------------------------------------------------------

#2  Gym Hero by Max Pulse
    Genre: pop | Mood: intense | Tempo: 132 BPM
    Match Score: 0.235 / 1.000

    Why this song?
      - Energy match (0.94)
------------------------------------------------------------

#3  Storm Runner by Voltline
    Genre: rock | Mood: intense | Tempo: 152 BPM
    Match Score: 0.230 / 1.000

    Why this song?
      - Energy match (0.92)
------------------------------------------------------------

#4  Techno Pulse by Electronic Beats
    Genre: techno | Mood: energetic | Tempo: 135 BPM
    Match Score: 0.230 / 1.000

    Why this song?
      - Energy match (0.92)
------------------------------------------------------------

#5  Urban Beats by DJ Nova
    Genre: hip-hop | Mood: energetic | Tempo: 95 BPM
    Match Score: 0.220 / 1.000

    Why this song?
      - Energy match (0.88)
```

**Edge Case 5: Sleep/Dance Conflict (Lofi + 0.92 Energy)**
```
============================================================
  EDGE CASE 5: Sleep/Dance Conflict (Lofi + 0.92 Energy) -- Top 5 Results
============================================================

#1  Midnight Coding by LoRoom
    Genre: lofi | Mood: chill | Tempo: 78 BPM
    Match Score: 0.625 / 1.000

    Why this song?
      - Genre match
------------------------------------------------------------

#2  Focus Flow by LoRoom
    Genre: lofi | Mood: focused | Tempo: 80 BPM
    Match Score: 0.620 / 1.000

    Why this song?
      - Genre match
------------------------------------------------------------

#3  Library Rain by Paper Lanterns
    Genre: lofi | Mood: chill | Tempo: 72 BPM
    Match Score: 0.607 / 1.000

    Why this song?
      - Genre match
------------------------------------------------------------

#4  Island Vibes by Reggae Kings
    Genre: reggae | Mood: relaxed | Tempo: 100 BPM
    Match Score: 0.415 / 1.000

    Why this song?
      - Mood match
------------------------------------------------------------

#5  Coffee Shop Stories by Slow Stereo
    Genre: jazz | Mood: relaxed | Tempo: 90 BPM
    Match Score: 0.362 / 1.000

    Why this song?
      - Mood match
```

**Edge Case 6: Niche Genre (Classical Only)**
```
============================================================
  EDGE CASE 6: Niche Genre (Classical Only) -- Top 5 Results
============================================================

#1  Nocturne in D Minor by Classical Ensemble
    Genre: classical | Mood: melancholic | Tempo: 70 BPM
    Match Score: 1.000 / 1.000

    Why this song?
      - Genre match
      - Mood match
      - Energy match (1.00)
------------------------------------------------------------

#2  Heartbreak Road by Country Soul
    Genre: country | Mood: melancholic | Tempo: 92 BPM
    Match Score: 0.458 / 1.000

    Why this song?
      - Mood match
      - Energy match (0.83)
------------------------------------------------------------

#3  Spacewalk Thoughts by Orbit Bloom
    Genre: ambient | Mood: chill | Tempo: 60 BPM
    Match Score: 0.242 / 1.000

    Why this song?
      - Energy match (0.97)
------------------------------------------------------------

#4  Library Rain by Paper Lanterns
    Genre: lofi | Mood: chill | Tempo: 72 BPM
    Match Score: 0.225 / 1.000

    Why this song?
      - Energy match (0.90)
------------------------------------------------------------

#5  Coffee Shop Stories by Slow Stereo
    Genre: jazz | Mood: relaxed | Tempo: 90 BPM
    Match Score: 0.220 / 1.000

    Why this song?
      - Energy match (0.88)
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



