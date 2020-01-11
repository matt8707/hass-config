# Home Assistant Configuration

[Hass.io](https://home-assistant.io/) installed on a [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) and my use case is a [wall mounted](https://www.durable.eu/information-and-presentation/tablet-holder/wall-mounted-tablet-holder/tablet-holder-wall.html) tablet [[Samsung 10.1"]](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) displaying Home Assistant in [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/) and on desktop [applicationize](https://applicationize.me/) (chrome). I've opted for local control only but I expose my configuration to homekit with Apple Tv acting as a hub for remote connection. 

If you like anything here, Be sure to :star2: my repo!

<img src="https://github.com/matt8707/hass-config/blob/master/www/img/screen.png" />

## Features

  * A different take on designing a [Lovelace UI](https://www.home-assistant.io/lovelace/) using a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) in [panel mode](https://www.home-assistant.io/lovelace/views/#panel-mode).
  * Achieving a less cluttered interface by displaying [more information](https://github.com/thomasloven/hass-browser_mod#popup) on a [long press](https://www.home-assistant.io/lovelace/picture-elements/#hold_action). 
  * Animations and loading wheel for slow responding entities such as booting a computer.
  * [Applying sound](https://github.com/thomasloven/hass-browser_mod#media_player) to UI using automations listening for events.

### The sidebar

[Markdown Card](https://www.home-assistant.io/lovelace/markdown/) inside a [Picture Elements Card](https://www.home-assistant.io/lovelace/picture-elements/) to create dynamic [templates](https://www.home-assistant.io/docs/configuration/templating/).

  * Time and date with greeting based on time of day.
  * Lights and switches that are on, using natural language.
  * Temperature with emojis based on weather conditions.
  * Important calendar information.
  * Time since a person left home.

### Sidebar footer

The three icons at the bottom in order

  * Reload hassio.local in [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/).
  * Monitor [Home Assistant](https://home-assistant.io/), [tablet](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) and [Network Attached Storage](https://www.synology.com/products/DS918+).
  * A list of [scenes](https://www.home-assistant.io/integrations/scene/) **TODO**. 

<img src="https://github.com/matt8707/hass-config/blob/master/www/img/info.png" />

### Lights and sensors

All [Philips Hue](https://www2.meethue.com) lights with [sensors](https://www2.meethue.com/en-gb/p/hue-motion-sensor/8718696743171) in hallway, bathroom and walk-in closet.

  * Modified (CSS+JS) vertical [Light Entity Card](https://github.com/ljmerza/light-entity-card) for easier touch control. 
  * If applicable, show a Light Entity Card color wheel.
  * [Custom SVG](https://github.com/matt8707/hass-config/blob/master/www/custom-icons.html) icons to reflect current color.
  * Brightness percentage in a [Circle sensor](https://github.com/custom-cards/circle-sensor-card).
  ***
### Switches
  * [SwitchBot](https://www.switch-bot.com/bot) to cold boot computer. Numerous shell commands to monitor and control macOS.
  * [Belkin WeMo Switch](https://www.belkin.com/) to control studio monitors (speakers) with automations to apply [EQ calibration](https://www.sonarworks.com/reference) and volume control through AppleScript.
  * Control a pedestal fan, using [Belkin WeMo Switch](https://www.belkin.com/) and hue motion sensor temperature data to automate on summer nights.

<img src="https://github.com/matt8707/hass-config/blob/master/www/img/lights_switches.png" />

### Media

The idea is to conditionally display media player controls based on last active device such as [Apple TV](https://www.home-assistant.io/integrations/apple_tv/), [Playstation 4](https://www.home-assistant.io/integrations/ps4/), [Spotify](https://www.home-assistant.io/integrations/spotify/) or [Plex](https://www.home-assistant.io/integrations/plex/). If nothing is active then a poster of last downloaded movie/episode is shown ([Radarr](https://github.com/Radarr/Radarr)/[Sonarr](https://github.com/Sonarr/Sonarr)). But since tvOS 13 integration is broken atm I'm putting this as a **TODO**.
