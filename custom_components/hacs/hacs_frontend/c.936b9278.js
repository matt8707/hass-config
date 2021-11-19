import{_ as e,j as t,e as i,i as a,p as l,r as o,n,P as s,Q as d}from"./main-8113c4f2.js";import"./c.503c02b0.js";import{P as r}from"./c.4aad54ff.js";e([n("ha-button-menu")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"corner",value:()=>"TOP_START"},{kind:"field",decorators:[i({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[a("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"render",value:function(){return l`
      <div @click=${this._handleClick}>
        <slot name="trigger"></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),t),s({_template:d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[r]});
