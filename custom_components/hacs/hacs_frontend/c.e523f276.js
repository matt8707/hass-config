import{_ as s,H as t,e as o,t as i,m as e,aj as a,$ as r,p as l,ak as h,al as n,am as c,an as d,ai as p,d as _,r as y,n as m}from"./main-8113c4f2.js";import{a as u}from"./c.0a038163.js";import"./c.603d0a37.js";import"./c.698066d1.js";import{s as v}from"./c.220355a5.js";import{u as g}from"./c.6596fdfc.js";import"./c.51469fb0.js";import"./c.868d2b7c.js";import"./c.503c02b0.js";import"./c.9f27b448.js";import"./c.49d907c6.js";import"./c.e709cbfb.js";import"./c.936b9278.js";import"./c.4aad54ff.js";import"./c.33d2c1b4.js";import"./c.58dcfe74.js";import"./c.30bdb826.js";let b=s([m("hacs-install-dialog")],(function(s,t){return{F:class extends t{constructor(...t){super(...t),s(this)}},d:[{kind:"field",decorators:[o()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"_toggle",value:()=>!0},{kind:"field",decorators:[i()],key:"_installing",value:()=>!1},{kind:"field",decorators:[i()],key:"_error",value:void 0},{kind:"field",decorators:[i()],key:"_repository",value:void 0},{kind:"field",decorators:[i()],key:"_downloadRepositoryData",value:()=>({beta:!1,version:""})},{kind:"method",key:"shouldUpdate",value:function(s){return s.forEach((s,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===t&&(this._repository=this._getRepository(this.hacs.repositories,this.repository))}),s.has("sidebarDocked")||s.has("narrow")||s.has("active")||s.has("_toggle")||s.has("_error")||s.has("_repository")||s.has("_downloadRepositoryData")||s.has("_installing")}},{kind:"field",key:"_getRepository",value:()=>e((s,t)=>null==s?void 0:s.find(s=>s.id===t))},{kind:"field",key:"_getInstallPath",value:()=>e(s=>{let t=s.local_path;return"theme"===s.category&&(t=`${t}/${s.file_name}`),t})},{kind:"method",key:"firstUpdated",value:async function(){var s,t;if(this._repository=this._getRepository(this.hacs.repositories,this.repository),null===(s=this._repository)||void 0===s||!s.updated_info){await a(this.hass,this._repository.id);const s=await r(this.hass);this.dispatchEvent(new CustomEvent("update-hacs",{detail:{repositories:s},bubbles:!0,composed:!0})),this._repository=this._getRepository(s,this.repository)}this._toggle=!1,this.hass.connection.subscribeEvents(s=>this._error=s.data,"hacs/error"),this._downloadRepositoryData.beta=this._repository.beta,this._downloadRepositoryData.version="version"===(null===(t=this._repository)||void 0===t?void 0:t.version_or_commit)?this._repository.releases[0]:""}},{kind:"method",key:"render",value:function(){var s;if(!this.active||!this._repository)return l``;const t=this._getInstallPath(this._repository),o=[{type:"boolean",name:"beta"},{type:"select",name:"version",optional:!0,options:"version"===this._repository.version_or_commit?this._repository.releases.map(s=>[s,s]).concat("hacs/integration"===this._repository.full_name||this._repository.hide_default_branch?[]:[[this._repository.default_branch,this._repository.default_branch]]):[]}];return l`
      <hacs-dialog
        .active=${this.active}
        .narrow=${this.narrow}
        .hass=${this.hass}
        .secondary=${this.secondary}
        .title=${this._repository.name}
      >
        <div class="content">
          ${"version"===this._repository.version_or_commit?l`
                <ha-form
                  .disabled=${this._toggle}
                  ?narrow=${this.narrow}
                  .data=${this._downloadRepositoryData}
                  .schema=${o}
                  .computeLabel=${s=>"beta"===s.name?this.hacs.localize("dialog_install.show_beta"):this.hacs.localize("dialog_install.select_version")}
                  @value-changed=${this._valueChanged}
                >
                </ha-form>
              `:""}
          ${this._repository.can_install?"":l`<ha-alert alert-type="error" .rtl=${u(this.hass)}>
                ${this.hacs.localize("confirm.home_assistant_version_not_correct",{haversion:this.hass.config.version,minversion:this._repository.homeassistant})}
              </ha-alert>`}
          <div class="note">
            ${this.hacs.localize("repository.note_installed")}
            <code>'${t}'</code>
            ${"plugin"===this._repository.category&&"storage"!==this.hacs.status.lovelace_mode?l`
                  <p>${this.hacs.localize("repository.lovelace_instruction")}</p>
                  <pre>
                url: ${h({repository:this._repository,skipTag:!0})}
                type: module
                </pre
                  >
                `:""}
            ${"integration"===this._repository.category?l`<p>${this.hacs.localize("dialog_install.restart")}</p>`:""}
          </div>
          ${null!==(s=this._error)&&void 0!==s&&s.message?l`<ha-alert alert-type="error" .rtl=${u(this.hass)}>
                ${this._error.message}
              </ha-alert>`:""}
        </div>
        <mwc-button
          raised
          slot="primaryaction"
          ?disabled=${!(this._repository.can_install&&!this._toggle&&"version"!==this._repository.version_or_commit)&&!this._downloadRepositoryData.version}
          @click=${this._installRepository}
        >
          ${this._installing?l`<ha-circular-progress active size="small"></ha-circular-progress>`:this.hacs.localize("common.download")}
        </mwc-button>
        <hacs-link slot="secondaryaction" .url="https://github.com/${this._repository.full_name}">
          <mwc-button> ${this.hacs.localize("common.repository")} </mwc-button>
        </hacs-link>
      </hacs-dialog>
    `}},{kind:"method",key:"_valueChanged",value:async function(s){if(this._downloadRepositoryData.beta!==s.detail.value.beta){this._toggle=!0,await n(this.hass,this.repository);const s=await r(this.hass);this.dispatchEvent(new CustomEvent("update-hacs",{detail:{repositories:s},bubbles:!0,composed:!0})),this._repository=this._getRepository(s,this.repository),this._toggle=!1}this._downloadRepositoryData=s.detail.value}},{kind:"method",key:"_installRepository",value:async function(){var s;if(this._installing=!0,!this._repository)return;const t=this._downloadRepositoryData.version||this._repository.available_version||this._repository.default_branch;"commit"!==(null===(s=this._repository)||void 0===s?void 0:s.version_or_commit)?await c(this.hass,this._repository.id,t):await d(this.hass,this._repository.id),this.hacs.log.debug(this._repository.category,"_installRepository"),this.hacs.log.debug(this.hacs.status.lovelace_mode,"_installRepository"),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&await g(this.hass,this._repository,t),this._installing=!1,this.dispatchEvent(new Event("hacs-secondary-dialog-closed",{bubbles:!0,composed:!0})),this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&v(this,{title:this.hacs.localize("common.reload"),text:l`${this.hacs.localize("dialog.reload.description")}</br>${this.hacs.localize("dialog.reload.confirm")}`,dismissText:this.hacs.localize("common.cancel"),confirmText:this.hacs.localize("common.reload"),confirm:()=>{p.location.href=p.location.href}})}},{kind:"get",static:!0,key:"styles",value:function(){return[_,y`
        .note {
          margin-top: 12px;
        }
        .lovelace {
          margin-top: 8px;
        }
        pre {
          white-space: pre-line;
          user-select: all;
        }
      `]}}]}}),t);export{b as HacsInstallDialog};
