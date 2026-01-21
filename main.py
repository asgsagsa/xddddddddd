import pylast
import time
import warnings
from datetime import datetime, timedelta, timezone

warnings.filterwarnings("ignore")

ART = timezone(timedelta(hours=-3))

API_KEY = '49452d64180d104ac22e571cc5d0c0f0'
API_SECRET = '4ff0c076a69291d506c761b7dfecd083'
USERNAME = 'l0b'
PASSWORD_HASH = pylast.md5('lukrobv1583_')

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=USERNAME,
    password_hash=PASSWORD_HASH
)

TARGET = 3000          
BATCH_DELAY = 2.5     

def esperar_hasta_15():
    ahora = datetime.now(ART)
    hoy_15 = ahora.replace(hour=15, minute=0, second=0, microsecond=0)

    if ahora >= hoy_15:
        hoy_15 += timedelta(days=1)

    segundos = (hoy_15 - ahora).total_seconds()
    print(f"> Esperando hasta las 15:00 ART ({int(segundos)}s)")
    time.sleep(segundos)

def scrobble_batch(batch, start_number, max_retries=3):
    timestamp = int(time.time())
    scrobbles = []

    for i, track_data in enumerate(batch):
        scrobbles.append({
            'artist': track_data['artist'],
            'title': track_data['track'],
            'album': track_data['album'],
            'timestamp': timestamp + i
        })

    for attempt in range(max_retries):
        try:
            network.scrobble_many(scrobbles)
            for i, t in enumerate(scrobbles):
                print(f"[{start_number + i}] > {t['artist']} - {t['title']}")
            return len(scrobbles)
        except pylast.WSError as e:
            print(f"> Error Last.fm: {e}")
            time.sleep(10)
        except pylast.NetworkError:
            print("> Network error")
            time.sleep(5)

    return 0


canciones = [
    {"artist": "neva pray", "track": "tuyo", "album": "tuyo"},
    {"artist": "neva pray", "track": "tuyo", "album": "tuyo"},
    {"artist": "neva pray", "track": "tuyo", "album": "tuyo"},
    {"artist": "neva pray", "track": "tuyo", "album": "tuyo"},


]

while True:
    esperar_hasta_15()

    print("▶ Iniciando scrobbleo diario (3K exactos)")
    sent_today = 0
    count = 1
    index = 0

    while sent_today < TARGET:
        remaining = TARGET - sent_today
        batch = canciones[index:index+2]

        if not batch:
            index = 0
            continue

        batch = batch[:remaining]

        sent = scrobble_batch(batch, count)
        sent_today += sent
        count += sent
        index += 2

        print(f"> Total hoy: {sent_today}/{TARGET}")

        if sent_today >= TARGET:
            break

        time.sleep(BATCH_DELAY)

    print("✔ 3.000 scrobbles completados. Esperando mañana…")
