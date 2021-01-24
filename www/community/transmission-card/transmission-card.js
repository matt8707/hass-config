const LitElement = Object.getPrototypeOf(
  customElements.get("ha-panel-lovelace")
);
const html = LitElement.prototype.html;
const css = LitElement.prototype.css;

function hasConfigOrEntityChanged(element, changedProps) {
  if (changedProps.has("config")) {
    return true;
  }

  const oldHass = changedProps.get("hass");
  if (oldHass) {
    return (
      oldHass.states[element.config.entity] !==
        element.hass.states[element.config.entity]
    );
  }

  return true;
}

class TransmissionCard extends LitElement {

  static get properties() {
    return {
      config: {},
      hass: {},
      selectedType: undefined
    };
  }

  _getTorrents(hass, type, sensor_name) {
    var res = [];
    if (typeof hass.states[`sensor.${sensor_name}_${type}_torrents`] != "undefined") {
      const data1 = hass.states[`sensor.${sensor_name}_${type}_torrents`].attributes['torrent_info'];
      Object.keys(data1 || {}).forEach(function (key) {
        res.push({
          name: key,
          id: data1[key].id,
          percent: parseInt(data1[key].percent_done, 10),
          state: data1[key].status,
          added_date: data1[key].added_date,
          eta: data1[key].eta,
        });
      });
    }
    return res;
  }

  _getGAttributes(hass) {
    let sensor_name = this.config.sensor_name;
    if (typeof hass.states[`sensor.${sensor_name}_down_speed`] != "undefined") {
      return {
        down_speed: hass.states[`sensor.${sensor_name}_down_speed`].state,
        down_unit: hass.states[`sensor.${sensor_name}_down_speed`].attributes['unit_of_measurement'],
        up_speed: hass.states[`sensor.${sensor_name}_up_speed`].state,
        up_unit: hass.states[`sensor.${sensor_name}_up_speed`].attributes['unit_of_measurement'],
        status: hass.states[`sensor.${sensor_name}_status`].state
      }
    }
    return {
      down_speed: undefined,
      up_speed: undefined,
      down_unit: "MB/s",
      up_unit: "MB/s",
      status: "no sensor"
    };
  }

  _toggleTurtle() {
    this.hass.callService('switch', 'toggle', { entity_id: `switch.${this.config.sensor_name}_turtle_mode` });
  }

  _toggleType() {
    const torrent_types = ['total','active','completed','paused','started']

    const currentIndex = torrent_types.indexOf(this.selectedType);
    const nextIndex = (currentIndex + 1) % torrent_types.length;
    this.selectedType = torrent_types[nextIndex];
  }

  _startStop() {
    this.hass.callService('switch', 'toggle', { entity_id: `switch.${this.config.sensor_name}_switch` });
  }

  setConfig(config) {
    if (config.display_mode &&
      !['compact', 'full'].includes(config.display_mode)) {
        throw new Error('display_mode accepts only "compact" and "full" as value');
      }

    const defaultConfig = {
      'no_torrent_label': 'No torrents',
      'hide_turtle': false,
      'hide_startstop': false,
      'hide_type': false,
      'default_type': 'total',
      'display_mode': 'compact',
      'sensor_name': 'transmission',
    }

    this.config = {
      ...defaultConfig,
      ...config
    };

    this.selectedType = this.config.default_type;
  }

  render() {
    if (!this.config || !this.hass) {
      return html``;
    }

    const torrents = this._getTorrents(this.hass, this.selectedType, this.config.sensor_name);
    return html`
      <ha-card header="Transmission">
        <div>
          <div id="title">
              ${this.renderTitle()}
          </div>
          <div id="attributes">
          ${torrents.length > 0
            ? this.config.display_mode === 'compact'
              ? html`${torrents.map(torrent => this.renderTorrent(torrent))}`
              : html`
                <div class="torrents">
                  ${torrents.map(torrent => this.renderTorrentFull(torrent))}
                </div>`
            : html`<div class="no-torrent">${this.config.no_torrent_label}</div>`
          }
          </div>
        </div>
      </ha-card>
    `;
  }

  renderTitle() {
    const gattributes = this._getGAttributes(this.hass);
    return html
    `
      <div id="title1">
        <div class="status titleitem c-${gattributes.status.replace('/','')}"><p class="txtitem">${gattributes.status}</p></div>
        <div class="titleitem"><ha-icon icon="mdi:download" class="down down-color"></div>
        <div class="titleitem"><p class="txtitem">${gattributes.down_speed} ${gattributes.down_unit}</p></div>
        <div class="titleitem"><ha-icon icon="mdi:upload" class="up up-color"></div>
        <div class="titleitem"><p class="txtitem">${gattributes.up_speed} ${gattributes.up_unit}</p></div>
        ${this.renderTurtleButton()}
        ${this.renderStartStopButton()}
        ${this.renderSwitchTypeButton()}
      </div>
    `;
  }

  renderTorrent(torrent) {
    return html
    `
      <div class="progressbar">
          <div class="${torrent.state} progressin" style="width:${torrent.percent}%">
          </div>
          <div class="name">${torrent.name}</div>
        <div class="percent">${torrent.percent}%</div>
      </div>
    `;
  }

