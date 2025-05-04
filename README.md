# Jalkapalloseura
## Käyttötarkoitus
* Sovelluksessa käyttäjät pystyvät etsimään peliseuraa jalkapalloon. Ilmoituksessa lukee missä ja milloin pelivuoro on.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään ilmoituksia ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
* Käyttäjä pystyy etsimään ilmoituksia sen perusteella, milloin vuoro on.
* Käyttäjäsivu näyttää, montako ilmoitusta käyttäjä on lähettänyt ja listan ilmoituksista.
* Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. Kumpula Unisport, keskitason pelaaja).
* Käyttäjä pystyy ilmoittautumaan pelivuoroon. Ilmoituksessa näytetään, ketkä käyttäjät ovat ilmoittautuneet.

## Nykyinen tilanne
* Sovellukseen pystyy rekisteröitymään, kirjautumaan ja kirjautumaan ulos
* Etusivulla näkyy 10 ilmoitusta, jos ilmoituksia on enemmän, sivun voi vaihtaa
* Ilmoituksia voi julkaista, muokata ja poistaa
* Ilmoituksissa on otsikko, sijainti, päivämäärä, pelintaso ja tekstikenttä muulle tarkentavalle sisällölle
* Ilmoituksiin voi ilmoittautua ja ilmoittautumisen poistaa
* Ilmoituksessa näkyy lista ilmoittautuneista, ja etusivulla ilmoittautuneiden määrä
* Ilmoituksia voi hakea otsikon, sijainnin, pelintason ja sisällön perusteella
* Käyttäjillä on käyttäjäsivut
* Käyttäjäsivuilla näkyy mitä ilmoituksia käyttäjä on tehnyt, ja mihin hän on ilmoittautunut
* Jos ilmoituksia tai ilmoittautumisia on enemmän kuin 20, näkyviä ilmoituksia voi vaihtaa

## Käynnistysohjeet
Lataa flask kirjasto:\
$ pip install flask

Luo taulut:\
$ sqlite3 database.db < schema.sql

Käynnistä sovellus:\
$ flask run

Liitä saatu ip-osoite selaimesi hakuun.
