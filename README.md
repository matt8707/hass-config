# Home Assistant Configuration

[Home Assistant Container](https://www.home-assistant.io/installation/#compare-installation-methods) on a Synology DiskStation DS918+ NAS. [Wall mounted](https://www.durable.eu/en_DE/tablet-holder-wall/893323) tablet ([Galaxy Tab A 10.1](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/)) using [Fully Kiosk Browser](https://www.fully-kiosk.com/#get-kiosk-apps). My configuration is exposed to HomeKit with Apple TV acting as a hub for remote connection.

If you like anything here, be sure to :star2: my repo!

![dashboard](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/dash.png)

## Installation

**How do I install this theme?** <br>
There's no install button. I'm sharing my full configuration

**Can you please add this to HACS?** <br>
No, because this is not a custom card or integration

**Where do I even start?** <br>
[INSTALL.md explains how to get started](INSTALL.md) :tada:

## Features

* [Dashboard (Lovelace)](https://www.home-assistant.io/lovelace/) using custom [button-card](https://github.com/custom-cards/button-card) and [layout-card](https://github.com/thomasloven/lovelace-layout-card)
* Portrait, landscape and mobile view - [responsive_demo.mp4](https://user-images.githubusercontent.com/36163594/120789256-ad825000-c531-11eb-97c2-18904c48efdd.mp4) [[mirror]](https://drive.google.com/file/d/1BgGHFgKF2sfI7cvdbWUeCyU_85D2R5x3/view?usp=sharing)
* Less cluttered interface by displaying more information in a popup
* Loading animation for slow responding entities
* Adding tap audio feedback to the UI for wall-mounted tablet
* Icon [CSS animations](https://www.w3schools.com/css/css3_animations.asp) based on entity state

![animations](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/animations.gif)

#### Sidebar

* Time and date with greeting based on time of day
* Entities that are on, using natural language
* Mailbox counter to show received mail
* Temperature with emoji based on weather conditions
* Important calendar information
* Other conditional alerts

#### Footer

Popups that supports notifications.

![footer](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/footer.png)

#### Popups

Long press a button to show settings and information pertaining to the entity, using [browser_mod](https://github.com/thomasloven/hass-browser_mod). Light popups are automatically created using the `light` button-card template with 🍄 [Mushroom](https://github.com/piitaya/lovelace-mushroom)

<img src="https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/group.png" width="35%">

#### Media

Conditionally display media players based on the last active device. If nothing is active for 15 minutes, a poster of the last downloaded movie/episode is shown ([Plex](https://github.com/plexinc/pms-docker), [Radarr](https://github.com/Radarr/Radarr), [Sonarr](https://github.com/Sonarr/Sonarr)). Swipe to reveal non-active media players

![media](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/media.gif)

## Theme

[card-mod](https://github.com/thomasloven/lovelace-card-mod) is used for the styles in `include/themes.yaml` and each popup also contain styles depending on content.
I've made a tool to help with css element selectors - [https://matt8707.github.io/card-mod-helper/](https://matt8707.github.io/card-mod-helper/)

![media](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/cardmod_helper.png)

## Screenshots

| nas | vacuum |
| --- | --- |
| ![nas](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/nas.png) | ![vacuum](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/vacuum.png) |

| misc |
| --- |
| ![multi](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/multi.png) |

## Hardware

| Vendor | Product | Integration | Description |
|---|---|---|---|
| Ubiquiti | UniFi Dream Machine | [unifi](https://www.home-assistant.io/integrations/unifi/) | Router, controller, switch and access point |
| Synology | DiskStation DS918+ | [synology_dsm](https://www.home-assistant.io/integrations/synology_dsm/) | 4x4TB NAS - [matt8707/docker-compose-dsm](https://github.com/matt8707/docker-compose-dsm) |
| Raspberry | Pi 3 Model B+ | [shell_command](https://www.home-assistant.io/integrations/shell_command/) | Bluetooth communication - [matt8707/docker-compose-rpi](https://github.com/matt8707/docker-compose-rpi) |
| Samsung | Galaxy Tab A SM-T510 | [custom](https://github.com/cgarwood/homeassistant-fullykiosk) | Wall mounted tablet in hallway by the front door |
| Philips | Hue | [hue](https://www.home-assistant.io/integrations/hue/) | Bridge, 15 bulbs, 3 motion sensors, 2 dimmer switches |
| Apple | iMac | [shell_command](https://www.home-assistant.io/integrations/shell_command/) | All-in-one desktop computer |
| SwitchBot | SwitchBot Bot | [custom](https://github.com/fphammerle/switchbot-mqtt) | Bluetooth device that mechanically turns on my computer |
| Xiaomi | Mi Roborock S50 | [xiaomi_miio](https://www.home-assistant.io/integrations/xiaomi_miio/) | Robot vacuum with lidar -  [xiaomi-cloud-map-extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor) |
| Broadlink | RM4 Pro, HTS2 cable | [broadlink](https://www.home-assistant.io/integrations/broadlink/) | Infrared transmitter for AC unit with temp/humidity sensor |
| Gosund | SP112 | [esphome](https://www.home-assistant.io/integrations/esphome/) | 3x tuya wifi plugs with power monitoring, flashed with ESPHome |
| Belkin | WeMo | [wemo](https://www.home-assistant.io/integrations/wemo/) | 2x wifi plugs and 1x motion sensor |
| Google | Nest Mini | [cast](https://www.home-assistant.io/integrations/cast/) | Not really used, Google sent me one |
| Deltaco | SH-P01 | [tuya](https://www.home-assistant.io/integrations/tuya/) | Cheap wifi plug for balcony LED lights |
| Phoscon | ConBee II | [custom](https://github.com/Koenkk/zigbee2mqtt) | Zigbee USB gateway using zigbee2mqtt |
| Xiaomi | Aqara MCCGQ11LM | [mqtt](https://www.home-assistant.io/integrations/mqtt/) | 3x zigbee door/window contact sensors |
| Apple | TV 4K | [apple_tv](https://www.home-assistant.io/integrations/apple_tv/) | 2x set-top-boxes that streams content from Plex |
| Sony | Bravia KDL-55W905A | [braviatv](https://www.home-assistant.io/integrations/braviatv/) | 2013 mid-range 55" 1080p 3D TV |
| Samsung | UE50RU6025KXXC | [custom](https://github.com/ollo69/ha-samsungtv-smart) | 2019 low-range 50" 4K HDR TV |
| Sony | PlayStation 5 | [custom](https://github.com/FunkeyFlo/ps5-mqtt) | Game console - State, sleep and wake |
| Apple | iPhone X | [ios](https://www.home-assistant.io/integrations/ios/) | Home Assistant Companion App for iOS |

*Note: I do not recommend "Belkin WeMo" or "Deltaco SH-P01"*

---

**GitHub Repository**
[https://github.com/matt8707/hass-config](https://github.com/matt8707/hass-config)

**Home Assistant Community Topic**
[https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594)
