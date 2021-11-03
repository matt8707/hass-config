const e="lovelace-player-device-id";function t(){if(!localStorage[e]){const t=()=>Math.floor(1e5*(1+Math.random())).toString(16).substring(1);window.fully&&"function"==typeof fully.getDeviceId?localStorage[e]=fully.getDeviceId():localStorage[e]=`${t()}${t()}-${t()}${t()}`}return localStorage[e]}let s=t();const o=o=>{null!==o&&("clear"===o?localStorage.removeItem(e):localStorage[e]=o,s=t())},i=new URLSearchParams(window.location.search);function a(){return document.querySelector("hc-main")?document.querySelector("hc-main").hass:document.querySelector("home-assistant")?document.querySelector("home-assistant").hass:void 0}function n(e){return document.querySelector("hc-main")?document.querySelector("hc-main").provideHass(e):document.querySelector("home-assistant")?document.querySelector("home-assistant").provideHass(e):void 0}function r(){var e,t=document.querySelector("hc-main");return t?((e=t._lovelaceConfig).current_view=t._lovelacePath,e):(t=(t=(t=(t=(t=(t=(t=(t=(t=document.querySelector("home-assistant"))&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root"))?((e=t.lovelace).current_view=t.___curView,e):null}function l(){var e=document.querySelector("hc-main");return e=e?(e=(e=(e=e&&e.shadowRoot)&&e.querySelector("hc-lovelace"))&&e.shadowRoot)&&e.querySelector("hui-view")||e.querySelector("hui-panel-view"):(e=(e=(e=(e=(e=(e=(e=(e=(e=(e=(e=(e=document.querySelector("home-assistant"))&&e.shadowRoot)&&e.querySelector("home-assistant-main"))&&e.shadowRoot)&&e.querySelector("app-drawer-layout partial-panel-resolver"))&&e.shadowRoot||e)&&e.querySelector("ha-panel-lovelace"))&&e.shadowRoot)&&e.querySelector("hui-root"))&&e.shadowRoot)&&e.querySelector("ha-app-layout"))&&e.querySelector("#view"))&&e.firstElementChild}async function c(){if(customElements.get("hui-view"))return!0;await customElements.whenDefined("partial-panel-resolver");const e=document.createElement("partial-panel-resolver");if(e.hass={panels:[{url_path:"tmp",component_name:"lovelace"}]},e._updateRoutes(),await e.routerOptions.routes.tmp.load(),!customElements.get("ha-panel-lovelace"))return!1;const t=document.createElement("ha-panel-lovelace");return t.hass=a(),void 0===t.hass&&(await new Promise((e=>{window.addEventListener("connection-status",(t=>{console.log(t),e()}),{once:!0})})),t.hass=a()),t.panel={config:{mode:null}},t._fetchConfig(),!0}async function d(e,t,s=!1){let o=e;"string"==typeof t&&(t=t.split(/(\$| )/)),""===t[t.length-1]&&t.pop();for(const[e,i]of t.entries())if(i.trim().length){if(!o)return null;o.localName&&o.localName.includes("-")&&await customElements.whenDefined(o.localName),o.updateComplete&&await o.updateComplete,o="$"===i?s&&e==t.length-1?[o.shadowRoot]:o.shadowRoot:s&&e==t.length-1?o.querySelectorAll(i):o.querySelector(i)}return o}async function h(e,t,s=!1,o=1e4){return Promise.race([d(e,t,s),new Promise(((e,t)=>setTimeout((()=>t(new Error("timeout"))),o)))]).catch((e=>{if(!e.message||"timeout"!==e.message)throw e;return null}))}function u(e,t,s=null){if((e=new Event(e,{bubbles:!0,cancelable:!1,composed:!0})).detail=t||{},s)s.dispatchEvent(e);else{var o=l();o&&o.dispatchEvent(e)}}i.get("deviceID")&&o(i.get("deviceID"));let m=window.cardHelpers;async function p(){const e=document.querySelector("home-assistant")||document.querySelector("hc-root");u("hass-more-info",{entityId:"."},e);const t=await h(e,"$ card-tools-popup");t&&t.closeDialog()}async function w(e,t,s=!1,o={},i=!1){if(!customElements.get("card-tools-popup")){const e=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),t=e.prototype.html,s=e.prototype.css;class o extends e{static get properties(){return{open:{},large:{reflect:!0,type:Boolean},hass:{}}}updated(e){e.has("hass")&&this.card&&(this.card.hass=this.hass)}closeDialog(){this.open=!1}async _makeCard(){const e=await window.loadCardHelpers();this.card=await e.createCardElement(this._card),this.card.hass=this.hass,this.requestUpdate()}async _applyStyles(){let e=await h(this,"$ ha-dialog");customElements.whenDefined("card-mod").then((async()=>{if(!e)return;customElements.get("card-mod").applyToElement(e,"more-info",this._style,{config:this._card},[],!1)}))}async showDialog(e,t,s=!1,o={},i=!1){this.title=e,this._card=t,this.large=s,this._style=o,this.fullscreen=!!i,this._makeCard(),await this.updateComplete,this.open=!0,await this._applyStyles()}_enlarge(){this.large=!this.large}render(){return this.open?t`
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
          `:t``}static get styles(){return s`
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
          `}}customElements.define("card-tools-popup",o)}const a=document.querySelector("home-assistant")||document.querySelector("hc-root");if(!a)return;let r=await h(a,"$ card-tools-popup");if(!r){r=document.createElement("card-tools-popup");const e=a.shadowRoot.querySelector("ha-more-info-dialog");e?a.shadowRoot.insertBefore(r,e):a.shadowRoot.appendChild(r),n(r)}if(!window._moreInfoDialogListener){const e=async e=>{if(e.state&&"cardToolsPopup"in e.state)if(e.state.cardToolsPopup){const{title:t,card:s,large:o,style:i,fullscreen:a}=e.state.params;w(t,s,o,i,a)}else r.closeDialog()};window.addEventListener("popstate",e),window._moreInfoDialogListener=!0}history.replaceState({cardToolsPopup:!1},""),history.pushState({cardToolsPopup:!0,params:{title:e,card:t,large:s,style:o,fullscreen:i}},""),r.showDialog(e,t,s,o,i)}async function y(e,t=!1){const s=document.querySelector("hc-main")||document.querySelector("home-assistant");u("hass-more-info",{entityId:e},s);const o=await h(s,"$ ha-more-info-dialog");return o&&(o.large=t),o}new Promise((async(e,t)=>{m&&e();const s=async()=>{m=await window.loadCardHelpers(),window.cardHelpers=m,e()};window.loadCardHelpers?s():window.addEventListener("load",(async()=>{c(),window.loadCardHelpers&&s()}))}));const _=[customElements.whenDefined("home-assistant-main"),customElements.whenDefined("hui-view")];Promise.race(_).then((()=>{const e=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),t=e.prototype.html;e.prototype.css;class s extends e{setConfig(e){}render(){return t` <div>Nothing to configure.</div> `}}customElements.get("browser-player-editor")||(customElements.define("browser-player-editor",s),window.customCards=window.customCards||[],window.customCards.push({type:"browser-player",name:"Browser Player",preview:!0}))}));const v=[customElements.whenDefined("home-assistant-main"),customElements.whenDefined("hui-view")];Promise.race(v).then((()=>{const e=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),t=e.prototype.html,i=e.prototype.css;customElements.get("browser-player")||customElements.define("browser-player",class extends e{static get properties(){return{hass:{}}}static getConfigElement(){return document.createElement("browser-player-editor")}static getStubConfig(){return{}}async setConfig(e){for(this._config=e;!window.browser_mod;)await new Promise((e=>setTimeout(e,1e3)));for(const e of["play","pause","ended","volumechange","canplay","loadeddata"])window.browser_mod.player.addEventListener(e,(()=>this.requestUpdate()))}handleMute(e){window.browser_mod.player_mute()}handleVolumeChange(e){const t=parseFloat(e.target.value);window.browser_mod.player_set_volume(t)}handleMoreInfo(e){y("media_player."+window.browser_mod.entity_id)}handlePlayPause(e){window.browser_mod.player.paused?window.browser_mod.player_play():window.browser_mod.player_pause()}setDeviceID(){const e=prompt("Set deviceID",s);e!==s&&(o(e),this.requestUpdate())}render(){if(!window.browser_mod)return window.setTimeout((()=>this.requestUpdate()),100),t``;const e=window.browser_mod.player;return t`
        <ha-card>
          <div class="card-content">
            <ha-icon-button @click=${this.handleMute}>
              <ha-icon
                .icon=${e.muted?"mdi:volume-off":"mdi:volume-high"}
              ></ha-icon>
            </ha-icon-button>
            <ha-slider
              min="0"
              max="1"
              step="0.01"
              ?disabled=${e.muted}
              value=${e.volume}
              @change=${this.handleVolumeChange}
            ></ha-slider>

            ${"stopped"===window.browser_mod.player_state?t`<div class="placeholder"></div>`:t`
                  <ha-icon-button @click=${this.handlePlayPause} highlight>
                    <ha-icon
                      .icon=${e.paused?"mdi:play":"mdi:pause"}
                    ></ha-icon>
                  </ha-icon-button>
                `}
            <ha-icon-button @click=${this.handleMoreInfo}>
              <ha-icon .icon=${"mdi:cog"}></ha-icon>
            </ha-icon-button>
          </div>

          <div class="device-id" @click=${this.setDeviceID}>${s}</div>
        </ha-card>
      `}static get styles(){return i`
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
        ha-icon-button ha-icon {
          display: flex;
        }
      `}})}));class g{async connect(){if(null!==document.querySelector("hc-main"))this._connection=a().connection;else{if(!window.hassConnection)return void window.setTimeout((()=>this.connect()),100);this._connection=(await window.hassConnection).conn}this._connection.subscribeMessage((e=>this.msg_callback(e)),{type:"browser_mod/connect",deviceID:s}),this._hass_patched=!1,n(this)}set hass(e){this._hass=e}get connected(){return void 0!==this._connection}msg_callback(e){console.log(e)}sendUpdate(e){this.connected&&this._connection.sendMessage({type:"browser_mod/update",deviceID:s,data:e})}}const f=e=>class extends e{constructor(){super(),this.player=new Audio;for(const e of["play","pause","ended","volumechange"])this.player.addEventListener(e,(()=>this.player_update()));window.addEventListener("click",(()=>{this.player.ended||this.player.play()}),{once:!0})}player_update(e){this.sendUpdate({player:{volume:this.player.volume,muted:this.player.muted,src:this.player.src,state:this.player_state}})}get player_state(){return this.player.src?this.player.ended?"stopped":this.player.paused?"paused":"playing":"stopped"}player_play(e){e&&(this.player.src=e),this.player.play()}player_pause(){this.player.pause()}player_stop(){this.player.pause(),this.player.src=null}player_set_volume(e){void 0!==e&&(this.player.volume=e)}player_mute(e){void 0===e&&(e=!this.player.muted),this.player.muted=Boolean(e)}},b=e=>class extends e{get isFully(){return void 0!==window.fully}constructor(){if(super(),this.isFully){this._fullyMotion=!1,this._motionTimeout=void 0;for(const e of["screenOn","screenOff","pluggedAC","pluggedUSB","onBatteryLevelChanged","unplugged","networkReconnect","onMotion"])window.fully.bind(e,`window.browser_mod.fully_update("${e}");`);window.fully.bind("onScreensaverStart","window.browser_mod.fully_screensaver = true; window.browser_mod.screen_update();"),window.fully.bind("onScreensaverStop","window.browser_mod.fully_screensaver = false; window.browser_mod.screen_update();"),this._keepingAlive=!1}}fully_update(e){this.isFully&&("screenOn"===e?(window.clearTimeout(this._keepAliveTimer),this._keepingAlive||this.screen_update()):"screenOff"===e?(this.screen_update(),this._keepingAlive=!1,this.config.force_stay_awake&&(this._keepAliveTimer=window.setTimeout((()=>{this._keepingAlive=!0,window.fully.turnScreenOn(),window.fully.turnScreenOff()}),27e4))):"onMotion"===e&&this.fullyMotionTriggered(),this.sendUpdate({fully:{battery:window.fully.getBatteryLevel(),charging:window.fully.isPlugged(),motion:this._fullyMotion,ip:window.fully.getIp4Address()}}))}startCamera(){void 0===this._fullyCameraTimer&&(this._fullyCameraTimer=window.setInterval((()=>{this.sendUpdate({camera:window.fully.getCamshotJpgBase64()})}),200))}stopCamera(){window.clearInterval(this._fullyCameraTimer),this._fullyCameraTimer=void 0}fullyMotionTriggered(){this._keepingAlive||(this._fullyMotion=!0,this.startCamera(),clearTimeout(this._motionTimeout),this._motionTimeout=setTimeout((()=>{this._fullyMotion=!1,this.stopCamera(),this.fully_update()}),5e3),this.fully_update())}},S=e=>class extends e{setup_camera(){console.log("Starting camera"),this._video||(this._video=document.createElement("video"),this._video.autoplay=!0,this._video.playsInline=!0,this._video.style.display="none",this._canvas=document.createElement("canvas"),this._canvas.style.display="none",document.body.appendChild(this._video),document.body.appendChild(this._canvas),navigator.mediaDevices&&(console.log("Starting devices"),navigator.mediaDevices.getUserMedia({video:!0,audio:!1}).then((e=>{this._video.srcObject=e,this._video.play(),this.update_camera()})),this._camera_framerate=2,window.addEventListener("click",(()=>{(this._video.ended||this._video.paused)&&this._video.play()}),{once:!0})))}update_camera(){this._canvas.width=this._video.videoWidth,this._canvas.height=this._video.videoHeight;this._canvas.getContext("2d").drawImage(this._video,0,0,this._video.videoWidth,this._video.videoHeight),this.sendUpdate({camera:this._canvas.toDataURL("image/jpeg")}),setTimeout((()=>this.update_camera()),Math.round(1e3/this._camera_framerate))}},k=e=>class extends e{constructor(){super(),this._blackout_panel=document.createElement("div"),this._screenSaver=void 0,this._screenSaverTimer=void 0,this._screenSaverTimeOut=0,this._screenSaver={fn:void 0,clearfn:void 0,timer:void 0,timeout:void 0,listeners:{},active:!1},this._blackout_panel.style.cssText="\n            position: fixed;\n            left: 0;\n            top: 0;\n            padding: 0;\n            margin: 0;\n            width: 100%;\n            height: 100%;\n            background: black;\n            display: none;\n        ",document.body.appendChild(this._blackout_panel)}screensaver_set(e,t,s){this._ss_clear(),this._screenSaver={fn:e,clearfn:t,timer:void 0,timeout:s,listeners:{},active:!1};const o=()=>this.screensaver_update();for(const e of["mousemove","mousedown","keydown","touchstart"])window.addEventListener(e,o),this._screenSaver.listeners[e]=o;this._screenSaver.timer=window.setTimeout((()=>this._ss_run()),1e3*s)}screensaver_update(){this._screenSaver.active?this.screensaver_stop():(window.clearTimeout(this._screenSaver.timer),this._screenSaver.timer=window.setTimeout((()=>this._ss_run()),1e3*this._screenSaver.timeout))}screensaver_stop(){this._ss_clear(),this._screenSaver.active=!1,this._screenSaver.clearfn&&this._screenSaver.clearfn(),this._screenSaver.timeout&&this.screensaver_set(this._screenSaver.fn,this._screenSaver.clearfn,this._screenSaver.timeout)}_ss_clear(){window.clearTimeout(this._screenSaverTimer);for(const[e,t]of Object.entries(this._screenSaver.listeners))window.removeEventListener(e,t)}_ss_run(){this._screenSaver.active=!0,this._screenSaver.fn()}do_blackout(e){this.screensaver_set((()=>{this.isFully?this.config.screensaver?window.fully.startScreensaver():window.fully.turnScreenOff(!0):this._blackout_panel.style.display="block",this.screen_update()}),(()=>{(this._blackout_panel.style.display="block")&&(this._blackout_panel.style.display="none"),this.isFully&&(window.fully.getScreenOn()||window.fully.turnScreenOn(),window.fully.stopScreensaver()),this.screen_update()}),e||0)}no_blackout(){this.isFully&&(window.fully.turnScreenOn(),window.fully.stopScreensaver()),this.screensaver_stop()}screen_update(){this.sendUpdate({screen:{blackout:this.isFully?void 0!==this.fully_screensaver?this.fully_screensaver:!window.fully.getScreenOn():Boolean("block"===this._blackout_panel.style.display),brightness:this.isFully?window.fully.getScreenBrightness():void 0}})}},E=e=>class extends e{constructor(){super(),document.querySelector("home-assistant")&&document.querySelector("home-assistant").addEventListener("hass-more-info",(e=>this._popup_card(e)));null!==document.querySelector("hc-main")||c()}_popup_card(e){if(!r())return;if(!e.detail||!e.detail.entityId)return;const t={...r().config.popup_cards,...r().config.views[r().current_view].popup_cards}[e.detail.entityId];t&&(this.do_popup(t),window.setTimeout((()=>{u("hass-more-info",{entityID:"."},document.querySelector("home-assistant"))}),50))}do_popup(e){if(!(e.title||e.auto_close||e.hide_header))return void console.error("browser_mod: popup: Must specify title, auto_close or hide_header.");if(!e.card)return void console.error("browser_mod: popup: No card specified");const t=()=>{w(e.title,e.card,e.large,e.style,e.auto_close||e.hide_header)};e.auto_close?this.screensaver_set(t,p,e.time):t()}do_close_popup(){this.screensaver_stop(),p()}do_more_info(e,t){e&&y(e,t)}do_toast(e,t){e&&u("hass-notification",{message:e,duration:parseInt(t)},document.querySelector("home-assistant"))}},x=e=>class extends e{constructor(){super(),document.addEventListener("visibilitychange",(()=>this.sensor_update())),window.addEventListener("location-changed",(()=>this.sensor_update())),window.setInterval((()=>this.sensor_update()),1e4)}sensor_update(){(async()=>{const e=navigator.getBattery?await navigator.getBattery():void 0;this.sendUpdate({browser:{path:window.location.pathname,visibility:document.visibilityState,userAgent:navigator.userAgent,currentUser:this._hass&&this._hass.user&&this._hass.user.name,fullyKiosk:this.isFully,width:window.innerWidth,height:window.innerHeight,battery_level:this.isFully?window.fully.getBatteryLevel():e?100*e.level:void 0,charging:this.isFully?window.fully.isPlugged():e?e.charging:void 0,darkMode:this._hass&&this._hass.themes&&this._hass.themes.darkMode,userData:this._hass&&this._hass.user,config:this.config}})})()}do_navigate(e){e&&(history.pushState(null,"",e),u("location-changed",{},document.querySelector("home-assistant")))}};var q="1.5.1";class C extends(((e,t)=>t.reduceRight(((e,t)=>t(e)),e))(g,[x,E,k,S,b,f])){constructor(){super(),this.entity_id=s.replace("-","_"),this.cast=null!==document.querySelector("hc-main"),this.connect(),document.body.addEventListener("ll-custom",(e=>{e.detail.browser_mod&&this.msg_callback(e.detail.browser_mod)})),console.info(`%cBROWSER_MOD ${q} IS INSTALLED\n    %cDeviceID: ${s}`,"color: green; font-weight: bold","")}async msg_callback(e){const t={update:e=>this.update(e),debug:e=>this.debug(e),play:e=>this.player_play(e.media_content_id),pause:e=>this.player_pause(),stop:e=>this.player_stop(),"set-volume":e=>this.player_set_volume(e.volume_level),mute:e=>this.player_mute(e.mute),toast:e=>this.do_toast(e.message,e.duration),popup:e=>this.do_popup(e),"close-popup":e=>this.do_close_popup(),"more-info":e=>this.do_more_info(e.entity_id,e.large),navigate:e=>this.do_navigate(e.navigation_path),"set-theme":e=>this.set_theme(e),"lovelace-reload":e=>this.lovelace_reload(e),"window-reload":()=>window.location.reload(),blackout:e=>this.do_blackout(e.time?parseInt(e.time):void 0),"no-blackout":e=>{e.brightness&&this.isFully&&window.fully.setScreenBrightness(e.brightness),this.no_blackout()},"call-service":e=>this.call_service(e),commands:async e=>{for(const t of e.commands)await this.msg_callback(t)},delay:async e=>await new Promise((t=>{window.setTimeout(t,1e3*e.seconds)}))};await t[e.command.replace("_","-")](e)}debug(e){w("deviceID",{type:"markdown",content:`# ${s}`}),alert(s)}set_theme(e){e.theme||(e.theme="default"),u("settheme",{theme:e.theme},document.querySelector("home-assistant"))}lovelace_reload(e){const t=l();t&&u("config-refresh",{},t)}call_service(e){const t=e=>{if("string"==typeof e&&"this"===e)return s;if(Array.isArray(e))return e.map(t);if(e.constructor==Object)for(const s in e)e[s]=t(e[s]);return e},[o,i]=e.service.split(".",2);let a=t(JSON.parse(JSON.stringify(e.service_data)));this._hass.callService(o,i,a)}update(e=null){e&&(e.name&&(this.entity_id=e.name.toLowerCase()),e.camera&&!this.isFully&&this.setup_camera(),this.config={...this.config,...e}),this.player_update(),this.fully_update(),this.screen_update(),this.sensor_update()}}const D=[customElements.whenDefined("home-assistant"),customElements.whenDefined("hc-main")];Promise.race(D).then((()=>{window.setTimeout((()=>{window.browser_mod=window.browser_mod||new C}),1e3)}));
