import streamlit as st
import requests
import html

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Music Search",
    page_icon="🎵",
    layout="centered"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 17px;
    margin-bottom: 35px;
}

.search-title {
    font-size: 25px;
    font-weight: 600;
    margin-bottom: 8px;
}

.result-card {
    background: #f8f9fc;
    border: 1px solid #e3e5eb;
    border-radius: 16px;
    padding: 18px;
    margin-top: 10px;
    margin-bottom: 25px;
}

.song-title {
    font-size: 25px;
    font-weight: 700;
    margin-bottom: 12px;
}

.info {
    font-size: 16px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #888;
    font-size: 13px;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎵 Music Search</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Search for a song and explore its information</div>',
    unsafe_allow_html=True
)

# =========================================================
# SEARCH
# =========================================================

st.markdown(
    '<div class="search-title">🔎 Search for a Song</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([5, 1])

with col1:
    song_name = st.text_input(
        "Song name",
        placeholder="e.g. Shape of You",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button(
        "🔍 Search",
        use_container_width=True
    )

# =========================================================
# SEARCH API
# =========================================================

if search_button:

    if song_name.strip() == "":
        st.warning("⚠️ Please enter a song name.")

    else:

        url = "https://itunes.apple.com/search"

        params = {
            "term": song_name,
            "media": "music",
            "entity": "song",
            "limit": 5,
            "country": "IN"
        }

        try:

            with st.spinner("🔎 Searching..."):

                response = requests.get(
                    url,
                    params=params,
                    timeout=15
                )

                response.raise_for_status()

                data = response.json()

                results = data.get("results", [])

            # =================================================
            # RESULTS
            # =================================================

            if results:

                st.success(
                    f"🎵 Found {len(results)} songs"
                )

                st.markdown("### 🎧 Search Results")

                for i, song in enumerate(results):

                    track_name = song.get(
                        "trackName",
                        "Unknown Song"
                    )

                    artist_name = song.get(
                        "artistName",
                        "Unknown Artist"
                    )

                    album_name = song.get(
                        "collectionName",
                        "Unknown Album"
                    )

                    genre = song.get(
                        "primaryGenreName",
                        "Unknown"
                    )

                    release_date = song.get(
                        "releaseDate",
                        "Unknown"
                    )

                    if release_date != "Unknown":
                        release_date = release_date[:10]

                    artwork = song.get("artworkUrl100")

                    preview_url = song.get("previewUrl")

                    track_url = song.get("trackViewUrl")

                    # Make artwork larger
                    if artwork:
                        artwork = artwork.replace(
                            "100x100",
                            "300x300"
                        )

                    # =================================================
                    # RESULT CARD
                    # =================================================

                    st.markdown(
                        '<div class="result-card">',
                        unsafe_allow_html=True
                    )

                    image_col, info_col = st.columns(
                        [1, 2.5]
                    )

                    # Artwork
                    with image_col:

                        if artwork:
                            st.image(
                                artwork,
                                width=220
                            )
                        else:
                            st.write("🖼️ No artwork")

                    # Information
                    with info_col:

                        st.markdown(
                            f'<div class="song-title">'
                            f'🎵 {html.escape(track_name)}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"""
                            <div class="info">

                            👤 <b>Artist:</b>
                            {html.escape(artist_name)}

                            <br>

                            💿 <b>Album:</b>
                            {html.escape(album_name)}

                            <br>

                            📅 <b>Release Date:</b>
                            {html.escape(release_date)}

                            <br>

                            🎼 <b>Genre:</b>
                            {html.escape(genre)}

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                    # =================================================
                    # PREVIEW
                    # =================================================

                    if preview_url:

                        st.markdown("#### ▶️ Song Preview")

                        st.audio(
                            preview_url,
                            format="audio/mp4"
                        )

                        # =================================================
                        # SPEED
                        # =================================================

                        speed = st.selectbox(
                            "⏩ Playback Speed",
                            [
                                0.5,
                                0.75,
                                1.0,
                                1.25,
                                1.5,
                                2.0
                            ],
                            index=2,
                            key=f"speed_{i}"
                        )

                        st.markdown(
                            f"""
                            <script>
                            setTimeout(function() {{
                                const audios =
                                    window.parent.document
                                    .querySelectorAll('audio');

                                if (audios.length > 0) {{
                                    audios[audios.length - 1]
                                    .playbackRate = {speed};
                                }}
                            }}, 500);
                            </script>
                            """,
                            unsafe_allow_html=True
                        )

                        # =================================================
                        # DOWNLOAD
                        # =================================================

                        try:

                            audio_response = requests.get(
                                preview_url,
                                timeout=15
                            )

                            if audio_response.status_code == 200:

                                safe_filename = (
                                    track_name
                                    .replace("/", "_")
                                    .replace("\\", "_")
                                    .replace(":", "_")
                                )

                                st.download_button(
                                    "⬇️ Download Preview",
                                    data=audio_response.content,
                                    file_name=f"{safe_filename}.m4a",
                                    mime="audio/mp4",
                                    key=f"download_{i}",
                                    use_container_width=True
                                )

                        except requests.RequestException:

                            st.warning(
                                "⚠️ Download unavailable."
                            )

                    else:

                        st.info(
                            "🎧 No preview is available for this song."
                        )

                    # =================================================
                    # OPEN SONG
                    # =================================================

                    if track_url:

                        st.link_button(
                            "🌐 Open Song",
                            track_url,
                            use_container_width=True
                        )

            else:

                st.warning(
                    "😕 No songs found. Try another song name."
                )

        except requests.RequestException:

            st.error(
                "❌ Unable to connect to the music service."
            )

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🎵 Music Search & Information System
        <br>
        Built using Python, Streamlit & Music API
    </div>
    """,
    unsafe_allow_html=True
)