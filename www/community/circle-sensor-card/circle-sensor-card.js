import {
  LitElement, html
} from 'https://unpkg.com/@polymer/lit-element@^0.5.2/lit-element.js?module';

class CircleSensorCard extends LitElement {
  static get properties() {
    return {
      hass: Object,
      config: Object,
      state: Object,
      dashArray: String
    }
  }

  _render({ state, dashArray, config }) {
    return html`
      <style>
          :host {
            cursor: pointer;
          }

          .container {
            position: relative;
            height: 100%;
            display: flex;
            flex-direction: column;
          }

          .labelContainer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
          }
          
          #label {
            display: flex;
            line-height: 1;
          }
          
          #label.bold {
            font-weight: bold;
          }
          
          #label, #name {
            margin: 1% 0;
          }

          .text, #name {
            font-size: 100%;
          }
          
          .unit {
            font-size: 75%;
          }

      </style>
      <div class="container" id="container" on-click="${() => this._click()}">
        <svg viewbox="0 0 200 200" id="svg">
          <circle id="circle" cx="50%" cy="50%" r="45%"
            fill$="${config.fill || 'rgba(255, 255, 255, .75)'}"
            stroke$="${config.stroke_color || '#03a9f4'}"
            stroke-dasharray$="${dashArray}"
            stroke-width$="${config.stroke_width || 6}" 
            transform="rotate(-90 100 100)"/>
        </svg>
        <span class="labelContainer">
          ${config.name != null ? html`<span id="name">${config.name}</span>` : ''}
          <span id="label" class$="${!!config.name ? 'bold' : ''}">
            <span class="text">
              ${config.attribute ? state.attributes[config.attribute] : state.state}
            </span>
            <span class="unit">
              ${config.show_max
                ? html`&nbsp/ ${config.attribute_max ? state.attributes[config.attribute_max] : config.max}`
                : (config.units ? config.units : state.attributes.unit_of_measurement)}
            </span>
          </span>
        </span>
      </div>
    `;
  }

  _createRoot() {
    const shadow = this.attachShadow({ mode: 'open' })
    if (!this.config.show_card) {
      return shadow;
    }
    const card = document.createElement('ha-card');
    shadow.appendChild(card);
    return card;
  }

  _didRender() {
    this.circle = this._root.querySelector('#circle');
    if (this.config) {
      this._updateConfig();
    }
  }

  setConfig(config) {
    if (!config.entity) {
      throw Error('No entity defined')
    }
    this.config = config;
    if (this.circle) {
      this._updateConfig();
    }
  }

  getCardSize() {
    return 3;
  }

  _updateConfig() {
    const container = this._root.querySelector('.labelContainer');
    container.style.color = 'var(--primary-text-color)';

    if (this.config.font_style) {
      Object.keys(this.config.font_style).forEach((prop) => {
        container.style.setProperty(prop, this.config.font_style[prop]);
      });
    }
  }

  set hass(hass) {
    this.state = hass.states[this.config.entity];

    if (this.config.attribute) {
      if (!this.state.attributes[this.config.attribute] ||
          isNaN(this.state.attributes[this.config.attribute])) {
        console.error(`Attribute [${this.config.attribute}] is not a number`);
        return;
      }
    } else {
      if (!this.state || isNaN(this.state.state)) {
        console.error(`State is not a number`);
        return;
      }
    }

    const state = this.config.attribute
      ? this.state.attributes[this.config.attribute]
      : this.state.state;
    const r = 200 * .45;
    const min = this.config.min || 0;
    const max = this.config.attribute_max
      ? this.state.attributes[this.config.attribute_max]
      : (this.config.max || 100);
    const val = this._calculateValueBetween(min, max, state);
    const score = val * 2 * Math.PI * r;
    const total = 10 * r;
    this.dashArray = `${score} ${total}`;

    let colorStops = {};
    colorStops[min] = this.config.stroke_color || '#03a9f4';
    if (this.config.color_stops) {
      Object.keys(this.config.color_stops).forEach((key) => {
        colorStops[key] = this.config.color_stops[key];
      });
    }

    if (this.circle) {
      const stroke = this._calculateStrokeColor(state, colorStops);
      this.circle.setAttribute('stroke', stroke);
    }
  }

  _click() {
    this._fire('hass-more-info', { entityId: this.config.entity });
  }

  _calculateStrokeColor(state, stops) {
    const sortedStops = Object.keys(stops).map(n => Number(n)).sort((a, b) => a - b);
    let start, end, val;
    const l = sortedStops.length;
    if (state <= sortedStops[0]) {
      return stops[sortedStops[0]];
    } else if (state >= sortedStops[l - 1]) {
      return stops[sortedStops[l - 1]];
    } else {
      for (let i = 0; i < l - 1; i++) {
        const s1 = sortedStops[i];
        const s2 = sortedStops[i + 1];
        if (state >= s1 && state < s2) {
          [start, end] = [stops[s1], stops[s2]];
          if (!this.config.gradient) {
            return start;
          }
          val = this._calculateValueBetween(s1, s2, state);
          break;
        }
      }
    }
    return this._getGradientValue(start, end, val);
  }

  _calculateValueBetween(start, end, val) {
    return (val - start) / (end - start);
  }

  _getGradientValue(colorA, colorB, val) {
    const v1 = 1 - val;
    const v2 = val;
    const decA = this._hexColorToDecimal(colorA);
    const decB = this._hexColorToDecimal(colorB);
    const rDec = Math.floor((decA[0] * v1) + (decB[0] * v2));
    const gDec = Math.floor((decA[1] * v1) + (decB[1] * v2));
    const bDec = Math.floor((decA[2] * v1) + (decB[2] * v2));
    const rHex = this._padZero(rDec.toString(16));
    const gHex = this._padZero(gDec.toString(16));
    const bHex = this._padZero(bDec.toString(16));
    return `#${rHex}${gHex}${bHex}`;
  }

  _hexColorToDecimal(color) {
    let c = color.substr(1);
    if (c.length === 3) {
      c = `${c[0]}${c[0]}${c[1]}${c[1]}${c[2]}${c[2]}`;
    }

    const [r, g, b] = c.match(/.{2}/g);
    return [parseInt(r, 16), parseInt(g, 16), parseInt(b, 16)];
  }

  _padZero(val) {
    if (val.length < 2) {
      val = `0${val}`;
    }
    return val.substr(0, 2);
  }

  _fire(type, detail) {
    const event = new Event(type, {
      bubbles: true,
      cancelable: false,
      composed: true
    });
    event.detail = detail || {};
    this.shadowRoot.dispatchEvent(event);
    return event;
  }
}
customElements.define('circle-sensor-card', CircleSensorCard);
