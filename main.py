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
    SCROBBLE_DELAY = 2.6  

    ARTISTAS = [
        {"artist": "moneynumbdapain", "track": "carrera", "album": "1IVINGSUFFER"},
        {"artist": "naxowo", "track": "nicki minaj", "album": "nicki minaj"},
        {"artist": "1oneam", "track": "Vogue", "album": "Vogue"},
        {"artist": "unixzo", "track": "fashion whore", "album": "fashion whore"},
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


    def esperar_hasta_15():
        ahora = datetime.now(ART)
        hoy_15 = ahora.replace(hour=15, minute=0, second=0, microsecond=0)
        if ahora >= hoy_15:
            hoy_15 += timedelta(days=1)
        time.sleep((hoy_15 - ahora).total_seconds())

    def artista_del_dia():
        hoy = datetime.now(ART).date()
        ayer = hoy - timedelta(days=1)

        idx_hoy = hoy.toordinal() % len(ARTISTAS)
        idx_ayer = ayer.toordinal() % len(ARTISTAS)

        if idx_hoy == idx_ayer:
            idx_hoy = (idx_hoy + 1) % len(ARTISTAS)

        return ARTISTAS[idx_hoy]

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
                print("🚫 RATE LIMIT — paro hasta mañana")
                return None
            print("Error:", e)
            return False


    while True:
        esperar_hasta_15()

        track = artista_del_dia()
        print(f"\n🎵 Artista del día: {track['artist']}")

        enviados = 0

        while enviados < TARGET:
            res = scrobble(track, enviados + 1)

            if res is None:
                break

            if res:
                enviados += 1

            time.sleep(SCROBBLE_DELAY)

        print(f"✔ {enviados} scrobbles completados hoy\n")
