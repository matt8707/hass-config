const LitElement = Object.getPrototypeOf(customElements.get("hui-view"))
const html = LitElement.prototype.html
const css = LitElement.prototype.css

class ButtonEntityRow extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
      rows: { type: Array }
    }
  }

  static get styles() {
    return css`
      hui-generic-entity-row {
        margin: var(--ha-themed-slider-margin, initial);
      }
      .flex-box {
        display: flex;
        justify-content: space-evenly;
      }
      paper-button {
        cursor: pointer;
        padding: 8px;
        position: relative;
        display: inline-flex;
        align-items: center;
      }
      .button-default {
        color: var(--paper-item-icon-color);
      }
      .button-active {
        color: var(--paper-item-icon-active-color);
      }
      .button-inactive {
        color: var(--paper-item-icon-color);
      }
      .button-unavailable {
        color: var(--state-icon-unavailable-color);
      }
    `
  }

  render() {
    return html`
      ${this.rows.map(row => {
        return html`
          <div class="flex-box">
            ${row.map(button => {
              const entityState = this.hass.states[button.entityId] || {}
              const icon = this._getCurrentIcon(button, entityState)
              const style = this._getCurrentStyle(button, entityState)
              const iconStyle = this._getCurrentIconStyle(button, entityState)
              const name =
                button.name || (!icon && entityState.attributes ? entityState.attributes.friendly_name : null)

              return html`
                <paper-button
                  @click="${() => this._handleButtonClick(button)}"
                  style="${style}"
                  class="${this._getCurrentClass(entityState)}"
                >
                  ${icon &&
                    html`
                      <ha-icon icon="${icon}" style="${iconStyle} ${name ? "padding-right: 5px;" : ""}"></ha-icon>
                    `}
                  ${name}
                  <paper-ripple center class="${name ? "" : "circle"}"></paper-ripple>
                </paper-button>
              `
            })}
          </div>
        `
      })}
    `
  }

  setConfig(config) {
    if (!config.buttons) throw new Error("missing buttons")
    if (!Array.isArray(config.buttons)) throw new Error("buttons must be an array")
    if (config.buttons.length <= 0) throw new Error("at least one button required")

    if (!Array.isArray(config.buttons[0])) {
      config.buttons = [config.buttons]
    }

    this.config = config
    this.rows = config.buttons.map(row =>
      row.map(item => {
        let button =
          typeof item === "string"
            ? {
                entityId: item,
                icon: undefined,
                stateIcons: undefined,
                stateStyles: undefined,
                stateIconStyles: undefined,
                style: undefined,
                iconStyle: undefined,
                name: undefined,
                service: undefined,
                serviceData: undefined
              }
            : {
                entityId: item.entity,
                icon: item.icon,
                stateIcons: item.state_icons,
                stateStyles: item.state_styles,
                stateIconStyles: item.state_icon_styles,
                style: item.style,
                iconStyle: item.icon_style,
                name: item.name,
                service: item.service,
                serviceData: item.service_data
              }

        if (!button.service) {
          button = { ...button, ...this._withDefaultEntityService(button.entityId) }
        }

        button.serviceData = this._getObjectData(button.serviceData)
        button.stateIcons = this._getObjectData(button.stateIcons)

        return button
      })
    )
  }

  _withDefaultEntityService(entityId) {
    const domain = entityId.split(".")[0]
    let service
    switch (domain) {
      case "automation":
      case "cover":
      case "fan":
      case "input_boolean":
      case "light":
      case "script":
      case "switch":
      case "vacuum":
        service = "toggle"
        break
      case "media_player":
        service = "media_play_pause"
        break
      case "scene":
        service = "turn_on"
        break
      default:
        // No service available, will open the entity state modal if any
        return {
          service: undefined,
          serviceData: undefined
        }
    }

    return {
      service: `${domain}.${service}`,
      serviceData: {
        entity_id: entityId
      }
    }
  }

  _getCurrentIcon(button, entityState) {
    let icon = button.icon

    if (button.stateIcons && button.stateIcons[entityState.state]) {
      icon = button.stateIcons[entityState.state]
    }
    if (!icon && entityState.attributes && entityState.attributes.icon) {
      icon = entityState.attributes.icon
    }

    return icon
  }

  _getCurrentStyle(button, entityState) {
    const mergedStyle = {
      ...this._getObjectData(button.style || {}),
      ...this._getObjectData((button.stateStyles && button.stateStyles[entityState.state]) || {})
    }

    return Object.keys(mergedStyle)
      .reduce((style, rule) => {
        return [...style, `${rule}: ${mergedStyle[rule]};`]
      }, [])
      .join(" ")
  }

  _getCurrentIconStyle(button, entityState) {
    const mergedStyle = {
      ...this._getObjectData(button.iconStyle || {}),
      ...this._getObjectData((button.stateIconStyles && button.stateStyles[entityState.state]) || {})
    }

    return Object.keys(mergedStyle)
      .reduce((style, rule) => {
        return [...style, `${rule}: ${mergedStyle[rule]};`]
      }, [])
      .join(" ")
  }

  _getCurrentClass(entityState) {
    switch (entityState.state) {
      case "on":
        return "button-active"
      case "off":
        return "button-inactive"
      case "unavailable":
        return "button-unavailable"
      default:
        return "button-default"
    }
  }

  _mergeArrayItemsToObject(arrayOfObjects) {
    return arrayOfObjects.reduce((obj, item) => ({ ...obj, ...item }), {})
  }

  _getObjectData(data = {}) {
    return Array.isArray(data) ? this._mergeArrayItemsToObject(data) : data
  }

  _handleButtonClick(button) {
    if (button.service) {
      const service = button.service.split(".")
      this.hass.callService(service[0], service[1], button.serviceData)
    } else if (button.entityId) {
      this._showEntityMoreInfo(button.entityId)
    }
  }

  _showEntityMoreInfo(entityId) {
    const event = new Event("hass-more-info", { bubbles: true, cancelable: false, composed: true })
    event.detail = { entityId }
    this.dispatchEvent(event)
  }
}

customElements.define("button-entity-row", ButtonEntityRow)
