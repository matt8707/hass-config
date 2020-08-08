# Home Assistant Configuration

[Home Assistant Core](https://home-assistant.io/) in [docker](https://www.docker.com/) on a  [Synology DiskStation DS918+](https://www.synology.com/products/DS918+). My use case is a [wall mounted](https://www.durable.eu/information-and-presentation/tablet-holder/wall-mounted-tablet-holder/tablet-holder-wall.html) tablet [[Samsung 10.1"](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/)] displaying Home Assistant in [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/) and on desktop using [applicationize](https://applicationize.me/) (chrome). My configuration is exposed to HomeKit with Apple Tv acting as a hub for remote connection. I also support [Nabu Casa](https://www.nabucasa.com/).

If you like anything here, Be sure to :star2: my repo!

![screenshot](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/screenshot.png)

## Features

* A different take on designing a [Lovelace UI](https://www.home-assistant.io/lovelace/) using a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) in [panel mode](https://www.home-assistant.io/lovelace/dashboards-and-views#panel)
* Achieving a less cluttered interface by displaying [more information](https://github.com/thomasloven/hass-browser_mod#popup) on a [long press](https://www.home-assistant.io/lovelace/picture-elements/#hold_action)
* Loading wheel for slow responding entities such as booting a computer.
* [Adding sounds](https://github.com/thomasloven/hass-browser_mod#media_player) to the UI using automations listening for events
* [CSS Animations](https://www.w3schools.com/css/css3_animations.asp) based on state

![animations](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/animations.gif)

### The sidebar

[Markdown Card](https://www.home-assistant.io/lovelace/markdown/) inside a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) to create dynamic [templates](https://www.home-assistant.io/docs/configuration/templating/).

* Time and date with greeting based on time of day
* Lights and switches that are on, using natural language
* Temperature with emoji based on weather conditions
* Important calendar information
* Other conditional alerts

### Sidebar footer

The three icons at the bottom in order

* Card to control [robot vacuum](https://www.mi-store.se/en/smart-homes/robot-vacuum-cleaners/xiaomi-robot-vacuum-2-roborock)
* Monitor [Home Assistant](https://home-assistant.io/), [tablet](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) and [Network Attached Storage](https://www.synology.com/products/DS918+)
* Lists available HACS updates and release notes for Home Assistant

![info](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info.png)

### Media

Conditionally displaying media player controls based on last active device such as [Apple TV](https://www.home-assistant.io/integrations/apple_tv/), [Playstation 4](https://www.home-assistant.io/integrations/ps4/), [Google Nest Mini](https://www.home-assistant.io/integrations/cast/). If nothing is active for 15 minutes then a poster of last downloaded movie/episode is shown ([Radarr](https://github.com/Radarr/Radarr)/[Sonarr](https://github.com/Sonarr/Sonarr)). Swipe to reveal other than last active media players.

![media](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/media.gif)

### Lights and sensors

All [Philips Hue](https://www2.meethue.com) lights with [sensors](https://www2.meethue.com/en-gb/p/hue-motion-sensor/8718696743171) in hallway, bathroom and walk-in closet.

* Injecting current lamp color to only parts of an icon
* Vertical dimmer for touch
* Brightness in a dynamic circle

![light](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/light.gif)

***

### Switches

* [SwitchBot](https://www.switch-bot.com/bot) to cold boot computer with a raspberry as a [hub](https://github.com/OpenWonderLabs/python-host). Numerous shell commands to monitor and control macOS
* [Belkin WeMo Switch](https://www.belkin.com/) to control studio monitors (speakers) with automations to apply [EQ calibration](https://www.sonarworks.com/reference) and volume control through AppleScript
* Control a pedestal fan, using [Belkin WeMo Switch](https://www.belkin.com/) and hue motion sensor temperature data to automate on summer nights
* [Broadlink](https://www.ibroadlink.com/products/ir+rf) to control fan and air purifier with IR and [Gosund Smart Wi-Fi Plug](https://www.gosund.com/download/smart_plug/127.html) for power/state

![info_light](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_light.png)

***

### Custom icons

I made some custom icons located in `www/custom_icons.js`. If you want to make your own I recommend reading the [material design principles](https://material.io/design/iconography/system-icons.html#design-principles).

![custom_icons](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/custom_icons.png)

### Misc

![vacuum](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/vacuum.png)

![misc](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/misc.png)

![tracker](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/tracker.png)

***

**Home Assistant Community Topic**  
[https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594)
