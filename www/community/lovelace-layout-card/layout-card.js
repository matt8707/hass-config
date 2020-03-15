!function(t){var e={};function i(n){if(e[n])return e[n].exports;var r=e[n]={i:n,l:!1,exports:{}};return t[n].call(r.exports,r,r.exports,i),r.l=!0,r.exports}i.m=t,i.c=e,i.d=function(t,e,n){i.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},i.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.t=function(t,e){if(1&e&&(t=i(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(i.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var r in t)i.d(n,r,function(e){return t[e]}.bind(null,r));return n},i.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return i.d(e,"a",e),e},i.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},i.p="",i(i.s=5)}([function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});e.ContentRect=function(t){if("getBBox"in t){var e=t.getBBox();return Object.freeze({height:e.height,left:0,top:0,width:e.width})}var i=window.getComputedStyle(t);return Object.freeze({height:parseFloat(i.height||"0"),left:parseFloat(i.paddingLeft||"0"),top:parseFloat(i.paddingTop||"0"),width:parseFloat(i.width||"0")})}},function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=i(2),r=i(3),o=[],s=function(){function t(t){this.$$observationTargets=[],this.$$activeTargets=[],this.$$skippedTargets=[];var e=function(t){if(void 0===t)return"Failed to construct 'ResizeObserver': 1 argument required, but only 0 present.";if("function"!=typeof t)return"Failed to construct 'ResizeObserver': The callback provided as parameter 1 is not a function."}(t);if(e)throw TypeError(e);this.$$callback=t,o.push(this)}return t.prototype.observe=function(t){var e=a("observe",t);if(e)throw TypeError(e);c(this.$$observationTargets,t)>0||(this.$$observationTargets.push(new n.ResizeObservation(t)),p())},t.prototype.unobserve=function(t){var e=a("unobserve",t);if(e)throw TypeError(e);var i=c(this.$$observationTargets,t);i<0||(this.$$observationTargets.splice(i,1),m())},t.prototype.disconnect=function(){this.$$observationTargets=[],this.$$activeTargets=[]},t}();function a(t,e){return void 0===e?"Failed to execute '"+t+"' on 'ResizeObserver': 1 argument required, but only 0 present.":e instanceof window.Element?void 0:"Failed to execute '"+t+"' on 'ResizeObserver': parameter 1 is not of type 'Element'."}function c(t,e){for(var i=0;i<t.length;i+=1)if(t[i].target===e)return i;return-1}e.ResizeObserver=s;var l,d=function(t){o.forEach((function(e){e.$$activeTargets=[],e.$$skippedTargets=[],e.$$observationTargets.forEach((function(i){i.isActive()&&(h(i.target)>t?e.$$activeTargets.push(i):e.$$skippedTargets.push(i))}))}))},u=function(){var t=1/0;return o.forEach((function(e){if(e.$$activeTargets.length){var i=[];e.$$activeTargets.forEach((function(e){var n=new r.ResizeObserverEntry(e.target);i.push(n),e.$$broadcastWidth=n.contentRect.width,e.$$broadcastHeight=n.contentRect.height;var o=h(e.target);o<t&&(t=o)})),e.$$callback(i,e),e.$$activeTargets=[]}})),t},h=function(t){for(var e=0;t.parentNode;)t=t.parentNode,e+=1;return e},f=function(){var t,e=0;for(d(e);o.some((function(t){return!!t.$$activeTargets.length}));)e=u(),d(e);o.some((function(t){return!!t.$$skippedTargets.length}))&&(t=new window.ErrorEvent("ResizeLoopError",{message:"ResizeObserver loop completed with undelivered notifications."}),window.dispatchEvent(t))},p=function(){l||g()},g=function(){l=window.requestAnimationFrame((function(){f(),g()}))},m=function(){l&&!o.some((function(t){return!!t.$$observationTargets.length}))&&(window.cancelAnimationFrame(l),l=void 0)};e.install=function(){return window.ResizeObserver=s}},function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=i(0),r=function(){function t(t){this.target=t,this.$$broadcastWidth=this.$$broadcastHeight=0}return Object.defineProperty(t.prototype,"broadcastWidth",{get:function(){return this.$$broadcastWidth},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"broadcastHeight",{get:function(){return this.$$broadcastHeight},enumerable:!0,configurable:!0}),t.prototype.isActive=function(){var t=n.ContentRect(this.target);return!!t&&(t.width!==this.broadcastWidth||t.height!==this.broadcastHeight)},t}();e.ResizeObservation=r},function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=i(0),r=function(t){this.target=t,this.contentRect=n.ContentRect(t)};e.ResizeObserverEntry=r},function(t){t.exports=JSON.parse('{"name":"layout-card","version":"1.2.1","description":"","private":true,"scripts":{"build":"webpack","watch":"webpack --watch --mode=development","update-card-tools":"npm uninstall card-tools && npm install thomasloven/lovelace-card-tools"},"author":"Thomas Lovén","license":"MIT","devDependencies":{"webpack":"^4.41.5","webpack-cli":"^3.3.10"},"dependencies":{"card-tools":"github:thomasloven/lovelace-card-tools","resize-observer":"^1.0.0"}}')},function(t,e,i){"use strict";i.r(e);const n=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),r=n.prototype.html,o=n.prototype.css;function s(){return document.querySelector("hc-main")?document.querySelector("hc-main").hass:document.querySelector("home-assistant")?document.querySelector("home-assistant").hass:void 0}function a(t,e,i=null){if((t=new Event(t,{bubbles:!0,cancelable:!1,composed:!0})).detail=e||{},i)i.dispatchEvent(t);else{var n=function(){var t=document.querySelector("hc-main");return t=t?(t=(t=(t=t&&t.shadowRoot)&&t.querySelector("hc-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-view"):(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=document.querySelector("home-assistant"))&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root"))&&t.shadowRoot)&&t.querySelector("ha-app-layout #view"))&&t.firstElementChild}();n&&n.dispatchEvent(t)}}let c=window.cardHelpers;const l=new Promise(async(t,e)=>{c&&t(),window.loadCardHelpers&&(c=await window.loadCardHelpers(),window.cardHelpers=c,t())});function d(t,e){const i=document.createElement("hui-error-card");return i.setConfig({type:"error",error:t,origConfig:e}),i}function u(t,e){if(!e||"object"!=typeof e||!e.type)return d(`No ${t} type configured`,e);let i=e.type;if(i=i.startsWith("custom:")?i.substr("custom:".length):`hui-${i}-${t}`,customElements.get(i))return function(t,e){let i=document.createElement(t);try{i.setConfig(JSON.parse(JSON.stringify(e)))}catch(t){i=d(t,e)}return l.then(()=>{a("ll-rebuild",{},i)}),i}(i,e);const n=d(`Custom element doesn't exist: ${i}.`,e);n.style.display="None";const r=setTimeout(()=>{n.style.display=""},2e3);return customElements.whenDefined(i).then(()=>{clearTimeout(r),a("ll-rebuild",{},n)}),n}function h(t,e,i){t.forEach(t=>{if(!t)return;const n=e[function(){let t=0;for(let n=0;n<e.length;n++){if(e[n].length<i.min_height)return n;e[n].length<e[t].length&&(t=n)}return t}()];n.appendChild(t),n.length+=t.getCardSize?t.getCardSize():1})}var f=i(1);class p extends n{static get properties(){return{hass:{},_config:{}}}async setConfig(t){this._config={min_height:5,column_width:300,max_width:t.column_width||"500px",min_columns:t.column_num||1,max_columns:100,...t},this.cards=[],this.columns=[],this._layoutWidth=0}connectedCallback(){super.connectedCallback();let t=this.parentElement,e=10;for(;e--&&t&&("HUI-PANEL-VIEW"===t.tagName&&this.classList.add("panel"),"DIV"!==t.tagName););}async firstUpdated(){window.addEventListener("location-changed",()=>{""===location.hash&&setTimeout(()=>this.updateSize(),100)}),this.resizer||(this.resizer=new f.ResizeObserver(()=>this.updateSize()),this.resizer.observe(this)),this.updateSize()}updateSize(){const t=this.getBoundingClientRect().width;t&&t!==this._layoutWidth&&(this._layoutWidth=t,this.resizer.disconnect(),this.place_cards(),this.requestUpdate().then(()=>this.resizer.observe(this)))}async updated(t){if(!this.cards.length&&(this._config.entities&&this._config.entities.length||this._config.cards&&this._config.cards.length)){this.clientWidth;this.cards=await this.build_cards(),this.place_cards(),this.requestUpdate()}t.has("hass")&&this.hass&&this.cards&&this.cards.forEach(t=>{t&&(t.hass=this.hass)})}async build_card(t){if("break"===t)return null;const e={...t,...this._config.card_options},i=function(t){return c?c.createCardElement(t):u("card",t)}(e);return i.hass=s(),i.style.gridColumn=e.gridcol,i.style.gridRow=e.gridrow,this.shadowRoot.querySelector("#staging").appendChild(i),new Promise((t,e)=>i.updateComplete?i.updateComplete.then(()=>t(i)):t(i))}async build_cards(){const t=this.shadowRoot.querySelector("#staging");for(;t.lastChild;)t.removeChild(t.lastChild);return Promise.all((this._config.entities||this._config.cards).map(t=>this.build_card(t)))}place_cards(){"grid"!==this._config.layout&&this.cards.length&&(this.columns=function(t,e,i){const n=t=>"string"==typeof t&&t.endsWith("%")?Math.floor(e*parseInt(t)/100):parseInt(t);let r=0;if("object"==typeof i.column_width){let t=e;for(;t>0;){let e=i.column_width[r];void 0===e&&(e=i.column_width.slice(-1)[0]),t-=n(e),r+=1}r=Math.max(r-1,1)}else r=Math.floor(e/n(i.column_width));r=Math.max(r,i.min_columns),r=Math.min(r,i.max_columns),r=Math.max(r,1);let o=[];for(let t=0;t<r;t++){const t=document.createElement("div");t.classList.add("column"),t.classList.add("cards"),t.length=0,o.push(t)}switch(i.layout){case"horizontal":!function(t,e,i){let n=0;t.forEach(t=>{if(n+=1,!t)return;const i=e[(n-1)%e.length];i.appendChild(t),i.length+=t.getCardSize?t.getCardSize():1})}(t,o);break;case"vertical":!function(t,e,i){let n=0;t.forEach(t=>{if(!t)return void(n+=1);const i=e[n%e.length];i.appendChild(t),i.length+=t.getCardSize?t.getCardSize():1})}(t,o);break;case"auto":default:h(t,o,i)}return o=o.filter(t=>t.childElementCount>0),o}(this.cards,this._layoutWidth||1,this._config),this._config.rtl&&this.columns.reverse(),this.format_columns())}format_columns(){const t=(t,e,i,n="px")=>{if(void 0===this._config[e])return"";let r=`${t}: `;const o=this._config[e];return"object"==typeof o?o.length>i?r+=`${o[i]}`:r+=`${o.slice(-1)}`:r+=`${o}`,r.endsWith("px")||r.endsWith("%")||(r+=n),r+";"};for(const[e,i]of this.columns.entries()){const n=[t("max-width","max_width",e),t("min-width","min_width",e),t("width","column_width",e),t("flex-grow","flex_grow",e,"")];i.style.cssText="".concat(...n)}}getCardSize(){if(this.columns)return Math.max.apply(Math,this.columns.map(t=>t.length))}render(){return"grid"===this._config.layout?r`
        <div id="staging" class="grid"
        style="
        display: grid;
        grid-template-rows: ${this._config.gridrows};
        grid-template-columns: ${this._config.gridcols};
        "></div>
      `:r`
      <div id="columns"
      style="
      ${this._config.justify_content?`justify-content: ${this._config.justify_content};`:""}
      ">
        ${this.columns.map(t=>r`
          ${t}
        `)}
      </div>
      <div id="staging"></div>
    `}static get styles(){return o`
      :host {
        padding: 0;
        display: block;
        margin-bottom: 0!important;
      }
      :host(.panel) {
        padding: 0 4px;
        margin-top: 8px;
      }

      #columns {
        display: flex;
        flex-direction: row;
        justify-content: center;
        margin-top: -8px;
      }

      .column {
        flex-basis: 0;
        flex-grow: 1;
        overflow-x: hidden;
      }
      .column:first-child {
        margin-left: -4px;
      }
      .column:last-child {
        margin-right: -4px;
      }


      .cards>*,
      .grid>* {
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
      #staging.grid {
        margin: 0 -4px;
      }
    `}get _cardModder(){return{target:this}}}if(!customElements.get("layout-card")){customElements.define("layout-card",p);const t=i(4);console.info(`%cLAYOUT-CARD ${t.version} IS INSTALLED`,"color: green; font-weight: bold","")}}]);