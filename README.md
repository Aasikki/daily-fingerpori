



[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Aasikki&repository=daily-fingerpori&category=integration)

# `[FIN]` Päivän Fingerpori Home Assistantille
Hakee päivän Fingerporin [darkbalin RSS-syötteestä](https://darkball.net/sarjakuvien-rss-syotteet/) ja näyttää sen kuvaentiteettinä Home Assistantissa.

Toimii parhaiten tekemäni sarjakuva-kortin kanssa: https://github.com/Aasikki/comic-card, mutta voit tietysti käyttää mitä tahansa korttia, joka esittää kuvia kuvaentiteeteistä, kuten HA:n sisäänrakennettua kuvakorttia.

## Asennus ja käyttöönotto:

 1. Integraation voi asentaa [HACS:ista](https://hacs.xyz/). Ohjeet HACS:in käyttöön löydät [täältä](https://hacs.xyz/docs/use/) (englanniksi).
    
 2. Asennuksen jälkeen ota integraatio käyttöön Home Assistantissa kohdasta: <br> `Asetukset -> Laitteet & palvelut -> Lisää integraatio -> Daily Fingerpori`.
    
 3. Tässä kohtaa voit muuttaa sarjakuvan päivitysväliä (oletuksena suositus: 3 tuntia), <br> ja painaa "Lähetä", jonka jälkeen integraatio on käytössä!

## Käyttö:
Kun integraatio on otettu käyttöön, `Laitteet & palvelut` -sivulta pitäisi löytyä `Daily Fingerpori` -niminen integraatio, josta löydät sarjakuvan kuvaentiteettinä, sekä napin, josta sarjakuvan voi manuaalisesti päivittää.

> **Vinkki!**
> Jos haluat päivittää sarjakuvan tiettyyn aikaan, voit tehdä automaation, joka päivittää sarjakuvan käyttämällä päivitysnappia (sarjakuva päivittyy siitä huolimatta myös asetetun päivitysvälin mukaan).

<br>

# `[ENG]` Daily Fingerpori for Home Assistant
Gets the daily Fingerpori comic from [darkball's RSS feed](https://darkball.net/sarjakuvien-rss-syotteet/) and displays it as an image entity in Home Assistant.

Best when used together with my comic card: https://github.com/Aasikki/comic-card, but of course you can use any card that can display images from image entities, like the built-in picture card.

## Installation and configuration:

 1. The integration can be installed from [HACS](https://hacs.xyz/). Instructions for using HACS can be found [here](https://hacs.xyz/docs/use/).
    
 2. After installing, set up the integration in Home Assistant from: <br> `Settings -> Devices & services -> Add integration -> Daily Fingerpori`.
    
 3. From here you can change the comic update interval (default recommendation: 3 hours), <br> and press "Submit", after which the integration is in use!

## Usage:
After setting up the integration, you should find an integration called `Daily Fingerpori` from the `Devices & services` -page, where you can find the comic as a picture entity, as well as a button for manually updating the comic.

> **Tip!**
> If you want to update the comic at a specific time, you can make an automation that will update the comic using the update button (the comic will still also be updated by the configured update interval).

<br>
<br>

<img width="611" height="376" alt="kuva" src="https://github.com/user-attachments/assets/0fce2824-778c-4987-bf5d-79ac0dc0d7a2" />
