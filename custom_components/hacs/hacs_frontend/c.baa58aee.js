import{_ as i,H as t,e,p as s,n as o}from"./main-ff32767d.js";import"./c.8234372d.js";import"./c.dc9789c3.js";import"./c.9f27b448.js";import"./c.0a038163.js";let c=i([o("hacs-progress-dialog")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[e()],key:"title",value:void 0},{kind:"field",decorators:[e()],key:"content",value:void 0},{kind:"field",decorators:[e()],key:"confirmText",value:void 0},{kind:"field",decorators:[e()],key:"confirm",value:void 0},{kind:"field",decorators:[e({type:Boolean})],key:"_inProgress",value:()=>!1},{kind:"method",key:"shouldUpdate",value:function(i){return i.has("active")||i.has("title")||i.has("content")||i.has("confirmText")||i.has("confirm")||i.has("_inProgress")}},{kind:"method",key:"render",value:function(){return this.active?s`
      <hacs-dialog .active=${this.active} .hass=${this.hass} title=${this.title||""}>
        <div class="content">
          ${this.content||""}
        </div>
        <mwc-button slot="secondaryaction" ?disabled=${this._inProgress} @click=${this._close}>
          ${this.hacs.localize("common.cancel")}
        </mwc-button>
        <mwc-button slot="primaryaction" @click=${this._confirmed}>
          ${this._inProgress?s`<ha-circular-progress active size="small"></ha-circular-progress>`:this.confirmText||this.hacs.localize("common.yes")}</mwc-button
          >
        </mwc-button>
      </hacs-dialog>
    `:s``}},{kind:"method",key:"_confirmed",value:async function(){this._inProgress=!0,await this.confirm(),this._inProgress=!1,this._close()}},{kind:"method",key:"_close",value:function(){this.active=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0}))}}]}}),t);export{c as HacsProgressDialog};
