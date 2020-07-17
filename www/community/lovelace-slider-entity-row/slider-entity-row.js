!function(t){var e={};function s(i){if(e[i])return e[i].exports;var a=e[i]={i:i,l:!1,exports:{}};return t[i].call(a.exports,a,a.exports,s),a.l=!0,a.exports}s.m=t,s.c=e,s.d=function(t,e,i){s.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},s.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.t=function(t,e){if(1&e&&(t=s(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(s.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)s.d(i,a,function(e){return t[e]}.bind(null,a));return i},s.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return s.d(e,"a",e),e},s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},s.p="",s(s.s=1)}([function(t){t.exports=JSON.parse('{"name":"slider-entity-row","private":true,"version":"1.0.0","description":"slider-entity-row =================","scripts":{"build":"webpack","watch":"webpack --watch --mode=development","update-card-tools":"npm uninstall card-tools && npm install thomasloven/lovelace-card-tools"},"repository":{"type":"git","url":"github.com:thomasloven/lovelace-slider-entity-row"},"keywords":[],"author":"Thomas Lovén","license":"MIT","devDependencies":{"webpack":"^4.42.1","webpack-cli":"^3.3.11"},"dependencies":{"card-tools":"github:thomasloven/lovelace-card-tools"}}')},function(t,e,s){"use strict";s.r(e);const i=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),a=i.prototype.html,r=i.prototype.css;class n{constructor(t){this._config=t}set hass(t){this._hass=t,this.stateObj=this._config.entity in t.states?t.states[this._config.entity]:null}get value(){return this._value?Math.round(this._value/this.step)*this.step:0}set value(t){t!==this.value&&(this._value=t)}get string(){return""+this.value}get hidden(){return!1}get hasSlider(){return!0}get hasToggle(){return!0}get isOff(){return 0===this.value}get min(){return void 0!==this._config.min?this._config.min:void 0!==this._min?this._min:0}get max(){return void 0!==this._config.max?this._config.max:void 0!==this._max?this._max:100}get step(){return void 0!==this._config.step?this._config.step:void 0!==this._step?this._step:5}}const u={light:class extends n{get attribute(){return this._config.attribute||"brightness"}get _value(){if(!this.stateObj||"on"!==this.stateObj.state)return 0;switch(this.attribute){case"color_temp":return Math.ceil(this.stateObj.attributes.color_temp);case"white_value":return Math.ceil(this.stateObj.attributes.white_value);case"brightness":return Math.ceil(100*this.stateObj.attributes.brightness/255);case"red":return this.stateObj.attributes.rgb_color?Math.ceil(this.stateObj.attributes.rgb_color[0]):0;case"green":return this.stateObj.attributes.rgb_color?Math.ceil(this.stateObj.attributes.rgb_color[1]):0;case"blue":return this.stateObj.attributes.rgb_color?Math.ceil(this.stateObj.attributes.rgb_color[2]):0;case"hue":return this.stateObj.attributes.hs_color?Math.ceil(this.stateObj.attributes.hs_color[0]):0;case"saturation":return this.stateObj.attributes.hs_color?Math.ceil(this.stateObj.attributes.hs_color[1]):0;case"effect":return this.stateObj.attributes.effect_list?this.stateObj.attributes.effect_list.indexOf(this.stateObj.attributes.effect):0;default:return 0}}get _step(){switch(this.attribute){case"effect":return 1;default:return 5}}get _min(){switch(this.attribute){case"color_temp":return this.stateObj?this.stateObj.attributes.min_mireds:0;default:return 0}}get _max(){switch(this.attribute){case"color_temp":return this.stateObj?this.stateObj.attributes.max_mireds:0;case"red":case"green":case"blue":case"white_value":return 255;case"hue":return 360;case"effect":return this.stateObj&&this.stateObj.attributes.effect_list?this.stateObj.attributes.effect_list.length-1:0;default:return 100}}set _value(t){if(!this.stateObj)return;let e,s=this.attribute,i=!0;switch(s){case"brightness":(t=Math.ceil(t/100*255))||(i=!1);break;case"red":case"green":case"blue":e=this.stateObj.attributes.rgb_color||[0,0,0],"red"===s&&(e[0]=t),"green"===s&&(e[1]=t),"blue"===s&&(e[2]=t),t=e,s="rgb_color";break;case"hue":case"saturation":e=this.stateObj.attributes.hs_color||[0,0],"hue"===s&&(e[0]=t),"saturation"===s&&(e[1]=t),t=e,s="hs_color";break;case"effect":t=this.stateObj.attributes.effect_list[t],s="effect"}i?this._hass.callService("light","turn_on",{entity_id:this.stateObj.entity_id,[s]:t}):this._hass.callService("light","turn_off",{entity_id:this.stateObj.entity_id})}get string(){if(this.stateObj&&"off"===this.stateObj.state)return this._hass.localize("state.default.off");switch(this.attribute){case"color_temp":return""+this.value;case"brightness":case"saturation":return this.value+" %";case"hue":return this.value+" °";case"effect":return this.stateObj?this.stateObj.attributes.effect:"";default:return this.value}}get hasSlider(){if(!this.stateObj)return!1;switch(this.attribute){case"brightness":return"brightness"in this.stateObj.attributes||!!("supported_features"in this.stateObj.attributes&&1&this.stateObj.attributes.supported_features);case"color_temp":return"color_temp"in this.stateObj.attributes||!!("supported_features"in this.stateObj.attributes&&2&this.stateObj.attributes.supported_features);case"white_value":return"white_value"in this.stateObj.attributes||!!("supported_features"in this.stateObj.attributes&&128&this.stateObj.attributes.supported_features);case"red":case"green":case"blue":return"rgb_color"in this.stateObj.attributes||!!("supported_features"in this.stateObj.attributes&&16&this.stateObj.attributes.supported_features);case"hue":case"saturation":return"hs_color"in this.stateObj.attributes||!!("supported_features"in this.stateObj.attributes&&16&this.stateObj.attributes.supported_features);case"effect":return"effect"in this.stateObj.attributes;default:return!1}}},media_player:class extends n{get _value(){return"on"===this.stateObj.is_volume_muted?0:Math.ceil(100*this.stateObj.attributes.volume_level)}set _value(t){t/=100,this._hass.callService("media_player","volume_set",{entity_id:this.stateObj.entity_id,volume_level:t})}get isOff(){return"off"===this.stateObj.state}get string(){return this.stateObj.attributes.is_volume_muted?"-":this.stateObj.attributes.volume_level?this.value+" %":this._hass.localize("state.media_player.off")}get hasToggle(){return!1}},climate:class extends n{get _value(){return this.stateObj.attributes.temperature}set _value(t){this._hass.callService("climate","set_temperature",{entity_id:this.stateObj.entity_id,temperature:t})}get string(){return"off"===this.stateObj.attributes.hvac_mode?this._hass.localize("state.climate.off"):`${this.value} ${this._hass.config.unit_system.temperature}`}get isOff(){return"off"===this.stateObj.attributes.hvac_mode}get _min(){return this.stateObj.attributes.min_temp}get _max(){return this.stateObj.attributes.max_temp}get _step(){return 1}},cover:class extends n{get attribute(){return this._config.attribute||"position"}get _value(){switch(this.attribute){case"position":return"closed"===this.stateObj.state?0:this.stateObj.attributes.current_position;case"tilt":return this.stateObj.attributes.current_tilt_position;default:return 0}}set _value(t){switch(this.attribute){case"position":this._hass.callService("cover","set_cover_position",{entity_id:this.stateObj.entity_id,position:t});break;case"tilt":this._hass.callService("cover","set_cover_tilt_position",{entity_id:this.stateObj.entity_id,tilt_position:t})}}get string(){if(!this.hasSlider)return"";switch(this.attribute){case"position":return"closed"===this.stateObj.state?this._hass.localize("state.cover.closed"):this.value+" %";case"tilt":return this.value}}get hasToggle(){return!1}get hasSlider(){switch(this.attribute){case"position":if("current_position"in this.stateObj.attributes)return!0;if("supported_features"in this.stateObj.attributes&&4&this.stateObj.attributes.supported_features)return!0;case"tilt":if("current_tilt_position"in this.stateObj.attributes)return!0;if("supported_features"in this.stateObj.attributes&&128&this.stateObj.attributes.supported_features)return!0;default:return!1}}get _step(){return 10}},fan:class extends n{get _value(){return"off"!==this.stateObj.state?this.stateObj.attributes.speed_list.indexOf(this.stateObj.attributes.speed):0}set _value(t){t in this.stateObj.attributes.speed_list?this._hass.callService("fan","turn_on",{entity_id:this.stateObj.entity_id,speed:this.stateObj.attributes.speed_list[t]}):this._hass.callService("fan","turn_off",{entity_id:this.stateObj.entity_id})}get string(){return"off"===this.stateObj.state?this._hass.localize("state.default.off"):this.stateObj.attributes.speed}get hasSlider(){return"speed"in this.stateObj.attributes}get _max(){return this.stateObj.attributes.speed_list.length-1}get _step(){return 1}},input_number:class extends n{get _value(){return this.stateObj.state}set _value(t){this._hass.callService("input_number","set_value",{entity_id:this.stateObj.entity_id,value:t})}get string(){return`${parseFloat(this.stateObj.state)} ${this.stateObj.attributes.unit_of_measurement||""}`.trim()}get isOff(){return!1}get hasToggle(){return!1}get hasSlider(){return"slider"===this.stateObj.attributes.mode}get _min(){return this.stateObj.attributes.min}get _max(){return this.stateObj.attributes.max}get _step(){return this.stateObj.attributes.step}},input_select:class extends n{get _value(){return this.stateObj.attributes.options.indexOf(this.stateObj.state)}set _value(t){t in this.stateObj.attributes.options&&this._hass.callService("input_select","select_option",{entity_id:this.stateObj.entity_id,option:this.stateObj.attributes.options[t]})}get string(){return this.stateObj.state}get isOff(){return!1}get hasToggle(){return!1}get hasSlider(){return this.stateObj.attributes.options&&this.stateObj.attributes.options.length>0}get _max(){return this.stateObj.attributes.options.length-1}get _step(){return 1}}};class h extends i{static get properties(){return{hass:{},hide_state:{}}}setConfig(t){if(this._config=t,!t.entity)throw new Error("No entity specified.");const e=t.entity.split(".")[0],s=u[e];if(!s)throw new Error("Unsupported entity type: "+e);this.ctrl=new s(t)}async resized(){await this.updateComplete,this.shadowRoot&&(this.hide_state=this._config.full_row?this.parentElement.clientWidth<=180:this.parentElement.clientWidth<=335)}async firstUpdated(){await this.resized()}render(){const t=this.ctrl;if(t.hass=this.hass,!t.stateObj)return a`
      <hui-warning>
        ${this.hass.localize("ui.panel.lovelace.warning.entity_not_found","entity",this._config.entity)}
      </hui-warning>
      `;const e=this.hass.translationMetadata.translations[this.hass.language||"en"].isRTL?"rtl":"ltr",s=a`
      <ha-slider
        .min=${t.min}
        .max=${t.max}
        .step=${t.step}
        .value=${t.value}
        .dir=${e}
        pin
        @change=${e=>t.value=this.shadowRoot.querySelector("ha-slider").value}
        class=${this._config.full_row?"full":""}
        ignore-bar-touch
      ></ha-slider>
    `,i=a`
      <ha-entity-toggle
        .stateObj=${this.hass.states[this._config.entity]}
        .hass=${this.hass}
        .class="state"
      ></ha-entity-toggle>
    `,r=a`
    <div class="wrapper" @click=${t=>t.stopPropagation()}>
      ${"unavailable"===t.stateObj.state?a`
            <span class="state">
            unavailable
            </span>
        `:a`
            ${this._config.hide_when_off&&t.isOff||!t.hasSlider?"":s}

            ${this._config.toggle?t.hasToggle?i:"":(this._config.hide_state||this.hide_state)&&!1!==this._config.hide_state?"":a`
                    <span class="state">
                      ${t.string}
                    </span>
                  `}
          `}
    </div>
    `;return this._config.full_row?this._config.hide_when_off&&t.isOff?a``:r:a`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
      > ${r} </hui-generic-entity-row>
    `}static get styles(){return r`
      .wrapper {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        flex-grow: 2;
        height: 40px;
      }
      .state {
        min-width: 45px;
        text-align: end;
        margin-left: 5px;
      }
      ha-entity-toggle {
        min-width: auto;
        margin-left: 8px;
      }
      ha-slider {
        width: 100%;
        min-width: 100px;
      }
      ha-slider:not(.full) {
        max-width: 200px;
      }
    `}}if(!customElements.get("slider-entity-row")){customElements.define("slider-entity-row",h);const t=s(0);console.info(`%cSLIDER-ENTITY-ROW ${t.version} IS INSTALLED`,"color: green; font-weight: bold","")}}]);