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
BATCH_DELAY = 3.0

ARTISTAS = [
         {
        "artist": "Nightlight",
        "track": "nada",
        "album": "YFC"
    },
     {
        "artist": "moneynumbdapain",
        "track": "carrera",
        "album": "1IVINGSUFFER"
    },

        {
        "artist": "naxowo",
        "track": "nicki minaj",
        "album": "nicki minaj"
    },
    
    {
        "artist": "bleood",
        "track": "bugs are crawling under your skin",
        "album": "bugs are crawling under your skin"
    },

        {
        "artist": "neva pray",
        "track": "tuyo",
        "album": "tuyo"
    },
  
  
       {
        "artist": "suban",
        "track": "face Melting // she Love it",
        "album": "face Melting // she Love it"
    },
         {
        "artist": "xaviersobased",
        "track": "in the yo",
        "album": "in the yo"
    },

      {
        "artist": "Aeter",
        "track": "boyfriend",
        "album": "boyfriend"
    },
        {
        "artist": "Jaydes",
        "track": "rose",
        "album": "ghetto cupid"
    },
  
    {
        "artist": "Lucy Bedroque",
        "track": "TAKE ME BACK",
        "album": "SISTERHOOD"
    },

    {
        "artist": "1oneam",
        "track": "Vogue",
        "album": "Vogue"
    },

    {
        "artist": "elijxhwtf",
        "track": "perc baby",
        "album": "perc baby"
    },

    {
        "artist": "Nettspend",
        "track": "Yoda",
        "album": "Yoda"
    },

    {
        "artist": "xaviersobased",
        "track": "in the yo",
        "album": "in the yo"
    },
    {
        "artist": "yuke",
        "track": "right now",
        "album": "right now"
    },

       {
        "artist": "Sexadlibs",
        "track": "my tongue tie d im trauma Tized",
        "album": "my tongue tie d im trauma Tized"
    },




]

def esperar_hasta_15():
    ahora = datetime.now(ART)
    hoy_15 = ahora.replace(hour=15, minute=0, second=0, microsecond=0)

    if ahora >= hoy_15:
        hoy_15 += timedelta(days=1)

    segundos = (hoy_15 - ahora).total_seconds()
    print(f"> Esperando hasta las 15:00 ART ({int(segundos)}s)")
    time.sleep(segundos)

def artista_del_dia():
    hoy = datetime.now(ART).date()
    ayer = hoy - timedelta(days=1)

    idx_hoy = hoy.toordinal() % len(ARTISTAS)
    idx_ayer = ayer.toordinal() % len(ARTISTAS)

    if idx_hoy == idx_ayer:
        idx_hoy = (idx_hoy + 1) % len(ARTISTAS)

    return ARTISTAS[idx_hoy]

def scrobble_batch(batch, start_number, max_retries=3):
    timestamp = int(time.time())
    scrobbles = []

    for i, track in enumerate(batch):
        scrobbles.append({
            'artist': track['artist'],
            'title': track['track'],
            'album': track['album'],
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

while True:
    esperar_hasta_15()

    track_base = artista_del_dia()
    print(f"🎵 Artista de hoy: {track_base['artist']}")

    sent_today = 0
    count = 1

    while sent_today < TARGET:
        remaining = TARGET - sent_today

        batch = [track_base, track_base]
        batch = batch[:remaining]

        sent = scrobble_batch(batch, count)
        sent_today += sent
        count += sent

        print(f"> Total hoy: {sent_today}/{TARGET}")

        if sent_today >= TARGET:
            break

        time.sleep(BATCH_DELAY)

    print("✔ 3.000 scrobbles completados. Esperando mañana…")
