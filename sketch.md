# Music Recommender Data Flow

## Pipeline: Input → Process → Output

```mermaid
graph TD
    A["INPUT: User Preferences<br/>(favorite_genre, favorite_mood,<br/>target_energy, likes_acoustic)"] --> B["Load CSV<br/>(songs.csv)"]
    B --> C["Song Data<br/>(4 songs loaded)"]
    
    C --> D{"THE LOOP:<br/>Score Each Song"}
    
    D --> E1["Song 1<br/>Sunrise City"]
    D --> E2["Song 2<br/>Midnight Coding"]
    D --> E3["Song 3<br/>Storm Runner"]
    D --> E4["Song 4<br/>Library Rain"]
    
    E1 --> F["Scoring Logic Applied:<br/>✓ Genre match +2.0<br/>✓ Mood match +1.0<br/>✓ Energy similarity 0.0-1.0<br/>= Total Score"]
    E2 --> F
    E3 --> F
    E4 --> F
    
    F --> G["Scored Results<br/>Song: Score, Reasons<br/>Example:<br/>Sunrise City: 3.82<br/>Midnight Coding: 0.58<br/>..."]
    
    G --> H["Sort by Score<br/>Descending"]
    
    H --> I["OUTPUT: Top K Rankings<br/>(k=5 recommendations)"]
    
    I --> J["#1 Sunrise City - 3.82<br/>#2 Midnight Coding - 0.58<br/>#3 Storm Runner - 0.45<br/>..."]
    
    style A fill:#e1f5ff
    style I fill:#c8e6c9
    style D fill:#fff9c4
    style F fill:#fff9c4
```

## 3-Stage Pipeline

| Stage | What Happens | Data |
|-------|--------------|------|
| **INPUT** | Capture user's taste preferences | Genre, mood, energy target, acoustic preference |
| **PROCESS** | Loop through every song in CSV, score each one against user prefs | Each song gets scored: genre match (+2), mood match (+1), energy similarity (0-1) |
| **OUTPUT** | Sort by score, return top K results | Ranked list with explanations why each song matched |

## Key Logic in `score_song()`
- Compares each song's attributes against user preferences
- Accumulates points for matches
- Returns (score, reasons) tuple
- Then `recommend_songs()` sorts all scores and returns top K
