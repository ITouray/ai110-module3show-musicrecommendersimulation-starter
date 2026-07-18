from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialize recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs and return top k recommendations for the user."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song is recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    print(f"  ✓ Loaded {len(songs)} songs")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    
    Scoring Logic:
    - +2.0 points for genre match
    - +1.0 point for mood match
    - Energy similarity: 0.0 to 1.0 based on how close energy is to target
    
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []
    
    # Genre match: +2.0 points
    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        score += 2.0
        reasons.append("Genre match")
    
    # Mood match: +1.0 point
    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        score += 1.0
        reasons.append("Mood match")
    
    # Energy similarity: 0.0 to 1.0 (max score when energy matches target exactly)
    energy_diff = abs(float(song['energy']) - user_prefs['target_energy'])
    energy_similarity = max(0.0, 1.0 - energy_diff)
    score += energy_similarity
    
    # Only mention energy if it's a meaningful match
    if energy_similarity >= 0.7:
        reasons.append(f"Energy match ({energy_similarity:.2f})")
    
    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    
    Scores all songs, ranks by score, and returns top k results.
    Expected return format: (song_dict, normalized_score, explanation)
    
    Required by src/main.py
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))
    
    # Sort by score in descending order
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k with normalized scores and explanations
    # Max possible score is 2.0 (genre) + 1.0 (mood) + 1.0 (energy) = 4.0
    results = []
    for song, score, reasons in scored_songs[:k]:
        explanation = " | ".join(reasons) if reasons else "No strong match"
        normalized_score = min(score / 4.0, 1.0)  # Normalize to 0.0-1.0 range
        results.append((song, normalized_score, explanation))
    
    return results
