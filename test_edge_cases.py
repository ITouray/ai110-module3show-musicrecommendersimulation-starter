"""
Test edge case profiles to reveal algorithm weaknesses and unexpected behavior.
"""

from src.recommender import load_songs, recommend_songs


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
    # EDGE CASE 1: Non-existent Genre (Forces Mood/Energy Only)
    # =========================================================
    nonexistent_genre = {
        "favorite_genre": "reggaeton",  # Not in dataset
        "favorite_mood": "energetic",
        "target_energy": 0.85,
    }

    # =========================================================
    # EDGE CASE 2: Non-existent Mood (Forces Genre/Energy Only)
    # =========================================================
    nonexistent_mood = {
        "favorite_genre": "jazz",
        "favorite_mood": "transcendent",  # Not in dataset
        "target_energy": 0.5,
    }

    # =========================================================
    # EDGE CASE 3: Extremely Low Energy (Seeks Quietest Songs)
    # =========================================================
    ultra_low_energy = {
        "favorite_genre": "classical",
        "favorite_mood": "melancholic",
        "target_energy": 0.1,
    }

    # =========================================================
    # EDGE CASE 4: Extremely High Energy (Seeks Loudest Songs)
    # =========================================================
    ultra_high_energy = {
        "favorite_genre": "metal",
        "favorite_mood": "aggressive",
        "target_energy": 0.99,
    }

    # =========================================================
    # EDGE CASE 5: Sleepy + Energetic Conflict (Sleep Playlist But Wants to Dance)
    # =========================================================
    sleep_dance_conflict = {
        "favorite_genre": "lofi",
        "favorite_mood": "relaxed",
        "target_energy": 0.92,  # High energy but wants relaxed mood
    }

    # =========================================================
    # EDGE CASE 6: All-or-Nothing Genre (Only One Song Matches)
    # =========================================================
    niche_genre = {
        "favorite_genre": "classical",
        "favorite_mood": "melancholic",
        "target_energy": 0.25,
    }

    # Run all edge case tests
    test_profile(songs, nonexistent_genre, "EDGE CASE 1: Non-existent Genre (Reggaeton)", k=5)
    test_profile(songs, nonexistent_mood, "EDGE CASE 2: Non-existent Mood (Transcendent)", k=5)
    test_profile(songs, ultra_low_energy, "EDGE CASE 3: Extremely Low Energy (0.1)", k=5)
    test_profile(songs, ultra_high_energy, "EDGE CASE 4: Extremely High Energy (0.99)", k=5)
    test_profile(songs, sleep_dance_conflict, "EDGE CASE 5: Sleep/Dance Conflict (Lofi + 0.92 Energy)", k=5)
    test_profile(songs, niche_genre, "EDGE CASE 6: Niche Genre (Classical Only)", k=5)


if __name__ == "__main__":
    main()
