import pylast
import time
import warnings
import json
import httpx
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

warnings.filterwarnings("ignore")

ART = timezone(timedelta(hours=-3))
STATE_FILE = Path("/data/state.json")

API_KEY = "49452d64180d104ac22e571cc5d0c0f0"
API_SECRET = "4ff0c076a69291d506c761b7dfecd083"
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
        {"artist": "vampireosamagang666", "track": "barbie", "album": "barbie"},
        {"artist": "bleood", "track": "bugs are crawling under your skin", "album": "bugs are crawling under your skin"},
    {"artist": "neva pray", "track": "tuyo", "album": "tuyo"},
        {"artist": "sexadlibs", "track": "my tongue tie d im trauma Tized", "album": "my tongue tie d im trauma Tized"},
 {"artist": "unixzo", "track": "fashion whore", "album": "fashion whore"},
    {"artist": "zatru", "track": "all i wunna", "album": "all i wunna"},
    {"artist": "slattuhs", "track": "i will kill u w/ my fukin bare hands @fuckkekx", "album": "i will kill u w/ my fukin bare hands @fuckkekx"},
    {"artist": "War6aw", "track": "on my soul", "album": "on my soul"},
    {"artist": "jaydes", "track": "rose", "album": "ghetto cupid"},
    {"artist": "moneynumbdapain", "track": "carrera", "album": "1IVINGSUFFER"},
    {"artist": "naxowo", "track": "nicki minaj", "album": "nicki minaj"},
    {"artist": "1oneam", "track": "Vogue", "album": "Vogue"},
    {"artist": "Bladee", "track": "Be Nice 2 Me", "album": "Icedancer"},
    {"artist": "Lucy Bedroque", "track": "TAKE ME BACK", "album": "SISTERHOOD"},
    {"artist": "suban", "track": "face Melting // she Love it", "album": "face Melting // she Love it"},
    {"artist": "xaviersobased", "track": "in the yo", "album": "in the yo"},
    {"artist": "yuke", "track": "iam goin", "album": "ian goin"},
    {"artist": "Aeter", "track": "boyfriend", "album": "boyfriend"},
    {"artist": "Nightlight", "track": "nada", "album": "YFC"},
]

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "artist_index": 0,
        "count": 0,
        "date": ""
    }

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state))

def esperar_hasta_15():
    ahora = datetime.now(ART)
    hoy_15 = ahora.replace(hour=15, minute=0, second=0, microsecond=0)
    if ahora >= hoy_15:
        hoy_15 += timedelta(days=1)
    tiempo = (hoy_15 - ahora).total_seconds()
    print(f"⏳ Esperando hasta las 15:00 ({int(tiempo)}s)")
    time.sleep(tiempo)

def scrobble(track, n, retries=4):
    for attempt in range(retries):
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

            print(f"❌ pylast error ({attempt+1}/{retries}): {e}")
            time.sleep(5)

        except httpx.ReadTimeout:
            print(f"⏱ TIMEOUT ({attempt+1}/{retries}) — reintentando…")
            time.sleep(5 + random.uniform(0, 3))

        except Exception as e:
            print(f"💥 Error raro ({attempt+1}/{retries}): {e}")
            time.sleep(5)

    print("⚠️ Falló después de varios intentos, sigo")
    return False

print("🚀 Scrobbler diario iniciado")

while True:
    esperar_hasta_15()

    state = load_state()
    hoy = str(datetime.now(ART).date())

    if state["date"] != hoy:
        state["date"] = hoy
        state["count"] = 0

    track = ARTISTAS[state["artist_index"] % len(ARTISTAS)]
    print(f"🎵 Artista del día: {track['artist']}")

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
