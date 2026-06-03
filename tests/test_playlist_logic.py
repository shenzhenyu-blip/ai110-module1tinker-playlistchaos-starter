from playlist_logic import classify_song, search_songs, calculate_stats, lucky_pick, normalize_song


PROFILE = {
    "favorite_genre": "pop",
    "hype_min_energy": 7,
    "chill_max_energy": 3,
}


def test_classification_rules():
    assert classify_song({"title": "Loud", "artist": "A", "genre": "Jazz", "energy": 8}, PROFILE) == "Hype"
    assert classify_song({"title": "Party Night", "artist": "A", "genre": "Party", "energy": 4}, PROFILE) == "Hype"
    assert classify_song({"title": "Sleep Waves", "artist": "A", "genre": "Ambient", "energy": 5}, PROFILE) == "Chill"
    assert classify_song({"title": "Regular Song", "artist": "A", "genre": "Folk", "energy": 5}, PROFILE) == "Mixed"


def test_search_case_insensitive_partial_match():
    songs = [
        {"title": "Thunderstruck", "artist": "AC/DC", "genre": "Rock", "energy": 6},
        {"title": "Regular Song", "artist": "Some Artist", "genre": "Pop", "energy": 5},
    ]

    results = search_songs(songs, "ac", "artist")
    assert len(results) == 1
    assert results[0]["artist"] == "AC/DC"


def test_stats_unique_count_and_average():
    song = {"title": "Same Song", "artist": "Same Artist", "genre": "Rock", "energy": 8}
    playlists = {
        "Hype": [song],
        "Chill": [song],
        "Mixed": [],
    }

    stats = calculate_stats(playlists)

    assert stats["total_songs"] == 1
    assert stats["average_energy"] == 8
    assert stats["hype_ratio"] == 100


def test_lucky_pick_respects_mode():
    playlists = {
        "Hype": [{"title": "Hype Song", "artist": "A", "genre": "Rock", "energy": 8}],
        "Chill": [{"title": "Chill Song", "artist": "B", "genre": "Ambient", "energy": 2}],
        "Mixed": [{"title": "Mixed Song", "artist": "C", "genre": "Folk", "energy": 5}],
    }

    for _ in range(10):
        assert lucky_pick(playlists, "Hype")["title"] == "Hype Song"
        assert lucky_pick(playlists, "Chill")["title"] == "Chill Song"

    assert lucky_pick({"Hype": [], "Chill": [], "Mixed": []}, "Any") is None


def test_normalization():
    song = normalize_song(
        {
            "title": "  Test Song  ",
            "artist": "  Artist Name  ",
            "genre": "  Rock  ",
            "energy": "7",
        }
    )

    assert song["title"] == "Test Song"
    assert song["artist"] == "artist name"
    assert song["genre"] == "rock"
    assert song["energy"] == 7
