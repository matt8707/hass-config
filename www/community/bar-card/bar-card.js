class BarCard extends HTMLElement {
  constructor () {
    super()
    this.attachShadow({ mode: 'open' })
  }
  setConfig (config) {
    // Default Card variables
    const initialConfig = Object.assign({}, config)

    if (!config.height) config.height = '40px'
    if (!config.direction) config.direction = 'right'
    if (!config.rounding) config.rounding = '3px'
    if (!config.title_position) config.title_position = 'left'
    if (!config.icon_position) config.icon_position = 'off'
    if (!config.indicator) config.indicator = 'auto'
    if (!config.saturation) config.saturation = '50%'
    if (!config.animation) config.animation = 'auto'
    if (!config.speed) config.speed = 1000
    if (!config.delay) config.delay = 5000
    if (!config.min) config.min = 0
    if (!config.max) config.max = 100
    if (!config.padding) config.padding = '4px'
    if (!config.align) config.align = 'center'
    if (!config.color) config.color = 'var(--custom-bar-card-color, var(--primary-color))'
    if (!config.tap_action) config.tap_action = 'info'
    if (!config.show_value) config.show_value = true
    if (!config.limit_value) config.limit_value = false
    if (!config.show_minmax) config.show_minmax = false
    if (!config.title) config.title = false
    if (!config.severity) config.severity = false
    if (!config.target) config.target = false
    if (!config.attribute) config.attribute = false
    if (!config.icon) config.icon = false
    if (!config.charge_entity) config.charge_entity = false
    if (!config.unit_of_measurement) config.unit_of_measurement = false
    if (!config.card_style) config.card_style = false
    if (!config.icon_style) config.icon_style = false
    if (!config.title_style) config.title_style = false
    if (!config.value_style) config.value_style = false
    if (!config.minmax_style) config.minmax_style = false
    if (!config.background_style) config.background_style = false
    if (!config.visibility) config.visibility = false
    if (!config.decimal) config.decimal = false

    // Check entity types
    let updateArray
    if (config.entities) {
        let newArray = []
        config.entities.forEach(section => {
          let type = typeof(section)
          if (type == 'string'){
            let constructObject = {"entity":section}
            newArray.push(constructObject)
            updateArray = true
          } else if (type == 'object') {
            newArray.push(section)
            updateArray = true
          }
        })
        if(updateArray == true){
          config.entities = newArray;
        }
    } else if (config.entity) {
      config.entities = [{"entity":config.entity}]
    }

    // Check if title position is inside
    if (!config.width) {
      switch (config.title_position) {
        case 'inside':
        case 'top':
        case 'bottom':
        case 'off':
          config.width = '100%'
          break
        case 'left':
        case 'right':
          config.width = '70%'
      }
      switch (config.icon_position) {
        case 'top':
        case 'bottom':
          config.width = '100%'
          break
        case 'left':
        case 'right':
          config.width = 'calc(100% - 50px)'
          break
        case 'inside':
        case 'off':
          switch (config.title_position) {
            case 'inside':
            case 'top':
            case 'bottom':
            case 'off':
              config.width = '100%'
              break
            case 'left':
            case 'right':
              config.width = '70%'
          }
      }
    }

    if (config.card_style !== false) var cardStyle = this._customStyle(config.card_style)

    // Define card container
    let cardContainer = document.createElement('ha-card')
    let cardContainerStyle = document.createElement('style')
    cardContainerStyle.textContent = `
      ha-card {
        padding: calc(${config.padding} / 2);
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        ${cardStyle}
      }
    `
    // For each entity in entities list create cardElements
    this._configArray = []
    this._initialConfigArray = []
    for (let i = 0; i <= config.entities.length-1; i++){
      const entityName = config.entities[i].entity.split('.')
      this._configArray[i] = Object.assign({},config)
      this._initialConfigArray[i] = Object.assign({}, initialConfig)
      Object.keys(config).forEach(section => {
        const config = this._configArray[i]
        const entities = config.entities[i]
        const initialConfig = this._initialConfigArray[i]
        if (entities[section] !== undefined) {
          config[section] = entities[section]
          initialConfig[section] = entities[section]
        }
      })
      cardContainer.appendChild(this._cardElements(this._configArray[i], entityName[0]+'_'+entityName[1]+'_'+i, config.entities[i].entity))
    }

    // Add card container to root
    this.shadowRoot.appendChild(cardContainer)
    this.shadowRoot.appendChild(cardContainerStyle)

    // For each entity in entities list update entity.
    if (this._hass) {
      for(let i=0; i <= config.entities.length-1; i++){
        let entityName = config.entities[i].entity.split('.')
        this._updateEntity(config.entities[i].entity, entityName[0]+'_'+entityName[1]+'_'+i, i)
      }
    }

    // Set config for this card.
    this._config = config
  }

  // On hass update
  set hass (hass) {
    this._hass = hass
    const config = this._config
    for(let i=0; i <= config.entities.length-1; i++){
      let entityName = config.entities[i].entity.split('.')
      this._updateEntity(config.entities[i].entity, entityName[0]+'_'+entityName[1]+'_'+i, i)
    }
  }

  // Create card elements
  _cardElements(config, id, entity) {
    const card = document.createElement('div')
    card.id = 'card_'+id
    const container = document.createElement('div')
    container.id = 'container_'+id
    const background = document.createElement('div')
    background.id = 'background_'+id
    const backgroundBar = document.createElement('div')
    backgroundBar.id = 'backgroundBar_'+id
    const bar = document.createElement('div')
    bar.id = 'bar_'+id
    const contentBar = document.createElement('div')
    contentBar.id = 'contentBar_'+id
    var icon = document.createElement('ha-icon')
    icon.id = 'icon_'+id
    var title = document.createElement('div')
    title.id = 'title_'+id
    var titleBar = document.createElement('div')
    titleBar.id = 'titleBar_'+id
    const valueContainer = document.createElement('div')
    valueContainer.id = 'value_container_'+id
    const minValue = document.createElement('div')
    minValue.id = 'min_value_'+id
    const value = document.createElement('div')
    value.id = 'value_'+id
    const maxValue = document.createElement('div')
    maxValue.id = 'max_value_'+id
    var chargeBar = document.createElement('div')
    chargeBar.id = 'chargeBar_'+id
    var targetBar = document.createElement('div')
    targetBar.id = 'targetBar_'+id
    var targetMarker = document.createElement('div')
    targetMarker.id = 'targetMarker_'+id
    var indicatorContainer = document.createElement('div')
    indicatorContainer.id = 'indicatorContainer_'+id
    var indicatorBar = document.createElement('div')
    indicatorBar.id = 'indicatorBar_'+id
    var indicator = document.createElement('div')
    indicator.id = 'indicator_'+id

    // Start building card
    background.appendChild(backgroundBar)
    background.appendChild(bar)
    bar.appendChild(targetMarker)
    background.appendChild(targetBar)
    background.appendChild(chargeBar)
    indicatorContainer.appendChild(indicator)
    switch (config.align) {
      case 'center':
      case 'center-split':
      case 'left-split':
      case 'right-split':
        indicatorBar.appendChild(indicatorContainer)
        background.appendChild(indicatorBar)
        break
      default:
        background.appendChild(indicatorContainer)
    }
    switch (config.icon_position) {
      case 'inside':
      case 'off':
        contentBar.appendChild(icon)
        break
      case 'left':
      case 'right':
      case 'top':
      case 'bottom':
        titleBar.appendChild(icon)
        container.appendChild(titleBar)
    }
    switch (config.title_position) {
      case 'left':
      case 'right':
      case 'top':
      case 'bottom':
        if (config.title_position != 'inside') {
          titleBar.appendChild(title)
          container.appendChild(titleBar)
        }
        container.appendChild(background)
        break
      case 'inside':
        contentBar.appendChild(title)
        container.appendChild(contentBar)
        container.appendChild(background)
        break
      case 'off':
        container.appendChild(background)
    }
    contentBar.appendChild(valueContainer)
    if (config.show_minmax == true) {
      valueContainer.appendChild(minValue)
    }
    valueContainer.appendChild(value)
    if (config.show_minmax == true) {
      valueContainer.appendChild(maxValue)
    }
    background.appendChild(contentBar)
    card.appendChild(container)
    card.appendChild(this._styleElements(config, id))
    switch (config.tap_action) {
      case 'info':
        card.addEventListener('click', event => {
          this._showAttributes('hass-more-info', { entityId: entity })
        })
        break
      case 'service':
        card.addEventListener('click', event => {
          this._serviceCall(config.service_options.domain, config.service_options.service, config.service_options.data)
        })
        break
    }

    return card
  }

  // Create style elements
  _styleElements(config, id) {
    const style = document.createElement('style');
    if (config.value_style !== false) var valueStyle = this._customStyle(config.value_style)
    if (config.minmax_style !== false) var minmaxStyle = this._customStyle(config.minmax_style)
    if (config.title_style !== false) var titleStyle = this._customStyle(config.title_style)
    if (config.icon_style !== false) var iconStyle = this._customStyle(config.icon_style)
    if (config.background_style !== false) var backgroundStyle = this._customStyle(config.background_style)

    // Sets position of the titleBar
    let titleAlign
    let titleWidth
    let titleflexDirection
    switch (config.title_position) {
      case 'left':
        titleWidth = 'width: calc(100% - ' + config.width + ');'
        titleAlign = 'justify-content: flex-start;'
        titleflexDirection = 'flex-direction: row;'
        break
      case 'right':
        titleWidth = 'width: calc(100% - ' + config.width + ');'
        titleAlign = 'justify-content: flex-start;'
        titleflexDirection = 'flex-direction: row-reverse;'
        break
      case 'top':
        titleWidth = 'width: 100%;'
        titleAlign = 'justify-content: center;'
        titleflexDirection = 'flex-direction: column;'
        break
      case 'bottom':
        titleWidth = 'width: 100%;'
        titleAlign = 'justify-content: center;'
        titleflexDirection = 'flex-direction: column-reverse;'
        break
    }
    switch (config.icon_position) {
      case 'left':
        titleWidth = 'width: calc(100% - ' + config.width + ');'
        if (config.title_position == 'off' || config.title_position == 'inside') titleAlign = 'justify-content: center;'
        else titleAlign = 'justify-content: flex-start;'
        titleflexDirection = 'flex-direction: row;'
        break
      case 'right':
        titleWidth = 'width: calc(100% - ' + config.width + ');'
        if (config.title_position == 'off' || config.title_position == 'inside') titleAlign = 'justify-content: center;'
        else titleAlign = 'justify-content: flex-start;'
        titleflexDirection = 'flex-direction: row-reverse;'
        break
      case 'top':
        titleWidth = 'width: 100%;'
        titleAlign = 'justify-content: center;'
        titleflexDirection = 'flex-direction: column;'
        break
      case 'bottom':
        titleWidth = 'width: 100%;'
        titleAlign = 'justify-content: center;'
        titleflexDirection = 'flex-direction: column-reverse;'
        break
    }

    // Set value flex direction based on card direction
    let valueflexDirection
    switch (config.direction) {
      case 'left':
      case 'left-reverse':
        valueflexDirection = 'flex-direction: row-reverse;'
        break
      case 'right':
      case 'right-reverse':
        valueflexDirection = 'flex-direction: row;'
        break
      case 'up':
      case 'up-reverse':
        valueflexDirection = 'flex-direction: column-reverse;'
        break
      case 'down':
      case 'down-reverse':
        valueflexDirection = 'flex-direction: column;'
        break
    }

    // Set marker direction based on card direction
    let markerDirection
    let barFrom
    let insideWhitespace
    switch (config.direction) {
      case 'left':
      case 'left-reverse':
        barFrom = 'left'
        markerDirection = 'right'
        insideWhitespace = 'nowrap'
        break
      case 'right':
      case 'right-reverse':
        barFrom = 'right'
        markerDirection = 'left'
        insideWhitespace = 'nowrap'
        break
      case 'up':
      case 'up-reverse':
        barFrom = 'top'
        markerDirection = 'bottom'
        break
      case 'down':
      case 'down-reverse':
        barFrom = 'bottom'
        markerDirection = 'top'
        break
    }

    // Set marker style based on bar direction
    let markerStyle
    if (barFrom == 'left' || barFrom == 'right') {
      markerStyle = `
        ${markerDirection}: var(--targetMarker-percent);
        height: ${config.height};
        border-left: 2px dashed var(--bar-color);
      `
    } else {
      markerStyle = `
        ${markerDirection}: var(--targetMarker-percent);
        width: 100%;
        border-top: 2px dashed var(--bar-color);
      `
    }

    // Set title style based on title position
    let titlePositionStyle
    if (config.title_position == 'inside') {
      titlePositionStyle = `
      width: calc(100% - 8px);
      font-weight: bold;
      color: #FFF;
      text-shadow: 1px 1px #0007;
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: ${insideWhitespace};
      `
    } else {
      titlePositionStyle = `
      color: var(--primary-text-color);
      padding-left: 10px;
      padding-right: 10px;
      padding-top: 4px;
      padding-bottom: 4px;
      text-overflow: ellipsis;
      overflow: hidden;
      `
    }
    let iconMarginStyle = ''
    if (config.icon_position !== 'inside' && config.title_position !== 'off' && config.title_position !== 'inside') {
      iconMarginStyle = `
      margin-left: 8px;
      `
    }

    let justifyContent
    let alignItems
    let textAlign
    let flexDirection
    switch (config.align) {
      case 'right':
        flexDirection = 'column'
        textAlign = 'right'
        alignItems = 'flex-end'
        justifyContent = 'center'
        break
      case 'left':
        flexDirection = 'column'
        justifyContent = 'center'
        alignItems = 'flex-start'
        textAlign = 'left'
        break
      case 'top':
        flexDirection = 'column'
        justifyContent = 'flex-start'
        alignItems = 'center'
        textAlign = 'center'
        break
      case 'top-split':
        flexDirection = 'row'
        justifyContent = 'space-between'
        alignItems = 'flex-start'
        if (config.icon_position != 'off') textAlign = 'center'
        if (config.icon_position == 'inside') textAlign = 'center'
        else textAlign = 'left'
        break
      case 'bottom':
        flexDirection = 'column'
        justifyContent = 'flex-end'
        alignItems = 'center'
        textAlign = 'center'
        break
      case 'bottom-split':
        flexDirection = 'row'
        justifyContent = 'space-between'
        alignItems = 'flex-end'
        if (config.icon_position != 'off') textAlign = 'center'
        if (config.icon_position == 'inside') textAlign = 'center'
        else textAlign = 'left'
        break
      case 'split':
        alignItems = 'center'
        flexDirection = 'row'
        justifyContent = 'space-between'
        if (config.icon_position != 'off') textAlign = 'center'
        if (config.icon_position == 'inside') textAlign = 'center'
        else textAlign = 'left'
        break
      case 'left-split':
        flexDirection = 'column'
        justifyContent = 'space-between'
        alignItems = 'flex-start'
        break
      case 'right-split':
        flexDirection = 'column'
        justifyContent = 'space-between'
        alignItems = 'flex-end'
        textAlign = 'right'
        break
      case 'center':
        flexDirection = 'column'
        textAlign = 'center'
        justifyContent = 'center'
        alignItems = 'center'
        break
      case 'center-split':
        flexDirection = 'column'
        textAlign = 'center'
        justifyContent = 'space-between'
        alignItems = 'center'
    }
    if (config.title_position != 'inside') textAlign = 'left'

    // Set CSS styles
    let haCardWidth
    if (config.columns) haCardWidth = Math.trunc(100 / Number(config.columns))
    else haCardWidth = 100;

    style.textContent = `
      #card_${id} {
        padding: ${config.padding};
        width: calc(${haCardWidth}% - (${config.padding} * 2));
        --card-display: visible;
        display: var(--card-display);
      }
      #container_${id} {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        ${titleflexDirection}
      }
      #background_${id} {
        cursor: pointer;
        position: relative;
        display: flex;
        flex-direction: var(--flex-direction);
        width: ${config.width};
        height: ${config.height};
      }
      #contentBar_${id} {
        position: relative;
        display: flex;
        flex-direction: ${flexDirection};
        align-items: ${alignItems};
        justify-content: ${justifyContent};
        --padding: 4px;
        height: calc(${config.height} - (var(--padding)*2));
        width: calc(100% - (var(--padding)*2));
        padding: var(--padding);
      }
      #bar_${id}, #backgroundBar_${id}, #targetBar_${id}, #valueBar_${id}, #chargeBar_${id}, #chargeBarColor_${id}, #valueBar_${id}, #indicatorBar_${id} {
        position: absolute;
        height: 100%;
        width: 100%;
        border-radius: ${config.rounding};
      }
      #backgroundBar_${id} {
        background: var(--bar-color);
        filter: brightness(0.5);
        opacity: 0.25;
        ${backgroundStyle}
      }
      #bar_${id} {
        background: linear-gradient(to ${barFrom}, var(--bar-color) var(--bar-percent), #0000 var(--bar-percent), #0000 var(--bar-percent));
      }
      #chargeBar_${id} {
        background: linear-gradient(to ${barFrom}, #FFF0 var(--bar-percent), var(--bar-color) var(--bar-percent), var(--bar-color) var(--bar-charge-percent), #FFF0 var(--bar-charge-percent));
        filter: var(--bar-charge-brightness);
        opacity: var(--bar-charge-opacity);
      }
      #targetBar_${id} {
        display: var(--target-display);
        filter: brightness(0.66);
        opacity: 0.33;
        background: linear-gradient(to ${barFrom}, #FFF0 var(--targetBar-left-percent), var(--bar-color) var(--targetBar-left-percent), var(--bar-color) var(--targetBar-right-percent), #FFF0 var(--targetBar-right-percent));
      }
      #targetMarker_${id} {
        display: var(--target-display);
        position: absolute;
        background: #FFF0;
        ${markerStyle}
        filter: brightness(0.75);
      }
      #icon_${id} {
        display: var(--icon-display);
        position: relative;
        font-weight: bold;
        color: #FFF;
        filter: drop-shadow(1px 1px #0005);
        ${iconMarginStyle}
        ${iconStyle}
      }
      #title_${id} {
        position: relative;
        text-align: ${textAlign};
        ${titlePositionStyle}
        ${titleStyle};
      }
      #value_container_${id} {
        position: relative;
        display: ${config.show_minmax ? 'flex' : 'contents'};
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        ${config.show_minmax ? 'text-align: center;' : ''};
        ${valueflexDirection};
      }
      #value_${id}, #min_value_${id}, #max_value_${id} {
        position: relative;
        font-weight: bold;
        font-size: 13px;
        color: #FFF;
        text-shadow: 1px 1px #0007;
        white-space: nowrap;
        ${config.show_minmax ? 'flex-grow: 1;' : ''};
        ${config.show_minmax ? 'text-align: center;' : ''};
      }
      #value_${id} {
        ${valueStyle}
      }
      #min_value_${id}, #max_value_${id} {
        ${minmaxStyle}
      }
      #titleBar_${id} {
        position: relative;
        display: flex;
        align-items: center;
        height: 32px;
        ${titleAlign}
        ${titleWidth}
        ${titleStyle}
      }
      #indicatorBar_${id} {
        display: flex;
        --flex-direction: row;
        flex-direction: var(--flex-direction);
        align-items: var(--flex-align);
        justify-content: var(--justify-content);
      }
      #indicator_${id} {
        position: relative;
        filter: brightness(0.75);
        color: var(--bar-color);
        --padding-left: 0px;
        padding-left: var(--padding-left);
        --padding-right: 0px;
        padding-right: var(--padding-right);
      }
      #indicatorContainer_${id} {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
      }
    `
    return style
  }

  // Create style string from CSS options
  _customStyle (style) {
    let styleString = ''
    Object.keys(style).forEach(section => {
      styleString = styleString + section + ':' + style[section] + '; '
    })
    return styleString
  }

  // Translates entity percentage to bar percentage
  _translatePercent (value, min, max, index, entity) {
    const config = this._configAttributeCheck(entity, index)
    switch (config.direction) {
      case 'right-reverse':
      case 'left-reverse':
      case 'up-reverse':
      case 'down-reverse':
        return 100 - (100 * (value - min) / (max - min))
      default:
        return 100 * (value - min) / (max - min)
    }
  }

  // Map range function
  _mapRange (num, in_min, in_max, out_min, out_max) {
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  }

  // Returns color based on severity array
  _computeSeverity (stateValue, sections, hass) {
    let numberValue = Number(stateValue)
    let color
    sections.forEach(section => {
      let actualValue = this._valueEntityCheck(section.value, hass)
      if (numberValue <= actualValue && !color) {
        color = section.color
      }
    })
    return color
  }

  // Returns icon based on severity array
  _computeSeverityIcon (stateValue, sections, hass) {
    let numberValue = Number(stateValue)
    let icon
    sections.forEach(section => {
      let actualValue = this._valueEntityCheck(section.value, hass)
      if (numberValue <= actualValue && !icon) {
        icon = section.icon
      }
    })
    return icon
  }

  // Check if value is NaN, otherwise assume it's an entity
  _valueEntityCheck (value, hass) {
    if (isNaN(value)) {
      const valueArray = value.split('.')
      if (valueArray[2] == 'attributes') {
        if (this._hass.states[valueArray[0]+'.'+valueArray[1]] == undefined) {
          throw new Error('Invalid target, min or max entity')
        } else {
          const hassObject = hass.states[valueArray[0]+'.'+valueArray[1]]
          const attributes = hassObject[valueArray[2]]
          const attribute = attributes[valueArray[3]]
          return attribute
        }
      } else {
        if (this._hass.states[value] == undefined) throw new Error('Invalid target, min or max entity')
        else return hass.states[value].state
      }
    } else {
      return value
    }
  }

  // Check if min is defined otherwise check for min attribute
  _minCheck (entity, hass, index) {
    const config = this._configAttributeCheck(entity, index)
    if (hass.states[entity].attributes.min && config.entity_config == true) return hass.states[entity].attributes.min
    else return config.min
  }

  // Check if max is defined otherwise check for max attribute
  _maxCheck (entity, hass, index) {
    const config = this._configAttributeCheck(entity, index)
    if (hass.states[entity].attributes.max && config.entity_config == true) return hass.states[entity].attributes.max
    else return config.max
  }

  _serviceCall (domain, service, data) {
    const hass = this._hass
    hass.callService(domain, service, data)
  }

  // Press action
  _showAttributes (type, detail, options) {
    const root = this.shadowRoot
    options = options || {}
    detail = (detail === null || detail === undefined) ? {} : detail
    const event = new Event(type, {
      bubbles: options.bubbles === undefined ? true : options.bubbles,
      cancelable: Boolean(options.cancelable),
      composed: options.composed === undefined ? true : options.composed
    })
    event.detail = detail
    root.dispatchEvent(event)
    return event
  }

  // Update bar percentages
  _updateBar (entityState, hass, id, entity, index) {
    const minValue = this._valueEntityCheck(this._minCheck(entity, hass, index), hass)
    const maxValue = this._valueEntityCheck(this._maxCheck(entity, hass, index), hass)
    const barElement = this.shadowRoot.getElementById('bar_'+id)

    if (!isNaN(entityState)) {
      barElement.style.setProperty('--bar-percent', `${this._translatePercent(entityState, minValue, maxValue, index, entity)}%`)
      barElement.style.setProperty('--bar-charge-percent', `${this._translatePercent(entityState, minValue, maxValue, index, entity)}%`)
    } else {
      barElement.style.setProperty('--bar-percent', `100%`)
      barElement.style.setProperty('--bar-charge-percent', `100%`)
    }
  }

  // Create animation
  _updateAnimation (entityState, configDuration, configStop, id, entity, index) {
    const config = this._configAttributeCheck(entity, index)
    const root = this.shadowRoot
    const hass = this._hass
    const element = root.getElementById('chargeBar_'+id)
    let configDirection = this._animationDirection[id]

    const minValue = this._valueEntityCheck(this._minCheck(entity, hass, index), hass)
    const maxValue = this._valueEntityCheck(this._maxCheck(entity, hass, index), hass)

    let currentPercent = this._translatePercent(entityState, minValue, maxValue, index, entity)
    let totalFrames = currentPercent * 3 + (config.delay / (config.speed / 250) / 3)
    let scaledPercent = currentPercent * 3

    if (configStop == true) {
      configDuration = 0
    }

    let options = {
      iterations: Infinity,
      iterationStart: 0,
      delay: 0,
      endDelay: 0,
      direction: 'normal',
      duration: configDuration,
      fill: 'both'
    }

    switch (config.direction) {
      case 'left-reverse':
      case 'right-reverse':
      case 'up-reverse':
      case 'down-reverse':
        if (configDirection == 'normal') configDirection = 'reverse'
        else configDirection = 'normal'
    }
    let keyframes = []
    let i = scaledPercent
    if (configDirection == 'normal') {
      for (; i <= totalFrames;) {
        let opacity = this._mapRange(i / 3, currentPercent, currentPercent + 25, 0.5, 0)
        let keyframe = {'--bar-charge-percent': i / 3 + '%', '--bar-percent': currentPercent + '%', '--bar-charge-opacity': opacity}
        keyframes.push(keyframe)
        i++
      }
      element.style.setProperty('--bar-charge-brightness','brightness(1)')
    }
    if (configDirection == 'reverse') {
      for (; i <= totalFrames;) {
        const reversePercent = currentPercent - ((i - scaledPercent) / 3)
        let opacity = this._mapRange(i / 3, currentPercent, currentPercent + 25, 0.5, 0)
        let keyframe = {'--bar-charge-percent': currentPercent + '%', '--bar-percent': reversePercent + '%', '--bar-charge-opacity': opacity}
        keyframes.push(keyframe)
        i++
      }
      element.style.setProperty('--bar-charge-brightness','brightness(0.25)')
    }
    const animation = element.animate(keyframes, options)
    animation.id = id
    return animation
  }

  // Sets position and direction of the indicator
  _updateIndicator (config, position, direction, id, color) {
    const root = this.shadowRoot
    const indicatorElement = root.getElementById('indicator_'+id)
    const indicatorBarElement = root.getElementById('indicatorBar_'+id)

    indicatorElement.style.setProperty('--bar-color', color)

    switch (direction) {
      case 'up':
        indicatorElement.textContent = '▲'
        switch (position) {
          case 'left':
            indicatorElement.style.setProperty('--padding-left','4px')
            break
          case 'right':
          case 'auto':
            root.getElementById('background_'+id).style.setProperty('--flex-direction','row-reverse')
            switch (config.align) {
              case 'center':
              case 'center-split':
              case 'left-split':
              case 'right-split':
                indicatorBarElement.style.setProperty('--justify-content','flex-end')
            }
            indicatorElement.style.setProperty('--padding-right','4px')
            indicatorElement.style.setProperty('--padding-left','0px')
            break
          case 'top':
          case 'auto-vertical':
            indicatorBarElement.style.setProperty('--justify-content','flex-start')
            indicatorBarElement.style.setProperty('--flex-direction','column')
            break
          case 'bottom':
            indicatorBarElement.style.setProperty('--justify-content','flex-end')
            indicatorBarElement.style.setProperty('--flex-direction','column')
        }
        break
      case 'down':
        indicatorElement.textContent = '▼'
        switch (position) {
          case 'right':
            root.getElementById('background_'+id).style.setProperty('--flex-direction','row-reverse')
            indicatorElement.style.setProperty('--padding-right','4px')
            indicatorElement.style.setProperty('--padding-left','0px')
            break
          case 'left':
          case 'auto':
            root.getElementById('background_'+id).style.setProperty('--flex-direction','row')
            switch (config.align) {
              case 'center':
              case 'center-split':
              case 'left-split':
              case 'right-split':
                indicatorBarElement.style.setProperty('--justify-content','flex-start')
            }
            indicatorElement.style.setProperty('--padding-left','4px')
            indicatorElement.style.setProperty('--padding-right','0px')
            break
          case 'bottom':
          case 'auto-vertical':
            indicatorBarElement.style.setProperty('--justify-content','flex-end')
            indicatorBarElement.style.setProperty('--flex-direction','column')
          case 'top':
            indicatorBarElement.style.setProperty('--justify-content','flex-start')
            indicatorBarElement.style.setProperty('--flex-direction','column')
        }
        break
      case 'off':
        indicatorElement.textContent = ''
        indicatorElement.style.setProperty('--padding-left','0px')
        indicatorElement.style.setProperty('--padding-right','0px')
    }
  }

  // Scale the target bar size
  _updateTargetBar (entityState, target, color, id, entity, index) {
    const config = this._configAttributeCheck(entity, index)
    const root = this.shadowRoot
    const targetBarElement = root.getElementById('targetBar_'+id)
    const targetMarkerElement = root.getElementById('targetMarker_'+id)
    if (config.target !== false) {
      const hass = this._hass
      const minValue = this._valueEntityCheck(this._minCheck(entity, hass, index), hass, index)
      const maxValue = this._valueEntityCheck(this._maxCheck(entity, hass, index), hass, index)
      let currentPercent = this._translatePercent(entityState, minValue, maxValue, index, entity)
      let targetPercent = this._translatePercent(target, minValue, maxValue, index, entity)
      let initialPercent
      let diffPercent
      if (currentPercent > targetPercent) {
        initialPercent = targetPercent
        diffPercent = currentPercent
      } else {
        initialPercent = currentPercent
        diffPercent = targetPercent
      }
      targetBarElement.style.setProperty('--targetBar-left-percent', initialPercent + '%')
      targetBarElement.style.setProperty('--targetBar-right-percent', diffPercent + '%')
      targetBarElement.style.setProperty('--bar-color', color)
      targetMarkerElement.style.setProperty('--targetMarker-percent', targetPercent + '%')
      targetMarkerElement.style.setProperty('--bar-color', color)
    } else {
      targetBarElement.style.setProperty('--target-display', 'none')
      targetMarkerElement.style.setProperty('--target-display', 'none')
    }
  }

  _calculateBarColor (config, entityState, hass) {
    let barColor
    if (config.severity == false) {
      barColor = config.color
    } else {
      barColor = this._computeSeverity(entityState, config.severity, hass)
    }
    return barColor
  }

  // Check entity attribute overrides
  _configAttributeCheck (entity, index) {
    const hass = this._hass
    const config = Object.assign({}, this._configArray[index])
    const entityAttributes = hass.states[entity].attributes
    if (config.entity_config == true) {
      Object.keys(config).forEach(section => {
        if (this._initialConfigArray[index][section] == undefined) {
          if (entityAttributes[section] !== undefined) {
            if (section == 'severity' && typeof(entityAttributes[section]) == 'string') config[section] = JSON.parse(entityAttributes[section])
            else config[section] = entityAttributes[section]
          }
        }
      })
    }
    return config
  }

  // On entity update
  _updateEntity (entity, id, index) {
    const hass = this._hass
    const entityObject = hass.states[entity]
    const root = this.shadowRoot

    // Check if entity exists
    if (entityObject == undefined) {
      root.getElementById('value_'+id).textContent = `Entity doesn't exist.`
      root.getElementById('value_'+id).style.setProperty('color', '#FF0000')
      if (root.getElementById('icon'+id) !== null) {
        root.getElementById('icon_'+id).style.setProperty('--icon-display', 'none')
      }
      if (root.getElementById('titleBar_'+id) !== null) {
        root.getElementById('titleBar_'+id).style.setProperty('display', 'none')
      }
      return
    }
    
    // Define config
    const config = this._configAttributeCheck(entity, index)

    // Define Title
    if (config.title == false) config.title = entityObject.attributes.friendly_name

    // Check for title position config
    if (config.title_position != 'off') root.getElementById('title_'+id).textContent = config.title
    if (!this._entityState) this._entityState = []

    // Define variables that have possible entities
    let configTarget
    if (config.target != false) configTarget = this._valueEntityCheck(config.target, hass)
    const configMin = this._valueEntityCheck(this._minCheck(entity, hass, index), hass)
    const configMax = this._valueEntityCheck(this._maxCheck(entity, hass, index), hass)

    // Define Entity State
    let entityState
    if (entityObject == undefined || entityObject.state == 'unknown' || entityObject.state == 'unavailable') {
      entityState = 'N/A'
    } else {
      if (config.attribute !== false) {
        entityState = entityObject.attributes[config.attribute]
      } else {
        entityState = entityObject.state
      }
      
      if(!isNaN(entityState)){
        entityState = Number(entityState)
      }

      if (config.limit_value) {
        entityState = Math.min(entityState, configMax)
        entityState = Math.max(entityState, configMin)
      }
      
      if (config.decimal !== false) {
        entityState = entityState.toFixed(config.decimal)
      }
    }

    // Define Icon
    if (config.icon_position != 'off') {
      if (config.icon == false) {
        root.getElementById('icon_'+id).icon = entityObject.attributes.icon
      } else { 
        if (config.severity == false || this._computeSeverityIcon(entityState, config.severity, hass) == undefined) {
          root.getElementById('icon_'+id).icon = config.icon
        } else {
          root.getElementById('icon_'+id).icon = this._computeSeverityIcon(entityState, config.severity, hass)
        }
      }
    } else {
      root.getElementById('icon_'+id).style.setProperty('--icon-display', 'none')
    }

    // Set measurement
    let measurement
    if (entityObject == undefined || entityObject.state == 'unknown') measurement = ''
    else if (config.unit_of_measurement !== false) measurement = config.unit_of_measurement
    else measurement = entityObject.attributes.unit_of_measurement || ''

    // Define target, min and max if not defined
    if (!this._entityTarget) this._entityTarget = {}
    if (!this._currentMin) this._currentMin = {}
    if (!this._currentMax) this._currentMax = {}

    // Defined elements
    const barElement = root.getElementById('bar_'+id)

    // Define global currentAnimation
    if (!this._currentAnimation) this._currentAnimation = {}
    if (!this._animationDirection) this._animationDirection = {}

    // Define chargeEntityState
    let chargeEntityState
    if (config.charge_entity !== false) chargeEntityState = hass.states[config.charge_entity].state

    // On entity update
    if (entityState !== this._entityState[id]) {
      const barColor = this._calculateBarColor(config, entityState, hass)

      if (!isNaN(entityState)) {
        if (config.visibility !== false) {
          if (entityState == 'N/A' || config.visibility == true) {
            root.getElementById('card_'+id).style.setProperty('--card-display', 'visible')
          } else {
            if (eval(entityState + " " + config.visibility)) {
              root.getElementById('card_'+id).style.setProperty('--card-display', 'visible')
            } else {
              root.getElementById('card_'+id).style.setProperty('--card-display', 'none')
            }
          }
        }
      }
      this._updateBar(entityState, hass, id, entity, index)
      this._updateTargetBar(entityState, configTarget, barColor, id, entity, index)
      this._entityTarget[id] = configTarget
      barElement.style.setProperty('--bar-color', barColor)
      if (config.show_minmax == true) {
        root.getElementById('min_value_'+id).textContent = `${configMin} ${measurement}`
        root.getElementById('max_value_'+id).textContent = `${configMax} ${measurement}`
      }
      if (config.show_value == true) root.getElementById('value_'+id).textContent = `${entityState} ${measurement}`
      if (config.animation !== 'off') root.getElementById('chargeBar_'+id).style.setProperty('--bar-color', barColor)
      if (entityState == 'N/A') root.getElementById('backgroundBar_'+id).style.setProperty('--bar-color', '#666')
      else root.getElementById('backgroundBar_'+id).style.setProperty('--bar-color', barColor)

      if (config.indicator !== 'off') {
        if (entityState > this._entityState[id]) this._updateIndicator(config, config.indicator, 'up', id, barColor)
        if (entityState < this._entityState[id]) this._updateIndicator(config, config.indicator, 'down', id, barColor)
      }

      // Animation is auto
      if (config.animation == 'auto') {
        const barColor = this._calculateBarColor(config, entityState, hass)
        if (entityState > this._entityState[id]) {
          this._animationDirection[id] = 'normal'
          if (this._currentAnimation[id]) {
            this._currentAnimation[id].pause()
          }
          this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
        }
        if (entityState < this._entityState[id]) {
          this._animationDirection[id] = 'reverse'
          if (this._currentAnimation[id]) {
            this._currentAnimation[id].pause()
          }
          this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
        }
        if (entityState == configMax || entityState == configMin) {
          if (entityState == configMax) {
            barElement.style.setProperty('--bar-color', barColor)
            if (config.indicator !== 'off') this._updateIndicator(config, config.indicator, 'off', id, barColor)
            if (this._currentAnimation[id]) {
              this._currentAnimation[id].pause()
            }
          }
          if (entityState == configMin) {
            if (config.indicator !== 'off') this._updateIndicator(config, config.indicator, 'off', id, barColor)
            if (this._currentAnimation[id]) {
              this._currentAnimation[id].pause()
            }
          }
        }
      }
    }

    // Animation is charge
    if (config.charge_entity !== false) {
      if (!this._currentChargeState) this._currentChargeState = {}
      if (this._currentChargeState[id] !== chargeEntityState || entityState !== this._entityState[id]) {
        const barColor = this._calculateBarColor(config, entityState, hass)
        switch (chargeEntityState) {
          case "charging":
          case "on":
          case "true":
            if (config.indicator !== 'off') this._updateIndicator(config, config.indicator, 'up', id, barColor)
            if (!this._currentAnimation[id] || chargeEntityState != this._currentChargeState || entityState > this._entityState[id]) {
              this._currentChargeState[id] = chargeEntityState
              this._animationDirection[id] = 'normal'
              this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
            }
            break
          case "discharging":
          case "off":
          case "false":
            if (config.indicator !== 'off') this._updateIndicator(config, config.indicator, 'down', id, barColor)
            if (!this._currentAnimation[id] || chargeEntityState != this._currentChargeState || entityState < this._entityState[id]) {
              this._currentChargeState[id] = chargeEntityState
              this._animationDirection[id] = 'reverse'
              this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
            }
            break
        }
      }
    }

    // On target update
    if (config.target != false) {
      if (configTarget != this._entityTarget[id]) {
        const barColor = this._calculateBarColor(config, entityState, hass)
        this._updateTargetBar(entityState, configTarget, barColor, id, entity, index)
        this._entityTarget[id] = configTarget
        if (this._currentAnimation[id] && config.animation !== 'off') this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
      }
    }

    // On min update
    if (configMin !== this._currentMin[id]) {
      this._updateBar(entityState, hass, id, entity, index)
      this._currentMin[id] = configMin
      if (config.target != false) {
        const barColor = this._calculateBarColor(config, entityState, hass)
        this._updateTargetBar(entityState, configTarget, barColor, id, entity, index)
        this._currentMin[id] = configMin
      }
      if (this._currentAnimation[id] && config.animation !== 'off') this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
    }

    // On max update
    if (configMax !== this._currentMax[id]) {
      this._updateBar(entityState, hass, id, entity, index)
      this._currentMax[id] = configMax
      if (config.target != false) {
        const barColor = this._calculateBarColor(config, entityState, hass)
        this._updateTargetBar(entityState, configTarget, barColor, id, entity, index)
        this._currentMax[id] = configMax
      }
      if (this._currentAnimation[id] && config.animation !== 'off') this._currentAnimation[id] = this._updateAnimation(entityState, config.delay, false, id, entity, index)
    }
    this._entityState[id] = entityState
  }

  getCardSize () {
    return 1
  }
}

customElements.define('bar-card', BarCard)

console.info(
  `%cBAR-CARD\n%cVersion: 1.6.1`,
  "color: green; font-weight: bold;",
  ""
);
