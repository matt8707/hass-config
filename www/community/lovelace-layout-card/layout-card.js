!function(t){var e={};function n(s){if(e[s])return e[s].exports;var o=e[s]={i:s,l:!1,exports:{}};return t[s].call(o.exports,o,o.exports,n),o.l=!0,o.exports}n.m=t,n.c=e,n.d=function(t,e,s){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:s})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var s=Object.create(null);if(n.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)n.d(s,o,function(e){return t[e]}.bind(null,o));return s},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=0)}([function(t,e,n){"use strict";n.r(e);const s=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),o=s.prototype.html,i=s.prototype.css;const r="custom:";function c(t,e){const n=document.createElement("hui-error-card");return n.setConfig({type:"error",error:t,origConfig:e}),n}function a(t,e){if(!e||"object"!=typeof e||!e.type)return c(`No ${t} type configured`,e);let n=e.type;if(n=n.startsWith(r)?n.substr(r.length):`hui-${n}-${t}`,customElements.get(n))return function(t,e){const n=document.createElement(t);try{n.setConfig(e)}catch(t){return c(t,e)}return n}(n,e);const s=c(`Custom element doesn't exist: ${n}.`,e);s.style.display="None";const o=setTimeout(()=>{s.style.display=""},2e3);return customElements.whenDefined(n).then(()=>{clearTimeout(o),function(t,e,n=null){if((t=new Event(t,{bubbles:!0,cancelable:!1,composed:!0})).detail=e||{},n)n.dispatchEvent(t);else{var s=document.querySelector("home-assistant");(s=(s=(s=(s=(s=(s=(s=(s=(s=(s=(s=s&&s.shadowRoot)&&s.querySelector("home-assistant-main"))&&s.shadowRoot)&&s.querySelector("app-drawer-layout partial-panel-resolver"))&&s.shadowRoot||s)&&s.querySelector("ha-panel-lovelace"))&&s.shadowRoot)&&s.querySelector("hui-root"))&&s.shadowRoot)&&s.querySelector("ha-app-layout #view"))&&s.firstElementChild)&&s.dispatchEvent(t)}}("ll-rebuild",{},s)}),s}function l(){return document.querySelector("home-assistant").hass}const u=2;class d extends s{static get version(){return u}static get properties(){return{noHass:{type:Boolean}}}setConfig(t){var e;this._config=t,this.el?this.el.setConfig(t):(this.el=this.create(t),this._hass&&(this.el.hass=this._hass),this.noHass&&(e=this,document.querySelector("home-assistant").provideHass(e)))}set config(t){this.setConfig(t)}set hass(t){this._hass=t,this.el&&(this.el.hass=t)}createRenderRoot(){return this}render(){return o`${this.el}`}}const h=function(t,e){const n=Object.getOwnPropertyDescriptors(e.prototype);for(const[e,s]of Object.entries(n))"constructor"!==e&&Object.defineProperty(t.prototype,e,s);const s=Object.getOwnPropertyDescriptors(e);for(const[e,n]of Object.entries(s))"prototype"!==e&&Object.defineProperty(t,e,n);const o=Object.getPrototypeOf(e),i=Object.getOwnPropertyDescriptors(o.prototype);for(const[e,n]of Object.entries(i))"constructor"!==e&&Object.defineProperty(Object.getPrototypeOf(t).prototype,e,n);const r=Object.getOwnPropertyDescriptors(o);for(const[e,n]of Object.entries(r))"prototype"!==e&&Object.defineProperty(Object.getPrototypeOf(t),e,n)},m=customElements.get("card-maker");if(!m||!m.version||m.version<u){class t extends d{create(t){return function(t){return a("card",t)}(t)}getCardSize(){return this.firstElementChild&&this.firstElementChild.getCardSize?this.firstElementChild.getCardSize():1}}m?h(m,t):customElements.define("card-maker",t)}const f=customElements.get("element-maker");if(!f||!f.version||f.version<u){class t extends d{create(t){return function(t){return a("element",t)}(t)}}f?h(f,t):customElements.define("element-maker",t)}const p=customElements.get("entity-row-maker");if(!p||!p.version||p.version<u){class t extends d{create(t){return function(t){const e=new Set(["call-service","divider","section","weblink"]);if(!t)return c("Invalid configuration given.",t);if("string"==typeof t&&(t={entity:t}),"object"!=typeof t||!t.entity&&!t.type)return c("Invalid configuration given.",t);const n=t.type||"default";if(e.has(n)||n.startsWith(r))return a("row",t);const s=t.entity.split(".",1)[0];return Object.assign(t,{type:{alert:"toggle",automation:"toggle",climate:"climate",cover:"cover",fan:"toggle",group:"group",input_boolean:"toggle",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",remote:"toggle",scene:"scene",script:"script",sensor:"sensor",timer:"timer",switch:"toggle",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime"}[s]||"text"}),a("entity-row",t)}(t)}}p?h(p,t):customElements.define("entity-row-maker",t)}function g(t,e,n){t.forEach(t=>{if(!t)return;const s=e[function(){let t=0;for(let s=0;s<e.length;s++){if(e[s].length<n.min_height)return s;e[s].length<e[t].length&&(t=s)}return t}()];s.appendChild(t),s.length+=t.getCardSize?t.getCardSize():1})}customElements.define("layout-card",class extends s{static get properties(){return{hass:{},_config:{}}}async setConfig(t){this._config={min_height:5,column_width:300,max_width:t.column_width||"500px",min_columns:t.column_num||1,max_columns:100,...t},this.cards=[],this.columns=[]}async firstUpdated(){window.addEventListener("resize",()=>this.place_cards()),window.addEventListener("hass-open-menu",()=>setTimeout(()=>this.place_cards(),100)),window.addEventListener("hass-close-menu",()=>setTimeout(()=>this.place_cards(),100)),window.addEventListener("location-changed",()=>{""===location.hash&&setTimeout(()=>this.place_cards(),100)})}async updated(t){!this.cards.length&&(this._config.entities&&this._config.entities.length||this._config.cards&&this._config.cards.length)&&(this.cards=await this.build_cards(),this.place_cards()),t.has("hass")&&this.hass&&this.cards&&this.cards.forEach(t=>{t&&(t.hass=this.hass)})}async build_card(t){if("break"===t)return null;const e=document.createElement("card-maker");return e.config={...t,...this._config.card_options},e.hass=l(),this.shadowRoot.querySelector("#staging").appendChild(e),new Promise((t,n)=>e.updateComplete.then(()=>t(e)))}async build_cards(){const t=this.shadowRoot.querySelector("#staging");for(;t.lastChild;)t.removeChild(t.lastChild);return Promise.all((this._config.entities||this._config.cards).map(t=>this.build_card(t)))}place_cards(){const t=this.shadowRoot.querySelector("#columns").clientWidth;this.columns=function(t,e,n){const s=t=>"string"==typeof t&&t.endsWith("%")?Math.floor(e*parseInt(t)/100):parseInt(t);let o=0;if("object"==typeof n.column_width){let t=e;for(;t>0;){let e=n.column_width[o];void 0===e&&(e=n.column_width.slice(-1)[0]),t-=s(e),o+=1}o=Math.max(o-1,1)}else o=Math.floor(e/s(n.column_width));o=Math.max(o,n.min_columns),o=Math.min(o,n.max_columns);let i=[];for(let t=0;t<o;t++){const t=document.createElement("div");t.classList.add("column"),t.length=0,i.push(t)}switch(n.layout){case"horizontal":!function(t,e,n){let s=0;t.forEach(t=>{if(s+=1,!t)return;const n=e[(s-1)%e.length];n.appendChild(t),n.length+=t.getCardSize?t.getCardSize():1})}(t,i);break;case"vertical":!function(t,e,n){let s=0;t.forEach(t=>{if(!t)return void(s+=1);const n=e[s%e.length];n.appendChild(t),n.length+=t.getCardSize?t.getCardSize():1})}(t,i);break;case"auto":default:g(t,i,n)}return i=i.filter(t=>t.childElementCount>0)}(this.cards,t,this._config),this._config.rtl&&this.columns.reverse(),this.format_columns(),this.requestUpdate()}format_columns(){const t=(t,e,n,s="px")=>{if(void 0===this._config[e])return"";let o=`${t}: `;const i=this._config[e];return"object"==typeof i?i.length>n?o+=`${i[n]}`:o+=`${i.slice(-1)}`:o+=`${i}`,o.endsWith("px")||o.endsWith("%")||(o+=s),o+";"};for(const[e,n]of this.columns.entries()){const s=[t("max-width","max_width",e),t("min-width","min_width",e),t("width","column_width",e),t("flex-grow","flex_grow",e,"")];n.style.cssText="".concat(...s)}}getCardSize(){if(this.columns)return Math.max.apply(Math,this.columns.map(t=>t.length))}_isPanel(){if(this.isPanel)return!0;let t=this.parentElement,e=10;for(;e--;){if("hui-panel-view"===t.localName)return!0;if("div"===t.localName)return!1;t=t.parentElement}return!1}render(){return o`
      <div id="columns"
      class="
      ${this._isPanel()?"panel":" "}
      "
      style="
      ${this._config.justify_content?`justify-content: ${this._config.justify_content};`:""}
      ">
        ${this.columns.map(t=>o`
          ${t}
        `)}
      </div>
      <div id="staging"></div>
    `}static get styles(){return i`
      :host {
        padding: 0 4px;
        display: block;
        margin-bottom: 0!important;
      }

      #columns {
        display: flex;
        flex-direction: row;
        justify-content: center;
        margin-top: -8px;
      }
      #columns.panel {
        margin-top: 0;
      }

      .column {
        flex-basis: 0;
        flex-grow: 1;
        overflow-x: hidden;
      }

      card-maker>* {
        display: block;
        margin: 4px 4px 8px;
      }
      card-maker:first-child>* {
        margin-top: 8px;
      }
      card-maker:last-child>* {
        margin-bottom: 4px;
      }

      #staging {
        visibility: hidden;
        height: 0;
      }
    `}get _cardModder(){return{target:this}}})}]);