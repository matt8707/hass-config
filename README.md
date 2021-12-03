# Home Assistant Configuration

[Home Assistant Container](https://www.home-assistant.io/installation/#compare-installation-methods) on a Synology DiskStation DS918+ NAS. Use cases are a [Galaxy Tab A 10.1](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) ([wall mounted](https://www.durable.eu/information-and-presentation/tablet-holder/wall-mounted-tablet-holder/tablet-holder-wall.html)) tablet with [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/) and [homeassistant-desktop](https://github.com/mrvnklm/homeassistant-desktop) on macOS. My configuration is exposed to HomeKit with Apple TV acting as a hub for remote connection. I also support [Nabu Casa](https://www.nabucasa.com/).

If you like anything here, be sure to :star2: my repo!

![screenshot](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/screenshot.png)


## Update 2021.12 🎁

This is now the **[top thread of all time](https://community.home-assistant.io/top?period=all)** 😮

* Releases on GitHub to segment changes
  * All releases - [matt8707/hass-config/releases](https://github.com/matt8707/hass-config/releases)
  * All changes - [matt8707/hass-config/commits/master](https://github.com/matt8707/hass-config/commits/master)
* Installation notes added further down
* Hardware and docker-compose files


**Buttons** `custom:button-card`

* [hide "extra_styles fix"](https://github.com/matt8707/hass-config/commit/c560bded8288bcfbb15b1c019475efa8d81de3bf) - make the "catch-all" button non-clickable ([#injecting-css-with-extra_styles](https://github.com/custom-cards/button-card#injecting-css-with-extra_styles))

* [bug fixes and improvements ™](https://github.com/matt8707/hass-config/commit/f9a16d2b5781873b2191d74e3c475447b9d00fe0) - shorten overall template code, fix loader on computer lock and tv icon animation

* [person last_changed persistence with fallback](https://github.com/matt8707/hass-config/commit/9738395788e5ee66f40fc50b47a604713172171f) - if set up, the timestamp is retained with mqtt across restarts

* [add person zone](https://github.com/matt8707/hass-config/commit/9e8e53a52d820a9b5af49a0a1eb72ef1848f71a5) - location is shown instead of "not home" when in a zone

* [fix icon light color](https://github.com/matt8707/hass-config/commit/b0b5e624a213390ad889c7d2b89eae931e2218f5) - color temperature shown as blue, hs shown as actual color

* [button-card → light-popup-card actions and theme](https://github.com/matt8707/hass-config/commit/b87f6d243bcf79cc069f254fb01fc4a2e1b35b1c) - revert button-card workaround, make use of actions

* [fix text alignment when #name is truncated...](https://github.com/matt8707/hass-config/commit/661623655ac7ed4a1360c21e3181397ac684ba51) - on small screens, the text was centered when the name didn't fit

* [align lock icon on ios](https://github.com/matt8707/hass-config/commit/ad72f73886c279ca25a54a9b1e187eb5333b2ca7) - on small screens the lock icon was not vertically aligned


**Theme** `custom:card-mod`

* [card-mod resource → module](https://github.com/matt8707/hass-config/commit/a14d5447a908b5f2098bad94dc8017b27466e9bb) - documentation [#performance-improvements](https://github.com/thomasloven/lovelace-card-mod#performance-improvements)

* [fix brave icon height and firefox shrinking icons](https://github.com/matt8707/hass-config/commit/895ec555087dfc67b0671af391f8943c7ee38af2) - brave and firefox browser compatibility

* [swipe-card height](https://github.com/matt8707/hass-config/commit/f9ad21c8b0314781ee3d5fabc9684f08fe978a08) - force 100% height when only using button cards in a grid

* [themes sidebar_update_color fix 2021.11.0](https://github.com/matt8707/hass-config/commit/8be2e4ad321f578347377e5685697ee977ccfa70) - ha-icon is now called ha-state-icon


**Sidebar**
* [mailbox sensors and automation](https://github.com/matt8707/hass-config/commit/95b4797f681fb3768a629f8442dafe5645fc9f1c) - add mailbox counter (using two aqara contact sensors)

* [sidebar battery map entities](https://github.com/matt8707/hass-config/commit/d9c8710fcd261475b91a2601f6ef66c9ab3d73e8) - list all batteries below the 5% threshold, thanks @Se7enair

* [add time offset to skånetrafiken PT sensor](https://github.com/matt8707/hass-config/commit/af5284a08dfa8be7a448c593d82a3ce877dfc8f5) - "walking time" bus departure offset


**Database**

💡 [SQL command to list worst offenders](https://community.home-assistant.io/t/how-to-reduce-your-database-size-and-extend-the-life-of-your-sd-card/205299/24). I managed to decrease my db size by ≈ 80%

```bash
docker exec -it mariadb \
  mysql homeassistant -u"root" -p"password" \
  -e"SELECT entity_id, COUNT(*) AS count FROM states GROUP BY entity_id ORDER BY COUNT(*) DESC LIMIT 10;" \
  -e"SELECT JSON_VALUE(event_data, '$.entity_id') AS entity_id, COUNT(*) AS count FROM events WHERE JSON_VALUE(event_data, '$.entity_id') IS NOT NULL GROUP BY JSON_VALUE(event_data, '$.entity_id') ORDER BY COUNT(*) DESC LIMIT 10;"
```

* [db optimization](https://github.com/matt8707/hass-config/commit/b37bcd983f03a9fa18b8a099f3903e1bb497ffa3) - exclude browser_mod from recorder
* [lower db commit interval](https://github.com/matt8707/hass-config/commit/3d4a6e95e49c1f4c77f39a269f52eb8efa74edb2) - decrease recorder interval and influxdb precision


**Other**

* @svalmorri [made a nice button for roller shutters](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594/2062)

* [remove valetudo](https://github.com/matt8707/hass-config/commit/2484e724f06b6e61b133c322dd0e7a14cfcd8e9b) - don't want to spend my time maintaining a vacuum cleaner...

* [vacuum-map-card 1 → 2](https://github.com/matt8707/hass-config/commit/d58b510a570a8e878fb47a5c0f6d662f1602187a) - configuration changes and styling

* [fix vacuum sensors for 2021.11.1, maybe?](https://github.com/matt8707/hass-config/commit/ac1c5c14e9db5ea00c9e88922cb10ca76e21d7da) - template seconds to percent left

* [mini-graph-card → apexcharts](https://github.com/matt8707/hass-config/commit/37156817c59e181451114c2531730b6e0fac088c) - better graphs, I posted some [examples](https://community.home-assistant.io/t/apexcharts-card-a-highly-customizable-graph-card/272877/1240)

* [update template sensors, remove legacy](https://github.com/matt8707/hass-config/commit/bdc4c9b135f51f6e4cad4916f3adb3a9f522709a) - convert all legacy template sensors

* [template warnings](https://github.com/matt8707/hass-config/commit/8b14c9cb13d9d225380111d892795defbe87f207) and [stfu home-assistant.log](https://github.com/matt8707/hass-config/commit/d2653664937600a199fc001b5e65488d7ffde88a) - template "default" log warnings

* [add unifi and rpi sensors](https://github.com/matt8707/hass-config/commit/fb76db22fa4dd03bb96f332a3e230c7e4841736a) - command_line sensors for router and raspberry pi


*If you want, you can [buy me a beer](https://www.buymeacoffee.com/matt8707)* :blush:


## Installation

> **How do I install this theme?**
> There's no install button. I'm sharing my full configuration

> **Can you please add this to HACS?**
> No, because this is not a custom card or integration

> **Where do I even start?**
> [This post explains how to get started](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594/1717) :tada:


## Features

* [Lovelace UI](https://www.home-assistant.io/lovelace/) using custom [button-card](https://github.com/custom-cards/button-card) and [layout-card](https://github.com/thomasloven/lovelace-layout-card)
* Portrait, landscape and mobile view - [responsive_demo.mp4](https://user-images.githubusercontent.com/36163594/120789256-ad825000-c531-11eb-97c2-18904c48efdd.mp4)
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
* Geofenced bus departures
* Important calendar information
* Other conditional alerts


#### Sidebar footer

* Vacuum - card to control robot vacuum, with a live map
* Information - monitor Home Assistant, tablet and NAS
* Updates - lists Home Assistant release notes and HACS updates

#### Popups

Long press a button to show settings and information pertaining to the entity, using [browser_mod](https://github.com/thomasloven/hass-browser_mod). Light popups are automatically created using the `light` button-card template with [light-popup-card](https://github.com/DBuit/light-popup-card) and [light-entity-card](https://github.com/ljmerza/light-entity-card)

![light](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/light.gif)


#### Media

Conditionally display media players based on the last active device. If nothing is active for 15 minutes, a poster of the last downloaded movie/episode is shown ([Plex](https://github.com/plexinc/pms-docker), [Radarr](https://github.com/Radarr/Radarr), [Sonarr](https://github.com/Sonarr/Sonarr)). Swipe to reveal non-active media players

![media](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/media.gif)


## Theme

[card-mod](https://github.com/thomasloven/lovelace-card-mod) is used for the styles in `include/themes.yaml` and each popup also contain styles depending on content.
I've made a tool to help with css element selectors - [https://matt8707.github.io/card-mod-helper/](https://matt8707.github.io/card-mod-helper/)

![media](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/cardmod_helper.png)


## Screenshots

| [![imac_light](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_light_2.png)](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_light_2.png)<br>iMac and Light | [![information](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_2.png)](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_2.png)<br>Information | [![vacuum](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/vacuum_2.png)](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/vacuum_2.png)<br>Vacuum |
|:---:|:---:|:---:|
| [![misc](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/misc_2.png)](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/misc_2.png)<br>**Misc** | [![person_updates](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/tracker_updates.png)](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/tracker_updates.png)<br>**Person and Updates** | [![custom_icons](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/custom_icons.png)](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/custom_icons.png)<br>**www/custom_icons.js** |


## Hardware

<details>
<summary>click to expand</summary>

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
| Sony | PlayStation 5 | [custom](https://github.com/dhleong/playactor) | Game console - State, sleep and wake [#ps5 thread](https://community.home-assistant.io/t/playstation-5-command-line-sensor-help-command-failed-empty-json/256275/60) |
| Apple | iPhone X | [ios](https://www.home-assistant.io/integrations/ios/) | Home Assistant Companion App for iOS |

*Note: I do not recommend "Belkin WeMo" or "Deltaco SH-P01"*

</details>

---

**GitHub Repository**
[https://github.com/matt8707/hass-config](https://github.com/matt8707/hass-config)

**Home Assistant Community Topic**
[https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594)
