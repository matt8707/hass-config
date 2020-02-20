!function(t){var e={};function n(i){if(e[i])return e[i].exports;var s=e[i]={i:i,l:!1,exports:{}};return t[i].call(s.exports,s,s.exports,n),s.l=!0,s.exports}n.m=t,n.c=e,n.d=function(t,e,i){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(n.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var s in t)n.d(i,s,function(e){return t[e]}.bind(null,s));return i},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="",n(n.s=0)}([function(t,e,n){"use strict";n.r(e);const i=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),s=i.prototype.html,o=i.prototype.css;function r(){return document.querySelector("hc-main")?document.querySelector("hc-main").hass:document.querySelector("home-assistant")?document.querySelector("home-assistant").hass:void 0}function c(t,e,n=null){if((t=new Event(t,{bubbles:!0,cancelable:!1,composed:!0})).detail=e||{},n)n.dispatchEvent(t);else{var i=function(){var t=document.querySelector("hc-main");return t=t?(t=(t=(t=t&&t.shadowRoot)&&t.querySelector("hc-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-view"):(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=document.querySelector("home-assistant"))&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root"))&&t.shadowRoot)&&t.querySelector("ha-app-layout #view"))&&t.firstElementChild}();i&&i.dispatchEvent(t)}}function a(t,e){const n=document.createElement("hui-error-card");return n.setConfig({type:"error",error:t,origConfig:e}),n}function l(t,e){if(!e||"object"!=typeof e||!e.type)return a(`No ${t} type configured`,e);let n=e.type;if(n=n.startsWith("custom:")?n.substr("custom:".length):`hui-${n}-${t}`,customElements.get(n))return function(t,e){const n=document.createElement(t);try{n.setConfig(e)}catch(t){return a(t,e)}return n}(n,e);const i=a(`Custom element doesn't exist: ${n}.`,e);i.style.display="None";const s=setTimeout(()=>{i.style.display=""},2e3);return customElements.whenDefined(n).then(()=>{clearTimeout(s),c("ll-rebuild",{},i)}),i}function u(t){return l("card",t)}class d extends i{static get version(){return 2}static get properties(){return{noHass:{type:Boolean}}}setConfig(t){var e;this._config=t,this.el?this.el.setConfig(t):(this.el=this.create(t),this._hass&&(this.el.hass=this._hass),this.noHass&&(e=this,document.querySelector("hc-main")?document.querySelector("hc-main").provideHass(e):document.querySelector("home-assistant")&&document.querySelector("home-assistant").provideHass(e)))}set config(t){this.setConfig(t)}set hass(t){this._hass=t,this.el&&(this.el.hass=t)}createRenderRoot(){return this}render(){return s`${this.el}`}}const h=function(t,e){const n=Object.getOwnPropertyDescriptors(e.prototype);for(const[e,i]of Object.entries(n))"constructor"!==e&&Object.defineProperty(t.prototype,e,i);const i=Object.getOwnPropertyDescriptors(e);for(const[e,n]of Object.entries(i))"prototype"!==e&&Object.defineProperty(t,e,n);const s=Object.getPrototypeOf(e),o=Object.getOwnPropertyDescriptors(s.prototype);for(const[e,n]of Object.entries(o))"constructor"!==e&&Object.defineProperty(Object.getPrototypeOf(t).prototype,e,n);const r=Object.getOwnPropertyDescriptors(s);for(const[e,n]of Object.entries(r))"prototype"!==e&&Object.defineProperty(Object.getPrototypeOf(t),e,n)},m=customElements.get("card-maker");if(!m||!m.version||m.version<2){class t extends d{create(t){return u(t)}getCardSize(){return this.firstElementChild&&this.firstElementChild.getCardSize?this.firstElementChild.getCardSize():1}}m?h(m,t):customElements.define("card-maker",t)}const f=customElements.get("element-maker");if(!f||!f.version||f.version<2){class t extends d{create(t){return function(t){return l("element",t)}(t)}}f?h(f,t):customElements.define("element-maker",t)}const p=customElements.get("entity-row-maker");if(!p||!p.version||p.version<2){class t extends d{create(t){return function(t){const e=new Set(["call-service","divider","section","weblink"]);if(!t)return a("Invalid configuration given.",t);if("string"==typeof t&&(t={entity:t}),"object"!=typeof t||!t.entity&&!t.type)return a("Invalid configuration given.",t);const n=t.type||"default";if(e.has(n)||n.startsWith("custom:"))return l("row",t);const i=t.entity.split(".",1)[0];return Object.assign(t,{type:{alert:"toggle",automation:"toggle",climate:"climate",cover:"cover",fan:"toggle",group:"group",input_boolean:"toggle",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",remote:"toggle",scene:"scene",script:"script",sensor:"sensor",timer:"timer",switch:"toggle",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime"}[i]||"text"}),l("entity-row",t)}(t)}}p?h(p,t):customElements.define("entity-row-maker",t)}function g(t,e,n){t.forEach(t=>{if(!t)return;const i=e[function(){let t=0;for(let i=0;i<e.length;i++){if(e[i].length<n.min_height)return i;e[i].length<e[t].length&&(t=i)}return t}()];i.appendChild(t),i.length+=t.getCardSize?t.getCardSize():1})}customElements.get("layout-card")||customElements.define("layout-card",class extends i{static get properties(){return{hass:{},_config:{}}}async setConfig(t){this._config={min_height:5,column_width:300,max_width:t.column_width||"500px",min_columns:t.column_num||1,max_columns:100,...t},this.cards=[],this.columns=[]}connectedCallback(){super.connectedCallback(),this.place_cards(this.clientWidth)}async firstUpdated(){window.addEventListener("resize",()=>this.place_cards()),window.addEventListener("hass-open-menu",()=>setTimeout(()=>this.place_cards(),100)),window.addEventListener("hass-close-menu",()=>setTimeout(()=>this.place_cards(),100)),window.addEventListener("location-changed",()=>{""===location.hash&&setTimeout(()=>this.place_cards(),100)})}async updated(t){if(!this.cards.length&&(this._config.entities&&this._config.entities.length||this._config.cards&&this._config.cards.length)){const t=this.clientWidth;this.cards=await this.build_cards(),this.place_cards(t)}t.has("hass")&&this.hass&&this.cards&&this.cards.forEach(t=>{t&&(t.hass=this.hass)})}async build_card(t){if("break"===t)return null;const e={...t,...this._config.card_options},n=u(e);return n.hass=r(),n.style.gridColumn=e.gridcol,n.style.gridRow=e.gridrow,this.shadowRoot.querySelector("#staging").appendChild(n),new Promise((t,e)=>n.updateComplete?n.updateComplete.then(()=>t(n)):t(n))}async build_cards(){const t=this.shadowRoot.querySelector("#staging");for(;t.lastChild;)t.removeChild(t.lastChild);return Promise.all((this._config.entities||this._config.cards).map(t=>this.build_card(t)))}place_cards(t){"grid"!==this._config.layout&&(void 0!==t&&(this.lastWidth=t),this.lastWidth=this.clientWidth||this.lastWidth,t=this.lastWidth,this.columns=function(t,e,n){const i=t=>"string"==typeof t&&t.endsWith("%")?Math.floor(e*parseInt(t)/100):parseInt(t);let s=0;if("object"==typeof n.column_width){let t=e;for(;t>0;){let e=n.column_width[s];void 0===e&&(e=n.column_width.slice(-1)[0]),t-=i(e),s+=1}s=Math.max(s-1,1)}else s=Math.floor(e/i(n.column_width));s=Math.max(s,n.min_columns),s=Math.min(s,n.max_columns),s=Math.max(s,1);let o=[];for(let t=0;t<s;t++){const t=document.createElement("div");t.classList.add("column"),t.classList.add("cards"),t.length=0,o.push(t)}switch(n.layout){case"horizontal":!function(t,e,n){let i=0;t.forEach(t=>{if(i+=1,!t)return;const n=e[(i-1)%e.length];n.appendChild(t),n.length+=t.getCardSize?t.getCardSize():1})}(t,o);break;case"vertical":!function(t,e,n){let i=0;t.forEach(t=>{if(!t)return void(i+=1);const n=e[i%e.length];n.appendChild(t),n.length+=t.getCardSize?t.getCardSize():1})}(t,o);break;case"auto":default:g(t,o,n)}return o=o.filter(t=>t.childElementCount>0),o}(this.cards,t||1,this._config),this._config.rtl&&this.columns.reverse(),this.format_columns(),this.requestUpdate())}format_columns(){const t=(t,e,n,i="px")=>{if(void 0===this._config[e])return"";let s=`${t}: `;const o=this._config[e];return"object"==typeof o?o.length>n?s+=`${o[n]}`:s+=`${o.slice(-1)}`:s+=`${o}`,s.endsWith("px")||s.endsWith("%")||(s+=i),s+";"};for(const[e,n]of this.columns.entries()){const i=[t("max-width","max_width",e),t("min-width","min_width",e),t("width","column_width",e),t("flex-grow","flex_grow",e,"")];n.style.cssText="".concat(...i)}}getCardSize(){if(this.columns)return Math.max.apply(Math,this.columns.map(t=>t.length))}_isPanel(){if(this.isPanel)return!0;let t=this.parentElement,e=10;for(;e--&&t;){if("hui-panel-view"===t.localName)return!0;if("div"===t.localName)return!1;t=t.parentElement}return!1}render(){return"grid"===this._config.layout?s`
        <div id="staging" class="grid cards"
        style="
        display: grid;
        grid-template-rows: ${this._config.gridrows};
        grid-template-columns: ${this._config.gridcols};
        "></div>
      `:s`
      <div id="columns"
      class="
      ${this._isPanel()?"panel":" "}
      "
      style="
      ${this._config.justify_content?`justify-content: ${this._config.justify_content};`:""}
      ">
        ${this.columns.map(t=>s`
          ${t}
        `)}
      </div>
      <div id="staging"></div>
    `}static get styles(){return o`
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


      .cards>* {
        display: block;
        margin: 4px 4px 8px;
      }
      .cards>*:first-child {
        margin-top: 8px;
      }
      .cards>*:last-child {
        margin-bottom: 4px;
      }

      #staging:not(.grid) {
        visibility: hidden;
        height: 0;
      }
    `}get _cardModder(){return{target:this}}})}]);