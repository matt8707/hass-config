# Home Assistant Configuration

[Home Assistant Container](https://www.home-assistant.io/installation/#compare-installation-methods) ([Docker](https://hub.docker.com/r/homeassistant/home-assistant)) on a NAS ([Synology DiskStation DS918+](https://www.synology.com/products/DS918+)). My use case is a [wall mounted](https://www.durable.eu/information-and-presentation/tablet-holder/wall-mounted-tablet-holder/tablet-holder-wall.html) tablet ([Galaxy Tab A 10.1](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/)) using [Fully Kiosk Browser](https://www.ozerov.de/fully-kiosk-browser/), and on desktop using [homeassistant-desktop](https://github.com/mrvnklm/homeassistant-desktop). My configuration is exposed to HomeKit with Apple Tv acting as a hub for remote connection. I also support [Nabu Casa](https://www.nabucasa.com/).

If you like anything here be sure to :star2: my repo!

![screenshot](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/screenshot.png)

# August 2021

* Changed sidebar to a `vertical-stack`, easier to add various cards
* `markdown` → `custom:button-card`, faster and easier to style
* Theme now only applies to dashboard and not other sections
* Optimization of styles and cross-browser compatibility
* Workaround for known issues:

  * ~~card-mod randomly not applying markdown styling on 2021.6.0 [#130](https://github.com/thomasloven/lovelace-card-mod/issues/130)~~ <br>`markdown` → `custom:button-card`<br>[ui-lovelace#L52](https://github.com/matt8707/hass-config/blob/c5ef7a9130cc347d5785773fda7437c05dc4bdb2/ui-lovelace.yaml#L52), [themes#L123](https://github.com/matt8707/hass-config/blob/c5ef7a9130cc347d5785773fda7437c05dc4bdb2/include/themes.yaml#L123), [button_card_templates#L137](https://github.com/matt8707/hass-config/blob/c5ef7a9130cc347d5785773fda7437c05dc4bdb2/button_card_templates.yaml#L137)

  * ~~swipe-card not updating size unless resizing window [#32](https://github.com/bramkragten/swipe-card/issues/32) [#147](https://github.com/thomasloven/lovelace-layout-card/issues/147)~~ <br>`horizontal-stack` and `margin: 0` <br>[ui-lovelace#L284](https://github.com/matt8707/hass-config/blob/c5ef7a9130cc347d5785773fda7437c05dc4bdb2/ui-lovelace.yaml#L284), [themes#L110](https://github.com/matt8707/hass-config/blob/c5ef7a9130cc347d5785773fda7437c05dc4bdb2/include/themes.yaml#L110), [button_card_templates#L769](https://github.com/matt8707/hass-config/blob/c5ef7a9130cc347d5785773fda7437c05dc4bdb2/button_card_templates.yaml#L769)

*If you want, you can [buy me a beer](https://www.buymeacoffee.com/matt8707)* :blush:

<details>

  ---

  <summary>June 2021</summary>

  ### June 2021

  While picture elements is still a valid card for layouts that doesn't follow a specific grid, this dashboard does. Instead of placing button cards using coordinates, it's now placed onto a grid that is responsive.

  **Layout** `custom:layout-card`
  * CSS grid everything and as a bonus...
  * Mobile and portrait dashboards

  https://user-images.githubusercontent.com/36163594/120789256-ad825000-c531-11eb-97c2-18904c48efdd.mp4

  **Buttons** `custom:button-card`
  * Loader template doesn't need any `input_boolean` helpers anymore 
  * Icons will only animate on state change to prevent all icons animating on dashboard refresh
  * Some entity checks for undefined entities, no errors on restarts
  * Added a bounce effect to the button when pressed

  **Theme** `custom:card-mod`
  * Reworked themes with focus on performance
  * Wrote a tool to help with styling [card-mod-helper](https://matt8707.github.io/card-mod-helper/)

  **Deprecated**
  *If you're looking for picture elements, browse this repository before March 2021 [https://github.com/matt8707/hass-config/tree/c9dd19e04bd4fde2322e610a42f4e246b58ee19a](https://github.com/matt8707/hass-config/tree/c9dd19e04bd4fde2322e610a42f4e246b58ee19a)*

  **Includes**
  Since this configuration is split into several yaml files, I'm using [lovelace-gulp-watch](https://github.com/akmolina28/lovelace-gulp-watch), which auto updates lovelace if an included file is changed.
</details>

---

## Features

* A different take on designing a [Lovelace UI](https://www.home-assistant.io/lovelace/) using [custom:layout-card](https://github.com/thomasloven/lovelace-layout-card)
* Achieving a less cluttered interface by displaying [more information](https://github.com/thomasloven/hass-browser_mod#popup) on a [long press](https://www.home-assistant.io/lovelace/picture-elements/#hold_action)
* Loading wheel for slow responding entities such as booting a computer.
* [Adding sounds](https://github.com/thomasloven/hass-browser_mod#media_player) to the UI using automations listening for events
* [CSS Animations](https://www.w3schools.com/css/css3_animations.asp) based on state

![animations](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/animations.gif)

### The sidebar

* Time and date with greeting based on time of day
* Lights and switches that are on, using natural language
* Temperature with emoji based on weather conditions
* Important calendar information
* Other conditional alerts

### Sidebar footer

The three icons at the bottom in order:

* Card to control [robot vacuum](https://www.mi-store.se/en/smart-homes/robot-vacuum-cleaners/xiaomi-robot-vacuum-2-roborock)
* Monitor [Home Assistant](https://home-assistant.io/), [tablet](https://www.samsung.com/us/mobile/tablets/galaxy-tab-a/galaxy-tab-a-10-1-2019-32gb-black-wi-fi-sm-t510nzkaxar/) and [Network Attached Storage](https://www.synology.com/products/DS918+)
* Lists available HACS updates and release notes for Home Assistant

![info](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_2.png)

### Media

Conditionally displaying media player controls based on last active device such as [Apple TV](https://www.home-assistant.io/integrations/apple_tv/), Spotify, [Google Nest Mini](https://www.home-assistant.io/integrations/cast/). If nothing is active for 15 minutes then a poster of last downloaded movie/episode is shown ([Radarr](https://github.com/Radarr/Radarr)/[Sonarr](https://github.com/Sonarr/Sonarr)). Swipe to reveal other than last active media players.

![media](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/media.gif)

### Lights and sensors

All [Philips Hue](https://www2.meethue.com) lights with [sensors](https://www2.meethue.com/en-gb/p/hue-motion-sensor/8718696743171) in hallway, bathroom and walk-in closet.

![light](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/light.gif)


### Switches

* [SwitchBot](https://www.switch-bot.com/bot) to cold boot computer with a raspberry as a [hub](https://github.com/OpenWonderLabs/python-host). Numerous shell commands to monitor and control macOS
* [Belkin WeMo Switch](https://www.belkin.com/) to control studio monitors (speakers) with automations to apply [EQ calibration](https://www.sonarworks.com/reference) and volume control through AppleScript
* Control a pedestal fan, using [Belkin WeMo Switch](https://www.belkin.com/) and hue motion sensor temperature data to automate on summer nights
* [Broadlink](https://www.ibroadlink.com/products/ir+rf) to control fan and air purifier with IR and [Gosund Smart Wi-Fi Plug](https://www.gosund.com/download/smart_plug/127.html) for power/state

![info_light](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/info_light_2.png)


### Custom icons

I made some custom icons located in `www/custom_icons.js`. If you want to make your own I recommend reading the [material design principles](https://material.io/design/iconography/system-icons.html#design-principles).

![custom_icons](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/custom_icons.png)


### Misc

![vacuum](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/vacuum_2.png)

![misc](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/misc_2.png)

![tracker](https://raw.githubusercontent.com/matt8707/hass-config/master/www/img/tracker_updates.png)

***

**Home Assistant Community Topic**  
[https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594](https://community.home-assistant.io/t/a-different-take-on-designing-a-lovelace-ui/162594)
