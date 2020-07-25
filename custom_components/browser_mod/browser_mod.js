!function(e){var t={};function o(i){if(t[i])return t[i].exports;var s=t[i]={i:i,l:!1,exports:{}};return e[i].call(s.exports,s,s.exports,o),s.l=!0,s.exports}o.m=e,o.c=t,o.d=function(e,t,i){o.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:i})},o.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},o.t=function(e,t){if(1&t&&(e=o(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var i=Object.create(null);if(o.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var s in e)o.d(i,s,function(t){return e[t]}.bind(null,s));return i},o.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return o.d(t,"a",t),t},o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},o.p="",o(o.s=1)}([function(e){e.exports=JSON.parse('{"name":"browser_mod","private":true,"version":"1.1.2","description":"","scripts":{"build":"webpack","watch":"webpack --watch --mode=development","update-card-tools":"npm uninstall card-tools && npm install thomasloven/lovelace-card-tools"},"keywords":[],"author":"Thomas Lovén","license":"MIT","devDependencies":{"webpack":"^4.43.0","webpack-cli":"^3.3.11"},"dependencies":{"card-tools":"github:thomasloven/lovelace-card-tools"}}')},function(e,t,o){"use strict";o.r(t);let i=function(){if(window.fully&&"function"==typeof fully.getDeviceId)return fully.getDeviceId();if(!localStorage["lovelace-player-device-id"]){const e=()=>Math.floor(1e5*(1+Math.random())).toString(16).substring(1);localStorage["lovelace-player-device-id"]=`${e()}${e()}-${e()}${e()}`}return localStorage["lovelace-player-device-id"]}();function s(){return document.querySelector("hc-main")?document.querySelector("hc-main").hass:document.querySelector("home-assistant")?document.querySelector("home-assistant").hass:void 0}function a(e){return document.querySelector("hc-main")?document.querySelector("hc-main").provideHass(e):document.querySelector("home-assistant")?document.querySelector("home-assistant").provideHass(e):void 0}function n(){var e,t=document.querySelector("hc-main");return t?((e=t._lovelaceConfig).current_view=t._lovelacePath,e):(t=(t=(t=(t=(t=(t=(t=(t=(t=document.querySelector("home-assistant"))&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root"))?((e=t.lovelace).current_view=t.___curView,e):null}function r(){var e=document.querySelector("hc-main");return e=e?(e=(e=(e=e&&e.shadowRoot)&&e.querySelector("hc-lovelace"))&&e.shadowRoot)&&e.querySelector("hui-view")||e.querySelector("hui-panel-view"):(e=(e=(e=(e=(e=(e=(e=(e=(e=(e=(e=(e=document.querySelector("home-assistant"))&&e.shadowRoot)&&e.querySelector("home-assistant-main"))&&e.shadowRoot)&&e.querySelector("app-drawer-layout partial-panel-resolver"))&&e.shadowRoot||e)&&e.querySelector("ha-panel-lovelace"))&&e.shadowRoot)&&e.querySelector("hui-root"))&&e.shadowRoot)&&e.querySelector("ha-app-layout"))&&e.querySelector("#view"))&&e.firstElementChild}async function l(){if(customElements.get("hui-view"))return!0;await customElements.whenDefined("partial-panel-resolver");const e=document.createElement("partial-panel-resolver");if(e.hass={panels:[{url_path:"tmp",component_name:"lovelace"}]},e._updateRoutes(),await e.routerOptions.routes.tmp.load(),!customElements.get("ha-panel-lovelace"))return!1;const t=document.createElement("ha-panel-lovelace");return t.hass=s(),t.panel={config:{mode:null}},t._fetchConfig(),!0}async function c(e,t,o=!1){let i=e;"string"==typeof t&&(t=t.split(/(?=\$)|(?<=\$)| /));for(const[e,s]of t.entries()){if(!i)return null;i.localName&&i.localName.includes("-")&&await customElements.whenDefined(i.localName),i.updateComplete&&await i.updateComplete,i="$"===s?o&&e==t.length-1?[i.shadowRoot]:i.shadowRoot:o&&e==t.length-1?i.querySelectorAll(s):i.querySelector(s)}return i}async function d(e,t,o=!1,i=1e4){return Promise.race([c(e,t,o),new Promise((e,t)=>setTimeout(()=>t(new Error("timeout")),i))]).catch(e=>{if(!e.message||"timeout"!==e.message)throw e;return null})}function u(e,t,o=null){if((e=new Event(e,{bubbles:!0,cancelable:!1,composed:!0})).detail=t||{},o)o.dispatchEvent(e);else{var i=r();i&&i.dispatchEvent(e)}}let h=window.cardHelpers;new Promise(async(e,t)=>{h&&e();const o=async()=>{h=await window.loadCardHelpers(),window.cardHelpers=h,e()};window.loadCardHelpers?o():window.addEventListener("load",async()=>{l(),window.loadCardHelpers&&o()})});async function m(e,t,o=!1,i={},s=!1){if(!customElements.get("card-tools-popup")){const e=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),t=e.prototype.html,o=e.prototype.css;class i extends e{static get properties(){return{open:{},large:{reflect:!0,type:Boolean},hass:{}}}updated(e){e.has("hass")&&this.card&&(this.card.hass=this.hass)}closeDialog(){this.open=!1}async _makeCard(){const e=await window.loadCardHelpers();this.card=await e.createCardElement(this._card),this.card.hass=this.hass,this.requestUpdate()}async _applyStyles(){let e=await d(this,"$ ha-dialog");customElements.whenDefined("card-mod").then(async()=>{if(!e)return;customElements.get("card-mod").applyToElement(e,"more-info",this._style,{config:this._card},[],!1)})}async showDialog(e,t,o=!1,i={},s=!1){this.title=e,this._card=t,this.large=o,this._style=i,this.fullscreen=!!s,this._makeCard(),await this.updateComplete,this.open=!0,await this._applyStyles()}_enlarge(){this.large=!this.large}render(){return this.open?t`
            <ha-dialog
              open
              @closed=${this.closeDialog}
              .heading=${!0}
              hideActions
              @ll-rebuild=${this._makeCard}
            >
            ${this.fullscreen?t`<div slot="heading"></div>`:t`
                <app-toolbar slot="heading">
                  <mwc-icon-button
                    .label=${"dismiss"}
                    dialogAction="cancel"
                  >
                    <ha-icon
                      .icon=${"mdi:close"}
                    ></ha-icon>
                  </mwc-icon-button>
                  <div class="main-title" @click=${this._enlarge}>
                    ${this.title}
                  </div>
                </app-toolbar>
              `}
              <div class="content">
                ${this.card}
              </div>
            </ha-dialog>
          `:t``}static get styles(){return o`
          ha-dialog {
            --mdc-dialog-min-width: 400px;
            --mdc-dialog-max-width: 600px;
            --mdc-dialog-heading-ink-color: var(--primary-text-color);
            --mdc-dialog-content-ink-color: var(--primary-text-color);
            --justify-action-buttons: space-between;
          }
          @media all and (max-width: 450px), all and (max-height: 500px) {
            ha-dialog {
              --mdc-dialog-min-width: 100vw;
              --mdc-dialog-max-width: 100vw;
              --mdc-dialog-min-height: 100%;
              --mdc-dialog-max-height: 100%;
              --mdc-shape-medium: 0px;
              --vertial-align-dialog: flex-end;
            }
          }

          app-toolbar {
            flex-shrink: 0;
            color: var(--primary-text-color);
            background-color: var(--secondary-background-color);
          }

          .main-title {
            margin-left: 16px;
            line-height: 1.3em;
            max-height: 2.6em;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
          }
          .content {
            margin: -20px -24px;
          }

          @media all and (max-width: 450px), all and (max-height: 500px) {
            app-toolbar {
              background-color: var(--app-header-background-color);
              color: var(--app-header-text-color, white);
            }
          }

          @media all and (min-width: 451px) and (min-height: 501px) {
            ha-dialog {
              --mdc-dialog-max-width: 90vw;
            }

            .content {
              width: 400px;
            }
            :host([large]) .content {
              width: calc(90vw - 48px);
            }

            :host([large]) app-toolbar {
              max-width: calc(90vw - 32px);
            }
          }
          `}}customElements.define("card-tools-popup",i)}const n=document.querySelector("home-assistant")||document.querySelector("hc-root");if(!n)return;let r=await d(n,"$ card-tools-popup");if(r||(r=document.createElement("card-tools-popup"),n.shadowRoot.appendChild(r),a(r)),!window._moreInfoDialogListener){const e=async e=>{if(e.state&&"cardToolsPopup"in e.state)if(e.state.cardToolsPopup){const{title:t,card:o,large:i,style:s,fullscreen:a}=e.state.params;m(t,o,i,s,a)}else r.closeDialog()};window.addEventListener("popstate",e),window._moreInfoDialogListener=!0}history.replaceState({cardToolsPopup:!1},""),history.pushState({cardToolsPopup:!0,params:{title:e,card:t,large:o,style:i,fullscreen:s}},""),r.showDialog(e,t,o,i,s)}function p(e,t=!1){const o=document.querySelector("hc-main")||document.querySelector("home-assistant");u("hass-more-info",{entityId:e},o);const i=o._moreInfoEl;return i.large=t,i}const w=[customElements.whenDefined("home-assistant-main"),customElements.whenDefined("hui-view")];Promise.race(w).then(()=>{const e=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),t=e.prototype.html;e.prototype.css;class o extends e{setConfig(e){}render(){return t`
          <div>
          Nothing to configure.
          </div>
          `}}customElements.get("browser-player-editor")||(customElements.define("browser-player-editor",o),window.customCards=window.customCards||[],window.customCards.push({type:"browser-player",name:"Browser Player",preview:!0}))});const y=[customElements.whenDefined("home-assistant-main"),customElements.whenDefined("hui-view")];Promise.race(y).then(()=>{const e=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),t=e.prototype.html,o=e.prototype.css;customElements.get("browser-player")||customElements.define("browser-player",class extends e{static get properties(){return{hass:{}}}static getConfigElement(){return document.createElement("browser-player-editor")}static getStubConfig(){return{}}setConfig(e){this._config=e}handleMute(e){window.browser_mod.mute({})}handleVolumeChange(e){const t=parseFloat(e.target.value);window.browser_mod.set_volume({volume_level:t})}handleMoreInfo(e){p("media_player."+window.browser_mod.entity_id)}handlePlayPause(e){window.browser_mod.player.paused?window.browser_mod.play({}):window.browser_mod.pause({})}render(){if(!window.browser_mod)return window.setTimeout(()=>this.requestUpdate(),100),t``;const e=window.browser_mod.player;return t`
    <ha-card>
      <div class="card-content">
      <ha-icon-button
        .icon=${e.muted?"mdi:volume-off":"mdi:volume-high"}
        @click=${this.handleMute}
      ></ha-icon-button>
      <ha-paper-slider
        min=0
        max=1
        step=0.01
        ?disabled=${e.muted}
        value=${e.volume}
        @change=${this.handleVolumeChange}
      ></ha-paper-slider>

      ${"stopped"===window.browser_mod.player_state?t`<div class="placeholder"></div>`:t`
          <paper-icon-button
            .icon=${e.paused?"mdi:play":"mdi:pause"}
            @click=${this.handlePlayPause}
            highlight
          ></paper-icon-button>
          `}
      <paper-icon-button
        .icon=${"mdi:settings"}
        @click=${this.handleMoreInfo}
      ></paper-icon-button>
      </div>

      <div class="device-id">
      ${i}
      </div>

    </ha-card>
    `}static get styles(){return o`
    paper-icon-button[highlight] {
      color: var(--accent-color);
    }
    .card-content {
      display: flex;
      justify-content: center;
    }
    .placeholder {
      width: 24px;
      padding: 8px;
    }
    .device-id {
      opacity: 0.7;
      font-size: xx-small;
      margin-top: -10px;
      user-select: all;
      -webkit-user-select: all;
      -moz-user-select: all;
      -ms-user-select: all;
    }
    `}})});class v{set hass(e){if(!e)return;if(this._hass=e,this.hassPatched)return;const t=e.callService;e.callService=(e,o,s)=>{if(s&&s.deviceID)if(Array.isArray(s.deviceID)){const e=s.deviceID.indexOf("this");-1!==e&&((s=JSON.parse(JSON.stringify(s))).deviceID[e]=i)}else"this"===s.deviceID&&((s=JSON.parse(JSON.stringify(s))).deviceID=i);return t(e,o,s)},this.hassPatched=!0,document.querySelector("hc-main")?document.querySelector("hc-main").hassChanged(e,e):document.querySelector("home-assistant").hassChanged(e,e)}playOnce(e){this._video&&this._video.play(),window.browser_mod.playedOnce||(window.browser_mod.player.play(),window.browser_mod.playedOnce=!0)}async _load_lovelace(){if(!await l()){window.setTimeout(this._load_lovelace.bind(this),100)}}_connect(){window.hassConnection?window.hassConnection.then(e=>this.connect(e.conn)):window.setTimeout(()=>this._connect(),100)}constructor(){this.entity_id=i.replace("-","_"),this.cast=null!==document.querySelector("hc-main"),this.cast?this.connect(s().connection):(window.setTimeout(this._load_lovelace.bind(this),500),this._connect(),document.querySelector("home-assistant").addEventListener("hass-more-info",this.popup_card.bind(this))),this.player=new Audio,this.playedOnce=!1,this.autoclose_popup_active=!1;const e=this.update.bind(this);this.player.addEventListener("ended",e),this.player.addEventListener("play",e),this.player.addEventListener("pause",e),this.player.addEventListener("volumechange",e),document.addEventListener("visibilitychange",e),window.addEventListener("location-changed",e),window.addEventListener("click",this.playOnce),window.addEventListener("mousemove",this.no_blackout.bind(this)),window.addEventListener("mousedown",this.no_blackout.bind(this)),window.addEventListener("keydown",this.no_blackout.bind(this)),window.addEventListener("touchstart",this.no_blackout.bind(this)),a(this),window.fully&&(this._fullyMotion=!1,this._motionTimeout=void 0,fully.bind("screenOn","browser_mod.update();"),fully.bind("screenOff","browser_mod.update();"),fully.bind("pluggedAC","browser_mod.update();"),fully.bind("pluggedUSB","browser_mod.update();"),fully.bind("onBatteryLevelChanged","browser_mod.update();"),fully.bind("unplugged","browser_mod.update();"),fully.bind("networkReconnect","browser_mod.update();"),fully.bind("onMotion","browser_mod.fullyMotion();")),this._screenSaver=void 0,this._screenSaverTimer=void 0,this._screenSaverTime=0,this._blackout=document.createElement("div"),this._blackout.style.cssText="\n    position: fixed;\n    left: 0;\n    top: 0;\n    padding: 0;\n    margin: 0;\n    width: 100%;\n    height: 100%;\n    background: black;\n    visibility: hidden;\n    ",document.body.appendChild(this._blackout);const t=o(0);console.info(`%cBROWSER_MOD ${t.version} IS INSTALLED\n    %cDeviceID: ${i}`,"color: green; font-weight: bold","")}connect(e){this.conn=e,e.subscribeMessage(e=>this.callback(e),{type:"browser_mod/connect",deviceID:i})}callback(e){switch(e.command){case"update":this.update(e);break;case"debug":this.debug(e);break;case"play":this.play(e);break;case"pause":this.pause(e);break;case"stop":this.stop(e);break;case"set_volume":this.set_volume(e);break;case"mute":this.mute(e);break;case"toast":this.toast(e);break;case"popup":this.popup(e);break;case"close-popup":this.close_popup(e);break;case"navigate":this.navigate(e);break;case"more-info":this.more_info(e);break;case"set-theme":this.set_theme(e);break;case"lovelace-reload":this.lovelace_reload(e);break;case"blackout":this.blackout(e);break;case"no-blackout":this.no_blackout(e)}}get player_state(){return this.player.src?this.player.ended?"stopped":this.player.paused?"paused":"playing":"stopped"}popup_card(e){if(!n())return;const t=n(),o={...t.config.popup_cards,...t.config.views[t.current_view].popup_cards};if(!e.detail||!e.detail.entityId)return;const i=o[e.detail.entityId];i&&window.setTimeout(()=>{u("hass-more-info",{entityId:"."},document.querySelector("home-assistant")),m(i.title,i.card,i.large||!1,i.style)},50)}debug(e){m("deviceID",{type:"markdown",content:"# "+i}),alert(i)}_set_screensaver(e,t){if(clearTimeout(this._screenSaverTimer),e){if(-1==(t=parseInt(t)))return clearTimeout(this._screenSaverTimer),void(this._screenSaverTime=0);this._screenSaverTime=1e3*t,this._screenSaver=e,this._screenSaverTimer=setTimeout(this._screenSaver,this._screenSaverTime)}else this._screenSaverTime&&(this._screenSaverTimer=setTimeout(this._screenSaver,this._screenSaverTime))}play(e){const t=e.media_content_id;t&&(this.player.src=t),this.player.play()}pause(e){this.player.pause()}stop(e){this.player.pause(),this.player.src=null}set_volume(e){void 0!==e.volume_level&&(this.player.volume=e.volume_level)}mute(e){void 0===e.mute&&(e.mute=!this.player.muted),this.player.muted=Boolean(e.mute)}toast(e){e.message&&u("hass-notification",{message:e.message,duration:void 0!==e.duration?parseInt(e.duration):void 0},document.querySelector("home-assistant"))}popup(e){if(!e.title&&!e.auto_close)return;if(!e.card)return;const t=()=>{m(e.title,e.card,e.large,e.style,e.auto_close||e.hide_header),e.auto_close&&(this.autoclose_popup_active=!0)};e.auto_close&&e.time?this._set_screensaver(t,e.time):t()}close_popup(e){this._set_screensaver(),this.autoclose_popup_active=!1,async function(){const e=document.querySelector("home-assistant")||document.querySelector("hc-root"),t=await d(e,"$ card-tools-popup");t&&t.closeDialog()}()}navigate(e){e.navigation_path&&(history.pushState(null,"",e.navigation_path),u("location-changed",{},document.querySelector("home-assistant")))}more_info(e){e.entity_id&&p(e.entity_id,e.large)}set_theme(e){e.theme||(e.theme="default"),u("settheme",e.theme,document.querySelector("home-assistant"))}lovelace_reload(e){const t=r();t&&u("config-refresh",{},t)}blackout(e){const t=()=>{window.fully?fully.turnScreenOff():this._blackout.style.visibility="visible",this.update()};e.time?this._set_screensaver(t,e.time):t()}no_blackout(e){if(this._set_screensaver(),this.autoclose_popup_active)return this.close_popup();window.fully?(fully.getScreenOn()||fully.turnScreenOn(),e.brightness&&fully.setScreenBrightness(e.brightness),this.update()):"hidden"!==this._blackout.style.visibility&&(this._blackout.style.visibility="hidden",this.update())}is_blackout(){return window.fully?!fully.getScreenOn():Boolean("visible"===this._blackout.style.visibility)}fullyMotion(){this._fullyMotion=!0,clearTimeout(this._motionTimeout),this._motionTimeout=setTimeout(()=>{this._fullyMotion=!1,this.update()},5e3),this.update()}start_camera(){this._video||(this._video=document.createElement("video"),this._video.autoplay=!0,this._video.playsInline=!0,this._video.style.cssText="\n    visibility: hidden;\n    width: 0;\n    height: 0;\n    ",this._canvas=document.createElement("canvas"),this._canvas.style.cssText="\n    visibility: hidden;\n    width: 0;\n    height: 0;\n    ",document.body.appendChild(this._canvas),document.body.appendChild(this._video),navigator.mediaDevices.getUserMedia({video:!0,audio:!1}).then(e=>{this._video.srcObject=e,this._video.play(),this.send_cam()}))}send_cam(e){this._canvas.getContext("2d").drawImage(this._video,0,0,this._canvas.width,this._canvas.height),this.conn.sendMessage({type:"browser_mod/update",deviceID:i,data:{camera:this._canvas.toDataURL("image/png")}}),setTimeout(this.send_cam.bind(this),5e3)}update(e=null){this.conn&&(e&&(e.name&&(this.entity_id=e.name.toLowerCase()),e.camera&&this.start_camera()),this.conn.sendMessage({type:"browser_mod/update",deviceID:i,data:{browser:{path:window.location.pathname,visibility:document.visibilityState,userAgent:navigator.userAgent,currentUser:this._hass&&this._hass.user&&this._hass.user.name,fullyKiosk:!!window.fully||void 0,width:window.innerWidth,height:window.innerHeight},player:{volume:this.player.volume,muted:this.player.muted,src:this.player.src,state:this.player_state},screen:{blackout:this.is_blackout(),brightness:window.fully?fully.getScreenBrightness():void 0},fully:window.fully?{battery:window.fully?fully.getBatteryLevel():void 0,charging:window.fully?fully.isPlugged():void 0,motion:window.fully?this._fullyMotion:void 0}:void 0}}))}}const g=[customElements.whenDefined("home-assistant-main"),customElements.whenDefined("hui-view")];Promise.race(g).then(()=>{window.browser_mod=window.browser_mod||new v})}]);