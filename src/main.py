"""
main.py
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(recommendations: list, k: int, profile_name: str = "") -> None:
    """Prints the recommendation results in a clean, readable layout."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {profile_name} -- Top {k} Results".center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']} | Tempo: {int(song['tempo_bpm'])} BPM")
        print(f"    Match Score: {score:.3f} / 1.000")
        print()
        print("    Why this song?")
        # explanation is reasons joined by " | " — split to print each on its own line
        for reason in explanation.split(" | "):
            print(f"      - {reason}")
        print("-" * width)

def test_profile(songs: list, user_prefs: dict, profile_name: str, k: int = 5) -> None:
    """Test a single user profile and print recommendations."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print_recommendations(recommendations, k, profile_name)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # =========================================================
    # PROFILE 1: High-Energy Pop (from "Sunrise City")
    # =========================================================
    pop_happy = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.82,
        "target_tempo": 118,
        "target_danceability": 0.79,
        "seed_id": 1,  # Sunrise City
    }

    # =========================================================
    # PROFILE 2: Chill Lofi (from "Midnight Coding")
    # =========================================================
    chill_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.42,
        "target_tempo": 78,
        "target_danceability": 0.62,
        "seed_id": 2,  # Midnight Coding
    }

    # =========================================================
    # PROFILE 3: Deep Intense Rock (from "Storm Runner")
    # =========================================================
    intense_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.91,
        "target_tempo": 152,
        "target_danceability": 0.66,
        "seed_id": 3,  # Storm Runner
    }

    # =========================================================
    # PROFILE 4: Sad/Angry Metal (Edge Case)
    # =========================================================
    sad_metal = {
        "favorite_genre": "metal",
        "favorite_mood": "aggressive",
        "target_energy": 0.95,
        "target_tempo": 175,
        "target_danceability": 0.45,
        "seed_id": 11,  # Thunder Beast
    }

    # =========================================================
    # PROFILE 5: Contradictory Preferences (Stress Test)
    # - High energy but sad mood (does this exist in dataset?)
    # =========================================================
    contradictory = {
        "favorite_genre": "electronic",
        "favorite_mood": "sad",
        "target_energy": 0.89,          # High energy
        "target_tempo": 126,
        "target_danceability": 0.91,
        "seed_id": 16,                  # Club Paradox (euphoric, not sad)
    }

    # Run all profile tests
    test_profile(songs, pop_happy, "PROFILE 1: High-Energy Pop", k=5)
    test_profile(songs, chill_lofi, "PROFILE 2: Chill Lofi", k=5)
    test_profile(songs, intense_rock, "PROFILE 3: Deep Intense Rock", k=5)
    test_profile(songs, sad_metal, "PROFILE 4: Sad/Angry Metal", k=5)
    test_profile(songs, contradictory, "PROFILE 5: Contradictory (High Energy + Sad Mood)", k=5)


if __name__ == "__main__":
    main()