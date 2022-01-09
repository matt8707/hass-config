import{_ as s,H as t,e as o,t as i,m as e,aj as a,$ as r,p as l,ak as h,al as n,am as c,an as d,ao as p,ai as _,d as y,r as m,n as u}from"./main-25487c89.js";import{a as v}from"./c.0a038163.js";import"./c.a816d055.js";import"./c.149d05db.js";import{s as g}from"./c.bd24fdea.js";import{u as b}from"./c.2fca0a2d.js";import"./c.988357e4.js";import"./c.7a168374.js";import"./c.1122ce3c.js";import"./c.9f27b448.js";import"./c.cac1db56.js";import"./c.619fb63b.js";import"./c.a0a505ec.js";import"./c.27392995.js";import"./c.e4c27bcc.js";import"./c.d0e4127a.js";import"./c.a06a99f1.js";let f=s([u("hacs-download-dialog")],(function(s,t){return{F:class extends t{constructor(...t){super(...t),s(this)}},d:[{kind:"field",decorators:[o()],key:"repository",value:void 0},{kind:"field",decorators:[i()],key:"_toggle",value:()=>!0},{kind:"field",decorators:[i()],key:"_installing",value:()=>!1},{kind:"field",decorators:[i()],key:"_error",value:void 0},{kind:"field",decorators:[i()],key:"_repository",value:void 0},{kind:"field",decorators:[i()],key:"_downloadRepositoryData",value:()=>({beta:!1,version:""})},{kind:"method",key:"shouldUpdate",value:function(s){return s.forEach((s,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar")),"repositories"===t&&(this._repository=this._getRepository(this.hacs.repositories,this.repository))}),s.has("sidebarDocked")||s.has("narrow")||s.has("active")||s.has("_toggle")||s.has("_error")||s.has("_repository")||s.has("_downloadRepositoryData")||s.has("_installing")}},{kind:"field",key:"_getRepository",value:()=>e((s,t)=>null==s?void 0:s.find(s=>s.id===t))},{kind:"field",key:"_getInstallPath",value:()=>e(s=>{let t=s.local_path;return"theme"===s.category&&(t=`${t}/${s.file_name}`),t})},{kind:"method",key:"firstUpdated",value:async function(){var s,t;if(this._repository=this._getRepository(this.hacs.repositories,this.repository),null===(s=this._repository)||void 0===s||!s.updated_info){await a(this.hass,this._repository.id);const s=await r(this.hass);this.dispatchEvent(new CustomEvent("update-hacs",{detail:{repositories:s},bubbles:!0,composed:!0})),this._repository=this._getRepository(s,this.repository)}this._toggle=!1,this.hass.connection.subscribeEvents(s=>this._error=s.data,"hacs/error"),this._downloadRepositoryData.beta=this._repository.beta,this._downloadRepositoryData.version="version"===(null===(t=this._repository)||void 0===t?void 0:t.version_or_commit)?this._repository.releases[0]:""}},{kind:"method",key:"render",value:function(){var s;if(!this.active||!this._repository)return l``;const t=this._getInstallPath(this._repository),o=[{type:"boolean",name:"beta"},{type:"select",name:"version",optional:!0,options:"version"===this._repository.version_or_commit?this._repository.releases.map(s=>[s,s]).concat("hacs/integration"===this._repository.full_name||this._repository.hide_default_branch?[]:[[this._repository.default_branch,this._repository.default_branch]]):[]}];return l`
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
                  .computeLabel=${s=>"beta"===s.name?this.hacs.localize("dialog_download.show_beta"):this.hacs.localize("dialog_download.select_version")}
                  @value-changed=${this._valueChanged}
                >
                </ha-form>
              `:""}
          ${this._repository.can_install?"":l`<ha-alert alert-type="error" .rtl=${v(this.hass)}>
                ${this.hacs.localize("confirm.home_assistant_version_not_correct",{haversion:this.hass.config.version,minversion:this._repository.homeassistant})}
              </ha-alert>`}
          <div class="note">
            ${this.hacs.localize("repository.note_downloaded")}
            <code>'${t}'</code>
            ${"plugin"===this._repository.category&&"storage"!==this.hacs.status.lovelace_mode?l`
                  <p>${this.hacs.localize("repository.lovelace_instruction")}</p>
                  <pre>
                url: ${h({repository:this._repository,skipTag:!0})}
                type: module
                </pre
                  >
                `:""}
            ${"integration"===this._repository.category?l`<p>${this.hacs.localize("dialog_download.restart")}</p>`:""}
          </div>
          ${null!==(s=this._error)&&void 0!==s&&s.message?l`<ha-alert alert-type="error" .rtl=${v(this.hass)}>
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
    `}},{kind:"method",key:"_valueChanged",value:async function(s){let t=!1;if(this._downloadRepositoryData.beta!==s.detail.value.beta&&(t=!0,this._toggle=!0,await n(this.hass,this.repository)),s.detail.value.version&&(t=!0,this._toggle=!0,await c(this.hass,this.repository,s.detail.value.version)),t){const s=await r(this.hass);this.dispatchEvent(new CustomEvent("update-hacs",{detail:{repositories:s},bubbles:!0,composed:!0})),this._repository=this._getRepository(s,this.repository),this._toggle=!1}this._downloadRepositoryData=s.detail.value}},{kind:"method",key:"_installRepository",value:async function(){var s;if(this._installing=!0,!this._repository)return;const t=this._downloadRepositoryData.version||this._repository.available_version||this._repository.default_branch;"commit"!==(null===(s=this._repository)||void 0===s?void 0:s.version_or_commit)?await d(this.hass,this._repository.id,t):await p(this.hass,this._repository.id),this.hacs.log.debug(this._repository.category,"_installRepository"),this.hacs.log.debug(this.hacs.status.lovelace_mode,"_installRepository"),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&await b(this.hass,this._repository,t),this._installing=!1,this.dispatchEvent(new Event("hacs-secondary-dialog-closed",{bubbles:!0,composed:!0})),this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0})),"plugin"===this._repository.category&&"storage"===this.hacs.status.lovelace_mode&&g(this,{title:this.hacs.localize("common.reload"),text:l`${this.hacs.localize("dialog.reload.description")}</br>${this.hacs.localize("dialog.reload.confirm")}`,dismissText:this.hacs.localize("common.cancel"),confirmText:this.hacs.localize("common.reload"),confirm:()=>{_.location.href=_.location.href}})}},{kind:"get",static:!0,key:"styles",value:function(){return[y,m`
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
      `]}}]}}),t);export{f as HacsDonwloadDialog};
