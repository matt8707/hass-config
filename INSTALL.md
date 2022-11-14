# Installation

* Install and configure [HACS](https://hacs.xyz/)

* Within HACS Frontend add the following repositories
  * [button-card](https://github.com/custom-cards/button-card)
  * [card-mod](https://github.com/thomasloven/lovelace-card-mod)
  * [layout-card](https://github.com/thomasloven/lovelace-layout-card)
  * [Swipe Card](https://github.com/bramkragten/swipe-card)

* Manually copy over these files from [matt8707/hass-config](https://github.com/matt8707/hass-config)
  * `ui-lovelace.yaml`
  * `button_card_templates` folder
  * `popup` folder
  * `themes.yaml`
  * `sidebar.yaml`

* In `configuration.yaml` add lines [[docs](https://www.home-assistant.io/lovelace/dashboards/)]

  ```yaml
  frontend: !include themes.yaml
  template: !include sidebar.yaml

  lovelace:
    mode: yaml
    resources:
      - url: /hacsfiles/button-card/button-card.js
        type: module
      - url: /hacsfiles/lovelace-layout-card/layout-card.js
        type: module
      - url: /hacsfiles/swipe-card/swipe-card.js
        type: module
  ```

* [Restart](https://my.home-assistant.io/redirect/server_controls/) Home Assistant

* **Select dark mode and [tablet theme](https://my.home-assistant.io/redirect/profile/) ← DON'T SKIP THIS STEP!**

Then add your entities, [browser_mod](https://github.com/thomasloven/hass-browser_mod) for popups etc...

## FAQ

**Why is the text in popups inverted?**
You didn't select dark mode in your [user profile](https://my.home-assistant.io/redirect/profile/)

**Why does a broken icon appear when I toggle a button?**
You need to add [www/loader.svg](https://github.com/matt8707/hass-config/blob/master/www/loader.svg)

**How do I add fonts?**
Copy [www/fonts.css](https://github.com/matt8707/hass-config/blob/master/www/fonts.css) and read the comment in that file

**How do I get the tilt effect?**
Add [www/vanilla-tilt.min.js](https://github.com/matt8707/hass-config/blob/master/www/vanilla-tilt.min.js)

**In the update popup I get an error saying "marked"**
You need to add [www/marked.min.js](https://github.com/matt8707/hass-config/blob/master/www/marked.min.js) to parse hass release notes

**How do I get popups to work?**
Read the the [browser_mod](https://github.com/thomasloven/hass-browser_mod) documentation
