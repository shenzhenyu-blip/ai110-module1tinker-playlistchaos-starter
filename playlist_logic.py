import random


HYPE_KEYWORDS = {"rock", "punk", "party"}
CHILL_KEYWORDS = {"lofi", "ambient", "sleep"}


def normalize_text(value):
    """Trim whitespace and convert text to lowercase for reliable comparisons."""
    return str(value).strip().lower()


def normalize_song(song):
    """
    Return a cleaned song dictionary.

    Titles keep their original capitalization for display.
    Artists and genres are lowercased because they are mainly used for comparison.
    """
    return {
        "title": str(song.get("title", "")).strip(),
        "artist": normalize_text(song.get("artist", "")),
        "genre": normalize_text(song.get("genre", "")),
        "energy": int(song.get("energy", 0)),
    }


def classify_song(song, profile):
    """
    Classify a song as Hype, Chill, or Mixed.

    Hype rules:
    - energy is greater than or equal to hype_min_energy
    - genre matches the user's favorite genre
    - genre contains a hype keyword such as rock, punk, or party

    Chill rules:
    - energy is less than or equal to chill_max_energy
    - title contains a chill keyword such as lofi, ambient, or sleep

    If a song matches both Hype and Chill, Hype wins because Hype is checked first.
    """
    cleaned_song = normalize_song(song)

    favorite_genre = normalize_text(profile.get("favorite_genre", ""))
    hype_min_energy = int(profile.get("hype_min_energy", 7))
    chill_max_energy = int(profile.get("chill_max_energy", 3))

    title = normalize_text(cleaned_song["title"])
    genre = cleaned_song["genre"]
    energy = cleaned_song["energy"]

    is_hype = (
        energy >= hype_min_energy
        or genre == favorite_genre
        or any(keyword in genre for keyword in HYPE_KEYWORDS)
    )

    is_chill = (
        energy <= chill_max_energy
        or any(keyword in title for keyword in CHILL_KEYWORDS)
    )

    if is_hype:
        return "Hype"

    if is_chill:
        return "Chill"

    return "Mixed"


def search_songs(songs, query, field):
    """
    Search songs with case-insensitive partial matching.

    Example:
    Searching "AC" in the artist field matches "AC/DC".
    """
    normalized_query = normalize_text(query)

    if not normalized_query:
        return songs

    matching_songs = []

    for song in songs:
        field_value = normalize_text(song.get(field, ""))
        if normalized_query in field_value:
            matching_songs.append(song)

    return matching_songs


def _unique_song_key(song):
    """Create a stable key to prevent duplicate songs from being counted twice."""
    cleaned_song = normalize_song(song)
    return (
        normalize_text(cleaned_song["title"]),
        cleaned_song["artist"],
        cleaned_song["genre"],
    )


def get_unique_songs(playlists):
    """Return unique songs from all playlist categories."""
    unique_songs = {}

    for playlist in playlists.values():
        for song in playlist:
            unique_songs[_unique_song_key(song)] = normalize_song(song)

    return list(unique_songs.values())


def calculate_stats(playlists):
    """
    Calculate total unique songs, average energy, and hype ratio.

    Total Songs:
    Unique count across all playlists.

    Average Energy:
    Mathematical average energy across unique songs.

    Hype Ratio:
    Percentage of Hype songs compared with total unique songs.
    """
    unique_songs = get_unique_songs(playlists)
    total_songs = len(unique_songs)

    if total_songs == 0:
        return {
            "total_songs": 0,
            "average_energy": 0,
            "hype_ratio": 0,
        }

    average_energy = sum(song["energy"] for song in unique_songs) / total_songs

    unique_hype_songs = {
        _unique_song_key(song)
        for song in playlists.get("Hype", [])
    }
    hype_ratio = len(unique_hype_songs) / total_songs * 100

    return {
        "total_songs": total_songs,
        "average_energy": round(average_energy, 2),
        "hype_ratio": round(hype_ratio, 2),
    }


def lucky_pick(playlists, mode):
    """
    Pick a random song.

    Hype, Chill, and Mixed only draw from their selected playlist.
    Any draws from the combined Hype, Chill, and Mixed playlists.
    """
    if mode == "Any":
        song_pool = (
            playlists.get("Hype", [])
            + playlists.get("Chill", [])
            + playlists.get("Mixed", [])
        )
    else:
        song_pool = playlists.get(mode, [])

    if not song_pool:
        return None

    return random.choice(song_pool)
