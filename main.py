import pylast
import time
import warnings
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

warnings.filterwarnings("ignore")

ART = timezone(timedelta(hours=-3))
STATE_FILE = Path("/data/state.json")

API_KEY = "835ee3c2ba3d6d4e114989ac855179db"
API_SECRET = "db646e5321c3c471312bea47f4d93ce2"
USERNAME = "l0b"
PASSWORD_HASH = pylast.md5("lukrobv1583_")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=USERNAME,
    password_hash=PASSWORD_HASH
)

TARGET = 3000
SCROBBLE_DELAY = 2.6

ARTISTAS = [
    {"artist": "moneynumbdapain", "track": "carrera", "album": "1IVINGSUFFER"},
    {"artist": "naxowo", "track": "nicki minaj", "album": "nicki minaj"},
    {"artist": "1oneam", "track": "Vogue", "album": "Vogue"},
    {"artist": "unixzo", "track": "fashion whore", "album": "fashion whore"},
    {"artist": "zatru", "track": "all i wunna", "album": "all i wunna"},
    {"artist": "slattuhs", "track": "i will kill u w/ my fukin bare hands @fuckkekx", "album": "i will kill u w/ my fukin bare hands @fuckkekx"},
    {"artist": "War6aw", "track": "on my soul", "album": "on my soul"},
    {"artist": "jaydes", "track": "rose", "album": "ghetto cupid"},
    {"artist": "Lucy Bedroque", "track": "TAKE ME BACK", "album": "SISTERHOOD"},
    {"artist": "bleood", "track": "bugs are crawling under your skin", "album": "bugs are crawling under your skin"},
    {"artist": "neva pray", "track": "tuyo", "album": "tuyo"},
    {"artist": "suban", "track": "face Melting // she Love it", "album": "face Melting // she Love it"},
    {"artist": "xaviersobased", "track": "in the yo", "album": "in the yo"},
    {"artist": "yuke", "track": "iam goin", "album": "ian goin"},
    {"artist": "sexadlibs", "track": "my tongue tie d im trauma Tized", "album": "my tongue tie d im trauma Tized"},
    {"artist": "Aeter", "track": "boyfriend", "album": "boyfriend"},
    {"artist": "Nightlight", "track": "nada", "album": "YFC"},
]

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "artist_index": 0,
        "count": 0,
        "date": str(datetime.now(ART).date())
    }

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state))

def esperar_hasta_15():
    ahora = datetime.now(ART)
    hoy_15 = ahora.replace(hour=15, minute=0, second=0, microsecond=0)
    if ahora >= hoy_15:
        hoy_15 += timedelta(days=1)
    time.sleep((hoy_15 - ahora).total_seconds())

def scrobble(track, n):
    try:
        network.scrobble(
            artist=track["artist"],
            title=track["track"],
            album=track["album"],
            timestamp=int(time.time())
        )
        print(f"[{n}] {track['artist']} - {track['track']}")
        return True
    except pylast.WSError as e:
        if "Rate" in str(e) or "29" in str(e):
            print("🚫 RATE LIMIT — guardo estado y paro")
            return None
        print("Error:", e)
        return False

while True:
    esperar_hasta_15()

    state = load_state()
    hoy = str(datetime.now(ART).date())

    if state["date"] != hoy:
        state["date"] = hoy
        state["count"] = 0

    artist_index = state["artist_index"] % len(ARTISTAS)
    track = ARTISTAS[artist_index]

    print(f"\n🎵 Artista: {track['artist']} ({state['count']}/{TARGET})")

    while state["count"] < TARGET:
        res = scrobble(track, state["count"] + 1)

        if res is None:
            save_state(state)
            break

        if res:
            state["count"] += 1
            save_state(state)

        time.sleep(SCROBBLE_DELAY)

    if state["count"] >= TARGET:
        print(f"✔ {track['artist']} completado")
        state["artist_index"] += 1
        state["count"] = 0
        save_state(state)
