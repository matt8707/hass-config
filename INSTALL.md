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

**Something isn't working!**</br>
1. Read the documentation for that card e.g. https://github.com/custom-cards/button-card
2. Search forum topic e.g. https://community.home-assistant.io/t/lovelace-button-card/65981
3. This is not a help center for everything Home Assistant

**Why is the text in popups inverted?**</br>
You didn't select dark mode in your [user profile](https://my.home-assistant.io/redirect/profile/)

**Why does a broken icon appear when I toggle a button?**</br>
You need to add [www/loader.svg](https://github.com/matt8707/hass-config/blob/master/www/loader.svg)

**In the update popup I get an error saying "marked"**</br>
Add [www/marked.min.js](https://github.com/matt8707/hass-config/blob/master/www/marked.min.js) and under [resources](https://github.com/matt8707/hass-config/blob/39bbedd2f9de03f8558bd909a8392ae4925f4b09/configuration.yaml#L38) add that file as a module

**How do I get the tilt effect?**</br>
Add [www/vanilla-tilt.min.js](https://github.com/matt8707/hass-config/blob/master/www/vanilla-tilt.min.js) and under [resources](https://github.com/matt8707/hass-config/blob/39bbedd2f9de03f8558bd909a8392ae4925f4b09/configuration.yaml#L39) add that file as a module

**How do I add fonts?**</br>
Copy [www/fonts.css](https://github.com/matt8707/hass-config/blob/master/www/fonts.css) and read the comment in that file and under [resources](https://github.com/matt8707/hass-config/blob/39bbedd2f9de03f8558bd909a8392ae4925f4b09/configuration.yaml#L41) add that file as css

**How do I get popups to work?**</br>
Read the the [browser_mod](https://github.com/thomasloven/hass-browser_mod) documentation
