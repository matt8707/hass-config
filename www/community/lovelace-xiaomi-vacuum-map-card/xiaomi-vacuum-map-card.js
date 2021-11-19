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
function e(e,t,a,i){var n,r=arguments.length,o=r<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,a):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,a,i);else for(var s=e.length-1;s>=0;s--)(n=e[s])&&(o=(r<3?n(o):r>3?n(t,a,o):n(t,a))||o);return r>3&&o&&Object.defineProperty(t,a,o),o
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */}const t=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,a=Symbol();class i{constructor(e,t){if(t!==a)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return t&&void 0===this.t&&(this.t=new CSSStyleSheet,this.t.replaceSync(this.cssText)),this.t}toString(){return this.cssText}}const n=new Map,r=e=>{let t=n.get(e);return void 0===t&&n.set(e,t=new i(e,a)),t},o=(e,...t)=>{const a=1===e.length?e[0]:t.reduce(((t,a,n)=>t+(e=>{if(e instanceof i)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(a)+e[n+1]),e[0]);return r(a)},s=t?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const a of e.cssRules)t+=a.cssText;return(e=>r("string"==typeof e?e:e+""))(t)})(e):e
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */;var l,c,d,p;const u={toAttribute(e,t){switch(t){case Boolean:e=e?"":null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let a=e;switch(t){case Boolean:a=null!==e;break;case Number:a=null===e?null:Number(e);break;case Object:case Array:try{a=JSON.parse(e)}catch(e){a=null}}return a}},m=(e,t)=>t!==e&&(t==t||e==e),h={attribute:!0,type:String,converter:u,reflect:!1,hasChanged:m};class v extends HTMLElement{constructor(){super(),this.Πi=new Map,this.Πo=void 0,this.Πl=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this.Πh=null,this.u()}static addInitializer(e){var t;null!==(t=this.v)&&void 0!==t||(this.v=[]),this.v.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,a)=>{const i=this.Πp(a,t);void 0!==i&&(this.Πm.set(i,a),e.push(i))})),e}static createProperty(e,t=h){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const a="symbol"==typeof e?Symbol():"__"+e,i=this.getPropertyDescriptor(e,a,t);void 0!==i&&Object.defineProperty(this.prototype,e,i)}}static getPropertyDescriptor(e,t,a){return{get(){return this[t]},set(i){const n=this[e];this[t]=i,this.requestUpdate(e,n,a)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||h}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this.Πm=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const a of t)this.createProperty(a,e[a])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const a=new Set(e.flat(1/0).reverse());for(const e of a)t.unshift(s(e))}else void 0!==e&&t.push(s(e));return t}static"Πp"(e,t){const a=t.attribute;return!1===a?void 0:"string"==typeof a?a:"string"==typeof e?e.toLowerCase():void 0}u(){var e;this.Πg=new Promise((e=>this.enableUpdating=e)),this.L=new Map,this.Π_(),this.requestUpdate(),null===(e=this.constructor.v)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,a;(null!==(t=this.ΠU)&&void 0!==t?t:this.ΠU=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(a=e.hostConnected)||void 0===a||a.call(e))}removeController(e){var t;null===(t=this.ΠU)||void 0===t||t.splice(this.ΠU.indexOf(e)>>>0,1)}"Π_"(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this.Πi.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const a=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return((e,a)=>{t?e.adoptedStyleSheets=a.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):a.forEach((t=>{const a=document.createElement("style");a.textContent=t.cssText,e.appendChild(a)}))})(a,this.constructor.elementStyles),a}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)})),this.Πl&&(this.Πl(),this.Πo=this.Πl=void 0)}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)})),this.Πo=new Promise((e=>this.Πl=e))}attributeChangedCallback(e,t,a){this.K(e,a)}"Πj"(e,t,a=h){var i,n;const r=this.constructor.Πp(e,a);if(void 0!==r&&!0===a.reflect){const o=(null!==(n=null===(i=a.converter)||void 0===i?void 0:i.toAttribute)&&void 0!==n?n:u.toAttribute)(t,a.type);this.Πh=e,null==o?this.removeAttribute(r):this.setAttribute(r,o),this.Πh=null}}K(e,t){var a,i,n;const r=this.constructor,o=r.Πm.get(e);if(void 0!==o&&this.Πh!==o){const e=r.getPropertyOptions(o),s=e.converter,l=null!==(n=null!==(i=null===(a=s)||void 0===a?void 0:a.fromAttribute)&&void 0!==i?i:"function"==typeof s?s:null)&&void 0!==n?n:u.fromAttribute;this.Πh=o,this[o]=l(t,e.type),this.Πh=null}}requestUpdate(e,t,a){let i=!0;void 0!==e&&(((a=a||this.constructor.getPropertyOptions(e)).hasChanged||m)(this[e],t)?(this.L.has(e)||this.L.set(e,t),!0===a.reflect&&this.Πh!==e&&(void 0===this.Πk&&(this.Πk=new Map),this.Πk.set(e,a))):i=!1),!this.isUpdatePending&&i&&(this.Πg=this.Πq())}async"Πq"(){this.isUpdatePending=!0;try{for(await this.Πg;this.Πo;)await this.Πo}catch(e){Promise.reject(e)}const e=this.performUpdate();return null!=e&&await e,!this.isUpdatePending}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this.Πi&&(this.Πi.forEach(((e,t)=>this[t]=e)),this.Πi=void 0);let t=!1;const a=this.L;try{t=this.shouldUpdate(a),t?(this.willUpdate(a),null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(a)):this.Π$()}catch(e){throw t=!1,this.Π$(),e}t&&this.E(a)}willUpdate(e){}E(e){var t;null===(t=this.ΠU)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}"Π$"(){this.L=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this.Πg}shouldUpdate(e){return!0}update(e){void 0!==this.Πk&&(this.Πk.forEach(((e,t)=>this.Πj(t,this[t],e))),this.Πk=void 0),this.Π$()}updated(e){}firstUpdated(e){}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var _,g,f,b;v.finalized=!0,v.elementProperties=new Map,v.elementStyles=[],v.shadowRootOptions={mode:"open"},null===(c=(l=globalThis).reactiveElementPlatformSupport)||void 0===c||c.call(l,{ReactiveElement:v}),(null!==(d=(p=globalThis).reactiveElementVersions)&&void 0!==d?d:p.reactiveElementVersions=[]).push("1.0.0-rc.2");const y=globalThis.trustedTypes,x=y?y.createPolicy("lit-html",{createHTML:e=>e}):void 0,w=`lit$${(Math.random()+"").slice(9)}$`,E="?"+w,k=`<${E}>`,z=document,P=(e="")=>z.createComment(e),M=e=>null===e||"object"!=typeof e&&"function"!=typeof e,S=Array.isArray,C=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,T=/-->/g,$=/>/g,N=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,A=/'/g,R=/"/g,L=/^(?:script|style|textarea)$/i,O=e=>(t,...a)=>({_$litType$:e,strings:t,values:a}),I=O(1),j=O(2),D=Symbol.for("lit-noChange"),F=Symbol.for("lit-nothing"),U=new WeakMap,V=z.createTreeWalker(z,129,null,!1);class q{constructor({strings:e,_$litType$:t},a){let i;this.parts=[];let n=0,r=0;const o=e.length-1,s=this.parts,[l,c]=((e,t)=>{const a=e.length-1,i=[];let n,r=2===t?"<svg>":"",o=C;for(let t=0;t<a;t++){const a=e[t];let s,l,c=-1,d=0;for(;d<a.length&&(o.lastIndex=d,l=o.exec(a),null!==l);)d=o.lastIndex,o===C?"!--"===l[1]?o=T:void 0!==l[1]?o=$:void 0!==l[2]?(L.test(l[2])&&(n=RegExp("</"+l[2],"g")),o=N):void 0!==l[3]&&(o=N):o===N?">"===l[0]?(o=null!=n?n:C,c=-1):void 0===l[1]?c=-2:(c=o.lastIndex-l[2].length,s=l[1],o=void 0===l[3]?N:'"'===l[3]?R:A):o===R||o===A?o=N:o===T||o===$?o=C:(o=N,n=void 0);const p=o===N&&e[t+1].startsWith("/>")?" ":"";r+=o===C?a+k:c>=0?(i.push(s),a.slice(0,c)+"$lit$"+a.slice(c)+w+p):a+w+(-2===c?(i.push(void 0),t):p)}const s=r+(e[a]||"<?>")+(2===t?"</svg>":"");return[void 0!==x?x.createHTML(s):s,i]})(e,t);if(this.el=q.createElement(l,a),V.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(i=V.nextNode())&&s.length<o;){if(1===i.nodeType){if(i.hasAttributes()){const e=[];for(const t of i.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(w)){const a=c[r++];if(e.push(t),void 0!==a){const e=i.getAttribute(a.toLowerCase()+"$lit$").split(w),t=/([.?@])?(.*)/.exec(a);s.push({type:1,index:n,name:t[2],strings:e,ctor:"."===t[1]?W:"?"===t[1]?G:"@"===t[1]?Z:Y})}else s.push({type:6,index:n})}for(const t of e)i.removeAttribute(t)}if(L.test(i.tagName)){const e=i.textContent.split(w),t=e.length-1;if(t>0){i.textContent=y?y.emptyScript:"";for(let a=0;a<t;a++)i.append(e[a],P()),V.nextNode(),s.push({type:2,index:++n});i.append(e[t],P())}}}else if(8===i.nodeType)if(i.data===E)s.push({type:2,index:n});else{let e=-1;for(;-1!==(e=i.data.indexOf(w,e+1));)s.push({type:7,index:n}),e+=w.length-1}n++}}static createElement(e,t){const a=z.createElement("template");return a.innerHTML=e,a}}function H(e,t,a=e,i){var n,r,o,s;if(t===D)return t;let l=void 0!==i?null===(n=a.Σi)||void 0===n?void 0:n[i]:a.Σo;const c=M(t)?void 0:t._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(r=null==l?void 0:l.O)||void 0===r||r.call(l,!1),void 0===c?l=void 0:(l=new c(e),l.T(e,a,i)),void 0!==i?(null!==(o=(s=a).Σi)&&void 0!==o?o:s.Σi=[])[i]=l:a.Σo=l),void 0!==l&&(t=H(e,l.S(e,t.values),l,i)),t}class B{constructor(e,t){this.l=[],this.N=void 0,this.D=e,this.M=t}u(e){var t;const{el:{content:a},parts:i}=this.D,n=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:z).importNode(a,!0);V.currentNode=n;let r=V.nextNode(),o=0,s=0,l=i[0];for(;void 0!==l;){if(o===l.index){let t;2===l.type?t=new X(r,r.nextSibling,this,e):1===l.type?t=new l.ctor(r,l.name,l.strings,this,e):6===l.type&&(t=new K(r,this,e)),this.l.push(t),l=i[++s]}o!==(null==l?void 0:l.index)&&(r=V.nextNode(),o++)}return n}v(e){let t=0;for(const a of this.l)void 0!==a&&(void 0!==a.strings?(a.I(e,a,t),t+=a.strings.length-2):a.I(e[t])),t++}}class X{constructor(e,t,a,i){this.type=2,this.N=void 0,this.A=e,this.B=t,this.M=a,this.options=i}setConnected(e){var t;null===(t=this.P)||void 0===t||t.call(this,e)}get parentNode(){return this.A.parentNode}get startNode(){return this.A}get endNode(){return this.B}I(e,t=this){e=H(this,e,t),M(e)?e===F||null==e||""===e?(this.H!==F&&this.R(),this.H=F):e!==this.H&&e!==D&&this.m(e):void 0!==e._$litType$?this._(e):void 0!==e.nodeType?this.$(e):(e=>{var t;return S(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])})(e)?this.g(e):this.m(e)}k(e,t=this.B){return this.A.parentNode.insertBefore(e,t)}$(e){this.H!==e&&(this.R(),this.H=this.k(e))}m(e){const t=this.A.nextSibling;null!==t&&3===t.nodeType&&(null===this.B?null===t.nextSibling:t===this.B.previousSibling)?t.data=e:this.$(z.createTextNode(e)),this.H=e}_(e){var t;const{values:a,_$litType$:i}=e,n="number"==typeof i?this.C(e):(void 0===i.el&&(i.el=q.createElement(i.h,this.options)),i);if((null===(t=this.H)||void 0===t?void 0:t.D)===n)this.H.v(a);else{const e=new B(n,this),t=e.u(this.options);e.v(a),this.$(t),this.H=e}}C(e){let t=U.get(e.strings);return void 0===t&&U.set(e.strings,t=new q(e)),t}g(e){S(this.H)||(this.H=[],this.R());const t=this.H;let a,i=0;for(const n of e)i===t.length?t.push(a=new X(this.k(P()),this.k(P()),this,this.options)):a=t[i],a.I(n),i++;i<t.length&&(this.R(a&&a.B.nextSibling,i),t.length=i)}R(e=this.A.nextSibling,t){var a;for(null===(a=this.P)||void 0===a||a.call(this,!1,!0,t);e&&e!==this.B;){const t=e.nextSibling;e.remove(),e=t}}}class Y{constructor(e,t,a,i,n){this.type=1,this.H=F,this.N=void 0,this.V=void 0,this.element=e,this.name=t,this.M=i,this.options=n,a.length>2||""!==a[0]||""!==a[1]?(this.H=Array(a.length-1).fill(F),this.strings=a):this.H=F}get tagName(){return this.element.tagName}I(e,t=this,a,i){const n=this.strings;let r=!1;if(void 0===n)e=H(this,e,t,0),r=!M(e)||e!==this.H&&e!==D,r&&(this.H=e);else{const i=e;let o,s;for(e=n[0],o=0;o<n.length-1;o++)s=H(this,i[a+o],t,o),s===D&&(s=this.H[o]),r||(r=!M(s)||s!==this.H[o]),s===F?e=F:e!==F&&(e+=(null!=s?s:"")+n[o+1]),this.H[o]=s}r&&!i&&this.W(e)}W(e){e===F?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class W extends Y{constructor(){super(...arguments),this.type=3}W(e){this.element[this.name]=e===F?void 0:e}}class G extends Y{constructor(){super(...arguments),this.type=4}W(e){e&&e!==F?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class Z extends Y{constructor(){super(...arguments),this.type=5}I(e,t=this){var a;if((e=null!==(a=H(this,e,t,0))&&void 0!==a?a:F)===D)return;const i=this.H,n=e===F&&i!==F||e.capture!==i.capture||e.once!==i.once||e.passive!==i.passive,r=e!==F&&(i===F||n);n&&this.element.removeEventListener(this.name,this,i),r&&this.element.addEventListener(this.name,this,e),this.H=e}handleEvent(e){var t,a;"function"==typeof this.H?this.H.call(null!==(a=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==a?a:this.element,e):this.H.handleEvent(e)}}class K{constructor(e,t,a){this.element=e,this.type=6,this.N=void 0,this.V=void 0,this.M=t,this.options=a}I(e){H(this,e)}}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var J,Q,ee,te,ae,ie;null===(g=(_=globalThis).litHtmlPlatformSupport)||void 0===g||g.call(_,q,X),(null!==(f=(b=globalThis).litHtmlVersions)&&void 0!==f?f:b.litHtmlVersions=[]).push("2.0.0-rc.3"),(null!==(J=(ie=globalThis).litElementVersions)&&void 0!==J?J:ie.litElementVersions=[]).push("3.0.0-rc.2");class ne extends v{constructor(){super(...arguments),this.renderOptions={host:this},this.Φt=void 0}createRenderRoot(){var e,t;const a=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=a.firstChild),a}update(e){const t=this.render();super.update(e),this.Φt=((e,t,a)=>{var i,n;const r=null!==(i=null==a?void 0:a.renderBefore)&&void 0!==i?i:t;let o=r._$litPart$;if(void 0===o){const e=null!==(n=null==a?void 0:a.renderBefore)&&void 0!==n?n:null;r._$litPart$=o=new X(t.insertBefore(P(),e),e,void 0,a)}return o.I(e),o})(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this.Φt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.Φt)||void 0===e||e.setConnected(!1)}render(){return D}}ne.finalized=!0,ne._$litElement$=!0,null===(ee=(Q=globalThis).litElementHydrateSupport)||void 0===ee||ee.call(Q,{LitElement:ne}),null===(ae=(te=globalThis).litElementPlatformSupport)||void 0===ae||ae.call(te,{LitElement:ne});
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const re=e=>t=>"function"==typeof t?((e,t)=>(window.customElements.define(e,t),t))(e,t):((e,t)=>{const{kind:a,elements:i}=t;return{kind:a,elements:i,finisher(t){window.customElements.define(e,t)}}})(e,t)
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */,oe=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?{...t,finisher(a){a.createProperty(t.key,e)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:t.key,initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(a){a.createProperty(t.key,e)}};function se(e){return(t,a)=>void 0!==a?((e,t,a)=>{t.constructor.createProperty(a,e)})(e,t,a):oe(e,t)
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */}function le(e){return se({...e,state:!0,attribute:!1})}var ce="[^\\s]+";function de(e,t){for(var a=[],i=0,n=e.length;i<n;i++)a.push(e[i].substr(0,t));return a}var pe=function(e){return function(t,a){var i=a[e].map((function(e){return e.toLowerCase()})),n=i.indexOf(t.toLowerCase());return n>-1?n:null}};function ue(e){for(var t=[],a=1;a<arguments.length;a++)t[a-1]=arguments[a];for(var i=0,n=t;i<n.length;i++){var r=n[i];for(var o in r)e[o]=r[o]}return e}var me=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],he=["January","February","March","April","May","June","July","August","September","October","November","December"],ve=de(he,3),_e={dayNamesShort:de(me,3),dayNames:me,monthNamesShort:ve,monthNames:he,amPm:["am","pm"],DoFn:function(e){return e+["th","st","nd","rd"][e%10>3?0:(e-e%10!=10?1:0)*e%10]}},ge=(ue({},_e),function(e){return+e-1}),fe=[null,"[1-9]\\d?"],be=[null,ce],ye=["isPm",ce,function(e,t){var a=e.toLowerCase();return a===t.amPm[0]?0:a===t.amPm[1]?1:null}],xe=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(e){var t=(e+"").match(/([+-]|\d\d)/gi);if(t){var a=60*+t[1]+parseInt(t[2],10);return"+"===t[0]?a:-a}return 0}];pe("monthNamesShort"),pe("monthNames");var we;!function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}}(),function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}}(),function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}}(),function(e){e.language="language",e.system="system",e.comma_decimal="comma_decimal",e.decimal_comma="decimal_comma",e.space_comma="space_comma",e.none="none"}(we||(we={}));var Ee=["closed","locked","off"],ke=function(e,t,a,i){i=i||{},a=null==a?{}:a;var n=new Event(t,{bubbles:void 0===i.bubbles||i.bubbles,cancelable:Boolean(i.cancelable),composed:void 0===i.composed||i.composed});return n.detail=a,e.dispatchEvent(n),n},ze=function(e){ke(window,"haptic",e)},Pe=function(e,t,a,i){if(i||(i={action:"more-info"}),!i.confirmation||i.confirmation.exemptions&&i.confirmation.exemptions.some((function(e){return e.user===t.user.id}))||(ze("warning"),confirm(i.confirmation.text||"Are you sure you want to "+i.action+"?")))switch(i.action){case"more-info":(a.entity||a.camera_image)&&ke(e,"hass-more-info",{entityId:a.entity?a.entity:a.camera_image});break;case"navigate":i.navigation_path&&function(e,t,a){void 0===a&&(a=!1),a?history.replaceState(null,"",t):history.pushState(null,"",t),ke(window,"location-changed",{replace:a})}(0,i.navigation_path);break;case"url":i.url_path&&window.open(i.url_path);break;case"toggle":a.entity&&(function(e,t){(function(e,t,a){void 0===a&&(a=!0);var i,n=function(e){return e.substr(0,e.indexOf("."))}(t),r="group"===n?"homeassistant":n;switch(n){case"lock":i=a?"unlock":"lock";break;case"cover":i=a?"open_cover":"close_cover";break;default:i=a?"turn_on":"turn_off"}e.callService(r,i,{entity_id:t})})(e,t,Ee.includes(e.states[t].state))}(t,a.entity),ze("success"));break;case"call-service":if(!i.service)return void ze("failure");var n=i.service.split(".",2);t.callService(n[0],n[1],i.service_data),ze("success");break;case"fire-dom-event":ke(e,"ll-custom",i)}};function Me(e){return void 0!==e&&"none"!==e.action}var Se={version:"Version",invalid_configuration:"Invalid configuration {0}",description:"A card that lets you control your vacuum",old_configuration:"Old configuration detected. Adjust your config to the latest schema or create a new card from the scratch.",old_configuration_migration_link:"Migration guide"},Ce={invalid:"Invalid template!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Points",vacuum_clean_segment:"Rooms",vacuum_clean_zone:"Zone cleanup",vacuum_clean_zone_predefined:"Zones list",vacuum_follow_path:"Path"},Te={preset:{entity:{missing:"Missing property: entity"},preset_name:{missing:"Missing property: preset_name"},platform:{invalid:"Invalid vacuum platform: {0}"},map_source:{missing:"Missing property: map_source",none_provided:"No camera neither image provided",ambiguous:"Only one map source allowed"},calibration_source:{missing:"Missing property: calibration_source",ambiguous:"Only one calibration source allowed",none_provided:"No calibration source provided",calibration_points:{invalid_number:"Exactly 3 or 4 calibration points required",missing_map:"Each calibration point must contain map coordinates",missing_vacuum:"Each calibration point must contain vacuum coordinates",missing_coordinate:"Map and vacuum calibration points must contain both x and y coordinate"}},icons:{invalid:"Error in configuration: icons",icon:{missing:"Each entry of icons list must contain icon property"}},tiles:{invalid:"Error in configuration: tiles",entity:{missing:"Each entry of tiles list must contain entity"},label:{missing:"Each entry of tiles list must contain label"}},map_modes:{invalid:"Error in configuration: map_modes",icon:{missing:"Missing icon of map mode"},name:{missing:"Missing name of map mode"},template:{invalid:"Invalid template: {0}"},predefined_selections:{not_applicable:"Mode {0} does not support predefined selections",zones:{missing:"Missing zones configuration",invalid_parameters_number:"Each zone must have 4 parameters"},points:{position:{missing:"Missing points configuration",invalid_parameters_number:"Each point must have 2 parameters"}},rooms:{id:{missing:"Missing room id",invalid_format:"Invalid room id: {0}"},outline:{invalid_parameters_number:"Each point of room outline must have 2 parameters"}},label:{x:{missing:"Label must have x property"},y:{missing:"Label must have y property"},text:{missing:"Label must have text property"}},icon:{x:{missing:"Icon must have x property"},y:{missing:"Icon must have y property"},name:{missing:"Icon must have name property"}}},service_call_schema:{missing:"Missing service call schema",service:{missing:"Service call schema must contain service",invalid:"Invalid service: {0}"}}}},invalid_entities:"Invalid entities:",invalid_calibration:"Invalid calibration, please check your configuration"},$e={status:"Status",battery_level:"Battery",fan_speed:"Fan speed",sensor_dirty_left:"Sensors left",filter_left:"Filter left",main_brush_left:"Main brush left",side_brush_left:"Side brush left",cleaning_count:"Cleaning count",cleaned_area:"Cleaned area",cleaning_time:"Cleaning time"},Ne={vacuum_start:"Start",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Return to base",vacuum_clean_spot:"Clean spot",vacuum_locate:"Locate",vacuum_set_fan_speed:"Change fan speed"},Ae={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Re={success:"Success!",no_selection:"No selection provided",failed:"Failed to call service"},Le={description:{before_link:"This visual editor supports only a basic configuration with a camera entity created using ",link_text:"Xiaomi Cloud Map Extractor",after_link:". For more advanced setup use YAML mode."},label:{name:"Title (optional)",entity:"Vacuum entity (required)",camera:"Camera entity (required)",vacuum_platform:"Vacuum platform (required)",map_locked:"Map locked (optional)",two_finger_pan:"Two finger pan (optional)"}},Oe={common:Se,map_mode:Ce,validation:Te,label:$e,icon:Ne,unit:Ae,popups:Re,editor:Le},Ie={version:"Version",invalid_configuration:"Configuración inválida {0}",description:"Una tarjeta para controlar tu aspiradora",old_configuration:"Configuración antigua detectada. Ajusta la configuración al formato actual o crea una nueva tarjeta.",old_configuration_migration_link:"Guía de migrado."},je={invalid:"Plantilla inválida!",vacuum_goto:"Marcar e ir",vacuum_goto_predefined:"Puntos",vacuum_clean_segment:"Habitaciones",vacuum_clean_zone:"Limpiar zona",vacuum_clean_zone_predefined:"Lista de zonas",vacuum_follow_path:"Ruta"},De={preset:{entity:{missing:"Propiedad no encontrada: entity"},preset_name:{missing:"Propiedad no encontrada: preset_name"},platform:{invalid:"Plataforma de aspiradora inválida: {0}"},map_source:{missing:"Propiedad no encontrada: map_source",none_provided:"Sin cámara ni imagen proporcionada",ambiguous:"Solo se permite una fuente de mapa"},calibration_source:{missing:"Propiedad no encontrada: calibration_source",ambiguous:"Solo se permite una fuente de calibración",none_provided:"No se proporciona fuente de calibración",calibration_points:{invalid_number:"Se requieren 3 o 4 puntos de calibración",missing_map:"Cada punto de calibración debe contener las coordenadas del mapa",missing_vacuum:"Cada punto de calibración debe contener las coordenadas de la aspiradora",missing_coordinate:"Los puntos de calibración de la aspiradora y del mapa deben contener las coordenadas x e y"}},icons:{invalid:"Error en la configuración: icons",icon:{missing:"Cada entrada de la lista de iconos debe contener la propiedad del icono."}},tiles:{invalid:"Error en la configuración: tiles",entity:{missing:"Cada entrada de la lista de mosaicos debe contener la entidad."},label:{missing:"Cada entrada de la lista de mosaicos debe contener una etiqueta."}},map_modes:{invalid:"Error en la configuración: map_modes",icon:{missing:"Falta el icono del modo de mapa"},name:{missing:"Falta el nombre del modo de mapa"},template:{invalid:"Plantilla inválida: {0}"},predefined_selections:{not_applicable:"El modo {0} no admite selecciones predefinidas",zones:{missing:"Faltan configuraciones de zonas",invalid_parameters_number:"Cada zona debe tener 4 parámetros"},points:{position:{missing:"Faltan configuraciones de puntos",invalid_parameters_number:"Cada punto debe tener 2 parámetros"}},rooms:{id:{missing:"Falta la identificación de la habitación",invalid_format:"Identificación de la habitación inválida: {0}"},outline:{invalid_parameters_number:"Cada punto del contorno de la habitación debe tener 2 parámetros"}},label:{x:{missing:"La etiqueta debe tener la propiedad x"},y:{missing:"La etiqueta debe tener la propiedad y"},text:{missing:"La etiqueta debe tener la propiedad text"}},icon:{x:{missing:"El ícono debe tener la propiedad x"},y:{missing:"El ícono debe tener la propiedad y"},name:{missing:"El ícono debe tener la propiedad name"}}},service_call_schema:{missing:"Falta un esquema de llamada de servicio",service:{missing:"El esquema de llamada de servicio debe contener service",invalid:"Servicio inválido: {0}"}}}},invalid_entities:"Entidades inválidas:",invalid_calibration:"Calibración inválida, verifique la configuración."},Fe={status:"Estado",battery_level:"Batería",fan_speed:"Velocidad del ventilador",sensor_dirty_left:"Sensor izquierdo",filter_left:"Filtro derecho",main_brush_left:"Cepillo principal izquierdo",side_brush_left:"Cepillo lateral izquierdo",cleaning_count:"Contador de limpieza",cleaned_area:"Área limpia",cleaning_time:"Tiempo de limpieza"},Ue={vacuum_start:"Comenzar",vacuum_pause:"Pausar",vacuum_stop:"Detener",vacuum_return_to_base:"Volver a la base",vacuum_clean_spot:"Punto limpio",vacuum_locate:"Localizar",vacuum_set_fan_speed:"Cambiar la velocidad del ventilador"},Ve={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},qe={success:"Listo!",no_selection:"No se ha proporcionado ninguna selección",failed:"No se pudo llamar al servicio"},He={description:{before_link:"Este editor visual solo admite una configuración básica con una entidad de cámara creada utilizando ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Para una configuración más avanzada, utilice el modo YAML."},label:{name:"Título (opcional)",entity:"Entidad de la aspiradora (requerido)",camera:"Entidad de la cámara (requerido)",vacuum_platform:"Plataforma de la aspiradora (requerido)",map_locked:"Bloquear mapa (opcional)",two_finger_pan:"Mover con dos dedos (opcional)"}},Be={common:Ie,map_mode:je,validation:De,label:Fe,icon:Ue,unit:Ve,popups:qe,editor:He},Xe={version:"Version",invalid_configuration:"Configuration invalide {0}",description:"Une carte qui vous permet de contrôler votre robot aspirateur",old_configuration:"Ancienne configuration détectée. Ajustez votre configuration à la nouvelle version ou récréez totalement une nouvelle carte.",old_configuration_migration_link:"Guide de migration"},Ye={invalid:"Template incorrect !",vacuum_goto:"Cible",vacuum_goto_predefined:"Points",vacuum_clean_segment:"Pièces",vacuum_clean_zone:"Nettoyage de zone",vacuum_clean_zone_predefined:"Liste des zones",vacuum_follow_path:"Chemin"},We={preset:{entity:{missing:"Paramètre manquant : entity"},preset_name:{missing:"Paramètre manquant : preset_name"},platform:{invalid:"Plateforme incorrecte : {0}"},map_source:{missing:"Paramètre manquant : map_source",none_provided:"Aucune caméra ou image fournie",ambiguous:"Une seule source de carte autorisée"},calibration_source:{missing:"Paramètre manquant : calibration_source",ambiguous:"Une seule source de calibration autorisée",none_provided:"Aucune source de calibration fournie",calibration_points:{invalid_number:"3 ou 4 points de calibration sont nécessaires",missing_map:"Chaque point de calibration doit avoir des coordonnées de carte",missing_vacuum:"Chaque point de calibration doit avoir des coordonnées de robot",missing_coordinate:"Tous les points de calibration doivent avoir des coordonnées x et y"}},icons:{invalid:"Erreur de configuration : icônes",icon:{missing:"Chaque élément de la liste d'icônes doit avoir une propriété « icon »"}},tiles:{invalid:"Erreur de configuration : tuiles",entity:{missing:"Chaque élément de la liste de tuiles doit avoir une propriété « entity »"},label:{missing:"Chaque élément de la liste de tuiles doit avoir une propriété « label »"}},map_modes:{invalid:"Erreur de configuration : modes de carte",icon:{missing:"Icône de mode de carte manquante"},name:{missing:"Nom de mode de carte manquant"},template:{invalid:"Template incorrect : {0}"},predefined_selections:{not_applicable:"Ce mode {0} ne supporte pas les sélections prédéfinies",zones:{missing:"Configuration des zones manquante",invalid_parameters_number:"Chaque zone doit avoir 4 paramètres"},points:{position:{missing:"Configuration des points manquante",invalid_parameters_number:"Chaque point doit avoir 2 paramètres"}},rooms:{id:{missing:"id de pièce manquant",invalid_format:"id de pièce incorrect : {0}"},outline:{invalid_parameters_number:"Chaque point de contour de pièce doit avoir 2 paramètres"}},label:{x:{missing:"L'étiquette doit avoir une propriété « x »"},y:{missing:"L'étiquette doit avoir une propriété « y »"},text:{missing:"L'étiquette doit avoir une propriété « text »"}},icon:{x:{missing:"L'icône doit avoir une propriété x property"},y:{missing:"L'icône doit avoir une propriété y property"},name:{missing:"L'icône doit avoir une propriété « name »"}}},service_call_schema:{missing:"Missing service call schema",service:{missing:"Service call schema must contain service",invalid:"Invalid service: {0}"}}}},invalid_entities:"Entités incorrectes :",invalid_calibration:"Calibration incorrecte, vérifiez votre configuration"},Ge={status:"Statut",battery_level:"Batterie",fan_speed:"Puissance",sensor_dirty_left:"Capteurs",filter_left:"Filtre",main_brush_left:"Brosse princ.",side_brush_left:"Brosse lat.",cleaning_count:"Nbr de nettoyages",cleaned_area:"Surface nettoyée",cleaning_time:"Temps de nettoyage"},Ze={vacuum_start:"Démarrage",vacuum_pause:"Pause",vacuum_stop:"Stop",vacuum_return_to_base:"Retour à la base",vacuum_clean_spot:"Nettoyage ciblé",vacuum_locate:"Localiser",vacuum_set_fan_speed:"Changer la puissance d'aspiration"},Ke={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},Je={success:"Réussi !",no_selection:"Aucune sélection fournie",failed:"L'appel du service a échoué"},Qe={description:{before_link:"L'éditeur visuel permet seulement une configuration de base avec une entité caméra créée avec ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Pour une configuration plus avancée, utilisez le mode YAML."},label:{name:"Titre (optionnel)",entity:"Entité du robot (obligatoire)",camera:"Entité de la caméra (obligatoire)",vacuum_platform:"Platforme (obligatoire)",map_locked:"Verrouiller la carte (optionnel)",two_finger_pan:"Défilement à deux doigts (optionnel)"}},et={common:Xe,map_mode:Ye,validation:We,label:Ge,icon:Ze,unit:Ke,popups:Je,editor:Qe},tt={version:"Versione",invalid_configuration:"Configurazione non valida {0}",description:"Una card per controllare il tuo robot aspirapolvere",old_configuration:"Trovata una vecchia configurazione. Correggi la configurazione all'ultima possibile o crea una nuova card.",old_configuration_migration_link:"Guida Migrazione"},at={invalid:"Template non valido!",vacuum_goto:"Pin & Go",vacuum_goto_predefined:"Punti",vacuum_clean_segment:"Stanze",vacuum_clean_zone:"Pulizia a Zone",vacuum_clean_zone_predefined:"Lista Zone",vacuum_follow_path:"Percorso"},it={preset:{entity:{missing:"Proprietà Mancante: entity"},preset_name:{missing:"Proprietà Mancante: preset_name"},platform:{invalid:"Piattaforma aspirapolvere non valida: {0}"},map_source:{missing:"Proprietà Mancante: map_source",none_provided:"Inserire camera o immagine",ambiguous:"È consentita una sola sorgente della mappa"},calibration_source:{missing:"Proprietà Mancante: calibration_source",ambiguous:"È consentita una solo una sorgente di calibrazione",none_provided:"Nessuna fonte di calibrazione fornita",calibration_points:{invalid_number:"Esattamente 3 o 4 punti di calibrazione richiesti",missing_map:"Ogni punto di calibrazione deve contenere le coordinate della mappa",missing_vacuum:"Ciascun punto di calibrazione deve contenere le coordinate dell'aspirapolvere",missing_coordinate:"I punti di calibrazione della mappa e dell'aspirapolvere devono contenere sia le coordinate x che y"}},icons:{invalid:"Errore nella configurazione: icons",icon:{missing:"Ogni voce dell'elenco delle icone deve contenere la proprietà dell'icona"}},tiles:{invalid:"Errore nella configurazione: tiles",entity:{missing:"Ogni voce dell'elenco 'tile' deve contenere una entity"},label:{missing:"Ogni voce dell'elenco 'tile' deve contenere una label"}},map_modes:{invalid:"Errore nella configurazione: map_modes",icon:{missing:"Icona della modalità mappa mancante"},name:{missing:"Nome della modalità mappa mancante"},template:{invalid:"Template non valido: {0}"},predefined_selections:{not_applicable:"Modalità {0} non supporta le selezioni predefinite",zones:{missing:"Configurazione zone mancante",invalid_parameters_number:"Ogni zona deve avere 4 parametri"},points:{position:{missing:"Configurazione punti mancante",invalid_parameters_number:"Ogni punto deve avere 2 parametri"}},rooms:{id:{missing:"ID stanza mancante",invalid_format:"ID stanza non valido: {0}"},outline:{invalid_parameters_number:"Ogni punto del contorno della stanza deve avere 2 parametri"}},label:{x:{missing:"Label deve avere la proprietà x"},y:{missing:"Label deve avere la proprietà y"},text:{missing:"Label deve avere la proprietà text"}},icon:{x:{missing:"Icon deve avere la proprietà x"},y:{missing:"Icon deve avere la proprietà y"},name:{missing:"Icon deve avere la proprietà name"}}},service_call_schema:{missing:"Schema della chiamata al servizio mancante",service:{missing:"La chiamata al servizio deve contenere un servizio",invalid:"Servizio non valido: {0}"}}}},invalid_entities:"Entità non valide:",invalid_calibration:"Calibrazione non valida, per favore controlla la configurazione"},nt={status:"Stato",battery_level:"Batteria",fan_speed:"Velocità Ventola",sensor_dirty_left:"Sensori",filter_left:"Filtro",main_brush_left:"Spazzola Principale",side_brush_left:"Spazzola laterale",cleaning_count:"Conteggio pulizia",cleaned_area:"Area pulita",cleaning_time:"Tempo di pulizia"},rt={vacuum_start:"Avvia",vacuum_pause:"Pausa",vacuum_stop:"Stop",vacuum_return_to_base:"Ritorna alla base",vacuum_clean_spot:"Pulizia spot",vacuum_locate:"Localizza",vacuum_set_fan_speed:"Cambia velocità ventola"},ot={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},st={success:"Confermato!",no_selection:"Nessuna Selezione",failed:"Chiamata al servizio fallita"},lt={description:{before_link:"Questo editor visivo supporta solo una configurazione di base con un'entità telecamera creata utilizzando ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Per una configurazione più avanzata usa la modalità YAML."},label:{name:"Titolo (opzionale)",entity:"Entità Aspirapolvere (obbligatorio)",camera:"Entità camera (obbligatorio)",vacuum_platform:"Piattaforma aspirapolvere (obbligatorio)",map_locked:"Blocco mappa (opzionale)",two_finger_pan:"Zoom a due dita (opzionale)"}},ct={common:tt,map_mode:at,validation:it,label:nt,icon:rt,unit:ot,popups:st,editor:lt},dt={version:"Wersja",invalid_configuration:"Nieprawidłowa konfiguracja {0}",description:"Karta pozwalająca na kontrolowanie odkurzacza",old_configuration:"Wykryto starą wersję konfiguracji. Dostosuj kartę do najnowszej wersji, albo utwórz ją od nowa.",old_configuration_migration_link:"Przewodnik po migracji"},pt={invalid:"Nieprawidłowa wartość template",vacuum_goto:"Idź do punktu",vacuum_goto_predefined:"Zapisane punkty",vacuum_clean_segment:"Pokoje",vacuum_clean_zone:"Sprzątanie strefowe",vacuum_clean_zone_predefined:"Zapisane strefy",vacuum_follow_path:"Ścieżka"},ut={preset:{entity:{missing:"Brakujący parametr: entity"},preset_name:{missing:"Brakujący parametr: preset_name"},platform:{invalid:"Nieprawidłowa platforma odkurzacza: {0}"},map_source:{missing:"Brakujący parametr: map_source",none_provided:"Nie podano źródła mapy",ambiguous:"Można podać tylko jedno źródło mapy"},calibration_source:{missing:"Brakujący parametr: calibration_source",ambiguous:"Można podać tylko jedno źródło kalibracji",none_provided:"Nie podano źródła kalibracji",calibration_points:{invalid_number:"Wymagane 3 bądź 4 punkty kalibracyjne",missing_map:"Każdy punkt kalibracyjny musi posiadać współrzędne na mapie",missing_vacuum:"Każdy punkt kalibracyjny musi posiadać współrzędne w układzie odkurzacza",missing_coordinate:"Każdy punkt kalibracyjny musi mieć współrzędne x i y"}},icons:{invalid:"Błąd w konfiguracji: icons",icon:{missing:'Każda pozycja na liście ikon musi posiadać parametr "icon"'}},tiles:{invalid:"Błąd w konfiguracji: tiles",entity:{missing:'Każda pozycja na liście kafelków musi posiadać parametr "entity"'},label:{missing:'Każda pozycja na liście kafelków musi posiadać parametr "label"'}},map_modes:{invalid:"Błąd w konfiguracji: map_modes",icon:{missing:"Brakująca ikona szablonu trybu mapy"},name:{missing:"Brakująca nazwa szablonu trybu mapy"},template:{invalid:"Nieprawidłowy szablon trybu mapy: {0}"},predefined_selections:{not_applicable:"Szablon {0} nie wspiera zapisywania zaznaczeń",zones:{missing:"Brakująca lista zapisanych stref",invalid_parameters_number:"Każda zapisana strefa musi posiadać 4 współrzędne"},points:{position:{missing:"Brakująca lista zapisanych punktów",invalid_parameters_number:"Każdy zapisany punkt musi posiadać 2 współrzędne"}},rooms:{id:{missing:"Brakujący identyfikator pokoju",invalid_format:"Nieprawidłowy identyfikator pokoju: {0}"},outline:{invalid_parameters_number:"Każdy punkt obrysu pokoju musi posiadać 2 współrzędne"}},label:{x:{missing:"Każda etykieta musi posiadać współrzędną x"},y:{missing:"Każda etykieta musi posiadać współrzędną y"},text:{missing:"Każda etykieta musi posiadać tekst"}},icon:{x:{missing:"Każda ikona musi posiadać współrzędną x"},y:{missing:"Każda ikona musi posiadać współrzędną y"},name:{missing:'Każda ikona musi posiadać parametr "name"'}}},service_call_schema:{missing:"Brakujący schemat wywołania usługi",service:{missing:"Każdy schemat usługi musi posiadać podaną nazwę usługi  ",invalid:"Nieprawidłowa usługa: {0}"}}}},invalid_entities:"Nieprawidłowe encje:",invalid_calibration:"Nieprawidłowa kalibracja, sprawdź konfigurację"},mt={status:"Status",battery_level:"Bateria",fan_speed:"Moc",sensor_dirty_left:"Sensory",filter_left:"Filtr",main_brush_left:"Główna szczotka",side_brush_left:"Boczna szczotka",cleaning_count:"Licznik sprzątań",cleaned_area:"Powierzchnia",cleaning_time:"Czas sprzątania"},ht={vacuum_start:"Uruchom",vacuum_pause:"Wstrzymaj",vacuum_stop:"Zatrzymaj",vacuum_return_to_base:"Wróć do stacji dokującej",vacuum_clean_spot:"Wyczyść miejsce",vacuum_locate:"Zlokalizuj",vacuum_set_fan_speed:"Zmień prędkość wentylatora"},vt={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},_t={success:"Usługa wywołana!",no_selection:"Nie wybrano zaznaczenia",failed:"Błąd wywołania usługi"},gt={description:{before_link:"Ten edytor interfejsu wspiera jedynie podstawową konfigurację dla kamery utworzonej przy użyciu ",link_text:"Xiaomi Cloud Map Extractora",after_link:". W celu bardziej zaawansowanej konfiguracji użyj trybu YAML."},label:{name:"Tytuł (opcjonalny)",entity:"Encja odkurzacza (wymagana)",camera:"Kamera z mapą (wymagana)",vacuum_platform:"Platforma integracji odkurzacza (wymagana)",map_locked:"Blokada mapy (opcjonalna)",two_finger_pan:"Przesuwanie mapy dwoma palcami (opcjonalne)"}},ft={common:dt,map_mode:pt,validation:ut,label:mt,icon:ht,unit:vt,popups:_t,editor:gt},bt={version:"Versão",invalid_configuration:"configuração inválida {0}",description:"Um cartão que permite que você controlar seu aspirador",old_configuration:"Configuração antiga detectada. Ajuste sua configuração para a versão mais recente ou crie um novo cartão do zero.",old_configuration_migration_link:"Guia de migração"},yt={invalid:"template inválido!",vacuum_goto:"Click & vai",vacuum_goto_predefined:"Local",vacuum_clean_segment:"Quartos",vacuum_clean_zone:"Limpar zona",vacuum_clean_zone_predefined:"Lista de zonas",vacuum_follow_path:"Seguir caminho"},xt={preset:{entity:{missing:"Propriedade ausente: entidade"},preset_name:{missing:"Propriedade ausente: preset_name"},platform:{invalid:"Plataforma de aspirador inválida: {0}"},map_source:{missing:"Propriedade ausente: map_source",none_provided:"Nenhuma câmera nem imagem fornecida",ambiguous:"Apenas uma fonte de mapa permitida"},calibration_source:{missing:"Propriedade ausente: calibration_source",ambiguous:"Apenas uma fonte de calibração permitida",none_provided:"Nenhuma fonte de calibração fornecida",calibration_points:{invalid_number:"Exatamente 3 ou 4 pontos de calibração são necessários",missing_map:"Cada ponto de calibração deve conter coordenadas do mapa",missing_vacuum:"Cada ponto de calibração deve conter coordenadas do aspirador",missing_coordinate:"Os pontos de calibração do mapa e do aspirador devem conter as coordenadas x e y"}},icons:{invalid:"Erro na configuração: icones",icon:{missing:"Cada entrada na lista de ícones deve conter a propriedade do ícone"}},tiles:{invalid:"Erro na configuração: tiles",entity:{missing:"Cada entrada da lista de tiles deve conter entidade"},label:{missing:"Cada entrada da lista de tiles deve conter label"}},map_modes:{invalid:"Erro na configuração: map_modes",icon:{missing:"Falta o ícone no modo de mapa"},name:{missing:"Falta o nome no modo de mapa"},template:{invalid:"Template inválido: {0}"},predefined_selections:{not_applicable:"O modo {0} não oferece suporte a seleções predefinidas",zones:{missing:"Falta a Configuração de zonas",invalid_parameters_number:"Cada zona deve ter 4 parâmetros"},points:{position:{missing:"Falta a configuração do local",invalid_parameters_number:"Cada local deve ter 2 parâmetros"}},rooms:{id:{missing:"Falta o id do quarto",invalid_format:"Id inválido do quarto: {0}"},outline:{invalid_parameters_number:"Cada local da borda do quarto deve ter 2 parâmetros"}},label:{x:{missing:"A label deve ter a propriedade x"},y:{missing:"A label deve ter a propriedade y"},text:{missing:"A label deve ter um texto"}},icon:{x:{missing:"O ícone deve ter a propriedade x"},y:{missing:"O ícone deve ter a propriedade y"},name:{missing:"O ícone deve ter um nome"}}},service_call_schema:{missing:"Falta o call service",service:{missing:"O call service deve conter o serviço",invalid:"serviço inválido: {0}"}}}},invalid_entities:"entidades inválidas:",invalid_calibration:"Calibração inválida, verifique sua configuração"},wt={status:"Status",battery_level:"Bateria",fan_speed:"Velocidade",sensor_dirty_left:"Sensores",filter_left:"Filtro",main_brush_left:"Escova principal",side_brush_left:"Escova lateral",cleaning_count:"Contagem de limpezas",cleaned_area:"Área limpa",cleaning_time:"Tempo de limpeza"},Et={vacuum_start:"Começar",vacuum_pause:"Pausar",vacuum_stop:"Parar",vacuum_return_to_base:"Voltar para a base",vacuum_clean_spot:"Limpar local",vacuum_locate:"Localizar",vacuum_set_fan_speed:"Mudar velocidade"},kt={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},zt={success:"Successo!",no_selection:"Nenhuma seleção fornecida",failed:"Falha em chamar o serviço"},Pt={description:{before_link:"Este editor suporta apenas uma configuração básica usando uma entidade de câmera",link_text:"Xiaomi Cloud Map Extractor",after_link:". Para um setup avancado use o YAML mode."},label:{name:"Título (opicional)",entity:"Entidade do aspirador (Obrigatório)",camera:"Entidade da camera (Obrigatório)",vacuum_platform:"Plataforma do aspirador (Obrigatório)",map_locked:"Mapa travado (Opicional)",two_finger_pan:"Movimente com dois dedos (Opicional)"}},Mt={common:bt,map_mode:yt,validation:xt,label:wt,icon:Et,unit:kt,popups:zt,editor:Pt},St={version:"Версия",invalid_configuration:"Неверная конфигурация {0}",description:"Карточка, позволяющая управлять вашим пылесосом",old_configuration:"Обнаружена устаревшая конфигурация. Приведите ваш конфиг в соответствие с новой версией, или создайте новую карточку с нуля.",old_configuration_migration_link:"Руководство по переходу с предыдущих версий."},Ct={invalid:"Неверный шаблон!",vacuum_goto:"Точка назначения",vacuum_goto_predefined:"Предустановленные точки",vacuum_clean_segment:"Комнаты",vacuum_clean_zone:"Уборка зоны",vacuum_clean_zone_predefined:"Список зон",vacuum_follow_path:"Путь"},Tt={preset:{entity:{missing:"Не указано свойство: entity"},preset_name:{missing:"Не указано свойство: preset_name"},platform:{invalid:"Неверная платформа: {0}"},map_source:{missing:"Не указано свойство: map_source",none_provided:"Не предоставлена ни камера ни изображение",ambiguous:"Допустим только один источник для карты"},calibration_source:{missing:"Не указано свойство: calibration_source",ambiguous:"Допустим только один источник для калибровки",none_provided:"Не предоставлен источник калибровки",calibration_points:{invalid_number:"Для калибровки требуется 3 или 4 точки",missing_map:"Каждая точка калибровки должна содержать координаты карты",missing_vacuum:"Каждая точка калибровки должна содержать координаты пылесоса",missing_coordinate:"Калибровочные точки карты и пылесоса должны содержать как x так и y координаты"}},icons:{invalid:"Ошибка в конфигурации: icons",icon:{missing:"Каждое вхождение в списке иконок должен содержать icon property"}},tiles:{invalid:"Ошибка в конфигурации: tiles",entity:{missing:"Каждое вхождение в списке плиток должно содержать entity"},label:{missing:"Каждое вхождение в списке плиток должно содержать label"}},map_modes:{invalid:"Ошибка в конфигурации: map_modes",icon:{missing:"Не указана иконка для влажной уборки"},name:{missing:"Не указано имя для влажной уборки"},template:{invalid:"Неверный шаблон: {0}"},predefined_selections:{not_applicable:"Режим {0} не поддерживает предустановленые элементы",zones:{missing:"Не указана конфигурация зоны",invalid_parameters_number:"Каждая зона должна содержать 4 параметра"},points:{position:{missing:"Не указана конфигурация для точек",invalid_parameters_number:"Каждая точка должна содержать 2 параметра"}},rooms:{id:{missing:"Не указан id комнаты",invalid_format:"Некорректный id комнаты: {0}"},outline:{invalid_parameters_number:"Каждая точка контура комнаты должна содержать 2 параметра"}},label:{x:{missing:"Ярлык должен содержать свойство x"},y:{missing:"Ярлык должен содержать свойство y"},text:{missing:"Ярлык должен содержать свойство text"}},icon:{x:{missing:"Иконка должна содержать свойство x"},y:{missing:"Иконка должна содержать свойство y"},name:{missing:"Иконка должна содержать свойство name"}}},service_call_schema:{missing:"Отсутствует схема вызова службы",service:{missing:"Схема вызова службы должна содержать service",invalid:"Некорректная служба: {0}"}}}},invalid_entities:"Некорректные сущности:",invalid_calibration:"Некорректная калибровка, проверьте вашу конфигурацию"},$t={status:"Статус",battery_level:"Уровень заряда",fan_speed:"Мощность всасывания",sensor_dirty_left:"Уровень загрязнения датчиков",filter_left:"Ресурс фильтра",main_brush_left:"Ресурс основной щётки",side_brush_left:"Ресурс боковой щётки",cleaning_count:"Число уборок",cleaned_area:"Площадь уборки",cleaning_time:"Время уборки"},Nt={vacuum_start:"Старт",vacuum_pause:"Пауза",vacuum_stop:"Стоп",vacuum_return_to_base:"Вернуть к базе",vacuum_clean_spot:"Убрать точку",vacuum_locate:"Обнаружить",vacuum_set_fan_speed:"Изменить мощность всасывания"},At={hour_shortcut:"ч",meter_shortcut:"м",meter_squared_shortcut:"м²",minute_shortcut:"мин"},Rt={success:"Успех!",no_selection:"Ничего не выбрано",failed:"Не удалось вызвать службу"},Lt={description:{before_link:"Данный редактор поддерживает только базовую конфигурацию с камерой, созданной посредством",link_text:"Xiaomi Cloud Map Extractor",after_link:". Для более тонкой настройки, используйте YAML-мод."},label:{name:"Заголовок (опционально)",entity:"Сущность пылесоса (обязательно)",camera:"Сущность камеры (обязательно)",vacuum_platform:"Платформа пылесоса (обязательно)",map_locked:"Блокировка карты (опционально)",two_finger_pan:"Перемещение жестом двумя пальцами (опционально)"}},Ot={common:St,map_mode:Ct,validation:Tt,label:$t,icon:Nt,unit:At,popups:Rt,editor:Lt},It={version:"Version",invalid_configuration:"Недійсна конфігурація {0}",description:"Картка, яка дає змогу контролювати пилосос",old_configuration:"Виявлено стару конфігурацію. Налаштуйте конфігурацію до останньої схеми або створіть нову картку з початку.",old_configuration_migration_link:"Посібник з міграції"},jt={invalid:"Недійсний шаблон!",vacuum_goto:"Рух до цілі",vacuum_goto_predefined:"Збережені точки",vacuum_clean_segment:"Кімнати",vacuum_clean_zone:"Зональне прибирання",vacuum_clean_zone_predefined:"Список зон",vacuum_follow_path:"Шлях"},Dt={preset:{entity:{missing:"Відсутній параметр: entity"},preset_name:{missing:"Відсутній параметр: preset_name"},platform:{invalid:"Недійсна платформа пилососа: {0}"},map_source:{missing:"Відсутній параметр: map_source",none_provided:"Не вказано джерело мапи",ambiguous:"Дозволено тільки одне джерело мапи"},calibration_source:{missing:"Відсутній параметр: calibration_source",ambiguous:"Дозволено тільки одне джерело калібрування",none_provided:"Не вказано джерело калібрування",calibration_points:{invalid_number:"Потрібні 3 або 4 точки калібрування",missing_map:"Кожна точка калібрування повинна мати координати на мапі",missing_vacuum:"Кожна точка калібрування повинна мати координати в системі пилососа",missing_coordinate:"Кожна точка калібрування повинна мати координати x і y"}},icons:{invalid:"Помилка в конфігурації: icons",icon:{missing:'Кожен елемент у списку піктограм повинен мати параметр "icon"'}},tiles:{invalid:"Помилка в конфігурації: tiles",entity:{missing:'Кожен елемент у списку плиток повинен мати параметр "entity"'},label:{missing:'Кожен елемент у списку плиток повинен мати параметр "label"'}},map_modes:{invalid:"Помилка в конфігурації: map_modes",icon:{missing:"Відсутня піктограма шаблону режиму мапи"},name:{missing:"Відсутня назва шаблону режиму мапи"},template:{invalid:"Недійсний шаблон: {0}"},predefined_selections:{not_applicable:"Шаблон {0} не підтримує збереження вибраних елементів",zones:{missing:"Відсутній список збережених зон",invalid_parameters_number:"Кожна збережена зона повинна мати 4 координати"},points:{position:{missing:"Відсутній список збережених точок",invalid_parameters_number:"Кожна записана точка повинна мати 2 координати"}},rooms:{id:{missing:"Відсутній ідентифікатор кімнати",invalid_format:"Недійсний ідентифікатор кімнати: {0}"},outline:{invalid_parameters_number:"Кожна точка контуру кімнати повинна мати 2 координати"}},label:{x:{missing:"Кожна мітка повинна мати координату x"},y:{missing:"Кожна мітка повинна мати координату y"},text:{missing:"Кожна мітка повинна містити текст"}},icon:{x:{missing:"Кожна піктограма повинна мати координату x"},y:{missing:"Кожна піктограма повинна мати координату y"},name:{missing:'Кожна піктограма повинна мати параметр "name"'}}},service_call_schema:{missing:"Відсутня схема виклику служби",service:{missing:"Кожна схема служби повинна мати назву служби",invalid:"Недійсна служба: {0}"}}}},invalid_entities:"Недійсні сутності:",invalid_calibration:"Неправильне калібрування, перевірте конфігурацію"},Ft={status:"Статус",battery_level:"Батарея",fan_speed:"Потужність",sensor_dirty_left:"Сенсор",filter_left:"Фільтр",main_brush_left:"Основна щітка",side_brush_left:"Бокова щітка",cleaning_count:"Лічильник прибирань",cleaned_area:"Прибрано",cleaning_time:"Час прибирання"},Ut={vacuum_start:"Старт",vacuum_pause:"Пауза",vacuum_stop:"Стоп",vacuum_return_to_base:"Повернення на базу",vacuum_clean_spot:"Прибрати місце",vacuum_locate:"Пошук",vacuum_set_fan_speed:"Зміна потужності"},Vt={hour_shortcut:"h",meter_shortcut:"m",meter_squared_shortcut:"m²",minute_shortcut:"min"},qt={success:"Успіх!",no_selection:"Виділення не зроблено",failed:"Не вдалося викликати службу"},Ht={description:{before_link:"Цей редактор інтерфейсу підтримує лише базову конфігурацію для камери, створеної за допомогою ",link_text:"Xiaomi Cloud Map Extractor",after_link:". Для більш розширеного налаштування використовуйте режим YAML."},label:{name:"Назва (опція)",entity:"Сутність пилососу (необхідно)",camera:"Сутність камери (необхідно)",vacuum_platform:"Платформа інтеграції пилососу (необхідно)",map_locked:"Блокування мапи (опція)",two_finger_pan:"Переміщеня мапи двома пальцями (опція)"}},Bt={common:It,map_mode:jt,validation:Dt,label:Ft,icon:Ut,unit:Vt,popups:qt,editor:Ht};const Xt={en:Object.freeze({__proto__:null,common:Se,map_mode:Ce,validation:Te,label:$e,icon:Ne,unit:Ae,popups:Re,editor:Le,default:Oe}),es:Object.freeze({__proto__:null,common:Ie,map_mode:je,validation:De,label:Fe,icon:Ue,unit:Ve,popups:qe,editor:He,default:Be}),fr:Object.freeze({__proto__:null,common:Xe,map_mode:Ye,validation:We,label:Ge,icon:Ze,unit:Ke,popups:Je,editor:Qe,default:et}),it:Object.freeze({__proto__:null,common:tt,map_mode:at,validation:it,label:nt,icon:rt,unit:ot,popups:st,editor:lt,default:ct}),pl:Object.freeze({__proto__:null,common:dt,map_mode:pt,validation:ut,label:mt,icon:ht,unit:vt,popups:_t,editor:gt,default:ft}),"pt-BR":Object.freeze({__proto__:null,common:bt,map_mode:yt,validation:xt,label:wt,icon:Et,unit:kt,popups:zt,editor:Pt,default:Mt}),ru:Object.freeze({__proto__:null,common:St,map_mode:Ct,validation:Tt,label:$t,icon:Nt,unit:At,popups:Rt,editor:Lt,default:Ot}),uk:Object.freeze({__proto__:null,common:It,map_mode:jt,validation:Dt,label:Ft,icon:Ut,unit:Vt,popups:qt,editor:Ht,default:Bt})};function Yt(e,t="",a="",i=""){const n="en";if(!i)try{i=JSON.parse(localStorage.getItem("selectedLanguage")||'"en"')}catch(e){i=(localStorage.getItem("selectedLanguage")||n).replace(/['"]+/g,"")}let r;try{r=Wt(e,null!=i?i:n)}catch(t){r=Wt(e,n)}return void 0===r&&(r=Wt(e,n)),r=null!=r?r:e,""!==t&&""!==a&&(r=r.replace(t,a)),r}function Wt(e,t){return e.split(".").reduce(((e,t)=>e[t]),Xt[t])}function Gt(e,t){return"string"==typeof e?Yt(e,"","",t):Yt(...e,t)}var Zt={defaultTemplates:["vacuum_clean_zone","vacuum_goto"],templates:{vacuum_clean_segment:{name:"map_mode.vacuum_clean_segment",icon:"mdi:floor-plan",selection_type:"ROOM",repeats_type:"NONE",service_call_schema:{service:"xiaomi_miio.vacuum_clean_segment",service_data:{segments:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!0,max_selections:5,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"xiaomi_miio.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!0,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"xiaomi_miio.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_goto:{name:"map_mode.vacuum_goto",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"xiaomi_miio.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_goto_predefined:{name:"map_mode.vacuum_goto_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"xiaomi_miio.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_follow_path:{name:"map_mode.vacuum_follow_path",icon:"mdi:map-marker-path",selection_type:"MANUAL_PATH",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"script.vacuum_follow_path",service_data:{path:"[[selection]]",entity_id:"[[entity_id]]"}}}}},Kt={from_attributes:[{attribute:"sensor_dirty_left",label:"label.sensor_dirty_left",icon:"mdi:eye-outline",unit:"unit.hour_shortcut"},{attribute:"filter_left",label:"label.filter_left",icon:"mdi:air-filter",unit:"unit.hour_shortcut"},{attribute:"main_brush_left",label:"label.main_brush_left",icon:"mdi:brush",unit:"unit.hour_shortcut"},{attribute:"side_brush_left",label:"label.side_brush_left",icon:"mdi:brush",unit:"unit.hour_shortcut"},{attribute:"cleaning_count",label:"label.cleaning_count",icon:"mdi:counter"}],from_sensors:[{unique_id_prefix:"consumable_sensor_dirty_left_",label:"label.sensor_dirty_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"consumable_filter_left_",label:"label.filter_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"consumable_main_brush_left_",label:"label.main_brush_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"consumable_side_brush_left_",label:"label.side_brush_left",unit:"unit.hour_shortcut",multiplier:.0002777777777777778},{unique_id_prefix:"clean_history_count_",label:"label.cleaning_count"}]},Jt={map_modes:Zt,sensors_from:"2021.11.0",tiles:Kt},Qt=Object.freeze({__proto__:null,map_modes:Zt,sensors_from:"2021.11.0",tiles:Kt,default:Jt}),ea={defaultTemplates:["vacuum_clean_zone","vacuum_goto"],templates:{vacuum_clean_segment:{name:"map_mode.vacuum_clean_segment",icon:"mdi:floor-plan",selection_type:"ROOM",repeats_type:"NONE",service_call_schema:{service:"vacuum.vacuum_clean_segment",service_data:{segments:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!1,max_selections:5,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!1,repeats_type:"EXTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.vacuum_clean_zone",service_data:{zone:"[[selection]]",repeats:"[[repeats]]",entity_id:"[[entity_id]]"}}},vacuum_goto:{name:"map_mode.vacuum_goto",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"vacuum.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_goto_predefined:{name:"map_mode.vacuum_goto_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"vacuum.vacuum_goto",service_data:{x_coord:"[[point_x]]",y_coord:"[[point_y]]",entity_id:"[[entity_id]]"}}},vacuum_follow_path:{name:"map_mode.vacuum_follow_path",icon:"mdi:map-marker-path",selection_type:"MANUAL_PATH",coordinates_rounding:!1,repeats_type:"NONE",service_call_schema:{service:"script.vacuum_follow_path",service_data:{path:"[[selection]]",entity_id:"[[entity_id]]"}}}}},ta={from_attributes:[{attribute:"cleaned_area",label:"label.cleaned_area",icon:"mdi:texture-box",unit:"unit.meter_squared_shortcut"},{attribute:"cleaning_time",label:"label.cleaning_time",icon:"mdi:timer-sand",unit:"unit.minute_shortcut"}]},aa={map_modes:ea,tiles:ta},ia=Object.freeze({__proto__:null,map_modes:ea,tiles:ta,default:aa}),na={defaultTemplates:["vacuum_clean_zone","vacuum_goto"],templates:{vacuum_clean_segment:{name:"map_mode.vacuum_clean_segment",icon:"mdi:floor-plan",selection_type:"ROOM",repeats_type:"NONE",service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_segment_clean",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone:{name:"map_mode.vacuum_clean_zone",icon:"mdi:select-drag",selection_type:"MANUAL_RECTANGLE",coordinates_rounding:!0,max_selections:5,repeats_type:"INTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_zoned_clean",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_clean_zone_predefined:{name:"map_mode.vacuum_clean_zone_predefined",icon:"mdi:floor-plan",selection_type:"PREDEFINED_RECTANGLE",max_selections:5,coordinates_rounding:!0,repeats_type:"INTERNAL",max_repeats:3,service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_zoned_clean",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_goto:{name:"map_mode.vacuum_goto",icon:"mdi:map-marker-plus",selection_type:"MANUAL_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_goto_target",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_goto_predefined:{name:"map_mode.vacuum_goto_predefined",icon:"mdi:map-marker",selection_type:"PREDEFINED_POINT",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"vacuum.send_command",service_data:{command:"app_goto_target",params:"[[selection]]",entity_id:"[[entity_id]]"}}},vacuum_follow_path:{name:"map_mode.vacuum_follow_path",icon:"mdi:map-marker-path",selection_type:"MANUAL_PATH",coordinates_rounding:!0,repeats_type:"NONE",service_call_schema:{service:"script.vacuum_follow_path",service_data:{path:"[[selection]]",entity_id:"[[entity_id]]"}}}}},ra={from_attributes:[],from_sensors:[]},oa={map_modes:na,tiles:ra},sa=Object.freeze({__proto__:null,map_modes:na,tiles:ra,default:oa});const la=(e,t,a)=>{_a(a);const i=function(e,t){const a=da(e),i=da(t),n=a.pop(),r=i.pop(),o=ma(a,i);return 0!==o?o:n&&r?ma(n.split("."),r.split(".")):n||r?n?-1:1:0}(e,t);return ha[a].includes(i)},ca=/^v?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,da=e=>{if("string"!=typeof e)throw new TypeError("Invalid argument expected string");const t=e.match(ca);if(!t)throw new Error(`Invalid argument not valid semver ('${e}' received)`);return t.shift(),t},pa=e=>{const t=parseInt(e,10);return isNaN(t)?e:t},ua=(e,t)=>{const[a,i]=((e,t)=>typeof e!=typeof t?[String(e),String(t)]:[e,t])(pa(e),pa(t));return a>i?1:a<i?-1:0},ma=(e,t)=>{for(let a=0;a<Math.max(e.length,t.length);a++){const i=ua(e[a]||0,t[a]||0);if(0!==i)return i}return 0},ha={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1]},va=Object.keys(ha),_a=e=>{if("string"!=typeof e)throw new TypeError("Invalid operator type, expected string but got "+typeof e);if(-1===va.indexOf(e))throw new Error(`Invalid operator, expected one of ${va.join("|")}`)};class ga{static getPlatforms(){return Array.from(ga.TEMPLATES.keys())}static isValidModeTemplate(e,t){return void 0!==t&&Object.keys(this.getPlatformTemplate(e).map_modes.templates).includes(t)}static getModeTemplate(e,t){return this.getPlatformTemplate(e).map_modes.templates[t]}static generateDefaultModes(e){return this.getPlatformTemplate(e).map_modes.defaultTemplates.map((e=>({template:e})))}static getTilesFromAttributesTemplates(e){var t;return null!==(t=this.getPlatformTemplate(e).tiles.from_attributes)&&void 0!==t?t:[]}static getTilesFromSensorsTemplates(e){var t;return null!==(t=this.getPlatformTemplate(e).tiles.from_sensors)&&void 0!==t?t:[]}static usesSensors(e,t){const a=this.getPlatformTemplate(t).sensors_from;return!!a&&la(e.config.version,a,">=")}static getPlatformTemplate(e){var t,a;return null!==(a=null!==(t=this.TEMPLATES.get(e))&&void 0!==t?t:this.TEMPLATES.get(this.DEFAULT_PLATFORM))&&void 0!==a?a:{templates:[],defaultTemplates:{}}}}ga.SEND_COMMAND_PLATFORM="send_command",ga.DEFAULT_PLATFORM="default",ga.MIIO2_KH_PLATFORM="KrzysztofHajdamowicz/miio2",ga.TEMPLATES=new Map([[ga.DEFAULT_PLATFORM,Qt],[ga.MIIO2_KH_PLATFORM,ia],[ga.SEND_COMMAND_PLATFORM,sa]]);let fa=class extends ne{constructor(){super(...arguments),this._initialized=!1}setConfig(e){this._config=e,this.loadCardHelpers()}shouldUpdate(){return this._initialized||this._initialize(),!0}get _title(){var e;return(null===(e=this._config)||void 0===e?void 0:e.title)||""}get _entity(){var e;return(null===(e=this._config)||void 0===e?void 0:e.entity)||""}get _vacuum_platform(){var e;return(null===(e=this._config)||void 0===e?void 0:e.vacuum_platform)||""}get _camera(){var e,t;return(null===(t=null===(e=this._config)||void 0===e?void 0:e.map_source)||void 0===t?void 0:t.camera)||""}get _map_locked(){var e;return(null===(e=this._config)||void 0===e?void 0:e.map_locked)||!1}get _two_finger_pan(){var e;return(null===(e=this._config)||void 0===e?void 0:e.two_finger_pan)||!1}render(){if(!this.hass||!this._helpers)return I``;this._helpers.importMoreInfoControl("climate");const e=Object.keys(this.hass.states),t=e.filter((e=>"camera"===e.substr(0,e.indexOf(".")))).filter((e=>{var t;return null===(t=this.hass)||void 0===t?void 0:t.states[e].attributes.calibration_points})),a=e.filter((e=>"vacuum"===e.substr(0,e.indexOf(".")))),i=ga.getPlatforms();return I`
            <div class="card-config">
                <div class="description">
                    ${Gt("editor.description.before_link")}<a
                        target="_blank"
                        href="https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor"
                        >${Gt("editor.description.link_text")}</a
                    >${Gt("editor.description.after_link")}
                </div>
                <div class="values">
                    <paper-input
                        label=${Gt("editor.label.name")}
                        .value=${this._title}
                        .configValue=${"title"}
                        @value-changed=${this._titleChanged}></paper-input>
                </div>
                <div class="values">
                    <paper-dropdown-menu
                        label=${Gt("editor.label.entity")}
                        @value-changed=${this._entityChanged}
                        .configValue=${"entity"}>
                        <paper-listbox slot="dropdown-content" .selected=${a.indexOf(this._entity)}>
                            ${a.map((e=>I` <paper-item>${e}</paper-item> `))}
                        </paper-listbox>
                    </paper-dropdown-menu>
                </div>
                <div class="values">
                    <paper-dropdown-menu
                        label=${Gt("editor.label.vacuum_platform")}
                        @value-changed=${this._entityChanged}
                        .configValue=${"vacuum_platform"}>
                        <paper-listbox slot="dropdown-content" .selected=${i.indexOf(this._vacuum_platform)}>
                            ${i.map((e=>I` <paper-item>${e}</paper-item> `))}
                        </paper-listbox>
                    </paper-dropdown-menu>
                </div>
                <div class="values">
                    <paper-dropdown-menu
                        label=${Gt("editor.label.camera")}
                        @value-changed=${this._cameraChanged}
                        .configValue=${"camera"}>
                        <paper-listbox slot="dropdown-content" .selected=${t.indexOf(this._camera)}>
                            ${t.map((e=>I` <paper-item>${e}</paper-item> `))}
                        </paper-listbox>
                    </paper-dropdown-menu>
                </div>
                <div class="values">
                    <ha-formfield .label=${Gt("editor.label.map_locked")}>
                        <ha-switch
                            .checked=${this._map_locked}
                            .configValue=${"map_locked"}
                            @change=${this._valueChanged}></ha-switch>
                    </ha-formfield>
                </div>
                <div class="values">
                    <ha-formfield .label=${Gt("editor.label.two_finger_pan")}>
                        <ha-switch
                            .checked=${this._two_finger_pan}
                            .configValue=${"two_finger_pan"}
                            @change=${this._valueChanged}></ha-switch>
                    </ha-formfield>
                </div>
            </div>
        `}_initialize(){void 0!==this.hass&&void 0!==this._config&&void 0!==this._helpers&&(this._initialized=!0)}async loadCardHelpers(){this._helpers=await window.loadCardHelpers()}_entityChanged(e){this._valueChanged(e)}_cameraChanged(e){if(!this._config||!this.hass)return;const t=e.target.value;if(this._camera===t)return;const a=Object.assign({},this._config);a.map_source={camera:t},a.calibration_source={camera:!0},this._config=a,ke(this,"config-changed",{config:this._config})}_titleChanged(e){this._valueChanged(e)}_valueChanged(e){if(!this._config||!this.hass)return;const t=e.target;if(this[`_${t.configValue}`]!==t.value){if(t.configValue)this._config=Object.assign(Object.assign({},this._config),{[t.configValue]:void 0!==t.checked?t.checked:t.value});else{const e=Object.assign({},this._config);delete e[t.configValue],this._config=e}ke(this,"config-changed",{config:this._config})}}static get styles(){return o`
            .values {
                padding-left: 16px;
                margin: 8px;
                display: grid;
            }

            ha-formfield {
                padding: 8px;
            }
        `}};e([se({attribute:!1})],fa.prototype,"hass",void 0),e([le()],fa.prototype,"_config",void 0),e([le()],fa.prototype,"_helpers",void 0),fa=e([re("xiaomi-vacuum-map-card-editor")],fa);const ba="ontouchstart"in window||navigator.maxTouchPoints>0;class ya extends HTMLElement{constructor(){super(),this.holdTime=500,this.held=!1,this.ripple=document.createElement("mwc-ripple")}connectedCallback(){Object.assign(this.style,{position:"absolute",width:ba?"100px":"50px",height:ba?"100px":"50px",transform:"translate(-50%, -50%)",pointerEvents:"none",zIndex:"999"}),this.appendChild(this.ripple),this.ripple.primary=!0,["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((e=>{document.addEventListener(e,(()=>{clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0}),{passive:!0})}))}bind(e,t){if(e.actionHandler)return;e.actionHandler=!0,e.addEventListener("contextmenu",(e=>{const t=e||window.event;return t.preventDefault&&t.preventDefault(),t.stopPropagation&&t.stopPropagation(),t.cancelBubble=!0,t.returnValue=!1,!1}));const a=e=>{let t,a;this.held=!1,e.touches?(t=e.touches[0].pageX,a=e.touches[0].pageY):(t=e.pageX,a=e.pageY),this.timer=window.setTimeout((()=>{this.startAnimation(t,a),this.held=!0}),this.holdTime)},i=a=>{a.preventDefault(),["touchend","touchcancel"].includes(a.type)&&void 0===this.timer||(clearTimeout(this.timer),this.stopAnimation(),this.timer=void 0,this.held?ke(e,"action",{action:"hold"}):t.hasDoubleClick?"click"===a.type&&a.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,ke(e,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,ke(e,"action",{action:"double_tap"})):ke(e,"action",{action:"tap"}))};e.addEventListener("touchstart",a,{passive:!0}),e.addEventListener("touchend",i),e.addEventListener("touchcancel",i),e.addEventListener("mousedown",a,{passive:!0}),e.addEventListener("click",i),e.addEventListener("keyup",(e=>{13===e.keyCode&&i(e)}))}startAnimation(e,t){Object.assign(this.style,{left:`${e}px`,top:`${t}px`,display:null}),this.ripple.disabled=!1,this.ripple.active=!0,this.ripple.unbounded=!0}stopAnimation(){this.ripple.active=!1,this.ripple.disabled=!0,this.style.display="none"}}customElements.define("action-handler-xiaomi-vacuum-map-card",ya);const xa=(e,t)=>{const a=(()=>{const e=document.body;if(e.querySelector("action-handler-xiaomi-vacuum-map-card"))return e.querySelector("action-handler-xiaomi-vacuum-map-card");const t=document.createElement("action-handler-xiaomi-vacuum-map-card");return e.appendChild(t),t})();a&&a.bind(e,t)},wa=(e=>(...t)=>({_$litDirective$:e,values:t}))(class extends class{constructor(e){}T(e,t,a){this.Σdt=e,this.M=t,this.Σct=a}S(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}}{update(e,[t]){return xa(e.element,t),D}render(e){}});class Ea{constructor(e){this.id=-1,this.nativePointer=e,this.pageX=e.pageX,this.pageY=e.pageY,this.clientX=e.clientX,this.clientY=e.clientY,self.Touch&&e instanceof Touch?this.id=e.identifier:ka(e)&&(this.id=e.pointerId)}getCoalesced(){return"getCoalescedEvents"in this.nativePointer?this.nativePointer.getCoalescedEvents().map((e=>new Ea(e))):[this]}}const ka=e=>self.PointerEvent&&e instanceof PointerEvent,za=()=>{};class Pa{constructor(e,{start:t=(()=>!0),move:a=za,end:i=za,rawUpdates:n=!1}={}){this._element=e,this.startPointers=[],this.currentPointers=[],this._pointerStart=e=>{if(0===e.button&&this._triggerPointerStart(new Ea(e),e))if(ka(e)){(e.target&&"setPointerCapture"in e.target?e.target:this._element).setPointerCapture(e.pointerId),this._element.addEventListener(this._rawUpdates?"pointerrawupdate":"pointermove",this._move),this._element.addEventListener("pointerup",this._pointerEnd),this._element.addEventListener("pointercancel",this._pointerEnd)}else window.addEventListener("mousemove",this._move),window.addEventListener("mouseup",this._pointerEnd)},this._touchStart=e=>{for(const t of Array.from(e.changedTouches))this._triggerPointerStart(new Ea(t),e)},this._move=e=>{const t=this.currentPointers.slice(),a="changedTouches"in e?Array.from(e.changedTouches).map((e=>new Ea(e))):[new Ea(e)],i=[];for(const e of a){const t=this.currentPointers.findIndex((t=>t.id===e.id));-1!==t&&(i.push(e),this.currentPointers[t]=e)}0!==i.length&&this._moveCallback(t,i,e)},this._triggerPointerEnd=(e,t)=>{const a=this.currentPointers.findIndex((t=>t.id===e.id));if(-1===a)return!1;this.currentPointers.splice(a,1),this.startPointers.splice(a,1);const i="touchcancel"===t.type||"pointercancel"===t.type;return this._endCallback(e,t,i),!0},this._pointerEnd=e=>{if(this._triggerPointerEnd(new Ea(e),e))if(ka(e)){if(this.currentPointers.length)return;this._element.removeEventListener(this._rawUpdates?"pointerrawupdate":"pointermove",this._move),this._element.removeEventListener("pointerup",this._pointerEnd),this._element.removeEventListener("pointercancel",this._pointerEnd)}else window.removeEventListener("mousemove",this._move),window.removeEventListener("mouseup",this._pointerEnd)},this._touchEnd=e=>{for(const t of Array.from(e.changedTouches))this._triggerPointerEnd(new Ea(t),e)},this._startCallback=t,this._moveCallback=a,this._endCallback=i,this._rawUpdates=n&&"onpointerrawupdate"in window,self.PointerEvent?this._element.addEventListener("pointerdown",this._pointerStart):(this._element.addEventListener("mousedown",this._pointerStart),this._element.addEventListener("touchstart",this._touchStart),this._element.addEventListener("touchmove",this._move),this._element.addEventListener("touchend",this._touchEnd),this._element.addEventListener("touchcancel",this._touchEnd))}stop(){this._element.removeEventListener("pointerdown",this._pointerStart),this._element.removeEventListener("mousedown",this._pointerStart),this._element.removeEventListener("touchstart",this._touchStart),this._element.removeEventListener("touchmove",this._move),this._element.removeEventListener("touchend",this._touchEnd),this._element.removeEventListener("touchcancel",this._touchEnd),this._element.removeEventListener(this._rawUpdates?"pointerrawupdate":"pointermove",this._move),this._element.removeEventListener("pointerup",this._pointerEnd),this._element.removeEventListener("pointercancel",this._pointerEnd),window.removeEventListener("mousemove",this._move),window.removeEventListener("mouseup",this._pointerEnd)}_triggerPointerStart(e,t){return!!this._startCallback(e,t)&&(this.currentPointers.push(e),this.startPointers.push(e),!0)}}var Ma,Sa;!function(e){e[e.MANUAL_RECTANGLE=0]="MANUAL_RECTANGLE",e[e.PREDEFINED_RECTANGLE=1]="PREDEFINED_RECTANGLE",e[e.ROOM=2]="ROOM",e[e.MANUAL_PATH=3]="MANUAL_PATH",e[e.MANUAL_POINT=4]="MANUAL_POINT",e[e.PREDEFINED_POINT=5]="PREDEFINED_POINT"}(Ma||(Ma={})),function(e){e[e.NONE=0]="NONE",e[e.INTERNAL=1]="INTERNAL",e[e.EXTERNAL=2]="EXTERNAL"}(Sa||(Sa={}));class Ca{constructor(e,t,a,i){this.domain=e,this.service=t,this.serviceData=a,this.target=i}}class Ta{constructor(e){this.service=e.service,this.serviceData=e.service_data,this.target=e.target}apply(e,t,a){const i=i=>Ta.getReplacedValue(i,e,t,a);let n,r;this.serviceData&&(n=this.getFilledTemplate(this.serviceData,i)),this.target&&(r=this.getFilledTemplate(this.target,i));const o=this.service.split(".");return new Ca(o[0],o[1],n,r)}getFilledTemplate(e,t){const a=JSON.parse(JSON.stringify(e));return this.replacer(a,t),a}replacer(e,t){for(const[a,i]of Object.entries(e))"object"==typeof i?this.replacer(i,t):"string"==typeof i&&(e[a]=t(i))}static getReplacedValue(e,t,a,i){switch(e){case"[[entity_id]]":return t;case"[[selection]]":return a;case"[[repeats]]":return i;case"[[point_x]]":return this.isPoint(a)?a[0]:e;case"[[point_y]]":return this.isPoint(a)?a[1]:e;default:return e}}static isPoint(e){return"number"==typeof e[0]&&2==e.length}}class $a{constructor(e,t,a){var i,n,r,o,s,l,c,d;this.config=t,this.name=null!==(i=t.name)&&void 0!==i?i:Gt("map_mode.invalid",a),this.icon=null!==(n=t.icon)&&void 0!==n?n:"mdi:help",this.selectionType=t.selection_type?Ma[t.selection_type]:Ma.PREDEFINED_POINT,this.maxSelections=null!==(r=t.max_selections)&&void 0!==r?r:999,this.coordinatesRounding=null===(o=t.coordinates_rounding)||void 0===o||o,this.runImmediately=null!==(s=t.run_immediately)&&void 0!==s&&s,this.repeatsType=t.repeats_type?Sa[t.repeats_type]:Sa.NONE,this.maxRepeats=null!==(l=t.max_repeats)&&void 0!==l?l:1,this.serviceCallSchema=new Ta(null!==(c=t.service_call_schema)&&void 0!==c?c:{}),this.predefinedSelections=null!==(d=t.predefined_selections)&&void 0!==d?d:[],this._applyTemplateIfPossible(e,t,a),$a.PREDEFINED_SELECTION_TYPES.includes(this.selectionType)||(this.runImmediately=!1)}_applyTemplateIfPossible(e,t,a){if(!t.template||!ga.isValidModeTemplate(e,t.template))return;const i=ga.getModeTemplate(e,t.template);!t.name&&i.name&&(this.name=Gt(i.name,a)),!t.icon&&i.icon&&(this.icon=i.icon),!t.selection_type&&i.selection_type&&(this.selectionType=Ma[i.selection_type]),!t.max_selections&&i.max_selections&&(this.maxSelections=i.max_selections),void 0===t.coordinates_rounding&&void 0!==i.coordinates_rounding&&(this.coordinatesRounding=i.coordinates_rounding),void 0===t.run_immediately&&void 0!==i.run_immediately&&(this.runImmediately=i.run_immediately),!t.repeats_type&&i.repeats_type&&(this.repeatsType=Sa[i.repeats_type]),!t.max_repeats&&i.max_repeats&&(this.maxRepeats=i.max_repeats),!t.service_call_schema&&i.service_call_schema&&(this.serviceCallSchema=new Ta(i.service_call_schema))}getServiceCall(e,t,a){return this.serviceCallSchema.apply(e,t,a)}}$a.PREDEFINED_SELECTION_TYPES=[Ma.PREDEFINED_RECTANGLE,Ma.ROOM,Ma.PREDEFINED_POINT];class Na{constructor(e,t){this.x=e,this.y=t}}function Aa(e){e.preventDefault(),e.stopPropagation(),e.stopImmediatePropagation()}function Ra(e,t){const a=e.indexOf(t,0);return a>-1&&e.splice(a,1),a}function La(e,t){var a,i,n,r;const o=new Set;return e.entity&&o.add(e.entity),e.map_source.camera&&o.add(e.map_source.camera),e.calibration_source.entity&&o.add(e.calibration_source.entity),(null!==(a=e.icons)&&void 0!==a?a:[]).filter((e=>e.conditions)).flatMap((e=>e.conditions)).map((e=>null==e?void 0:e.entity)).forEach((e=>{e&&o.add(e)})),(null!==(i=e.tiles)&&void 0!==i?i:[]).forEach((e=>o.add(e.entity))),(null!==(n=e.tiles)&&void 0!==n?n:[]).filter((e=>e.conditions)).flatMap((e=>e.conditions)).map((e=>null==e?void 0:e.entity)).forEach((e=>{e&&o.add(e)})),(null!==(r=e.map_modes)&&void 0!==r?r:[]).map((a=>{var i;return new $a(null!==(i=e.vacuum_platform)&&void 0!==i?i:"default",a,t)})).forEach((e=>function(e){const t=new Set;switch(e.selectionType){case Ma.PREDEFINED_RECTANGLE:e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.zones)).forEach((e=>t.add(e.zones.split(".attributes.")[0])));break;case Ma.PREDEFINED_POINT:e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.position)).forEach((e=>t.add(e.position.split(".attributes.")[0])))}return t}(e).forEach((e=>o.add(e))))),o}function Oa(e,t){var a;return(null!==(a=e.conditions)&&void 0!==a?a:[]).every((e=>function(e,t){const a=e.attribute?t.states[e.entity].attributes[e.attribute]:t.states[e.entity].state;return e.value?a==e.value:!!e.value_not&&a!=e.value_not}(e,t)))}function Ia(e,t){return e?t():null}function ja(e,t){return a=>{e.hass&&t&&a.detail.action&&function(e,t,a,i){var n;"double_tap"===i&&a.double_tap_action?n=a.double_tap_action:"hold"===i&&a.hold_action?n=a.hold_action:"tap"===i&&a.tap_action&&(n=a.tap_action),Pe(e,t,a,n)}(e,e.hass,t,a.detail.action)}}function Da(e,t){let a,i;e instanceof MouseEvent&&(a=e.clientX,i=e.clientY),window.TouchEvent&&e instanceof TouchEvent&&e.touches&&(a=e.touches[0].clientX,i=e.touches[0].clientY);const n=t.getScreenCTM();return n?new Na((a-n.e)/n.a,(i-n.f)/n.d):new Na(0,0)}function Fa(e,t){return t?Math.sqrt((t.clientX-e.clientX)**2+(t.clientY-e.clientY)**2):0}function Ua(e,t){return t?{clientX:(e.clientX+t.clientX)/2,clientY:(e.clientY+t.clientY)/2}:e}function Va(e,t){return"number"==typeof e?e:e.trimRight().endsWith("%")?t*parseFloat(e)/100:parseFloat(e)}let qa;function Ha(){return qa||(qa=document.createElementNS("http://www.w3.org/2000/svg","svg"))}function Ba(){return Ha().createSVGMatrix()}function Xa(){return Ha().createSVGPoint()}class Ya extends HTMLElement{constructor(){super(),this._transform=Ba(),this._enablePan=!0,this._twoFingerPan=!1,new MutationObserver((()=>this._stageElChange())).observe(this,{childList:!0});const e=new Pa(this,{start:(t,a)=>!(a.target.classList.contains("draggable")&&e.currentPointers.length<2)&&(!(2===e.currentPointers.length||!this._positioningEl)&&((this.enablePan||1==e.currentPointers.length||a instanceof PointerEvent&&"mouse"==a.pointerType)&&(this.enablePan=!0),!0)),move:t=>{this.enablePan&&this._onPointerMove(t,e.currentPointers)},end:(t,a,i)=>(this.twoFingerPan&&1==e.currentPointers.length&&(this.enablePan=!1),Aa(a),!1)});this.addEventListener("wheel",(e=>this._onWheel(e)))}static get observedAttributes(){return["min-scale","max-scale","no-default-pan","two-finger-pan"]}attributeChangedCallback(e,t,a){"min-scale"===e&&this.scale<this.minScale&&this.setTransform({scale:this.minScale}),"max-scale"===e&&this.scale>this.maxScale&&this.setTransform({scale:this.maxScale}),"no-default-pan"===e&&(this.enablePan=!("1"==a||"true"==a)),"two-finger-pan"===e&&("1"==a||"true"==a?(this.twoFingerPan=!0,this.enablePan=!1):this.twoFingerPan=!1)}get minScale(){const e=this.getAttribute("min-scale");if(!e)return.01;const t=parseFloat(e);return Number.isFinite(t)?Math.max(.01,t):.01}set minScale(e){e&&this.setAttribute("min-scale",String(e))}get maxScale(){const e=this.getAttribute("max-scale");if(!e)return 100;const t=parseFloat(e);return Number.isFinite(t)?Math.min(100,t):100}set maxScale(e){e&&this.setAttribute("max-scale",String(e))}set enablePan(e){this._enablePan=e,this._enablePan?this._enablePan&&"none"!=this.style.touchAction&&(this.style.touchAction="none"):this.style.touchAction="pan-y pan-x"}get enablePan(){return this._enablePan}set twoFingerPan(e){this._twoFingerPan=e}get twoFingerPan(){return this._twoFingerPan}connectedCallback(){this._stageElChange()}get x(){return this._transform.e}get y(){return this._transform.f}get scale(){return this._transform.a}scaleTo(e,t={}){let{originX:a=0,originY:i=0}=t;const{relativeTo:n="content",allowChangeEvent:r=!1}=t,o="content"===n?this._positioningEl:this;if(!o||!this._positioningEl)return void this.setTransform({scale:e,allowChangeEvent:r});const s=o.getBoundingClientRect();if(a=Va(a,s.width),i=Va(i,s.height),"content"===n)a+=this.x,i+=this.y;else{const e=this._positioningEl.getBoundingClientRect();a-=e.left,i-=e.top}this._applyChange({allowChangeEvent:r,originX:a,originY:i,scaleDiff:e/this.scale})}setTransform(e={}){const{scale:t=this.scale,allowChangeEvent:a=!1}=e;let{x:i=this.x,y:n=this.y}=e;if(!this._positioningEl)return void this._updateTransform(t,i,n,a);const r=this.getBoundingClientRect(),o=this._positioningEl.getBoundingClientRect();if(!r.width||!r.height)return void this._updateTransform(t,i,n,a);let s=Xa();s.x=o.left-r.left,s.y=o.top-r.top;let l=Xa();l.x=o.width+s.x,l.y=o.height+s.y;const c=Ba().translate(i,n).scale(t).multiply(this._transform.inverse());s=s.matrixTransform(c),l=l.matrixTransform(c),s.x>r.width?i+=r.width-s.x:l.x<0&&(i+=-l.x),s.y>r.height?n+=r.height-s.y:l.y<0&&(n+=-l.y),this._updateTransform(t,i,n,a)}_updateTransform(e,t,a,i){if(!(e<this.minScale)&&!(e>this.maxScale)&&(e!==this.scale||t!==this.x||a!==this.y)&&(this._transform.e=t,this._transform.f=a,this._transform.d=this._transform.a=e,this.style.setProperty("--x",this.x+"px"),this.style.setProperty("--y",this.y+"px"),this.style.setProperty("--scale",this.scale+""),i)){const e=new Event("change",{bubbles:!0});this.dispatchEvent(e)}}_stageElChange(){this._positioningEl=void 0,0!==this.children.length&&(this._positioningEl=this.children[0],this.children.length>1&&console.warn("<pinch-zoom> must not have more than one child."),this.setTransform({allowChangeEvent:!0}))}_onWheel(e){if(!this._positioningEl)return;e.preventDefault();const t=this._positioningEl.getBoundingClientRect();let{deltaY:a}=e;const{ctrlKey:i,deltaMode:n}=e;1===n&&(a*=15);const r=1-a/(i?100:300);this._applyChange({scaleDiff:r,originX:e.clientX-t.left,originY:e.clientY-t.top,allowChangeEvent:!0})}_onPointerMove(e,t){if(!this._positioningEl)return;const a=this._positioningEl.getBoundingClientRect(),i=Ua(e[0],e[1]),n=Ua(t[0],t[1]),r=i.clientX-a.left,o=i.clientY-a.top,s=Fa(e[0],e[1]),l=Fa(t[0],t[1]),c=s?l/s:1;this._applyChange({originX:r,originY:o,scaleDiff:c,panX:n.clientX-i.clientX,panY:n.clientY-i.clientY,allowChangeEvent:!0})}_applyChange(e={}){const{panX:t=0,panY:a=0,originX:i=0,originY:n=0,scaleDiff:r=1,allowChangeEvent:o=!1}=e,s=Ba().translate(t,a).translate(i,n).translate(this.x,this.y).scale(r).translate(-i,-n).scale(this.scale);this.setTransform({allowChangeEvent:o,scale:s.a,x:s.e,y:s.f})}}customElements.define("pinch-zoom",Ya);class Wa{constructor(e){this._context=e}scaled(e){return e/this._context.scale()}scaledCss(e){return parseFloat(this._context.cssEvaluator(e))/this._context.scale()}realScaled(e){return window.chrome?e/this._context.realScale():this.scaled(e/this._context.realScale())}realScaled2(e){return e*this._context.realScale()}realScaled2Point(e){return[this.realScaled2(e[0]),this.realScaled2(e[1])]}realScaledPoint(e){return[this.realScaled(e[0]),this.realScaled(e[1])]}update(){this._context.update()}localize(e){return this._context.localize(e)}getMousePosition(e){return this._context.mousePositionCalculator(e)}vacuumToRealMap(e,t){var a;const i=null===(a=this._context.coordinatesConverter())||void 0===a?void 0:a.vacuumToMap(e,t);if(!i)throw Error("Missing calibration");return i}vacuumToScaledMap(e,t){return this.realScaled2Point(this.vacuumToRealMap(e,t))}scaledMapToVacuum(e,t){const[a,i]=this.realScaledPoint([e,t]);return this.realMapToVacuum(a,i)}realMapToVacuum(e,t){var a;const i=null===(a=this._context.coordinatesConverter())||void 0===a?void 0:a.mapToVacuum(e,t);if(!i)throw Error("Missing calibration");return this._context.roundMap(i)}renderIcon(e,t,a){const i=e?this.vacuumToScaledMap(e.x,e.y):[];return j`${Ia(null!=e&&i.length>0,(()=>j`
                <foreignObject class="${a}"
                               style="--x-icon: ${i[0]}px; --y-icon: ${i[1]}px"
                               @click="${t}">
                    <div class="map-icon-wrapper">
                        <ha-icon icon="${null==e?void 0:e.name}"></ha-icon>
                    </div>
                </foreignObject>
            `))}`}renderLabel(e,t){const a=e?this.vacuumToScaledMap(e.x,e.y):[];return j`${Ia(null!=e&&a.length>0,(()=>{var i,n;return j`
                <text class="${t}"
                      style="--offset-x: ${null!==(i=null==e?void 0:e.offset_x)&&void 0!==i?i:0}px; --offset-y: ${null!==(n=null==e?void 0:e.offset_y)&&void 0!==n?n:0}px"
                      x="${a[0]}"
                      y="${a[1]}">
                    ${null==e?void 0:e.text}
                </text>
            `}))}`}vacuumToMapRect(e){const[t,a,i,n]=e,r=[t,a],o=[i,a],s=[i,n],l=[t,n],c=this.vacuumToScaledMap(t,a),d=this.vacuumToScaledMap(i,a),p=this.vacuumToScaledMap(i,n),u=this.vacuumToScaledMap(t,n),m=[r,o,s,l,r,o,s,l],h=[c,d,p,u,c,d,p,u],v=[c,d,p,u],_=h.indexOf(Wa.findTopLeft(v));return[h.slice(_,_+4),m.slice(_,_+4)]}static findTopLeft(e){const t=e.sort(((e,t)=>e[1]-t[1]))[0],a=e.indexOf(t),i=e[(a+1)%4],n=e[(a+3)%4];return Wa.calcAngle(t,i)<Wa.calcAngle(t,n)?i:t}static calcAngle(e,t){let a=Math.atan2(t[1]-e[1],t[0]-e[0]);return a>Math.PI/2&&(a=Math.PI-a),a}static get styles(){return o`
            .map-icon-wrapper {
                width: inherit;
                height: inherit;
                background: inherit;
                display: flex;
                align-items: center;
                justify-content: center;
            }
        `}}var Ga;!function(e){e[e.NONE=0]="NONE",e[e.RESIZE=1]="RESIZE",e[e.MOVE=2]="MOVE"}(Ga||(Ga={}));class Za extends Wa{constructor(e,t,a,i,n,r){super(r),this._id=n,this._dragMode=Ga.NONE,this._vacRect=this._toVacuumFromDimensions(e,t,a,i),this._vacRectSnapshot=this._vacRect}render(){const e=this._vacRect,t=this.vacuumToMapRect(e)[0],a=t[0],i=t[2],n=t[3],r=Za.calcAngle(t[0],t[3]);return j`
            <g class="manual-rectangle-wrapper ${this.isSelected()?"selected":""}"
               style="--x-resize:${i[0]}px; 
                      --y-resize:${i[1]}px;
                      --x-delete:${n[0]}px;
                      --y-delete:${n[1]}px;
                      --x-description:${a[0]}px;
                      --y-description:${a[1]}px;
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
                         points="${Za._toPoints(t)}">
                </polygon>
                <text class="manual-rectangle-description">
                    ${this._id} ${this._getDimensions()}
                </text>
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
        `}isSelected(){return null!=this._selectedElement}_getDimensions(){const[e,t,a,i]=this.toVacuum(),n=a-e,r=i-t,o=this._context.roundingEnabled()?1e3:1,s=e=>(e/o).toFixed(1);return`${s(n)}${this.localize("unit.meter_shortcut")} x ${s(r)}${this.localize("unit.meter_shortcut")}`}_startDrag(e){var t;if(window.TouchEvent&&e instanceof TouchEvent&&e.touches.length>1)return;if(!e.target.classList.contains("draggable"))return;if(!(null===(t=e.target.parentElement)||void 0===t?void 0:t.classList.contains("manual-rectangle-wrapper")))return;if(!e.target.parentElement)return;Aa(e),this._selectedTarget=e.target;const a=e.target;a.classList.contains("movable")?this._dragMode=Ga.MOVE:a.classList.contains("resizer")?this._dragMode=Ga.RESIZE:this._dragMode=Ga.NONE,this._selectedElement=e.target.parentElement,this._vacRectSnapshot=[...this._vacRect];const i=this.getMousePosition(e);this._startPointSnapshot=this.scaledMapToVacuum(i.x,i.y),this.update()}externalDrag(e){this._drag(e)}_drag(e){if(!(window.TouchEvent&&e instanceof TouchEvent&&e.touches.length>1)&&this._selectedElement){Aa(e);const t=this.getMousePosition(e);if(t){const e=this.scaledMapToVacuum(t.x,t.y),a=e[0]-this._startPointSnapshot[0],i=e[1]-this._startPointSnapshot[1];switch(this._dragMode){case Ga.MOVE:this._vacRect=[this._vacRectSnapshot[0]+a,this._vacRectSnapshot[1]+i,this._vacRectSnapshot[2]+a,this._vacRectSnapshot[3]+i],this._setup(this.vacuumToMapRect(this._vacRect)[0]);break;case Ga.RESIZE:const e=this.vacuumToMapRect(this._vacRectSnapshot)[1][0],t=[...this._vacRect];e[0]===this._vacRectSnapshot[0]?this._vacRect[2]=this._vacRectSnapshot[2]+a:this._vacRect[0]=this._vacRectSnapshot[0]-a,e[1]===this._vacRectSnapshot[1]?this._vacRect[3]=this._vacRectSnapshot[3]-i:this._vacRect[1]=this._vacRectSnapshot[1]+i,(this._vacRect[0]>this._vacRect[2]||this._vacRect[1]>this._vacRect[3])&&(this._vacRect=t),this._setup(this.vacuumToMapRect(this._vacRect)[0]);case Ga.NONE:}}}}_setup(e){var t,a,i,n,r,o,s,l,c,d,p,u,m,h,v,_,g;null===(i=null===(a=null===(t=this._selectedElement)||void 0===t?void 0:t.children)||void 0===a?void 0:a.item(0))||void 0===i||i.setAttribute("points",Za._toPoints(e));const f=e[0],b=e[2],y=e[3],x=Za.calcAngle(e[0],e[3]);null===(r=null===(n=this._selectedElement)||void 0===n?void 0:n.style)||void 0===r||r.setProperty("--x-resize",b[0]+"px"),null===(s=null===(o=this._selectedElement)||void 0===o?void 0:o.style)||void 0===s||s.setProperty("--y-resize",b[1]+"px"),null===(c=null===(l=this._selectedElement)||void 0===l?void 0:l.style)||void 0===c||c.setProperty("--x-delete",y[0]+"px"),null===(p=null===(d=this._selectedElement)||void 0===d?void 0:d.style)||void 0===p||p.setProperty("--y-delete",y[1]+"px"),null===(m=null===(u=this._selectedElement)||void 0===u?void 0:u.style)||void 0===m||m.setProperty("--x-description",f[0]+"px"),null===(v=null===(h=this._selectedElement)||void 0===h?void 0:h.style)||void 0===v||v.setProperty("--y-description",f[1]+"px"),null===(g=null===(_=this._selectedElement)||void 0===_?void 0:_.style)||void 0===g||g.setProperty("--angle-description",x+"rad")}_endDrag(e){Aa(e),this._selectedElement=null,this._selectedTarget=null,this.update()}_delete(e){Aa(e);const t=Ra(this._context.selectedManualRectangles(),this);if(t>-1){for(let e=t;e<this._context.selectedManualRectangles().length;e++)this._context.selectedManualRectangles()[e]._id=(e+1).toString();ze("selection"),this._context.update()}}static _toPoints(e){return e.map((e=>e.join(", "))).join(" ")}_toVacuumFromDimensions(e,t,a,i){const n=this.realScaled(e),r=this.realScaled(t),o=this.realScaled(a),s=this.realScaled(i),l=this.realMapToVacuum(n,r),c=this.realMapToVacuum(n+o,r+s),d=[l[0],c[0]].sort(),p=[l[1],c[1]].sort();return[d[0],p[0],d[1],p[1]]}toVacuum(e=null){return null!=e?[...this._vacRect,e]:this._vacRect}static get styles(){return o`
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
        `}}class Ka{constructor(e,t,a,i,n,r,o,s,l,c,d,p,u,m){this.scale=e,this.realScale=t,this.mousePositionCalculator=a,this.update=i,this.coordinatesConverter=n,this.selectedManualRectangles=r,this.selectedPredefinedRectangles=o,this.selectedRooms=s,this.selectedPredefinedPoint=l,this.roundingEnabled=c,this.maxSelections=d,this.cssEvaluator=p,this.runImmediately=u,this.localize=m}roundMap([e,t]){return this.roundingEnabled()?[Math.round(e),Math.round(t)]:[e,t]}}class Ja extends Wa{constructor(e,t,a){super(a),this._x=e,this._y=t}}class Qa extends Ja{constructor(e,t,a){super(e,t,a)}render(){return j`
            <g class="manual-point-wrapper" style="--x-point:${this._x}px; --y-point:${this._y}px;">
                <circle class="manual-point"></circle>
            </g>
        `}imageX(){return this.realScaled(this._x)}imageY(){return this.realScaled(this._y)}toVacuum(e=null){const[t,a]=this.realMapToVacuum(this.imageX(),this.imageY());return null===e?[t,a]:[t,a,e]}static get styles(){return o`
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
        `}}class ei extends Wa{constructor(e,t,a){super(a),this.x=e,this.y=t}imageX(){return this.realScaled(this.x)}imageY(){return this.realScaled(this.y)}renderMask(){return j`
            <circle style="r: var(--radius)"
                    cx="${this.x}"
                    cy="${this.y}"
                    fill="black">
            </circle>`}render(){return j`
            <circle class="manual-path-point"
                    cx="${this.x}"
                    cy="${this.y}">
            </circle>`}}class ti extends Wa{constructor(e,t){super(t),this.points=e}render(){if(0===this.points.length)return j``;const e=this.points.map((e=>e.x)),t=this.points.map((e=>e.y)),a=Math.max(...e),i=Math.min(...e),n=Math.max(...t),r=Math.min(...t);return j`
            <g class="manual-path-wrapper">
                <defs>
                    <mask id="manual-path-circles-filter">
                        <rect x="${i}" y="${r}" width="${a-i}" height="${n-r}"
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
        `}toVacuum(e=null){return this.points.map((t=>{const[a,i]=this.realMapToVacuum(t.imageX(),t.imageY());return null===e?[a,i]:[a,i,e]}))}addPoint(e,t){this.points.push(new ei(e,t,this._context))}clear(){this.points=[]}removeLast(){this.points.pop()}static get styles(){return o`
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
        `}}class ai extends Wa{constructor(e,t){var a;super(t),this._config=e,this._selected=!1,this._iconConfig=null!==(a=this._config.icon)&&void 0!==a?a:{x:this._config.position[0],y:this._config.position[1],name:"mdi:map-marker"}}render(){return j`
            <g class="predefined-point-wrapper ${this._selected?"selected":""}">
                ${this.renderIcon(this._iconConfig,(()=>this._click()),"predefined-point-icon-wrapper")}
                ${this.renderLabel(this._config.label,"predefined-point-label")}
            </g>
        `}_click(){if(this._selected=!this._selected,ze("selection"),this._selected){const e=this._context.selectedPredefinedPoint().pop();void 0!==e&&(e._selected=!1),this._context.selectedPredefinedPoint().push(this)}else Ra(this._context.selectedPredefinedPoint(),this);if(this._context.runImmediately())return this._selected=!1,void Ra(this._context.selectedPredefinedPoint(),this);this.update()}toVacuum(e=null){return"string"==typeof this._config.position?[0,0]:null===e?this._config.position:[...this._config.position,e]}static get styles(){return o`
            .predefined-point-wrapper {
            }

            .predefined-point-icon-wrapper {
                x: var(--x-icon);
                y: var(--y-icon);
                height: var(--map-card-internal-predefined-point-icon-wrapper-size);
                width: var(--map-card-internal-predefined-point-icon-wrapper-size);
                border-radius: var(--map-card-internal-small-radius);
                transform-box: fill-box;
                transform: scale(calc(1 / var(--map-scale)))
                    translate(
                        calc(var(--map-card-internal-predefined-point-icon-wrapper-size) / -2),
                        calc(var(--map-card-internal-predefined-point-icon-wrapper-size) / -2)
                    );
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
                transform: translate(
                    calc(var(--offset-x) / var(--map-scale)),
                    calc(var(--offset-y) / var(--map-scale))
                );
                font-size: calc(var(--map-card-internal-predefined-point-label-font-size) / var(--map-scale));
                fill: var(--map-card-internal-predefined-point-label-color);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-point-wrapper.selected > .predefined-point-icon-wrapper {
                background: var(--map-card-internal-predefined-point-icon-background-color-selected);
                color: var(--map-card-internal-predefined-point-icon-color-selected);
            }

            .predefined-point-wrapper.selected > .predefined-point-label {
                fill: var(--map-card-internal-predefined-point-label-color-selected);
            }
        `}static getFromEntities(e,t,a){return e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.position)).map((e=>e.position.split(".attributes."))).flatMap((e=>{const a=t.states[e[0]],i=2===e.length?a.attributes[e[1]]:a.state;let n;try{n=JSON.parse(i)}catch(e){n=i}return n})).map((e=>new ai({position:e,label:void 0,icon:{x:e[0],y:e[1],name:"mdi:map-marker"}},a())))}}class ii extends Wa{constructor(e,t){super(t),this._config=e,this._selected=!1}render(){let e=[];"string"!=typeof this._config.zones&&(e=this._config.zones);const t=e.map((e=>this.vacuumToMapRect(e)[0]));return j`
            <g class="predefined-rectangle-wrapper ${this._selected?"selected":""}">
                ${t.map((e=>j`
                    <polygon class="predefined-rectangle"
                             points="${e.map((e=>e.join(", "))).join(" ")}"
                             @click="${()=>this._click()}">
                    </polygon>
                `))}
                ${this.renderIcon(this._config.icon,(()=>this._click()),"predefined-rectangle-icon-wrapper")}
                ${this.renderLabel(this._config.label,"predefined-rectangle-label")}
            </g>
        `}_click(){if(!this._selected&&this._context.selectedPredefinedRectangles().map((e=>e.size())).reduce(((e,t)=>e+t),0)+this.size()>this._context.maxSelections())ze("failure");else{if(this._selected=!this._selected,this._selected?this._context.selectedPredefinedRectangles().push(this):Ra(this._context.selectedPredefinedRectangles(),this),this._context.runImmediately())return this._selected=!1,void Ra(this._context.selectedPredefinedRectangles(),this);ze("selection"),this.update()}}size(){return this._config.zones.length}toVacuum(e){return"string"==typeof this._config.zones?[]:null===e?this._config.zones:this._config.zones.map((t=>[...t,e]))}static get styles(){return o`
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
                transform: scale(calc(1 / var(--map-scale)))
                    translate(
                        calc(var(--map-card-internal-predefined-rectangle-icon-wrapper-size) / -2),
                        calc(var(--map-card-internal-predefined-rectangle-icon-wrapper-size) / -2)
                    );
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
                transform: translate(
                    calc(var(--offset-x) / var(--map-scale)),
                    calc(var(--offset-y) / var(--map-scale))
                );
                font-size: calc(var(--map-card-internal-predefined-rectangle-label-font-size) / var(--map-scale));
                fill: var(--map-card-internal-predefined-rectangle-label-color);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .predefined-rectangle-wrapper.selected > .predefined-rectangle {
                stroke: var(--map-card-internal-predefined-rectangle-line-color-selected);
                fill: var(--map-card-internal-predefined-rectangle-fill-color-selected);
            }

            .predefined-rectangle-wrapper.selected > .predefined-rectangle-icon-wrapper {
                background: var(--map-card-internal-predefined-rectangle-icon-background-color-selected);
                color: var(--map-card-internal-predefined-rectangle-icon-color-selected);
            }

            .predefined-rectangle-wrapper.selected > .predefined-rectangle-label {
                fill: var(--map-card-internal-predefined-rectangle-label-color-selected);
            }
        `}static getFromEntities(e,t,a){return e.predefinedSelections.map((e=>e)).filter((e=>"string"==typeof e.zones)).map((e=>e.zones.split(".attributes."))).flatMap((e=>{const a=t.states[e[0]],i=2===e.length?a.attributes[e[1]]:a.state;let n;try{n=JSON.parse(i)}catch(e){n=i}return n})).map((e=>new ii({zones:[e],label:void 0,icon:{x:(e[0]+e[2])/2,y:(e[1]+e[3])/2,name:"mdi:broom"}},a())))}}class ni extends Wa{constructor(e,t){super(t),this._config=e,this._selected=!1}render(){var e,t;const a=(null!==(t=null===(e=this._config)||void 0===e?void 0:e.outline)&&void 0!==t?t:[]).map((e=>this.vacuumToScaledMap(e[0],e[1])));return j`
            <g class="room-wrapper ${this._selected?"selected":""} room-${this._config.id}-wrapper">
                <polygon class="room-outline"
                         points="${a.map((e=>e.join(", "))).join(" ")}"
                         @click="${()=>this._click()}">
                </polygon>
                ${this.renderIcon(this._config.icon,(()=>this._click()),"room-icon-wrapper")}
                ${this.renderLabel(this._config.label,"room-label")}
            </g>
        `}toVacuum(){return this._config.id}_click(){if(!this._selected&&this._context.selectedRooms().length>=this._context.maxSelections())ze("failure");else{if(this._selected=!this._selected,this._selected?this._context.selectedRooms().push(this):Ra(this._context.selectedRooms(),this),this._context.runImmediately())return this._selected=!1,void Ra(this._context.selectedRooms(),this);ze("selection"),this.update()}}static get styles(){return o`
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
                transform: scale(calc(1 / var(--map-scale)))
                    translate(
                        calc(var(--map-card-internal-room-icon-wrapper-size) / -2),
                        calc(var(--map-card-internal-room-icon-wrapper-size) / -2)
                    );
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
                transform: translate(
                    calc(var(--offset-x) / var(--map-scale)),
                    calc(var(--offset-y) / var(--map-scale))
                );
                font-size: calc(var(--map-card-internal-room-label-font-size) / var(--map-scale));
                fill: var(--map-card-internal-room-label-color);
                transition: color var(--map-card-internal-transitions-duration) ease,
                    background var(--map-card-internal-transitions-duration) ease;
            }

            .room-wrapper.selected > .room-outline {
                stroke: var(--map-card-internal-room-outline-line-color-selected);
                fill: var(--map-card-internal-room-outline-fill-color-selected);
            }

            .room-wrapper.selected > .room-icon-wrapper {
                background: var(--map-card-internal-room-icon-background-color-selected);
                color: var(--map-card-internal-room-icon-color-selected);
            }

            .room-wrapper.selected > .room-label {
                fill: var(--map-card-internal-room-label-color-selected);
            }
        `}}function ri(e){return e.x?e.y?e.name?[]:["validation.preset.map_modes.predefined_selections.icon.name.missing"]:["validation.preset.map_modes.predefined_selections.icon.y.missing"]:["validation.preset.map_modes.predefined_selections.icon.x.missing"]}function oi(e){return e.x?e.y?e.text?[]:["validation.preset.map_modes.predefined_selections.label.text.missing"]:["validation.preset.map_modes.predefined_selections.label.y.missing"]:["validation.preset.map_modes.predefined_selections.label.x.missing"]}function si(e,t,a){var i,n;if(!t)return["validation.preset.map_modes.invalid"];if(t.template&&!ga.isValidModeTemplate(e,t.template))return[["validation.preset.map_modes.template.invalid","{0}",t.template]];const r=[];t.template||t.icon||r.push("validation.preset.map_modes.icon.missing"),t.template||t.name||r.push("validation.preset.map_modes.name.missing"),t.template||t.service_call_schema||r.push("validation.preset.map_modes.service_call_schema.missing");const o=new $a(e,t,a);switch(o.selectionType){case Ma.PREDEFINED_RECTANGLE:o.predefinedSelections.flatMap((e=>function(e){const t=e,a=[];return t.zones||a.push("validation.preset.map_modes.predefined_selections.zones.missing"),"string"!=typeof t.zones&&t.zones.filter((e=>4!=e.length)).length>0&&a.push("validation.preset.map_modes.predefined_selections.zones.invalid_parameters_number"),t.icon&&ri(t.icon).forEach((e=>a.push(e))),t.label&&oi(t.label).forEach((e=>a.push(e))),a}(e))).forEach((e=>r.push(e)));break;case Ma.ROOM:o.predefinedSelections.flatMap((e=>function(e){var t;const a=e,i=[];return a.id||i.push("validation.preset.map_modes.predefined_selections.rooms.id.missing"),a.id.toString().match(/^[a-z0-9]+$/i)||i.push(["validation.preset.map_modes.predefined_selections.rooms.id.invalid_format","{0}",a.id.toString()]),(null!==(t=a.outline)&&void 0!==t?t:[]).filter((e=>2!=e.length)).length>0&&i.push("validation.preset.map_modes.predefined_selections.rooms.outline.invalid_parameters_number"),a.icon&&ri(a.icon).forEach((e=>i.push(e))),a.label&&oi(a.label).forEach((e=>i.push(e))),i}(e))).forEach((e=>r.push(e)));break;case Ma.PREDEFINED_POINT:o.predefinedSelections.flatMap((e=>function(e){var t;const a=e,i=[];return a.position||i.push("validation.preset.map_modes.predefined_selections.points.position.missing"),"string"!=typeof a.position&&2!=(null===(t=a.position)||void 0===t?void 0:t.length)&&i.push("validation.preset.map_modes.predefined_selections.points.position.invalid_parameters_number"),a.icon&&ri(a.icon).forEach((e=>i.push(e))),a.label&&oi(a.label).forEach((e=>i.push(e))),i}(e))).forEach((e=>r.push(e)));break;case Ma.MANUAL_RECTANGLE:case Ma.MANUAL_PATH:case Ma.MANUAL_POINT:null!==(n=null===(i=o.predefinedSelections)||void 0===i?void 0:i.length)&&void 0!==n&&n&&r.push(["validation.preset.map_modes.predefined_selections.not_applicable","{0}",Ma[o.selectionType]])}return t.service_call_schema&&function(e){return e.service?e.service.includes(".")?[]:[["validation.preset.map_modes.service_call_schema.service.invalid","{0}",e.service]]:["validation.preset.map_modes.service_call_schema.service.missing"]}(t.service_call_schema).forEach((e=>r.push(e))),r}function li(e,t,a){var i,n,r,o;const s=[],l=new Map([["entity","validation.preset.entity.missing"],["map_source","validation.preset.map_source.missing"],["calibration_source","validation.preset.calibration_source.missing"]]),c=Object.keys(e);var d,p;l.forEach(((e,t)=>{c.includes(t)||s.push(e)})),e.map_source&&(d=e.map_source,d.camera||d.image?d.camera&&d.image?["validation.preset.map_source.ambiguous"]:[]:["validation.preset.map_source.none_provided"]).forEach((e=>s.push(e))),e.calibration_source&&(p=e.calibration_source,Object.keys(p).filter((e=>"attribute"!=e)).length>1?["validation.preset.calibration_source.ambiguous"]:p.calibration_points?[3,4].includes(p.calibration_points.length)?p.calibration_points.flatMap((e=>function(e){const t=[];return(null==e?void 0:e.map)||t.push("validation.preset.calibration_source.calibration_points.missing_map"),(null==e?void 0:e.vacuum)||t.push("validation.preset.calibration_source.calibration_points.missing_vacuum"),[null==e?void 0:e.map,null==e?void 0:e.vacuum].filter((e=>!e.x||!e.y)).length>0&&t.push("validation.preset.calibration_source.calibration_points.missing_coordinate"),t}(e))):["validation.preset.calibration_source.calibration_points.invalid_number"]:[]).forEach((e=>s.push(e))),e.vacuum_platform&&!ga.getPlatforms().includes(e.vacuum_platform)&&s.push(["validation.preset.platform.invalid","{0}",e.vacuum_platform]);const u=null!==(i=e.vacuum_platform)&&void 0!==i?i:"default";return(null!==(n=e.icons)&&void 0!==n?n:[]).flatMap((e=>function(e){if(!e)return["validation.preset.icons.invalid"];const t=[];return e.icon||t.push("validation.preset.icons.icon.missing"),t}(e))).forEach((e=>s.push(e))),(null!==(r=e.tiles)&&void 0!==r?r:[]).flatMap((e=>function(e){if(!e)return["validation.preset.tiles.invalid"];const t=[];return e.entity||t.push("validation.preset.tiles.entity.missing"),e.label||t.push("validation.preset.tiles.label.missing"),t}(e))).forEach((e=>s.push(e))),(null!==(o=e.map_modes)&&void 0!==o?o:[]).flatMap((e=>si(u,e,a))).forEach((e=>s.push(e))),!e.preset_name&&t&&s.push("validation.preset.preset_name.missing"),s}class ci{static generate(e,t,a,i){if(!e)return new Promise((e=>e([])));const n=ga.usesSensors(e,a),r=e.states[t],o=[];return o.push(...this.getCommonTiles(r,t,i)),n?this.addTilesFromSensors(e,t,a,o,i):new Promise((e=>e(this.addTilesFromAttributes(r,t,a,o,i))))}static getCommonTiles(e,t,a){const i=[];return"status"in e.attributes&&i.push({entity:t,label:Gt("label.status",a),attribute:"status",icon:"mdi:robot-vacuum"}),"battery_level"in e.attributes&&"battery_icon"in e.attributes&&i.push({entity:t,label:Gt("label.battery_level",a),attribute:"battery_level",icon:e.attributes.battery_icon,unit:"%"}),"battery_level"in e.attributes&&!("battery_icon"in e.attributes)&&i.push({entity:t,label:Gt("label.battery_level",a),attribute:"battery_level",icon:"mdi:battery",unit:"%"}),"fan_speed"in e.attributes&&i.push({entity:t,label:Gt("label.fan_speed",a),attribute:"fan_speed",icon:"mdi:fan"}),i}static addTilesFromAttributes(e,t,a,i,n){return ga.getTilesFromAttributesTemplates(a).filter((t=>t.attribute in e.attributes)).forEach((e=>i.push({entity:t,label:Gt(e.label,n),attribute:e.attribute,icon:e.icon,unit:e.unit?Gt(e.unit,n):void 0,precision:e.precision,multiplier:e.multiplier}))),i}static async addTilesFromSensors(e,t,a,i,n){const r=(await async function(e,t){const a=(await e.callWS({type:"entity/source",entity_id:[t]}))[t].config_entry,i=(await e.callWS({type:"config/entity_registry/list"})).filter((e=>e.config_entry_id===a));return Promise.all(i.map((t=>e.callWS({type:"config/entity_registry/get",entity_id:t.entity_id}))))}(e,t)).filter((e=>null===e.disabled_by)),o=r.filter((e=>e.entity_id===t))[0].unique_id;return ga.getTilesFromSensorsTemplates(a).map((e=>({tile:e,entity:r.filter((t=>t.unique_id===`${e.unique_id_prefix}${o}`))}))).flatMap((e=>e.entity.map((t=>this.mapToTile(t,e.tile.label,e.tile.unit,e.tile.multiplier,n))))).forEach((e=>i.push(e))),new Promise((e=>e(i)))}static mapToTile(e,t,a,i,n){var r;return{entity:e.entity_id,label:Gt(t,n),icon:null!==(r=e.icon)&&void 0!==r?r:e.original_icon,multiplier:i||void 0,precision:i?1:void 0,unit:a?Gt(a,n):void 0}}}class di{static generate(e,t,a){if(!e)return[];const i=e.states[t],n=[];n.push({icon:"mdi:play",conditions:[{entity:t,value_not:"cleaning"},{entity:t,value_not:"error"},{entity:t,value_not:"returning"}],tooltip:Gt("icon.vacuum_start",a),tap_action:{action:"call-service",service:"vacuum.start",service_data:{entity_id:t}}}),n.push({icon:"mdi:pause",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"idle"},{entity:t,value_not:"error"},{entity:t,value_not:"paused"}],tooltip:Gt("icon.vacuum_pause",a),tap_action:{action:"call-service",service:"vacuum.pause",service_data:{entity_id:t}}}),n.push({icon:"mdi:stop",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"idle"},{entity:t,value_not:"error"},{entity:t,value_not:"paused"}],tooltip:Gt("icon.vacuum_stop",a),tap_action:{action:"call-service",service:"vacuum.stop",service_data:{entity_id:t}}}),n.push({icon:"mdi:home-map-marker",conditions:[{entity:t,value_not:"docked"}],tooltip:Gt("icon.vacuum_return_to_base",a),tap_action:{action:"call-service",service:"vacuum.return_to_base",service_data:{entity_id:t}}}),n.push({icon:"mdi:target-variant",conditions:[{entity:t,value_not:"docked"},{entity:t,value_not:"error"},{entity:t,value_not:"cleaning"}],tooltip:Gt("icon.vacuum_clean_spot",a),tap_action:{action:"call-service",service:"vacuum.clean_spot",service_data:{entity_id:t}}}),n.push({icon:"mdi:map-marker",tooltip:Gt("icon.vacuum_locate",a),tap_action:{action:"call-service",service:"vacuum.locate",service_data:{entity_id:t}}});const r="fan_speed_list"in i.attributes?i.attributes.fan_speed_list:[];for(let e=0;e<r.length;e++){const i=r[e],o=r[(e+1)%r.length];n.push({icon:i in this._ICON_MAPPING?this._ICON_MAPPING[i]:"mdi:fan-alert",conditions:[{entity:t,attribute:"fan_speed",value:i}],tooltip:Gt("icon.vacuum_set_fan_speed",a),tap_action:{action:"call-service",service:"vacuum.set_fan_speed",service_data:{entity_id:t,fan_speed:o}}})}return n}}di._ICON_MAPPING={Silent:"mdi:fan-remove",Standard:"mdi:fan-speed-1",Medium:"mdi:fan-speed-2",Turbo:"mdi:fan-speed-3",Auto:"mdi:fan-auto",Gentle:"mdi:waves"};class pi{static render(e,t){var a,i,n;let r=e.attribute?t.hass.states[e.entity].attributes[e.attribute]:t.hass.states[e.entity].state;return"number"!=typeof r&&isNaN(+r)||(r=parseFloat(r.toString())*(null!==(a=e.multiplier)&&void 0!==a?a:1),null!=e.precision&&(r=r.toFixed(e.precision))),I`
            <div
                class="tile-wrapper clickable ripple"
                .title=${null!==(i=e.tooltip)&&void 0!==i?i:""}
                @action=${ja(t,e)}
                .actionHandler=${wa({hasHold:Me(null==e?void 0:e.hold_action),hasDoubleClick:Me(null==e?void 0:e.double_tap_action)})}>
                <div class="tile-title">${e.label}</div>
                <div class="tile-value-wrapper">
                    ${Ia(!!e.icon,(()=>I` <div class="tile-icon">
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
        `}}class ui{static render(e,t){var a;return I`
            <paper-button
                class="vacuum-actions-item clickable ripple"
                .title=${null!==(a=e.tooltip)&&void 0!==a?a:""}
                @action=${ja(t,e)}
                .actionHandler=${wa({hasHold:Me(null==e?void 0:e.hold_action),hasDoubleClick:Me(null==e?void 0:e.double_tap_action)})}>
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
        `}}class mi{static render(){return I`
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
        `}}class hi{static render(e,t,a){const i=()=>e[t];return I`
            <paper-menu-button
                class="modes-dropdown-menu"
                vertical-align="bottom"
                horizontal-align="left"
                no-animations="true"
                close-on-activate="true">
                <div class="modes-dropdown-menu-button" slot="dropdown-trigger" alt="bottom align">
                    <paper-button class="modes-dropdown-menu-button-button">
                        <ha-icon icon="${i().icon}" class="dropdown-icon"></ha-icon>
                    </paper-button>
                    <div class="modes-dropdown-menu-button-text">${i().name}</div>
                </div>
                <paper-listbox
                    class="modes-dropdown-menu-listbox"
                    slot="dropdown-content"
                    selected="${t}"
                    @iron-select="${e=>{a(parseInt(e.detail.item.attributes["mode-id"].value))}}">
                    ${e.map(((a,i)=>I` <div mode-id="${i}">
                            <div class="modes-dropdown-menu-entry ${t===i?"selected":""}">
                                <div
                                    class="modes-dropdown-menu-entry-button-wrapper ${0===i?"first":""} ${i===e.length-1?"last":""} ${t===i?"selected":""}">
                                    <paper-button
                                        class="modes-dropdown-menu-entry-button ${t===i?"selected":""}">
                                        <ha-icon icon="${a.icon}"></ha-icon>
                                    </paper-button>
                                </div>
                                <div class="modes-dropdown-menu-entry-text">${a.name}</div>
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
        `}}function vi(e,t){return Array.isArray(t)?[e.a*t[0]+e.c*t[1]+e.e,e.b*t[0]+e.d*t[1]+e.f]:{x:e.a*t.x+e.c*t.y+e.e,y:e.b*t.x+e.d*t.y+e.f}}function _i(...e){const t=(e,t)=>({a:e.a*t.a+e.c*t.b,c:e.a*t.c+e.c*t.d,e:e.a*t.e+e.c*t.f+e.e,b:e.b*t.a+e.d*t.b,d:e.b*t.c+e.d*t.d,f:e.b*t.e+e.d*t.f+e.f});switch((e=Array.isArray(e[0])?e[0]:e).length){case 0:throw new Error("no matrices provided");case 1:return e[0];case 2:return t(e[0],e[1]);default:{const[a,i,...n]=e;return _i(t(a,i),...n)}}}function gi(e,t){const a=null!=e[0].x?e[0].x:e[0][0],i=null!=e[0].y?e[0].y:e[0][1],n=null!=t[0].x?t[0].x:t[0][0],r=null!=t[0].y?t[0].y:t[0][1],o=null!=e[1].x?e[1].x:e[1][0],s=null!=e[1].y?e[1].y:e[1][1],l=null!=t[1].x?t[1].x:t[1][0],c=null!=t[1].y?t[1].y:t[1][1],d=null!=e[2].x?e[2].x:e[2][0],p=null!=e[2].y?e[2].y:e[2][1],u=null!=t[2].x?t[2].x:t[2][0],m=null!=t[2].y?t[2].y:t[2][1],h={a:n-u,b:r-m,c:l-u,d:c-m,e:u,f:m},v=function(e){const{a:t,b:a,c:i,d:n,e:r,f:o}=e,s=t*n-a*i;return{a:n/s,b:a/-s,c:i/-s,d:t/s,e:(n*r-i*o)/-s,f:(a*r-t*o)/s}}({a:a-d,b:i-p,c:o-d,d:s-p,e:d,f:p});return function(e,t=1e10){return{a:Math.round(e.a*t)/t,b:Math.round(e.b*t)/t,c:Math.round(e.c*t)/t,d:Math.round(e.d*t)/t,e:Math.round(e.e*t)/t,f:Math.round(e.f*t)/t}}(_i([h,v]))}function fi(e,t,a,i){this.message=e,this.expected=t,this.found=a,this.location=i,this.name="SyntaxError","function"==typeof Error.captureStackTrace&&Error.captureStackTrace(this,fi)}!function(e,t){function a(){this.constructor=e}a.prototype=t.prototype,e.prototype=new a}(fi,Error),fi.buildMessage=function(e,t,a){var i={literal:function(e){return'"'+r(e.text)+'"'},class:function(e){var t=e.parts.map((function(e){return Array.isArray(e)?o(e[0])+"-"+o(e[1]):o(e)}));return"["+(e.inverted?"^":"")+t+"]"},any:function(){return"any character"},end:function(){return"end of input"},other:function(e){return e.description},not:function(e){return"not "+s(e.expected)}};function n(e){return e.charCodeAt(0).toString(16).toUpperCase()}function r(e){return e.replace(/\\/g,"\\\\").replace(/"/g,'\\"').replace(/\0/g,"\\0").replace(/\t/g,"\\t").replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/[\x00-\x0F]/g,(function(e){return"\\x0"+n(e)})).replace(/[\x10-\x1F\x7F-\x9F]/g,(function(e){return"\\x"+n(e)}))}function o(e){return e.replace(/\\/g,"\\\\").replace(/\]/g,"\\]").replace(/\^/g,"\\^").replace(/-/g,"\\-").replace(/\0/g,"\\0").replace(/\t/g,"\\t").replace(/\n/g,"\\n").replace(/\r/g,"\\r").replace(/[\x00-\x0F]/g,(function(e){return"\\x0"+n(e)})).replace(/[\x10-\x1F\x7F-\x9F]/g,(function(e){return"\\x"+n(e)}))}function s(e){return i[e.type](e)}return"Expected "+function(e){var t,a,i=e.map(s);if(i.sort(),i.length>0){for(t=1,a=1;t<i.length;t++)i[t-1]!==i[t]&&(i[a]=i[t],a++);i.length=a}switch(i.length){case 1:return i[0];case 2:return i[0]+" or "+i[1];default:return i.slice(0,-1).join(", ")+", or "+i[i.length-1]}}(e)+" but "+function(e){return e?'"'+r(e)+'"':"end of input"}(t)+" found."};var bi,yi,xi,wi=(bi=function(e,t){function a(e){var t;return"object"==typeof e?"object"==typeof(t=e[0])?[e.length,t.length]:[e.length]:[]}function i(e,t,a,n){if(a===t.length-1)return n(e);var r,o=t[a],s=Array(o);for(r=o-1;r>=0;r--)s[r]=i(e[r],t,a+1,n);return s}function n(e){var t,a=e.length,i=Array(a);for(t=a-1;-1!==t;--t)i[t]=e[t];return i}function r(e){if("object"!=typeof e)return e;var t=n;return i(e,a(e),0,t)}function o(e,t,a){void 0===a&&(a=0);var i,n=e[a],r=Array(n);if(a===e.length-1){for(i=n-2;i>=0;i-=2)r[i+1]=t,r[i]=t;return-1===i&&(r[0]=t),r}for(i=n-1;i>=0;i--)r[i]=o(e,t,a+1);return r}function s(e){return function(e){var t,a,i,n,r=e.length,o=Array(r);for(t=r-1;t>=0;t--){for(n=Array(r),a=t+2,i=r-1;i>=a;i-=2)n[i]=0,n[i-1]=0;for(i>t&&(n[i]=0),n[t]=e[t],i=t-1;i>=1;i-=2)n[i]=0,n[i-1]=0;0===i&&(n[0]=0),o[t]=n}return o}(o([e],1))}function l(e,t){var a,i,n,r,o,s,l,c,d,p,u;for(r=e.length,o=t.length,s=t[0].length,l=Array(r),a=r-1;a>=0;a--){for(c=Array(s),d=e[a],n=s-1;n>=0;n--){for(p=d[o-1]*t[o-1][n],i=o-2;i>=1;i-=2)u=i-1,p+=d[i]*t[i][n]+d[u]*t[u][n];0===i&&(p+=d[0]*t[0][n]),c[n]=p}l[a]=c}return l}function c(e,t){var a,i,n=e.length,r=e[n-1]*t[n-1];for(a=n-2;a>=1;a-=2)i=a-1,r+=e[a]*t[a]+e[i]*t[i];return 0===a&&(r+=e[0]*t[0]),r}function d(e){var t,a,i,n,r,o=e.length,s=e[0].length,l=Array(s);for(a=0;a<s;a++)l[a]=Array(o);for(t=o-1;t>=1;t-=2){for(n=e[t],i=e[t-1],a=s-1;a>=1;--a)(r=l[a])[t]=n[a],r[t-1]=i[a],(r=l[--a])[t]=n[a],r[t-1]=i[a];0===a&&((r=l[0])[t]=n[0],r[t-1]=i[0])}if(0===t){for(i=e[0],a=s-1;a>=1;--a)l[a][0]=i[a],l[--a][0]=i[a];0===a&&(l[0][0]=i[0])}return l}function p(e,t,i){if(i){var n=t;t=e,e=n}var o,p=[[e[0],e[1],1,0,0,0,-1*t[0]*e[0],-1*t[0]*e[1]],[0,0,0,e[0],e[1],1,-1*t[1]*e[0],-1*t[1]*e[1]],[e[2],e[3],1,0,0,0,-1*t[2]*e[2],-1*t[2]*e[3]],[0,0,0,e[2],e[3],1,-1*t[3]*e[2],-1*t[3]*e[3]],[e[4],e[5],1,0,0,0,-1*t[4]*e[4],-1*t[4]*e[5]],[0,0,0,e[4],e[5],1,-1*t[5]*e[4],-1*t[5]*e[5]],[e[6],e[7],1,0,0,0,-1*t[6]*e[6],-1*t[6]*e[7]],[0,0,0,e[6],e[7],1,-1*t[7]*e[6],-1*t[7]*e[7]]],u=t;try{o=function(e){var t,i,n,o,l,c,d,p,u=a(e),m=Math.abs,h=u[0],v=u[1],_=r(e),g=s(h);for(c=0;c<v;++c){var f=-1,b=-1;for(l=c;l!==h;++l)(d=m(_[l][c]))>b&&(f=l,b=d);for(i=_[f],_[f]=_[c],_[c]=i,o=g[f],g[f]=g[c],g[c]=o,p=i[c],d=c;d!==v;++d)i[d]/=p;for(d=v-1;-1!==d;--d)o[d]/=p;for(l=h-1;-1!==l;--l)if(l!==c){for(t=_[l],n=g[l],p=t[c],d=c+1;d!==v;++d)t[d]-=i[d]*p;for(d=v-1;d>0;--d)n[d]-=o[d]*p,n[--d]-=o[d]*p;0===d&&(n[0]-=o[0]*p)}}return g}(l(d(p),p))}catch(e){return[1,0,0,0,1,0,0,0]}for(var m,h=function(e,t){var a,i=e.length,n=Array(i);for(a=i-1;a>=0;a--)n[a]=c(e[a],t);return n}(l(o,d(p)),u),v=0;v<h.length;v++)h[v]=(m=h[v],Math.round(1e10*m)/1e10);return h[8]=1,h}Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t){var a=p(e,t,!1);return function(e,t){return function(e,t,a){var i=[];return i[0]=(e[0]*t+e[1]*a+e[2])/(e[6]*t+e[7]*a+1),i[1]=(e[3]*t+e[4]*a+e[5])/(e[6]*t+e[7]*a+1),i}(a,e,t)}}},bi(yi={exports:{}},yi.exports),yi.exports),Ei=function(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}(wi);!function(e){e[e.AFFINE=0]="AFFINE",e[e.PERSPECTIVE=1]="PERSPECTIVE"}(xi||(xi={}));class ki{constructor(e){const t=null==e?void 0:e.map((e=>e.map)),a=null==e?void 0:e.map((e=>e.vacuum));if(t&&a)if(3===t.length)this.transformMode=xi.AFFINE,this.mapToVacuumMatrix=gi(t,a),this.vacuumToMapMatrix=gi(a,t),this.calibrated=!(!this.mapToVacuumMatrix||!this.vacuumToMapMatrix);else{this.transformMode=xi.PERSPECTIVE;const e=t.flatMap((e=>[e.x,e.y])),i=a.flatMap((e=>[e.x,e.y]));this.mapToVacuumTransformer=Ei(e,i),this.vacuumToMapTransformer=Ei(i,e),this.calibrated=!0}else this.calibrated=!1}mapToVacuum(e,t){if(this.transformMode===xi.AFFINE&&this.mapToVacuumMatrix)return vi(this.mapToVacuumMatrix,[e,t]);if(this.transformMode===xi.PERSPECTIVE&&this.mapToVacuumTransformer)return this.mapToVacuumTransformer(e,t);throw Error("Missing calibration")}vacuumToMap(e,t){if(this.transformMode===xi.AFFINE&&this.vacuumToMapMatrix)return vi(this.vacuumToMapMatrix,[e,t]);if(this.transformMode===xi.PERSPECTIVE&&this.vacuumToMapTransformer)return this.vacuumToMapTransformer(e,t);throw Error("Missing calibration")}}console.info(`%c  XIAOMI-VACUUM-MAP-CARD \n%c  ${Gt("common.version")} v2.0.2    `,"color: orange; font-weight: bold; background: black","color: white; font-weight: bold; background: dimgray");const zi=window;zi.customCards=zi.customCards||[],zi.customCards.push({type:"xiaomi-vacuum-map-card",name:"Xiaomi Vacuum Map Card",description:Gt("common.description"),preview:!0});let Pi=class extends ne{constructor(){super(...arguments),this.oldConfig=!1,this.watchedEntities=[],this.repeats=1,this.selectedMode=0,this.mapLocked=!1,this.configErrors=[],this.selectedManualRectangles=[],this.selectedManualPath=new ti([],this._getContext()),this.selectedPredefinedRectangles=[],this.selectedRooms=[],this.selectedPredefinedPoint=[],this.selectablePredefinedRectangles=[],this.selectableRooms=[],this.selectablePredefinedPoints=[],this.modes=[]}static async getConfigElement(){return document.createElement("xiaomi-vacuum-map-card-editor")}static getStubConfig(e){const t=Object.keys(e.states),a=t.filter((e=>"camera"===e.substr(0,e.indexOf(".")))).filter((t=>null==e?void 0:e.states[t].attributes.calibration_points)),i=t.filter((e=>"vacuum"===e.substr(0,e.indexOf("."))));if(0!==a.length&&0!==i.length)return{type:"custom:xiaomi-vacuum-map-card",map_source:{camera:a[0]},calibration_source:{camera:!0},entity:i[0],vacuum_platform:"default"}}set hass(e){const t=!this._hass&&e;this._hass=e,t&&this._firstHass()}get hass(){return this._hass}setConfig(e){if(!e)throw new Error(this._localize("common.invalid_configuration"));this.config=e,function(e){return e.map_image||e.map_camera}(e)?this.oldConfig=!0:(this.configErrors=function(e){var t,a,i;const n=[],r=(null!==(a=null===(t=e.additional_presets)||void 0===t?void 0:t.length)&&void 0!==a?a:0)>0;return li(e,r,e.language).forEach((e=>n.push(e))),null===(i=e.additional_presets)||void 0===i||i.flatMap((t=>li(t,r,e.language))).forEach((e=>n.push(e))),n.map((t=>Gt(t,e.language)))}(this.config),this.configErrors.length>0||(this.watchedEntities=function(e){var t;const a=new Set;return[e,...null!==(t=e.additional_presets)&&void 0!==t?t:[]].flatMap((t=>[...La(t,e.language)])).forEach((e=>a.add(e))),[...a]}(this.config),this._setPresetIndex(0,!1,!0),this.requestUpdate("config")))}_getCurrentPreset(){return this.currentPreset}_getCalibration(e){var t,a,i,n,r,o,s;return e.calibration_source.calibration_points&&[3,4].includes(e.calibration_source.calibration_points.length)?e.calibration_source.calibration_points:this.hass?e.calibration_source.entity&&!(null===(t=e.calibration_source)||void 0===t?void 0:t.attribute)?JSON.parse(null===(a=this.hass.states[e.calibration_source.entity])||void 0===a?void 0:a.state):e.calibration_source.entity&&(null===(i=e.calibration_source)||void 0===i?void 0:i.attribute)?null===(n=this.hass.states[e.calibration_source.entity])||void 0===n?void 0:n.attributes[e.calibration_source.attribute]:e.calibration_source.camera?null===(s=this.hass.states[null!==(o=null===(r=e.map_source)||void 0===r?void 0:r.camera)&&void 0!==o?o:""])||void 0===s?void 0:s.attributes.calibration_points:void 0:void 0}_firstHass(){0!==this.configErrors.length||this.oldConfig||this._setPresetIndex(this.presetIndex,!1,!0)}_setPresetIndex(e,t=!1,a=!1){var i,n,r,o,s,l,c,d,p,u,m,h,v,_;if((e=Math.min(Math.max(e,0),null!==(n=null===(i=this.config.additional_presets)||void 0===i?void 0:i.length)&&void 0!==n?n:0))===this.presetIndex&&!a)return;const g=0===e?this.config:(null!==(r=this.config.additional_presets)&&void 0!==r?r:[])[e-1];this.mapLocked||null===(o=this._getPinchZoom())||void 0===o||o.setTransform({scale:1,x:0,y:0,allowChangeEvent:!0}),t&&ze("selection"),this.mapLocked=null!==(s=null==g?void 0:g.map_locked)&&void 0!==s&&s,this.selectedMode=0,this.mapScale=1,this.mapX=0,this.mapY=0,this.hass&&this._updateCalibration(g);const f=null!==(l=g.vacuum_platform)&&void 0!==l?l:"default";this.modes=(0===(null!==(d=null===(c=g.map_modes)||void 0===c?void 0:c.length)&&void 0!==d?d:0)?ga.generateDefaultModes(f):null!==(p=g.map_modes)&&void 0!==p?p:[]).map((e=>new $a(f,e,this.config.language))),this.presetIndex=e,this.currentPreset=g,this._setCurrentMode(0);const b=-1===(null!==(m=null===(u=g.icons)||void 0===u?void 0:u.length)&&void 0!==m?m:-1)?di.generate(this.hass,g.entity,this.config.language):g.append_icons?[...di.generate(this.hass,g.entity,this.config.language),...null!==(h=g.icons)&&void 0!==h?h:[]]:g.icons,y=-1===(null!==(_=null===(v=g.tiles)||void 0===v?void 0:v.length)&&void 0!==_?_:-1)?ci.generate(this.hass,g.entity,f,this.config.language):g.append_tiles?ci.generate(this.hass,g.entity,f,this.config.language).then((e=>{var t;return[...e,...null!==(t=g.tiles)&&void 0!==t?t:[]]})):new Promise((e=>{var t;return e(null!==(t=g.tiles)&&void 0!==t?t:[])}));y.then((e=>this._setPreset(Object.assign(Object.assign({},g),{tiles:e,icons:b})))).then((()=>this.requestUpdate()))}_setPreset(e){this.currentPreset=e}_updateCalibration(e){this.coordinatesConverter=void 0;const t=this._getCalibration(e);this.coordinatesConverter=new ki(t)}_getMapSrc(e){if(e.map_source.camera)return`${this.hass.states[e.map_source.camera].attributes.entity_picture}&v=${+new Date}`;if(e.map_source.image)return`${e.map_source.image}`;throw new Error("No map SRC!")}shouldUpdate(e){return!!this.config&&function(e,t,a,i){if(t.has("config")||a)return!0;const n=t.get("hass");return!n||e.some((e=>n.states[e]!==(null==i?void 0:i.states[e])))}(this.watchedEntities,e,!1,this.hass)}render(){var e,t,a,i;if(this.oldConfig)return this._showOldConfig();if(this.configErrors.length>0)return this._showConfigErrors(this.configErrors);const n=function(e,t){const a=Object.keys(t.states);return e.filter((e=>!a.includes(e)))}(this.watchedEntities,this.hass);if(n.length>0)return this._showInvalidEntities(n);const r=this._getCurrentPreset();this._updateCalibration(r);const o=r.tiles,s=r.icons,l=this.modes,c=this._getMapSrc(r),d=!!this.coordinatesConverter&&this.coordinatesConverter.calibrated,p=d?this._createMapControls():[],u=Ia(d,(()=>{var e,t,a,i,n,o,s,l;return I`
                <div
                    id="map-zoomer-content"
                    style="
                 margin-top: ${-1*(null!==(t=null===(e=r.map_source.crop)||void 0===e?void 0:e.top)&&void 0!==t?t:0)}px;
                 margin-bottom: ${-1*(null!==(i=null===(a=r.map_source.crop)||void 0===a?void 0:a.bottom)&&void 0!==i?i:0)}px;
                 margin-left: ${-1*(null!==(o=null===(n=r.map_source.crop)||void 0===n?void 0:n.left)&&void 0!==o?o:0)}px;
                 margin-right: ${-1*(null!==(l=null===(s=r.map_source.crop)||void 0===s?void 0:s.right)&&void 0!==l?l:0)}px;">
                    <img
                        id="map-image"
                        alt="camera_image"
                        class="${this.mapScale*this.realScale>1?"zoomed":""}"
                        src="${c}" />
                    <div id="map-image-overlay">
                        <svg
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
            `}));return I`
            <ha-card
                .header="${this.config.title}"
                tabindex="0"
                style="--map-scale: ${this.mapScale}; --real-scale: ${this.realScale};">
                ${Ia((null!==(t=null===(e=this.config.additional_presets)||void 0===e?void 0:e.length)&&void 0!==t?t:0)>0,(()=>{var e,t,a;return I`
                        <div class="preset-selector-wrapper">
                            <ha-icon
                                icon="mdi:chevron-left"
                                class="preset-selector-icon ${0===this.presetIndex?"disabled":""}"
                                @click="${()=>this._setPresetIndex(this.presetIndex-1,!0)}"></ha-icon>
                            <div class="preset-label-wrapper">
                                <div class="preset-label">${r.preset_name}</div>
                                <div class="preset-indicator">
                                    ${new Array((null!==(t=null===(e=this.config.additional_presets)||void 0===e?void 0:e.length)&&void 0!==t?t:0)+1).fill(0).map(((e,t)=>t===this.presetIndex?"●":"○"))}
                                </div>
                            </div>
                            <ha-icon
                                icon="mdi:chevron-right"
                                class="preset-selector-icon ${this.presetIndex===(null===(a=this.config.additional_presets)||void 0===a?void 0:a.length)?"disabled":""}"
                                @click="${()=>this._setPresetIndex(this.presetIndex+1,!0)}"></ha-icon>
                        </div>
                    `}))}
                ${d?I`
                          <div id="map-wrapper" style="position: relative;">
                              ${this.mapLocked?I`
                                        <div min-scale="0.5" id="map-zoomer" @change="${this._calculateScale}">
                                            ${u}
                                        </div>
                                    `:r.two_finger_pan?I`
                                        <pinch-zoom
                                            min-scale="0.5"
                                            id="map-zoomer"
                                            @change="${this._calculateScale}"
                                            two-finger-pan="true"
                                            style="touch-action: none;">
                                            ${u}
                                        </pinch-zoom>
                                    `:I`
                                        <pinch-zoom
                                            min-scale="0.5"
                                            id="map-zoomer"
                                            @change="${this._calculateScale}"
                                            style="touch-action: none;">
                                            ${u}
                                        </pinch-zoom>
                                    `}

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
                    ${Ia(d&&(l.length>1||p.length>0),(()=>I`
                            <div>
                                <div class="map-controls">
                                    ${Ia(l.length>1,(()=>hi.render(l,this.selectedMode,(e=>this._setCurrentMode(e)))))}
                                    ${Ia(p.length>0,(()=>I` <div class="map-actions-list">${p}</div> `))}
                                </div>
                            </div>
                        `))}
                    ${Ia(0!==(null!==(a=null==s?void 0:s.length)&&void 0!==a?a:0),(()=>I`
                            <div class="vacuum-controls">
                                <div class="vacuum-actions-list">
                                    ${null==s?void 0:s.filter((e=>Oa(e,this.hass))).map((e=>ui.render(e,this)))}
                                </div>
                            </div>
                        `))}
                    ${Ia(0!==(null!==(i=null==o?void 0:o.length)&&void 0!==i?i:0),(()=>I`
                            <div class="tiles-wrapper">
                                ${null==o?void 0:o.filter((e=>Oa(e,this.hass))).map((e=>pi.render(e,this)))}
                            </div>
                        `))}
                </div>
                ${mi.render()}
            </ha-card>
        `}_createMapControls(){const e=[],t=this._getCurrentMode();return t.selectionType===Ma.MANUAL_RECTANGLE&&e.push(I`
                <paper-button class="map-actions-item clickable ripple" @click="${()=>this._addRectangle()}">
                    <ha-icon icon="mdi:plus"></ha-icon>
                </paper-button>
            `),t.selectionType===Ma.MANUAL_PATH&&e.push(I`
                <paper-button
                    class="map-actions-item clickable ripple"
                    @click="${()=>{this.selectedManualPath.removeLast(),ze("selection"),this.requestUpdate()}}">
                    <ha-icon icon="mdi:undo-variant"></ha-icon>
                </paper-button>
                <paper-button
                    class="map-actions-item clickable ripple"
                    @click="${()=>{this.selectedManualPath.clear(),ze("selection"),this.requestUpdate()}}">
                    <ha-icon icon="mdi:delete-empty"></ha-icon>
                </paper-button>
            `),t.repeatsType!==Sa.NONE&&e.push(I`
                <paper-button
                    class="map-actions-item clickable ripple"
                    @click="${()=>{this.repeats=this.repeats%t.maxRepeats+1,ze("selection")}}">
                    <div>×${this.repeats}</div>
                </paper-button>
            `),t.runImmediately||e.push(I`
                <paper-button
                    class="map-actions-item main clickable ripple"
                    @action="${this._handleRunAction()}"
                    .actionHandler="${wa({hasHold:!0,hasDoubleClick:!0})}">
                    <ha-icon icon="mdi:play"></ha-icon>
                    <ha-icon
                        icon="${t.icon}"
                        style="position: absolute; transform: scale(0.5) translate(15px, -20px)"></ha-icon>
                </paper-button>
            `),e}_getContext(){return new Ka((()=>this.mapScale),(()=>this.realScale),(e=>Da(e,this._getSvgWrapper())),(()=>this.requestUpdate()),(()=>this.coordinatesConverter),(()=>this.selectedManualRectangles),(()=>this.selectedPredefinedRectangles),(()=>this.selectedRooms),(()=>this.selectedPredefinedPoint),(()=>this._getCurrentMode().coordinatesRounding),(()=>this._getCurrentMode().maxSelections),(e=>this._getCssProperty(e)),(()=>this._runImmediately()),(e=>this._localize(e)))}_setCurrentMode(e){const t=this.modes[e];switch(this.selectedManualRectangles=[],this.selectedManualPoint=void 0,this.selectedManualPath.clear(),this.selectedPredefinedRectangles=[],this.selectedRooms=[],this.selectedPredefinedPoint=[],this.selectablePredefinedRectangles=[],this.selectableRooms=[],this.selectablePredefinedPoints=[],t.selectionType){case Ma.PREDEFINED_RECTANGLE:const e=ii.getFromEntities(t,this.hass,(()=>this._getContext())),a=t.predefinedSelections.map((e=>e)).filter((e=>"string"!=typeof e.zones)).map((e=>new ii(e,this._getContext())));this.selectablePredefinedRectangles=e.concat(a);break;case Ma.ROOM:this.selectableRooms=t.predefinedSelections.map((e=>new ni(e,this._getContext())));break;case Ma.PREDEFINED_POINT:const i=ai.getFromEntities(t,this.hass,(()=>this._getContext())),n=t.predefinedSelections.map((e=>e)).filter((e=>"string"!=typeof e.position)).map((e=>new ai(e,this._getContext())));this.selectablePredefinedPoints=i.concat(n)}this.selectedMode!=e&&ze("selection"),this.selectedMode=e}_getCurrentMode(){return this.modes[this.selectedMode]}_getSelection(e){var t,a;const i=e.repeatsType===Sa.INTERNAL?this.repeats:null;switch(e.selectionType){case Ma.MANUAL_RECTANGLE:return this.selectedManualRectangles.map((e=>e.toVacuum(i)));case Ma.PREDEFINED_RECTANGLE:return this.selectedPredefinedRectangles.map((e=>e.toVacuum(i))).reduce(((e,t)=>e.concat(t)),[]);case Ma.ROOM:const e=this.selectedRooms.map((e=>e.toVacuum()));return[...e,...i&&e.length>0?[i]:[]];case Ma.MANUAL_PATH:return this.selectedManualPath.toVacuum(i);case Ma.MANUAL_POINT:return null!==(a=null===(t=this.selectedManualPoint)||void 0===t?void 0:t.toVacuum(i))&&void 0!==a?a:[];case Ma.PREDEFINED_POINT:return this.selectedPredefinedPoint.map((e=>e.toVacuum(i))).reduce(((e,t)=>e.concat(t)),[])}}_runImmediately(){return!!this._getCurrentMode().runImmediately&&(this._run(!1),!0)}_run(e){const t=this._getCurrentPreset(),a=this._getCurrentMode(),i=this._getSelection(a);if(0==i.length)this._showToast("popups.no_selection","mdi:close",!1),ze("failure");else{const n=this.repeats,r=a.getServiceCall(t.entity,i,n),o=JSON.stringify(r,null,2);e?(this._showToast("popups.success","mdi:check",!0),console.log(o),window.alert(o),ze("success")):this.hass.callService(r.domain,r.service,r.serviceData).then((()=>{this._showToast("popups.success","mdi:check",!0),ze("success")}),(e=>{this._showToast("popups.failed","mdi:close",!1,e.message),ze("failure")}))}}updated(e){this._updateElements()}connectedCallback(){super.connectedCallback(),this._updateElements(),this._delay(100).then((()=>this.requestUpdate()))}_updateElements(){var e,t,a;const i=null===(a=null===(t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector(".modes-dropdown-menu"))||void 0===t?void 0:t.shadowRoot)||void 0===a?void 0:a.querySelector(".dropdown-content");i&&(i.style.borderRadius=this._getCssProperty("--map-card-internal-big-radius")),this._calculateBasicScale()}_drawSelection(){var e,t;switch(this._getCurrentMode().selectionType){case Ma.MANUAL_RECTANGLE:return j`${this.selectedManualRectangles.map((e=>e.render()))}`;case Ma.PREDEFINED_RECTANGLE:return j`${this.selectablePredefinedRectangles.map((e=>e.render()))}`;case Ma.ROOM:return j`${this.selectableRooms.map((e=>e.render()))}`;case Ma.MANUAL_PATH:return j`${null===(e=this.selectedManualPath)||void 0===e?void 0:e.render()}`;case Ma.MANUAL_POINT:return j`${null===(t=this.selectedManualPoint)||void 0===t?void 0:t.render()}`;case Ma.PREDEFINED_POINT:return j`${this.selectablePredefinedPoints.map((e=>e.render()))}`}}_toggleLock(){this.mapY=0,this.mapX=0,this.mapScale=1,this.mapLocked=!this.mapLocked,ze("selection")}_addRectangle(){var e,t,a,i,n,r,o,s;const l=this._getCurrentPreset(),c=null!==(t=null===(e=l.map_source.crop)||void 0===e?void 0:e.top)&&void 0!==t?t:0,d=null!==(i=null===(a=l.map_source.crop)||void 0===a?void 0:a.bottom)&&void 0!==i?i:0,p=null!==(r=null===(n=l.map_source.crop)||void 0===n?void 0:n.left)&&void 0!==r?r:0,u=null!==(s=null===(o=l.map_source.crop)||void 0===o?void 0:o.right)&&void 0!==s?s:0;if(this._calculateBasicScale(),this.selectedManualRectangles.length>=this._getCurrentMode().maxSelections)return void ze("failure");const m=this.realImageHeight*this.realScale-c-d,h=this.realImageWidth*this.realScale-p-u,v=(this.selectedManualRectangles.length+1).toString(),_=(h/3+p-this.mapX)/this.mapScale,g=(m/3+c-this.mapY)/this.mapScale,f=h/3/this.mapScale,b=m/3/this.mapScale;this.selectedManualRectangles.push(new Za(_,g,f,b,v,this._getContext())),ze("selection"),this.requestUpdate()}_mouseDown(e){e instanceof MouseEvent&&0!=e.button||(this.shouldHandleMouseUp=!0)}_mouseMove(e){e.target.classList.contains("draggable")||(this.selectedManualRectangles.filter((e=>e.isSelected())).forEach((t=>t.externalDrag(e))),this.shouldHandleMouseUp=!1)}_mouseUp(e){if(!(e instanceof MouseEvent&&0!=e.button)&&this.shouldHandleMouseUp){const t=Da(e,this._getSvgWrapper());switch(this._getCurrentMode().selectionType){case Ma.MANUAL_PATH:ze("selection"),this.selectedManualPath.addPoint(t.x,t.y);break;case Ma.MANUAL_POINT:ze("selection"),this.selectedManualPoint=new Qa(t.x,t.y,this._getContext());break;default:return}Aa(e),this.requestUpdate()}this.shouldHandleMouseUp=!1}_handleRunAction(){return e=>{if(this.hass&&e.detail.action)switch(e.detail.action){case"tap":this._run(!1);break;case"hold":this._run(!0);break;case"double_tap":console.log(JSON.stringify(Object.assign(Object.assign({},this._getCurrentPreset()),{additional_presets:void 0,title:void 0,type:void 0}),null,2)),window.alert("Configuration available in browser's console"),ze("success")}}}_restoreMap(){const e=this._getMapZoomerContent();e.style.transitionDuration=this._getCssProperty("--map-card-internal-transitions-duration"),this._getPinchZoom().setTransform({scale:1,x:0,y:0,allowChangeEvent:!0}),this.mapScale=1,ze("selection"),this._delay(300).then((()=>e.style.transitionDuration="0s"))}_getCssProperty(e){return getComputedStyle(this._getMapImage()).getPropertyValue(e)}_zoomIn(){ze("selection"),this._updateScale(1.5)}_zoomOut(){ze("selection"),this._updateScale(1/1.5)}_updateScale(e){const t=this._getMapZoomerContent(),a=this._getPinchZoom(),i=this._getPinchZoom().getBoundingClientRect();this.mapScale=Math.max(this.mapScale*e,.5),t.style.transitionDuration="200ms",a.scaleTo(this.mapScale,{originX:i.left+i.width/2,originY:i.top+i.height/2,relativeTo:"container",allowChangeEvent:!0}),this._delay(300).then((()=>t.style.transitionDuration="0s"))}_calculateBasicScale(){const e=this._getMapImage();e&&e.naturalWidth>0&&(this.realImageWidth=e.naturalWidth,this.realImageHeight=e.naturalHeight,this.realScale=e.width/e.naturalWidth)}_calculateScale(){const e=this._getPinchZoom();this.mapScale=e.scale,this.mapX=e.x,this.mapY=e.y}_getPinchZoom(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.getElementById("map-zoomer")}_getMapImage(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.getElementById("map-image")}_getMapZoomerContent(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.getElementById("map-zoomer-content")}_getSvgWrapper(){var e;return null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("#svg-wrapper")}_showConfigErrors(e){e.forEach((e=>console.error(e)));const t=document.createElement("hui-error-card");return t.setConfig({type:"error",error:e[0],origConfig:this.config}),I` ${t} `}_showOldConfig(){return I`
            <hui-warning>
                <h1>Xiaomi Vacuum Map Card ${"v2.0.2"}</h1>
                <p>${this._localize("common.old_configuration")}</p>
                <p>
                    <a
                        href="https://github.com/PiotrMachowski/lovelace-xiaomi-vacuum-map-card#migrating-from-v1xx"
                        target="_blank"
                        >${this._localize("common.old_configuration_migration_link")}</a
                    >
                </p>
            </hui-warning>
        `}_showInvalidEntities(e){return I`
            <hui-warning>
                <h1>${this._localize("validation.invalid_entities")}</h1>
                <ul>
                    ${e.map((e=>I` <li>
                            <pre>${e}</pre>
                        </li>`))}
                </ul>
            </hui-warning>
        `}_showInvalidCalibrationWarning(){return I`<hui-warning>${this._localize("validation.invalid_calibration")}</hui-warning> `}_localize(e){return Gt(e,this.config.language)}async _delay(e){await new Promise((t=>setTimeout((()=>t()),e)))}_showToast(e,t,a,i=""){var n,r,o;const s=null===(n=this.shadowRoot)||void 0===n?void 0:n.getElementById("toast"),l=null===(r=this.shadowRoot)||void 0===r?void 0:r.getElementById("toast-text"),c=null===(o=this.shadowRoot)||void 0===o?void 0:o.getElementById("toast-icon");s&&l&&c&&(s.className="show",l.innerText=this._localize(e)+(i?`\n${i}`:""),c.children[0].setAttribute("icon",t),c.style.color=a?"var(--map-card-internal-toast-successful-icon-color)":"var(--map-card-internal-toast-unsuccessful-icon-color)",this._delay(2e3).then((()=>s.className=s.className.replace("show",""))))}static get styles(){return o`
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
                width: calc(100% - 20px);
                display: inline-flex;
                align-content: center;
                justify-content: space-between;
                align-items: center;
                margin: 10px;
            }

            .preset-selector-icon.disabled {
                color: var(--map-card-internal-disabled-text-color);
            }

            .preset-label-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .preset-indicator {
                line-height: 50%;
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

            ${Wa.styles}
            ${Za.styles}
            ${ii.styles}
            ${ti.styles}
            ${Qa.styles}
            ${ai.styles}
            ${ni.styles}
            ${hi.styles}
            ${ui.styles}
            ${pi.styles}
            ${mi.styles}
        `}};e([se({attribute:!1})],Pi.prototype,"_hass",void 0),e([le()],Pi.prototype,"oldConfig",void 0),e([le()],Pi.prototype,"config",void 0),e([le()],Pi.prototype,"presetIndex",void 0),e([le()],Pi.prototype,"realScale",void 0),e([le()],Pi.prototype,"realImageWidth",void 0),e([le()],Pi.prototype,"realImageHeight",void 0),e([le()],Pi.prototype,"mapScale",void 0),e([le()],Pi.prototype,"mapX",void 0),e([le()],Pi.prototype,"mapY",void 0),e([le()],Pi.prototype,"repeats",void 0),e([le()],Pi.prototype,"selectedMode",void 0),e([le()],Pi.prototype,"mapLocked",void 0),e([le()],Pi.prototype,"configErrors",void 0),Pi=e([re("xiaomi-vacuum-map-card")],Pi);export{Pi as XiaomiVacuumMapCard};
