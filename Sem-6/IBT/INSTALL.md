# Návod na zostavenie aplikácie
## Knižnice a nástroje

Najprv je potrebné nainštalovať všetky nasledujúce balíčky. Tieto balíčky by mali byť dostupné pomocou 
nástroja apt-get. 
- python3 (>= 3.8.2)
- python3-venv (>= 3.8.2)
- postgis (>= 3.0.0)
- libmapnik-dev (>= 3.0.23)
- python3-mapnik (>= 1:0.0)


## Dáta

Dáta je možné získať na nasledujúcich odkazoch, ktoré stiahnu súbory typu osm.pbf.:
```
    https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf
    https://download.geofabrik.de/europe/slovakia-latest.osm.pbf
```

Pomocou nasledujúceho príkazu sa vytvorí jeden spoločný súbor:
```
    osmium merge slovakia.osm.pbf czechia.osm.pdf -o czechoslovakia.osm.pbf
```

Pomocou nasledujúcich príkazov je potrebné nastaviť databázu s rozšírením PostGIS:
```
    sudo service postgresql start
    sudo -u postgres createuser gisuser
    sudo -u postgres createdb --encoding=UTF8 --owner=gisuser gis
    psql --username=postgres --dbname=gis -c "CREATE EXTENSION postgis;"
    psql --username=postgres --dbname=gis -c "CREATE EXTENSION postgis_topology;"
```
Na vykonanie príkazov je zvyčajne potrebné potvrdenie od Postgresql superuser, ktorý sa implicitne nazýva 'postgres' s heslom 'postgres'.
Výsledná aplikácia očakáva existenciu používateľa 'gisuser' s heslom 'gisuser' a bežiaci databázový server na porte číslo 5432 (väčšinou implicitne použitý).

Teraz už je možné do databázy importovať dáta pomocou príkazu (import môže trvať aj vyše 20 minút):
```
    osm2pgsql -U gisuser -W -c -H localhost -d gis -E 4326 --slim --drop czechoslovakia.osm.pbf
```

Na dokončenie nastavení databázy, je ešte potrebné spustiť skript:
```
    psql -U gisuser -W -d gis -h localhost -a -f app/db_script
```


## Aplikácia

Pomocou nasledovných príkazov sa vytvorí a aktivuje virtuálne prostredie:
```
    cd app
    python3 -m venv venv --system-site-packages
    source venv/bin/activate
```

Teraz je pomocou nasledujúceho príkazu možné nainštalovať potrebné knižnice:
```
    pip install -r requirements.txt
```

Aplikáciu je možné spustiť pomocou nasledovných príkazov:
```
    export FLASK_APP=app.py
    flask run
```
