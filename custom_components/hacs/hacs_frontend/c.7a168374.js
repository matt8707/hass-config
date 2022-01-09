import{_ as e,H as i,e as t,p as o,O as s,d as a,r as c,n}from"./main-25487c89.js";import{c as l}from"./c.619fb63b.js";e([n("hacs-dialog")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({type:Boolean})],key:"hideActions",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"scrimClickAction",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"escapeKeyAction",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"noClose",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"maxWidth",value:()=>!1},{kind:"field",decorators:[t()],key:"title",value:void 0},{kind:"method",key:"render",value:function(){return this.active?o`<ha-dialog
      ?maxWidth=${this.maxWidth}
      ?open=${this.active}
      ?scrimClickAction=${this.scrimClickAction}
      ?escapeKeyAction=${this.escapeKeyAction}
      @closed=${this.closeDialog}
      ?hideActions=${this.hideActions}
      .heading=${this.noClose?this.title:l(this.hass,this.title)}
    >
      <slot></slot>
      <slot class="primary" name="primaryaction" slot="primaryAction"></slot>
      <slot class="secondary" name="secondaryaction" slot="secondaryAction"></slot>
    </ha-dialog>`:o``}},{kind:"method",key:"closeDialog",value:function(){this.active=!1,this.dispatchEvent(new CustomEvent("closed",{bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[s,a,c`
        ha-dialog[maxWidth] {
          --mdc-dialog-max-width: calc(100vw - 32px);
        }
      `]}}]}}),i);
