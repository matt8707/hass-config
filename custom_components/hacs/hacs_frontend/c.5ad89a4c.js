import{_ as e,j as t,e as i,i as n,p as o,J as a,K as l,L as r,r as s,n as d,m as c,d as u}from"./main-ff32767d.js";import"./c.ddf0aa65.js";import{b as h}from"./c.5eb5124b.js";e([d("search-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"filter",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,attribute:"no-underline"})],key:"noUnderline",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[i({type:String})],key:"label",value:void 0},{kind:"method",key:"focus",value:function(){this.shadowRoot.querySelector("paper-input").focus()}},{kind:"field",decorators:[n("paper-input",!0)],key:"_input",value:void 0},{kind:"method",key:"render",value:function(){return o`
      <paper-input
        .autofocus=${this.autofocus}
        .label=${this.label||"Search"}
        .value=${this.filter}
        @value-changed=${this._filterInputChanged}
        .noLabelFloat=${this.noLabelFloat}
      >
        <slot name="prefix" slot="prefix">
          <ha-svg-icon class="prefix" .path=${a}></ha-svg-icon>
        </slot>
        ${this.filter&&o`
          <ha-icon-button
            slot="suffix"
            @click=${this._clearSearch}
            .label=${this.hass.localize("ui.common.clear")}
            .path=${l}
          ></ha-icon-button>
        `}
      </paper-input>
    `}},{kind:"method",key:"updated",value:function(e){e.has("noUnderline")&&(this.noUnderline||void 0!==e.get("noUnderline"))&&(this._input.inputElement.parentElement.shadowRoot.querySelector("div.unfocused-line").style.display=this.noUnderline?"none":"block")}},{kind:"method",key:"_filterChanged",value:async function(e){r(this,"value-changed",{value:String(e)})}},{kind:"method",key:"_filterInputChanged",value:async function(e){this._filterChanged(e.target.value)}},{kind:"method",key:"_clearSearch",value:async function(){this._filterChanged("")}},{kind:"get",static:!0,key:"styles",value:function(){return s`
      ha-svg-icon,
      ha-icon-button {
        color: var(--primary-text-color);
      }
      ha-icon-button {
        --mdc-icon-button-size: 24px;
      }
      ha-svg-icon.prefix {
        margin: 8px;
      }
    `}}]}}),t);const f=c((e,t)=>e.filter(e=>p(e.name).includes(p(t))||p(e.description).includes(p(t))||p(e.category).includes(p(t))||p(e.full_name).includes(p(t))||p(e.authors).includes(p(t))||p(e.domain).includes(p(t)))),p=c(e=>String(e||"").toLocaleLowerCase().replace(/-|_| /g,""));e([d("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"get",static:!0,key:"styles",value:function(){return[h.styles,s`
        :host(:not([alignEnd])) ::slotted(ha-switch) {
          margin-right: 10px;
        }
        :host([dir="rtl"]:not([alignEnd])) ::slotted(ha-switch) {
          margin-left: 10px;
          margin-right: auto;
        }
      `]}}]}}),h),e([d("hacs-filter")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"method",key:"render",value:function(){var e;return o`
      <div class="filter">
        ${null===(e=this.filters)||void 0===e?void 0:e.map(e=>o`
            <ha-formfield
              class="checkbox"
              .label=${this.hacs.localize("common."+e.id)||e.value}
            >
              <ha-checkbox
                .checked=${e.checked||!1}
                .id=${e.id}
                @click=${this._filterClick}
              >
              </ha-checkbox>
            </ha-formfield>
          `)}
      </div>
    `}},{kind:"method",key:"_filterClick",value:function(e){const t=e.currentTarget;this.dispatchEvent(new CustomEvent("filter-change",{detail:{id:t.id},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[u,s`
        .filter {
          display: flex;
          border-bottom: 1px solid var(--divider-color);
          align-items: center;
          font-size: 16px;
          height: 32px;
          line-height: 4px;
          background-color: var(--sidebar-background-color);
          padding: 0 16px;
          box-sizing: border-box;
        }

        .checkbox:not(:first-child) {
          margin-left: 20px;
        }
      `]}}]}}),t);export{f};
