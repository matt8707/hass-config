import{_ as o,j as e,e as t,r,p as a,n}from"./main-ff32767d.js";import{m as i}from"./c.b90fecee.js";import{a as s}from"./c.8ada3ef5.js";const d=(o,e)=>o&&o.config.components.includes(e);o([n("ha-card")],(function(o,e){return{F:class extends e{constructor(...e){super(...e),o(this)}},d:[{kind:"field",decorators:[t()],key:"header",value:void 0},{kind:"field",decorators:[t({type:Boolean,reflect:!0})],key:"outlined",value:()=>!1},{kind:"get",static:!0,key:"styles",value:function(){return r`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 4px);
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([outlined]) {
        box-shadow: none;
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return a`
      ${this.header?a`<h1 class="card-header">${this.header}</h1>`:a``}
      <slot></slot>
    `}}]}}),e);const c=async(o,e)=>s(o,{title:"Home Assistant Community Store",confirmText:e.localize("common.close"),text:i.html(`\n  **${e.localize("dialog_about.integration_version")}:** | ${e.configuration.version}\n  --|--\n  **${e.localize("dialog_about.frontend_version")}:** | 20211128181314\n  **${e.localize("common.repositories")}:** | ${e.repositories.length}\n  **${e.localize("dialog_about.downloaded_repositories")}:** | ${e.repositories.filter(o=>o.installed).length}\n\n  **${e.localize("dialog_about.useful_links")}:**\n\n  - [General documentation](https://hacs.xyz/)\n  - [Configuration](https://hacs.xyz/docs/configuration/start)\n  - [FAQ](https://hacs.xyz/docs/faq/what)\n  - [GitHub](https://github.com/hacs)\n  - [Discord](https://discord.gg/apgchf8)\n  - [Become a GitHub sponsor? ❤️](https://github.com/sponsors/ludeeus)\n  - [BuyMe~~Coffee~~Beer? 🍺🙈](https://buymeacoffee.com/ludeeus)\n\n  ***\n\n  _Everything you find in HACS is **not** tested by Home Assistant, that includes HACS itself.\n  The HACS and Home Assistant teams do not support **anything** you find here._`)});export{d as i,c as s};
