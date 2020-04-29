# Home Assistant Configuration

[Home Assistant Core](https://home-assistant.io/) in [docker](https://www.docker.com/) on a  [Synology DiskStation DS918+](https://www.synology.com/products/DS918+). My use case is a [wall mounted](https://www.durable.eu/information-and-presentation/tablet-holder/wall-mounted-tablet-holder/tablet-holder-wall.html) tablet [[Samsung 10.1"](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/)] displaying Home Assistant in [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/) and on desktop using [applicationize](https://applicationize.me/) (chrome). My configuration is exposed to HomeKit with Apple Tv acting as a hub for remote connection. I also support [Nabu Casa](https://www.nabucasa.com/).

If you like anything here, Be sure to :star2: my repo!

![s_main.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/s_main.png)

### New April 2020

The configuration is now fully configuarble with code and easier to maintain. I've transitioned from using images to [button-card](https://github.com/custom-cards/button-card). 

## Features

* A different take on designing a [Lovelace UI](https://www.home-assistant.io/lovelace/) using a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) in [panel mode](https://www.home-assistant.io/lovelace/views/#panel-mode).
* Achieving a less cluttered interface by displaying [more information](https://github.com/thomasloven/hass-browser_mod#popup) on a [long press](https://www.home-assistant.io/lovelace/picture-elements/#hold_action).
* Loading wheel for slow responding entities such as booting a computer.
* Animations and [applying sound](https://github.com/thomasloven/hass-browser_mod#media_player) to UI using automations listening for events.

### Media

Conditionally display media player controls based on last active device such as [Apple TV](https://www.home-assistant.io/integrations/apple_tv/), [Playstation 4](https://www.home-assistant.io/integrations/ps4/), [Google Nest Mini](https://www.home-assistant.io/integrations/cast/). If nothing is active for 15 minutes then a poster of last downloaded movie/episode is shown ([Radarr](https://github.com/Radarr/Radarr)/[Sonarr](https://github.com/Sonarr/Sonarr)). Swipe to reveal other than last active media players.

![lights_switches.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/con_media.gif)

### The sidebar

[Markdown Card](https://www.home-assistant.io/lovelace/markdown/) inside a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) to create dynamic [templates](https://www.home-assistant.io/docs/configuration/templating/).

* Time and date with greeting based on time of day.
* Lights and switches that are on, using natural language.
* Temperature with emojis based on weather conditions.
* Important calendar information.
* Other conditional alerts

### Sidebar footer

The three icons at the bottom in order

* Card to control [robot vacuum](https://www.mi-store.se/en/smart-homes/robot-vacuum-cleaners/xiaomi-robot-vacuum-2-roborock).
* Monitor [Home Assistant](https://home-assistant.io/), [tablet](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) and [Network Attached Storage](https://www.synology.com/products/DS918+).
* A list of [scenes](https://www.home-assistant.io/integrations/scene/) with a legend.

![s_info.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/s_info.png)

### Lights and sensors

All [Philips Hue](https://www2.meethue.com) lights with [sensors](https://www2.meethue.com/en-gb/p/hue-motion-sensor/8718696743171) in hallway, bathroom and walk-in closet.

* Now using [light-popup-card](https://github.com/DBuit/light-popup-card).
* Injecting current lamp color to only parts of an icon.
* Brightness percentage in a ~~circle sensor~~ custom field (SVG+JS).

***

### Switches

* [SwitchBot](https://www.switch-bot.com/bot) to cold boot computer with, for now, a raspberry as a [hub](https://github.com/OpenWonderLabs/python-host). Numerous shell commands to monitor and control macOS.
* [Belkin WeMo Switch](https://www.belkin.com/) to control studio monitors (speakers) with automations to apply [EQ calibration](https://www.sonarworks.com/reference) and volume control through AppleScript.
* Control a pedestal fan, using [Belkin WeMo Switch](https://www.belkin.com/) and hue motion sensor temperature data to automate on summer nights.

![s_light_switch.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/s_light_switch.png)

![s_misc.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/s_misc.png)

![s_vacuum.png](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/s_vacuum.png)

***

**Home Assistant Community Topic**  
[https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/)
