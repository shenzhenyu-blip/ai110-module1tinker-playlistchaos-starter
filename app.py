import streamlit as st

from playlist_logic import (
    classify_song,
    search_songs,
    calculate_stats,
    lucky_pick,
    normalize_song,
)


st.set_page_config(page_title="Playlist Chaos", page_icon="🎧", layout="wide")

DEFAULT_PROFILE = {
    "favorite_genre": "pop",
    "hype_min_energy": 7,
    "chill_max_energy": 3,
}

SAMPLE_SONGS = [
    {"title": "Thunderstruck", "artist": "AC/DC", "genre": "Rock", "energy": 6},
    {"title": "Sleep Waves", "artist": "Calm Artist", "genre": "Ambient", "energy": 5},
    {"title": "Regular Song", "artist": "Some Artist", "genre": "Pop", "energy": 5},
    {"title": "Party Night", "artist": "DJ Test", "genre": "Party", "energy": 4},
    {"title": "Lofi Rain", "artist": "Chill Person", "genre": "Hip Hop", "energy": 6},
    {"title": "Loud Song", "artist": "Random", "genre": "Jazz", "energy": 8},
]


def initialize_state():
    """Create Streamlit session state values used by the app."""
    if "profile" not in st.session_state:
        st.session_state.profile = DEFAULT_PROFILE.copy()

    if "playlists" not in st.session_state:
        st.session_state.playlists = {
            "Hype": [],
            "Chill": [],
            "Mixed": [],
        }


def add_song_to_playlist(song):
    """Normalize, classify, and store a song."""
    cleaned_song = normalize_song(song)
    mood = classify_song(cleaned_song, st.session_state.profile)
    st.session_state.playlists[mood].append(cleaned_song)
    return cleaned_song, mood


def get_all_songs():
    """Return every song from all playlists."""
    songs = []
    for playlist in st.session_state.playlists.values():
        songs.extend(playlist)
    return songs


def display_playlist(name, songs):
    """Render one playlist section."""
    st.subheader(f"{name} Playlist")

    if not songs:
        st.caption("No songs yet.")
        return

    for song in songs:
        st.write(
            f"🎵 **{song['title']}** — {song['artist']} "
            f"({song['genre']}, energy {song['energy']})"
        )


initialize_state()

st.title("🎧 Playlist Chaos")
st.write(
    "Debugged version: songs are normalized, classified into Hype/Chill/Mixed, "
    "search uses case-insensitive partial matching, stats are calculated from unique songs, "
    "and Lucky Pick respects the selected playlist."
)

with st.sidebar:
    st.header("Profile Settings")

    st.session_state.profile["favorite_genre"] = st.text_input(
        "Favorite genre",
        value=st.session_state.profile["favorite_genre"],
        help="Songs with this exact genre are classified as Hype.",
    )

    st.session_state.profile["hype_min_energy"] = st.slider(
        "Hype minimum energy",
        min_value=1,
        max_value=10,
        value=int(st.session_state.profile["hype_min_energy"]),
    )

    st.session_state.profile["chill_max_energy"] = st.slider(
        "Chill maximum energy",
        min_value=1,
        max_value=10,
        value=int(st.session_state.profile["chill_max_energy"]),
    )

    st.divider()

    if st.button("Load sample songs"):
        for sample_song in SAMPLE_SONGS:
            add_song_to_playlist(sample_song)
        st.success("Sample songs loaded.")

    if st.button("Reset playlists"):
        st.session_state.playlists = {
            "Hype": [],
            "Chill": [],
            "Mixed": [],
        }
        st.success("Playlists reset.")


left_col, right_col = st.columns([1, 1])

with left_col:
    st.header("Add a Song")

    with st.form("song_form", clear_on_submit=True):
        title = st.text_input("Title")
        artist = st.text_input("Artist")
        genre = st.text_input("Genre")
        energy = st.slider("Energy", min_value=1, max_value=10, value=5)

        submitted = st.form_submit_button("Add Song")

    if submitted:
        if not title.strip() or not artist.strip() or not genre.strip():
            st.warning("Please enter a title, artist, and genre.")
        else:
            song, mood = add_song_to_playlist(
                {
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "energy": energy,
                }
            )
            st.success(f"Added '{song['title']}' to the {mood} playlist.")

    st.header("Lucky Pick")
    pick_mode = st.selectbox("Choose a playlist", ["Any", "Hype", "Chill", "Mixed"])

    if st.button("Pick a song"):
        picked_song = lucky_pick(st.session_state.playlists, pick_mode)

        if picked_song is None:
            st.warning("No songs available for this selection.")
        else:
            st.info(
                f"🎲 Lucky Pick: **{picked_song['title']}** by {picked_song['artist']} "
                f"from {pick_mode if pick_mode != 'Any' else 'all playlists'}."
            )


with right_col:
    st.header("Playlist Statistics")
    stats = calculate_stats(st.session_state.playlists)

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("Total Songs", stats["total_songs"])
    metric_col_2.metric("Average Energy", stats["average_energy"])
    metric_col_3.metric("Hype Ratio", f"{stats['hype_ratio']}%")

    st.header("Search")
    search_field = st.selectbox("Search field", ["title", "artist", "genre"])
    query = st.text_input("Search query")

    results = search_songs(get_all_songs(), query, search_field)

    if query.strip():
        st.write(f"Found {len(results)} result(s).")
        for song in results:
            st.write(
                f"🔎 **{song['title']}** — {song['artist']} "
                f"({song['genre']}, energy {song['energy']})"
            )


st.divider()
st.header("Playlists")

hype_col, chill_col, mixed_col = st.columns(3)

with hype_col:
    display_playlist("Hype", st.session_state.playlists["Hype"])

with chill_col:
    display_playlist("Chill", st.session_state.playlists["Chill"])

with mixed_col:
    display_playlist("Mixed", st.session_state.playlists["Mixed"])
