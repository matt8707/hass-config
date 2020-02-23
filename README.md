# Home Assistant Configuration

[Home Assistant Core](https://home-assistant.io/) in [docker](https://www.docker.com/) on a  [Synology DiskStation DS918+](https://www.synology.com/products/DS918+). My use case is a [wall mounted](https://www.durable.eu/information-and-presentation/tablet-holder/wall-mounted-tablet-holder/tablet-holder-wall.html) tablet [[Samsung 10.1"](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/)] displaying Home Assistant in [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/) and on desktop using [applicationize](https://applicationize.me/) (chrome). My configuration is exposed to HomeKit with Apple Tv acting as a hub for remote connection. I also support [Nabu Casa](https://www.nabucasa.com/).

If you like anything here, Be sure to :star2: my repo!

![screen.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/screen2.png)

## Features

* A different take on designing a [Lovelace UI](https://www.home-assistant.io/lovelace/) using a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) in [panel mode](https://www.home-assistant.io/lovelace/views/#panel-mode).
* Achieving a less cluttered interface by displaying [more information](https://github.com/thomasloven/hass-browser_mod#popup) on a [long press](https://www.home-assistant.io/lovelace/picture-elements/#hold_action).
* Fake on-state and loading wheel for slow responding entities such as booting a computer.
* Animations and [applying sound](https://github.com/thomasloven/hass-browser_mod#media_player) to UI using automations listening for events.

### Media

Conditionally display media player controls based on last active device such as [Apple TV](https://www.home-assistant.io/integrations/apple_tv/), [Playstation 4](https://www.home-assistant.io/integrations/ps4/), [Google Nest Mini](https://www.home-assistant.io/integrations/cast/). If nothing is active for 15 minutes then a poster of last downloaded movie/episode is shown ([Radarr](https://github.com/Radarr/Radarr)/[Sonarr](https://github.com/Sonarr/Sonarr)). But what if I want to control the second last active device? Swipe to reveal...

![lights_switches.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/con_media.gif)

### The sidebar

[Markdown Card](https://www.home-assistant.io/lovelace/markdown/) inside a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) to create dynamic [templates](https://www.home-assistant.io/docs/configuration/templating/).

* Time and date with greeting based on time of day.
* Lights and switches that are on, using natural language.
* Temperature with emojis based on weather conditions.
* Important calendar information.
* Time since a person left home.

### Sidebar footer

The three icons at the bottom in order

* Card to control [robot vacuum](https://www.mi-store.se/en/smart-homes/robot-vacuum-cleaners/xiaomi-robot-vacuum-2-roborock).
* Monitor [Home Assistant](https://home-assistant.io/), [tablet](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) and [Network Attached Storage](https://www.synology.com/products/DS918+).
* A list of [scenes](https://www.home-assistant.io/integrations/scene/) with a legend.

![info2.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info2.png)

### Lights and sensors

All [Philips Hue](https://www2.meethue.com) lights with [sensors](https://www2.meethue.com/en-gb/p/hue-motion-sensor/8718696743171) in hallway, bathroom and walk-in closet.

* Modified (CSS+JS) vertical [Light Entity Card](https://github.com/ljmerza/light-entity-card) for easier touch control.
* If applicable, show a Light Entity Card color wheel.
* [Custom SVG](https://github.com/matt8707/hass-config/blob/master/www/custom-icons_v01.html) icons to reflect current color.
* Brightness percentage in a [Circle sensor](https://github.com/custom-cards/circle-sensor-card).

***

### Switches

* [SwitchBot](https://www.switch-bot.com/bot) to cold boot computer (with [usb bluetooth adapter](https://plugable.com/products/usb-bt4le) in NAS). Numerous shell commands to monitor and control macOS.
* [Belkin WeMo Switch](https://www.belkin.com/) to control studio monitors (speakers) with automations to apply [EQ calibration](https://www.sonarworks.com/reference) and volume control through AppleScript.
* Control a pedestal fan, using [Belkin WeMo Switch](https://www.belkin.com/) and hue motion sensor temperature data to automate on summer nights.

![lights_switches.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/lights_switches.png)

***

**Home Assistant Community Topic**  
[https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/)
