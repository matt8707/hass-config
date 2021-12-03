import{g as t,h as e,e as i,t as a,C as o,j as s,R as n,p as r,o as d,r as l,n as c,_ as p,D as h,E as m,P as u,Q as f,S as b,aN as x,l as g,m as v,aL as y,b as w,aO as _,aP as k,aQ as $,a3 as z,aR as R,K as T,aj as C,aS as E,ah as F,ap as S,ak as L,as as A,at as I,d as j,a as P,aT as B,aU as M,aV as O,aW as D,aX as H,s as N,c as U}from"./main-ff32767d.js";import{f as V}from"./c.5ad89a4c.js";import{a as Y}from"./c.0a038163.js";import"./c.6c82c461.js";import{i as K,s as q}from"./c.90d2c145.js";import"./c.a390ecd0.js";import"./c.5eb5124b.js";import"./c.453f783f.js";import"./c.6e967352.js";import{s as W}from"./c.8ada3ef5.js";import"./c.e86c9db8.js";import"./c.ddf0aa65.js";import"./c.335672c7.js";import"./c.b90fecee.js";import"./c.72739fe6.js";import"./c.9f27b448.js";class G extends s{constructor(){super(...arguments),this.mini=!1,this.exited=!1,this.disabled=!1,this.extended=!1,this.showIconAtEnd=!1,this.reducedTouchTarget=!1,this.icon="",this.label="",this.shouldRenderRipple=!1,this.useStateLayerCustomProperties=!1,this.rippleHandlers=new n(()=>(this.shouldRenderRipple=!0,this.ripple))}render(){const t=this.mini&&!this.reducedTouchTarget,e={"mdc-fab--mini":this.mini,"mdc-fab--touch":t,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended,"icon-end":this.showIconAtEnd},i=this.label?this.label:this.icon;return r`<button
          class="mdc-fab ${d(e)}"
          ?disabled="${this.disabled}"
          aria-label="${i}"
          @mouseenter=${this.handleRippleMouseEnter}
          @mouseleave=${this.handleRippleMouseLeave}
          @focus=${this.handleRippleFocus}
          @blur=${this.handleRippleBlur}
          @mousedown=${this.handleRippleActivate}
          @touchstart=${this.handleRippleStartPress}
          @touchend=${this.handleRippleDeactivate}
          @touchcancel=${this.handleRippleDeactivate}><!--
        -->${this.renderBeforeRipple()}<!--
        -->${this.renderRipple()}<!--
        -->${this.showIconAtEnd?this.renderLabel():""}<!--
        --><span class="material-icons mdc-fab__icon"><!--
          --><slot name="icon">${this.icon}</slot><!--
       --></span><!--
        -->${this.showIconAtEnd?"":this.renderLabel()}<!--
        -->${this.renderTouchTarget()}<!--
      --></button>`}renderIcon(){return r``}renderTouchTarget(){const t=this.mini&&!this.reducedTouchTarget;return r`${t?r`<div class="mdc-fab__touch"></div>`:""}`}renderLabel(){const t=""!==this.label&&this.extended;return r`${t?r`<span class="mdc-fab__label">${this.label}</span>`:""}`}renderBeforeRipple(){return r``}renderRipple(){return this.shouldRenderRipple?r`<mwc-ripple class="ripple"
        .internalUseStateLayerCustomProperties="${this.useStateLayerCustomProperties}"
         ></mwc-ripple>`:""}handleRippleActivate(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.handleRippleStartPress(t)}handleRippleStartPress(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}G.shadowRootOptions={mode:"open",delegatesFocus:!0},t([e("mwc-ripple")],G.prototype,"ripple",void 0),t([i({type:Boolean})],G.prototype,"mini",void 0),t([i({type:Boolean})],G.prototype,"exited",void 0),t([i({type:Boolean})],G.prototype,"disabled",void 0),t([i({type:Boolean})],G.prototype,"extended",void 0),t([i({type:Boolean})],G.prototype,"showIconAtEnd",void 0),t([i({type:Boolean})],G.prototype,"reducedTouchTarget",void 0),t([i()],G.prototype,"icon",void 0),t([i()],G.prototype,"label",void 0),t([a()],G.prototype,"shouldRenderRipple",void 0),t([a()],G.prototype,"useStateLayerCustomProperties",void 0),t([o({passive:!0})],G.prototype,"handleRippleStartPress",null);const Q=l`:host .mdc-fab .material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}:host{outline:none;--mdc-ripple-color: currentcolor;user-select:none;-webkit-tap-highlight-color:transparent;display:inline-flex;-webkit-tap-highlight-color:transparent;display:inline-flex;outline:none;user-select:none}:host .mdc-touch-target-wrapper{display:inline}:host .mdc-elevation-overlay{position:absolute;border-radius:inherit;pointer-events:none;opacity:0;opacity:var(--mdc-elevation-overlay-opacity, 0);transition:opacity 280ms cubic-bezier(0.4, 0, 0.2, 1);background-color:#fff;background-color:var(--mdc-elevation-overlay-color, #fff)}:host .mdc-fab{position:relative;display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1)}:host .mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}:host .mdc-fab::-moz-focus-inner{padding:0;border:0}:host .mdc-fab:hover{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab.mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(.mdc-ripple-upgraded):focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus{outline:none}:host .mdc-fab:hover{cursor:pointer}:host .mdc-fab>svg{width:100%}:host .mdc-fab--mini{width:40px;height:40px}:host .mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding-left:20px;padding-right:20px;width:auto;max-width:100%;height:48px;line-height:normal}:host .mdc-fab--extended .mdc-fab__ripple{border-radius:24px}:host .mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-right:12px}[dir=rtl] :host .mdc-fab--extended .mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:calc(12px - 20px)}:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:calc(12px - 20px)}[dir=rtl] :host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-right:12px}:host .mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}:host .mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host .mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:"";pointer-events:none}:host .mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}:host .mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}:host .mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2),0px 6px 10px 0px rgba(0, 0, 0, 0.14),0px 1px 18px 0px rgba(0,0,0,.12)}:host .mdc-fab .mdc-fab__icon{width:24px;height:24px;font-size:24px}:host .mdc-fab,:host .mdc-fab:not(:disabled) .mdc-fab__icon,:host .mdc-fab:not(:disabled) .mdc-fab__label,:host .mdc-fab:disabled .mdc-fab__icon,:host .mdc-fab:disabled .mdc-fab__label{color:#fff;color:var(--mdc-theme-on-secondary, #fff)}:host .mdc-fab:not(.mdc-fab--extended){border-radius:50%}:host .mdc-fab:not(.mdc-fab--extended) .mdc-fab__ripple{border-radius:50%}:host .mdc-fab{position:relative;display:inline-flex;position:relative;align-items:center;justify-content:center;box-sizing:border-box;width:56px;height:56px;padding:0;border:none;fill:currentColor;text-decoration:none;cursor:pointer;user-select:none;-moz-appearance:none;-webkit-appearance:none;overflow:visible;transition:box-shadow 280ms cubic-bezier(0.4, 0, 0.2, 1),opacity 15ms linear 30ms,transform 270ms 0ms cubic-bezier(0, 0, 0.2, 1)}:host .mdc-fab .mdc-elevation-overlay{width:100%;height:100%;top:0;left:0}:host .mdc-fab::-moz-focus-inner{padding:0;border:0}:host .mdc-fab:hover{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab.mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(.mdc-ripple-upgraded):focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2),0px 8px 10px 1px rgba(0, 0, 0, 0.14),0px 3px 14px 2px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2),0px 12px 17px 2px rgba(0, 0, 0, 0.14),0px 5px 22px 4px rgba(0,0,0,.12)}:host .mdc-fab:active,:host .mdc-fab:focus{outline:none}:host .mdc-fab:hover{cursor:pointer}:host .mdc-fab>svg{width:100%}:host .mdc-fab--mini{width:40px;height:40px}:host .mdc-fab--extended{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-button-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-button-font-size, 0.875rem);line-height:2.25rem;line-height:var(--mdc-typography-button-line-height, 2.25rem);font-weight:500;font-weight:var(--mdc-typography-button-font-weight, 500);letter-spacing:0.0892857143em;letter-spacing:var(--mdc-typography-button-letter-spacing, 0.0892857143em);text-decoration:none;text-decoration:var(--mdc-typography-button-text-decoration, none);text-transform:uppercase;text-transform:var(--mdc-typography-button-text-transform, uppercase);border-radius:24px;padding-left:20px;padding-right:20px;width:auto;max-width:100%;height:48px;line-height:normal}:host .mdc-fab--extended .mdc-fab__ripple{border-radius:24px}:host .mdc-fab--extended .mdc-fab__icon{margin-left:calc(12px - 20px);margin-right:12px}[dir=rtl] :host .mdc-fab--extended .mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__icon[dir=rtl]{margin-left:12px;margin-right:calc(12px - 20px)}:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon{margin-left:12px;margin-right:calc(12px - 20px)}[dir=rtl] :host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon,:host .mdc-fab--extended .mdc-fab__label+.mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-right:12px}:host .mdc-fab--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}:host .mdc-fab--touch .mdc-fab__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}:host .mdc-fab::before{position:absolute;box-sizing:border-box;width:100%;height:100%;top:0;left:0;border:1px solid transparent;border-radius:inherit;content:"";pointer-events:none}:host .mdc-fab__label{justify-content:flex-start;text-overflow:ellipsis;white-space:nowrap;overflow-x:hidden;overflow-y:visible}:host .mdc-fab__icon{transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform}:host .mdc-fab .mdc-fab__icon{display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab--exited{transform:scale(0);opacity:0;transition:opacity 15ms linear 150ms,transform 180ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab--exited .mdc-fab__icon{transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab .ripple{overflow:hidden}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab.mdc-fab--extended .ripple{border-radius:24px}:host .mdc-fab .mdc-fab__label{z-index:0}:host .mdc-fab .mdc-fab__icon ::slotted(*){width:inherit;height:inherit;font-size:inherit}:host .mdc-fab--extended.mdc-fab--exited .mdc-fab__icon ::slotted(*){transform:scale(0);transition:transform 135ms 0ms cubic-bezier(0.4, 0, 1, 1)}:host .mdc-fab{padding-top:0px;padding-top:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-right:0px;padding-right:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-bottom:0px;padding-bottom:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-left:0px;padding-left:max(0px, var(--mdc-fab-focus-outline-width, 0px));box-shadow:0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14), 0px 1px 18px 0px rgba(0, 0, 0, 0.12))}:host .mdc-fab:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(:disabled):not(.mdc-ripple-upgraded):focus{border-color:initial;border-color:var(--mdc-fab-focus-outline-color, initial)}:host .mdc-fab:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab:not(:disabled):not(.mdc-ripple-upgraded):focus{border-style:solid;border-width:var(--mdc-fab-focus-outline-width, 0px);padding-top:0px;padding-top:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-right:0px;padding-right:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-bottom:0px;padding-bottom:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-left:0px;padding-left:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1))}:host .mdc-fab:hover,:host .mdc-fab:focus{box-shadow:0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 5px 5px -3px rgba(0, 0, 0, 0.2), 0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12))}:host .mdc-fab:active{box-shadow:0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12);box-shadow:var(--mdc-fab-box-shadow, 0px 7px 8px -4px rgba(0, 0, 0, 0.2), 0px 12px 17px 2px rgba(0, 0, 0, 0.14), 0px 5px 22px 4px rgba(0, 0, 0, 0.12))}:host .mdc-fab .ripple{overflow:hidden}:host .mdc-fab .mdc-fab__label{z-index:0}:host .mdc-fab:not(.mdc-fab--extended) .ripple{border-radius:50%}:host .mdc-fab.mdc-fab--extended .ripple{border-radius:24px}:host .mdc-fab .mdc-fab__icon{width:24px;width:var(--mdc-icon-size, 24px);height:24px;height:var(--mdc-icon-size, 24px);font-size:24px;font-size:var(--mdc-icon-size, 24px);transition:transform 180ms 90ms cubic-bezier(0, 0, 0.2, 1);fill:currentColor;will-change:transform;display:inline-flex;align-items:center;justify-content:center}:host .mdc-fab.mdc-fab--extended{padding-top:0px;padding-top:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-right:20px;padding-right:max(var(--mdc-fab-extended-label-padding, 20px), var(--mdc-fab-focus-outline-width, 0px));padding-bottom:0px;padding-bottom:max(0px, var(--mdc-fab-focus-outline-width, 0px));padding-left:20px;padding-left:max(var(--mdc-fab-extended-label-padding, 20px), var(--mdc-fab-focus-outline-width, 0px))}:host .mdc-fab.mdc-fab--extended:not(:disabled).mdc-ripple-upgraded--background-focused,:host .mdc-fab.mdc-fab--extended:not(:disabled):not(.mdc-ripple-upgraded):focus{border-style:solid;border-width:var(--mdc-fab-focus-outline-width, 0px);padding-top:0px;padding-top:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-right:20px;padding-right:max(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-bottom:0px;padding-bottom:max(calc(0px - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(0px - var(--mdc-fab-focus-outline-width, 0px)) * -1));padding-left:20px;padding-left:max(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)), calc(calc(var(--mdc-fab-extended-label-padding, 20px) - var(--mdc-fab-focus-outline-width, 0px)) * -1))}:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon{margin-left:12px;margin-left:var(--mdc-fab-extended-icon-padding, 12px);margin-right:calc(12px - 20px);margin-right:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px))}[dir=rtl] :host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon,:host .mdc-fab.mdc-fab--extended.icon-end .mdc-fab__icon[dir=rtl]{margin-left:calc(12px - 20px);margin-left:calc(var(--mdc-fab-extended-icon-padding, 12px) - var(--mdc-fab-extended-label-padding, 20px));margin-right:12px;margin-right:var(--mdc-fab-extended-icon-padding, 12px)}`;let X=class extends G{};X.styles=[Q],X=t([c("mwc-fab")],X),p([c("ha-fab")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(t){h(m(i.prototype),"firstUpdated",this).call(this,t),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),X),u({_template:f`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=b(this).parentNode,e=b(this).getOwnerRoot();return this.for?b(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===b(this).textContent.trim()){for(var t=!0,e=b(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,a=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),s=this.getBoundingClientRect(),n=(o.width-s.width)/2,r=(o.height-s.height)/2,d=o.left-a.left,l=o.top-a.top;switch(this.position){case"top":e=d+n,i=l-s.height-t;break;case"bottom":e=d+n,i=l+o.height+t;break;case"left":e=d-s.width-t,i=l+r;break;case"right":e=d+o.width+t,i=l+r}this.fitToVisibleBounds?(a.left+e+s.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),a.top+i+s.height>window.innerHeight?(this.style.bottom=a.height-l+t+"px",this.style.top="auto"):(this.style.top=Math.max(-a.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}}),p([c("ha-icon-overflow-menu")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Array})],key:"items",value:()=>[]},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:()=>!1},{kind:"method",key:"render",value:function(){return r`
      ${this.narrow?r` <!-- Collapsed Representation for Small Screens -->
            <ha-button-menu
              @click=${this._handleIconOverflowMenuOpened}
              @closed=${this._handleIconOverflowMenuClosed}
              class="ha-icon-overflow-menu-overflow"
              corner="BOTTOM_START"
              absolute
            >
              <mwc-icon-button
                .title=${this.hass.localize("ui.common.menu")}
                .label=${this.hass.localize("ui.common.overflow_menu")}
                slot="trigger"
              >
                <ha-svg-icon .path=${x}></ha-svg-icon>
              </mwc-icon-button>

              ${this.items.map(t=>r`
                  <mwc-list-item
                    graphic="icon"
                    .disabled=${t.disabled}
                    @click=${t.action}
                  >
                    <div slot="graphic">
                      <ha-svg-icon .path=${t.path}></ha-svg-icon>
                    </div>
                    ${t.label}
                  </mwc-list-item>
                `)}
            </ha-button-menu>`:r`
            <!-- Icon Representation for Big Screens -->

            ${this.items.map(t=>t.narrowOnly?"":r`<div>
                    ${t.tooltip?r`<paper-tooltip animation-delay="0" position="left">
                          ${t.tooltip}
                        </paper-tooltip>`:""}
                    <mwc-icon-button
                      @click=${t.action}
                      .label=${t.label}
                      .disabled=${t.disabled}
                    >
                      <ha-svg-icon .path=${t.path}></ha-svg-icon>
                    </mwc-icon-button>
                  </div> `)}
          `}
    `}},{kind:"method",key:"_handleIconOverflowMenuOpened",value:function(){const t=this.closest(".mdc-data-table__row");t&&(t.style.zIndex="1")}},{kind:"method",key:"_handleIconOverflowMenuClosed",value:function(){const t=this.closest(".mdc-data-table__row");t&&(t.style.zIndex="")}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: flex;
        justify-content: flex-end;
      }
    `}}]}}),s);const J=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){this["__"+String(e.key)]=t},get(){return this["__"+String(e.key)]},enumerable:!0,configurable:!0},finisher(i){const a=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){if(a.call(this),this[e.key]){const i=this.renderRoot.querySelector(t);if(!i)return;i.scrollTop=this[e.key]}}}});p([c("ha-tab")],(function(t,s){return{F:class extends s{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"active",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[i()],key:"name",value:void 0},{kind:"field",decorators:[e("mwc-ripple")],key:"_ripple",value:void 0},{kind:"field",decorators:[a()],key:"_shouldRenderRipple",value:()=>!1},{kind:"method",key:"render",value:function(){return r`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${g(this.name)}
        @focus=${this.handleRippleFocus}
        @blur=${this.handleRippleBlur}
        @mousedown=${this.handleRippleActivate}
        @mouseup=${this.handleRippleDeactivate}
        @mouseenter=${this.handleRippleMouseEnter}
        @mouseleave=${this.handleRippleMouseLeave}
        @touchstart=${this.handleRippleActivate}
        @touchend=${this.handleRippleDeactivate}
        @touchcancel=${this.handleRippleDeactivate}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?r`<slot name="icon"></slot>`:""}
        ${!this.narrow||this.active?r`<span class="name">${this.name}</span>`:""}
        ${this._shouldRenderRipple?r`<mwc-ripple></mwc-ripple>`:""}
      </div>
    `}},{kind:"field",key:"_rippleHandlers",value(){return new n(()=>(this._shouldRenderRipple=!0,this._ripple))}},{kind:"method",key:"_handleKeyDown",value:function(t){13===t.keyCode&&t.target.click()}},{kind:"method",decorators:[o({passive:!0})],key:"handleRippleActivate",value:function(t){this._rippleHandlers.startPress(t)}},{kind:"method",key:"handleRippleDeactivate",value:function(){this._rippleHandlers.endPress()}},{kind:"method",key:"handleRippleMouseEnter",value:function(){this._rippleHandlers.startHover()}},{kind:"method",key:"handleRippleMouseLeave",value:function(){this._rippleHandlers.endHover()}},{kind:"method",key:"handleRippleFocus",value:function(){this._rippleHandlers.startFocus()}},{kind:"method",key:"handleRippleBlur",value:function(){this._rippleHandlers.endFocus()}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }

      :host([narrow]) div {
        padding: 0 4px;
      }
    `}}]}}),s),p([c("hass-tabs-subpage")],(function(t,e){class s extends e{constructor(...e){super(...e),t(this)}}return{F:s,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[i({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[i({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[i()],key:"backCallback",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[i({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"field",decorators:[a()],key:"_activeTab",value:void 0},{kind:"field",decorators:[J(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return v((t,e,i,a,o,s,n)=>t.filter(t=>(!t.component||t.core||K(this.hass,t.component))&&(!t.advancedOnly||i)).map(t=>r`
            <a href=${t.path}>
              <ha-tab
                .hass=${this.hass}
                .active=${t.path===(null==e?void 0:e.path)}
                .narrow=${this.narrow}
                .name=${t.translationKey?n(t.translationKey):t.name}
              >
                ${t.iconPath?r`<ha-svg-icon
                      slot="icon"
                      .path=${t.iconPath}
                    ></ha-svg-icon>`:""}
              </ha-tab>
            </a>
          `))}},{kind:"method",key:"willUpdate",value:function(t){if(t.has("route")&&(this._activeTab=this.tabs.find(t=>`${this.route.prefix}${this.route.path}`.includes(t.path))),t.has("hass")){const e=t.get("hass");e&&e.language===this.hass.language||(this.rtl=Y(this.hass))}h(m(s.prototype),"willUpdate",this).call(this,t)}},{kind:"method",key:"render",value:function(){var t,e;const i=this._getTabs(this.tabs,this._activeTab,null===(t=this.hass.userData)||void 0===t?void 0:t.showAdvanced,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),a=i.length>1||!this.narrow;return r`
      <div class="toolbar">
        ${this.mainPage||!this.backPath&&null!==(e=history.state)&&void 0!==e&&e.root?r`
              <ha-menu-button
                .hassio=${this.supervisor}
                .hass=${this.hass}
                .narrow=${this.narrow}
              ></ha-menu-button>
            `:this.backPath?r`
              <a href=${this.backPath}>
                <ha-icon-button-arrow-prev
                  .hass=${this.hass}
                ></ha-icon-button-arrow-prev>
              </a>
            `:r`
              <ha-icon-button-arrow-prev
                .hass=${this.hass}
                @click=${this._backTapped}
              ></ha-icon-button-arrow-prev>
            `}
        ${this.narrow?r`<div class="main-title"><slot name="header"></slot></div>`:""}
        ${a?r`
              <div id="tabbar" class=${d({"bottom-bar":this.narrow})}>
                ${i}
              </div>
            `:""}
        <div id="toolbar-icon">
          <slot name="toolbar-icon"></slot>
        </div>
      </div>
      <div
        class="content ${d({tabs:a})}"
        @scroll=${this._saveScrollPos}
      >
        <slot></slot>
      </div>
      <div id="fab" class=${d({tabs:a})}>
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[o({passive:!0})],key:"_saveScrollPos",value:function(t){this._savedScrollPos=t.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
        height: 100%;
        background-color: var(--primary-background-color);
      }

      :host([narrow]) {
        width: 100%;
        position: fixed;
      }

      ha-menu-button {
        margin-right: 24px;
      }

      .toolbar {
        display: flex;
        align-items: center;
        font-size: 20px;
        height: var(--header-height);
        background-color: var(--sidebar-background-color);
        font-weight: 400;
        border-bottom: 1px solid var(--divider-color);
        padding: 0 16px;
        box-sizing: border-box;
      }
      .toolbar a {
        color: var(--app-header-text-color);
        text-decoration: none;
      }
      .bottom-bar a {
        width: 25%;
      }

      #tabbar {
        display: flex;
        font-size: 14px;
        overflow: hidden;
      }

      #tabbar > a {
        overflow: hidden;
        max-width: 45%;
      }

      #tabbar.bottom-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 0 16px;
        box-sizing: border-box;
        background-color: var(--sidebar-background-color);
        border-top: 1px solid var(--divider-color);
        justify-content: space-around;
        z-index: 2;
        font-size: 12px;
        width: 100%;
        padding-bottom: env(safe-area-inset-bottom);
      }

      #tabbar:not(.bottom-bar) {
        flex: 1;
        justify-content: center;
      }

      :host(:not([narrow])) #toolbar-icon {
        min-width: 40px;
      }

      ha-menu-button,
      ha-icon-button-arrow-prev,
      ::slotted([slot="toolbar-icon"]) {
        flex-shrink: 0;
        pointer-events: auto;
        color: var(--sidebar-icon-color);
      }

      .main-title {
        flex: 1;
        max-height: var(--header-height);
        line-height: 20px;
        color: var(--sidebar-text-color);
      }

      .content {
        position: relative;
        width: calc(
          100% - env(safe-area-inset-left) - env(safe-area-inset-right)
        );
        margin-left: env(safe-area-inset-left);
        margin-right: env(safe-area-inset-right);
        height: calc(100% - 1px - var(--header-height));
        height: calc(
          100% - 1px - var(--header-height) - env(safe-area-inset-bottom)
        );
        overflow: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([narrow]) .content.tabs {
        height: calc(100% - 2 * var(--header-height));
        height: calc(
          100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
        );
      }

      #fab {
        position: fixed;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      :host([narrow]) #fab.tabs {
        bottom: calc(84px + env(safe-area-inset-bottom));
      }
      #fab[is-wide] {
        bottom: 24px;
        right: 24px;
      }
      :host([rtl]) #fab {
        right: auto;
        left: calc(16px + env(safe-area-inset-left));
      }
      :host([rtl][is-wide]) #fab {
        bottom: 24px;
        left: 24px;
        right: auto;
      }
    `}}]}}),s);p([c("hacs-repository-card")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:void 0},{kind:"get",key:"_borderClass",value:function(){const t={};return this.hacs.addedToLovelace(this.hacs,this.repository)&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?t["status-update"]=!0:this.repository.new&&!this.repository.installed&&(t["status-new"]=!0):t["status-issue"]=!0,0!==Object.keys(t).length&&(t["status-border"]=!0),t}},{kind:"get",key:"_headerClass",value:function(){const t={};return this.hacs.addedToLovelace(this.hacs,this.repository)&&"pending-restart"!==this.repository.status?this.repository.pending_upgrade?t["update-header"]=!0:this.repository.new&&!this.repository.installed?t["new-header"]=!0:t["default-header"]=!0:t["issue-header"]=!0,t}},{kind:"get",key:"_headerTitle",value:function(){return this.hacs.addedToLovelace(this.hacs,this.repository)?"pending-restart"===this.repository.status?this.hacs.localize("repository_card.pending_restart"):this.repository.pending_upgrade?this.hacs.localize("repository_card.pending_update"):this.repository.new&&!this.repository.installed?this.hacs.localize("repository_card.new_repository"):"":this.hacs.localize("repository_card.not_loaded")}},{kind:"method",key:"render",value:function(){const t=this.repository.local_path.split("/");return r`
      <ha-card class=${d(this._borderClass)} ?narrow=${this.narrow}>
        <div class="card-content">
          <div class="group-header">
            <div class="status-header ${d(this._headerClass)}">${this._headerTitle}</div>
            <div class="title pointer" @click=${this._showReopsitoryInfo}>
              <h1>${this.repository.name}</h1>
              ${"integration"!==this.repository.category?r` <ha-chip>
                    ${this.hacs.localize("common."+this.repository.category)}
                  </ha-chip>`:""}
            </div>
          </div>
          <paper-item>
            <paper-item-body> ${this.repository.description} </paper-item-body>
          </paper-item>
        </div>
        <div class="card-actions">
          ${this.repository.installed?r` <ha-icon-overflow-menu
                slot="toolbar-icon"
                narrow
                .hass=${this.hass}
                .items=${[{path:y,label:this.hacs.localize("repository_card.information"),action:()=>this._showReopsitoryInfo()},{path:w,label:this.hacs.localize("common.repository"),action:()=>{var t;return null===(t=top)||void 0===t?void 0:t.open("https://github.com/"+this.repository.full_name,"_blank","noreferrer=true")}},{path:_,label:this.hacs.localize("repository_card.update_information"),action:()=>this._updateReopsitoryInfo()},{path:k,label:this.hacs.localize("repository_card.redownload"),action:()=>this._installRepository()},{category:"plugin",path:$,label:this.hacs.localize("repository_card.open_source"),action:()=>{var e;return null===(e=top)||void 0===e?void 0:e.open(`/hacsfiles/${t.pop()}/${this.repository.file_name}`,"_blank","noreferrer=true")}},{path:z,label:this.hacs.localize("repository_card.open_issue"),action:()=>{var t;return null===(t=top)||void 0===t?void 0:t.open(`https://github.com/${this.repository.full_name}/issues`,"_blank","noreferrer=true")}},{hideForId:"172733314",path:R,label:this.hacs.localize("repository_card.report"),action:()=>{var t;return null===(t=top)||void 0===t?void 0:t.open(`https://github.com/hacs/integration/issues/new?assignees=ludeeus&labels=flag&template=removal.yml&repo=${this.repository.full_name}&title=Request for removal of ${this.repository.full_name}`,"_blank","noreferrer=true")}},{hideForId:"172733314",path:T,label:this.hacs.localize("common.remove"),action:()=>this._uninstallRepositoryDialog()}].filter(t=>!(t.category&&this.repository.category!==t.category||t.hideForId&&String(this.repository.id)===t.hideForId))}
              >
              </ha-icon-overflow-menu>`:""}
          ${this.repository.new&&!this.repository.installed?r`<div>
                  <mwc-button @click=${this._setNotNew}>
                    ${this.hacs.localize("repository_card.dismiss")}
                  </mwc-button>
                </div>
                <div>
                  <mwc-button @click=${this._installRepository} raised>
                    ${this.hacs.localize("common.download")}
                  </mwc-button>
                </div> `:this.repository.pending_upgrade&&this.hacs.addedToLovelace(this.hacs,this.repository)?r`<div>
                <mwc-button class="update-header" @click=${this._updateRepository} raised>
                  ${this.hacs.localize("common.update")}
                </mwc-button>
              </div> `:""}
        </div>
      </ha-card>
    `}},{kind:"method",key:"_updateReopsitoryInfo",value:async function(){await C(this.hass,this.repository.id)}},{kind:"method",key:"_showReopsitoryInfo",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"repository-info",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_updateRepository",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"update",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_setNotNew",value:async function(){await E(this.hass,this.repository.id)}},{kind:"method",key:"_installRepository",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"download",repository:this.repository.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepositoryDialog",value:async function(){if("integration"===this.repository.category&&this.repository.config_flow){if((await(t=this.hass,t.callApi("GET","config/config_entries/entry"))).some(t=>t.domain===this.repository.domain)){if(await W(this,{title:this.hacs.localize("dialog.configured.title"),text:this.hacs.localize("dialog.configured.message",{name:this.repository.name}),dismissText:this.hacs.localize("common.ignore"),confirmText:this.hacs.localize("common.navigate"),confirm:()=>{F("/config/integrations",{replace:!0})}}))return}}var t;this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"progress",title:this.hacs.localize("dialog.remove.title"),confirmText:this.hacs.localize("dialog.remove.title"),content:this.hacs.localize("dialog.remove.message",{name:this.repository.name}),confirm:async()=>{await this._uninstallRepository()}},bubbles:!0,composed:!0}))}},{kind:"method",key:"_uninstallRepository",value:async function(){var t;if("plugin"===this.repository.category&&"yaml"!==(null===(t=this.hacs.status)||void 0===t?void 0:t.lovelace_mode)){const t=await S(this.hass),e=L({repository:this.repository,skipTag:!0});await Promise.all(t.filter(t=>t.url.includes(e)).map(t=>A(this.hass,String(t.id))))}await I(this.hass,this.repository.id)}},{kind:"get",static:!0,key:"styles",value:function(){return[j,l`
        ha-card {
          display: flex;
          flex-direction: column;
          height: 100%;
          width: 480px;
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
          border-color: transparent;
          border-radius: var(--ha-card-border-radius, 4px);
        }

        .title {
          display: flex;
          justify-content: space-between;
        }
        .card-content {
          padding: 0 0 3px 0;
          height: 100%;
        }
        .card-actions {
          border-top: none;
          bottom: 0;
          display: flex;
          flex-direction: row-reverse;
          justify-content: space-between;
          align-items: center;
          padding: 5px;
        }
        .group-header {
          height: auto;
          align-content: center;
        }
        .group-header h1 {
          margin: 0;
          padding: 8px 16px;
          font-size: 22px;
        }
        h1 {
          margin-top: 0;
          min-height: 24px;
        }

        .pointer {
          cursor: pointer;
        }
        paper-item-body {
          opacity: var(--dark-primary-opacity);
          font-size: 14px;
        }

        .status-new {
          border-color: var(--hcv-color-new);
        }

        .status-update {
          border-color: var(--hcv-color-update);
        }

        .status-issue {
          border-color: var(--hcv-color-error);
        }

        .new-header {
          background-color: var(--hcv-color-new);
          color: var(--hcv-text-color-on-background);
        }

        .issue-header {
          background-color: var(--hcv-color-error);
          color: var(--hcv-text-color-on-background);
        }

        .update-header {
          background-color: var(--hcv-color-update);
          color: var(--hcv-text-color-on-background);
        }

        .default-header {
          padding: 2px 0 !important;
        }

        mwc-button.update-header {
          --mdc-theme-primary: var(--hcv-color-update);
          --mdc-theme-on-primary: var(--hcv-text-color-on-background);
        }

        .status-border {
          border-style: solid;
          border-width: min(var(--ha-card-border-width, 1px), 10px);
        }

        .status-header {
          top: 0;
          padding: 6px 1px;
          margin: -1px;
          width: 100%;
          font-weight: 500;
          text-align: center;
          left: 0;
          border-top-left-radius: var(--ha-card-border-radius, 4px);
          border-top-right-radius: var(--ha-card-border-radius, 4px);
        }

        ha-card[narrow] {
          width: calc(100% - 24px);
          margin: 11px;
        }

        ha-chip {
          padding: 4px;
          margin-top: 3px;
        }
      `]}}]}}),s);let Z=p([c("hacs-store-panel")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:()=>({})},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[i()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"narrow",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"isWide",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"sections",value:void 0},{kind:"field",decorators:[i()],key:"section",value:void 0},{kind:"field",key:"_repositoriesInActiveSection",value(){return v((t,e)=>[(null==t?void 0:t.filter(t=>{var i,a,o;return(null===(i=this.hacs.sections)||void 0===i||null===(a=i.find(t=>t.id===e))||void 0===a||null===(o=a.categories)||void 0===o?void 0:o.includes(t.category))&&t.installed}))||[],(null==t?void 0:t.filter(t=>{var i,a,o;return(null===(i=this.hacs.sections)||void 0===i||null===(a=i.find(t=>t.id===e))||void 0===a||null===(o=a.categories)||void 0===o?void 0:o.includes(t.category))&&t.new&&!t.installed}))||[]])}},{kind:"get",key:"allRepositories",value:function(){const[t,e]=this._repositoriesInActiveSection(this.hacs.repositories,this.section);return e.concat(t)}},{kind:"field",key:"_filterRepositories",value:()=>v(V)},{kind:"get",key:"visibleRepositories",value:function(){const t=this.allRepositories.filter(t=>{var e,i;return null===(e=this.filters[this.section])||void 0===e||null===(i=e.find(e=>e.id===t.category))||void 0===i?void 0:i.checked});return this._filterRepositories(t,this._searchInput)}},{kind:"method",key:"firstUpdated",value:async function(){this.addEventListener("filter-change",t=>this._updateFilters(t))}},{kind:"method",key:"_updateFilters",value:function(t){var e;const i=null===(e=this.filters[this.section])||void 0===e?void 0:e.find(e=>e.id===t.detail.id);this.filters[this.section].find(t=>t.id===i.id).checked=!i.checked,this.requestUpdate()}},{kind:"method",key:"render",value:function(){var t;if(!this.hacs)return r``;const e=this._repositoriesInActiveSection(this.hacs.repositories,this.section)[1];if(!this.filters[this.section]&&this.hacs.configuration.categories){var i;const t=null===(i=P(this.hacs.language,this.route))||void 0===i?void 0:i.categories;this.filters[this.section]=[],null==t||t.filter(t=>{var e;return null===(e=this.hacs.configuration)||void 0===e?void 0:e.categories.includes(t)}).forEach(t=>{this.filters[this.section].push({id:t,value:t,checked:!0})})}return r`<hass-tabs-subpage
      back-path="/hacs/entry"
      .hass=${this.hass}
      .narrow=${this.narrow}
      .route=${this.route}
      .tabs=${this.hacs.sections}
      hasFab
    >
      <ha-icon-overflow-menu
        slot="toolbar-icon"
        narrow
        .hass=${this.hass}
        .items=${[{path:B,label:this.hacs.localize("menu.documentation"),action:()=>{var t;return null===(t=top)||void 0===t?void 0:t.open("https://hacs.xyz/","_blank","noreferrer=true")}},{path:w,label:"GitHub",action:()=>{var t;return null===(t=top)||void 0===t?void 0:t.open("https://github.com/hacs","_blank","noreferrer=true")}},{path:z,label:this.hacs.localize("menu.open_issue"),action:()=>{var t;return null===(t=top)||void 0===t?void 0:t.open("https://hacs.xyz/docs/issues","_blank","noreferrer=true")}},{path:M,label:this.hacs.localize("menu.custom_repositories"),disabled:this.hacs.status.disabled||this.hacs.status.background_task,action:()=>this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"custom-repositories",repositories:this.hacs.repositories},bubbles:!0,composed:!0}))},{path:y,label:this.hacs.localize("menu.about"),action:()=>q(this,this.hacs)}]}
      >
      </ha-icon-overflow-menu>
      ${this.narrow?r`
            <div slot="header">
              <slot name="header">
                <search-input
                  .hass=${this.hass}
                  class="header"
                  no-label-float
                  .label=${this.hacs.localize("search.downloaded")}
                  .filter=${this._searchInput||""}
                  @value-changed=${this._inputValueChanged}
                ></search-input>
              </slot>
            </div>
          `:r`<div class="search">
            <search-input
              .hass=${this.hass}
              no-label-float
              .label=${0===e.length?this.hacs.localize("search.downloaded"):this.hacs.localize("search.downloaded_new")}
              .filter=${this._searchInput||""}
              @value-changed=${this._inputValueChanged}
            ></search-input>
          </div>`}
      <div class="content ${this.narrow?"narrow-content":""}">
        ${(null===(t=this.filters[this.section])||void 0===t?void 0:t.length)>1?r`<div class="filters">
              <hacs-filter
                .hacs=${this.hacs}
                .filters="${this.filters[this.section]}"
              ></hacs-filter>
            </div>`:""}
        ${null!=e&&e.length?r`<ha-alert .rtl=${Y(this.hass)}>
              ${this.hacs.localize("store.new_repositories_note")}
              <mwc-button
                slot="action"
                .label=${this.hacs.localize("menu.dismiss")}
                @click=${this._clearAllNewRepositories}
              >
              </mwc-button>
            </ha-alert> `:""}
        <div class="container ${this.narrow?"narrow":""}">
          ${void 0===this.hacs.repositories?"":0===this.allRepositories.length?this._renderEmpty():0===this.visibleRepositories.length?this._renderNoResultsFound():this._renderRepositories()}
        </div>
      </div>
      <ha-fab
        slot="fab"
        .label=${this.hacs.localize("store.explore")}
        .extended=${!this.narrow}
        @click=${this._addRepository}
      >
        <ha-svg-icon slot="icon" .path=${O}></ha-svg-icon>
      </ha-fab>
    </hass-tabs-subpage>`}},{kind:"method",key:"_renderRepositories",value:function(){return this.visibleRepositories.map(t=>r`<hacs-repository-card
          .hass=${this.hass}
          .hacs=${this.hacs}
          .repository=${t}
          .narrow=${this.narrow}
          ?narrow=${this.narrow}
        ></hacs-repository-card>`)}},{kind:"method",key:"_clearAllNewRepositories",value:async function(){var t;await D(this.hass,(null===(t=P(this.hacs.language,this.route))||void 0===t?void 0:t.categories)||[])}},{kind:"method",key:"_renderNoResultsFound",value:function(){return r`<ha-alert
      .rtl=${Y(this.hass)}
      alert-type="warning"
      .title="${this.hacs.localize("store.no_repositories")} 😕"
    >
      ${this.hacs.localize("store.no_repositories_found_desc1",{searchInput:this._searchInput})}
      <br />
      ${this.hacs.localize("store.no_repositories_found_desc2")}
    </ha-alert>`}},{kind:"method",key:"_renderEmpty",value:function(){return r`<ha-alert
      .title="${this.hacs.localize("store.no_repositories")} 😕"
      .rtl=${Y(this.hass)}
    >
      ${this.hacs.localize("store.no_repositories_desc1")}
      <br />
      ${this.hacs.localize("store.no_repositories_desc2")}
    </ha-alert>`}},{kind:"method",key:"_inputValueChanged",value:function(t){this._searchInput=t.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_addRepository",value:function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"add-repository",repositories:this.hacs.repositories,section:this.section},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[j,H,N,U,l`
        .filter {
          border-bottom: 1px solid var(--divider-color);
        }
        .content {
          height: calc(100vh - 128px);
          overflow: auto;
        }
        .narrow-content {
          height: calc(100vh - 128px);
        }
        .container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
          justify-items: center;
          grid-gap: 8px 8px;
          padding: 8px 16px 16px;
          margin-bottom: 64px;
        }
        ha-svg-icon {
          color: var(--hcv-text-color-on-background);
        }
        hacs-repository-card {
          max-width: 500px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        hacs-repository-card[narrow] {
          width: 100%;
        }
        hacs-repository-card[narrow]:last-of-type {
          margin-bottom: 64px;
        }
        ha-alert {
          color: var(--hcv-text-color-primary);
          display: block;
          margin-top: -4px;
        }
        .narrow {
          width: 100%;
          display: block;
          padding: 0px;
          margin: 0;
        }

        .bottom-bar {
          position: fixed !important;
        }
      `]}}]}}),s);export{Z as HacsStorePanel};
