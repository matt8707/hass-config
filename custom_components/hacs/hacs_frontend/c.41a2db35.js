import{v as t,w as e,M as i,g as s,e as c,A as a,i as o,h as r,t as d,C as n,B as l,R as h,z as p,p as m,l as u,r as b,n as _,L as v,_ as k,D as f,E as w,j as g,o as y,O as x}from"./main-ff32767d.js";import"./c.ddf0aa65.js";import"./c.dc9789c3.js";import{o as C}from"./c.9f27b448.js";import"./c.335672c7.js";import"./c.0a038163.js";var R={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},E={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"},$=function(i){function s(t){return i.call(this,e(e({},s.defaultAdapter),t))||this}return t(s,i),Object.defineProperty(s,"strings",{get:function(){return E},enumerable:!1,configurable:!0}),Object.defineProperty(s,"cssClasses",{get:function(){return R},enumerable:!1,configurable:!0}),Object.defineProperty(s,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),s.prototype.setChecked=function(t){this.adapter.setNativeControlChecked(t),this.updateAriaChecked(t),this.updateCheckedStyling(t)},s.prototype.setDisabled=function(t){this.adapter.setNativeControlDisabled(t),t?this.adapter.addClass(R.DISABLED):this.adapter.removeClass(R.DISABLED)},s.prototype.handleChange=function(t){var e=t.target;this.updateAriaChecked(e.checked),this.updateCheckedStyling(e.checked)},s.prototype.updateCheckedStyling=function(t){t?this.adapter.addClass(R.CHECKED):this.adapter.removeClass(R.CHECKED)},s.prototype.updateAriaChecked=function(t){this.adapter.setNativeControlAttr(E.ARIA_CHECKED_ATTR,""+!!t)},s}(i);class A extends l{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=$,this.rippleHandlers=new h(()=>(this.shouldRenderRipple=!0,this.ripple))}changeHandler(t){this.mdcFoundation.handleChange(t),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},p(this.mdcRoot)),{setNativeControlChecked:t=>{this.formElement.checked=t},setNativeControlDisabled:t=>{this.formElement.disabled=t},setNativeControlAttr:(t,e)=>{this.formElement.setAttribute(t,e)}})}renderRipple(){return this.shouldRenderRipple?m`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const t=this.formElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.formElement;t&&(this.rippleHandlers.endFocus(),t.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",t=>{this.dispatchEvent(new Event("change",t))})}render(){return m`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${u(this.ariaLabel)}"
              aria-labelledby="${u(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}s([c({type:Boolean}),C((function(t){this.mdcFoundation.setChecked(t)}))],A.prototype,"checked",void 0),s([c({type:Boolean}),C((function(t){this.mdcFoundation.setDisabled(t)}))],A.prototype,"disabled",void 0),s([a,c({attribute:"aria-label"})],A.prototype,"ariaLabel",void 0),s([a,c({attribute:"aria-labelledby"})],A.prototype,"ariaLabelledBy",void 0),s([o(".mdc-switch")],A.prototype,"mdcRoot",void 0),s([o("input")],A.prototype,"formElement",void 0),s([r("mwc-ripple")],A.prototype,"ripple",void 0),s([d()],A.prototype,"shouldRenderRipple",void 0),s([n({passive:!0})],A.prototype,"handleRippleMouseDown",null),s([n({passive:!0})],A.prototype,"handleRippleTouchStart",null);const D=b`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`;let L=class extends A{};L.styles=[D],L=s([_("mwc-switch")],L);k([_("ha-switch")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[c({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){f(w(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--switch-checked-color)"),this.addEventListener("change",()=>{this.haptic&&v(window,"haptic","light")})}},{kind:"get",static:!0,key:"styles",value:function(){return[L.styles,b`
        .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
          background-color: var(--switch-checked-button-color);
          border-color: var(--switch-checked-button-color);
        }
        .mdc-switch.mdc-switch--checked .mdc-switch__track {
          background-color: var(--switch-checked-track-color);
          border-color: var(--switch-checked-track-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--switch-unchecked-button-color);
          border-color: var(--switch-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--switch-unchecked-track-color);
          border-color: var(--switch-unchecked-track-color);
        }
      `]}}]}}),L),k([_("dialog-box")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[c({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"_params",value:void 0},{kind:"field",decorators:[d()],key:"_value",value:void 0},{kind:"method",key:"showDialog",value:async function(t){this._params=t,t.prompt&&(this._value=t.defaultValue)}},{kind:"method",key:"closeDialog",value:function(){var t,e;return!(null!==(t=this._params)&&void 0!==t&&t.confirmation||null!==(e=this._params)&&void 0!==e&&e.prompt)&&(!this._params||(this._dismiss(),!0))}},{kind:"method",key:"render",value:function(){if(!this._params)return m``;const t=this._params.confirmation||this._params.prompt;return m`
      <ha-dialog
        open
        ?scrimClickAction=${t}
        ?escapeKeyAction=${t}
        @closed=${this._dialogClosed}
        defaultAction="ignore"
        .heading=${this._params.title?this._params.title:this._params.confirmation&&this.hass.localize("ui.dialogs.generic.default_confirmation_title")}
      >
        <div>
          ${this._params.text?m`
                <p
                  class=${y({"no-bottom-padding":Boolean(this._params.prompt),warning:Boolean(this._params.warning)})}
                >
                  ${this._params.text}
                </p>
              `:""}
          ${this._params.prompt?m`
                <paper-input
                  dialogInitialFocus
                  .value=${this._value}
                  @keyup=${this._handleKeyUp}
                  @value-changed=${this._valueChanged}
                  .label=${this._params.inputLabel?this._params.inputLabel:""}
                  .type=${this._params.inputType?this._params.inputType:"text"}
                ></paper-input>
              `:""}
        </div>
        ${t&&m`
          <mwc-button @click=${this._dismiss} slot="secondaryAction">
            ${this._params.dismissText?this._params.dismissText:this.hass.localize("ui.dialogs.generic.cancel")}
          </mwc-button>
        `}
        <mwc-button
          @click=${this._confirm}
          ?dialogInitialFocus=${!this._params.prompt}
          slot="primaryAction"
        >
          ${this._params.confirmText?this._params.confirmText:this.hass.localize("ui.dialogs.generic.ok")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_valueChanged",value:function(t){this._value=t.detail.value}},{kind:"method",key:"_dismiss",value:function(){var t;null!==(t=this._params)&&void 0!==t&&t.cancel&&this._params.cancel(),this._close()}},{kind:"method",key:"_handleKeyUp",value:function(t){13===t.keyCode&&this._confirm()}},{kind:"method",key:"_confirm",value:function(){this._params.confirm&&this._params.confirm(this._value),this._close()}},{kind:"method",key:"_dialogClosed",value:function(t){"ignore"!==t.detail.action&&this._dismiss()}},{kind:"method",key:"_close",value:function(){this._params&&(this._params=void 0,v(this,"dialog-closed",{dialog:this.localName}))}},{kind:"get",static:!0,key:"styles",value:function(){return[x,b`
        :host([inert]) {
          pointer-events: initial !important;
          cursor: initial !important;
        }
        a {
          color: var(--primary-color);
        }
        p {
          margin: 0;
          padding-top: 6px;
          padding-bottom: 24px;
          color: var(--primary-text-color);
        }
        .no-bottom-padding {
          padding-bottom: 0;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        ha-dialog {
          /* Place above other dialogs */
          --dialog-z-index: 104;
        }
        .warning {
          color: var(--warning-color);
        }
      `]}}]}}),g);