  renderTorrentFull(torrent) {
    return html`
    <div class="torrent">
      <div class="torrent_name">${torrent.name}</div>
      <div class="torrent_state">${torrent.state}</div>
      <div class="progressbar">
        <div class="${torrent.state} progressin" style="width:${torrent.percent}%">
        </div>
      </div>
      <div class="torrent_details">${torrent.percent} %</div>
    </div>
    `
  }

  renderTurtleButton() {
    if (this.config.hide_turtle) {
      return html``;
    }

    if (typeof this.hass.states[`switch.${this.config.sensor_name}_turtle_mode`] == "undefined") {
      return html``;
    }

    const state = this.hass.states[`switch.${this.config.sensor_name}_turtle_mode`].state;
    return html`
      <div class="titleitem">
        <ha-icon-button
          class="turtle_${state}"
          icon="mdi:turtle"
          @click="${this._toggleTurtle}"
          title="turtle mode"
          id="turtle">
        </ha-icon-button>
      </div>
    `;
  }

  renderStartStopButton() {
    if (this.config.hide_startstop) {
      return html``;
    }

    if (typeof this.hass.states[`switch.${this.config.sensor_name}_switch`] == "undefined") {
      return html``;
    }

    const state = this.hass.states[`switch.${this.config.sensor_name}_switch`].state;
    return html`
      <div class="titleitem">
        <ha-icon-button
          class="start_${state}"
          icon="${state === 'on' ? 'mdi:stop' : 'mdi:play'}"
          @click="${this._startStop}"
          title="start/stop all"
          id="start">
        </ha-icon-button>
      </div>
    `;
  }

  renderSwitchTypeButton() {
    if (this.config.hide_type) {
      return html``;
    }

    return html`
      <div>
        <p
          id="ttype"
          @click="${this._toggleType}">
          ${this.selectedType}
        </p>
      </div>
    `;
  }

  getCardSize() {
    return 1;
  }

  static get styles() {
    return css`
    #attributes {
      margin-top: 0.4em;
      padding-bottom: 0.8em;
    }
    .progressbar {
      border-radius: 0.4em;
      margin-bottom: 0.6em;
      height: 1.4em;
      display: flex;
      background-color: #f1f1f1;
      z-index: 0;
      position: relative;
      margin-left: 1.4em;
      margin-right: 1.4em;
    }
    .progressin {
      border-radius: 0.4em;
      height: 100%;
      z-index: 1;
      position: absolute;
    }
    .name {
      margin-left: 0.7em;
      width: calc(100% - 60px);
      overflow: hidden;
      z-index: 2;
      color: var(--text-light-primary-color, var(--primary-text-color));
      line-height: 1.4em;
    }
    .percent {
      vertical-align: middle;
      z-index: 2;
      margin-left: 1.7em;
      margin-right: 0.7em;
      color: var(--text-light-primary-color, var(--primary-text-color));
      line-height: 1.4em;
    }
    .downloading {
      background-color: var(--paper-item-icon-active-color);
    }
    .c-Downloading, .c-UpDown {
      color: var(--paper-item-icon-active-color);
    }
    .seeding {
      background-color: var(--light-primary-color);
    }
    .c-seeding {
      color: var(--light-primary-color);
    }
    .stopped {
      background-color: var(--label-badge-grey);
    }
    .c-idle {
      color: var(--label-badge-grey);
    }
    .up, .down {
      display: inline-block;
      padding-top: 12px;
    }
    .up-color {
      width: 2em;
      color: var(--light-primary-color);
    }
    .down-color {
      width: 2em;
      color: var(--paper-item-icon-active-color);
      margin-left: 1em;
    }

    #title {
      position: relative;
      display: inline;
      width: 100%;
    }
    #title1 {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      width: 100%;
    }
    .titleitem {
      width: auto;
      margin-left: 0.7em;
    }

    .status {
      font-size: 1em;
    }
    .turtle_off {
      color: var(--light-primary-color);
    }
    .turtle_on {
      color: var(--paper-item-icon-active-color);
    }
    .start_on {
      color: var(--light-primary-color);
    }
    .start_off {
      color: var(--primary-color);
    }
    .no-torrent {
      margin-left: 1.4em;
    }
    #ttype {
      background-color: var(--light-primary-color);
      color: var(--text-light-primary-color, var(--primary-text-color));
      border-radius: 0.4em;
      margin-bottom: 0.7em;
      margin-left: 0.7em;
      height: 1.5em;
      line-height: 1.5em;
      display: flex;
      padding-left: 1.3em;
      padding-right: 1em;
      width: auto;
    }
    .torrents {
      margin-left: 1.4em;
      margin-right: 1.4em;
    }
    .torrent:not(:last-child) {
      border-bottom: 1px solid var(--divider-color);
    }
    .torrents .progressbar {
      margin: 0 0 0 0;
      height: 4px;
    }
    .torrent_name {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .torrent_state {
      font-size: 0.7em;
      text-transform: capitalize;
    }
    .torrent_details {
      font-size: 0.7em;
    }
    `;
  }
}

customElements.define('transmission-card', TransmissionCard);

// Puts card into the UI card picker dialog
(window).customCards = (window).customCards || [];
(window).customCards.push({
  type: 'transmission-card',
  name: 'Transmission Card',
  preview: true,
  description: 'This Lovelace custom card displays torrents information provided by the Transmission Integration.',
});
