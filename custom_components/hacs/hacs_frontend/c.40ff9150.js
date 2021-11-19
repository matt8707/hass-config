import{_ as e,j as a,e as s,i,p as t,au as o,o as n,L as r,r as l,n as d,H as c,m as h,D as p,E as m,av as u,aw as v,am as g,an as y,ai as _,c as f,d as x}from"./main-8113c4f2.js";import{a as b}from"./c.0a038163.js";import"./c.603d0a37.js";import{s as k}from"./c.220355a5.js";import{m as $}from"./c.a935d548.js";import{u as w}from"./c.6596fdfc.js";import"./c.51469fb0.js";import"./c.868d2b7c.js";import"./c.e709cbfb.js";import"./c.9f27b448.js";const z=()=>new Promise(e=>{var a;a=e,requestAnimationFrame(()=>setTimeout(a,0))});e([d("ha-expansion-panel")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[s({type:Boolean,reflect:!0})],key:"expanded",value:()=>!1},{kind:"field",decorators:[s({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"field",decorators:[s()],key:"header",value:void 0},{kind:"field",decorators:[s()],key:"secondary",value:void 0},{kind:"field",decorators:[i(".container")],key:"_container",value:void 0},{kind:"method",key:"render",value:function(){return t`
      <div class="summary" @click=${this._toggleContainer}>
        <slot class="header" name="header">
          ${this.header}
          <slot class="secondary" name="secondary">${this.secondary}</slot>
        </slot>
        <ha-svg-icon
          .path=${o}
          class="summary-icon ${n({expanded:this.expanded})}"
        ></ha-svg-icon>
      </div>
      <div
        class="container ${n({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
      >
        <slot></slot>
      </div>
    `}},{kind:"method",key:"_handleTransitionEnd",value:function(){this._container.style.removeProperty("height")}},{kind:"method",key:"_toggleContainer",value:async function(){const e=!this.expanded;r(this,"expanded-will-change",{expanded:e}),e&&await z();const a=this._container.scrollHeight;this._container.style.height=a+"px",e||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=e,r(this,"expanded-changed",{expanded:this.expanded})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: 1px;
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        border-radius: var(--ha-card-border-radius, 4px);
        padding: 0 8px;
      }

      .summary {
        display: flex;
        padding: var(--expansion-panel-summary-padding, 0);
        min-height: 48px;
        align-items: center;
        cursor: pointer;
        overflow: hidden;
        font-weight: 500;
      }

      .summary-icon {
        transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
        margin-left: auto;
      }

      .summary-icon.expanded {
        transform: rotate(180deg);
      }

      .container {
        overflow: hidden;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
        height: 0px;
      }

      .container.expanded {
        height: auto;
      }

      .header {
        display: block;
      }

      .secondary {
        display: block;
        color: var(--secondary-text-color);
        font-size: 12px;
      }
    `}}]}}),a);let j=e([d("hacs-update-dialog")],(function(e,a){class i extends a{constructor(...a){super(...a),e(this)}}return{F:i,d:[{kind:"field",decorators:[s()],key:"repository",value:void 0},{kind:"field",decorators:[s({type:Boolean})],key:"_updating",value:()=>!1},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"_releaseNotes",value:()=>[]},{kind:"field",key:"_getRepository",value:()=>h((e,a)=>e.find(e=>e.id===a))},{kind:"method",key:"firstUpdated",value:async function(e){p(m(i.prototype),"firstUpdated",this).call(this,e);const a=this._getRepository(this.hacs.repositories,this.repository);a&&("commit"!==a.version_or_commit&&(this._releaseNotes=await u(this.hass,a.id),this._releaseNotes=this._releaseNotes.filter(e=>e.tag>a.installed_version)),this.hass.connection.subscribeEvents(e=>this._error=e.data,"hacs/error"))}},{kind:"method",key:"render",value:function(){var e;if(!this.active)return t``;const a=this._getRepository(this.hacs.repositories,this.repository);return a?t`
      <hacs-dialog
        .active=${this.active}
        .title=${this.hacs.localize("dialog_update.title")}
        .hass=${this.hass}
      >
        <div class=${n({content:!0,narrow:this.narrow})}>
          <p class="message">
            ${this.hacs.localize("dialog_update.message",{name:a.name})}
          </p>
          <div class="version-container">
            <div class="version-element">
              <span class="version-number">${a.installed_version}</span>
              <small class="version-text">${this.hacs.localize("dialog_update.installed_version")}</small>
            </div>

            <span class="version-separator">
              <ha-svg-icon
                .path=${v}
              ></ha-svg-icon>
            </span>

            <div class="version-element">
                <span class="version-number">${a.available_version}</span>
                <small class="version-text">${this.hacs.localize("dialog_update.available_version")}</small>
              </div>
            </div>
          </div>

          ${this._releaseNotes.length>0?this._releaseNotes.map(e=>t`
                    <ha-expansion-panel
                      .header=${e.name&&e.name!==e.tag?`${e.tag}: ${e.name}`:e.tag}
                      outlined
                      ?expanded=${1===this._releaseNotes.length}
                    >
                      ${e.body?$.html(e.body,a):this.hacs.localize("dialog_update.no_info")}
                    </ha-expansion-panel>
                  `):""}
          ${a.can_install?"":t`<ha-alert alert-type="error" .rtl=${b(this.hass)}>
                  ${this.hacs.localize("confirm.home_assistant_version_not_correct",{haversion:this.hass.config.version,minversion:a.homeassistant})}
                </ha-alert>`}
          ${"integration"===a.category?t`<p>${this.hacs.localize("dialog_install.restart")}</p>`:""}
          ${null!==(e=this._error)&&void 0!==e&&e.message?t`<ha-alert alert-type="error" .rtl=${b(this.hass)}>
                  ${this._error.message}
                </ha-alert>`:""}
        </div>
        <mwc-button
          slot="primaryaction"
          ?disabled=${!a.can_install}
          @click=${this._updateRepository}
          raised
          >
          ${this._updating?t`<ha-circular-progress active size="small"></ha-circular-progress>`:this.hacs.localize("common.update")}
          </mwc-button
        >
        <div class="secondary" slot="secondaryaction">
          <hacs-link .url=${this._getChanglogURL()||""}>
            <mwc-button>${this.hacs.localize("dialog_update.changelog")}
          </mwc-button>
          </hacs-link>
          <hacs-link .url="https://github.com/${a.full_name}">
            <mwc-button>${this.hacs.localize("common.repository")}
          </mwc-button>
          </hacs-link>
        </div>
      </hacs-dialog>
    `:t``}},{kind:"method",key:"_updateRepository",value:async function(){this._updating=!0;const e=this._getRepository(this.hacs.repositories,this.repository);e&&("commit"!==e.version_or_commit?await g(this.hass,e.id,e.available_version):await y(this.hass,e.id),"plugin"===e.category&&"storage"===this.hacs.status.lovelace_mode&&await w(this.hass,e,e.available_version),this._updating=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===e.category&&k(this,{title:this.hacs.localize("common.reload"),text:t`${this.hacs.localize("dialog.reload.description")}</br>${this.hacs.localize("dialog.reload.confirm")}`,dismissText:this.hacs.localize("common.cancel"),confirmText:this.hacs.localize("common.reload"),confirm:()=>{_.location.href=_.location.href}}))}},{kind:"method",key:"_getChanglogURL",value:function(){const e=this._getRepository(this.hacs.repositories,this.repository);if(e)return"commit"===e.version_or_commit?`https://github.com/${e.full_name}/compare/${e.installed_version}...${e.available_version}`:`https://github.com/${e.full_name}/releases`}},{kind:"get",static:!0,key:"styles",value:function(){return[f,x,l`
        .content {
          width: 360px;
          display: contents;
        }
        ha-expansion-panel {
          margin: 8px 0;
        }
        ha-expansion-panel[expanded] {
          padding-bottom: 16px;
        }

        .secondary {
          display: flex;
        }
        .message {
          text-align: center;
          margin: 0;
        }
        .version-container {
          margin: 24px 0 12px 0;
          width: 360px;
          min-width: 100%;
          max-width: 100%;
          display: flex;
          flex-direction: row;
        }
        .version-element {
          display: flex;
          flex-direction: column;
          flex: 1;
          padding: 0 12px;
          text-align: center;
        }
        .version-text {
          color: var(--secondary-text-color);
        }
        .version-number {
          font-size: 1.5rem;
          margin-bottom: 4px;
        }
      `]}}]}}),c);export{j as HacsUpdateDialog};
