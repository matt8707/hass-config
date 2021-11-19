import{_ as e,j as t,e as i,p as o,o as s,K as r,L as n,r as c,n as a,a1 as l,a2 as d,a3 as u,a4 as p}from"./main-8113c4f2.js";const v={info:l,warning:d,error:u,success:p};e([a("ha-alert")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"title",value:()=>""},{kind:"field",decorators:[i({attribute:"alert-type"})],key:"alertType",value:()=>"info"},{kind:"field",decorators:[i({attribute:"action-text"})],key:"actionText",value:()=>""},{kind:"field",decorators:[i({type:Boolean})],key:"dismissable",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"rtl",value:()=>!1},{kind:"method",key:"render",value:function(){return o`
      <div
        class="issue-type ${s({rtl:this.rtl,[this.alertType]:!0})}"
      >
        <div class="icon ${this.title?"":"no-title"}">
          <ha-svg-icon .path=${v[this.alertType]}></ha-svg-icon>
        </div>
        <div class="content">
          <div class="main-content">
            ${this.title?o`<div class="title">${this.title}</div>`:""}
            <slot></slot>
          </div>
          <div class="action">
            ${this.actionText?o`<mwc-button
                  @click=${this._action_clicked}
                  .label=${this.actionText}
                ></mwc-button>`:this.dismissable?o`<ha-icon-button
                  @click=${this._dismiss_clicked}
                  label="Dismiss alert"
                  .path=${r}
                ></ha-icon-button>`:""}
          </div>
        </div>
      </div>
    `}},{kind:"method",key:"_dismiss_clicked",value:function(){n(this,"alert-dismissed-clicked")}},{kind:"method",key:"_action_clicked",value:function(){n(this,"alert-action-clicked")}},{kind:"field",static:!0,key:"styles",value:()=>c`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
      margin: 4px 0;
    }
    .issue-type.rtl {
      flex-direction: row-reverse;
    }
    .issue-type::before {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      margin-right: 8px;
      width: 24px;
    }
    .icon.no-title {
      align-self: center;
    }
    .issue-type.rtl > .icon {
      margin-right: 0px;
      margin-left: 8px;
      width: 24px;
    }
    .issue-type.rtl > .content {
      flex-direction: row-reverse;
      text-align: right;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
    }
    .main-content {
      overflow-wrap: anywhere;
    }
    .title {
      margin-top: 2px;
      font-weight: bold;
    }
    mwc-button {
      --mdc-theme-primary: var(--primary-text-color);
    }
    ha-icon-button {
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--info-color);
    }
    .issue-type.info::before {
      background-color: var(--info-color);
    }

    .issue-type.warning > .icon {
      color: var(--warning-color);
    }
    .issue-type.warning::before {
      background-color: var(--warning-color);
    }

    .issue-type.error > .icon {
      color: var(--error-color);
    }
    .issue-type.error::before {
      background-color: var(--error-color);
    }

    .issue-type.success > .icon {
      color: var(--success-color);
    }
    .issue-type.success::before {
      background-color: var(--success-color);
    }
  `}]}}),t);
