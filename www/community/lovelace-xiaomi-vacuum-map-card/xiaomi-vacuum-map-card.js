/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
function e(e,t,i,a){var n,r=arguments.length,o=r<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,i):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,i,a);else for(var s=e.length-1;s>=0;s--)(n=e[s])&&(o=(r<3?n(o):r>3?n(t,i,o):n(t,i))||o);return r>3&&o&&Object.defineProperty(t,i,o),o
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */}const t=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol();class a{constructor(e,t){if(t!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return t&&void 0===this.t&&(this.t=new CSSStyleSheet,this.t.replaceSync(this.cssText)),this.t}toString(){return this.cssText}}const n=new Map,r=e=>{let t=n.get(e);return void 0===t&&n.set(e,t=new a(e,i)),t},o=(e,...t)=>{const i=1===e.length?e[0]:t.reduce(((t,i,n)=>t+(e=>{if(e instanceof a)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+e[n+1]),e[0]);return r(i)},s=t?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const i of e.cssRules)t+=i.cssText;return(e=>r("string"==typeof e?e:e+""))(t)})(e):e
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */;var l,c,d,u;const m={toAttribute(e,t){switch(t){case Boolean:e=e?"":null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let i=e;switch(t){case Boolean:i=null!==e;break;case Number:i=null===e?null:Number(e);break;case Object:case Array:try{i=JSON.parse(e)}catch(e){i=null}}return i}},p=(e,t)=>t!==e&&(t==t||e==e),_={attribute:!0,type:String,converter:m,reflect:!1,hasChanged:p};class h extends HTMLElement{constructor(){super(),this.Πi=new Map,this.Πo=void 0,this.Πl=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this.Πh=null,this.u()}static addInitializer(e){var t;null!==(t=this.v)&&void 0!==t||(this.v=[]),this.v.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,i)=>{const a=this.Πp(i,t);void 0!==a&&(this.Πm.set(a,i),e.push(a))})),e}static createProperty(e,t=_){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const i="symbol"==typeof e?Symbol():"__"+e,a=this.getPropertyDescriptor(e,i,t);void 0!==a&&Object.defineProperty(this.prototype,e,a)}}static getPropertyDescriptor(e,t,i){return{get(){return this[t]},set(a){const n=this[e];this[t]=a,this.requestUpdate(e,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||_}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this.Πm=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const i of t)this.createProperty(i,e[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const i=new Set(e.flat(1/0).reverse());for(const e of i)t.unshift(s(e))}else void 0!==e&&t.push(s(e));return t}static"Πp"(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}u(){var e;this.Πg=new Promise((e=>this.enableUpdating=e)),this.L=new Map,this.Π_(),this.requestUpdate(),null===(e=this.constructor.v)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,i;(null!==(t=this.ΠU)&&void 0!==t?t:this.ΠU=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(i=e.hostConnected)||void 0===i||i.call(e))}removeController(e){var t;null===(t=this.ΠU)||void 0===t||t.splice(this.ΠU.indexOf(e)>>>0,1)}"Π_"(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this.Πi.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const i=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return((e,i)=>{t?e.adoptedStyleSheets=i.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):i.forEach((t=>{const i=document.createElement("style");i.textContent=t.cssText,e.appendChild(i)}))})(i,this.constructor.elementStyles),i}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)})),this.Πl&&(this.Πl(),this.Πo=this.Πl=void 0)}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)})),this.Πo=new Promise((e=>this.Πl=e))}attributeChangedCallback(e,t,i){this.K(e,i)}"Πj"(e,t,i=_){var a,n;const r=this.constructor.Πp(e,i);if(void 0!==r&&!0===i.reflect){const o=(null!==(n=null===(a=i.converter)||void 0===a?void 0:a.toAttribute)&&void 0!==n?n:m.toAttribute)(t,i.type);this.Πh=e,null==o?this.removeAttribute(r):this.setAttribute(r,o),this.Πh=null}}K(e,t){var i,a,n;const r=this.constructor,o=r.Πm.get(e);if(void 0!==o&&this.Πh!==o){const e=r.getPropertyOptions(o),s=e.converter,l=null!==(n=null!==(a=null===(i=s)||void 0===i?void 0:i.fromAttribute)&&void 0!==a?a:"function"==typeof s?s:null)&&void 0!==n?n:m.fromAttribute;this.Πh=o,this[o]=l(t,e.type),this.Πh=null}}requestUpdate(e,t,i){let a=!0;void 0!==e&&(((i=i||this.constructor.getPropertyOptions(e)).hasChanged||p)(this[e],t)?(this.L.has(e)||this.L.set(e,t),!0===i.reflect&&this.Πh!==e&&(void 0===this.Πk&&(this.Πk=new Map),this.Πk.set(e,i))):a=!1),!this.isUpdatePending&&a&&(this.Πg=this.Πq())}async"Πq"(){this.isUpdatePending=!0;try{for(await this.Πg;this.Πo;)await this.Πo}catch(e){Promise.reject(e)}const e=this.performUpdate();return null!=e&&await e,!this.isUpdatePending}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this.Πi&&(this.Πi.forEach(((e,t)=>this[t]=e)),this.Πi=void 0);let t=!1;const i=this.L;try{t=this.shouldUpdate(i),t?(this.willUpdate(i),null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(i)):this.Π$()}catch(e){throw t=!1,this.Π$(),e}t&&this.E(i)}willUpdate(e){}E(e){var t;null===(t=this.ΠU)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}"Π$"(){this.L=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this.Πg}shouldUpdate(e){return!0}update(e){void 0!==this.Πk&&(this.Πk.forEach(((e,t)=>this.Πj(t,this[t],e))),this.Πk=void 0),this.Π$()}updated(e){}firstUpdated(e){}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var v,g,f,b;h.finalized=!0,h.elementProperties=new Map,h.elementStyles=[],h.shadowRootOptions={mode:"open"},null===(c=(l=globalThis).reactiveElementPlatformSupport)||void 0===c||c.call(l,{ReactiveElement:h}),(null!==(d=(u=globalThis).reactiveElementVersions)&&void 0!==d?d:u.reactiveElementVersions=[]).push("1.0.0-rc.2");const y=globalThis.trustedTypes,x=y?y.createPolicy("lit-html",{createHTML:e=>e}):void 0,k=`lit$${(Math.random()+"").slice(9)}$`,A="?"+k,w=`<${A}>`,E=document,z=(e="")=>E.createComment(e),P=e=>null===e||"object"!=typeof e&&"function"!=typeof e,S=Array.isArray,M=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,T=/-->/g,C=/>/g,N=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,R=/'/g,L=/"/g,O=/^(?:script|style|textarea)$/i,$=e=>(t,...i)=>({_$litType$:e,strings:t,values:i}),j=$(1),I=$(2),D=Symbol.for("lit-noChange"),F=Symbol.for("lit-nothing"),V=new WeakMap,U=E.createTreeWalker(E,129,null,!1);class X{constructor({strings:e,_$litType$:t},i){let a;this.parts=[];let n=0,r=0;const o=e.length-1,s=this.parts,[l,c]=((e,t)=>{const i=e.length-1,a=[];let n,r=2===t?"<svg>":"",o=M;for(let t=0;t<i;t++){const i=e[t];let s,l,c=-1,d=0;for(;d<i.length&&(o.lastIndex=d,l=o.exec(i),null!==l);)d=o.lastIndex,o===M?"!--"===l[1]?o=T:void 0!==l[1]?o=C:void 0!==l[2]?(O.test(l[2])&&(n=RegExp("</"+l[2],"g")),o=N):void 0!==l[3]&&(o=N):o===N?">"===l[0]?(o=null!=n?n:M,c=-1):void 0===l[1]?c=-2:(c=o.lastIndex-l[2].length,s=l[1],o=void 0===l[3]?N:'"'===l[3]?L:R):o===L||o===R?o=N:o===T||o===C?o=M:(o=N,n=void 0);const u=o===N&&e[t+1].startsWith("/>")?" ":"";r+=o===M?i+w:c>=0?(a.push(s),i.slice(0,c)+"$lit$"+i.slice(c)+k+u):i+k+(-2===c?(a.push(void 0),t):u)}const s=r+(e[i]||"<?>")+(2===t?"</svg>":"");return[void 0!==x?x.createHTML(s):s,a]})(e,t);if(this.el=X.createElement(l,i),U.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(a=U.nextNode())&&s.length<o;){if(1===a.nodeType){if(a.hasAttributes()){const e=[];for(const t of a.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(k)){const i=c[r++];if(e.push(t),void 0!==i){const e=a.getAttribute(i.toLowerCase()+"$lit$").split(k),t=/([.?@])?(.*)/.exec(i);s.push({type:1,index:n,name:t[2],strings:e,ctor:"."===t[1]?B:"?"===t[1]?G:"@"===t[1]?W:K})}else s.push({type:6,index:n})}for(const t of e)a.removeAttribute(t)}if(O.test(a.tagName)){const e=a.textContent.split(k),t=e.length-1;if(t>0){a.textContent=y?y.emptyScript:"";for(let i=0;i<t;i++)a.append(e[i],z()),U.nextNode(),s.push({type:2,index:++n});a.append(e[t],z())}}}else if(8===a.nodeType)if(a.data===A)s.push({type:2,index:n});else{let e=-1;for(;-1!==(e=a.data.indexOf(k,e+1));)s.push({type:7,index:n}),e+=k.length-1}n++}}static createElement(e,t){const i=E.createElement("template");return i.innerHTML=e,i}}function H(e,t,i=e,a){var n,r,o,s;if(t===D)return t;let l=void 0!==a?null===(n=i.Σi)||void 0===n?void 0:n[a]:i.Σo;const c=P(t)?void 0:t._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(r=null==l?void 0:l.O)||void 0===r||r.call(l,!1),void 0===c?l=void 0:(l=new c(e),l.T(e,i,a)),void 0!==a?(null!==(o=(s=i).Σi)&&void 0!==o?o:s.Σi=[])[a]=l:i.Σo=l),void 0!==l&&(t=H(e,l.S(e,t.values),l,a)),t}class q{constructor(e,t){this.l=[],this.N=void 0,this.D=e,this.M=t}u(e){var t;const{el:{content:i},parts:a}=this.D,n=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:E).importNode(i,!0);U.currentNode=n;let r=U.nextNode(),o=0,s=0,l=a[0];for(;void 0!==l;){if(o===l.index){let t;2===l.type?t=new Z(r,r.nextSibling,this,e):1===l.type?t=new l.ctor(r,l.name,l.strings,this,e):6===l.type&&(t=new Y(r,this,e)),this.l.push(t),l=a[++s]}o!==(null==l?void 0:l.index)&&(r=U.nextNode(),o++)}return n}v(e){let t=0;for(const i of this.l)void 0!==i&&(void 0!==i.strings?(i.I(e,i,t),t+=i.strings.length-2):i.I(e[t])),t++}}class Z{constructor(e,t,i,a){this.type=2,this.N=void 0,this.A=e,this.B=t,this.M=i,this.options=a}setConnected(e){var t;null===(t=this.P)||void 0===t||t.call(this,e)}get parentNode(){return this.A.parentNode}get startNode(){return this.A}get endNode(){return this.B}I(e,t=this){e=H(this,e,t),P(e)?e===F||null==e||""===e?(this.H!==F&&this.R(),this.H=F):e!==this.H&&e!==D&&this.m(e):void 0!==e._$litType$?this._(e):void 0!==e.nodeType?this.$(e):(e=>{var t;return S(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])})(e)?this.g(e):this.m(e)}k(e,t=this.B){return this.A.parentNode.insertBefore(e,t)}$(e){this.H!==e&&(this.R(),this.H=this.k(e))}m(e){const t=this.A.nextSibling;null!==t&&3===t.nodeType&&(null===this.B?null===t.nextSibling:t===this.B.previousSibling)?t.data=e:this.$(E.createTextNode(e)),this.H=e}_(e){var t;const{values:i,_$litType$:a}=e,n="number"==typeof a?this.C(e):(void 0===a.el&&(a.el=X.createElement(a.h,this.options)),a);if((null===(t=this.H)||void 0===t?void 0:t.D)===n)this.H.v(i);else{const e=new q(n,this),t=e.u(this.options);e.v(i),this.$(t),this.H=e}}C(e){let t=V.get(e.strings);return void 0===t&&V.set(e.strings,t=new X(e)),t}g(e){S(this.H)||(this.H=[],this.R());const t=this.H;let i,a=0;for(const n of e)a===t.length?t.push(i=new Z(this.k(z()),this.k(z()),this,this.options)):i=t[a],i.I(n),a++;a<t.length&&(this.R(i&&i.B.nextSibling,a),t.length=a)}R(e=this.A.nextSibling,t){var i;for(null===(i=this.P)||void 0===i||i.call(this,!1,!0,t);e&&e!==this.B;){const t=e.nextSibling;e.remove(),e=t}}}class K{constructor(e,t,i,a,n){this.type=1,this.H=F,this.N=void 0,this.V=void 0,this.element=e,this.name=t,this.M=a,this.options=n,i.length>2||""!==i[0]||""!==i[1]?(this.H=Array(i.length-1).fill(F),this.strings=i):this.H=F}get tagName(){return this.element.tagName}I(e,t=this,i,a){const n=this.strings;let r=!1;if(void 0===n)e=H(this,e,t,0),r=!P(e)||e!==this.H&&e!==D,r&&(this.H=e);else{const a=e;let o,s;for(e=n[0],o=0;o<n.length-1;o++)s=H(this,a[i+o],t,o),s===D&&(s=this.H[o]),r||(r=!P(s)||s!==this.H[o]),s===F?e=F:e!==F&&(e+=(null!=s?s:"")+n[o+1]),this.H[o]=s}r&&!a&&this.W(e)}W(e){e===F?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class B extends K{constructor(){super(...arguments),this.type=3}W(e){this.element[this.name]=e===F?void 0:e}}class G extends K{constructor(){super(...arguments),this.type=4}W(e){e&&e!==F?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class W extends K{constructor(){super(...arguments),this.type=5}I(e,t=this){var i;if((e=null!==(i=H(this,e,t,0))&&void 0!==i?i:F)===D)return;const a=this.H,n=e===F&&a!==F||e.capture!==a.capture||e.once!==a.once||e.passive!==a.passive,r=e!==F&&(a===F||n);n&&this.element.removeEventListener(this.name,this,a),r&&this.element.addEventListener(this.name,this,e),this.H=e}handleEvent(e){var t,i;"function"==typeof this.H?this.H.call(null!==(i=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==i?i:this.element,e):this.H.handleEvent(e)}}class Y{constructor(e,t,i){this.element=e,this.type=6,this.N=void 0,this.V=void 0,this.M=t,this.options=i}I(e){H(this,e)}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var J,Q,ee,te,ie,ae;null===(g=(v=globalThis).litHtmlPlatformSupport)||void 0===g||g.call(v,X,Z),(null!==(f=(b=globalThis).litHtmlVersions)&&void 0!==f?f:b.litHtmlVersions=[]).push("2.0.0-rc.3"),(null!==(J=(ae=globalThis).litElementVersions)&&void 0!==J?J:ae.litElementVersions=[]).push("3.0.0-rc.2");class ne extends h{constructor(){super(...arguments),this.renderOptions={host:this},this.Φt=void 0}createRenderRoot(){var e,t;const i=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=i.firstChild),i}update(e){const t=this.render();super.update(e),this.Φt=((e,t,i)=>{var a,n;const r=null!==(a=null==i?void 0:i.renderBefore)&&void 0!==a?a:t;let o=r._$litPart$;if(void 0===o){const e=null!==(n=null==i?void 0:i.renderBefore)&&void 0!==n?n:null;r._$litPart$=o=new Z(t.insertBefore(z(),e),e,void 0,i)}return o.I(e),o})(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this.Φt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.Φt)||void 0===e||e.setConnected(!1)}render(){return D}}ne.finalized=!0,ne._$litElement$=!0,null===(ee=(Q=globalThis).litElementHydrateSupport)||void 0===ee||ee.call(Q,{LitElement:ne}),null===(ie=(te=globalThis).litElementPlatformSupport)||void 0===ie||ie.call(te,{LitElement:ne});
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const re=e=>t=>"function"==typeof t?((e,t)=>(window.customElements.define(e,t),t))(e,t):((e,t)=>{const{kind:i,elements:a}=t;return{kind:i,elements:a,finisher(t){window.customElements.define(e,t)}}})(e,t)
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */,oe=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?{...t,finisher(i){i.createProperty(t.key,e)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:t.key,initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(i){i.createProperty(t.key,e)}};function se(e){return(t,i)=>void 0!==i?((e,t,i)=>{t.constructor.createProperty(i,e)})(e,t,i):oe(e,t)
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */}function le(e){return se({...e,state:!0,attribute:!1})}var ce="[^\\s]+";function de(e,t){for(var i=[],a=0,n=e.length;a<n;a++)i.push(e[a].substr(0,t));return i}var ue=function(e){return function(t,i){var a=i[e].map((function(e){return e.toLowerCase()})),n=a.indexOf(t.toLowerCase());return n>-1?n:null}};function me(e){for(var t=[],i=1;i<arguments.length;i++)t[i-1]=arguments[i];for(var a=0,n=t;a<n.length;a++){var r=n[a];for(var o in r)e[o]=r[o]}return e}var pe=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],_e=["January","February","March","April","May","June","July","August","September","October","November","December"],he=de(_e,3),ve={dayNamesShort:de(pe,3),dayNames:pe,monthNamesShort:he,monthNames:_e,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10?1:0)*e%10]}},ge=(me({},ve),function(e){return+e-1}),fe=[null,"[1-9]\\d?"],be=[null,ce],ye=["isPm",ce,function(e,t){var i=e.toLowerCase();return i===t.amPm[0]?0:i===t.amPm[1]?1:null}],xe=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(e){var t=(e+"").match(/([+-]|\d\d)/gi);if(t){var i=60*+t[1]+parseInt(t[2],10);return"+"===t[0]?i:-i}return 0}];ue("monthNamesShort"),ue("monthNames");var ke;!function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}}(),function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}}(),function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}}(),function(e){e.language="language",e.system="system",e.comma_decimal="comma_decimal",e.decimal_comma="decimal_comma",e.space_comma="space_comma",e.none="none"}(ke||(ke={}));var Ae=["closed","locked","off"],we=function(e,t,i,a){a=a||{},i=null==i?{}:i;var n=new Event(t,{bubbles:void 0===a.bubbles||a.bubbles,cancelable:Boolean(a.cancelable),composed:void 0===a.composed||a.composed});return n.detail=i,e.dispatchEvent(n),n},Ee=function(e){we(window,"haptic",e)},ze=function(e,t,i,a){if(a||(a={action:"more-info"}),!a.confirmation||a.confirmation.exemptions&&a.confirmation.exemptions.some((function(e){return e.user===t.user.id}))||(Ee("warning"),confirm(a.confirmation.text||"Are you sure you want to "+a.action+"?")))switch(a.action){case"more-info":(i.entity||i.camera_image)&&we(e,"hass-more-info",{entityId:i.entity?i.entity:i.camera_image});break;case"navigate":a.navigation_path&&function(e,t,i){void 0===i&&(i=!1),i?history.replaceState(null,"",t):history.pushState(null,"",t),we(window,"location-changed",{replace:i})}(0,a.navigation_path);break;case"url":a.url_path&&window.open(a.url_path);break;case"toggle":i.entity&&(function(e,t){(function(e,t,i){void 0===i&&(i=!0);var a,n=function(e){return e.substr(0,e.indexOf("."))}(t),r="group"===n?"homeassistant":n;switch(n){case"lock":a=i?"unlock":"lock";break;case"cover":a=i?"open_cover":"close_cover";break;default:a=i?"turn_on":"turn_off"}e.callService(r,a,{entity_id:t})})(e,t,Ae.includes(e.states[t].state))}(t,i.entity),Ee("success"));break;case"call-service":if(!a.service)return void Ee("failure");var n=a.service.split(".",2);t.callService(n[0],n[1],a.service_data),Ee("success");break;case"fire-dom-event":we(e,"ll-custom",a)}};function Pe(e){return void 0!==e&&"none"!==e.action}var Se={version:"Version",invalid_configuration:"Ugyldig konfiguration {0}",description:"Et kort som lader dig styre din robotstøvsuger",old_configuration:"Gammel opsætning fundet. Juster dine indstillinger til det seneste format, eller lav et nyt kort fra bunden.",old_configuration_migration_link:"Migrerings vejledning"},Me={invalid:"Ugyldigt template!",vacuum_goto:"Klik & Gå",vacuum_goto_predefined:"Punkter",vacuum_clean_segment:"Rum",vacuum_clean_zone:"Zone rengøring",vacuum_clean_zone_predefined:"Zoner",vacuum_follow_path:"Sti"},Te={preset:{entity:{missing:"Mangler indstilling: entity"},preset_name:{missing:"Mangler indstilling: preset_name"},platform:{invalid:"Ugyldig støvsuger platform: {0}"},map_source:{missing:"Mangler indstilling: map_source",none_provided:"Intet kamera eller billede er angivet",ambiguous:"Kun en kort-kilde tilladt"},calibration_source:{missing:"Mangler indstilling: calibration_source",ambiguous:"Kun en kalibrerings-kilde tilladt",none_provided:"Ingen kalibrerings kilde angivet",calibration_points:{invalid_number:"Nøjagtigt 3 eller 4 kalibreringspunkter påkrævet",missing_map:"Alle kalibreringspunkter skal indeholde kort koordinater",missing_vacuum:"Alle kalibreringspunkter skal indeholde støvsuger koordinater",missing_coordinate:"Kort og støvsugers kalibreringspunkter skal indeholde både x og y koordinater"}},icons:{invalid:"Fejl i konfiguration: icons",icon:{missing:"Alle punkter i icons listen skal indeholde icon egenskaben"}},tiles:{invalid:"Fejl i konfiguration: tiles",entity:{missing:"Alle punkter i tiles listen skal indehold entity egenskaben"},label:{missing:"Alle punkter i tiles listen skal indehold label egenskaben"}},map_modes:{invalid:"Fejl i konfiguration: map_modes",icon:{missing:"Ikon mangler"},name:{missing:"Navn mangler"},template:{invalid:"Ugyldigt template: {0}"},predefined_selections:{not_applicable:"Mode {0} understøtter ikke predefinerede valg",zones:{missing:"Zone konfiguration mangler",invalid_parameters_number:"En zone skal indeholde 4 parametre."},points:{position:{missing:"Punkt konfiguration mangler",invalid_parameters_number:"Et punkt skal indeholde 2 parametre"}},rooms:{id:{missing:"Rummets id mangler",invalid_format:"Ugyldigt rum id: {0}"},outline:{invalid_parameters_number:"Et punkt i rummets kant skal indeholde 2 parametre"}},label:{x:{missing:"Label skal indeholde egenskaben x"},y:{missing:"Label skal indeholde egenskaben y"},text:{missing:"Label skal indeholde egenskaben text"}},icon:{x:{missing:"Icon skal indeholde egenskaben x"},y:{missing:"Icon skal indeholde egenskaben y"},name:{missing:"Icon skal indeholde egenskaben name"}}},service_call_schema:{missing:"Service-kald indstillingerne mangler",service:{missing:"Service-kald indstillinger skal indeholde en service",invalid:"Ugyldig service: {0}"}}}},invalid_entities:"Ugyldige entiteter:",invalid_calibration:"Ugyldig kalibrering, du bedes gennemgå din konfiguration"},Ce={status:"Status",battery_level:"Batteri",fan_speed:"Hastighed",sensor_dirty_left:"Sensor vedl.",filter_left:"Filter vedl.",main_brush_left:"Hovedbørste vedl.",side_brush_left:"Sidebørste vedl.",cleaning_count:"Rengøringstæller",cleaned_area:"Rengjort areal",cleaning_time:"Rengørings tid"},Ne={vacuum_start:"Start",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Returner",vacuum_clean_spot:"Spotrengør",vacuum_locate:"Find",vacuum_set_fan_speed:"Skift hastighed"},Re={hour_shortcut:"t",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Le={success:"Succes!",no_selection:"Intet valg angivet",failed:"Service-kald fejlede"},Oe={description:{before_link:"Den visuelle editor understøtter kun kun en konfiguration med en kamera entitet lavet med ",link_text:"Xiaomi Cloud Map Extractor",after_link:". For en mere advanceret konfiguration, brug YAML mode."},label:{name:"Titel (valgfrit)",entity:"Støvsuger entitet (påkrævet)",camera:"Kamera entitet (påkrævet)",vacuum_platform:"Støvsuger platform (påkrævet)",map_locked:"Kort låst (valgfrit)",two_finger_pan:"To-finger panorering (valgfrit)"}},$e={common:Se,map_mode:Me,validation:Te,label:Ce,icon:Ne,unit:Re,popups:Le,editor:Oe},je={version:"Version",invalid_configuration:"Ungültige Konfiguration {0}",description:"Eine Karte, mit der Sie Ihren Staubsauger kontrollieren können.",old_configuration:"Es wurde eine alte Konfiguration erkannt. Passen Sie Ihre Konfiguration an das neueste Schema an oder erstellen Sie eine neue Karte von Grund auf.",old_configuration_migration_link:"Migrationsanleitung"},Ie={invalid:"Ungültige Vorlage!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Punkte",vacuum_clean_segment:"Räume",vacuum_clean_zone:"Zone reinigen",vacuum_clean_zone_predefined:"Zonenliste",vacuum_follow_path:"Pfad"},De={preset:{entity:{missing:"Fehlende Eigenschaft: entity"},preset_name:{missing:"Fehlende Eigenschaft: preset_name,"},platform:{invalid:"Ungültige Staubsauger-Plattform: {0}"},map_source:{missing:"Fehlende Eigenschaft: map_source",none_provided:"Keine Kamera und kein Bild vorhanden",ambiguous:"Nur eine Kartenquelle erlaubt"},calibration_source:{missing:"Fehlende Eigenschaft: calibration_source",ambiguous:"Nur eine Kalibrierungsquelle erlaubt",none_provided:"Keine Kalibrierungsquelle vorhanden",calibration_points:{invalid_number:"Genau 3 oder 4 Kalibrierungspunkte erforderlich",missing_map:"Jeder Kalibrierungspunkt muss Kartenkoordinaten enthalten",missing_vacuum:"Jeder Kalibrierungspunkt muss Stabsauger-Koordinaten enthalten",missing_coordinate:"Karten- und Vakuumkalibrierungspunkte müssen sowohl x- als auch y-Koordinaten enthalten"}},icons:{invalid:"Fehler in der Konfiguration: icons",icon:{missing:"Jeder Eintrag der Icon-Liste muss die Ikoneneigenschaft"}},tiles:{invalid:"Fehler in der Konfiguration: tiles",entity:{missing:"Jeder Eintrag der Kachel-Liste muss eine Entität enthalten"},label:{missing:"Jeder Eintrag der Kachel-Liste muss ein Label enthalten"}},map_modes:{invalid:"Fehler in der Konfiguration: map_modes",icon:{missing:"Fehlendes Symbol für den Kartenmodus"},name:{missing:"Fehlender Name für den Kartenmodus"},template:{invalid:"Ungültige Vorlage: {0}"},predefined_selections:{not_applicable:"Modus {0} unterstützt keine vordefinierte Auswahl",zones:{missing:"Fehlende Zonenkonfiguration",invalid_parameters_number:"Jede Zone muss 4 Parameter haben"},points:{position:{missing:"Konfiguration der fehlenden Punkte",invalid_parameters_number:"Jeder Punkt muss 2 Parameter haben"}},rooms:{id:{missing:"Fehlende Raum ID",invalid_format:"Ungültige Raum ID: {0}"},outline:{invalid_parameters_number:"Jeder Punkt des Raumes muss 2 Parameter haben."}},label:{x:{missing:"Das Label muss die Eigenschaft x haben"},y:{missing:"Das Label muss die Eigenschaft y haben"},text:{missing:"Das Label muss eine Text-Eigenschaft haben"}},icon:{x:{missing:"Das Icon muss die Eigenschaft x haben"},y:{missing:"Das Icon muss die Eigenschaft y haben"},name:{missing:"Das Icon muss eine Text-Eigenschaft haben"}}},service_call_schema:{missing:"Fehlendes Schema des Service-Aufrufs",service:{missing:"Schema des Service-Aufrufs muss Dienst enthalten",invalid:"Ungültiger Service: {0}"}}}},invalid_entities:"Ungültige Entitäten:",invalid_calibration:"Ungültige Kalibrierung, bitte überprüfen Sie Ihre Konfiguration"},Fe={status:"Status",battery_level:"Batterie",fan_speed:"Lüftergeschwindigkeit",sensor_dirty_left:"Sensoren verbleibend",filter_left:"Filter verbleibend",main_brush_left:"Hauptbürste verbleibend",side_brush_left:"Seitenbürste verbleibend",cleaning_count:"Anzahl der Reinigungen",cleaned_area:"Gereinigte Fläche",cleaning_time:"Zeit der Reinigung"},Ve={vacuum_start:"Start",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Rückkehr zur Basis",vacuum_clean_spot:"Reinige Stelle",vacuum_locate:"Finden",vacuum_set_fan_speed:"Lüftergeschwindigkeit ändern"},Ue={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Xe={success:"Erfolg!",no_selection:"Keine Auswahl vorgesehen",failed:"Der Dienst konnte nicht aufgerufen werden"},He={description:{before_link:"Dieser visuelle Editor unterstützt nur eine einfache Konfiguration mit einer Kameraeinheit, die mit ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Für erweiterte Einstellungen verwenden Sie den YAML-Modus."},label:{name:"Titel (optional)",entity:"Staubsauger Entität (required)",camera:"Kamera Entität (required)",vacuum_platform:"Staubsauger-Plattform (required)",map_locked:"Karte gesperrt (optional)",two_finger_pan:"Zwei-Finger-Pan (optional)"}},qe={common:je,map_mode:Ie,validation:De,label:Fe,icon:Ve,unit:Ue,popups:Xe,editor:He},Ze={version:"Version",invalid_configuration:"Invalid configuration {0}",description:"A card that lets you control your vacuum",old_configuration:"Old configuration detected. Adjust your config to the latest schema or create a new card from the scratch.",old_configuration_migration_link:"Migration guide"},Ke={invalid:"Invalid template!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Points",vacuum_clean_segment:"Rooms",vacuum_clean_point:"Clean point",vacuum_clean_point_predefined:"Points",vacuum_clean_zone:"Zone cleanup",vacuum_clean_zone_predefined:"Zones list",vacuum_follow_path:"Path"},Be={preset:{entity:{missing:"Missing property: entity"},preset_name:{missing:"Missing property: preset_name"},platform:{invalid:"Invalid vacuum platform: {0}"},map_source:{missing:"Missing property: map_source",none_provided:"No camera neither image provided",ambiguous:"Only one map source allowed"},calibration_source:{missing:"Missing property: calibration_source",ambiguous:"Only one calibration source allowed",none_provided:"No calibration source provided",calibration_points:{invalid_number:"Exactly 3 or 4 calibration points required",missing_map:"Each calibration point must contain map coordinates",missing_vacuum:"Each calibration point must contain vacuum coordinates",missing_coordinate:"Map and vacuum calibration points must contain both x and y coordinate"}},icons:{invalid:"Error in configuration: icons",icon:{missing:"Each entry of icons list must contain icon property"}},tiles:{invalid:"Error in configuration: tiles",entity:{missing:"Each entry of tiles list must contain entity"},label:{missing:"Each entry of tiles list must contain label"}},map_modes:{invalid:"Error in configuration: map_modes",icon:{missing:"Missing icon of map mode"},name:{missing:"Missing name of map mode"},template:{invalid:"Invalid template: {0}"},predefined_selections:{not_applicable:"Mode {0} does not support predefined selections",zones:{missing:"Missing zones configuration",invalid_parameters_number:"Each zone must have 4 parameters"},points:{position:{missing:"Missing points configuration",invalid_parameters_number:"Each point must have 2 parameters"}},rooms:{id:{missing:"Missing room id",invalid_format:"Invalid room id: {0}"},outline:{invalid_parameters_number:"Each point of room outline must have 2 parameters"}},label:{x:{missing:"Label must have x property"},y:{missing:"Label must have y property"},text:{missing:"Label must have text property"}},icon:{x:{missing:"Icon must have x property"},y:{missing:"Icon must have y property"},name:{missing:"Icon must have name property"}}},service_call_schema:{missing:"Missing service call schema",service:{missing:"Service call schema must contain service",invalid:"Invalid service: {0}"}}}},invalid_entities:"Invalid entities:",invalid_calibration:"Invalid calibration, please check your configuration"},Ge={status:"Status",battery_level:"Battery",fan_speed:"Fan speed",sensor_dirty_left:"Sensors left",filter_left:"Filter left",main_brush_left:"Main brush left",side_brush_left:"Side brush left",cleaning_count:"Cleaning count",cleaned_area:"Cleaned area",cleaning_time:"Cleaning time",mop_left:"Mop left"},We={vacuum_start:"Start",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Return to base",vacuum_clean_spot:"Clean spot",vacuum_locate:"Locate",vacuum_set_fan_speed:"Change fan speed"},Ye={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Je={success:"Success!",no_selection:"No selection provided",failed:"Failed to call service"},Qe={description:{before_link:"This visual editor supports only a basic configuration with a camera entity created using ",link_text:"Xiaomi Cloud Map Extractor",after_link:". For more advanced setup use YAML mode."},label:{name:"Title (optional)",entity:"Vacuum entity (required)",camera:"Camera entity (required)",vacuum_platform:"Vacuum platform (required)",map_locked:"Map locked (optional)",two_finger_pan:"Two finger pan (optional)"}},et={common:Ze,map_mode:Ke,validation:Be,label:Ge,icon:We,unit:Ye,popups:Je,editor:Qe},tt={version:"Version",invalid_configuration:"Configuración inválida {0}",description:"Una tarjeta para controlar tu aspiradora",old_configuration:"Configuración antigua detectada. Ajusta la configuración al formato actual o crea una nueva tarjeta.",old_configuration_migration_link:"Guía de migrado."},it={invalid:"Plantilla inválida!",vacuum_goto:"Marcar e ir",vacuum_goto_predefined:"Puntos",vacuum_clean_segment:"Habitaciones",vacuum_clean_zone:"Limpiar área",vacuum_clean_zone_predefined:"Limpiar zonas",vacuum_follow_path:"Ruta"},at={preset:{entity:{missing:"Propiedad no encontrada: entity"},preset_name:{missing:"Propiedad no encontrada: preset_name"},platform:{invalid:"Plataforma de aspiradora inválida: {0}"},map_source:{missing:"Propiedad no encontrada: map_source",none_provided:"Sin cámara ni imagen proporcionada",ambiguous:"Solo se permite una fuente de mapa"},calibration_source:{missing:"Propiedad no encontrada: calibration_source",ambiguous:"Solo se permite una fuente de calibración",none_provided:"No se proporciona fuente de calibración",calibration_points:{invalid_number:"Se requieren 3 o 4 puntos de calibración",missing_map:"Cada punto de calibración debe contener las coordenadas del mapa",missing_vacuum:"Cada punto de calibración debe contener las coordenadas de la aspiradora",missing_coordinate:"Los puntos de calibración de la aspiradora y del mapa deben contener las coordenadas x e y"}},icons:{invalid:"Error en la configuración: icons",icon:{missing:"Cada entrada de la lista de iconos debe contener la propiedad del icono."}},tiles:{invalid:"Error en la configuración: tiles",entity:{missing:"Cada entrada de la lista de mosaicos debe contener la entidad."},label:{missing:"Cada entrada de la lista de mosaicos debe contener una etiqueta."}},map_modes:{invalid:"Error en la configuración: map_modes",icon:{missing:"Falta el icono del modo de mapa"},name:{missing:"Falta el nombre del modo de mapa"},template:{invalid:"Plantilla inválida: {0}"},predefined_selections:{not_applicable:"El modo {0} no admite selecciones predefinidas",zones:{missing:"Faltan configuraciones de zonas",invalid_parameters_number:"Cada zona debe tener 4 parámetros"},points:{position:{missing:"Faltan configuraciones de puntos",invalid_parameters_number:"Cada punto debe tener 2 parámetros"}},rooms:{id:{missing:"Falta la identificación de la habitación",invalid_format:"Identificación de la habitación inválida: {0}"},outline:{invalid_parameters_number:"Cada punto del contorno de la habitación debe tener 2 parámetros"}},label:{x:{missing:"La etiqueta debe tener la propiedad x"},y:{missing:"La etiqueta debe tener la propiedad y"},text:{missing:"La etiqueta debe tener la propiedad text"}},icon:{x:{missing:"El ícono debe tener la propiedad x"},y:{missing:"El ícono debe tener la propiedad y"},name:{missing:"El ícono debe tener la propiedad name"}}},service_call_schema:{missing:"Falta un esquema de llamada de servicio",service:{missing:"El esquema de llamada de servicio debe contener service",invalid:"Servicio inválido: {0}"}}}},invalid_entities:"Entidades inválidas:",invalid_calibration:"Calibración inválida, verifique la configuración."},nt={status:"Estado",battery_level:"Batería",fan_speed:"Velocidad del ventilador",sensor_dirty_left:"Sensores",filter_left:"Filtro",main_brush_left:"Cepillo principal",side_brush_left:"Cepillo lateral",cleaning_count:"Contador de limpieza",cleaned_area:"Área limpia",cleaning_time:"Tiempo de limpieza"},rt={vacuum_start:"Comenzar",vacuum_pause:"Pausar",vacuum_stop:"Detener",vacuum_return_to_base:"Volver a la base",vacuum_clean_spot:"Punto limpio",vacuum_locate:"Localizar",vacuum_set_fan_speed:"Cambiar la velocidad del ventilador"},ot={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},st={success:"Listo!",no_selection:"No se ha proporcionado ninguna selección",failed:"No se pudo llamar al servicio"},lt={description:{before_link:"Este editor visual solo admite una configuración básica con una entidad de cámara creada utilizando ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Para una configuración más avanzada, utilice el modo YAML."},label:{name:"Título (opcional)",entity:"Entidad de la aspiradora (requerido)",camera:"Entidad de la cámara (requerido)",vacuum_platform:"Plataforma de la aspiradora (requerido)",map_locked:"Bloquear mapa (opcional)",two_finger_pan:"Mover con dos dedos (opcional)"}},ct={common:tt,map_mode:it,validation:at,label:nt,icon:rt,unit:ot,popups:st,editor:lt},dt={version:"Version",invalid_configuration:"Configuration invalide {0}",description:"Une carte qui vous permet de contrôler votre robot aspirateur",old_configuration:"Ancienne configuration détectée. Ajustez votre configuration à la nouvelle version ou récréez totalement une nouvelle carte.",old_configuration_migration_link:"Guide de migration"},ut={invalid:"Template incorrect !",vacuum_goto:"Cible",vacuum_goto_predefined:"Points",vacuum_clean_segment:"Pièces",vacuum_clean_zone:"Nettoyage de zone",vacuum_clean_zone_predefined:"Liste des zones",vacuum_follow_path:"Chemin"},mt={preset:{entity:{missing:"Paramètre manquant : entity"},preset_name:{missing:"Paramètre manquant : preset_name"},platform:{invalid:"Plateforme incorrecte : {0}"},map_source:{missing:"Paramètre manquant : map_source",none_provided:"Aucune caméra ou image fournie",ambiguous:"Une seule source de carte autorisée"},calibration_source:{missing:"Paramètre manquant : calibration_source",ambiguous:"Une seule source de calibration autorisée",none_provided:"Aucune source de calibration fournie",calibration_points:{invalid_number:"3 ou 4 points de calibration sont nécessaires",missing_map:"Chaque point de calibration doit avoir des coordonnées de carte",missing_vacuum:"Chaque point de calibration doit avoir des coordonnées de robot",missing_coordinate:"Tous les points de calibration doivent avoir des coordonnées x et y"}},icons:{invalid:"Erreur de configuration : icônes",icon:{missing:"Chaque élément de la liste d'icônes doit avoir une propriété « icon »"}},tiles:{invalid:"Erreur de configuration : tuiles",entity:{missing:"Chaque élément de la liste de tuiles doit avoir une propriété « entity »"},label:{missing:"Chaque élément de la liste de tuiles doit avoir une propriété « label »"}},map_modes:{invalid:"Erreur de configuration : modes de carte",icon:{missing:"Icône de mode de carte manquante"},name:{missing:"Nom de mode de carte manquant"},template:{invalid:"Template incorrect : {0}"},predefined_selections:{not_applicable:"Ce mode {0} ne supporte pas les sélections prédéfinies",zones:{missing:"Configuration des zones manquante",invalid_parameters_number:"Chaque zone doit avoir 4 paramètres"},points:{position:{missing:"Configuration des points manquante",invalid_parameters_number:"Chaque point doit avoir 2 paramètres"}},rooms:{id:{missing:"id de pièce manquant",invalid_format:"id de pièce incorrect : {0}"},outline:{invalid_parameters_number:"Chaque point de contour de pièce doit avoir 2 paramètres"}},label:{x:{missing:"L'étiquette doit avoir une propriété « x »"},y:{missing:"L'étiquette doit avoir une propriété « y »"},text:{missing:"L'étiquette doit avoir une propriété « text »"}},icon:{x:{missing:"L'icône doit avoir une propriété x property"},y:{missing:"L'icône doit avoir une propriété y property"},name:{missing:"L'icône doit avoir une propriété « name »"}}},service_call_schema:{missing:"Missing service call schema",service:{missing:"Service call schema must contain service",invalid:"Invalid service: {0}"}}}},invalid_entities:"Entités incorrectes :",invalid_calibration:"Calibration incorrecte, vérifiez votre configuration"},pt={status:"Statut",battery_level:"Batterie",fan_speed:"Puissance",sensor_dirty_left:"Capteurs",filter_left:"Filtre",main_brush_left:"Brosse princ.",side_brush_left:"Brosse lat.",cleaning_count:"Nbr de nettoyages",cleaned_area:"Surface nettoyée",cleaning_time:"Temps de nettoyage"},_t={vacuum_start:"Démarrage",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Retour à la base",vacuum_clean_spot:"Nettoyage ciblé",vacuum_locate:"Localiser",vacuum_set_fan_speed:"Changer la puissance d'aspiration"},ht={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},vt={success:"Réussi !",no_selection:"Aucune sélection fournie",failed:"L'appel du service a échoué"},gt={description:{before_link:"L'éditeur visuel permet seulement une configuration de base avec une entité caméra créée avec ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Pour une configuration plus avancée, utilisez le mode YAML."},label:{name:"Titre (optionnel)",entity:"Entité du robot (obligatoire)",camera:"Entité de la caméra (obligatoire)",vacuum_platform:"Platforme (obligatoire)",map_locked:"Verrouiller la carte (optionnel)",two_finger_pan:"Défilement à deux doigts (optionnel)"}},ft={common:dt,map_mode:ut,validation:mt,label:pt,icon:_t,unit:ht,popups:vt,editor:gt},bt={version:"גירסה",invalid_configuration:"תצורה לא חוקית {0}",description:"כרטיס המאפשר לך לשלוט בשואב שלך",old_configuration:"זוהתה תצורה ישנה. התאם את התצורה שלך לסכמה העדכנית ביותר או צור כרטיס חדש מההתחלה.",old_configuration_migration_link:"מדריך להגירה"},yt={invalid:"תבנית לא חוקית!",vacuum_goto:"נעץ וסע",vacuum_goto_predefined:"נקודות",vacuum_clean_segment:"חדרים",vacuum_clean_point:"נקה נקודה",vacuum_clean_point_predefined:"נקודות",vacuum_clean_zone:"ניקוי אזור",vacuum_clean_zone_predefined:"רשימת אזורים",vacuum_follow_path:"נתיב"},xt={preset:{entity:{missing:"נכס חסר: ישות"},preset_name:{missing:"חסר מאפיין: preset_name"},platform:{invalid:"פלטפורמת שואב לא חוקית: {0}"},map_source:{missing:"נכס חסר: map_source",none_provided:"לא סופקה אף תמונה",ambiguous:"מותר רק מקור מפה אחד"},calibration_source:{missing:"חסר מאפיין: calibration_source",ambiguous:"מותר רק מקור כיול אחד",none_provided:"לא סופק מקור כיול",calibration_points:{invalid_number:"דרושות בדיוק 3 או 4 נקודות כיול",missing_map:"כל נקודת כיול חייבת להכיל קואורדינטות מפה",missing_vacuum:"כל נקודת כיול חייבת להכיל קואורדינטות שואב",missing_coordinate:"נקודות כיול במפה ובשואב חייבות להכיל גם קואורדינטות x וגם y"}},icons:{invalid:"שגיאה בתצורה: סמלילים",icon:{missing:"כל כניסה של רשימת הסמלילים חייבת להכיל מאפיין סמליל"}},tiles:{invalid:"שגיאה בתצורה: אריחים",entity:{missing:"כל ערך של רשימת אריחים חייב להכיל ישות"},label:{missing:"כל כניסה של רשימת אריחים חייבת להכיל תווית"}},map_modes:{invalid:"שגיאה בתצורה: map_modes",icon:{missing:"חסר סמליל של מצב מפה"},name:{missing:"חסר שם של מצב מפה"},template:{invalid:"תבנית לא חוקית: {0}"},predefined_selections:{not_applicable:"מצב {0} אינו תומך בבחירות מוגדרות מראש",zones:{missing:"תצורת אזורים חסרים",invalid_parameters_number:"כל אזור חייב לכלול 4 פרמטרים"},points:{position:{missing:"תצורת נקודות חסרות",invalid_parameters_number:"לכל נקודה חייבת להיות 2 פרמטרים"}},rooms:{id:{missing:"מזהה חדר חסר",invalid_format:"מזהה חדר לא חוקי: {0}"},outline:{invalid_parameters_number:"כל נקודה של מתאר החדר חייבת להיות בעלת 2 פרמטרים"}},label:{x:{missing:"חייב להיות מאפיין x לתבנית"},y:{missing:"חייב להיות מאפיין y לתבנית"},text:{missing:"חייב להיות מאפיין שם לתבנית"}},icon:{x:{missing:"חייב להיות מאפיין x לסמליל"},y:{missing:"חייב להיות מאפיין y לסמליל"},name:{missing:"חייב להיות מאפיין שם לסמליל"}}},service_call_schema:{missing:"סכימת קריאת שירות חסרה",service:{missing:"סכימת קריאת השירות חייבת להכיל שירות",invalid:"שירות לא חוקי: {0}"}}}},invalid_entities:"ישויות לא חוקיות:",invalid_calibration:"כיול לא חוקי, אנא בדוק את התצורה שלך"},kt={status:"סטטוס",battery_level:"סוללה",fan_speed:"מהירות מאוורר",sensor_dirty_left:"נותר לחיישנים",filter_left:"נותר למסנן",main_brush_left:"נותר למברשת ראשית",side_brush_left:"נותר למרשת צד",cleaning_count:"כמות נקיונות",cleaned_area:"שטח שנוקה",cleaning_time:"זמן ניקיון",mop_left:"נותר למטלית"},At={vacuum_start:"התחל",vacuum_pause:"השהה",vacuum_stop:"עצור",vacuum_return_to_base:"חזור לתחנת עגינה",vacuum_clean_spot:"ניקוי נקודה",vacuum_locate:"אתר",vacuum_set_fan_speed:"שנה מהירות מאוורר"},wt={hour_shortcut:"ש",meter_shortcut:"מ",meter_squared_shortcut:"m²",minute_shortcut:"דק"},Et={success:"הצליח!",no_selection:"לא סופקה בחירה",failed:"התקשרות לשירות נכשלה"},zt={description:{before_link:"עורך חזותי זה תומך רק בתצורה בסיסית עם ישות מצלמה שנוצרה באמצעות ",link_text:"Xiaomi Cloud Map Extractor",after_link:". להגדרה מתקדמת יותר השתמש במצב YAML."},label:{name:"כותרת (אופציונלי)",entity:"יישות שואב (נדרש)",camera:"יישות מצלמה (נדרש)",vacuum_platform:"פלטפורמת שואב (נדרש)",map_locked:"נעילת מפה (אופציונלי)",two_finger_pan:"צביטת שתי אצבעות (אופציונלי)"}},Pt={common:bt,map_mode:yt,validation:xt,label:kt,icon:At,unit:wt,popups:Et,editor:zt},St={version:"Verzió",invalid_configuration:"Érvénytelen konfiguráció {0}",description:"Egy kártya, amely lehetővé teszi a vákuum szabályozását",old_configuration:"Régi konfiguráció észlelve. Állítsa be a konfigurációt a legújabb sémához, vagy hozzon létre egy új kártyát.",old_configuration_migration_link:"Migrációs útmutató"},Mt={invalid:"Érvénytelen sablon!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Pontok",vacuum_clean_segment:"Szobák",vacuum_clean_zone:"Zóna takarítás",vacuum_clean_zone_predefined:"Zónák listája",vacuum_follow_path:"Pálya"},Tt={preset:{entity:{missing:"Hiányzó tulajdonság: entity"},preset_name:{missing:"Hiányzó tulajdonság: preset_name"},platform:{invalid:"Érvénytelen vákuumplatform: {0}"},map_source:{missing:"Hiányzó tulajdonság: map_source",none_provided:"Nincs kamera és kép sem biztosított",ambiguous:"Csak egy térképforrás engedélyezett"},calibration_source:{missing:"Hiányzó tulajdonság: calibration_source",ambiguous:"Csak egy kalibrációs forrás engedélyezett",none_provided:"incs megadva kalibrációs forrás",calibration_points:{invalid_number:"Pontosan 3 vagy 4 kalibrációs pont szükséges",missing_map:"Minden kalibrációs pontnak tartalmaznia kell a térkép koordinátáit",missing_vacuum:"Minden kalibrációs pontnak vákuumkoordinátákat kell tartalmaznia",missing_coordinate:"A térképi és vákuumkalibrációs pontoknak x és y koordinátát is tartalmazniuk kell"}},icons:{invalid:"Hiba a konfigurációban: icons",icon:{missing:"Az ikonlista minden bejegyzésének tartalmaznia kell az ikon tulajdonságot"}},tiles:{invalid:"Hiba a konfigurációban: tiles",entity:{missing:"A csempelista minden bejegyzésének tartalmaznia kell entitást"},label:{missing:"A csempelista minden bejegyzésének tartalmaznia kell egy címkét"}},map_modes:{invalid:"Hiba a konfigurációban: map_modes",icon:{missing:"Hiányzik a térkép mód ikonja"},name:{missing:"A térképmód neve hiányzik"},template:{invalid:"Érvénytelen sablon: {0}"},predefined_selections:{not_applicable:"A(z) {0} mód nem támogatja az előre meghatározott kijelöléseket",zones:{missing:"Hiányzó zónák konfigurációja",invalid_parameters_number:"Minden zónának 4 paraméterrel kell rendelkeznie"},points:{position:{missing:"Hiányzó pontok konfigurációja",invalid_parameters_number:"Minden pontnak 2 paraméterrel kell rendelkeznie"}},rooms:{id:{missing:"Hiányzó room id",invalid_format:"Érvénytelen room id: {0}"},outline:{invalid_parameters_number:"A helyiség körvonalának minden pontján 2 paraméterrel kell rendelkeznie"}},label:{x:{missing:"A címkének x tulajdonsággal kell rendelkeznie"},y:{missing:"A címkének y tulajdonsággal kell rendelkeznie"},text:{missing:"A címkének szövegtulajdonsággal kell rendelkeznie"}},icon:{x:{missing:"Az ikonnak x tulajdonsággal kell rendelkeznie"},y:{missing:"Az ikonnak y tulajdonsággal kell rendelkeznie"},name:{missing:"Az ikonnak név tulajdonsággal kell rendelkeznie"}}},service_call_schema:{missing:"Hiányzó szolgáltatáshívási séma",service:{missing:"A szolgáltatáshívási sémának tartalmaznia kell a szolgáltatást",invalid:"Érvénytelen szolgáltatás: {0}"}}}},invalid_entities:"Érvénytelen entitások:",invalid_calibration:"Érvénytelen kalibráció, ellenőrizze a konfigurációt"},Ct={status:"Státusz",battery_level:"Akkumulátor",fan_speed:"Ventilátor sebesség",sensor_dirty_left:"Szenzorok",filter_left:"Szűrő",main_brush_left:"Fő kefe",side_brush_left:"Oldalkefe",cleaning_count:"Takarítás számláló",cleaned_area:"Tisztított terület",cleaning_time:"Takarítási idő"},Nt={vacuum_start:"Indítás",vacuum_pause:"Szünet",vacuum_stop:"Álljon meg",vacuum_return_to_base:"Vissza a bázisra",vacuum_clean_spot:"Clean spot",vacuum_locate:"Helymeghatározás",vacuum_set_fan_speed:"Ventilátor sebesség módosítása"},Rt={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Lt={success:"Siker!",no_selection:"Nincs kiválasztva",failed:"Nem sikerült meghívni a szolgáltatást"},Ot={description:{before_link:"Ez a vizuális szerkesztő csak az alapkonfigurációt támogatja a segítségével létrehozott kameraentitással ",link_text:"Xiaomi Cloud Map Extractor",after_link:". A fejlettebb beállításhoz használja a YAML módot."},label:{name:"Cím (nem kötelező)",entity:"Vákuum entitás (kötelező)",camera:"Kamera entitás (kötelező)",vacuum_platform:"Vákuumos platform (szükséges)",map_locked:"Térkép zárolva (opcionális)",two_finger_pan:"Kétujjas pásztázás (opcionális)"}},$t={common:St,map_mode:Mt,validation:Tt,label:Ct,icon:Nt,unit:Rt,popups:Lt,editor:Ot},jt={version:"Versione",invalid_configuration:"Configurazione non valida {0}",description:"Una card per controllare il tuo robot aspirapolvere",old_configuration:"Trovata una vecchia configurazione. Correggi la configurazione all'ultima possibile o crea una nuova card.",old_configuration_migration_link:"Guida Migrazione"},It={invalid:"Template non valido!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Punti",vacuum_clean_segment:"Stanze",vacuum_clean_zone:"Pulizia a Zone",vacuum_clean_zone_predefined:"Lista Zone",vacuum_follow_path:"Percorso"},Dt={preset:{entity:{missing:"Proprietà Mancante: entity"},preset_name:{missing:"Proprietà Mancante: preset_name"},platform:{invalid:"Piattaforma aspirapolvere non valida: {0}"},map_source:{missing:"Proprietà Mancante: map_source",none_provided:"Inserire camera o immagine",ambiguous:"È consentita una sola sorgente della mappa"},calibration_source:{missing:"Proprietà Mancante: calibration_source",ambiguous:"È consentita una solo una sorgente di calibrazione",none_provided:"Nessuna fonte di calibrazione fornita",calibration_points:{invalid_number:"Esattamente 3 o 4 punti di calibrazione richiesti",missing_map:"Ogni punto di calibrazione deve contenere le coordinate della mappa",missing_vacuum:"Ciascun punto di calibrazione deve contenere le coordinate dell'aspirapolvere",missing_coordinate:"I punti di calibrazione della mappa e dell'aspirapolvere devono contenere sia le coordinate x che y"}},icons:{invalid:"Errore nella configurazione: icons",icon:{missing:"Ogni voce dell'elenco delle icone deve contenere la proprietà dell'icona"}},tiles:{invalid:"Errore nella configurazione: tiles",entity:{missing:"Ogni voce dell'elenco 'tile' deve contenere una entity"},label:{missing:"Ogni voce dell'elenco 'tile' deve contenere una label"}},map_modes:{invalid:"Errore nella configurazione: map_modes",icon:{missing:"Icona della modalità mappa mancante"},name:{missing:"Nome della modalità mappa mancante"},template:{invalid:"Template non valido: {0}"},predefined_selections:{not_applicable:"Modalità {0} non supporta le selezioni predefinite",zones:{missing:"Configurazione zone mancante",invalid_parameters_number:"Ogni zona deve avere 4 parametri"},points:{position:{missing:"Configurazione punti mancante",invalid_parameters_number:"Ogni punto deve avere 2 parametri"}},rooms:{id:{missing:"ID stanza mancante",invalid_format:"ID stanza non valido: {0}"},outline:{invalid_parameters_number:"Ogni punto del contorno della stanza deve avere 2 parametri"}},label:{x:{missing:"Label deve avere la proprietà x"},y:{missing:"Label deve avere la proprietà y"},text:{missing:"Label deve avere la proprietà text"}},icon:{x:{missing:"Icon deve avere la proprietà x"},y:{missing:"Icon deve avere la proprietà y"},name:{missing:"Icon deve avere la proprietà name"}}},service_call_schema:{missing:"Schema della chiamata al servizio mancante",service:{missing:"La chiamata al servizio deve contenere un servizio",invalid:"Servizio non valido: {0}"}}}},invalid_entities:"Entità non valide:",invalid_calibration:"Calibrazione non valida, per favore controlla la configurazione"},Ft={status:"Stato",battery_level:"Batteria",fan_speed:"Velocità Ventola",sensor_dirty_left:"Sensori",filter_left:"Filtro",main_brush_left:"Spazzola Principale",side_brush_left:"Spazzola laterale",cleaning_count:"Conteggio pulizia",cleaned_area:"Area pulita",cleaning_time:"Tempo di pulizia"},Vt={vacuum_start:"Avvia",vacuum_pause:"Pausa",vacuum_stop:"Stop",vacuum_return_to_base:"Ritorna alla base",vacuum_clean_spot:"Pulizia spot",vacuum_locate:"Localizza",vacuum_set_fan_speed:"Cambia velocità ventola"},Ut={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Xt={success:"Confermato!",no_selection:"Nessuna Selezione",failed:"Chiamata al servizio fallita"},Ht={description:{before_link:"Questo editor visivo supporta solo una configurazione di base con un'entità telecamera creata utilizzando ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Per una configurazione più avanzata usa la modalità YAML."},label:{name:"Titolo (opzionale)",entity:"Entità Aspirapolvere (obbligatorio)",camera:"Entità camera (obbligatorio)",vacuum_platform:"Piattaforma aspirapolvere (obbligatorio)",map_locked:"Blocco mappa (opzionale)",two_finger_pan:"Zoom a due dita (opzionale)"}},qt={common:jt,map_mode:It,validation:Dt,label:Ft,icon:Vt,unit:Ut,popups:Xt,editor:Ht},Zt={version:"Versie",invalid_configuration:"Ongeldige configuratie {0}",description:"Een kaart waarmee je jouw robotstofzuiger kunt bedienen.",old_configuration:"Oude configuratie gevonden. Pas je configuratie aan op basis van de nieuwe versie of maak een volledig nieuwe kaart.",old_configuration_migration_link:"Uitleg configuratie aanpassen"},Kt={invalid:"Ongeldig sjabloon!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Punten",vacuum_clean_segment:"Kamers",vacuum_clean_zone:"Zone schoonmaak",vacuum_clean_zone_predefined:"Zone lijst",vacuum_follow_path:"Pad"},Bt={preset:{entity:{missing:"Ontbrekende parameter: entity"},preset_name:{missing:"Ontbrekende parameter: preset_name"},platform:{invalid:"Ongeldig stofzuigerplatform: {0}"},map_source:{missing:"Ontbrekende parameter: map_source",none_provided:"Geen camera of afbeelding opgegeven",ambiguous:"Slechts één kaartbron toegestaan"},calibration_source:{missing:"Ontbrekende parameter: calibration_source",ambiguous:"Slechts één kalibratiebron toegestaan",none_provided:"Geen kalibratiebron opgegeven",calibration_points:{invalid_number:"Precies 3 of 4 kalibratiepunten vereist",missing_map:"Elk kalibratiepunt moet kaart coördinaten bevatten",missing_vacuum:"Elk kalibratiepunt moet stofzuiger coördinaten bevatten",missing_coordinate:"Kaart en stofzuiger kalibratiepunten moeten zowel een x als y coödinaat bevatten"}},icons:{invalid:"Fout in configuratie: icons",icon:{missing:"Elk item in de lijst moet de eigenschap « icon » bevatten"}},tiles:{invalid:"Fout in configuratie: tiles",entity:{missing:"Elk item in de lijst moet de eigenschap « entity » bevatten"},label:{missing:"Elk item in de lijst moet de eigenschap « label » bevatten"}},map_modes:{invalid:"Fout in configuratie: map_modes",icon:{missing:"Pictogram van kaartmodus ontbreekt"},name:{missing:"Naam van kaartmodus ontbreekt"},template:{invalid:"Ongeldig sjabloon: {0}"},predefined_selections:{not_applicable:"Modus {0} ondersteunt geen vooraf gedefinieerde selecties",zones:{missing:"Zone configuratie ontbreekt",invalid_parameters_number:"Elke zone moet 4 coördinaten hebben"},points:{position:{missing:"Punten configuratie ontbreekt",invalid_parameters_number:"Elk punt moet 2 coördinaten hebben"}},rooms:{id:{missing:"Kamer id ontbreekt",invalid_format:"Ongeldige kamer id: {0}"},outline:{invalid_parameters_number:"Elk punt van de kamer omtrek moet 2 coördinaten hebben"}},label:{x:{missing:"Elk label moet de eigenschap « x » bevatten"},y:{missing:"Elk label moet de eigenschap « y » bevatten"},text:{missing:"Elk label moet de eigenschap « text » bevatten"}},icon:{x:{missing:"Elk pictogram moet de eigenschap « x » bevatten"},y:{missing:"Elk pictogram moet de eigenschap « y » bevatten"},name:{missing:"Elk pictogram moet de eigenschap « name » bevatten"}}},service_call_schema:{missing:"Serviceoproep schema",service:{missing:"Serviceoproep schema moet een service bevatten",invalid:"Ongeldige service: {0}"}}}},invalid_entities:"Ongeldige entiteiten:",invalid_calibration:"Ongeldige kalibratie, controleer je configuratie"},Gt={status:"Status",battery_level:"Batterij",fan_speed:"Fan snelheid",sensor_dirty_left:"Sensors",filter_left:"Filter",main_brush_left:"Hoofdborstel",side_brush_left:"Zijborstel",cleaning_count:"Schoonmaakteller",cleaned_area:"Oppervlakte",cleaning_time:"Schoonmaaktijd"},Wt={vacuum_start:"Start",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Terug naar basisstation",vacuum_clean_spot:"Spot schoonmaak",vacuum_locate:"Lokaliseren",vacuum_set_fan_speed:"Fan snelheid aanpassen"},Yt={hour_shortcut:"u",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Jt={success:"Succes!",no_selection:"Geen selectie opgegeven",failed:"Fout bij aanroepen service"},Qt={description:{before_link:"Deze grafische editor ondersteunt slechts een basis configuratie met een camera entiteit welke gemaakt is met ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Gebruik de YAML modus voor een geavanceerde configuratie."},label:{name:"Titel (optioneel)",entity:"Stofzuiger entiteit (verplicht)",camera:"Camera entiteit (verplicht)",vacuum_platform:"stofzuigerplatform (verplicht)",map_locked:"Kaart vergrendelen (optioneel)",two_finger_pan:"Kaart verplaatsen met twee vingers (optioneel)"}},ei={common:Zt,map_mode:Kt,validation:Bt,label:Gt,icon:Wt,unit:Yt,popups:Jt,editor:Qt},ti={version:"Wersja",invalid_configuration:"Nieprawidłowa konfiguracja {0}",description:"Karta pozwalająca na kontrolowanie odkurzacza",old_configuration:"Wykryto starą wersję konfiguracji. Dostosuj kartę do najnowszej wersji, albo utwórz ją od nowa.",old_configuration_migration_link:"Przewodnik po migracji"},ii={invalid:"Nieprawidłowa wartość template",vacuum_goto:"Idź do punktu",vacuum_goto_predefined:"Zapisane punkty",vacuum_clean_segment:"Pokoje",vacuum_clean_point:"Sprzątanie punktowe",vacuum_clean_point_predefined:"Zapisane punkty",vacuum_clean_zone:"Sprzątanie strefowe",vacuum_clean_zone_predefined:"Zapisane strefy",vacuum_follow_path:"Ścieżka"},ai={preset:{entity:{missing:"Brakujący parametr: entity"},preset_name:{missing:"Brakujący parametr: preset_name"},platform:{invalid:"Nieprawidłowa platforma odkurzacza: {0}"},map_source:{missing:"Brakujący parametr: map_source",none_provided:"Nie podano źródła mapy",ambiguous:"Można podać tylko jedno źródło mapy"},calibration_source:{missing:"Brakujący parametr: calibration_source",ambiguous:"Można podać tylko jedno źródło kalibracji",none_provided:"Nie podano źródła kalibracji",calibration_points:{invalid_number:"Wymagane 3 bądź 4 punkty kalibracyjne",missing_map:"Każdy punkt kalibracyjny musi posiadać współrzędne na mapie",missing_vacuum:"Każdy punkt kalibracyjny musi posiadać współrzędne w układzie odkurzacza",missing_coordinate:"Każdy punkt kalibracyjny musi mieć współrzędne x i y"}},icons:{invalid:"Błąd w konfiguracji: icons",icon:{missing:'Każda pozycja na liście ikon musi posiadać parametr "icon"'}},tiles:{invalid:"Błąd w konfiguracji: tiles",entity:{missing:'Każda pozycja na liście kafelków musi posiadać parametr "entity"'},label:{missing:'Każda pozycja na liście kafelków musi posiadać parametr "label"'}},map_modes:{invalid:"Błąd w konfiguracji: map_modes",icon:{missing:"Brakująca ikona szablonu trybu mapy"},name:{missing:"Brakująca nazwa szablonu trybu mapy"},template:{invalid:"Nieprawidłowy szablon trybu mapy: {0}"},predefined_selections:{not_applicable:"Szablon {0} nie wspiera zapisywania zaznaczeń",zones:{missing:"Brakująca lista zapisanych stref",invalid_parameters_number:"Każda zapisana strefa musi posiadać 4 współrzędne"},points:{position:{missing:"Brakująca lista zapisanych punktów",invalid_parameters_number:"Każdy zapisany punkt musi posiadać 2 współrzędne"}},rooms:{id:{missing:"Brakujący identyfikator pokoju",invalid_format:"Nieprawidłowy identyfikator pokoju: {0}"},outline:{invalid_parameters_number:"Każdy punkt obrysu pokoju musi posiadać 2 współrzędne"}},label:{x:{missing:"Każda etykieta musi posiadać współrzędną x"},y:{missing:"Każda etykieta musi posiadać współrzędną y"},text:{missing:"Każda etykieta musi posiadać tekst"}},icon:{x:{missing:"Każda ikona musi posiadać współrzędną x"},y:{missing:"Każda ikona musi posiadać współrzędną y"},name:{missing:'Każda ikona musi posiadać parametr "name"'}}},service_call_schema:{missing:"Brakujący schemat wywołania usługi",service:{missing:"Każdy schemat usługi musi posiadać podaną nazwę usługi  ",invalid:"Nieprawidłowa usługa: {0}"}}}},invalid_entities:"Nieprawidłowe encje:",invalid_calibration:"Nieprawidłowa kalibracja, sprawdź konfigurację"},ni={status:"Status",battery_level:"Bateria",fan_speed:"Moc",sensor_dirty_left:"Sensory",filter_left:"Filtr",main_brush_left:"Główna szczotka",side_brush_left:"Boczna szczotka",cleaning_count:"Licznik sprzątań",cleaned_area:"Powierzchnia",cleaning_time:"Czas sprzątania",mop_left:"Mop"},ri={vacuum_start:"Uruchom",vacuum_pause:"Wstrzymaj",vacuum_stop:"Zatrzymaj",vacuum_return_to_base:"Wróć do stacji dokującej",vacuum_clean_spot:"Wyczyść miejsce",vacuum_locate:"Zlokalizuj",vacuum_set_fan_speed:"Zmień prędkość wentylatora"},oi={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},si={success:"Usługa wywołana!",no_selection:"Nie wybrano zaznaczenia",failed:"Błąd wywołania usługi"},li={description:{before_link:"Ten edytor interfejsu wspiera jedynie podstawową konfigurację dla kamery utworzonej przy użyciu ",link_text:"Xiaomi Cloud Map Extractora",after_link:". W celu bardziej zaawansowanej konfiguracji użyj trybu YAML."},label:{name:"Tytuł (opcjonalny)",entity:"Encja odkurzacza (wymagana)",camera:"Kamera z mapą (wymagana)",vacuum_platform:"Platforma integracji odkurzacza (wymagana)",map_locked:"Blokada mapy (opcjonalna)",two_finger_pan:"Przesuwanie mapy dwoma palcami (opcjonalne)"}},ci={common:ti,map_mode:ii,validation:ai,label:ni,icon:ri,unit:oi,popups:si,editor:li},di={version:"Versão",invalid_configuration:"configuração inválida {0}",description:"Um cartão que permite que você controlar seu aspirador",old_configuration:"Configuração antiga detectada. Ajuste sua configuração para a versão mais recente ou crie um novo cartão do zero.",old_configuration_migration_link:"Guia de migração"},ui={invalid:"template inválido!",vacuum_goto:"Click & vai",vacuum_goto_predefined:"Local",vacuum_clean_segment:"Quartos",vacuum_clean_zone:"Limpar zona",vacuum_clean_zone_predefined:"Lista de zonas",vacuum_follow_path:"Seguir caminho"},mi={preset:{entity:{missing:"Propriedade ausente: entidade"},preset_name:{missing:"Propriedade ausente: preset_name"},platform:{invalid:"Plataforma de aspirador inválida: {0}"},map_source:{missing:"Propriedade ausente: map_source",none_provided:"Nenhuma câmera nem imagem fornecida",ambiguous:"Apenas uma fonte de mapa permitida"},calibration_source:{missing:"Propriedade ausente: calibration_source",ambiguous:"Apenas uma fonte de calibração permitida",none_provided:"Nenhuma fonte de calibração fornecida",calibration_points:{invalid_number:"Exatamente 3 ou 4 pontos de calibração são necessários",missing_map:"Cada ponto de calibração deve conter coordenadas do mapa",missing_vacuum:"Cada ponto de calibração deve conter coordenadas do aspirador",missing_coordinate:"Os pontos de calibração do mapa e do aspirador devem conter as coordenadas x e y"}},icons:{invalid:"Erro na configuração: icones",icon:{missing:"Cada entrada na lista de ícones deve conter a propriedade do ícone"}},tiles:{invalid:"Erro na configuração: tiles",entity:{missing:"Cada entrada da lista de tiles deve conter entidade"},label:{missing:"Cada entrada da lista de tiles deve conter label"}},map_modes:{invalid:"Erro na configuração: map_modes",icon:{missing:"Falta o ícone no modo de mapa"},name:{missing:"Falta o nome no modo de mapa"},template:{invalid:"Template inválido: {0}"},predefined_selections:{not_applicable:"O modo {0} não oferece suporte a seleções predefinidas",zones:{missing:"Falta a Configuração de zonas",invalid_parameters_number:"Cada zona deve ter 4 parâmetros"},points:{position:{missing:"Falta a configuração do local",invalid_parameters_number:"Cada local deve ter 2 parâmetros"}},rooms:{id:{missing:"Falta o id do quarto",invalid_format:"Id inválido do quarto: {0}"},outline:{invalid_parameters_number:"Cada local da borda do quarto deve ter 2 parâmetros"}},label:{x:{missing:"A label deve ter a propriedade x"},y:{missing:"A label deve ter a propriedade y"},text:{missing:"A label deve ter um texto"}},icon:{x:{missing:"O ícone deve ter a propriedade x"},y:{missing:"O ícone deve ter a propriedade y"},name:{missing:"O ícone deve ter um nome"}}},service_call_schema:{missing:"Falta o call service",service:{missing:"O call service deve conter o serviço",invalid:"serviço inválido: {0}"}}}},invalid_entities:"entidades inválidas:",invalid_calibration:"Calibração inválida, verifique sua configuração"},pi={status:"Status",battery_level:"Bateria",fan_speed:"Velocidade",sensor_dirty_left:"Sensores",filter_left:"Filtro",main_brush_left:"Escova principal",side_brush_left:"Escova lateral",cleaning_count:"Contagem de limpezas",cleaned_area:"Área limpa",cleaning_time:"Tempo de limpeza"},_i={vacuum_start:"Começar",vacuum_pause:"Pausar",vacuum_stop:"Parar",vacuum_return_to_base:"Voltar para a base",vacuum_clean_spot:"Limpar local",vacuum_locate:"Localizar",vacuum_set_fan_speed:"Mudar velocidade"},hi={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},vi={success:"Successo!",no_selection:"Nenhuma seleção fornecida",failed:"Falha em chamar o serviço"},gi={description:{before_link:"Este editor suporta apenas uma configuração básica usando uma entidade de câmera",link_text:"Xiaomi Cloud Map Extractor",after_link:". Para um setup avancado use o YAML mode."},label:{name:"Título (opicional)",entity:"Entidade do aspirador (Obrigatório)",camera:"Entidade da camera (Obrigatório)",vacuum_platform:"Plataforma do aspirador (Obrigatório)",map_locked:"Mapa travado (Opicional)",two_finger_pan:"Movimente com dois dedos (Opicional)"}},fi={common:di,map_mode:ui,validation:mi,label:pi,icon:_i,unit:hi,popups:vi,editor:gi},bi={version:"Версия",invalid_configuration:"Неверная конфигурация {0}",description:"Карточка, позволяющая управлять вашим пылесосом",old_configuration:"Обнаружена устаревшая конфигурация. Приведите ваш конфиг в соответствие с новой версией, или создайте новую карточку с нуля.",old_configuration_migration_link:"Руководство по переходу с предыдущих версий."},yi={invalid:"Неверный шаблон!",vacuum_goto:"Точка назначения",vacuum_goto_predefined:"Предустановленные точки",vacuum_clean_segment:"Комнаты",vacuum_clean_point:"Уборка точки",vacuum_clean_point_predefined:"Список точек",vacuum_clean_zone:"Уборка зоны",vacuum_clean_zone_predefined:"Список зон",vacuum_follow_path:"Путь"},xi={preset:{entity:{missing:"Не указано свойство: entity"},preset_name:{missing:"Не указано свойство: preset_name"},platform:{invalid:"Неверная платформа: {0}"},map_source:{missing:"Не указано свойство: map_source",none_provided:"Не предоставлена ни камера ни изображение",ambiguous:"Допустим только один источник для карты"},calibration_source:{missing:"Не указано свойство: calibration_source",ambiguous:"Допустим только один источник для калибровки",none_provided:"Не предоставлен источник калибровки",calibration_points:{invalid_number:"Для калибровки требуется 3 или 4 точки",missing_map:"Каждая точка калибровки должна содержать координаты карты",missing_vacuum:"Каждая точка калибровки должна содержать координаты пылесоса",missing_coordinate:"Калибровочные точки карты и пылесоса должны содержать как x так и y координаты"}},icons:{invalid:"Ошибка в конфигурации: icons",icon:{missing:"Каждое вхождение в списке иконок должен содержать icon property"}},tiles:{invalid:"Ошибка в конфигурации: tiles",entity:{missing:"Каждое вхождение в списке плиток должно содержать entity"},label:{missing:"Каждое вхождение в списке плиток должно содержать label"}},map_modes:{invalid:"Ошибка в конфигурации: map_modes",icon:{missing:"Не указана иконка для влажной уборки"},name:{missing:"Не указано имя для влажной уборки"},template:{invalid:"Неверный шаблон: {0}"},predefined_selections:{not_applicable:"Режим {0} не поддерживает предустановленые элементы",zones:{missing:"Не указана конфигурация зоны",invalid_parameters_number:"Каждая зона должна содержать 4 параметра"},points:{position:{missing:"Не указана конфигурация для точек",invalid_parameters_number:"Каждая точка должна содержать 2 параметра"}},rooms:{id:{missing:"Не указан id комнаты",invalid_format:"Некорректный id комнаты: {0}"},outline:{invalid_parameters_number:"Каждая точка контура комнаты должна содержать 2 параметра"}},label:{x:{missing:"Ярлык должен содержать свойство x"},y:{missing:"Ярлык должен содержать свойство y"},text:{missing:"Ярлык должен содержать свойство text"}},icon:{x:{missing:"Иконка должна содержать свойство x"},y:{missing:"Иконка должна содержать свойство y"},name:{missing:"Иконка должна содержать свойство name"}}},service_call_schema:{missing:"Отсутствует схема вызова службы",service:{missing:"Схема вызова службы должна содержать service",invalid:"Некорректная служба: {0}"}}}},invalid_entities:"Некорректные сущности:",invalid_calibration:"Некорректная калибровка, проверьте вашу конфигурацию"},ki={status:"Статус",battery_level:"Уровень заряда",fan_speed:"Мощность всасывания",sensor_dirty_left:"Уровень загрязнения датчиков",filter_left:"Ресурс фильтра",main_brush_left:"Ресурс основной щётки",side_brush_left:"Ресурс боковой щётки",cleaning_count:"Число уборок",cleaned_area:"Площадь уборки",cleaning_time:"Время уборки",mop_left:"Ресурс тряпки"},Ai={vacuum_start:"Старт",vacuum_pause:"Пауза",vacuum_stop:"Стоп",vacuum_return_to_base:"Вернуть к базе",vacuum_clean_spot:"Убрать точку",vacuum_locate:"Обнаружить",vacuum_set_fan_speed:"Изменить мощность всасывания"},wi={hour_shortcut:"ч",meter_shortcut:"м",meter_squared_shortcut:"м²",minute_shortcut:"мин"},Ei={success:"Успех!",no_selection:"Ничего не выбрано",failed:"Не удалось вызвать службу"},zi={description:{before_link:"Данный редактор поддерживает только базовую конфигурацию с камерой, созданной посредством",link_text:"Xiaomi Cloud Map Extractor",after_link:". Для более тонкой настройки, используйте YAML-мод."},label:{name:"Заголовок (опционально)",entity:"Сущность пылесоса (обязательно)",camera:"Сущность камеры (обязательно)",vacuum_platform:"Платформа пылесоса (обязательно)",map_locked:"Блокировка карты (опционально)",two_finger_pan:"Перемещение жестом двумя пальцами (опционально)"}},Pi={common:bi,map_mode:yi,validation:xi,label:ki,icon:Ai,unit:wi,popups:Ei,editor:zi},Si={version:"Version",invalid_configuration:"Недійсна конфігурація {0}",description:"Картка, яка дає змогу контролювати пилосос",old_configuration:"Виявлено стару конфігурацію. Налаштуйте конфігурацію до останньої схеми або створіть нову картку з початку.",old_configuration_migration_link:"Посібник з міграції"},Mi={invalid:"Недійсний шаблон!",vacuum_goto:"Рух до цілі",vacuum_goto_predefined:"Збережені точки",vacuum_clean_segment:"Кімнати",vacuum_clean_zone:"Зональне прибирання",vacuum_clean_zone_predefined:"Список зон",vacuum_follow_path:"Шлях"},Ti={preset:{entity:{missing:"Відсутній параметр: entity"},preset_name:{missing:"Відсутній параметр: preset_name"},platform:{invalid:"Недійсна платформа пилососа: {0}"},map_source:{missing:"Відсутній параметр: map_source",none_provided:"Не вказано джерело мапи",ambiguous:"Дозволено тільки одне джерело мапи"},calibration_source:{missing:"Відсутній параметр: calibration_source",ambiguous:"Дозволено тільки одне джерело калібрування",none_provided:"Не вказано джерело калібрування",calibration_points:{invalid_number:"Потрібні 3 або 4 точки калібрування",missing_map:"Кожна точка калібрування повинна мати координати на мапі",missing_vacuum:"Кожна точка калібрування повинна мати координати в системі пилососа",missing_coordinate:"Кожна точка калібрування повинна мати координати x і y"}},icons:{invalid:"Помилка в конфігурації: icons",icon:{missing:'Кожен елемент у списку піктограм повинен мати параметр "icon"'}},tiles:{invalid:"Помилка в конфігурації: tiles",entity:{missing:'Кожен елемент у списку плиток повинен мати параметр "entity"'},label:{missing:'Кожен елемент у списку плиток повинен мати параметр "label"'}},map_modes:{invalid:"Помилка в конфігурації: map_modes",icon:{missing:"Відсутня піктограма шаблону режиму мапи"},name:{missing:"Відсутня назва шаблону режиму мапи"},template:{invalid:"Недійсний шаблон: {0}"},predefined_selections:{not_applicable:"Шаблон {0} не підтримує збереження вибраних елементів",zones:{missing:"Відсутній список збережених зон",invalid_parameters_number:"Кожна збережена зона повинна мати 4 координати"},points:{position:{missing:"Відсутній список збережених точок",invalid_parameters_number:"Кожна записана точка повинна мати 2 координати"}},rooms:{id:{missing:"Відсутній ідентифікатор кімнати",invalid_format:"Недійсний ідентифікатор кімнати: {0}"},outline:{invalid_parameters_number:"Кожна точка контуру кімнати повинна мати 2 координати"}},label:{x:{missing:"Кожна мітка повинна мати координату x"},y:{missing:"Кожна мітка повинна мати координату y"},text:{missing:"Кожна мітка повинна містити текст"}},icon:{x:{missing:"Кожна піктограма повинна мати координату x"},y:{missing:"Кожна піктограма повинна мати координату y"},name:{missing:'Кожна піктограма повинна мати параметр "name"'}}},service_call_schema:{missing:"Відсутня схема виклику служби",service:{missing:"Кожна схема служби повинна мати назву служби",invalid:"Недійсна служба: {0}"}}}},invalid_entities:"Недійсні сутності:",invalid_calibration:"Неправильне калібрування, перевірте конфігурацію"},Ci={status:"Статус",battery_level:"Батарея",fan_speed:"Потужність",sensor_dirty_left:"Сенсор",filter_left:"Фільтр",main_brush_left:"Основна щітка",side_brush_left:"Бокова щітка",cleaning_count:"Лічильник прибирань",cleaned_area:"Прибрано",cleaning_time:"Час прибирання"},Ni={vacuum_start:"Старт",vacuum_pause:"Пауза",vacuum_stop:"Стоп",vacuum_return_to_base:"Повернення на базу",vacuum_clean_spot:"Прибрати місце",vacuum_locate:"Пошук",vacuum_set_fan_speed:"Зміна потужності"},Ri={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Li={success:"Успіх!",no_selection:"Виділення не зроблено",failed:"Не вдалося викликати службу"},Oi={description:{before_link:"Цей редактор інтерфейсу підтримує лише базову конфігурацію для камери, створеної за допомогою ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Для більш розширеного налаштування використовуйте режим YAML."},label:{name:"Назва (опція)",entity:"Сутність пилососу (необхідно)",camera:"Сутність камери (необхідно)",vacuum_platform:"Платформа інтеграції пилососу (необхідно)",map_locked:"Блокування мапи (опція)",two_finger_pan:"Переміщеня мапи двома пальцями (опція)"}},$i={common:Si,map_mode:Mi,validation:Ti,label:Ci,icon:Ni,unit:Ri,popups:Li,editor:Oi},ji={version:"版本",invalid_configuration:"配置无效 {0}",description:"一个可以控制扫地机的卡片",old_configuration:"检测到旧版本的配置。请按照新版本说明修改配置或者重新创建新卡片",old_configuration_migration_link:"迁移向导"},Ii={invalid:"模板无效！",vacuum_goto:"指哪到哪",vacuum_goto_predefined:"目标点",vacuum_clean_segment:"选区清扫",vacuum_clean_point:"局部清扫",vacuum_clean_point_predefined:"局部目标",vacuum_clean_zone:"划区清扫",vacuum_clean_zone_predefined:"目标区域",vacuum_follow_path:"路径规划"},Di={preset:{entity:{missing:"缺少属性：entity"},preset_name:{missing:"缺少属性：preset_name"},platform:{invalid:"扫地机平台无效：{0}"},map_source:{missing:"缺少属性：map_source",none_provided:"未提供摄像头或者图像",ambiguous:"只允许一张地图"},calibration_source:{missing:"缺少属性：calibration_source",ambiguous:"只允许一个校准源",none_provided:"未提供校准源",calibration_points:{invalid_number:"需要3或4个校准点",missing_map:"每个校准点必须包含地图坐标",missing_vacuum:"每个校准点必须包含扫地机坐标",missing_coordinate:"地图校准点和扫地机校准点必须同时包含x坐标和y坐标"}},icons:{invalid:"配置错误：icons",icon:{missing:"图标列表中每一条记录必须包含icon属性"}},tiles:{invalid:"配置错误：tiles",entity:{missing:"板块列表中每一条记录必须包含实体"},label:{missing:"板块列表中每一条记录必须包含标签"}},map_modes:{invalid:"配置错误：map_modes",icon:{missing:"缺少该地图模式的图标"},name:{missing:"缺少该地图模式的名称"},template:{invalid:"模板无效：{0}"},predefined_selections:{not_applicable:"模式 {0} 不支持选择预置",zones:{missing:"缺少区域配置",invalid_parameters_number:"每个区域必须包含4个参数"},points:{position:{missing:"缺少坐标点配置",invalid_parameters_number:"每个坐标点必须包含2个参数"}},rooms:{id:{missing:"缺少房间id",invalid_format:"房间id无效：{0}"},outline:{invalid_parameters_number:"每个房间边框必须包含2个参数"}},label:{x:{missing:"标签必须包含x值"},y:{missing:"标签必须包含y值"},text:{missing:"标签必须包含文本值"}},icon:{x:{missing:"图标必须包含x值"},y:{missing:"标题必须包含y值"},name:{missing:"标题必须包含名称"}}},service_call_schema:{missing:"缺少服务调用架构",service:{missing:"服务调用架构必须包含服务",invalid:"服务无效：{0}"}}}},invalid_entities:"实体无效：",invalid_calibration:"校准无效，请检查配置"},Fi={status:"状态",battery_level:"剩余电量",fan_speed:"吸力",sensor_dirty_left:"传感器维护剩余",filter_left:"滤网剩余",main_brush_left:"主刷剩余",side_brush_left:"边刷剩余",cleaning_count:"总清扫次数",cleaned_area:"总清扫面积",cleaning_time:"总清扫时间",mop_left:"拖布剩余"},Vi={vacuum_start:"开始",vacuum_pause:"暂停",vacuum_stop:"结束",vacuum_return_to_base:"回充",vacuum_clean_spot:"局部清扫",vacuum_locate:"定位",vacuum_set_fan_speed:"更改吸力"},Ui={hour_shortcut:"小时",meter_shortcut:"米",meter_squared_shortcut:"平米",minute_shortcut:"分钟"},Xi={success:"指令发送成功！",no_selection:"未提供选择",failed:"调用服务失败"},Hi={description:{before_link:"该可视化编辑器仅支持一些基本配置，且必须使用以下集成创建的摄像机实体：",link_text:"Xiaomi Cloud Map Extractor",after_link:"。想要使用高级设置，请使用YAML模式"},label:{name:"标题（可选）",entity:"扫地机实体（必填）",camera:"摄像机实体（必填）",vacuum_platform:"扫地机平台（必填）",map_locked:"地图锁定（可选）",two_finger_pan:"双指缩放（可选）"}},qi={common:ji,map_mode:Ii,validation:Di,label:Fi,icon:Vi,unit:Ui,popups:Xi,editor:Hi};const Zi={da:Object.freeze({__proto__:null,common:Se,map_mode:Me,validation:Te,label:Ce,icon:Ne,unit:Re,popups:Le,editor:Oe,default:$e}),de:Object.freeze({__proto__:null,common:je,map_mode:Ie,validation:De,label:Fe,icon:Ve,unit:Ue,popups:Xe,editor:He,default:qe}),en:Object.freeze({__proto__:null,common:Ze,map_mode:Ke,validation:Be,label:Ge,icon:We,unit:Ye,popups:Je,editor:Qe,default:et}),es:Object.freeze({__proto__:null,common:tt,map_mode:it,validation:at,label:nt,icon:rt,unit:ot,popups:st,editor:lt,default:ct}),fr:Object.freeze({__proto__:null,common:dt,map_mode:ut,validation:mt,label:pt,icon:_t,unit:ht,popups:vt,editor:gt,default:ft}),he:Object.freeze({__proto__:null,common:bt,map_mode:yt,validation:xt,label:kt,icon:At,unit:wt,popups:Et,editor:zt,default:Pt}),hu:Object.freeze({__proto__:null,common:St,map_mode:Mt,validation:Tt,label:Ct,icon:Nt,unit:Rt,popups:Lt,editor:Ot,default:$t}),it:Object.freeze({__proto__:null,common:jt,map_mode:It,validation:Dt,label:Ft,icon:Vt,unit:Ut,popups:Xt,editor:Ht,default:qt}),nl:Object.freeze({__proto__:null,common:Zt,map_mode:Kt,validation:Bt,label:Gt,icon:Wt,unit:Yt,popups:Jt,editor:Qt,default:ei}),pl:Object.freeze({__proto__:null,common:ti,map_mode:ii,validation:ai,label:ni,icon:ri,unit:oi,popups:si,editor:li,default:ci}),"pt-BR":Object.freeze({__proto__:null,common:di,map_mode:ui,validation:mi,label:pi,icon:_i,unit:hi,popups:vi,editor:gi,default:fi}),ru:Object.freeze({__proto__:null,common:bi,map_mode:yi,validation:xi,label:ki,icon:Ai,unit:wi,popups:Ei,editor:zi,default:Pi}),uk:Object.freeze({__proto__:null,common:Si,map_mode:Mi,validation:Ti,label:Ci,icon:Ni,unit:Ri,popups:Li,editor:Oi,default:$i}),zh:Object.freeze({__proto__:null,common:ji,map_mode:Ii,validation:Di,label:Fi,icon:Vi,unit:Ui,popups:Xi,editor:Hi,default:qi})};function Ki(e,t="",i="",a=""){const n="en";if(!a)try{a=JSON.parse(localStorage.getItem("selectedLanguage")||'"en"')}catch(e){a=(localStorage.getItem("selectedLanguage")||n).replace(/['"]+/g,"")}let r;try{r=Bi(e,null!=a?a:n)}catch(t){r=Bi(e,n)}return void 0===r&&(r=Bi(e,n)),r=null!=r?r:e,""!==t&&""!==i&&(r=r.replace(t,i)),r}function Bi(e,t){return e.split(".").reduce(((e,t)=>e[t]),Zi[t])}function Gi(e,t){return"string"==typeof e?Ki(e,"","",t):Ki(...e,t)}function Wi(e,t,i){var a,n;return Gi(e,null!==(a=null==i?void 0:i.language)&&void 0!==a?a:null===(n=null==t?void 0:t.locale)||void 0===n?void 0:n.language)}var Yi={defaultTemplates:["vacuum_clean_zone","vacuum_goto"],templates:{vacuum_clean_segment:{name:"map_mode.vacuum_clean_segment",icon:"mdi:floor-plan",selection_type:"ROOM",repeats_type:"NONE",service_call_schema:{service:"xiaomi_miio.vacuum_clean_segment",service_data:{segments:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!0,max_selections:5,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"xiaomi_miio.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!0,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"xiaomi_miio.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_goto:{name:"map_mode.vacuum_goto",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"xiaomi_miio.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_goto_predefined:{name:"map_mode.vacuum_goto_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"xiaomi_miio.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_follow_path:{name:"map_mode.vacuum_follow_path",icon:"mdi:map-marker-path",selection_type:"MANUAL_PATH",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"script.vacuum_follow_path",service_data:{service:"xiaomi_miio.vacuum_goto",mode:"individual",path:"[[selection]]",entity_id:"[[entity_id]]"}}}}},Ji={from_attributes:[{attribute:"sensor_dirty_left",label:"label.sensor_dirty_left",icon:"mdi:eye-outline",unit:"unit.hour_shortcut"},{attribute:"filter_left",label:"label.filter_left",icon:"mdi:air-filter",unit:"unit.hour_shortcut"},{attribute:"main_brush_left",label:"label.main_brush_left",icon:"mdi:brush",unit:"unit.hour_shortcut"},{attribute:"side_brush_left",label:"label.side_brush_left",icon:"mdi:brush",unit:"unit.hour_shortcut"},{attribute:"cleaning_count",label:"label.cleaning_count",icon:"mdi:counter"}],from_sensors:[{unique_id_prefix:"consumable_sensor_dirty_left_",label:"label.sensor_dirty_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"consumable_filter_left_",label:"label.filter_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"consumable_main_brush_left_",label:"label.main_brush_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"consumable_side_brush_left_",label:"label.side_brush_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"clean_history_count_",label:"label.cleaning_count"}]},Qi={map_modes:Yi,sensors_from:"2021.11.0",tiles:Ji},ea=Object.freeze({__proto__:null,map_modes:Yi,sensors_from:"2021.11.0",tiles:Ji,default:Qi}),ta={defaultTemplates:["vacuum_clean_zone","vacuum_goto"],templates:{vacuum_clean_segment:{name:"map_mode.vacuum_clean_segment",icon:"mdi:floor-plan",selection_type:"ROOM",repeats_type:"NONE",service_call_schema:{service:"vacuum.vacuum_clean_segment",service_data:{segments:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!1,max_selections:5,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!1,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_goto:{name:"map_mode.vacuum_goto",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"vacuum.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_goto_predefined:{name:"map_mode.vacuum_goto_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"vacuum.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_follow_path:{name:"map_mode.vacuum_follow_path",icon:"mdi:map-marker-path",selection_type:"MANUAL_PATH",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"script.vacuum_follow_path",service_data:{service:"vacuum.vacuum_goto",mode:"individual",path:"[[selection]]",entity_id:"[[entity_id]]"}}}}},ia={from_attributes:[{attribute:"cleaned_area",label:"label.cleaned_area",icon:"mdi:texture-box",unit:"unit.meter_squared_shortcut"},{attribute:"cleaning_time",label:"label.cleaning_time",icon:"mdi:timer-sand",unit:"unit.minute_shortcut"}]},aa={map_modes:ta,tiles:ia},na=Object.freeze({__proto__:null,map_modes:ta,tiles:ia,default:aa}),ra={defaultTemplates:["vacuum_clean_zone","vacuum_clean_point"],templates:{vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!1,max_selections:5,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.xiaomi_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!1,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.xiaomi_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_clean_point:{name:"map_mode.vacuum_clean_point",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"vacuum.xiaomi_clean_point",service_data:{point:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_point_predefined:{name:"map_mode.vacuum_clean_point_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"vacuum.xiaomi_clean_point",service_data:{point:"[[selection]]",entity_id:"[[entity_id]]"}}}}},oa={from_attributes:[{attribute:"filter_left",label:"label.filter_left",icon:"mdi:air-filter",unit:"unit.hour_shortcut"},{attribute:"main_brush_left",label:"label.main_brush_left",icon:"mdi:brush",unit:"unit.hour_shortcut"},{attribute:"side_brush_left",label:"label.side_brush_left",icon:"mdi:brush",unit:"unit.hour_shortcut"},{attribute:"mop_left",label:"label.mop_left",icon:"mdi:format-color-fill",unit:"unit.hour_shortcut"}]},sa={map_modes:ra,tiles:oa},la=Object.freeze({__proto__:null,map_modes:ra,tiles:oa,default:sa}),ca={defaultTemplates:["vacuum_clean_zone","vacuum_goto"],templates:{vacuum_clean_segment:{name:"map_mode.vacuum_clean_segment",icon:"mdi:floor-plan",selection_type:"ROOM",repeats_type:"NONE",service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_segment_clean",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!0,max_selections:5,repeats_type:"INTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_zoned_clean",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!0,repeats_type:"INTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_zoned_clean",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_goto:{name:"map_mode.vacuum_goto",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_goto_target",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_goto_predefined:{name:"map_mode.vacuum_goto_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_goto_target",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_follow_path:{name:"map_mode.vacuum_follow_path",icon:"mdi:map-marker-path",selection_type:"MANUAL_PATH",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"script.vacuum_follow_path",service_data:{service:"vacuum.send_command",mode:"send_command",path:"[[selection]]",entity_id:"[[entity_id]]"}}}}},da={from_attributes:[],from_sensors:[]},ua={map_modes:ca,tiles:da},ma=Object.freeze({__proto__:null,map_modes:ca,tiles:da,default:ua});const pa=(e,t,i)=>{xa(i);const a=function(e,t){const i=ha(e),a=ha(t),n=i.pop(),r=a.pop(),o=fa(i,a);return 0!==o?o:n&&r?fa(n.split("."),r.split(".")):n||r?n?-1:1:0}(e,t);return ba[i].includes(a)},_a=/^v?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,ha=e=>{if("string"!=typeof e)throw new TypeError("Invalid argument expected string");const t=e.match(_a);if(!t)throw new Error(`Invalid argument not valid semver ('${e}' received)`);return t.shift(),t},va=e=>{const t=parseInt(e,10);return isNaN(t)?e:t},ga=(e,t)=>{const[i,a]=((e,t)=>typeof e!=typeof t?[String(e),String(t)]:[e,t])(va(e),va(t));return i>a?1:i<a?-1:0},fa=(e,t)=>{for(let i=0;i<Math.max(e.length,t.length);i++){const a=ga(e[i]||0,t[i]||0);if(0!==a)return a}return 0},ba={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1]},ya=Object.keys(ba),xa=e=>{if("string"!=typeof e)throw new TypeError("Invalid operator type, expected string but got "+typeof e);if(-1===ya.indexOf(e))throw new Error(`Invalid operator, expected one of ${ya.join("|")}`)};class ka{static getPlatforms(){return Array.from(ka.TEMPLATES.keys())}static isValidModeTemplate(e,t){return void 0!==t&&Object.keys(this.getPlatformTemplate(e).map_modes.templates).includes(t)}static getModeTemplate(e,t){return this.getPlatformTemplate(e).map_modes.templates[t]}static generateDefaultModes(e){return this.getPlatformTemplate(e).map_modes.defaultTemplates.map((e=>({template:e})))}static getTilesFromAttributesTemplates(e){var t;return null!==(t=this.getPlatformTemplate(e).tiles.from_attributes)&&void 0!==t?t:[]}static getTilesFromSensorsTemplates(e){var t;return null!==(t=this.getPlatformTemplate(e).tiles.from_sensors)&&void 0!==t?t:[]}static usesSensors(e,t){const i=this.getPlatformTemplate(t).sensors_from;return!!i&&pa(e.config.version.replace(/b.*/,""),i,">=")}static getPlatformTemplate(e){var t,i;return null!==(i=null!==(t=this.TEMPLATES.get(e))&&void 0!==t?t:this.TEMPLATES.get(this.DEFAULT_PLATFORM))&&void 0!==i?i:{templates:[],defaultTemplates:{}}}}ka.DEFAULT_PLATFORM="default",ka.KRZYSZTOFHAJDAMOWICZ_MIIO2_PLATFORM="KrzysztofHajdamowicz/miio2",ka.MAROTOWEB_VIOMISE_PLATFORM="marotoweb/viomise",ka.SEND_COMMAND_PLATFORM="send_command",ka.TEMPLATES=new Map([[ka.DEFAULT_PLATFORM,ea],[ka.KRZYSZTOFHAJDAMOWICZ_MIIO2_PLATFORM,na],[ka.MAROTOWEB_VIOMISE_PLATFORM,la],[ka.SEND_COMMAND_PLATFORM,ma]]);const Aa="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAYAAABxLb1rAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH5QsWDwwxfsgRyAAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAtkSURBVHja7d19zCVXXQfw725368JuC7JtUWKXKiLUF7aQVhRYSUEUGiGAaEUJEkBAMWZVasQivlQrxVZAFgIiiYCgIWDiGxZECoKKS60FxQCW1yLU0hcXWlraZdc/znmSeWbvs8+duTNz99l+PslNdp699/zuzD33d+ecOedMAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAoNh2n+3VWkicneWiSByT5xiTbk3w1yS1Jbkjy8fr41yT/mOTAgjHvmeRRSR6T5CFJTq2PE5P8X5Lrk/xHkquSvCPJfy3wme1O8tga7/QkpyXZkeTGGue/k1xeH/+jmh+zpqozzJk0Dh/lcTDJbUm+lOQTSd6T5DVJnpXkm3rGfPY6MZuPq+co7+FJ9ncoc+Xx9SQfSPL8JCd13IddSV6d5PaOMT+e5NeS3KtDrPPql2HeGIeSvCXJ/QaqC9cm2dahnFNar9+7QWL2ebxoSXXm8MiPbRMfr2XkoYV37lCSf07yY0k2LyEBbkpySX0fi34wP9jh/e9N8rUF492a5IJ14uxI8lcLxLgzyS8PVBcuWEIyuuA4SoBD15m7WgIcNA9tzjA2Jfn+JG9N8uEkD5747PVVSX6l1aR/b5JnJjkzycm1WfHNSb6nNo9fkeTfe8bbmuRNSV5Wy11xXZLLahK9b5K71eb3mfXsbV+Sz7bKunuSRx4l1r1rE/3xrb/vr0ntrNoE/oYk35JkT/0xaDZ9tyS5NMkfDfCZv7A23aa0jJhDm7LO3JW79HrnoXbm3df6/xNqIrlPDfL0JH9SP8B2Jv5akqf12IG3tcqZ55T2ia3X3JLkRzvEvF+S3699gPOeAf7hjF+ei2o/4zwf0uOT/Gfj9X9zlB+oK1qxbkjy1Dni3D3JS2acFV/Yoy78bWv7JROcjS0j5r4Rv5xT1Zm1fKbx2usGaiWOcbyWlof67tzWJM9I8skZH/DTJ0iA7T6/J/U88KfV/rL1EuBTZxzkH+8Rb0uSX6/N07Uq84tasf63nsF28TOtJHiw9pV2qQvnt758X60VcMxktIyYYyXAKevM8Z4AR8tDi+7c9iRvbJVxe5KzR0yA92k9f+yrZNuSfLHDF2we5yZ5w4y/n1o7e5sf5Lk9Y1zaes//1LEuPCXJE1p/e93IyWgZMfdt8DpzV06AC+ehoXbuda1yPlx/ucZIgA9rPf9tIyfAn2/FuyLjDSX6zVas1y9Q1t2SfLpV3vd1TEZJuVLePJN84MgJcOqY+zZ4nZEAO+ahzSPswM/VpsuKByX5qZE+1C0zmrFj+oXW9iX14A5tU5Lntf522QLl3ZYy7KLpeT3K+dVWX8zvTvDFXUbMjVhn6JGHxkiAd+bIYQu/ONJOtgf5Prg2Hcdw3yT3b2x/Ksk7R4p1ZsrV3xX7B2jev6E2o5vNqK4+kOSvG9srg83HtIyYG7HO0CMPbR4p+DtTOiNX7E73wbjz+GQrCe5I8tqUISFDayeMK0b8Jd/T2n7/AGVenzKQdsWu+ujqha1EeskElXkZMTdanaFHHhorAR5OmbrT9OiRYrWbdk9K8rEkL0iZBjeUs2ecmYylPX7pyoHK/dA6cebx0ZRO5hWPTPK4kSvyMmJutDpDjzy0ecTgV7W2v2ukOH8wI9YZKWP7PpYybu7dKQNQn1Ur5bYecdpN60+PeOxOaW1/dqByP7dOnHm9OGUox4rfG7kuTRXz+Rl2ZsOUdWYZhj5ek+ehMStt+8PeNVKc25P88FF+XXfWrL83yR/Xs6Avp/SrXZwyCX0eO1vbN4947Nrzgw8MVO6BdeLM69qsvjq3O8lPjlyRlxFzUVPWGXrkoTET4Jdb2yeNGOuG2ix6TpJr5nj+1iTnpPQt/VtNnues85p7rrN/Q2ofq1sHKveW1vbJC5R1cSuhXpTVU7zGsIyYi5iyztAjD42ZAKce63QoZezPd6RcRLgoZaWIL83x2ocn+WDKmK213DlhQm8nqu0DlbtjwC/kTVl9MeKMJD878mc8dsxX1Xrb5/E7S64zyzD08Zo8D42ZAIf8snVxuJ7Rvbg2fU9LWQThh1LGlL01ZTjCrGPxyhy56MBa73/nyF/0pnsMVG67nBsXLO/lSb7Q2L5wgi/5MmIOdfaxM0ztqHlozAR4xjpt8Sldl+Tv69nD+SmXwnenrI7SHpbw0jV+NdoXEE4fuUm/Zr/FAk5fJ05XtyX5rcb2qem2dNVGidnXlHWGHnlozAR4Vmv76mPswHwkyXNz5OjwB2b2dKv2QOQfGPG9tY/V2QOV2+7nvGqAMl+f1eMLfymrB3GPYRkx+5iyztAjD42ZAB/b+PehJO86Rg/QnyX5l9bfvnvG89rPefSI76k98HnPAGXubCX2TyX5/ADlfj2rl9janrJiyZiWEbOPKesMPfLQWAlwT8p0rhXvTVnK6Vj1kXX6DZIybOb6xva3pixYOYaPZvXFm4cm+c4Fy3xG6/N+z4Dv9+0p91ZZ8ZyMM/Nn2TG7mrLO0CMPjZEAT0gZhNx06TF+oO5obX9xxnMOpUyza7ow41ztPpzSP5lWM6+vbSmTw5teO/B7bi5asDXTXOVbRswupqwz9MhDYyTAl2b1ZPV3J/m7kXZyb8rV3kX3o7k01MGs3Tf2siRfaWw/LN3utTHLuSkr2rbty+qZD89MuYNYHxcl+bbG9vsy3PS65q9r83M+P+PfGmEZMbuass7QMQ8NmQBPTBlG0jxTOZB+yy7Na0vKFcF/WKD588SsvjhweavZ0nRzyhSspouT/ESPuJtrAn9XZk9Juy6rx7xtSvLnKVevu3h26zM52DpzGlJz0YJNM47V8RKziynrDAvkoUUWInxySr9V8/V3pPuE9a4Lor4gqxfL/NN0m3P8tJSl1pvveb2+tk058g5th+rp9rzj9R6XskDjevd3OCHlhkjNWDfX971eM2p7yn002nMw50l+ay1OOo83Ze35n3uP8ZhjLYk/ZZ1Zy2dy/C+IulAemudmJCfVpHRObW68MkeuNLxy274f6bHziyTA5uNDKSsqPyblTmkn1j6ieyX53vqluHJGhXzunO/z5JTb77Xj3pgyUPe8lLF722oFf0DKQOzLUm5a3n7d0SrzvTP7XsBX1l+53fVsYGvKLQIeUc84Pj/jNa+Zs/9pkWR0Rta+7ePeYzzmmDdFmrLOHM8JcLQ8NNQ9P/dn/WXLm82zRe4L/NMpQyIWfc9fqWV1PdV+9QCxb8r607m2J/nLBWIcTLltaN+68JSOx+blEyfAoWKOfV/gKevMFAnwWLsvcN88NEjgD9b+tK79U4veGH1X7Qf8RI/3fEeSN2exmRZ7UtYc6xr76pS5xzs6xDov5V7GXeL8RVYPBZgiAZ6SMuVoygQ4RMwpbow+dZ25qyXATnloS4edP5wyufvW2g/1hXpqvr+ejg8xqLaPzyX5jfr49pSlsR5Uv/S76unySbWJe6A2Oa6uzZG3Z/aQly7eXx/3Txno+oiUW1furE3urfWYXVv7cN6XsjLwNT1ivSPlStZDUgZ4nlub+KfVL8VNKeMHr0mZ+nd5Zs97HtsNtX/rt4/zmBuhzhxvjtU8BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASf4fJ6JYBxmOptUAAAAASUVORK5CYII=";let wa=class extends ne{constructor(){super(...arguments),this._initialized=!1}setConfig(e){this._config=e,this.loadCardHelpers()}shouldUpdate(){return this._initialized||this._initialize(),!0}get _title(){var e;return(null===(e=this._config)||void 0===e?void 0:e.title)||""}get _entity(){var e;return(null===(e=this._config)||void 0===e?void 0:e.entity)||""}get _vacuum_platform(){var e;return(null===(e=this._config)||void 0===e?void 0:e.vacuum_platform)||""}get _camera(){var e,t;return(null===(t=null===(e=this._config)||void 0===e?void 0:e.map_source)||void 0===t?void 0:t.camera)||""}get _map_locked(){var e;return(null===(e=this._config)||void 0===e?void 0:e.map_locked)||!1}get _two_finger_pan(){var e;return(null===(e=this._config)||void 0===e?void 0:e.two_finger_pan)||!1}render(){if(!this.hass||!this._helpers)return j``;this._helpers.importMoreInfoControl("climate");const e=Object.keys(this.hass.states),t=e.filter((e=>"camera"===e.substr(0,e.indexOf(".")))).filter((e=>{var t;return null===(t=this.hass)||void 0===t?void 0:t.states[e].attributes.calibration_points})),i=e.filter((e=>"vacuum"===e.substr(0,e.indexOf(".")))),a=ka.getPlatforms();return j`
            <div class="card-config">
                <div class="description">
                    ${this._localize("editor.description.before_link")}<a
                        target="_blank"
                        href="https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor"
                        >${this._localize("editor.description.link_text")}</a
                    >${this._localize("editor.description.after_link")}
                </div>
                <div class="values">
                    <paper-input
                        label=${this._localize("editor.label.name")}
                        .value=${this._title}
                        .configValue=${"title"}
                        @value-changed=${this._titleChanged}></paper-input>
                </div>
                <div class="values">
                    <paper-dropdown-menu
                        label=${this._localize("editor.label.entity")}
                        @value-changed=${this._entityChanged}
                        .configValue=${"entity"}>
                        <paper-listbox slot="dropdown-content" .selected=${i.indexOf(this._entity)}>
                            ${i.map((e=>j` <paper-item>${e}</paper-item> `))}
                        </paper-listbox>
                    </paper-dropdown-menu>
                </div>
                <div class="values">
                    <paper-dropdown-menu
                        label=${this._localize("editor.label.vacuum_platform")}
                        @value-changed=${this._entityChanged}
                        .configValue=${"vacuum_platform"}>
                        <paper-listbox slot="dropdown-content" .selected=${a.indexOf(this._vacuum_platform)}>
                            ${a.map((e=>j` <paper-item>${e}</paper-item> `))}
                        </paper-listbox>
                    </paper-dropdown-menu>
                </div>
                <div class="values">
                    <paper-dropdown-menu
                        label=${this._localize("editor.label.camera")}
                        @value-changed=${this._cameraChanged}
                        .configValue=${"camera"}>
                        <paper-listbox slot="dropdown-content" .selected=${t.indexOf(this._camera)}>
                            ${t.map((e=>j` <paper-item>${e}</paper-item> `))}
                        </paper-listbox>
                    </paper-dropdown-menu>
                </div>
                <div class="values">
                    <ha-formfield .label=${this._localize("editor.label.map_locked")}>
                        <ha-switch
                            .checked=${this._map_locked}
                            .configValue=${"map_locked"}
                            @change=${this._valueChanged}></ha-switch>
                    </ha-formfield>
                </div>
                <div class="values">
                    <ha-formfield .label=${this._localize("editor.label.two_finger_pan")}>
                        <ha-switch
                            .checked=${this._two_finger_pan}
                            .configValue=${"two_finger_pan"}
                            @change=${this._valueChanged}></ha-switch>
                    </ha-formfield>
                </div>
            </div>
        `}_initialize(){void 0!==this.hass&&void 0!==this._config&&void 0!==this._helpers&&(this._initialized=!0)}async loadCardHelpers(){this._helpers=await window.loadCardHelpers()}_entityChanged(e){this._valueChanged(e)}_cameraChanged(e){if(!this._config||!this.hass)return;const t=e.target.value;if(this._camera===t)return;const i=Object.assign({},this._config);i.map_source={camera:t},i.calibration_source={camera:!0},this._config=i,we(this,"config-changed",{config:this._config})}_titleChanged(e){this._valueChanged(e)}_valueChanged(e){if(!this._config||!this.hass)return;const t=e.target;if(this[`_${t.configValue}`]!==t.value){if(t.configValue)this._config=Object.assign(Object.assign({},this._config),{[t.configValue]:void 0!==t.checked?t.checked:t.value});else{const e=Object.assign({},this._config);delete e[t.configValue],this._config=e}we(this,"config-changed",{config:this._config})}}_localize(e){return Wi(e,this.hass)}static get styles(){return o`
            .values {
                padding-left: 16px;
                margin: 8px;
                display: grid;
            }

            ha-formfield {
                padding: 8px;
            }
        `}};e([se({attribute:!1})],wa.prototype,"hass",void 0),e([le()],wa.prototype,"_config",void 0),e([le()],wa.prototype,"_helpers",void 0),wa=e([re("xiaomi-vacuum-map-card-editor")],wa);const Ea="ontouchstart"in window||navigator.maxTouchPoints>0;class za extends HTMLElement{constructor(){super(),this.holdTime=500,this.held=!1,this.ripple=document.createElement("mwc-ripple")}connectedCallback(){Object.assign(this.style,{position:"absolute",width:Ea?"100px":"50px",height:Ea?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none",zIndex:"999"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((e=>{document.addEventListener(e,(()=>{clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0}),{passive:!0})}))}bind(e,t){if(e.actionHandler)return;e.actionHandler=!0,e.addEventListener("contextmenu",(e=>{const t=e||window.event;return t.preventDefault&&t.preventDefault(),t.stopPropagation&&t.stopPropagation(),t.cancelBubble=!0,t.returnValue=!1,!1}));const i=e=>{let t,i;this.held=!1,e.touches?(t=e.touches[0].pageX,i=e.touches[0].pageY):(t=e.pageX,i=e.pageY),this.timer=window.setTimeout((()=>{this.startAnimation(t,i),this.held=!0}),this.holdTime)},a=i=>{i.preventDefault(),["touchend","touchcancel"].includes(i.type)&&void 0===this.timer||(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0,this.held?we(e,"action",{action:"hold"}):t.hasDoubleClick?"click"===i.type&&i.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,we(e,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,we(e,"action",{action:"double_tap"})):we(e,"action",{action:"tap"}))};e.addEventListener("touchstart",i,{passive:!0}),e.addEventListener("touchend",a),e.addEventListener("touchcancel",a),e.addEventListener("mousedown",i,{passive:!0}),e.addEventListener("click",a),e.addEventListener("keyup",(e=>{13===e.keyCode&&a(e)}))}startAnimation(e,t){Object.assign(this.style,{left:`${e}px`,top:`${t}px`,display:null}),this.ripple.disabled=!1,this.ripple.active=!0,this.ripple.unbounded=!0}stopAnimation(){this.ripple.active=!1,this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler-xiaomi-vacuum-map-card",za);const Pa=(e,t)=>{const i=(()=>{const e=document.body;if(e.querySelector("action-handler-xiaomi-vacuum-map-card"))return e.querySelector("action-handler-xiaomi-vacuum-map-card");const t=document.createElement("action-handler-xiaomi-vacuum-map-card");return e.appendChild(t),t})();i&&i.bind(e,t)},Sa=(e=>(...t)=>({_$litDirective$:e,values:t}))(class extends class{constructor(e){}T(e,t,i){this.Σdt=e,this.M=t,this.Σct=i}S(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}}{update(e,[t]){return Pa(e.element,t),D}render(e){}});class Ma{constructor(e){this.id=-1,this.nativePointer=e,this.pageX=e.pageX,this.pageY=e.pageY,this.clientX=e.clientX,this.clientY=e.clientY,self.Touch&&e instanceof Touch?this.id=e.identifier:Ta(e)&&(this.id=e.pointerId)}getCoalesced(){return"getCoalescedEvents"in this.nativePointer?this.nativePointer.getCoalescedEvents().map((e=>new Ma(e))):[this]}}const Ta=e=>self.PointerEvent&&e instanceof PointerEvent,Ca=()=>{};class Na{constructor(e,{start:t=(()=>!0),move:i=Ca,end:a=Ca,rawUpdates:n=!1}={}){this._element=e,this.startPointers=[],this.currentPointers=[],this._pointerStart=e=>{if(0===e.button&&this._triggerPointerStart(new Ma(e),e))if(Ta(e)){(e.target&&"setPointerCapture"in e.target?e.target:this._element).setPointerCapture(e.pointerId),this._element.addEventListener(this._rawUpdates?"pointerrawupdate":"pointermove",this._move),this._element.addEventListener("pointerup",this._pointerEnd),this._element.addEventListener("pointercancel",this._pointerEnd)}else window.addEventListener("mousemove",this._move),window.addEventListener("mouseup",this._pointerEnd)},this._touchStart=e=>{for(const t of Array.from(e.changedTouches))this._triggerPointerStart(new Ma(t),e)},this._move=e=>{const t=this.currentPointers.slice(),i="changedTouches"in e?Array.from(e.changedTouches).map((e=>new Ma(e))):[new Ma(e)],a=[];for(const e of i){const t=this.currentPointers.findIndex((t=>t.id===e.id));-1!==t&&(a.push(e),this.currentPointers[t]=e)}0!==a.length&&this._moveCallback(t,a,e)},this._triggerPointerEnd=(e,t)=>{const i=this.currentPointers.findIndex((t=>t.id===e.id));if(-1===i)return!1;this.currentPointers.splice(i,1),this.startPointers.splice(i,1);const a="touchcancel"===t.type||"pointercancel"===t.type;return this._endCallback(e,t,a),!0},this._pointerEnd=e=>{if(this._triggerPointerEnd(new Ma(e),e))if(Ta(e)){if(this.currentPointers.length)return;this._element.removeEventListener(this._rawUpdates?"pointerrawupdate":"pointermove",this._move),this._element.removeEventListener("pointerup",this._pointerEnd),this._element.removeEventListener("pointercancel",this._pointerEnd)}else window.removeEventListener("mousemove",this._move),window.removeEventListener("mouseup",this._pointerEnd)},this._touchEnd=e=>{for(const t of Array.from(e.changedTouches))this._triggerPointerEnd(new Ma(t),e)},this._startCallback=t,this._moveCallback=i,this._endCallback=a,this._rawUpdates=n&&"onpointerrawupdate"in window,self.PointerEvent?this._element.addEventListener("pointerdown",this._pointerStart):(this._element.addEventListener("mousedown",this._pointerStart),this._element.addEventListener("touchstart",this._touchStart),this._element.addEventListener("touchmove",this._move),this._element.addEventListener("touchend",this._touchEnd),this._element.addEventListener("touchcancel",this._touchEnd))}stop(){this._element.removeEventListener("pointerdown",this._pointerStart),this._element.removeEventListener("mousedown",this._pointerStart),this._element.removeEventListener("touchstart",this._touchStart),this._element.removeEventListener("touchmove",this._move),this._element.removeEventListener("touchend",this._touchEnd),this._element.removeEventListener("touchcancel",this._touchEnd),this._element.removeEventListener(this._rawUpdates?"pointerrawupdate":"pointermove",this._move),this._element.removeEventListener("pointerup",this._pointerEnd),this._element.removeEventListener("pointercancel",this._pointerEnd),window.removeEventListener("mousemove",this._move),window.removeEventListener("mouseup",this._pointerEnd)}_triggerPointerStart(e,t){return!!this._startCallback(e,t)&&(this.currentPointers.push(e),this.startPointers.push(e),!0)}}var Ra,La;!function(e){e[e.MANUAL_RECTANGLE=0]="MANUAL_RECTANGLE",e[e.PREDEFINED_RECTANGLE=1]="PREDEFINED_RECTANGLE",e[e.ROOM=2]="ROOM",e[e.MANUAL_PATH=3]="MANUAL_PATH",e[e.MANUAL_POINT=4]="MANUAL_POINT",e[e.PREDEFINED_POINT=5]="PREDEFINED_POINT"}(Ra||(Ra={})),function(e){e[e.NONE=0]="NONE",e[e.INTERNAL=1]="INTERNAL",e[e.EXTERNAL=2]="EXTERNAL"}(La||(La={}));class Oa{constructor(e,t,i,a){this.domain=e,this.service=t,this.serviceData=i,this.target=a}}class $a{constructor(e){this.service=e.service,this.serviceData=e.service_data,this.target=e.target}apply(e,t,i){const a=a=>$a.getReplacedValue(a,e,t,i);let n,r;this.serviceData&&(n=this.getFilledTemplate(this.serviceData,a)),this.target&&(r=this.getFilledTemplate(this.target,a));const o=this.service.split(".");return new Oa(o[0],o[1],n,r)}getFilledTemplate(e,t){const i=JSON.parse(JSON.stringify(e));return this.replacer(i,t),i}replacer(e,t){for(const[i,a]of Object.entries(e))"object"==typeof a?this.replacer(a,t):"string"==typeof a&&(e[i]=t(a))}static getReplacedValue(e,t,i,a){switch(e){case"[[entity_id]]":return t;case"[[selection]]":return i;case"[[repeats]]":return a;case"[[point_x]]":return this.isPoint(i)?i[0]:e;case"[[point_y]]":return this.isPoint(i)?i[1]:e;default:return e}}static isPoint(e){return"number"==typeof e[0]&&2==e.length}}class ja{constructor(e,t,i){var a,n,r,o,s,l,c,d;this.config=t,this.name=null!==(a=t.name)&&void 0!==a?a:Gi("map_mode.invalid",i),this.icon=null!==(n=t.icon)&&void 0!==n?n:"mdi:help",this.selectionType=t.selection_type?Ra[t.selection_type]:Ra.PREDEFINED_POINT,this.maxSelections=null!==(r=t.max_selections)&&void 0!==r?r:999,this.coordinatesRounding=null===(o=t.coordinates_rounding)||void 0===o||o,this.runImmediately=null!==(s=t.run_immediately)&&void 0!==s&&s,this.repeatsType=t.repeats_type?La[t.repeats_type]:La.NONE,this.maxRepeats=null!==(l=t.max_repeats)&&void 0!==l?l:1,this.serviceCallSchema=new $a(null!==(c=t.service_call_schema)&&void 0!==c?c:{}),this.predefinedSelections=null!==(d=t.predefined_selections)&&void 0!==d?d:[],this._applyTemplateIfPossible(e,t,i),ja.PREDEFINED_SELECTION_TYPES.includes(this.selectionType)||(this.runImmediately=!1)}_applyTemplateIfPossible(e,t,i){if(!t.template||!ka.isValidModeTemplate(e,t.template))return;const a=ka.getModeTemplate(e,t.template);!t.name&&a.name&&(this.name=Gi(a.name,i)),!t.icon&&a.icon&&(this.icon=a.icon),!t.selection_type&&a.selection_type&&(this.selectionType=Ra[a.selection_type]),!t.max_selections&&a.max_selections&&(this.maxSelections=a.max_selections),void 0===t.coordinates_rounding&&void 0!==a.coordinates_rounding&&(this.coordinatesRounding=a.coordinates_rounding),void 0===t.run_immediately&&void 0!==a.run_immediately&&(this.runImmediately=a.run_immediately),!t.repeats_type&&a.repeats_type&&(this.repeatsType=La[a.repeats_type]),!t.max_repeats&&a.max_repeats&&(this.maxRepeats=a.max_repeats),!t.service_call_schema&&a.service_call_schema&&(this.serviceCallSchema=new $a(a.service_call_schema))}getServiceCall(e,t,i){return this.serviceCallSchema.apply(e,t,i)}}ja.PREDEFINED_SELECTION_TYPES=[Ra.PREDEFINED_RECTANGLE,Ra.ROOM,Ra.PREDEFINED_POINT];class Ia{constructor(e,t){this.x=e,this.y=t}}function Da(e){e.preventDefault(),e.stopPropagation(),e.stopImmediatePropagation()}function Fa(e,t){const i=e.indexOf(t,0);return i>-1&&e.splice(i,1),i}function Va(e,t){var i,a,n,r;const o=new Set;return e.entity&&o.add(e.entity),e.map_source.camera&&o.add(e.map_source.camera),e.calibration_source.entity&&o.add(e.calibration_source.entity),(null!==(i=e.icons)&&void 0!==i?i:[]).filter((e=>e.conditions)).flatMap((e=>e.conditions)).map((e=>null==e?void 0:e.entity)).forEach((e=>{e&&o.add(e)})),(null!==(a=e.tiles)&&void 0!==a?a:[]).forEach((e=>o.add(e.entity))),(null!==(n=e.tiles)&&void 0!==n?n:[]).filter((e=>e.conditions)).flatMap((e=>e.conditions)).map((e=>null==e?void 0:e.entity)).forEach((e=>{e&&o.add(e)})),(null!==(r=e.map_modes)&&void 0!==r?r:[]).map((i=>{var a;return new ja(null!==(a=e.vacuum_platform)&&void 0!==a?a:"default",i,t)})).forEach((e=>function(e){const t=new Set;switch(e.selectionType){case Ra.PREDEFINED_RECTANGLE:e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.zones)).forEach((e=>t.add(e.zones.split(".attributes.")[0])));break;case Ra.PREDEFINED_POINT:e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.position)).forEach((e=>t.add(e.position.split(".attributes.")[0])))}return t}(e).forEach((e=>o.add(e))))),o}function Ua(e,t){var i;return(null!==(i=e.conditions)&&void 0!==i?i:[]).every((e=>function(e,t){const i=e.attribute?t.states[e.entity].attributes[e.attribute]:t.states[e.entity].state;return e.value?i==e.value:!!e.value_not&&i!=e.value_not}(e,t)))}function Xa(e,t){return e?t():null}function Ha(e,t){return i=>{e.hass&&t&&i.detail.action&&function(e,t,i,a){var n;"double_tap"===a&&i.double_tap_action?n=i.double_tap_action:"hold"===a&&i.hold_action?n=i.hold_action:"tap"===a&&i.tap_action&&(n=i.tap_action),ze(e,t,i,n)}(e,e.hass,t,i.detail.action)}}function qa(e,t,i){let a,n;return e instanceof MouseEvent&&(a=e.offsetX,n=e.offsetY),window.TouchEvent&&e instanceof TouchEvent&&e.touches&&(a=(e.touches[0].clientX-t.getBoundingClientRect().x)/i,n=(e.touches[0].clientY-t.getBoundingClientRect().y)/i),new Ia(a,n)}function Za(e,t){return t?Math.sqrt((t.clientX-e.clientX)**2+(t.clientY-e.clientY)**2):0}function Ka(e,t){return t?{clientX:(e.clientX+t.clientX)/2,clientY:(e.clientY+t.clientY)/2}:e}function Ba(e,t){return"number"==typeof e?e:e.trimRight().endsWith("%")?t*parseFloat(e)/100:parseFloat(e)}let Ga;function Wa(){return Ga||(Ga=document.createElementNS("http://www.w3.org/2000/svg","svg"))}function Ya(){return Wa().createSVGMatrix()}function Ja(){return Wa().createSVGPoint()}class Qa extends HTMLElement{constructor(){super(),this._transform=Ya(),this._enablePan=!0,this._locked=!1,this._twoFingerPan=!1,new MutationObserver((()=>this._stageElChange())).observe(this,{childList:!0});const e=new Na(this,{start:(t,i)=>!(i.target.classList.contains("draggable")&&e.currentPointers.length<2)&&(!(2===e.currentPointers.length||!this._positioningEl||this.locked)&&((this.enablePan||1==e.currentPointers.length||i instanceof PointerEvent&&"mouse"==i.pointerType)&&(this.enablePan=!0),!0)),move:t=>{this.enablePan&&this._onPointerMove(t,e.currentPointers)},end:(t,i,a)=>(this.twoFingerPan&&1==e.currentPointers.length&&(this.enablePan=!1),Da(i),!1)});this.addEventListener("wheel",(e=>this._onWheel(e)))}static get observedAttributes(){return["min-scale","max-scale","no-default-pan","two-finger-pan","locked"]}attributeChangedCallback(e,t,i){"min-scale"===e&&this.scale<this.minScale&&this.setTransform({scale:this.minScale}),"max-scale"===e&&this.scale>this.maxScale&&this.setTransform({scale:this.maxScale}),"no-default-pan"===e&&(this.enablePan=!("1"==i||"true"==i)),"two-finger-pan"===e&&("1"==i||"true"==i?(this.twoFingerPan=!0,this.enablePan=!1):(this.twoFingerPan=!1,this.enablePan=!0)),"locked"===e&&(this.locked="1"==i||"true"==i)}get minScale(){const e=this.getAttribute("min-scale");if(!e)return.01;const t=parseFloat(e);return Number.isFinite(t)?Math.max(.01,t):.01}set minScale(e){e&&this.setAttribute("min-scale",String(e))}get maxScale(){const e=this.getAttribute("max-scale");if(!e)return 100;const t=parseFloat(e);return Number.isFinite(t)?Math.min(100,t):100}set maxScale(e){e&&this.setAttribute("max-scale",String(e))}set enablePan(e){this._enablePan=e,this._enablePan?this._enablePan&&"none"!=this.style.touchAction&&(this.style.touchAction="none"):this.style.touchAction="pan-y pan-x"}get enablePan(){return this._enablePan}set locked(e){this._locked=e}get locked(){return this._locked}set twoFingerPan(e){this._twoFingerPan=e}get twoFingerPan(){return this._twoFingerPan}connectedCallback(){this._stageElChange()}get x(){return this._transform.e}get y(){return this._transform.f}get scale(){return this._transform.a}scaleTo(e,t={}){let{originX:i=0,originY:a=0}=t;const{relativeTo:n="content",allowChangeEvent:r=!1}=t,o="content"===n?this._positioningEl:this;if(!o||!this._positioningEl)return void this.setTransform({scale:e,allowChangeEvent:r});const s=o.getBoundingClientRect();if(i=Ba(i,s.width),a=Ba(a,s.height),"content"===n)i+=this.x,a+=this.y;else{const e=this._positioningEl.getBoundingClientRect();i-=e.left,a-=e.top}this._applyChange({allowChangeEvent:r,originX:i,originY:a,scaleDiff:e/this.scale})}setTransform(e={}){const{scale:t=this.scale,allowChangeEvent:i=!1}=e;let{x:a=this.x,y:n=this.y}=e;if(!this._positioningEl)return void this._updateTransform(t,a,n,i);const r=this.getBoundingClientRect(),o=this._positioningEl.getBoundingClientRect();if(!r.width||!r.height)return void this._updateTransform(t,a,n,i);let s=Ja();s.x=o.left-r.left,s.y=o.top-r.top;let l=Ja();l.x=o.width+s.x,l.y=o.height+s.y;const c=Ya().translate(a,n).scale(t).multiply(this._transform.inverse());s=s.matrixTransform(c),l=l.matrixTransform(c),s.x>r.width?a+=r.width-s.x:l.x<0&&(a+=-l.x),s.y>r.height?n+=r.height-s.y:l.y<0&&(n+=-l.y),this._updateTransform(t,a,n,i)}_updateTransform(e,t,i,a){if(!(e<this.minScale)&&!(e>this.maxScale)&&(e!==this.scale||t!==this.x||i!==this.y)&&(this._transform.e=t,this._transform.f=i,this._transform.d=this._transform.a=e,this.style.setProperty("--x",this.x+"px"),this.style.setProperty("--y",this.y+"px"),this.style.setProperty("--scale",this.scale+""),a)){const e=new Event("change",{bubbles:!0});this.dispatchEvent(e)}}_stageElChange(){this._positioningEl=void 0,0!==this.children.length&&(this._positioningEl=this.children[0],this.children.length>1&&console.warn("<pinch-zoom> must not have more than one child."),this.setTransform({allowChangeEvent:!0}))}_onWheel(e){if(!this._positioningEl||this.locked)return;e.preventDefault();const t=this._positioningEl.getBoundingClientRect();let{deltaY:i}=e;const{ctrlKey:a,deltaMode:n}=e;1===n&&(i*=15);const r=1-i/(a?100:300);this._applyChange({scaleDiff:r,originX:e.clientX-t.left,originY:e.clientY-t.top,allowChangeEvent:!0})}_onPointerMove(e,t){if(!this._positioningEl)return;const i=this._positioningEl.getBoundingClientRect(),a=Ka(e[0],e[1]),n=Ka(t[0],t[1]),r=a.clientX-i.left,o=a.clientY-i.top,s=Za(e[0],e[1]),l=Za(t[0],t[1]),c=s?l/s:1;this._applyChange({originX:r,originY:o,scaleDiff:c,panX:n.clientX-a.clientX,panY:n.clientY-a.clientY,allowChangeEvent:!0})}_applyChange(e={}){const{panX:t=0,panY:i=0,originX:a=0,originY:n=0,scaleDiff:r=1,allowChangeEvent:o=!1}=e,s=Ya().translate(t,i).translate(a,n).translate(this.x,this.y).scale(r).translate(-a,-n).scale(this.scale);this.setTransform({allowChangeEvent:o,scale:s.a,x:s.e,y:s.f})}}customElements.define("pinch-zoom",Qa);class en{constructor(e){this._context=e}scaled(e){return e/this._context.scale()}scaledCss(e){return parseFloat(this._context.cssEvaluator(e))/this._context.scale()}realScaled(e){return e/this._context.realScale()}realScaled2(e){return e*this._context.realScale()}realScaled2Point(e){return[this.realScaled2(e[0]),this.realScaled2(e[1])]}realScaledPoint(e){return[this.realScaled(e[0]),this.realScaled(e[1])]}update(){this._context.update()}localize(e){return this._context.localize(e)}getMousePosition(e){return this._context.mousePositionCalculator(e)}vacuumToRealMap(e,t){var i;const a=null===(i=this._context.coordinatesConverter())||void 0===i?void 0:i.vacuumToMap(e,t);if(!a)throw Error("Missing calibration");return a}vacuumToScaledMap(e,t){return this.realScaled2Point(this.vacuumToRealMap(e,t))}scaledMapToVacuum(e,t){const[i,a]=this.realScaledPoint([e,t]);return this.realMapToVacuum(i,a)}realMapToVacuum(e,t){var i;const a=null===(i=this._context.coordinatesConverter())||void 0===i?void 0:i.mapToVacuum(e,t);if(!a)throw Error("Missing calibration");return this._context.roundMap(a)}renderIcon(e,t,i){const a=e?this.vacuumToScaledMap(e.x,e.y):[];return I`${Xa(null!=e&&a.length>0,(()=>I`
                <foreignObject class="icon-foreign-object"
                               style="--x-icon: ${a[0]}px; --y-icon: ${a[1]}px;"
                               x="${a[0]}px" y="${a[1]}px" width="36px" height="36px">         
                    <body xmlns="http://www.w3.org/1999/xhtml">
                      <div class="map-icon-wrapper ${i} clickable" @click="${t}" >
                          <ha-icon icon="${null==e?void 0:e.name}" style="background: transparent;"></ha-icon>
                      </div>
                    </body>
                </foreignObject>
            `))}`}renderLabel(e,t){const i=e?this.vacuumToScaledMap(e.x,e.y):[];return I`${Xa(null!=e&&i.length>0,(()=>{var a,n;return I`
                <text class="label-text ${t}"
                      x="${i[0]+this.scaled(null!==(a=null==e?void 0:e.offset_x)&&void 0!==a?a:0)}px"
                      y="${i[1]+this.scaled(null!==(n=null==e?void 0:e.offset_y)&&void 0!==n?n:0)}px">
                    ${null==e?void 0:e.text}
                </text>
            `}))}`}vacuumToMapRect([e,t,i,a]){const n=[e,t],r=[i,t],o=[i,a],s=[e,a],l=this.vacuumToScaledMap(e,t),c=this.vacuumToScaledMap(i,t),d=this.vacuumToScaledMap(i,a),u=this.vacuumToScaledMap(e,a),m=[n,r,o,s,n,r,o,s],p=[l,c,d,u,l,c,d,u],_=[l,c,d,u],h=p.indexOf(en.findTopLeft(_)),v=p.slice(h,h+4),g=this._isCounterClockwise(v),f=m.slice(h,h+4);return g?[en._reverse(v),en._reverse(f)]:[v,f]}_isCounterClockwise(e){let t=0;return e.forEach(((i,a)=>t+=(e[(a+1)%4][0]-i[0])*(e[(a+1)%4][1]+i[1]))),t<0}static findTopLeft(e){const t=e.sort(((e,t)=>e[1]-t[1]))[0],i=e.indexOf(t),a=e[(i+1)%4],n=e[(i+3)%4],r=en.calcAngle(t,a)<en.calcAngle(t,n)?a:n;return r[0]<t[0]?r:t}static calcAngle(e,t){let i=Math.atan2(t[1]-e[1],t[0]-e[0]);return i>Math.PI/2&&(i=Math.PI-i),i}static _reverse([e,t,i,a]){return[e,a,i,t]}static get styles(){return o`
            .icon-foreign-object {
                overflow: visible;
                pointer-events: none;
            }

            .map-icon-wrapper {
                position: center;
                display: flex;
                align-items: center;
                justify-content: center;
                pointer-events: auto;
            }
        `}}var tn;!function(e){e[e.NONE=0]="NONE",e[e.RESIZE=1]="RESIZE",e[e.MOVE=2]="MOVE"}(tn||(tn={}));class an extends en{constructor(e,t,i,a,n,r){super(r),this._id=n,this._dragMode=tn.NONE,this._vacRect=this._toVacuumFromDimensions(e,t,i,a),this._vacRectSnapshot=this._vacRect}render(){const e=this._vacRect,t=this.vacuumToMapRect(e)[0],i=t[0],a=t[2],n=t[3],r=an.calcAngle(t[0],t[3]);return I`
            <g class="manual-rectangle-wrapper ${this.isSelected()?"selected":""}"
               style="--x-resize:${a[0]}px; 
                      --y-resize:${a[1]}px;
                      --x-delete:${n[0]}px;
                      --y-delete:${n[1]}px;
                      --x-description:${i[0]}px;
                      --y-description:${i[1]}px;
                      --angle-description: ${r}rad;">
                <polygon class="manual-rectangle draggable movable"
                         @mousedown="${e=>this._startDrag(e)}"
                         @mousemove="${e=>this._drag(e)}"
                         @mouseup="${e=>this._endDrag(e)}"
                         @touchstart="${e=>this._startDrag(e)}"
                         @touchmove="${e=>this._drag(e)}"
                         @touchend="${e=>this._endDrag(e)}"
                         @touchleave="${e=>this._endDrag(e)}"
                         @touchcancel="${e=>this._endDrag(e)}"
                         points="${an._toPoints(t)}">
                </polygon>
                <g class="manual-rectangle-description">
                    <text>
                        ${this._id} ${this._getDimensions()}
                    </text>
                </g>
                <circle class="manual-rectangle-delete-circle clickable"
                        @mouseup="${e=>this._delete(e)}"></circle>
                <path class="manual-rectangle-delete-icon"
                      d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z">
                </path>
                <circle class="manual-rectangle-resize-circle draggable resizer"
                        @mousedown="${e=>this._startDrag(e)}"
                        @mousemove="${e=>this._drag(e)}"
                        @mouseup="${e=>this._endDrag(e)}"
                        @touchstart="${e=>this._startDrag(e)}"
                        @touchmove="${e=>this._drag(e)}"
                        @touchend="${e=>this._endDrag(e)}"
                        @touchleave="${e=>this._endDrag(e)}"
                        @touchcancel="${e=>this._endDrag(e)}">
                </circle>
                <path class="manual-rectangle-resize-icon"
                      d="M13,21H21V13H19V17.59L6.41,5H11V3H3V11H5V6.41L17.59,19H13V21Z">
                </path>
            </g>
        `}isSelected(){return null!=this._selectedElement}_getDimensions(){const[e,t,i,a]=this.toVacuum(),n=Math.abs(i-e),r=Math.abs(a-t),o=this._context.roundingEnabled()?1e3:1,s=e=>(e/o).toFixed(1);return`${s(n)}${this.localize("unit.meter_shortcut")} x ${s(r)}${this.localize("unit.meter_shortcut")}`}_startDrag(e){var t;if(window.TouchEvent&&e instanceof TouchEvent&&e.touches.length>1)return;if(!e.target.classList.contains("draggable"))return;if(!(null===(t=e.target.parentElement)||void 0===t?void 0:t.classList.contains("manual-rectangle-wrapper")))return;if(!e.target.parentElement)return;Da(e),this._selectedTarget=e.target;const i=e.target;i.classList.contains("movable")?this._dragMode=tn.MOVE:i.classList.contains("resizer")?this._dragMode=tn.RESIZE:this._dragMode=tn.NONE,this._selectedElement=e.target.parentElement,this._vacRectSnapshot=[...this._vacRect];const a=this.getMousePosition(e);this._startPointSnapshot=this.scaledMapToVacuum(a.x,a.y),this.update()}externalDrag(e){this._drag(e)}_drag(e){if(!(window.TouchEvent&&e instanceof TouchEvent&&e.touches.length>1)&&this._selectedElement){Da(e);const t=this.getMousePosition(e);if(t){const e=this.scaledMapToVacuum(t.x,t.y),i=e[0]-this._startPointSnapshot[0],a=e[1]-this._startPointSnapshot[1];switch(this._dragMode){case tn.MOVE:this._vacRect=[this._vacRectSnapshot[0]+i,this._vacRectSnapshot[1]+a,this._vacRectSnapshot[2]+i,this._vacRectSnapshot[3]+a],this._setup(this.vacuumToMapRect(this._vacRect)[0]);break;case tn.RESIZE:const e=this.vacuumToMapRect(this._vacRectSnapshot)[1][0],t=[...this._vacRect];e[0]===this._vacRectSnapshot[0]?this._vacRect[2]=this._vacRectSnapshot[2]+i:this._vacRect[0]=this._vacRectSnapshot[0]+i,e[1]===this._vacRectSnapshot[1]?this._vacRect[3]=this._vacRectSnapshot[3]+a:this._vacRect[1]=this._vacRectSnapshot[1]+a,Math.sign(this._vacRect[0]-this._vacRect[2])==Math.sign(t[0]-t[2])&&Math.sign(this._vacRect[1]-this._vacRect[3])==Math.sign(t[1]-t[3])||(this._vacRect=t),this._setup(this.vacuumToMapRect(this._vacRect)[0]);case tn.NONE:}}}}_setup(e){var t,i,a,n,r,o,s,l,c,d,u,m,p,_,h,v,g;null===(a=null===(i=null===(t=this._selectedElement)||void 0===t?void 0:t.children)||void 0===i?void 0:i.item(0))||void 0===a||a.setAttribute("points",an._toPoints(e));const f=e[0],b=e[2],y=e[3],x=an.calcAngle(e[0],e[3]);null===(r=null===(n=this._selectedElement)||void 0===n?void 0:n.style)||void 0===r||r.setProperty("--x-resize",b[0]+"px"),null===(s=null===(o=this._selectedElement)||void 0===o?void 0:o.style)||void 0===s||s.setProperty("--y-resize",b[1]+"px"),null===(c=null===(l=this._selectedElement)||void 0===l?void 0:l.style)||void 0===c||c.setProperty("--x-delete",y[0]+"px"),null===(u=null===(d=this._selectedElement)||void 0===d?void 0:d.style)||void 0===u||u.setProperty("--y-delete",y[1]+"px"),null===(p=null===(m=this._selectedElement)||void 0===m?void 0:m.style)||void 0===p||p.setProperty("--x-description",f[0]+"px"),null===(h=null===(_=this._selectedElement)||void 0===_?void 0:_.style)||void 0===h||h.setProperty("--y-description",f[1]+"px"),null===(g=null===(v=this._selectedElement)||void 0===v?void 0:v.style)||void 0===g||g.setProperty("--angle-description",x+"rad")}_endDrag(e){Da(e),this._selectedElement=null,this._selectedTarget=null,this.update()}_delete(e){Da(e);const t=Fa(this._context.selectedManualRectangles(),this);if(t>-1){for(let e=t;e<this._context.selectedManualRectangles().length;e++)this._context.selectedManualRectangles()[e]._id=(e+1).toString();Ee("selection"),this._context.update()}}static _toPoints(e){const t=e.filter((e=>!isNaN(e[0])&&!isNaN(e[1]))).map((e=>e.join(", "))).join(" ");return 3==t.length&&console.error(`Points: ${t}`),t}_toVacuumFromDimensions(e,t,i,a){const n=this.realScaled(e),r=this.realScaled(t),o=this.realScaled(i),s=this.realScaled(a),l=this.realMapToVacuum(n,r),c=this.realMapToVacuum(n+o,r+s),d=[l[0],c[0]].sort(),u=[l[1],c[1]].sort();return[d[0],u[0],d[1],u[1]]}toVacuum(e=null){const[t,i,a,n]=this._vacRect,r=[Math.min(t,a),Math.min(i,n),Math.max(t,a),Math.max(i,n)];return null!=e?[...r,e]:r}static get styles(){return o`
            .resizer {
                cursor: nwse-resize;
            }

            .movable {
                cursor: move;
            }

            .manual-rectangle-wrapper {
            }

            .manual-rectangle-wrapper.selected {
            }

            .manual-rectangle {
                stroke: var(--map-card-internal-manual-rectangle-line-color);
                stroke-linejoin: round;
                stroke-dasharray: calc(var(--map-card-internal-manual-rectangle-line-segment-line) / var(--map-scale)),
                    calc(var(--map-card-internal-manual-rectangle-line-segment-gap) / var(--map-scale));
                fill: var(--map-card-internal-manual-rectangle-fill-color);
                stroke-width: calc(var(--map-card-internal-manual-rectangle-line-width) / var(--map-scale));
            }

            .manual-rectangle-wrapper.selected > .manual-rectangle {
                stroke: var(--map-card-internal-manual-rectangle-line-color-selected);
                fill: var(--map-card-internal-manual-rectangle-fill-color-selected);
            }

            .manual-rectangle-description {
                transform: translate(
                        calc(
                            var(--x-description) + var(--map-card-internal-manual-rectangle-description-offset-x) /
                                var(--map-scale)
                        ),
                        calc(
                            var(--y-description) + var(--map-card-internal-manual-rectangle-description-offset-y) /
                                var(--map-scale)
                        )
                    )
                    rotate(var(--angle-description));
                font-size: calc(var(--map-card-internal-manual-rectangle-description-font-size) / var(--map-scale));
                fill: var(--map-card-internal-manual-rectangle-description-color);
                background: transparent;
            }

            .manual-rectangle-delete-circle {
                r: calc(var(--map-card-internal-manual-rectangle-delete-circle-radius) / var(--map-scale));
                cx: var(--x-delete);
                cy: var(--y-delete);
                stroke: var(--map-card-internal-manual-rectangle-delete-circle-line-color);
                fill: var(--map-card-internal-manual-rectangle-delete-circle-fill-color);
                stroke-width: calc(
                    var(--map-card-internal-manual-rectangle-delete-circle-line-width) / var(--map-scale)
                );
            }

            .manual-rectangle-delete-icon {
                fill: var(--map-card-internal-manual-rectangle-delete-icon-color);
                transform: translate(
                        calc(var(--x-delete) - 8.5px / var(--map-scale)),
                        calc(var(--y-delete) - 8.5px / var(--map-scale))
                    )
                    scale(calc(0.71 / var(--map-scale)));
                pointer-events: none;
            }

            .manual-rectangle-wrapper.selected > .manual-rectangle-delete-circle {
                stroke: var(--map-card-internal-manual-rectangle-delete-circle-line-color-selected);
                fill: var(--map-card-internal-manual-rectangle-delete-circle-fill-color-selected);
                opacity: 50%;
            }

            .manual-rectangle-wrapper.selected > .manual-rectangle-delete-icon {
                fill: var(--map-card-internal-manual-rectangle-delete-icon-color-selected);
                opacity: 50%;
            }

            .manual-rectangle-resize-circle {
                r: calc(var(--map-card-internal-manual-rectangle-resize-circle-radius) / var(--map-scale));
                cx: var(--x-resize);
                cy: var(--y-resize);
                stroke: var(--map-card-internal-manual-rectangle-resize-circle-line-color);
                fill: var(--map-card-internal-manual-rectangle-resize-circle-fill-color);
                stroke-width: calc(
                    var(--map-card-internal-manual-rectangle-resize-circle-line-width) / var(--map-scale)
                );
            }

            .manual-rectangle-resize-icon {
                fill: var(--map-card-internal-manual-rectangle-resize-icon-color);
                transform: translate(
                        calc(var(--x-resize) - 8.5px / var(--map-scale)),
                        calc(var(--y-resize) - 8.5px / var(--map-scale))
                    )
                    scale(calc(0.71 / var(--map-scale)));
                pointer-events: none;
            }

            .manual-rectangle-wrapper.selected > .manual-rectangle-resize-circle {
                stroke: var(--map-card-internal-manual-rectangle-resize-circle-line-color-selected);
                fill: var(--map-card-internal-manual-rectangle-resize-circle-fill-color-selected);
                opacity: 50%;
            }

            .manual-rectangle-wrapper.selected > .manual-rectangle-resize-icon {
                fill: var(--map-card-internal-manual-rectangle-resize-icon-color-selected);
                opacity: 50%;
            }
        `}}class nn{constructor(e,t,i,a,n,r,o,s,l,c,d,u,m,p){this.scale=e,this.realScale=t,this.mousePositionCalculator=i,this.update=a,this.coordinatesConverter=n,this.selectedManualRectangles=r,this.selectedPredefinedRectangles=o,this.selectedRooms=s,this.selectedPredefinedPoint=l,this.roundingEnabled=c,this.maxSelections=d,this.cssEvaluator=u,this.runImmediately=m,this.localize=p}roundMap([e,t]){return this.roundingEnabled()?[Math.round(e),Math.round(t)]:[e,t]}}class rn extends en{constructor(e,t,i){super(i),this._x=e,this._y=t}}class on extends rn{constructor(e,t,i){super(e,t,i)}render(){return I`
            <g class="manual-point-wrapper" style="--x-point:${this._x}px; --y-point:${this._y}px;">
                <circle class="manual-point"></circle>
            </g>
        `}imageX(){return this.realScaled(this._x)}imageY(){return this.realScaled(this._y)}toVacuum(e=null){const[t,i]=this.realMapToVacuum(this.imageX(),this.imageY());return null===e?[t,i]:[t,i,e]}static get styles(){return o`
            .manual-point-wrapper {
                stroke: var(--map-card-internal-manual-point-line-color);
                stroke-width: calc(var(--map-card-internal-manual-point-line-width) / var(--map-scale));
                --radius: calc(var(--map-card-internal-manual-point-radius) / var(--map-scale));
            }

            .manual-point {
                cx: var(--x-point);
                cy: var(--y-point);
                r: var(--radius);
                fill: var(--map-card-internal-manual-point-fill-color);
            }
        `}}class sn extends en{constructor(e,t,i){super(i),this.x=e,this.y=t}imageX(){return this.realScaled(this.x)}imageY(){return this.realScaled(this.y)}renderMask(){return I`
            <circle style="r: var(--radius)"
                    cx="${this.x}"
                    cy="${this.y}"
                    fill="black">
            </circle>`}render(){return I`
            <circle class="manual-path-point"
                    cx="${this.x}"
                    cy="${this.y}">
            </circle>`}}class ln extends en{constructor(e,t){super(t),this.points=e}render(){if(0===this.points.length)return I``;const e=this.points.map((e=>e.x)),t=this.points.map((e=>e.y)),i=Math.max(...e),a=Math.min(...e),n=Math.max(...t),r=Math.min(...t);return I`
            <g class="manual-path-wrapper">
                <defs>
                    <mask id="manual-path-circles-filter">
                        <rect x="${a}" y="${r}" width="${i-a}" height="${n-r}"
                              fill="white"></rect>
                        ${this.points.map((e=>e.renderMask()))}
                    </mask>
                </defs>
                ${this.points.map((e=>e.render()))}
                <polyline class="manual-path-line"
                          points="${this.points.map((e=>`${e.x},${e.y}`)).join(" ")}"
                          mask="url(#manual-path-circles-filter)">
                </polyline>
            </g>
        `}toVacuum(e=null){return this.points.map((t=>{const[i,a]=this.realMapToVacuum(t.imageX(),t.imageY());return null===e?[i,a]:[i,a,e]}))}addPoint(e,t){this.points.push(new sn(e,t,this._context))}clear(){this.points=[]}removeLast(){this.points.pop()}static get styles(){return o`
            .manual-path-wrapper {
                --radius: calc(var(--map-card-internal-manual-path-point-radius) / var(--map-scale));
            }

            .manual-path-line {
                fill: transparent;
                stroke: var(--map-card-internal-manual-path-line-color);
                stroke-width: calc(var(--map-card-internal-manual-path-line-width) / var(--map-scale));
            }

            .manual-path-point {
                r: var(--radius);
                stroke: var(--map-card-internal-manual-path-point-line-color);
                fill: var(--map-card-internal-manual-path-point-fill-color);
                stroke-width: calc(var(--map-card-internal-manual-path-point-line-width) / var(--map-scale));
            }
        `}}class cn extends en{constructor(e,t){var i;super(t),this._config=e,this._selected=!1,this._iconConfig=null!==(i=this._config.icon)&&void 0!==i?i:{x:this._config.position[0],y:this._config.position[1],name:"mdi:map-marker"}}render(){return I`
            <g class="predefined-point-wrapper ${this._selected?"selected":""}">
                ${this.renderIcon(this._iconConfig,(()=>this._click()),"predefined-point-icon-wrapper")}
                ${this.renderLabel(this._config.label,"predefined-point-label")}
            </g>
        `}_click(){if(this._selected=!this._selected,Ee("selection"),this._selected){const e=this._context.selectedPredefinedPoint().pop();void 0!==e&&(e._selected=!1),this._context.selectedPredefinedPoint().push(this)}else Fa(this._context.selectedPredefinedPoint(),this);if(this._context.runImmediately())return this._selected=!1,void Fa(this._context.selectedPredefinedPoint(),this);this.update()}toVacuum(e=null){return"string"==typeof this._config.position?[0,0]:null===e?this._config.position:[...this._config.position,e]}static get styles(){return o`
            .predefined-point-wrapper {
            }

            .predefined-point-icon-wrapper {
                x: var(--x-icon);
                y: var(--y-icon);
                height: var(--map-card-internal-predefined-point-icon-wrapper-size);
                width: var(--map-card-internal-predefined-point-icon-wrapper-size);
                border-radius: var(--map-card-internal-small-radius);
                transform-box: fill-box;
                overflow: hidden;
                transform: translate(
                        calc(var(--map-card-internal-predefined-point-icon-wrapper-size) / -2),
                        calc(var(--map-card-internal-predefined-point-icon-wrapper-size) / -2)
                    )
                    scale(calc(1 / var(--map-scale)));
                background: var(--map-card-internal-predefined-point-icon-background-color);
                color: var(--map-card-internal-predefined-point-icon-color);
                --mdc-icon-size: var(--map-card-internal-predefined-point-icon-size);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-point-label {
                text-anchor: middle;
                dominant-baseline: middle;
                pointer-events: none;
                font-size: calc(var(--map-card-internal-predefined-point-label-font-size) / var(--map-scale));
                fill: var(--map-card-internal-predefined-point-label-color);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-point-wrapper.selected > * > .predefined-point-icon-wrapper {
                background: var(--map-card-internal-predefined-point-icon-background-color-selected);
                color: var(--map-card-internal-predefined-point-icon-color-selected);
            }

            .predefined-point-wrapper.selected > .predefined-point-label {
                fill: var(--map-card-internal-predefined-point-label-color-selected);
            }
        `}static getFromEntities(e,t,i){return e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.position)).map((e=>e.position.split(".attributes."))).flatMap((e=>{const i=t.states[e[0]],a=2===e.length?i.attributes[e[1]]:i.state;let n;try{n=JSON.parse(a)}catch(e){n=a}return n})).map((e=>new cn({position:e,label:void 0,icon:{x:e[0],y:e[1],name:"mdi:map-marker"}},i())))}}class dn extends en{constructor(e,t){super(t),this._config=e,this._selected=!1}render(){let e=[];"string"!=typeof this._config.zones&&(e=this._config.zones);const t=e.map((e=>this.vacuumToMapRect(e)[0]));return I`
            <g class="predefined-rectangle-wrapper ${this._selected?"selected":""}">
                ${t.map((e=>I`
                    <polygon class="predefined-rectangle clickable"
                             points="${e.map((e=>e.join(", "))).join(" ")}"
                             @click="${()=>this._click()}">
                    </polygon>
                `))}
                ${this.renderIcon(this._config.icon,(()=>this._click()),"predefined-rectangle-icon-wrapper")}
                ${this.renderLabel(this._config.label,"predefined-rectangle-label")}
            </g>
        `}_click(){if(!this._selected&&this._context.selectedPredefinedRectangles().map((e=>e.size())).reduce(((e,t)=>e+t),0)+this.size()>this._context.maxSelections())Ee("failure");else{if(this._selected=!this._selected,this._selected?this._context.selectedPredefinedRectangles().push(this):Fa(this._context.selectedPredefinedRectangles(),this),this._context.runImmediately())return this._selected=!1,void Fa(this._context.selectedPredefinedRectangles(),this);Ee("selection"),this.update()}}size(){return this._config.zones.length}toVacuum(e){return"string"==typeof this._config.zones?[]:null===e?this._config.zones:this._config.zones.map((t=>[...t,e]))}static get styles(){return o`
            .predefined-rectangle-wrapper {
            }

            .predefined-rectangle-wrapper.selected {
            }

            .predefined-rectangle {
                width: var(--width);
                height: var(--height);
                x: var(--x);
                y: var(--y);
                stroke: var(--map-card-internal-predefined-rectangle-line-color);
                stroke-linejoin: round;
                stroke-dasharray: calc(
                        var(--map-card-internal-predefined-rectangle-line-segment-line) / var(--map-scale)
                    ),
                    calc(var(--map-card-internal-predefined-rectangle-line-segment-gap) / var(--map-scale));
                fill: var(--map-card-internal-predefined-rectangle-fill-color);
                stroke-width: calc(var(--map-card-internal-predefined-rectangle-line-width) / var(--map-scale));
                transition: stroke var(--map-card-internal-transitions-duration) ease,
                    fill var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-rectangle-icon-wrapper {
                x: var(--x-icon);
                y: var(--y-icon);
                height: var(--map-card-internal-predefined-rectangle-icon-wrapper-size);
                width: var(--map-card-internal-predefined-rectangle-icon-wrapper-size);
                border-radius: var(--map-card-internal-small-radius);
                transform-box: fill-box;
                transform: translate(
                        calc(var(--map-card-internal-predefined-rectangle-icon-wrapper-size) / -2),
                        calc(var(--map-card-internal-predefined-rectangle-icon-wrapper-size) / -2)
                    )
                    scale(calc(1 / var(--map-scale)));
                background: var(--map-card-internal-predefined-rectangle-icon-background-color);
                color: var(--map-card-internal-predefined-rectangle-icon-color);
                --mdc-icon-size: var(--map-card-internal-predefined-rectangle-icon-size);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-rectangle-label {
                text-anchor: middle;
                dominant-baseline: middle;
                pointer-events: none;
                font-size: calc(var(--map-card-internal-predefined-rectangle-label-font-size) / var(--map-scale));
                fill: var(--map-card-internal-predefined-rectangle-label-color);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-rectangle-wrapper.selected > .predefined-rectangle {
                stroke: var(--map-card-internal-predefined-rectangle-line-color-selected);
                fill: var(--map-card-internal-predefined-rectangle-fill-color-selected);
            }

            .predefined-rectangle-wrapper.selected > * > .predefined-rectangle-icon-wrapper {
                background: var(--map-card-internal-predefined-rectangle-icon-background-color-selected);
                color: var(--map-card-internal-predefined-rectangle-icon-color-selected);
            }

            .predefined-rectangle-wrapper.selected > .predefined-rectangle-label {
                fill: var(--map-card-internal-predefined-rectangle-label-color-selected);
            }
        `}static getFromEntities(e,t,i){return e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.zones)).map((e=>e.zones.split(".attributes."))).flatMap((e=>{const i=t.states[e[0]],a=2===e.length?i.attributes[e[1]]:i.state;let n;try{n=JSON.parse(a)}catch(e){n=a}return n})).map((e=>new dn({zones:[e],label:void 0,icon:{x:(e[0]+e[2])/2,y:(e[1]+e[3])/2,name:"mdi:broom"}},i())))}}class un extends en{constructor(e,t){super(t),this._config=e,this._selected=!1}render(){var e,t;const i=(null!==(t=null===(e=this._config)||void 0===e?void 0:e.outline)&&void 0!==t?t:[]).map((e=>this.vacuumToScaledMap(e[0],e[1])));return I`
            <g class="room-wrapper ${this._selected?"selected":""} room-${this._config.id}-wrapper">
                <polygon class="room-outline clickable"
                         points="${i.map((e=>e.join(", "))).join(" ")}"
                         @click="${()=>this._click()}">
                </polygon>
                ${this.renderIcon(this._config.icon,(()=>this._click()),"room-icon-wrapper")}
                ${this.renderLabel(this._config.label,"room-label")}
            </g>
        `}toVacuum(){return this._config.id}_click(){if(!this._selected&&this._context.selectedRooms().length>=this._context.maxSelections())Ee("failure");else{if(this._selected=!this._selected,this._selected?this._context.selectedRooms().push(this):Fa(this._context.selectedRooms(),this),this._context.runImmediately())return this._selected=!1,void Fa(this._context.selectedRooms(),this);Ee("selection"),this.update()}}static get styles(){return o`
            .room-wrapper {
            }

            .room-outline {
                stroke: var(--map-card-internal-room-outline-line-color);
                stroke-width: calc(var(--map-card-internal-room-outline-line-width) / var(--map-scale));
                fill: var(--map-card-internal-room-outline-fill-color);
                stroke-linejoin: round;
                stroke-dasharray: calc(var(--map-card-internal-room-outline-line-segment-line) / var(--map-scale)),
                    calc(var(--map-card-internal-room-outline-line-segment-gap) / var(--map-scale));
                transition: stroke var(--map-card-internal-transitions-duration) ease,
                    fill var(--map-card-internal-transitions-duration) ease;
            }

            .room-icon-wrapper {
                x: var(--x-icon);
                y: var(--y-icon);
                height: var(--map-card-internal-room-icon-wrapper-size);
                width: var(--map-card-internal-room-icon-wrapper-size);
                border-radius: var(--map-card-internal-small-radius);
                transform-box: fill-box;
                overflow: hidden;
                transform: translate(
                        calc(var(--map-card-internal-room-icon-wrapper-size) / -2),
                        calc(var(--map-card-internal-room-icon-wrapper-size) / -2)
                    )
                    scale(calc(1 / var(--map-scale)));
                background: var(--map-card-internal-room-icon-background-color);
                color: var(--map-card-internal-room-icon-color);
                --mdc-icon-size: var(--map-card-internal-room-icon-size);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .room-label {
                text-anchor: middle;
                dominant-baseline: middle;
                pointer-events: none;
                font-size: calc(var(--map-card-internal-room-label-font-size) / var(--map-scale));
                fill: var(--map-card-internal-room-label-color);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .room-wrapper.selected > .room-outline {
                stroke: var(--map-card-internal-room-outline-line-color-selected);
                fill: var(--map-card-internal-room-outline-fill-color-selected);
            }

            .room-wrapper.selected > * > .room-icon-wrapper {
                background: var(--map-card-internal-room-icon-background-color-selected);
                color: var(--map-card-internal-room-icon-color-selected);
            }

            .room-wrapper.selected > .room-label {
                fill: var(--map-card-internal-room-label-color-selected);
            }
        `}}function mn(e){return void 0===e.x?["validation.preset.map_modes.predefined_selections.icon.x.missing"]:void 0===e.y?["validation.preset.map_modes.predefined_selections.icon.y.missing"]:e.name?[]:["validation.preset.map_modes.predefined_selections.icon.name.missing"]}function pn(e){return void 0===e.x?["validation.preset.map_modes.predefined_selections.label.x.missing"]:void 0===e.y?["validation.preset.map_modes.predefined_selections.label.y.missing"]:e.text?[]:["validation.preset.map_modes.predefined_selections.label.text.missing"]}function _n(e,t,i){var a,n;if(!t)return["validation.preset.map_modes.invalid"];if(t.template&&!ka.isValidModeTemplate(e,t.template))return[["validation.preset.map_modes.template.invalid","{0}",t.template]];const r=[];t.template||t.icon||r.push("validation.preset.map_modes.icon.missing"),t.template||t.name||r.push("validation.preset.map_modes.name.missing"),t.template||t.service_call_schema||r.push("validation.preset.map_modes.service_call_schema.missing");const o=new ja(e,t,i);switch(o.selectionType){case Ra.PREDEFINED_RECTANGLE:o.predefinedSelections.flatMap((e=>function(e){const t=e,i=[];return t.zones||i.push("validation.preset.map_modes.predefined_selections.zones.missing"),"string"!=typeof t.zones&&t.zones.filter((e=>4!=e.length)).length>0&&i.push("validation.preset.map_modes.predefined_selections.zones.invalid_parameters_number"),t.icon&&mn(t.icon).forEach((e=>i.push(e))),t.label&&pn(t.label).forEach((e=>i.push(e))),i}(e))).forEach((e=>r.push(e)));break;case Ra.ROOM:o.predefinedSelections.flatMap((e=>function(e){var t;const i=e,a=[];return void 0===i.id&&a.push("validation.preset.map_modes.predefined_selections.rooms.id.missing"),i.id.toString().match(/^[a-z0-9]+$/i)||a.push(["validation.preset.map_modes.predefined_selections.rooms.id.invalid_format","{0}",i.id.toString()]),(null!==(t=i.outline)&&void 0!==t?t:[]).filter((e=>2!=e.length)).length>0&&a.push("validation.preset.map_modes.predefined_selections.rooms.outline.invalid_parameters_number"),i.icon&&mn(i.icon).forEach((e=>a.push(e))),i.label&&pn(i.label).forEach((e=>a.push(e))),a}(e))).forEach((e=>r.push(e)));break;case Ra.PREDEFINED_POINT:o.predefinedSelections.flatMap((e=>function(e){var t;const i=e,a=[];return i.position||a.push("validation.preset.map_modes.predefined_selections.points.position.missing"),"string"!=typeof i.position&&2!=(null===(t=i.position)||void 0===t?void 0:t.length)&&a.push("validation.preset.map_modes.predefined_selections.points.position.invalid_parameters_number"),i.icon&&mn(i.icon).forEach((e=>a.push(e))),i.label&&pn(i.label).forEach((e=>a.push(e))),a}(e))).forEach((e=>r.push(e)));break;case Ra.MANUAL_RECTANGLE:case Ra.MANUAL_PATH:case Ra.MANUAL_POINT:null!==(n=null===(a=o.predefinedSelections)||void 0===a?void 0:a.length)&&void 0!==n&&n&&r.push(["validation.preset.map_modes.predefined_selections.not_applicable","{0}",Ra[o.selectionType]])}return t.service_call_schema&&function(e){return e.service?e.service.includes(".")?[]:[["validation.preset.map_modes.service_call_schema.service.invalid","{0}",e.service]]:["validation.preset.map_modes.service_call_schema.service.missing"]}(t.service_call_schema).forEach((e=>r.push(e))),r}function hn(e,t,i){var a,n,r,o;const s=[],l=new Map([["entity","validation.preset.entity.missing"],["map_source","validation.preset.map_source.missing"],["calibration_source","validation.preset.calibration_source.missing"]]),c=Object.keys(e);var d,u;l.forEach(((e,t)=>{c.includes(t)||s.push(e)})),e.map_source&&(d=e.map_source,d.camera||d.image?d.camera&&d.image?["validation.preset.map_source.ambiguous"]:[]:["validation.preset.map_source.none_provided"]).forEach((e=>s.push(e))),e.calibration_source&&(u=e.calibration_source,Object.keys(u).filter((e=>"attribute"!=e)).length>1?["validation.preset.calibration_source.ambiguous"]:u.calibration_points?[3,4].includes(u.calibration_points.length)?u.calibration_points.flatMap((e=>function(e){const t=[];return(null==e?void 0:e.map)||t.push("validation.preset.calibration_source.calibration_points.missing_map"),(null==e?void 0:e.vacuum)||t.push("validation.preset.calibration_source.calibration_points.missing_vacuum"),[null==e?void 0:e.map,null==e?void 0:e.vacuum].filter((e=>void 0===e.x||void 0===e.y)).length>0&&t.push("validation.preset.calibration_source.calibration_points.missing_coordinate"),t}(e))):["validation.preset.calibration_source.calibration_points.invalid_number"]:[]).forEach((e=>s.push(e))),e.vacuum_platform&&!ka.getPlatforms().includes(e.vacuum_platform)&&s.push(["validation.preset.platform.invalid","{0}",e.vacuum_platform]);const m=null!==(a=e.vacuum_platform)&&void 0!==a?a:"default";return(null!==(n=e.icons)&&void 0!==n?n:[]).flatMap((e=>function(e){if(!e)return["validation.preset.icons.invalid"];const t=[];return e.icon||t.push("validation.preset.icons.icon.missing"),t}(e))).forEach((e=>s.push(e))),(null!==(r=e.tiles)&&void 0!==r?r:[]).flatMap((e=>function(e){if(!e)return["validation.preset.tiles.invalid"];const t=[];return e.entity||t.push("validation.preset.tiles.entity.missing"),e.label||t.push("validation.preset.tiles.label.missing"),t}(e))).forEach((e=>s.push(e))),(null!==(o=e.map_modes)&&void 0!==o?o:[]).flatMap((e=>_n(m,e,i))).forEach((e=>s.push(e))),!e.preset_name&&t&&s.push("validation.preset.preset_name.missing"),s}class vn{static generate(e,t,i,a){if(!e)return new Promise((e=>e([])));const n=ka.usesSensors(e,i),r=e.states[t],o=[];return r?(o.push(...this.getCommonTiles(r,t,a)),n?this.addTilesFromSensors(e,t,i,o,a):new Promise((e=>e(this.addTilesFromAttributes(r,t,i,o,a))))):new Promise((e=>e(o)))}static getCommonTiles(e,t,i){const a=[];return"status"in e.attributes&&a.push({entity:t,label:Gi("label.status",i),attribute:"status",icon:"mdi:robot-vacuum"}),"battery_level"in e.attributes&&"battery_icon"in e.attributes&&a.push({entity:t,label:Gi("label.battery_level",i),attribute:"battery_level",icon:e.attributes.battery_icon,unit:"%"}),"battery_level"in e.attributes&&!("battery_icon"in e.attributes)&&a.push({entity:t,label:Gi("label.battery_level",i),attribute:"battery_level",icon:"mdi:battery",unit:"%"}),"fan_speed"in e.attributes&&a.push({entity:t,label:Gi("label.fan_speed",i),attribute:"fan_speed",icon:"mdi:fan"}),a}static addTilesFromAttributes(e,t,i,a,n){return ka.getTilesFromAttributesTemplates(i).filter((t=>t.attribute in e.attributes)).forEach((e=>a.push({entity:t,label:Gi(e.label,n),attribute:e.attribute,icon:e.icon,unit:e.unit?Gi(e.unit,n):void 0,precision:e.precision,multiplier:e.multiplier}))),a}static async addTilesFromSensors(e,t,i,a,n){const r=(await async function(e,t){const i=(await e.callWS({type:"entity/source",entity_id:[t]}))[t].config_entry,a=(await e.callWS({type:"config/entity_registry/list"})).filter((e=>e.config_entry_id===i));return Promise.all(a.map((t=>e.callWS({type:"config/entity_registry/get",entity_id:t.entity_id}))))}(e,t)).filter((e=>null===e.disabled_by)),o=r.filter((e=>e.entity_id===t))[0].unique_id;return ka.getTilesFromSensorsTemplates(i).map((e=>({tile:e,entity:r.filter((t=>t.unique_id===`${e.unique_id_prefix}${o}`))}))).flatMap((e=>e.entity.map((t=>this.mapToTile(t,e.tile.label,e.tile.unit,e.tile.multiplier,n))))).forEach((e=>a.push(e))),new Promise((e=>e(a)))}static mapToTile(e,t,i,a,n){var r;return{entity:e.entity_id,label:Gi(t,n),icon:null!==(r=e.icon)&&void 0!==r?r:e.original_icon,multiplier:a||void 0,precision:a?1:void 0,unit:i?Gi(i,n):void 0}}}class gn{static generate(e,t,i){if(!e)return[];const a=e.states[t],n=[];n.push({icon:"mdi:play",conditions:[{entity:t,value_not:"cleaning"},{entity:t,value_not:"error"},{entity:t,value_not:"returning"}],tooltip:Gi("icon.vacuum_start",i),tap_action:{action:"call-service",service:"vacuum.start",service_data:{entity_id:t}}}),n.push({icon:"mdi:pause",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"idle"},{entity:t,value_not:"error"},{entity:t,value_not:"paused"}],tooltip:Gi("icon.vacuum_pause",i),tap_action:{action:"call-service",service:"vacuum.pause",service_data:{entity_id:t}}}),n.push({icon:"mdi:stop",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"idle"},{entity:t,value_not:"error"},{entity:t,value_not:"paused"}],tooltip:Gi("icon.vacuum_stop",i),tap_action:{action:"call-service",service:"vacuum.stop",service_data:{entity_id:t}}}),n.push({icon:"mdi:home-map-marker",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"returning"}],tooltip:Gi("icon.vacuum_return_to_base",i),tap_action:{action:"call-service",service:"vacuum.return_to_base",service_data:{entity_id:t}}}),n.push({icon:"mdi:target-variant",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"error"},{entity:t,value_not:"cleaning"},{entity:t,value_not:"returning"}],tooltip:Gi("icon.vacuum_clean_spot",i),tap_action:{action:"call-service",service:"vacuum.clean_spot",service_data:{entity_id:t}}}),n.push({icon:"mdi:map-marker",tooltip:Gi("icon.vacuum_locate",i),tap_action:{action:"call-service",service:"vacuum.locate",service_data:{entity_id:t}}});const r=a&&a.attributes?a.attributes.fan_speed_list:[];for(let e=0;e<r.length;e++){const a=r[e],o=r[(e+1)%r.length];n.push({icon:a in this._ICON_MAPPING?this._ICON_MAPPING[a]:"mdi:fan-alert",conditions:[{entity:t,attribute:"fan_speed",value:a}],tooltip:Gi("icon.vacuum_set_fan_speed",i),tap_action:{action:"call-service",service:"vacuum.set_fan_speed",service_data:{entity_id:t,fan_speed:o}}})}return n}}gn._ICON_MAPPING={Silent:"mdi:fan-remove",Standard:"mdi:fan-speed-1",Medium:"mdi:fan-speed-2",Turbo:"mdi:fan-speed-3",Auto:"mdi:fan-auto",Gentle:"mdi:waves"};class fn{static render(e,t){var i,a,n;let r=e.attribute?t.hass.states[e.entity].attributes[e.attribute]:t.hass.states[e.entity].state;return"number"!=typeof r&&isNaN(+r)||(r=parseFloat(r.toString())*(null!==(i=e.multiplier)&&void 0!==i?i:1),null!=e.precision&&(r=r.toFixed(e.precision))),j`
            <div
                class="tile-wrapper clickable ripple"
                .title=${null!==(a=e.tooltip)&&void 0!==a?a:""}
                @action=${Ha(t,e)}
                .actionHandler=${Sa({hasHold:Pe(null==e?void 0:e.hold_action),hasDoubleClick:Pe(null==e?void 0:e.double_tap_action)})}>
                <div class="tile-title">${e.label}</div>
                <div class="tile-value-wrapper">
                    ${Xa(!!e.icon,(()=>j` <div class="tile-icon">
                            <ha-icon icon="${e.icon}"></ha-icon>
                        </div>`))}
                    <div class="tile-value">${r}${null!==(n=e.unit)&&void 0!==n?n:""}</div>
                </div>
            </div>
        `}static get styles(){return o`
            .tile-wrapper {
                min-width: fit-content;
                width: 80px;
                padding: 10px;
                border-radius: var(--map-card-internal-small-radius);
                background-color: var(--map-card-internal-tertiary-color);
                flex-grow: 1;
                overflow: hidden;
                color: var(--map-card-internal-tertiary-text-color);
            }

            .tile-title {
                font-size: smaller;
            }

            .tile-value-wrapper {
                display: inline-flex;
                align-items: flex-end;
                padding-top: 5px;
            }

            .tile-icon {
                padding-right: 5px;
            }

            .tile-value {
            }
        `}}class bn{static render(e,t){var i;return j`
            <paper-button
                class="vacuum-actions-item clickable ripple"
                .title=${null!==(i=e.tooltip)&&void 0!==i?i:""}
                @action=${Ha(t,e)}
                .actionHandler=${Sa({hasHold:Pe(null==e?void 0:e.hold_action),hasDoubleClick:Pe(null==e?void 0:e.double_tap_action)})}>
                <ha-icon icon="${e.icon}"></ha-icon>
            </paper-button>
        `}static get styles(){return o`
            .vacuum-actions-item {
                float: left;
                width: 50px;
                height: 50px;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: transparent;
            }
        `}}class yn{static render(){return j`
            <div id="toast">
                <div id="toast-icon">
                    <ha-icon icon="mdi:check" style="vertical-align: center"></ha-icon>
                </div>
                <div id="toast-text">Success!</div>
            </div>
        `}static get styles(){return o`
            #toast {
                visibility: hidden;
                display: inline-flex;
                width: calc(100% - 60px);
                min-height: 50px;
                color: var(--primary-text-color);
                text-align: center;
                border-radius: var(--map-card-internal-small-radius);
                padding-left: 30px;
                position: absolute;
                z-index: 1;
                bottom: 30px;
                font-size: 17px;
            }

            #toast #toast-icon {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 50px;
                background-color: var(--map-card-internal-primary-color);
                border-top-left-radius: var(--map-card-internal-small-radius);
                border-bottom-left-radius: var(--map-card-internal-small-radius);
                color: #0f0;
            }

            #toast #toast-text {
                box-sizing: border-box;
                display: flex;
                align-items: center;
                padding-left: 10px;
                padding-right: 10px;
                -moz-box-sizing: border-box;
                -webkit-box-sizing: border-box;
                background-color: var(--paper-listbox-background-color);
                color: var(--primary-text-color);
                vertical-align: middle;
                overflow: hidden;
                border-color: var(--map-card-internal-primary-color);
                border-style: solid;
                border-width: 1px;
                border-top-right-radius: var(--map-card-internal-small-radius);
                border-bottom-right-radius: var(--map-card-internal-small-radius);
            }

            #toast.show {
                visibility: visible;
                -webkit-animation: fadein 0.5s, stay 1s 1s, fadeout 0.5s 1.5s;
                animation: fadein 0.5s, stay 1s 1s, fadeout 0.5s 1.5s;
            }

            @-webkit-keyframes fadein {
                from {
                    bottom: 0;
                    opacity: 0;
                }
                to {
                    bottom: 30px;
                    opacity: 1;
                }
            }
            @keyframes fadein {
                from {
                    bottom: 0;
                    opacity: 0;
                }
                to {
                    bottom: 30px;
                    opacity: 1;
                }
            }
            @-webkit-keyframes stay {
            }
            @keyframes stay {
            }
            @-webkit-keyframes fadeout {
                from {
                    bottom: 30px;
                    opacity: 1;
                }
                to {
                    bottom: 60px;
                    opacity: 0;
                }
            }
            @keyframes fadeout {
                from {
                    bottom: 30px;
                    opacity: 1;
                }
                to {
                    bottom: 60px;
                    opacity: 0;
                }
            }
        `}}class xn{static render(e,t,i){const a=()=>e[t];return j`
            <paper-menu-button
                class="modes-dropdown-menu"
                vertical-align="bottom"
                horizontal-align="left"
                no-animations="true"
                close-on-activate="true">
                <div class="modes-dropdown-menu-button" slot="dropdown-trigger" alt="bottom align">
                    <paper-button class="modes-dropdown-menu-button-button">
                        <ha-icon icon="${a().icon}" class="dropdown-icon"></ha-icon>
                    </paper-button>
                    <div class="modes-dropdown-menu-button-text">${a().name}</div>
                </div>
                <paper-listbox
                    class="modes-dropdown-menu-listbox"
                    slot="dropdown-content"
                    selected="${t}"
                    @iron-select="${e=>{i(parseInt(e.detail.item.attributes["mode-id"].value))}}">
                    ${e.map(((i,a)=>j` <div mode-id="${a}">
                            <div class="modes-dropdown-menu-entry clickable ${t===a?"selected":""}">
                                <div
                                    class="modes-dropdown-menu-entry-button-wrapper ${0===a?"first":""} ${a===e.length-1?"last":""} ${t===a?"selected":""}">
                                    <paper-button
                                        class="modes-dropdown-menu-entry-button ${t===a?"selected":""}">
                                        <ha-icon icon="${i.icon}"></ha-icon>
                                    </paper-button>
                                </div>
                                <div class="modes-dropdown-menu-entry-text">${i.name}</div>
                            </div>
                        </div>`))}
                </paper-listbox>
            </paper-menu-button>
        `}static get styles(){return o`
            .modes-dropdown-menu {
                border-radius: var(--map-card-internal-big-radius);
                padding: 0;
            }

            .modes-dropdown-menu-button {
                display: inline-flex;
            }

            .modes-dropdown-menu-button-button {
                width: 50px;
                height: 50px;
                border-radius: var(--map-card-internal-big-radius);
                display: flex;
                justify-content: center;
                background-color: var(--map-card-internal-primary-color);
                align-items: center;
            }

            .modes-dropdown-menu-button-text {
                display: inline-flex;
                line-height: 50px;
                background-color: transparent;
                padding-left: 10px;
                padding-right: 15px;
            }

            .modes-dropdown-menu-entry {
                display: inline-flex;
                width: 100%;
            }

            .modes-dropdown-menu-entry.selected {
                border-radius: var(--map-card-internal-big-radius);
                background-color: var(--map-card-internal-primary-color);
                color: var(--map-card-internal-primary-text-color);
            }

            .modes-dropdown-menu-entry-button-wrapper.first:not(.selected) {
                border-top-left-radius: var(--map-card-internal-big-radius);
                border-top-right-radius: var(--map-card-internal-big-radius);
            }

            .modes-dropdown-menu-entry-button-wrapper.last:not(.selected) {
                border-bottom-left-radius: var(--map-card-internal-big-radius);
                border-bottom-right-radius: var(--map-card-internal-big-radius);
            }

            .modes-dropdown-menu-entry-button.selected {
                border-top-left-radius: var(--map-card-internal-big-radius);
                border-bottom-left-radius: var(--map-card-internal-big-radius);
                background-color: var(--map-card-internal-primary-color);
                color: var(--map-card-internal-primary-text-color);
            }

            .modes-dropdown-menu-entry-button-wrapper {
                background-color: var(--map-card-internal-secondary-color);
                color: var(--map-card-internal-secondary-text-color);
                overflow: hidden;
            }

            .modes-dropdown-menu-entry-button {
                width: 50px;
                height: 50px;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: var(--map-card-internal-secondary-color);
                color: var(--map-card-internal-secondary-text-color);
            }

            .modes-dropdown-menu-entry-text {
                display: inline-flex;
                line-height: 50px;
                background-color: transparent;
                padding-left: 10px;
                padding-right: 15px;
            }

            .modes-dropdown-menu-listbox {
                padding: 0;
                background-color: transparent;
            }
        `}}function kn(e,t){return Array.isArray(t)?[e.a*t[0]+e.c*t[1]+e.e,e.b*t[0]+e.d*t[1]+e.f]:{x:e.a*t.x+e.c*t.y+e.e,y:e.b*t.x+e.d*t.y+e.f}}function An(...e){const t=(e,t)=>({a:e.a*t.a+e.c*t.b,c:e.a*t.c+e.c*t.d,e:e.a*t.e+e.c*t.f+e.e,b:e.b*t.a+e.d*t.b,d:e.b*t.c+e.d*t.d,f:e.b*t.e+e.d*t.f+e.f});switch((e=Array.isArray(e[0])?e[0]:e).length){case 0:throw new Error("no matrices provided");case 1:return e[0];case 2:return t(e[0],e[1]);default:{const[i,a,...n]=e;return An(t(i,a),...n)}}}function wn(e,t){const i=null!=e[0].x?e[0].x:e[0][0],a=null!=e[0].y?e[0].y:e[0][1],n=null!=t[0].x?t[0].x:t[0][0],r=null!=t[0].y?t[0].y:t[0][1],o=null!=e[1].x?e[1].x:e[1][0],s=null!=e[1].y?e[1].y:e[1][1],l=null!=t[1].x?t[1].x:t[1][0],c=null!=t[1].y?t[1].y:t[1][1],d=null!=e[2].x?e[2].x:e[2][0],u=null!=e[2].y?e[2].y:e[2][1],m=null!=t[2].x?t[2].x:t[2][0],p=null!=t[2].y?t[2].y:t[2][1],_={a:n-m,b:r-p,c:l-m,d:c-p,e:m,f:p},h=function(e){const{a:t,b:i,c:a,d:n,e:r,f:o}=e,s=t*n-i*a;return{a:n/s,b:i/-s,c:a/-s,d:t/s,e:(n*r-a*o)/-s,f:(i*r-t*o)/s}}({a:i-d,b:a-u,c:o-d,d:s-u,e:d,f:u});return function(e,t=1e10){return{a:Math.round(e.a*t)/t,b:Math.round(e.b*t)/t,c:Math.round(e.c*t)/t,d:Math.round(e.d*t)/t,e:Math.round(e.e*t)/t,f:Math.round(e.f*t)/t}}(An([_,h]))}function En(e,t,i,a){this.message=e,this.expected=t,this.found=i,this.location=a,this.name="SyntaxError","function"==typeof Error.captureStackTrace&&Error.captureStackTrace(this,En)}!function(e,t){function i(){this.constructor=e}i.prototype=t.prototype,e.prototype=new i}(En,Error),En.buildMessage=function(e,t,i){var a={literal:function(e){return'"'+r(e.text)+'"'},class:function(e){var t=e.parts.map((function(e){return Array.isArray(e)?o(e[0])+"-"+o(e[1]):o(e)}));return"["+(e.inverted?"^":"")+t+"]"},any:function(){return"any character"},end:function(){return"end of input"},other:function(e){return e.description},not:function(e){return"not "+s(e.expected)}};function n(e){return e.charCodeAt(0).toString(16).toUpperCase()}function r(e){return e.replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\0/g,"\\0").replace(/\t/g,"\\t").replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/[\x00-\x0F]/g,(function(e){return"\\x0"+n(e)})).replace(/[\x10-\x1F\x7F-\x9F]/g,(function(e){return"\\x"+n(e)}))}function o(e){return e.replace(/\\/g,"\\\\").replace(/\]/g,"\\]").replace(/\^/g,"\\^").replace(/-/g,"\\-").replace(/\0/g,"\\0").replace(/\t/g,"\\t").replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/[\x00-\x0F]/g,(function(e){return"\\x0"+n(e)})).replace(/[\x10-\x1F\x7F-\x9F]/g,(function(e){return"\\x"+n(e)}))}function s(e){return a[e.type](e)}return"Expected "+function(e){var t,i,a=e.map(s);if(a.sort(),a.length>0){for(t=1,i=1;t<a.length;t++)a[t-1]!==a[t]&&(a[i]=a[t],i++);a.length=i}switch(a.length){case 1:return a[0];case 2:return a[0]+" or "+a[1];default:return a.slice(0,-1).join(", ")+", or "+a[a.length-1]}}(e)+" but "+function(e){return e?'"'+r(e)+'"':"end of input"}(t)+" found."};var zn,Pn,Sn,Mn=(zn=function(e,t){function i(e){var t;return"object"==typeof e?"object"==typeof(t=e[0])?[e.length,t.length]:[e.length]:[]}function a(e,t,i,n){if(i===t.length-1)return n(e);var r,o=t[i],s=Array(o);for(r=o-1;r>=0;r--)s[r]=a(e[r],t,i+1,n);return s}function n(e){var t,i=e.length,a=Array(i);for(t=i-1;-1!==t;--t)a[t]=e[t];return a}function r(e){if("object"!=typeof e)return e;var t=n;return a(e,i(e),0,t)}function o(e,t,i){void 0===i&&(i=0);var a,n=e[i],r=Array(n);if(i===e.length-1){for(a=n-2;a>=0;a-=2)r[a+1]=t,r[a]=t;return-1===a&&(r[0]=t),r}for(a=n-1;a>=0;a--)r[a]=o(e,t,i+1);return r}function s(e){return function(e){var t,i,a,n,r=e.length,o=Array(r);for(t=r-1;t>=0;t--){for(n=Array(r),i=t+2,a=r-1;a>=i;a-=2)n[a]=0,n[a-1]=0;for(a>t&&(n[a]=0),n[t]=e[t],a=t-1;a>=1;a-=2)n[a]=0,n[a-1]=0;0===a&&(n[0]=0),o[t]=n}return o}(o([e],1))}function l(e,t){var i,a,n,r,o,s,l,c,d,u,m;for(r=e.length,o=t.length,s=t[0].length,l=Array(r),i=r-1;i>=0;i--){for(c=Array(s),d=e[i],n=s-1;n>=0;n--){for(u=d[o-1]*t[o-1][n],a=o-2;a>=1;a-=2)m=a-1,u+=d[a]*t[a][n]+d[m]*t[m][n];0===a&&(u+=d[0]*t[0][n]),c[n]=u}l[i]=c}return l}function c(e,t){var i,a,n=e.length,r=e[n-1]*t[n-1];for(i=n-2;i>=1;i-=2)a=i-1,r+=e[i]*t[i]+e[a]*t[a];return 0===i&&(r+=e[0]*t[0]),r}function d(e){var t,i,a,n,r,o=e.length,s=e[0].length,l=Array(s);for(i=0;i<s;i++)l[i]=Array(o);for(t=o-1;t>=1;t-=2){for(n=e[t],a=e[t-1],i=s-1;i>=1;--i)(r=l[i])[t]=n[i],r[t-1]=a[i],(r=l[--i])[t]=n[i],r[t-1]=a[i];0===i&&((r=l[0])[t]=n[0],r[t-1]=a[0])}if(0===t){for(a=e[0],i=s-1;i>=1;--i)l[i][0]=a[i],l[--i][0]=a[i];0===i&&(l[0][0]=a[0])}return l}function u(e,t,a){if(a){var n=t;t=e,e=n}var o,u=[[e[0],e[1],1,0,0,0,-1*t[0]*e[0],-1*t[0]*e[1]],[0,0,0,e[0],e[1],1,-1*t[1]*e[0],-1*t[1]*e[1]],[e[2],e[3],1,0,0,0,-1*t[2]*e[2],-1*t[2]*e[3]],[0,0,0,e[2],e[3],1,-1*t[3]*e[2],-1*t[3]*e[3]],[e[4],e[5],1,0,0,0,-1*t[4]*e[4],-1*t[4]*e[5]],[0,0,0,e[4],e[5],1,-1*t[5]*e[4],-1*t[5]*e[5]],[e[6],e[7],1,0,0,0,-1*t[6]*e[6],-1*t[6]*e[7]],[0,0,0,e[6],e[7],1,-1*t[7]*e[6],-1*t[7]*e[7]]],m=t;try{o=function(e){var t,a,n,o,l,c,d,u,m=i(e),p=Math.abs,_=m[0],h=m[1],v=r(e),g=s(_);for(c=0;c<h;++c){var f=-1,b=-1;for(l=c;l!==_;++l)(d=p(v[l][c]))>b&&(f=l,b=d);for(a=v[f],v[f]=v[c],v[c]=a,o=g[f],g[f]=g[c],g[c]=o,u=a[c],d=c;d!==h;++d)a[d]/=u;for(d=h-1;-1!==d;--d)o[d]/=u;for(l=_-1;-1!==l;--l)if(l!==c){for(t=v[l],n=g[l],u=t[c],d=c+1;d!==h;++d)t[d]-=a[d]*u;for(d=h-1;d>0;--d)n[d]-=o[d]*u,n[--d]-=o[d]*u;0===d&&(n[0]-=o[0]*u)}}return g}(l(d(u),u))}catch(e){return[1,0,0,0,1,0,0,0]}for(var p,_=function(e,t){var i,a=e.length,n=Array(a);for(i=a-1;i>=0;i--)n[i]=c(e[i],t);return n}(l(o,d(u)),m),h=0;h<_.length;h++)_[h]=(p=_[h],Math.round(1e10*p)/1e10);return _[8]=1,_}Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t){var i=u(e,t,!1);return function(e,t){return function(e,t,i){var a=[];return a[0]=(e[0]*t+e[1]*i+e[2])/(e[6]*t+e[7]*i+1),a[1]=(e[3]*t+e[4]*i+e[5])/(e[6]*t+e[7]*i+1),a}(i,e,t)}}},zn(Pn={exports:{}},Pn.exports),Pn.exports),Tn=function(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}(Mn);!function(e){e[e.AFFINE=0]="AFFINE",e[e.PERSPECTIVE=1]="PERSPECTIVE"}(Sn||(Sn={}));class Cn{constructor(e){const t=null==e?void 0:e.map((e=>e.map)),i=null==e?void 0:e.map((e=>e.vacuum));if(t&&i)if(3===t.length)this.transformMode=Sn.AFFINE,this.mapToVacuumMatrix=wn(t,i),this.vacuumToMapMatrix=wn(i,t),this.calibrated=!(!this.mapToVacuumMatrix||!this.vacuumToMapMatrix);else{this.transformMode=Sn.PERSPECTIVE;const e=t.flatMap((e=>[e.x,e.y])),a=i.flatMap((e=>[e.x,e.y]));this.mapToVacuumTransformer=Tn(e,a),this.vacuumToMapTransformer=Tn(a,e),this.calibrated=!0}else this.calibrated=!1}mapToVacuum(e,t){if(this.transformMode===Sn.AFFINE&&this.mapToVacuumMatrix)return kn(this.mapToVacuumMatrix,[e,t]);if(this.transformMode===Sn.PERSPECTIVE&&this.mapToVacuumTransformer)return this.mapToVacuumTransformer(e,t);throw Error("Missing calibration")}vacuumToMap(e,t){if(this.transformMode===Sn.AFFINE&&this.vacuumToMapMatrix)return kn(this.vacuumToMapMatrix,[e,t]);if(this.transformMode===Sn.PERSPECTIVE&&this.vacuumToMapTransformer)return this.vacuumToMapTransformer(e,t);throw Error("Missing calibration")}}const Nn="   XIAOMI-VACUUM-MAP-CARD",Rn=`   ${Gi("common.version")} v2.0.8`,Ln=Math.max(Nn.length,Rn.length)+3,On=(e,t)=>e+" ".repeat(t-e.length);console.info(`%c${On(Nn,Ln)}\n%c${On(Rn,Ln)}`,"color: orange; font-weight: bold; background: black","color: white; font-weight: bold; background: dimgray");const $n=window;$n.customCards=$n.customCards||[],$n.customCards.push({type:"xiaomi-vacuum-map-card",name:"Xiaomi Vacuum Map Card",description:Gi("common.description"),preview:!0});let jn=class extends ne{constructor(){super(...arguments),this.oldConfig=!1,this.repeats=1,this.selectedMode=0,this.mapLocked=!1,this.configErrors=[],this.connected=!1,this.watchedEntities=[],this.selectedManualRectangles=[],this.selectedManualPath=new ln([],this._getContext()),this.selectedPredefinedRectangles=[],this.selectedRooms=[],this.selectedPredefinedPoint=[],this.selectablePredefinedRectangles=[],this.selectableRooms=[],this.selectablePredefinedPoints=[],this.modes=[]}static async getConfigElement(){return document.createElement("xiaomi-vacuum-map-card-editor")}static getStubConfig(e){const t=Object.keys(e.states),i=t.filter((e=>"camera"===e.substr(0,e.indexOf(".")))).filter((t=>null==e?void 0:e.states[t].attributes.calibration_points)),a=t.filter((e=>"vacuum"===e.substr(0,e.indexOf("."))));if(0!==i.length&&0!==a.length)return{type:"custom:xiaomi-vacuum-map-card",map_source:{camera:i[0]},calibration_source:{camera:!0},entity:a[0],vacuum_platform:"default"}}set hass(e){const t=!this._hass&&e;this._hass=e,this.lastHassUpdate=new Date,t&&this._firstHass()}get hass(){return this._hass}setConfig(e){if(!e)throw new Error(this._localize("common.invalid_configuration"));this.config=e,function(e){return e.map_image||e.map_camera}(e)?this.oldConfig=!0:(this.configErrors=function(e){var t,i,a;const n=[],r=(null!==(i=null===(t=e.additional_presets)||void 0===t?void 0:t.length)&&void 0!==i?i:0)>0;return hn(e,r,e.language).forEach((e=>n.push(e))),null===(a=e.additional_presets)||void 0===a||a.flatMap((t=>hn(t,r,e.language))).forEach((e=>n.push(e))),n.map((t=>Gi(t,e.language)))}(this.config),this.configErrors.length>0||(this.watchedEntities=function(e){var t;const i=new Set;return[e,...null!==(t=e.additional_presets)&&void 0!==t?t:[]].flatMap((t=>[...Va(t,e.language)])).forEach((e=>i.add(e))),[...i]}(this.config),this._setPresetIndex(0,!1,!0),this.requestUpdate("config")))}getCardSize(){return 12}_getCurrentPreset(){return this.currentPreset}_getCalibration(e){var t,i,a,n,r,o,s;return e.calibration_source.calibration_points&&[3,4].includes(e.calibration_source.calibration_points.length)?e.calibration_source.calibration_points:this.hass?e.calibration_source.entity&&!(null===(t=e.calibration_source)||void 0===t?void 0:t.attribute)?JSON.parse(null===(i=this.hass.states[e.calibration_source.entity])||void 0===i?void 0:i.state):e.calibration_source.entity&&(null===(a=e.calibration_source)||void 0===a?void 0:a.attribute)?null===(n=this.hass.states[e.calibration_source.entity])||void 0===n?void 0:n.attributes[e.calibration_source.attribute]:e.calibration_source.camera?null===(s=this.hass.states[null!==(o=null===(r=e.map_source)||void 0===r?void 0:r.camera)&&void 0!==o?o:""])||void 0===s?void 0:s.attributes.calibration_points:void 0:void 0}_firstHass(){0!==this.configErrors.length||this.oldConfig||this._setPresetIndex(this.presetIndex,!1,!0)}_setPresetIndex(e,t=!1,i=!1){var a,n,r,o,s,l,c,d,u,m,p,_,h,v;if((e=Math.min(Math.max(e,0),null!==(n=null===(a=this.config.additional_presets)||void 0===a?void 0:a.length)&&void 0!==n?n:0))===this.presetIndex&&!i)return;const g=0===e?this.config:(null!==(r=this.config.additional_presets)&&void 0!==r?r:[])[e-1];this.mapLocked||null===(o=this._getPinchZoom())||void 0===o||o.setTransform({scale:1,x:0,y:0,allowChangeEvent:!0}),t&&Ee("selection"),this.mapLocked=null!==(s=null==g?void 0:g.map_locked)&&void 0!==s&&s,this.selectedMode=0,this.realScale=1,this.mapScale=1,this.mapX=0,this.mapY=0,this.hass&&this._updateCalibration(g);const f=null!==(l=g.vacuum_platform)&&void 0!==l?l:"default";this.modes=(0===(null!==(d=null===(c=g.map_modes)||void 0===c?void 0:c.length)&&void 0!==d?d:0)?ka.generateDefaultModes(f):null!==(u=g.map_modes)&&void 0!==u?u:[]).map((e=>new ja(f,e,this.config.language))),this.presetIndex=e,this.currentPreset=g;const b=-1===(null!==(p=null===(m=g.icons)||void 0===m?void 0:m.length)&&void 0!==p?p:-1)?gn.generate(this.hass,g.entity,this.config.language):g.append_icons?[...gn.generate(this.hass,g.entity,this.config.language),...null!==(_=g.icons)&&void 0!==_?_:[]]:g.icons,y=-1===(null!==(v=null===(h=g.tiles)||void 0===h?void 0:h.length)&&void 0!==v?v:-1)?vn.generate(this.hass,g.entity,f,this.config.language):g.append_tiles?vn.generate(this.hass,g.entity,f,this.config.language).then((e=>{var t;return[...e,...null!==(t=g.tiles)&&void 0!==t?t:[]]})):new Promise((e=>{var t;return e(null!==(t=g.tiles)&&void 0!==t?t:[])}));y.then((e=>this._setPreset(Object.assign(Object.assign({},g),{tiles:e,icons:b})))).then((()=>setTimeout((()=>this.requestUpdate()),100))).then((()=>this._setCurrentMode(0,!1)))}_setPreset(e){this.currentPreset=e}_updateCalibration(e){this.coordinatesConverter=void 0;const t=this._getCalibration(e);this.coordinatesConverter=new Cn(t)}_getMapSrc(e){return e.map_source.camera?this.connected&&this.lastHassUpdate&&this.lastHassUpdate.getTime()+36e4>=(new Date).getTime()?`${this.hass.states[e.map_source.camera].attributes.entity_picture}&v=${+new Date}`:Aa:e.map_source.image?`${e.map_source.image}`:Aa}shouldUpdate(e){return!!this.config&&function(e,t,i,a){if(t.has("config")||i)return!0;const n=t.get("hass");return!n||e.some((e=>n.states[e]!==(null==a?void 0:a.states[e])))}(this.watchedEntities,e,!1,this.hass)}render(){var e,t,i,a;if(this.oldConfig)return this._showOldConfig();if(this.configErrors.length>0)return this._showConfigErrors(this.configErrors);const n=function(e,t){const i=Object.keys(t.states);return e.filter((e=>!i.includes(e)))}(this.watchedEntities,this.hass);if(n.length>0)return this._showInvalidEntities(n);const r=this._getCurrentPreset();this._updateCalibration(r);const o=r.tiles,s=r.icons,l=this.modes,c=this._getMapSrc(r),d=!!this.coordinatesConverter&&this.coordinatesConverter.calibrated,u=d?this._createMapControls():[],m=Xa(d,(()=>{var e,t,i,a,n,o,s,l;return j`
                <div
                    id="map-zoomer-content"
                    style="
                 margin-top: ${-1*(null!==(t=null===(e=r.map_source.crop)||void 0===e?void 0:e.top)&&void 0!==t?t:0)}px;
                 margin-bottom: ${-1*(null!==(a=null===(i=r.map_source.crop)||void 0===i?void 0:i.bottom)&&void 0!==a?a:0)}px;
                 margin-left: ${-1*(null!==(o=null===(n=r.map_source.crop)||void 0===n?void 0:n.left)&&void 0!==o?o:0)}px;
                 margin-right: ${-1*(null!==(l=null===(s=r.map_source.crop)||void 0===s?void 0:s.right)&&void 0!==l?l:0)}px;">
                    <img
                        id="map-image"
                        alt="camera_image"
                        class="${this.mapScale*this.realScale>1?"zoomed":""}"
                        src="${c}"
                        @load="${()=>this._calculateBasicScale()}" />
                    <div id="map-image-overlay">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            version="2.0"
                            id="svg-wrapper"
                            width="100%"
                            height="100%"
                            @mousedown="${e=>this._mouseDown(e)}"
                            @mousemove="${e=>this._mouseMove(e)}"
                            @mouseup="${e=>this._mouseUp(e)}">
                            ${this._drawSelection()}
                        </svg>
                    </div>
                </div>
            `}));return j`
            <ha-card
                .header="${this.config.title}"
                style="--map-scale: ${this.mapScale}; --real-scale: ${this.realScale};">
                ${Xa((null!==(t=null===(e=this.config.additional_presets)||void 0===e?void 0:e.length)&&void 0!==t?t:0)>0,(()=>{var e,t,i;return j`
                        <div class="preset-selector-wrapper">
                            <div
                                class="preset-selector-icon-wrapper"
                                @click="${()=>this._setPresetIndex(this.presetIndex-1,!0)}">
                                <ha-icon
                                    icon="mdi:chevron-left"
                                    class="preset-selector-icon ${0===this.presetIndex?"disabled":""}">
                                </ha-icon>
                            </div>
                            <div class="preset-label-wrapper">
                                <div class="preset-label">${r.preset_name}</div>
                                <div class="preset-indicator">
                                    ${new Array((null!==(t=null===(e=this.config.additional_presets)||void 0===e?void 0:e.length)&&void 0!==t?t:0)+1).fill(0).map(((e,t)=>t===this.presetIndex?"●":"○"))}
                                </div>
                            </div>
                            <div
                                class="preset-selector-icon-wrapper"
                                @click="${()=>this._setPresetIndex(this.presetIndex+1,!0)}">
                                <ha-icon
                                    icon="mdi:chevron-right"
                                    class="preset-selector-icon ${this.presetIndex===(null===(i=this.config.additional_presets)||void 0===i?void 0:i.length)?"disabled":""}">
                                </ha-icon>
                            </div>
                        </div>
                    `}))}
                ${d?j`
                          <div class="map-wrapper">
                              <pinch-zoom
                                  min-scale="0.5"
                                  id="map-zoomer"
                                  @change="${this._calculateScale}"
                                  two-finger-pan="${r.two_finger_pan}"
                                  locked="${this.mapLocked}"
                                  style="touch-action: none;">
                                  ${m}
                              </pinch-zoom>
                              <div id="map-zoomer-overlay">
                                  <div style="right: 0; top: 0; position: absolute;">
                                      <ha-icon
                                          icon="${this.mapLocked?"mdi:lock":"mdi:lock-open"}"
                                          class="standalone-icon-on-map clickable ripple"
                                          @click="${this._toggleLock}"></ha-icon>
                                  </div>
                                  <div
                                      class="map-zoom-icons"
                                      style="visibility: ${this.mapLocked?"hidden":"visible"}">
                                      <ha-icon
                                          icon="mdi:restore"
                                          class="icon-on-map clickable ripple"
                                          @click="${this._restoreMap}"></ha-icon>
                                      <div class="map-zoom-icons-main">
                                          <ha-icon
                                              icon="mdi:magnify-minus"
                                              class="icon-on-map clickable ripple"
                                              @click="${this._zoomOut}"></ha-icon>
                                          <ha-icon
                                              icon="mdi:magnify-plus"
                                              class="icon-on-map clickable ripple"
                                              @click="${this._zoomIn}"></ha-icon>
                                      </div>
                                  </div>
                              </div>
                          </div>
                      `:this._showInvalidCalibrationWarning()}
                <div class="controls-wrapper">
                    ${Xa(d&&(l.length>1||u.length>0),(()=>j`
                            <div class="map-controls-wrapper">
                                <div class="map-controls">
                                    ${Xa(l.length>1,(()=>xn.render(l,this.selectedMode,(e=>this._setCurrentMode(e)))))}
                                    ${Xa(u.length>0,(()=>j` <div class="map-actions-list">${u}</div> `))}
                                </div>
                            </div>
                        `))}
                    ${Xa(0!==(null!==(i=null==s?void 0:s.length)&&void 0!==i?i:0),(()=>j`
                            <div class="vacuum-controls">
                                <div class="vacuum-actions-list">
                                    ${null==s?void 0:s.filter((e=>Ua(e,this.hass))).map((e=>bn.render(e,this)))}
                                </div>
                            </div>
                        `))}
                    ${Xa(0!==(null!==(a=null==o?void 0:o.length)&&void 0!==a?a:0),(()=>j`
                            <div class="tiles-wrapper">
                                ${null==o?void 0:o.filter((e=>Ua(e,this.hass))).map((e=>fn.render(e,this)))}
                            </div>
                        `))}
                </div>
                ${yn.render()}
            </ha-card>
        `}_createMapControls(){const e=[],t=this._getCurrentMode();return t.selectionType===Ra.MANUAL_RECTANGLE&&e.push(j`
                <paper-button class="map-actions-item clickable ripple" @click="${()=>this._addRectangle()}">
                    <ha-icon icon="mdi:plus"></ha-icon>
                </paper-button>
            `),t.selectionType===Ra.MANUAL_PATH&&e.push(j`
                <paper-button
                    class="map-actions-item clickable ripple"
                    @click="${()=>{this.selectedManualPath.removeLast(),Ee("selection"),this.requestUpdate()}}">
                    <ha-icon icon="mdi:undo-variant"></ha-icon>
                </paper-button>
                <paper-button
                    class="map-actions-item clickable ripple"
                    @click="${()=>{this.selectedManualPath.clear(),Ee("selection"),this.requestUpdate()}}">
                    <ha-icon icon="mdi:delete-empty"></ha-icon>
                </paper-button>
            `),t.repeatsType!==La.NONE&&e.push(j`
                <paper-button
                    class="map-actions-item clickable ripple"
                    @click="${()=>{this.repeats=this.repeats%t.maxRepeats+1,Ee("selection")}}">
                    <div>×${this.repeats}</div>
                </paper-button>
            `),t.runImmediately||e.push(j`
                <paper-button
                    class="map-actions-item main clickable ripple"
                    @action="${this._handleRunAction()}"
                    .actionHandler="${Sa({hasHold:!0,hasDoubleClick:!0})}">
                    <ha-icon icon="mdi:play"></ha-icon>
                    <ha-icon
                        icon="${t.icon}"
                        style="position: absolute; transform: scale(0.5) translate(15px, -20px)"></ha-icon>
                </paper-button>
            `),e}_getContext(){return new nn((()=>this.mapScale),(()=>this.realScale),(e=>this._getMousePosition(e)),(()=>this.requestUpdate()),(()=>this.coordinatesConverter),(()=>this.selectedManualRectangles),(()=>this.selectedPredefinedRectangles),(()=>this.selectedRooms),(()=>this.selectedPredefinedPoint),(()=>this._getCurrentMode().coordinatesRounding),(()=>this._getCurrentMode().maxSelections),(e=>this._getCssProperty(e)),(()=>this._runImmediately()),(e=>this._localize(e)))}_getMousePosition(e){return qa(e,this._getSvgWrapper(),this.mapScale)}_setCurrentMode(e,t=!0){const i=this.modes[e];switch(this.selectedManualRectangles=[],this.selectedManualPoint=void 0,this.selectedManualPath.clear(),this.selectedPredefinedRectangles=[],this.selectedRooms=[],this.selectedPredefinedPoint=[],this.selectablePredefinedRectangles=[],this.selectableRooms=[],this.selectablePredefinedPoints=[],i.selectionType){case Ra.PREDEFINED_RECTANGLE:const e=dn.getFromEntities(i,this.hass,(()=>this._getContext())),t=i.predefinedSelections.map((e=>e)).filter((e=>"string"!=typeof e.zones)).map((e=>new dn(e,this._getContext())));this.selectablePredefinedRectangles=e.concat(t);break;case Ra.ROOM:this.selectableRooms=i.predefinedSelections.map((e=>new un(e,this._getContext())));break;case Ra.PREDEFINED_POINT:const a=cn.getFromEntities(i,this.hass,(()=>this._getContext())),n=i.predefinedSelections.map((e=>e)).filter((e=>"string"!=typeof e.position)).map((e=>new cn(e,this._getContext())));this.selectablePredefinedPoints=a.concat(n)}this.selectedMode!=e&&t&&Ee("selection"),this.selectedMode=e}_getCurrentMode(){return this.modes[this.selectedMode]}_getSelection(e){var t,i;const a=e.repeatsType===La.INTERNAL?this.repeats:null;switch(e.selectionType){case Ra.MANUAL_RECTANGLE:return this.selectedManualRectangles.map((e=>e.toVacuum(a)));case Ra.PREDEFINED_RECTANGLE:return this.selectedPredefinedRectangles.map((e=>e.toVacuum(a))).reduce(((e,t)=>e.concat(t)),[]);case Ra.ROOM:const e=this.selectedRooms.map((e=>e.toVacuum()));return[...e,...a&&e.length>0?[a]:[]];case Ra.MANUAL_PATH:return this.selectedManualPath.toVacuum(a);case Ra.MANUAL_POINT:return null!==(i=null===(t=this.selectedManualPoint)||void 0===t?void 0:t.toVacuum(a))&&void 0!==i?i:[];case Ra.PREDEFINED_POINT:return this.selectedPredefinedPoint.map((e=>e.toVacuum(a))).reduce(((e,t)=>e.concat(t)),[])}}_runImmediately(){return!!this._getCurrentMode().runImmediately&&(this._run(!1),!0)}_run(e){const t=this._getCurrentPreset(),i=this._getCurrentMode(),a=this._getSelection(i);if(0==a.length)this._showToast("popups.no_selection","mdi:close",!1),Ee("failure");else{const n=this.repeats,r=i.getServiceCall(t.entity,a,n),o=JSON.stringify(r,null,2);e?(this._showToast("popups.success","mdi:check",!0),console.log(o),window.alert(o),Ee("success")):this.hass.callService(r.domain,r.service,r.serviceData).then((()=>{this._showToast("popups.success","mdi:check",!0),Ee("success")}),(e=>{this._showToast("popups.failed","mdi:close",!1,e.message),Ee("failure")}))}}updated(e){this._updateElements()}connectedCallback(){super.connectedCallback(),this.connected=!0,this._updateElements(),this._delay(100).then((()=>this.requestUpdate()))}disconnectedCallback(){super.disconnectedCallback(),this.connected=!1}_updateElements(){var e,t,i;const a=null===(i=null===(t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector(".modes-dropdown-menu"))||void 0===t?void 0:t.shadowRoot)||void 0===i?void 0:i.querySelector(".dropdown-content");a&&(a.style.borderRadius=this._getCssProperty("--map-card-internal-big-radius")),this._delay(100).then((()=>this._calculateBasicScale()))}_drawSelection(){var e,t;switch(this._getCurrentMode().selectionType){case Ra.MANUAL_RECTANGLE:return I`${this.selectedManualRectangles.map((e=>e.render()))}`;case Ra.PREDEFINED_RECTANGLE:return I`${this.selectablePredefinedRectangles.map((e=>e.render()))}`;case Ra.ROOM:return I`${this.selectableRooms.map((e=>e.render()))}`;case Ra.MANUAL_PATH:return I`${null===(e=this.selectedManualPath)||void 0===e?void 0:e.render()}`;case Ra.MANUAL_POINT:return I`${null===(t=this.selectedManualPoint)||void 0===t?void 0:t.render()}`;case Ra.PREDEFINED_POINT:return I`${this.selectablePredefinedPoints.map((e=>e.render()))}`}}_toggleLock(){this.mapLocked=!this.mapLocked,Ee("selection"),this._delay(500).then((()=>this.requestUpdate()))}_addRectangle(){var e,t,i,a,n,r,o,s;const l=this._getCurrentPreset(),c=null!==(t=null===(e=l.map_source.crop)||void 0===e?void 0:e.top)&&void 0!==t?t:0,d=null!==(a=null===(i=l.map_source.crop)||void 0===i?void 0:i.bottom)&&void 0!==a?a:0,u=null!==(r=null===(n=l.map_source.crop)||void 0===n?void 0:n.left)&&void 0!==r?r:0,m=null!==(s=null===(o=l.map_source.crop)||void 0===o?void 0:o.right)&&void 0!==s?s:0;if(this._calculateBasicScale(),this.selectedManualRectangles.length>=this._getCurrentMode().maxSelections)return void Ee("failure");const p=this.realImageHeight*this.realScale-c-d,_=this.realImageWidth*this.realScale-u-m,h=(this.selectedManualRectangles.length+1).toString(),v=(_/3+u-this.mapX)/this.mapScale,g=(p/3+c-this.mapY)/this.mapScale,f=_/3/this.mapScale,b=p/3/this.mapScale;this.selectedManualRectangles.push(new an(v,g,f,b,h,this._getContext())),Ee("selection"),this.requestUpdate()}_mouseDown(e){e instanceof MouseEvent&&0!=e.button||(this.shouldHandleMouseUp=!0)}_mouseMove(e){e.target.classList.contains("draggable")||(this.selectedManualRectangles.filter((e=>e.isSelected())).forEach((t=>t.externalDrag(e))),this.shouldHandleMouseUp=!1)}_mouseUp(e){if(!(e instanceof MouseEvent&&0!=e.button)&&this.shouldHandleMouseUp){const{x:t,y:i}=qa(e,this._getSvgWrapper(),1);switch(this._getCurrentMode().selectionType){case Ra.MANUAL_PATH:Ee("selection"),this.selectedManualPath.addPoint(t,i);break;case Ra.MANUAL_POINT:Ee("selection"),this.selectedManualPoint=new on(t,i,this._getContext());break;default:return}Da(e),this.requestUpdate()}this.shouldHandleMouseUp=!1}_handleRunAction(){return e=>{if(this.hass&&e.detail.action)switch(e.detail.action){case"tap":this._run(!1);break;case"hold":this._run(!0);break;case"double_tap":console.log(JSON.stringify(Object.assign(Object.assign({},this._getCurrentPreset()),{additional_presets:void 0,title:void 0,type:void 0}),null,2)),window.alert("Configuration available in browser's console"),Ee("success")}}}_restoreMap(){const e=this._getMapZoomerContent();e.style.transitionDuration=this._getCssProperty("--map-card-internal-transitions-duration"),this._getPinchZoom().setTransform({scale:1,x:0,y:0,allowChangeEvent:!0}),this.mapScale=1,Ee("selection"),this._delay(300).then((()=>e.style.transitionDuration="0s"))}_getCssProperty(e){return getComputedStyle(this._getMapImage()).getPropertyValue(e)}_zoomIn(){Ee("selection"),this._updateScale(1.5)}_zoomOut(){Ee("selection"),this._updateScale(1/1.5)}_updateScale(e){const t=this._getMapZoomerContent(),i=this._getPinchZoom(),a=this._getPinchZoom().getBoundingClientRect();this.mapScale=Math.max(this.mapScale*e,.5),t.style.transitionDuration="200ms",i.scaleTo(this.mapScale,{originX:a.left+a.width/2,originY:a.top+a.height/2,relativeTo:"container",allowChangeEvent:!0}),this._delay(300).then((()=>t.style.transitionDuration="0s"))}_calculateBasicScale(){const e=this._getMapImage();e&&e.naturalWidth>0&&(this.realImageWidth=e.naturalWidth,this.realImageHeight=e.naturalHeight,this.realScale=e.width/e.naturalWidth)}_calculateScale(){const e=this._getPinchZoom();this.mapScale=e.scale,this.mapX=e.x,this.mapY=e.y}_getPinchZoom(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.getElementById("map-zoomer")}_getMapImage(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.getElementById("map-image")}_getMapZoomerContent(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.getElementById("map-zoomer-content")}_getSvgWrapper(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("#svg-wrapper")}_showConfigErrors(e){e.forEach((e=>console.error(e)));const t=document.createElement("hui-error-card");return t.setConfig({type:"error",error:e[0],origConfig:this.config}),j` ${t} `}_showOldConfig(){return j`
            <hui-warning>
                <h1>Xiaomi Vacuum Map Card ${"v2.0.8"}</h1>
                <p>${this._localize("common.old_configuration")}</p>
                <p>
                    <a
                        href="https://github.com/PiotrMachowski/lovelace-xiaomi-vacuum-map-card#migrating-from-v1xx"
                        target="_blank"
                        >${this._localize("common.old_configuration_migration_link")}</a
                    >
                </p>
            </hui-warning>
        `}_showInvalidEntities(e){return j`
            <hui-warning>
                <h1>${this._localize("validation.invalid_entities")}</h1>
                <ul>
                    ${e.map((e=>j` <li>
                            <pre>${e}</pre>
                        </li>`))}
                </ul>
            </hui-warning>
        `}_showInvalidCalibrationWarning(){return j` <hui-warning>${this._localize("validation.invalid_calibration")}</hui-warning> `}_localize(e){return Wi(e,this.hass,this.config)}async _delay(e){await new Promise((t=>setTimeout((()=>t()),e)))}_showToast(e,t,i,a=""){var n,r,o;const s=null===(n=this.shadowRoot)||void 0===n?void 0:n.getElementById("toast"),l=null===(r=this.shadowRoot)||void 0===r?void 0:r.getElementById("toast-text"),c=null===(o=this.shadowRoot)||void 0===o?void 0:o.getElementById("toast-icon");s&&l&&c&&(s.className="show",l.innerText=this._localize(e)+(a?`\n${a}`:""),c.children[0].setAttribute("icon",t),c.style.color=i?"var(--map-card-internal-toast-successful-icon-color)":"var(--map-card-internal-toast-unsuccessful-icon-color)",this._delay(2e3).then((()=>s.className=s.className.replace("show",""))))}static get styles(){return o`
            ha-card {
                overflow: hidden;
                display: flow-root;
                --map-card-internal-primary-color: var(--map-card-primary-color, var(--slider-color));
                --map-card-internal-primary-text-color: var(--map-card-primary-text-color, var(--primary-text-color));
                --map-card-internal-secondary-color: var(--map-card-secondary-color, var(--slider-secondary-color));
                --map-card-internal-secondary-text-color: var(
                    --map-card-secondary-text-color,
                    var(--text-light-primary-color)
                );
                --map-card-internal-tertiary-color: var(--map-card-tertiary-color, var(--secondary-background-color));
                --map-card-internal-tertiary-text-color: var(--map-card-tertiary-text-color, var(--primary-text-color));
                --map-card-internal-disabled-text-color: var(
                    --map-card-disabled-text-color,
                    var(--disabled-text-color)
                );
                --map-card-internal-zoomer-background: var(
                    --map-card-zoomer-background,
                    var(--map-card-internal-tertiary-color)
                );
                --map-card-internal-ripple-color: var(--map-card-ripple-color, #7a7f87);
                --map-card-internal-big-radius: var(--map-card-big-radius, 25px);
                --map-card-internal-small-radius: var(--map-card-small-radius, 18px);
                --map-card-internal-predefined-point-icon-wrapper-size: var(
                    --map-card-predefined-point-icon-wrapper-size,
                    36px
                );
                --map-card-internal-predefined-point-icon-size: var(--map-card-predefined-point-icon-size, 24px);
                --map-card-internal-predefined-point-icon-color: var(
                    --map-card-predefined-point-icon-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-predefined-point-icon-color-selected: var(
                    --map-card-predefined-point-icon-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-predefined-point-icon-background-color: var(
                    --map-card-predefined-point-icon-background-color,
                    var(--map-card-internal-secondary-color)
                );
                --map-card-internal-predefined-point-icon-background-color-selected: var(
                    --map-card-predefined-point-icon-background-color-selected,
                    var(--map-card-internal-primary-color)
                );
                --map-card-internal-predefined-point-label-color: var(
                    --map-card-predefined-point-label-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-predefined-point-label-color-selected: var(
                    --map-card-predefined-point-label-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-predefined-point-label-font-size: var(
                    --map-card-predefined-point-label-font-size,
                    12px
                );
                --map-card-internal-manual-point-radius: var(--map-card-manual-point-radius, 5px);
                --map-card-internal-manual-point-line-color: var(--map-card-manual-point-line-color, yellow);
                --map-card-internal-manual-point-fill-color: var(--map-card-manual-point-fill-color, transparent);
                --map-card-internal-manual-point-line-width: var(--map-card-manual-point-line-width, 1px);
                --map-card-internal-manual-path-point-radius: var(--map-card-manual-path-point-radius, 5px);
                --map-card-internal-manual-path-point-line-color: var(--map-card-manual-path-point-line-color, yellow);
                --map-card-internal-manual-path-point-fill-color: var(
                    --map-card-manual-path-point-fill-color,
                    transparent
                );
                --map-card-internal-manual-path-point-line-width: var(--map-card-manual-path-point-line-width, 1px);
                --map-card-internal-manual-path-line-color: var(--map-card-manual-path-line-color, yellow);
                --map-card-internal-manual-path-line-width: var(--map-card-manual-path-line-width, 1px);
                --map-card-internal-predefined-rectangle-line-width: var(
                    --map-card-predefined-rectangle-line-width,
                    1px
                );
                --map-card-internal-predefined-rectangle-line-color: var(
                    --map-card-predefined-rectangle-line-color,
                    white
                );
                --map-card-internal-predefined-rectangle-fill-color: var(
                    --map-card-predefined-rectangle-fill-color,
                    transparent
                );
                --map-card-internal-predefined-rectangle-line-color-selected: var(
                    --map-card-predefined-rectangle-line-color-selected,
                    white
                );
                --map-card-internal-predefined-rectangle-fill-color-selected: var(
                    --map-card-predefined-rectangle-fill-color-selected,
                    rgba(255, 255, 255, 0.2)
                );
                --map-card-internal-predefined-rectangle-line-segment-line: var(
                    --map-card-predefined-rectangle-line-segment-line,
                    10px
                );
                --map-card-internal-predefined-rectangle-line-segment-gap: var(
                    --map-card-predefined-rectangle-line-segment-gap,
                    5px
                );
                --map-card-internal-predefined-rectangle-icon-wrapper-size: var(
                    --map-card-predefined-rectangle-icon-wrapper-size,
                    36px
                );
                --map-card-internal-predefined-rectangle-icon-size: var(
                    --map-card-predefined-rectangle-icon-size,
                    24px
                );
                --map-card-internal-predefined-rectangle-icon-color: var(
                    --map-card-predefined-rectangle-icon-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-predefined-rectangle-icon-color-selected: var(
                    --map-card-predefined-rectangle-icon-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-predefined-rectangle-icon-background-color: var(
                    --map-card-predefined-rectangle-icon-background-color,
                    var(--map-card-internal-secondary-color)
                );
                --map-card-internal-predefined-rectangle-icon-background-color-selected: var(
                    --map-card-predefined-rectangle-icon-background-color-selected,
                    var(--map-card-internal-primary-color)
                );
                --map-card-internal-predefined-rectangle-label-color: var(
                    --map-card-predefined-rectangle-label-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-predefined-rectangle-label-color-selected: var(
                    --map-card-predefined-rectangle-label-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-predefined-rectangle-label-font-size: var(
                    --map-card-predefined-rectangle-label-font-size,
                    12px
                );
                --map-card-internal-manual-rectangle-line-width: var(--map-card-manual-rectangle-line-width, 1px);
                --map-card-internal-manual-rectangle-line-color: var(--map-card-manual-rectangle-line-color, white);
                --map-card-internal-manual-rectangle-fill-color: var(
                    --map-card-manual-rectangle-fill-color,
                    rgba(255, 255, 255, 0.2)
                );
                --map-card-internal-manual-rectangle-line-color-selected: var(
                    --map-card-manual-rectangle-line-color-selected,
                    white
                );
                --map-card-internal-manual-rectangle-fill-color-selected: var(
                    --map-card-manual-rectangle-fill-color-selected,
                    transparent
                );
                --map-card-internal-manual-rectangle-line-segment-line: var(
                    --map-card-manual-rectangle-line-segment-line,
                    10px
                );
                --map-card-internal-manual-rectangle-line-segment-gap: var(
                    --map-card-manual-rectangle-line-segment-gap,
                    5px
                );
                --map-card-internal-manual-rectangle-description-color: var(
                    --map-card-manual-rectangle-description-color,
                    white
                );
                --map-card-internal-manual-rectangle-description-font-size: var(
                    --map-card-manual-rectangle-description-font-size,
                    12px
                );
                --map-card-internal-manual-rectangle-description-offset-x: var(
                    --map-card-manual-rectangle-description-offset-x,
                    2px
                );
                --map-card-internal-manual-rectangle-description-offset-y: var(
                    --map-card-manual-rectangle-description-offset-y,
                    -8px
                );
                --map-card-internal-manual-rectangle-delete-circle-radius: var(
                    --map-card-manual-rectangle-delete-circle-radius,
                    13px
                );
                --map-card-internal-manual-rectangle-delete-circle-line-color: var(
                    --map-card-manual-rectangle-delete-circle-line-color,
                    white
                );
                --map-card-internal-manual-rectangle-delete-circle-fill-color: var(
                    --map-card-manual-rectangle-delete-circle-fill-color,
                    var(--map-card-internal-secondary-color)
                );
                --map-card-internal-manual-rectangle-delete-circle-line-color-selected: var(
                    --map-card-manual-rectangle-delete-circle-line-color-selected,
                    white
                );
                --map-card-internal-manual-rectangle-delete-circle-fill-color-selected: var(
                    --map-card-manual-rectangle-delete-circle-fill-color-selected,
                    var(--map-card-internal-primary-color)
                );
                --map-card-internal-manual-rectangle-delete-circle-line-width: var(
                    --map-card-manual-rectangle-delete-circle-line-width,
                    1px
                );
                --map-card-internal-manual-rectangle-delete-icon-color: var(
                    --map-card-manual-rectangle-delete-icon-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-manual-rectangle-delete-icon-color-selected: var(
                    --map-card-manual-rectangle-delete-icon-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-manual-rectangle-resize-circle-radius: var(
                    --map-card-manual-rectangle-resize-circle-radius,
                    13px
                );
                --map-card-internal-manual-rectangle-resize-circle-line-color: var(
                    --map-card-manual-rectangle-resize-circle-line-color,
                    white
                );
                --map-card-internal-manual-rectangle-resize-circle-fill-color: var(
                    --map-card-manual-rectangle-resize-circle-fill-color,
                    var(--map-card-internal-secondary-color)
                );
                --map-card-internal-manual-rectangle-resize-circle-line-color-selected: var(
                    --map-card-manual-rectangle-resize-circle-line-color-selected,
                    white
                );
                --map-card-internal-manual-rectangle-resize-circle-fill-color-selected: var(
                    --map-card-manual-rectangle-resize-circle-fill-color-selected,
                    var(--map-card-internal-primary-color)
                );
                --map-card-internal-manual-rectangle-resize-circle-line-width: var(
                    --map-card-manual-rectangle-resize-circle-line-width,
                    1px
                );
                --map-card-internal-manual-rectangle-resize-icon-color: var(
                    --map-card-manual-rectangle-resize-icon-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-manual-rectangle-resize-icon-color-selected: var(
                    --map-card-manual-rectangle-resize-icon-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-room-outline-line-color: var(--map-card-room-outline-line-color, white);
                --map-card-internal-room-outline-line-width: var(--map-card-room-outline-line-width, 1px);
                --map-card-internal-room-outline-line-segment-line: var(
                    --map-card-room-outline-line-segment-line,
                    10px
                );
                --map-card-internal-room-outline-line-segment-gap: var(--map-card-room-outline-line-segment-gap, 5px);
                --map-card-internal-room-outline-fill-color: var(--map-card-room-outline-fill-color, transparent);
                --map-card-internal-room-outline-line-color-selected: var(
                    --map-card-room-outline-line-color-selected,
                    white
                );
                --map-card-internal-room-outline-fill-color-selected: var(
                    --map-card-room-outline-fill-color-selected,
                    rgba(255, 255, 255, 0.3)
                );
                --map-card-internal-room-icon-wrapper-size: var(--map-card-room-icon-wrapper-size, 36px);
                --map-card-internal-room-icon-size: var(--map-card-room-icon-size, 24px);
                --map-card-internal-room-icon-color: var(
                    --map-card-room-icon-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-room-icon-color-selected: var(
                    --map-card-room-icon-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-room-icon-background-color: var(
                    --map-card-room-icon-background-color,
                    var(--map-card-internal-secondary-color)
                );
                --map-card-internal-room-icon-background-color-selected: var(
                    --map-card-room-icon-background-color-selected,
                    var(--map-card-internal-primary-color)
                );
                --map-card-internal-room-label-color: var(
                    --map-card-room-color,
                    var(--map-card-internal-secondary-text-color)
                );
                --map-card-internal-room-label-color-selected: var(
                    --map-card-room-label-color-selected,
                    var(--map-card-internal-primary-text-color)
                );
                --map-card-internal-room-label-font-size: var(--map-card-room-label-font-size, 12px);
                --map-card-internal-toast-successful-icon-color: var(
                    --map-card-toast-successful-icon-color,
                    rgb(0, 255, 0)
                );
                --map-card-internal-toast-unsuccessful-icon-color: var(
                    --map-card-toast-unsuccessful-icon-color,
                    rgb(255, 0, 0)
                );
                --map-card-internal-transitions-duration: var(--map-card-transitions-duration, 200ms);
            }

            .clickable {
                cursor: pointer;
            }

            .preset-selector-wrapper {
                width: 100%;
                display: inline-flex;
                align-content: center;
                justify-content: space-between;
                align-items: center;
            }

            .preset-selector-icon-wrapper {
                height: 44px;
                width: 44px;
                display: grid;
                place-items: center;
            }

            .preset-selector-icon {
                cursor: pointer;
            }

            .preset-selector-icon.disabled {
                color: var(--map-card-internal-disabled-text-color);
                cursor: default;
            }

            .preset-label-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .preset-indicator {
                line-height: 50%;
            }

            .map-wrapper {
                position: relative;
                height: max-content;
            }

            #map-zoomer {
                overflow: hidden;
                display: block;
                --scale: 1;
                --x: 0;
                --y: 0;
                background: var(--map-card-internal-zoomer-background);
            }

            #map-zoomer-content {
                transform: translate(var(--x), var(--y)) scale(var(--scale));
                transform-origin: 0 0;
                position: relative;
            }

            #map-image {
                width: 100%;
                margin-bottom: -6px;
            }

            #map-image.zoomed {
                image-rendering: pixelated;
            }

            #map-image-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }

            .standalone-icon-on-map {
                background-color: var(--map-card-internal-secondary-color);
                color: var(--map-card-internal-secondary-text-color);
                border-radius: var(--map-card-internal-small-radius);
                margin: 5px;
                width: 36px;
                height: 36px;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .map-zoom-icons {
                right: 0;
                bottom: 0;
                position: absolute;
                display: inline-flex;
                background-color: var(--map-card-internal-secondary-color);
                color: var(--map-card-internal-secondary-text-color);
                border-radius: var(--map-card-internal-small-radius);
                margin: 5px;
            }

            .map-zoom-icons-main {
                display: inline-flex;
                border-radius: var(--map-card-internal-small-radius);
                background-color: var(--map-card-internal-primary-color);
                color: var(--map-card-internal-primary-text-color);
            }

            .icon-on-map {
                touch-action: auto;
                pointer-events: auto;
                height: 36px;
                width: 36px;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .controls-wrapper {
                margin: 15px;
            }

            .controls-wrapper > * {
                margin-top: 10px;
                margin-bottom: 10px;
            }

            .map-controls {
                width: 100%;
                display: inline-flex;
                gap: 10px;
                place-content: space-between;
                flex-wrap: wrap;
            }

            .map-actions-list {
                border-radius: var(--map-card-internal-big-radius);
                overflow: hidden;
                background-color: var(--map-card-internal-secondary-color);
                color: var(--map-card-internal-secondary-text-color);
                margin-left: auto;
                display: inline-flex;
            }

            .map-actions-item.main {
                border-radius: var(--map-card-internal-big-radius);
                background-color: var(--map-card-internal-primary-color);
                color: var(--map-card-internal-primary-text-color);
            }

            .map-actions-item {
                width: 50px;
                height: 50px;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: transparent;
            }

            .vacuum-controls {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .vacuum-actions-list {
                float: right;
                border-radius: var(--map-card-internal-big-radius);
                overflow: hidden;
                background-color: var(--map-card-internal-secondary-color);
                color: var(--map-card-internal-secondary-text-color);
            }

            .tiles-wrapper {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-evenly;
                align-items: stretch;
                gap: 5px;
            }

            .ripple {
                position: relative;
                overflow: hidden;
                transform: translate3d(0, 0, 0);
            }

            .ripple:after {
                content: "";
                display: block;
                position: absolute;
                border-radius: 50%;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                background-image: radial-gradient(circle, var(--map-card-internal-ripple-color) 2%, transparent 10.01%);
                background-repeat: no-repeat;
                background-position: 50%;
                transform: scale(10, 10);
                opacity: 0;
                transition: transform 0.5s, opacity 1s;
            }

            .ripple:active:after {
                transform: scale(0, 0);
                opacity: 0.7;
                transition: 0s;
            }

            ${en.styles}
            ${an.styles}
          ${dn.styles}
          ${ln.styles}
          ${on.styles}
          ${cn.styles}
          ${un.styles}
          ${xn.styles}
          ${bn.styles}
          ${fn.styles}
          ${yn.styles}
        `}};e([se({attribute:!1})],jn.prototype,"_hass",void 0),e([le()],jn.prototype,"oldConfig",void 0),e([le()],jn.prototype,"config",void 0),e([le()],jn.prototype,"presetIndex",void 0),e([le()],jn.prototype,"realScale",void 0),e([le()],jn.prototype,"realImageWidth",void 0),e([le()],jn.prototype,"realImageHeight",void 0),e([le()],jn.prototype,"mapScale",void 0),e([le()],jn.prototype,"mapX",void 0),e([le()],jn.prototype,"mapY",void 0),e([le()],jn.prototype,"repeats",void 0),e([le()],jn.prototype,"selectedMode",void 0),e([le()],jn.prototype,"mapLocked",void 0),e([le()],jn.prototype,"configErrors",void 0),e([le()],jn.prototype,"connected",void 0),jn=e([re("xiaomi-vacuum-map-card")],jn);export{jn as XiaomiVacuumMapCard};
