/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const t=new WeakMap,e=e=>"function"==typeof e&&t.has(e),r=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,i=(t,e,r=null)=>{for(;e!==r;){const r=e.nextSibling;t.removeChild(e),e=r}},s={},n={},o=`{{lit-${String(Math.random()).slice(2)}}}`,a=`\x3c!--${o}--\x3e`,h=new RegExp(`${o}|${a}`);class c{constructor(t,e){this.parts=[],this.element=e;const r=[],i=[],s=document.createTreeWalker(e.content,133,null,!1);let n=0,a=-1,c=0;const{strings:d,values:{length:f}}=t;for(;c<f;){const t=s.nextNode();if(null!==t){if(a++,1===t.nodeType){if(t.hasAttributes()){const e=t.attributes,{length:r}=e;let i=0;for(let t=0;t<r;t++)l(e[t].name,"$lit$")&&i++;for(;i-- >0;){const e=d[c],r=p.exec(e)[2],i=r.toLowerCase()+"$lit$",s=t.getAttribute(i);t.removeAttribute(i);const n=s.split(h);this.parts.push({type:"attribute",index:a,name:r,strings:n}),c+=n.length-1}}"TEMPLATE"===t.tagName&&(i.push(t),s.currentNode=t.content)}else if(3===t.nodeType){const e=t.data;if(e.indexOf(o)>=0){const i=t.parentNode,s=e.split(h),n=s.length-1;for(let e=0;e<n;e++){let r,n=s[e];if(""===n)r=u();else{const t=p.exec(n);null!==t&&l(t[2],"$lit$")&&(n=n.slice(0,t.index)+t[1]+t[2].slice(0,-"$lit$".length)+t[3]),r=document.createTextNode(n)}i.insertBefore(r,t),this.parts.push({type:"node",index:++a})}""===s[n]?(i.insertBefore(u(),t),r.push(t)):t.data=s[n],c+=n}}else if(8===t.nodeType)if(t.data===o){const e=t.parentNode;null!==t.previousSibling&&a!==n||(a++,e.insertBefore(u(),t)),n=a,this.parts.push({type:"node",index:a}),null===t.nextSibling?t.data="":(r.push(t),a--),c++}else{let e=-1;for(;-1!==(e=t.data.indexOf(o,e+1));)this.parts.push({type:"node",index:-1}),c++}}else s.currentNode=i.pop()}for(const t of r)t.parentNode.removeChild(t)}}const l=(t,e)=>{const r=t.length-e.length;return r>=0&&t.slice(r)===e},d=t=>-1!==t.index,u=()=>document.createComment(""),p=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
class f{constructor(t,e,r){this.__parts=[],this.template=t,this.processor=e,this.options=r}update(t){let e=0;for(const r of this.__parts)void 0!==r&&r.setValue(t[e]),e++;for(const t of this.__parts)void 0!==t&&t.commit()}_clone(){const t=r?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),e=[],i=this.template.parts,s=document.createTreeWalker(t,133,null,!1);let n,o=0,a=0,h=s.nextNode();for(;o<i.length;)if(n=i[o],d(n)){for(;a<n.index;)a++,"TEMPLATE"===h.nodeName&&(e.push(h),s.currentNode=h.content),null===(h=s.nextNode())&&(s.currentNode=e.pop(),h=s.nextNode());if("node"===n.type){const t=this.processor.handleTextExpression(this.options);t.insertAfterNode(h.previousSibling),this.__parts.push(t)}else this.__parts.push(...this.processor.handleAttributeExpressions(h,n.name,n.strings,this.options));o++}else this.__parts.push(void 0),o++;return r&&(document.adoptNode(t),customElements.upgrade(t)),t}}
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const g=` ${o} `;class m{constructor(t,e,r,i){this.strings=t,this.values=e,this.type=r,this.processor=i}getHTML(){const t=this.strings.length-1;let e="",r=!1;for(let i=0;i<t;i++){const t=this.strings[i],s=t.lastIndexOf("\x3c!--");r=(s>-1||r)&&-1===t.indexOf("--\x3e",s+1);const n=p.exec(t);e+=null===n?t+(r?g:a):t.substr(0,n.index)+n[1]+n[2]+"$lit$"+n[3]+o}return e+=this.strings[t],e}getTemplateElement(){const t=document.createElement("template");return t.innerHTML=this.getHTML(),t}}
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const b=t=>null===t||!("object"==typeof t||"function"==typeof t),y=t=>Array.isArray(t)||!(!t||!t[Symbol.iterator]);class v{constructor(t,e,r){this.dirty=!0,this.element=t,this.name=e,this.strings=r,this.parts=[];for(let t=0;t<r.length-1;t++)this.parts[t]=this._createPart()}_createPart(){return new w(this)}_getValue(){const t=this.strings,e=t.length-1;let r="";for(let i=0;i<e;i++){r+=t[i];const e=this.parts[i];if(void 0!==e){const t=e.value;if(b(t)||!y(t))r+="string"==typeof t?t:String(t);else for(const e of t)r+="string"==typeof e?e:String(e)}}return r+=t[e],r}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class w{constructor(t){this.value=void 0,this.committer=t}setValue(t){t===s||b(t)&&t===this.value||(this.value=t,e(t)||(this.committer.dirty=!0))}commit(){for(;e(this.value);){const t=this.value;this.value=s,t(this)}this.value!==s&&this.committer.commit()}}class _{constructor(t){this.value=void 0,this.__pendingValue=void 0,this.options=t}appendInto(t){this.startNode=t.appendChild(u()),this.endNode=t.appendChild(u())}insertAfterNode(t){this.startNode=t,this.endNode=t.nextSibling}appendIntoPart(t){t.__insert(this.startNode=u()),t.__insert(this.endNode=u())}insertAfterPart(t){t.__insert(this.startNode=u()),this.endNode=t.endNode,t.endNode=this.startNode}setValue(t){this.__pendingValue=t}commit(){for(;e(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=s,t(this)}const t=this.__pendingValue;t!==s&&(b(t)?t!==this.value&&this.__commitText(t):t instanceof m?this.__commitTemplateResult(t):t instanceof Node?this.__commitNode(t):y(t)?this.__commitIterable(t):t===n?(this.value=n,this.clear()):this.__commitText(t))}__insert(t){this.endNode.parentNode.insertBefore(t,this.endNode)}__commitNode(t){this.value!==t&&(this.clear(),this.__insert(t),this.value=t)}__commitText(t){const e=this.startNode.nextSibling,r="string"==typeof(t=null==t?"":t)?t:String(t);e===this.endNode.previousSibling&&3===e.nodeType?e.data=r:this.__commitNode(document.createTextNode(r)),this.value=t}__commitTemplateResult(t){const e=this.options.templateFactory(t);if(this.value instanceof f&&this.value.template===e)this.value.update(t.values);else{const r=new f(e,t.processor,this.options),i=r._clone();r.update(t.values),this.__commitNode(i),this.value=r}}__commitIterable(t){Array.isArray(this.value)||(this.value=[],this.clear());const e=this.value;let r,i=0;for(const s of t)r=e[i],void 0===r&&(r=new _(this.options),e.push(r),0===i?r.appendIntoPart(this):r.insertAfterPart(e[i-1])),r.setValue(s),r.commit(),i++;i<e.length&&(e.length=i,this.clear(r&&r.endNode))}clear(t=this.startNode){i(this.startNode.parentNode,t.nextSibling,this.endNode)}}class S{constructor(t,e,r){if(this.value=void 0,this.__pendingValue=void 0,2!==r.length||""!==r[0]||""!==r[1])throw new Error("Boolean attributes can only contain a single expression");this.element=t,this.name=e,this.strings=r}setValue(t){this.__pendingValue=t}commit(){for(;e(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=s,t(this)}if(this.__pendingValue===s)return;const t=!!this.__pendingValue;this.value!==t&&(t?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name),this.value=t),this.__pendingValue=s}}class x extends v{constructor(t,e,r){super(t,e,r),this.single=2===r.length&&""===r[0]&&""===r[1]}_createPart(){return new C(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class C extends w{}let M=!1;try{const t={get capture(){return M=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(t){}class k{constructor(t,e,r){this.value=void 0,this.__pendingValue=void 0,this.element=t,this.eventName=e,this.eventContext=r,this.__boundHandleEvent=t=>this.handleEvent(t)}setValue(t){this.__pendingValue=t}commit(){for(;e(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=s,t(this)}if(this.__pendingValue===s)return;const t=this.__pendingValue,r=this.value,i=null==t||null!=r&&(t.capture!==r.capture||t.once!==r.once||t.passive!==r.passive),n=null!=t&&(null==r||i);i&&this.element.removeEventListener(this.eventName,this.__boundHandleEvent,this.__options),n&&(this.__options=P(t),this.element.addEventListener(this.eventName,this.__boundHandleEvent,this.__options)),this.value=t,this.__pendingValue=s}handleEvent(t){"function"==typeof this.value?this.value.call(this.eventContext||this.element,t):this.value.handleEvent(t)}}const P=t=>t&&(M?{capture:t.capture,passive:t.passive,once:t.once}:t.capture)
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */;const N=new class{handleAttributeExpressions(t,e,r,i){const s=e[0];if("."===s){return new x(t,e.slice(1),r).parts}return"@"===s?[new k(t,e.slice(1),i.eventContext)]:"?"===s?[new S(t,e.slice(1),r)]:new v(t,e,r).parts}handleTextExpression(t){return new _(t)}};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */function A(t){let e=E.get(t.type);void 0===e&&(e={stringsArray:new WeakMap,keyString:new Map},E.set(t.type,e));let r=e.stringsArray.get(t.strings);if(void 0!==r)return r;const i=t.strings.join(o);return r=e.keyString.get(i),void 0===r&&(r=new c(t,t.getTemplateElement()),e.keyString.set(i,r)),e.stringsArray.set(t.strings,r),r}const E=new Map,$=new WeakMap;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.1.2");const O=(t,...e)=>new m(t,e,"html",N)
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */;function T(t,e){const{element:{content:r},parts:i}=t,s=document.createTreeWalker(r,133,null,!1);let n=H(i),o=i[n],a=-1,h=0;const c=[];let l=null;for(;s.nextNode();){a++;const t=s.currentNode;for(t.previousSibling===l&&(l=null),e.has(t)&&(c.push(t),null===l&&(l=t)),null!==l&&h++;void 0!==o&&o.index===a;)o.index=null!==l?-1:o.index-h,n=H(i,n),o=i[n]}c.forEach(t=>t.parentNode.removeChild(t))}const R=t=>{let e=11===t.nodeType?0:1;const r=document.createTreeWalker(t,133,null,!1);for(;r.nextNode();)e++;return e},H=(t,e=-1)=>{for(let r=e+1;r<t.length;r++){const e=t[r];if(d(e))return r}return-1};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const F=(t,e)=>`${t}--${e}`;let D=!0;void 0===window.ShadyCSS?D=!1:void 0===window.ShadyCSS.prepareTemplateDom&&(console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."),D=!1);const V=t=>e=>{const r=F(e.type,t);let i=E.get(r);void 0===i&&(i={stringsArray:new WeakMap,keyString:new Map},E.set(r,i));let s=i.stringsArray.get(e.strings);if(void 0!==s)return s;const n=e.strings.join(o);if(s=i.keyString.get(n),void 0===s){const r=e.getTemplateElement();D&&window.ShadyCSS.prepareTemplateDom(r,t),s=new c(e,r),i.keyString.set(n,s)}return i.stringsArray.set(e.strings,s),s},j=["html","svg"],q=new Set,z=(t,e,r)=>{q.add(t);const i=r?r.element:document.createElement("template"),s=e.querySelectorAll("style"),{length:n}=s;if(0===n)return void window.ShadyCSS.prepareTemplateStyles(i,t);const o=document.createElement("style");for(let t=0;t<n;t++){const e=s[t];e.parentNode.removeChild(e),o.textContent+=e.textContent}(t=>{j.forEach(e=>{const r=E.get(F(e,t));void 0!==r&&r.keyString.forEach(t=>{const{element:{content:e}}=t,r=new Set;Array.from(e.querySelectorAll("style")).forEach(t=>{r.add(t)}),T(t,r)})})})(t);const a=i.content;r?function(t,e,r=null){const{element:{content:i},parts:s}=t;if(null==r)return void i.appendChild(e);const n=document.createTreeWalker(i,133,null,!1);let o=H(s),a=0,h=-1;for(;n.nextNode();){for(h++,n.currentNode===r&&(a=R(e),r.parentNode.insertBefore(e,r));-1!==o&&s[o].index===h;){if(a>0){for(;-1!==o;)s[o].index+=a,o=H(s,o);return}o=H(s,o)}}}(r,o,a.firstChild):a.insertBefore(o,a.firstChild),window.ShadyCSS.prepareTemplateStyles(i,t);const h=a.querySelector("style");if(window.ShadyCSS.nativeShadow&&null!==h)e.insertBefore(h.cloneNode(!0),e.firstChild);else if(r){a.insertBefore(o,a.firstChild);const t=new Set;t.add(o),T(r,t)}};window.JSCompiler_renameProperty=(t,e)=>t;const B={toAttribute(t,e){switch(e){case Boolean:return t?"":null;case Object:case Array:return null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){switch(e){case Boolean:return null!==t;case Number:return null===t?null:Number(t);case Object:case Array:return JSON.parse(t)}return t}},Y=(t,e)=>e!==t&&(e==e||t==t),I={attribute:!0,type:String,converter:B,reflect:!1,hasChanged:Y},L=Promise.resolve(!0);class U extends HTMLElement{constructor(){super(),this._updateState=0,this._instanceProperties=void 0,this._updatePromise=L,this._hasConnectedResolver=void 0,this._changedProperties=new Map,this._reflectingProperties=void 0,this.initialize()}static get observedAttributes(){this.finalize();const t=[];return this._classProperties.forEach((e,r)=>{const i=this._attributeNameForProperty(r,e);void 0!==i&&(this._attributeToPropertyMap.set(i,r),t.push(i))}),t}static _ensureClassProperties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties",this))){this._classProperties=new Map;const t=Object.getPrototypeOf(this)._classProperties;void 0!==t&&t.forEach((t,e)=>this._classProperties.set(e,t))}}static createProperty(t,e=I){if(this._ensureClassProperties(),this._classProperties.set(t,e),e.noAccessor||this.prototype.hasOwnProperty(t))return;const r="symbol"==typeof t?Symbol():`__${t}`;Object.defineProperty(this.prototype,t,{get(){return this[r]},set(e){const i=this[t];this[r]=e,this._requestUpdate(t,i)},configurable:!0,enumerable:!0})}static finalize(){const t=Object.getPrototypeOf(this);if(t.hasOwnProperty("finalized")||t.finalize(),this.finalized=!0,this._ensureClassProperties(),this._attributeToPropertyMap=new Map,this.hasOwnProperty(JSCompiler_renameProperty("properties",this))){const t=this.properties,e=[...Object.getOwnPropertyNames(t),..."function"==typeof Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(t):[]];for(const r of e)this.createProperty(r,t[r])}}static _attributeNameForProperty(t,e){const r=e.attribute;return!1===r?void 0:"string"==typeof r?r:"string"==typeof t?t.toLowerCase():void 0}static _valueHasChanged(t,e,r=Y){return r(t,e)}static _propertyValueFromAttribute(t,e){const r=e.type,i=e.converter||B,s="function"==typeof i?i:i.fromAttribute;return s?s(t,r):t}static _propertyValueToAttribute(t,e){if(void 0===e.reflect)return;const r=e.type,i=e.converter;return(i&&i.toAttribute||B.toAttribute)(t,r)}initialize(){this._saveInstanceProperties(),this._requestUpdate()}_saveInstanceProperties(){this.constructor._classProperties.forEach((t,e)=>{if(this.hasOwnProperty(e)){const t=this[e];delete this[e],this._instanceProperties||(this._instanceProperties=new Map),this._instanceProperties.set(e,t)}})}_applyInstanceProperties(){this._instanceProperties.forEach((t,e)=>this[e]=t),this._instanceProperties=void 0}connectedCallback(){this._updateState=32|this._updateState,this._hasConnectedResolver&&(this._hasConnectedResolver(),this._hasConnectedResolver=void 0)}disconnectedCallback(){}attributeChangedCallback(t,e,r){e!==r&&this._attributeToProperty(t,r)}_propertyToAttribute(t,e,r=I){const i=this.constructor,s=i._attributeNameForProperty(t,r);if(void 0!==s){const t=i._propertyValueToAttribute(e,r);if(void 0===t)return;this._updateState=8|this._updateState,null==t?this.removeAttribute(s):this.setAttribute(s,t),this._updateState=-9&this._updateState}}_attributeToProperty(t,e){if(8&this._updateState)return;const r=this.constructor,i=r._attributeToPropertyMap.get(t);if(void 0!==i){const t=r._classProperties.get(i)||I;this._updateState=16|this._updateState,this[i]=r._propertyValueFromAttribute(e,t),this._updateState=-17&this._updateState}}_requestUpdate(t,e){let r=!0;if(void 0!==t){const i=this.constructor,s=i._classProperties.get(t)||I;i._valueHasChanged(this[t],e,s.hasChanged)?(this._changedProperties.has(t)||this._changedProperties.set(t,e),!0!==s.reflect||16&this._updateState||(void 0===this._reflectingProperties&&(this._reflectingProperties=new Map),this._reflectingProperties.set(t,s))):r=!1}!this._hasRequestedUpdate&&r&&this._enqueueUpdate()}requestUpdate(t,e){return this._requestUpdate(t,e),this.updateComplete}async _enqueueUpdate(){let t,e;this._updateState=4|this._updateState;const r=this._updatePromise;this._updatePromise=new Promise((r,i)=>{t=r,e=i});try{await r}catch(t){}this._hasConnected||await new Promise(t=>this._hasConnectedResolver=t);try{const t=this.performUpdate();null!=t&&await t}catch(t){e(t)}t(!this._hasRequestedUpdate)}get _hasConnected(){return 32&this._updateState}get _hasRequestedUpdate(){return 4&this._updateState}get hasUpdated(){return 1&this._updateState}performUpdate(){this._instanceProperties&&this._applyInstanceProperties();let t=!1;const e=this._changedProperties;try{t=this.shouldUpdate(e),t&&this.update(e)}catch(e){throw t=!1,e}finally{this._markUpdated()}t&&(1&this._updateState||(this._updateState=1|this._updateState,this.firstUpdated(e)),this.updated(e))}_markUpdated(){this._changedProperties=new Map,this._updateState=-5&this._updateState}get updateComplete(){return this._getUpdateComplete()}_getUpdateComplete(){return this._updatePromise}shouldUpdate(t){return!0}update(t){void 0!==this._reflectingProperties&&this._reflectingProperties.size>0&&(this._reflectingProperties.forEach((t,e)=>this._propertyToAttribute(e,this[e],t)),this._reflectingProperties=void 0)}updated(t){}firstUpdated(t){}}U.finalized=!0;
/**
@license
Copyright (c) 2019 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/
const W="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,J=Symbol();class Z{constructor(t,e){if(e!==J)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t}get styleSheet(){return void 0===this._styleSheet&&(W?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}const G=(t,...e)=>{const r=e.reduce((e,r,i)=>e+(t=>{if(t instanceof Z)return t.cssText;if("number"==typeof t)return t;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${t}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(r)+t[i+1],t[0]);return new Z(r,J)};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litElementVersions||(window.litElementVersions=[])).push("2.2.1");const K=t=>t.flat?t.flat(1/0):function t(e,r=[]){for(let i=0,s=e.length;i<s;i++){const s=e[i];Array.isArray(s)?t(s,r):r.push(s)}return r}(t);class Q extends U{static finalize(){super.finalize.call(this),this._styles=this.hasOwnProperty(JSCompiler_renameProperty("styles",this))?this._getUniqueStyles():this._styles||[]}static _getUniqueStyles(){const t=this.styles,e=[];if(Array.isArray(t)){K(t).reduceRight((t,e)=>(t.add(e),t),new Set).forEach(t=>e.unshift(t))}else t&&e.push(t);return e}initialize(){super.initialize(),this.renderRoot=this.createRenderRoot(),window.ShadowRoot&&this.renderRoot instanceof window.ShadowRoot&&this.adoptStyles()}createRenderRoot(){return this.attachShadow({mode:"open"})}adoptStyles(){const t=this.constructor._styles;0!==t.length&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow?W?this.renderRoot.adoptedStyleSheets=t.map(t=>t.styleSheet):this._needsShimAdoptedStyleSheets=!0:window.ShadyCSS.ScopingShim.prepareAdoptedCssText(t.map(t=>t.cssText),this.localName))}connectedCallback(){super.connectedCallback(),this.hasUpdated&&void 0!==window.ShadyCSS&&window.ShadyCSS.styleElement(this)}update(t){super.update(t);const e=this.render();e instanceof m&&this.constructor.render(e,this.renderRoot,{scopeName:this.localName,eventContext:this}),this._needsShimAdoptedStyleSheets&&(this._needsShimAdoptedStyleSheets=!1,this.constructor._styles.forEach(t=>{const e=document.createElement("style");e.textContent=t.cssText,this.renderRoot.appendChild(e)}))}render(){}}function X(t,e){(function(t){return"string"==typeof t&&t.includes(".")&&1===parseFloat(t)})(t)&&(t="100%");var r=function(t){return"string"==typeof t&&t.includes("%")}(t);return t=360===e?t:Math.min(e,Math.max(0,parseFloat(t))),r&&(t=parseInt(String(t*e),10)/100),Math.abs(t-e)<1e-6?1:t=360===e?(t<0?t%e+e:t%e)/parseFloat(String(e)):t%e/parseFloat(String(e))}function tt(t){return Math.min(1,Math.max(0,t))}function et(t){return t=parseFloat(t),(isNaN(t)||t<0||t>1)&&(t=1),t}function rt(t){return t<=1?100*Number(t)+"%":t}function it(t){return 1===t.length?"0"+t:String(t)}function st(t,e,r){t=X(t,255),e=X(e,255),r=X(r,255);var i=Math.max(t,e,r),s=Math.min(t,e,r),n=0,o=0,a=(i+s)/2;if(i===s)o=0,n=0;else{var h=i-s;switch(o=a>.5?h/(2-i-s):h/(i+s),i){case t:n=(e-r)/h+(e<r?6:0);break;case e:n=(r-t)/h+2;break;case r:n=(t-e)/h+4}n/=6}return{h:n,s:o,l:a}}function nt(t,e,r){return r<0&&(r+=1),r>1&&(r-=1),r<1/6?t+6*r*(e-t):r<.5?e:r<2/3?t+(e-t)*(2/3-r)*6:t}function ot(t,e,r){t=X(t,255),e=X(e,255),r=X(r,255);var i=Math.max(t,e,r),s=Math.min(t,e,r),n=0,o=i,a=i-s,h=0===i?0:a/i;if(i===s)n=0;else{switch(i){case t:n=(e-r)/a+(e<r?6:0);break;case e:n=(r-t)/a+2;break;case r:n=(t-e)/a+4}n/=6}return{h:n,s:h,v:o}}function at(t,e,r,i){var s=[it(Math.round(t).toString(16)),it(Math.round(e).toString(16)),it(Math.round(r).toString(16))];return i&&s[0].startsWith(s[0].charAt(1))&&s[1].startsWith(s[1].charAt(1))&&s[2].startsWith(s[2].charAt(1))?s[0].charAt(0)+s[1].charAt(0)+s[2].charAt(0):s.join("")}function ht(t){return Math.round(255*parseFloat(t)).toString(16)}function ct(t){return lt(t)/255}function lt(t){return parseInt(t,16)}Q.finalized=!0,Q.render=(t,e,r)=>{if(!r||"object"!=typeof r||!r.scopeName)throw new Error("The `scopeName` option is required.");const s=r.scopeName,n=$.has(e),o=D&&11===e.nodeType&&!!e.host,a=o&&!q.has(s),h=a?document.createDocumentFragment():e;if(((t,e,r)=>{let s=$.get(e);void 0===s&&(i(e,e.firstChild),$.set(e,s=new _(Object.assign({templateFactory:A},r))),s.appendInto(e)),s.setValue(t),s.commit()})(t,h,Object.assign({templateFactory:V(s)},r)),a){const t=$.get(h);$.delete(h);const r=t.value instanceof f?t.value.template:void 0;z(s,h,r),i(e,e.firstChild),e.appendChild(h),$.set(e,t)}!n&&o&&window.ShadyCSS.styleElement(e.host)};var dt={aliceblue:"#f0f8ff",antiquewhite:"#faebd7",aqua:"#00ffff",aquamarine:"#7fffd4",azure:"#f0ffff",beige:"#f5f5dc",bisque:"#ffe4c4",black:"#000000",blanchedalmond:"#ffebcd",blue:"#0000ff",blueviolet:"#8a2be2",brown:"#a52a2a",burlywood:"#deb887",cadetblue:"#5f9ea0",chartreuse:"#7fff00",chocolate:"#d2691e",coral:"#ff7f50",cornflowerblue:"#6495ed",cornsilk:"#fff8dc",crimson:"#dc143c",cyan:"#00ffff",darkblue:"#00008b",darkcyan:"#008b8b",darkgoldenrod:"#b8860b",darkgray:"#a9a9a9",darkgreen:"#006400",darkgrey:"#a9a9a9",darkkhaki:"#bdb76b",darkmagenta:"#8b008b",darkolivegreen:"#556b2f",darkorange:"#ff8c00",darkorchid:"#9932cc",darkred:"#8b0000",darksalmon:"#e9967a",darkseagreen:"#8fbc8f",darkslateblue:"#483d8b",darkslategray:"#2f4f4f",darkslategrey:"#2f4f4f",darkturquoise:"#00ced1",darkviolet:"#9400d3",deeppink:"#ff1493",deepskyblue:"#00bfff",dimgray:"#696969",dimgrey:"#696969",dodgerblue:"#1e90ff",firebrick:"#b22222",floralwhite:"#fffaf0",forestgreen:"#228b22",fuchsia:"#ff00ff",gainsboro:"#dcdcdc",ghostwhite:"#f8f8ff",gold:"#ffd700",goldenrod:"#daa520",gray:"#808080",green:"#008000",greenyellow:"#adff2f",grey:"#808080",honeydew:"#f0fff0",hotpink:"#ff69b4",indianred:"#cd5c5c",indigo:"#4b0082",ivory:"#fffff0",khaki:"#f0e68c",lavender:"#e6e6fa",lavenderblush:"#fff0f5",lawngreen:"#7cfc00",lemonchiffon:"#fffacd",lightblue:"#add8e6",lightcoral:"#f08080",lightcyan:"#e0ffff",lightgoldenrodyellow:"#fafad2",lightgray:"#d3d3d3",lightgreen:"#90ee90",lightgrey:"#d3d3d3",lightpink:"#ffb6c1",lightsalmon:"#ffa07a",lightseagreen:"#20b2aa",lightskyblue:"#87cefa",lightslategray:"#778899",lightslategrey:"#778899",lightsteelblue:"#b0c4de",lightyellow:"#ffffe0",lime:"#00ff00",limegreen:"#32cd32",linen:"#faf0e6",magenta:"#ff00ff",maroon:"#800000",mediumaquamarine:"#66cdaa",mediumblue:"#0000cd",mediumorchid:"#ba55d3",mediumpurple:"#9370db",mediumseagreen:"#3cb371",mediumslateblue:"#7b68ee",mediumspringgreen:"#00fa9a",mediumturquoise:"#48d1cc",mediumvioletred:"#c71585",midnightblue:"#191970",mintcream:"#f5fffa",mistyrose:"#ffe4e1",moccasin:"#ffe4b5",navajowhite:"#ffdead",navy:"#000080",oldlace:"#fdf5e6",olive:"#808000",olivedrab:"#6b8e23",orange:"#ffa500",orangered:"#ff4500",orchid:"#da70d6",palegoldenrod:"#eee8aa",palegreen:"#98fb98",paleturquoise:"#afeeee",palevioletred:"#db7093",papayawhip:"#ffefd5",peachpuff:"#ffdab9",peru:"#cd853f",pink:"#ffc0cb",plum:"#dda0dd",powderblue:"#b0e0e6",purple:"#800080",rebeccapurple:"#663399",red:"#ff0000",rosybrown:"#bc8f8f",royalblue:"#4169e1",saddlebrown:"#8b4513",salmon:"#fa8072",sandybrown:"#f4a460",seagreen:"#2e8b57",seashell:"#fff5ee",sienna:"#a0522d",silver:"#c0c0c0",skyblue:"#87ceeb",slateblue:"#6a5acd",slategray:"#708090",slategrey:"#708090",snow:"#fffafa",springgreen:"#00ff7f",steelblue:"#4682b4",tan:"#d2b48c",teal:"#008080",thistle:"#d8bfd8",tomato:"#ff6347",turquoise:"#40e0d0",violet:"#ee82ee",wheat:"#f5deb3",white:"#ffffff",whitesmoke:"#f5f5f5",yellow:"#ffff00",yellowgreen:"#9acd32"};function ut(t){var e={r:0,g:0,b:0},r=1,i=null,s=null,n=null,o=!1,a=!1;return"string"==typeof t&&(t=function(t){if(0===(t=t.trim().toLowerCase()).length)return!1;var e=!1;if(dt[t])t=dt[t],e=!0;else if("transparent"===t)return{r:0,g:0,b:0,a:0,format:"name"};var r=mt.rgb.exec(t);if(r)return{r:r[1],g:r[2],b:r[3]};if(r=mt.rgba.exec(t))return{r:r[1],g:r[2],b:r[3],a:r[4]};if(r=mt.hsl.exec(t))return{h:r[1],s:r[2],l:r[3]};if(r=mt.hsla.exec(t))return{h:r[1],s:r[2],l:r[3],a:r[4]};if(r=mt.hsv.exec(t))return{h:r[1],s:r[2],v:r[3]};if(r=mt.hsva.exec(t))return{h:r[1],s:r[2],v:r[3],a:r[4]};if(r=mt.hex8.exec(t))return{r:lt(r[1]),g:lt(r[2]),b:lt(r[3]),a:ct(r[4]),format:e?"name":"hex8"};if(r=mt.hex6.exec(t))return{r:lt(r[1]),g:lt(r[2]),b:lt(r[3]),format:e?"name":"hex"};if(r=mt.hex4.exec(t))return{r:lt(r[1]+r[1]),g:lt(r[2]+r[2]),b:lt(r[3]+r[3]),a:ct(r[4]+r[4]),format:e?"name":"hex8"};if(r=mt.hex3.exec(t))return{r:lt(r[1]+r[1]),g:lt(r[2]+r[2]),b:lt(r[3]+r[3]),format:e?"name":"hex"};return!1}(t)),"object"==typeof t&&(bt(t.r)&&bt(t.g)&&bt(t.b)?(e=function(t,e,r){return{r:255*X(t,255),g:255*X(e,255),b:255*X(r,255)}}(t.r,t.g,t.b),o=!0,a="%"===String(t.r).substr(-1)?"prgb":"rgb"):bt(t.h)&&bt(t.s)&&bt(t.v)?(i=rt(t.s),s=rt(t.v),e=function(t,e,r){t=6*X(t,360),e=X(e,100),r=X(r,100);var i=Math.floor(t),s=t-i,n=r*(1-e),o=r*(1-s*e),a=r*(1-(1-s)*e),h=i%6;return{r:255*[r,o,n,n,a,r][h],g:255*[a,r,r,o,n,n][h],b:255*[n,n,a,r,r,o][h]}}(t.h,i,s),o=!0,a="hsv"):bt(t.h)&&bt(t.s)&&bt(t.l)&&(i=rt(t.s),n=rt(t.l),e=function(t,e,r){var i,s,n;if(t=X(t,360),e=X(e,100),r=X(r,100),0===e)s=r,n=r,i=r;else{var o=r<.5?r*(1+e):r+e-r*e,a=2*r-o;i=nt(a,o,t+1/3),s=nt(a,o,t),n=nt(a,o,t-1/3)}return{r:255*i,g:255*s,b:255*n}}(t.h,i,n),o=!0,a="hsl"),Object.prototype.hasOwnProperty.call(t,"a")&&(r=t.a)),r=et(r),{ok:o,format:t.format||a,r:Math.min(255,Math.max(e.r,0)),g:Math.min(255,Math.max(e.g,0)),b:Math.min(255,Math.max(e.b,0)),a:r}}var pt="(?:[-\\+]?\\d*\\.\\d+%?)|(?:[-\\+]?\\d+%?)",ft="[\\s|\\(]+("+pt+")[,|\\s]+("+pt+")[,|\\s]+("+pt+")\\s*\\)?",gt="[\\s|\\(]+("+pt+")[,|\\s]+("+pt+")[,|\\s]+("+pt+")[,|\\s]+("+pt+")\\s*\\)?",mt={CSS_UNIT:new RegExp(pt),rgb:new RegExp("rgb"+ft),rgba:new RegExp("rgba"+gt),hsl:new RegExp("hsl"+ft),hsla:new RegExp("hsla"+gt),hsv:new RegExp("hsv"+ft),hsva:new RegExp("hsva"+gt),hex3:/^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,hex6:/^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/,hex4:/^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/,hex8:/^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/};function bt(t){return Boolean(mt.CSS_UNIT.exec(String(t)))}var yt=function(){function t(e,r){var i;if(void 0===e&&(e=""),void 0===r&&(r={}),e instanceof t)return e;this.originalInput=e;var s=ut(e);this.originalInput=e,this.r=s.r,this.g=s.g,this.b=s.b,this.a=s.a,this.roundA=Math.round(100*this.a)/100,this.format=null!=(i=r.format)?i:s.format,this.gradientType=r.gradientType,this.r<1&&(this.r=Math.round(this.r)),this.g<1&&(this.g=Math.round(this.g)),this.b<1&&(this.b=Math.round(this.b)),this.isValid=s.ok}return t.prototype.isDark=function(){return this.getBrightness()<128},t.prototype.isLight=function(){return!this.isDark()},t.prototype.getBrightness=function(){var t=this.toRgb();return(299*t.r+587*t.g+114*t.b)/1e3},t.prototype.getLuminance=function(){var t=this.toRgb(),e=t.r/255,r=t.g/255,i=t.b/255;return.2126*(e<=.03928?e/12.92:Math.pow((e+.055)/1.055,2.4))+.7152*(r<=.03928?r/12.92:Math.pow((r+.055)/1.055,2.4))+.0722*(i<=.03928?i/12.92:Math.pow((i+.055)/1.055,2.4))},t.prototype.getAlpha=function(){return this.a},t.prototype.setAlpha=function(t){return this.a=et(t),this.roundA=Math.round(100*this.a)/100,this},t.prototype.toHsv=function(){var t=ot(this.r,this.g,this.b);return{h:360*t.h,s:t.s,v:t.v,a:this.a}},t.prototype.toHsvString=function(){var t=ot(this.r,this.g,this.b),e=Math.round(360*t.h),r=Math.round(100*t.s),i=Math.round(100*t.v);return 1===this.a?"hsv("+e+", "+r+"%, "+i+"%)":"hsva("+e+", "+r+"%, "+i+"%, "+this.roundA+")"},t.prototype.toHsl=function(){var t=st(this.r,this.g,this.b);return{h:360*t.h,s:t.s,l:t.l,a:this.a}},t.prototype.toHslString=function(){var t=st(this.r,this.g,this.b),e=Math.round(360*t.h),r=Math.round(100*t.s),i=Math.round(100*t.l);return 1===this.a?"hsl("+e+", "+r+"%, "+i+"%)":"hsla("+e+", "+r+"%, "+i+"%, "+this.roundA+")"},t.prototype.toHex=function(t){return void 0===t&&(t=!1),at(this.r,this.g,this.b,t)},t.prototype.toHexString=function(t){return void 0===t&&(t=!1),"#"+this.toHex(t)},t.prototype.toHex8=function(t){return void 0===t&&(t=!1),function(t,e,r,i,s){var n=[it(Math.round(t).toString(16)),it(Math.round(e).toString(16)),it(Math.round(r).toString(16)),it(ht(i))];return s&&n[0].startsWith(n[0].charAt(1))&&n[1].startsWith(n[1].charAt(1))&&n[2].startsWith(n[2].charAt(1))&&n[3].startsWith(n[3].charAt(1))?n[0].charAt(0)+n[1].charAt(0)+n[2].charAt(0)+n[3].charAt(0):n.join("")}(this.r,this.g,this.b,this.a,t)},t.prototype.toHex8String=function(t){return void 0===t&&(t=!1),"#"+this.toHex8(t)},t.prototype.toRgb=function(){return{r:Math.round(this.r),g:Math.round(this.g),b:Math.round(this.b),a:this.a}},t.prototype.toRgbString=function(){var t=Math.round(this.r),e=Math.round(this.g),r=Math.round(this.b);return 1===this.a?"rgb("+t+", "+e+", "+r+")":"rgba("+t+", "+e+", "+r+", "+this.roundA+")"},t.prototype.toPercentageRgb=function(){var t=function(t){return Math.round(100*X(t,255))+"%"};return{r:t(this.r),g:t(this.g),b:t(this.b),a:this.a}},t.prototype.toPercentageRgbString=function(){var t=function(t){return Math.round(100*X(t,255))};return 1===this.a?"rgb("+t(this.r)+"%, "+t(this.g)+"%, "+t(this.b)+"%)":"rgba("+t(this.r)+"%, "+t(this.g)+"%, "+t(this.b)+"%, "+this.roundA+")"},t.prototype.toName=function(){if(0===this.a)return"transparent";if(this.a<1)return!1;for(var t="#"+at(this.r,this.g,this.b,!1),e=0,r=Object.keys(dt);e<r.length;e++){var i=r[e];if(dt[i]===t)return i}return!1},t.prototype.toString=function(t){var e=Boolean(t);t=null!=t?t:this.format;var r=!1,i=this.a<1&&this.a>=0;return e||!i||!t.startsWith("hex")&&"name"!==t?("rgb"===t&&(r=this.toRgbString()),"prgb"===t&&(r=this.toPercentageRgbString()),"hex"!==t&&"hex6"!==t||(r=this.toHexString()),"hex3"===t&&(r=this.toHexString(!0)),"hex4"===t&&(r=this.toHex8String(!0)),"hex8"===t&&(r=this.toHex8String()),"name"===t&&(r=this.toName()),"hsl"===t&&(r=this.toHslString()),"hsv"===t&&(r=this.toHsvString()),r||this.toHexString()):"name"===t&&0===this.a?this.toName():this.toRgbString()},t.prototype.clone=function(){return new t(this.toString())},t.prototype.lighten=function(e){void 0===e&&(e=10);var r=this.toHsl();return r.l+=e/100,r.l=tt(r.l),new t(r)},t.prototype.brighten=function(e){void 0===e&&(e=10);var r=this.toRgb();return r.r=Math.max(0,Math.min(255,r.r-Math.round(-e/100*255))),r.g=Math.max(0,Math.min(255,r.g-Math.round(-e/100*255))),r.b=Math.max(0,Math.min(255,r.b-Math.round(-e/100*255))),new t(r)},t.prototype.darken=function(e){void 0===e&&(e=10);var r=this.toHsl();return r.l-=e/100,r.l=tt(r.l),new t(r)},t.prototype.tint=function(t){return void 0===t&&(t=10),this.mix("white",t)},t.prototype.shade=function(t){return void 0===t&&(t=10),this.mix("black",t)},t.prototype.desaturate=function(e){void 0===e&&(e=10);var r=this.toHsl();return r.s-=e/100,r.s=tt(r.s),new t(r)},t.prototype.saturate=function(e){void 0===e&&(e=10);var r=this.toHsl();return r.s+=e/100,r.s=tt(r.s),new t(r)},t.prototype.greyscale=function(){return this.desaturate(100)},t.prototype.spin=function(e){var r=this.toHsl(),i=(r.h+e)%360;return r.h=i<0?360+i:i,new t(r)},t.prototype.mix=function(e,r){void 0===r&&(r=50);var i=this.toRgb(),s=new t(e).toRgb(),n=r/100;return new t({r:(s.r-i.r)*n+i.r,g:(s.g-i.g)*n+i.g,b:(s.b-i.b)*n+i.b,a:(s.a-i.a)*n+i.a})},t.prototype.analogous=function(e,r){void 0===e&&(e=6),void 0===r&&(r=30);var i=this.toHsl(),s=360/r,n=[this];for(i.h=(i.h-(s*e>>1)+720)%360;--e;)i.h=(i.h+s)%360,n.push(new t(i));return n},t.prototype.complement=function(){var e=this.toHsl();return e.h=(e.h+180)%360,new t(e)},t.prototype.monochromatic=function(e){void 0===e&&(e=6);for(var r=this.toHsv(),i=r.h,s=r.s,n=r.v,o=[],a=1/e;e--;)o.push(new t({h:i,s:s,v:n})),n=(n+a)%1;return o},t.prototype.splitcomplement=function(){var e=this.toHsl(),r=e.h;return[this,new t({h:(r+72)%360,s:e.s,l:e.l}),new t({h:(r+216)%360,s:e.s,l:e.l})]},t.prototype.triad=function(){return this.polyad(3)},t.prototype.tetrad=function(){return this.polyad(4)},t.prototype.polyad=function(e){for(var r=this.toHsl(),i=r.h,s=[this],n=360/e,o=1;o<e;o++)s.push(new t({h:(i+o*n)%360,s:r.s,l:r.l}));return s},t.prototype.equals=function(e){return this.toRgbString()===new t(e).toRgbString()},t}();function vt(t,e){return void 0===t&&(t=""),void 0===e&&(e={}),new yt(t,e)}function wt(t,e,r=null){if((t=new Event(t,{bubbles:!0,cancelable:!1,composed:!0})).detail=e||{},r)r.dispatchEvent(t);else{var i=function(){var t=document.querySelector("hc-main");return t=t?(t=(t=(t=t&&t.shadowRoot)&&t.querySelector("hc-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-view"):(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=document.querySelector("home-assistant"))&&t.shadowRoot)&&t.querySelector("home-assistant-main"))&&t.shadowRoot)&&t.querySelector("app-drawer-layout partial-panel-resolver"))&&t.shadowRoot||t)&&t.querySelector("ha-panel-lovelace"))&&t.shadowRoot)&&t.querySelector("hui-root"))&&t.shadowRoot)&&t.querySelector("ha-app-layout #view"))&&t.firstElementChild}();i&&i.dispatchEvent(t)}}const _t=customElements.get("home-assistant-main")?Object.getPrototypeOf(customElements.get("home-assistant-main")):Object.getPrototypeOf(customElements.get("hui-view")),St=_t.prototype.html;_t.prototype.css;let xt=window.cardHelpers;const Ct=new Promise(async(t,e)=>{xt&&t(),window.loadCardHelpers&&(xt=await window.loadCardHelpers(),window.cardHelpers=xt,t())});function Mt(t,e){const r=document.createElement("hui-error-card");return r.setConfig({type:"error",error:t,origConfig:e}),r}function kt(t,e){if(!e||"object"!=typeof e||!e.type)return Mt(`No ${t} type configured`,e);let r=e.type;if(r=r.startsWith("custom:")?r.substr("custom:".length):`hui-${r}-${t}`,customElements.get(r))return function(t,e){let r=document.createElement(t);try{r.setConfig(JSON.parse(JSON.stringify(e)))}catch(t){r=Mt(t,e)}return Ct.then(()=>{wt("ll-rebuild",{},r)}),r}(r,e);const i=Mt(`Custom element doesn't exist: ${r}.`,e);i.style.display="None";const s=setTimeout(()=>{i.style.display=""},2e3);return customElements.whenDefined(r).then(()=>{clearTimeout(s),wt("ll-rebuild",{},i)}),i}class Pt extends _t{static get version(){return 2}static get properties(){return{noHass:{type:Boolean}}}setConfig(t){var e;this._config=t,this.el?this.el.setConfig(t):(this.el=this.create(t),this._hass&&(this.el.hass=this._hass),this.noHass&&(e=this,document.querySelector("hc-main")?document.querySelector("hc-main").provideHass(e):document.querySelector("home-assistant")&&document.querySelector("home-assistant").provideHass(e)))}set config(t){this.setConfig(t)}set hass(t){this._hass=t,this.el&&(this.el.hass=t)}createRenderRoot(){return this}render(){return St`${this.el}`}}const Nt=function(t,e){const r=Object.getOwnPropertyDescriptors(e.prototype);for(const[e,i]of Object.entries(r))"constructor"!==e&&Object.defineProperty(t.prototype,e,i);const i=Object.getOwnPropertyDescriptors(e);for(const[e,r]of Object.entries(i))"prototype"!==e&&Object.defineProperty(t,e,r);const s=Object.getPrototypeOf(e),n=Object.getOwnPropertyDescriptors(s.prototype);for(const[e,r]of Object.entries(n))"constructor"!==e&&Object.defineProperty(Object.getPrototypeOf(t).prototype,e,r);const o=Object.getOwnPropertyDescriptors(s);for(const[e,r]of Object.entries(o))"prototype"!==e&&Object.defineProperty(Object.getPrototypeOf(t),e,r)},At=customElements.get("card-maker");if(!At||!At.version||At.version<2){class t extends Pt{create(t){return function(t){return xt?xt.createCardElement(t):kt("card",t)}(t)}getCardSize(){return this.firstElementChild&&this.firstElementChild.getCardSize?this.firstElementChild.getCardSize():1}}At?Nt(At,t):customElements.define("card-maker",t)}const Et=customElements.get("element-maker");if(!Et||!Et.version||Et.version<2){class t extends Pt{create(t){return function(t){return xt?xt.createHuiElement(t):kt("element",t)}(t)}}Et?Nt(Et,t):customElements.define("element-maker",t)}const $t=customElements.get("entity-row-maker");if(!$t||!$t.version||$t.version<2){class t extends Pt{create(t){return function(t){if(xt)return xt.createRowElement(t);const e=new Set(["call-service","cast","conditional","divider","section","select","weblink"]);if(!t)return Mt("Invalid configuration given.",t);if("string"==typeof t&&(t={entity:t}),"object"!=typeof t||!t.entity&&!t.type)return Mt("Invalid configuration given.",t);const r=t.type||"default";return e.has(r)||r.startsWith("custom:")?kt("row",t):kt("entity-row",{type:{alert:"toggle",automation:"toggle",climate:"climate",cover:"cover",fan:"toggle",group:"group",input_boolean:"toggle",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",remote:"toggle",scene:"scene",script:"script",sensor:"sensor",timer:"timer",switch:"toggle",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime"}[t.entity.split(".",1)[0]]||"text",...t})}(t)}}$t?Nt($t,t):customElements.define("entity-row-maker",t)}var Ot={},Tt=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,Rt="[^\\s]+",Ht=/\[([^]*?)\]/gm,Ft=function(){};function Dt(t,e){for(var r=[],i=0,s=t.length;i<s;i++)r.push(t[i].substr(0,e));return r}function Vt(t){return function(e,r,i){var s=i[t].indexOf(r.charAt(0).toUpperCase()+r.substr(1).toLowerCase());~s&&(e.month=s)}}function jt(t,e){for(t=String(t),e=e||2;t.length<e;)t="0"+t;return t}var qt=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],zt=["January","February","March","April","May","June","July","August","September","October","November","December"],Bt=Dt(zt,3),Yt=Dt(qt,3);Ot.i18n={dayNamesShort:Yt,dayNames:qt,monthNamesShort:Bt,monthNames:zt,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10)*t%10]}};var It={D:function(t){return t.getDate()},DD:function(t){return jt(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return t.getDay()},dd:function(t){return jt(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return t.getMonth()+1},MM:function(t){return jt(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return jt(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return jt(t.getFullYear(),4)},h:function(t){return t.getHours()%12||12},hh:function(t){return jt(t.getHours()%12||12)},H:function(t){return t.getHours()},HH:function(t){return jt(t.getHours())},m:function(t){return t.getMinutes()},mm:function(t){return jt(t.getMinutes())},s:function(t){return t.getSeconds()},ss:function(t){return jt(t.getSeconds())},S:function(t){return Math.round(t.getMilliseconds()/100)},SS:function(t){return jt(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return jt(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+jt(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)}},Lt={D:["\\d\\d?",function(t,e){t.day=e}],Do:["\\d\\d?"+Rt,function(t,e){t.day=parseInt(e,10)}],M:["\\d\\d?",function(t,e){t.month=e-1}],YY:["\\d\\d?",function(t,e){var r=+(""+(new Date).getFullYear()).substr(0,2);t.year=""+(e>68?r-1:r)+e}],h:["\\d\\d?",function(t,e){t.hour=e}],m:["\\d\\d?",function(t,e){t.minute=e}],s:["\\d\\d?",function(t,e){t.second=e}],YYYY:["\\d{4}",function(t,e){t.year=e}],S:["\\d",function(t,e){t.millisecond=100*e}],SS:["\\d{2}",function(t,e){t.millisecond=10*e}],SSS:["\\d{3}",function(t,e){t.millisecond=e}],d:["\\d\\d?",Ft],ddd:[Rt,Ft],MMM:[Rt,Vt("monthNamesShort")],MMMM:[Rt,Vt("monthNames")],a:[Rt,function(t,e,r){var i=e.toLowerCase();i===r.amPm[0]?t.isPm=!1:i===r.amPm[1]&&(t.isPm=!0)}],ZZ:["[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z",function(t,e){var r,i=(e+"").match(/([+-]|\d\d)/gi);i&&(r=60*i[1]+parseInt(i[2],10),t.timezoneOffset="+"===i[0]?r:-r)}]};Lt.dd=Lt.d,Lt.dddd=Lt.ddd,Lt.DD=Lt.D,Lt.mm=Lt.m,Lt.hh=Lt.H=Lt.HH=Lt.h,Lt.MM=Lt.M,Lt.ss=Lt.s,Lt.A=Lt.a,Ot.masks={default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"},Ot.format=function(t,e,r){var i=r||Ot.i18n;if("number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date in fecha.format");e=Ot.masks[e]||e||Ot.masks.default;var s=[];return(e=(e=e.replace(Ht,(function(t,e){return s.push(e),"@@@"}))).replace(Tt,(function(e){return e in It?It[e](t,i):e.slice(1,e.length-1)}))).replace(/@@@/g,(function(){return s.shift()}))},Ot.parse=function(t,e,r){var i=r||Ot.i18n;if("string"!=typeof e)throw new Error("Invalid format in fecha.parse");if(e=Ot.masks[e]||e,t.length>1e3)return null;var s={},n=[],o=[];e=e.replace(Ht,(function(t,e){return o.push(e),"@@@"}));var a,h=(a=e,a.replace(/[|\\{()[^$+*?.-]/g,"\\$&")).replace(Tt,(function(t){if(Lt[t]){var e=Lt[t];return n.push(e[1]),"("+e[0]+")"}return t}));h=h.replace(/@@@/g,(function(){return o.shift()}));var c=t.match(new RegExp(h,"i"));if(!c)return null;for(var l=1;l<c.length;l++)n[l-1](s,c[l],i);var d,u=new Date;return!0===s.isPm&&null!=s.hour&&12!=+s.hour?s.hour=+s.hour+12:!1===s.isPm&&12==+s.hour&&(s.hour=0),null!=s.timezoneOffset?(s.minute=+(s.minute||0)-+s.timezoneOffset,d=new Date(Date.UTC(s.year||u.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0))):d=new Date(s.year||u.getFullYear(),s.month||0,s.day||1,s.hour||0,s.minute||0,s.second||0,s.millisecond||0),d};var Ut=function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}return!1}()?function(t,e){return t.toLocaleDateString(e,{year:"numeric",month:"long",day:"numeric"})}:function(t){return Ot.format(t,"mediumDate")},Wt=function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}return!1}()?function(t,e){return t.toLocaleString(e,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"})}:function(t){return Ot.format(t,"haDateTime")},Jt=function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}return!1}()?function(t,e){return t.toLocaleTimeString(e,{hour:"numeric",minute:"2-digit"})}:function(t){return Ot.format(t,"shortTime")};function Zt(t,e,r){var i,s=function(t){return function(t){return t.substr(0,t.indexOf("."))}(t.entity_id)}(e);if("binary_sensor"===s)e.attributes.device_class&&(i=t("state."+s+"."+e.attributes.device_class+"."+e.state)),i||(i=t("state."+s+".default."+e.state));else if(e.attributes.unit_of_measurement&&!["unknown","unavailable"].includes(e.state))i=e.state+" "+e.attributes.unit_of_measurement;else if("input_datetime"===s){var n;if(e.attributes.has_time)if(e.attributes.has_date)n=new Date(e.attributes.year,e.attributes.month-1,e.attributes.day,e.attributes.hour,e.attributes.minute),i=Wt(n,r);else{var o=new Date;n=new Date(o.getFullYear(),o.getMonth(),o.getDay(),e.attributes.hour,e.attributes.minute),i=Jt(n,r)}else n=new Date(e.attributes.year,e.attributes.month-1,e.attributes.day),i=Ut(n,r)}else i="zwave"===s?["initializing","dead"].includes(e.state)?t("state.zwave.query_stage."+e.state,"query_stage",e.attributes.query_stage):t("state.zwave.default."+e.state):t("state."+s+"."+e.state);return i||(i=t("state.default."+e.state)||t("component."+s+".state."+e.state)||e.state),i}customElements.define("light-popup-card",class extends Q{constructor(){super(),this.actionRows=[],this.currentBrightness=0,this.settings=!1,this.settingsCustomCard=!1,this.settingsPosition="bottom"}static get properties(){return{hass:{},config:{},active:{}}}render(){var t=this.config.entity,e=this.hass.states[t],r=this.config.actionsInARow?this.config.actionsInARow:4;e.attributes.brightness&&e.attributes.brightness;var i=this.config.icon?this.config.icon:e.attributes.icon?e.attributes.icon:"mdi:lightbulb",s=this.config.borderRadius?this.config.borderRadius:"12px",n=this.config.supportedFeaturesTreshold?this.config.supportedFeaturesTreshold:9,o="actionSize"in this.config?this.config.actionSize:"50px",a=this.config.actions;if(a&&a.length>0)for(var h=Math.ceil(a.length/r),c=0;c<h;c++){this.actionRows[c]=[];for(var l=0;l<r;l++)a[c*r+l]&&(this.actionRows[c][l]=a[c*r+l])}var d=0;switch(e.state){case"on":d=1;break;case"off":d=0;break;default:d=0}var u=!("fullscreen"in this.config)||this.config.fullscreen,p=this.config.brightnessWidth?this.config.brightnessWidth:"150px",f=this.config.brightnessHeight?this.config.brightnessHeight:"400px",g=this.config.switchWidth?this.config.switchWidth:"380px",m=this.config.switchHeight?this.config.switchHeight:"150px",b=this._getColorForLightEntity(e,this.config.useTemperature,this.config.useBrightness),y="sliderColor"in this.config?this.config.sliderColor:"#FFF",v="sliderColoredByLight"in this.config&&this.config.sliderColoredByLight,w="sliderThumbColor"in this.config?this.config.sliderThumbColor:"#ddd",_="sliderTrackColor"in this.config?this.config.sliderTrackColor:"#ddd",S=0;if(this.currentBrightness=Math.round(e.attributes.brightness/2.55),this.settings="settings"in this.config,this.settingsCustomCard="settingsCard"in this.config,this.settingsPosition="settingsPosition"in this.config?this.config.settingsPosition:"bottom",this.settingsCustomCard&&this.config.settingsCard.cardOptions)if(this.config.settingsCard.cardOptions.entity&&"this"==this.config.settingsCard.cardOptions.entity)this.config.settingsCard.cardOptions.entity=t;else if(this.config.settingsCard.cardOptions.entity_id&&"this"==this.config.settingsCard.cardOptions.entity_id)this.config.settingsCard.cardOptions.entity_id=t;else if(this.config.settingsCard.cardOptions.entities)for(let e in this.config.settingsCard.cardOptions.entities)"this"==this.config.settingsCard.cardOptions.entities[e]&&(this.config.settingsCard.cardOptions.entities[e]=t);return O`
      <div class="${!0===u?"popup-wrapper":""}">
            <div id="popup" class="popup-inner" @click="${t=>this._close(t)}">
                <div class="icon${!0===u?" fullscreen":""}">
                    <ha-icon style="${"on"===e.state?"fill:"+b+";":""}" icon="${i}" />
                </div>
                ${e.attributes.supported_features>n?O`
                    <h4 id="brightnessValue" class="${"off"===e.state?"":"brightness"}" data-value="${this.currentBrightness}%">${"off"===e.state?Zt(this.hass.localize,e,this.hass.language):""}</h4>
                    <div class="range-holder" style="--slider-height: ${f};--slider-width: ${p};">
                        <input type="range" style="--slider-width: ${p};--slider-height: ${f}; --slider-border-radius: ${s};${v?"--slider-color:"+b+";":"--slider-color:"+y+";"}--slider-thumb-color:${w};--slider-track-color:${_};" .value="${"off"===e.state?0:Math.round(e.attributes.brightness/2.55)}" @input=${t=>this._previewBrightness(t.target.value)} @change=${t=>this._setBrightness(e,t.target.value)}>
                    </div>
                `:O`
                    <h4>${Zt(this.hass.localize,e,this.hass.language)}</h4>
                    <div class="switch-holder" style="--switch-height: ${m};--switch-width: ${g};">
                        <input type="range" style="--switch-width: ${g};--switch-height: ${m}; --slider-border-radius: ${s}" value="0" min="0" max="1" .value="${d}" @change=${()=>this._switch(e)}>
                    </div>
                `}

                ${a&&a.length>0?O`
                <div class="action-holder">

                    ${this.actionRows.map(t=>{S++;var e=0;return O`
                        <div class="action-row">
                        ${t.map(t=>(e++,O`
                            <div class="action" style="--size:${o};" @click="${t=>this._activateAction(t)}" data-service="${S}#${e}">
                                <span class="color" style="background-color: ${t.color};border-color: ${t.color};--size:${o};">${t.icon?O`<ha-icon icon="${t.icon}" />`:O``}</span>
                                ${t.name?O`<span class="name">${t.name}</span>`:O``}
                            </div>
                          `))}
                        </div>
                      `})}
                </div>`:O``}
                ${this.settings?O`<button class="settings-btn ${this.settingsPosition}${!0===u?" fullscreen":""}" @click="${()=>this._openSettings()}">${this.config.settings.openButton?this.config.settings.openButton:"Settings"}</button>`:O``}
            </div>
            
            ${this.settings?O`
              <div id="settings" class="settings-inner" @click="${t=>this._close(t)}">
                ${this.settingsCustomCard?O`
                  <card-maker nohass data-card="${this.config.settingsCard.type}" data-options="${JSON.stringify(this.config.settingsCard.cardOptions)}" data-style="${this.config.settingsCard.cardStyle?this.config.settingsCard.cardStyle:""}">
                  </card-maker>
                `:O`
                    <more-info-controls
                    .dialogElement=${null}
                    .canConfigure=${!1}
                    .hass=${this.hass}
                    .stateObj=${e}
                    style="--paper-slider-knob-color: white !important;
                    --paper-slider-knob-start-color: white !important;
                    --paper-slider-pin-color: white !important;
                    --paper-slider-active-color: white !important;
                    color: white !important;
                    --primary-text-color: white !important;"
                  ></more-info-controls>
                `}
                <button class="settings-btn ${this.settingsPosition}${!0===u?" fullscreen":""}" @click="${()=>this._closeSettings()}">${this.config.settings.closeButton?this.config.settings.closeButton:"Close"}</button>
              </div>
            `:O``}
        </div>
    `}updated(){}firstUpdated(){if(this.settings&&!this.settingsCustomCard){const t=this.shadowRoot.querySelector("more-info-controls").shadowRoot;t.removeChild(t.querySelector("app-toolbar"))}else this.settings&&this.settingsCustomCard&&this.shadowRoot.querySelectorAll("card-maker").forEach(t=>{var e={type:t.dataset.card};e=Object.assign({},e,JSON.parse(t.dataset.options)),t.config=e;let r="";if(t.dataset.style&&(r=t.dataset.style),""!=r){let e=0,i=setInterval((function(){let s=t.children[0];if(s){window.clearInterval(i);var n=document.createElement("style");n.innerHTML=r,s.shadowRoot.appendChild(n)}else 10==++e&&window.clearInterval(i)}),100)}})}_close(t){t&&(t.target.className.includes("popup-inner")||t.target.className.includes("settings-inner"))&&function(){const t=document.querySelector("hc-main")||document.querySelector("home-assistant"),e=t&&t._moreInfoEl;e&&e.close()}()}_openSettings(){this.shadowRoot.getElementById("popup").classList.add("off"),this.shadowRoot.getElementById("settings").classList.add("on")}_closeSettings(){this.shadowRoot.getElementById("settings").classList.remove("on"),this.shadowRoot.getElementById("popup").classList.remove("off")}_createRange(t){const e=[];for(let r=0;r<t;r++)e.push(r);return e}_previewBrightness(t){this.currentBrightness=t;const e=this.shadowRoot.getElementById("brightnessValue");e&&(e.dataset.value=t+"%")}_setBrightness(t,e){this.hass.callService("homeassistant","turn_on",{entity_id:t.entity_id,brightness:2.55*e})}_switch(t){this.hass.callService("homeassistant","toggle",{entity_id:t.entity_id})}_activateAction(t){if(t.target.dataset&&t.target.dataset.service){const[e,r]=t.target.dataset.service.split("#",2),i=this.actionRows[e-1][r-1],[s,n]=i.service.split(".",2);this.hass.callService(s,n,i.service_data)}}_getColorForLightEntity(t,e,r){var i=this.config.default_color?this.config.default_color:void 0;return t&&(t.attributes.rgb_color?(i=`rgb(${t.attributes.rgb_color.join(",")})`,t.attributes.brightness&&(i=this._applyBrightnessToColor(i,(t.attributes.brightness+245)/5))):e&&t.attributes.color_temp&&t.attributes.min_mireds&&t.attributes.max_mireds?(i=this._getLightColorBasedOnTemperature(t.attributes.color_temp,t.attributes.min_mireds,t.attributes.max_mireds),t.attributes.brightness&&(i=this._applyBrightnessToColor(i,(t.attributes.brightness+245)/5))):i=r&&t.attributes.brightness?this._applyBrightnessToColor(this._getDefaultColorForState(),(t.attributes.brightness+245)/5):this._getDefaultColorForState()),i}_applyBrightnessToColor(t,e){const r=new yt(this._getColorFromVariable(t));if(r.isValid){const t=r.mix("black",100-e).toString();if(t)return t}return t}_getLightColorBasedOnTemperature(t,e,r){const i=new yt("rgb(255, 160, 0)"),s=new yt("rgb(166, 209, 255)"),n=new yt("white"),o=(t-e)/(r-e)*100;return o<50?vt(s).mix(n,2*o).toRgbString():vt(n).mix(i,2*(o-50)).toRgbString()}_getDefaultColorForState(){return this.config.color_on?this.config.color_on:"#f7d959"}_getColorFromVariable(t){return void 0!==t&&"var"===t.substring(0,3)?window.getComputedStyle(document.documentElement).getPropertyValue(t.substring(4).slice(0,-1)).trim():t}setConfig(t){if(!t.entity)throw new Error("You need to define an entity");this.config=t}getCardSize(){return this.config.entities.length+1}static get styles(){return G`
        :host {
            background-color:#000!important;
        }
        .popup-wrapper {
            margin-top:64px;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
        .popup-inner {
            height: 100%;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        .popup-inner.off {
          display:none;
        }
        #settings {
          display:none;
        }
        .settings-inner {
          height: 100%;
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-direction: column;
        }
        #settings.on {
          display:flex;
        }
        .settings-btn {
          position:absolute;
          right:30px;
          background-color: #7f8082;
          color: #FFF;
          border: 0;
          padding: 5px 20px;
          border-radius: 10px;
          font-weight: 500;
          cursor: pointer;
        }
        .settings-btn.bottom {
          bottom:15px;
        }
        .settings-btn.bottom.fullscreen {
          margin:0;
        }
        .settings-btn.top {
          top: 25px;
        }
        .fullscreen {
          margin-top:-64px;
        }
        .icon {
            text-align:center;
            display:block;
            height: 40px;
            width: 40px;
            color: rgba(255,255,255,0.3);
            font-size: 30px;
            padding-top:5px;
        }
        .icon ha-icon {
            width:30px;
            height:30px;
        }
        .icon.on ha-icon {
            fill: #f7d959;
        }
        h4 {
            color: #FFF;
            display: block;
            font-weight: 300;
            margin-bottom: 30px;
            text-align: center;
            font-size:20px;
            margin-top:0;
            text-transform: capitalize;
        }
        h4.brightness:after {
            content: attr(data-value);
            padding-left: 1px;
        }
        
        .range-holder {
            height: var(--slider-height);
            width: var(--slider-width);
            position:relative;
            display: block;
        }
        .range-holder input[type="range"] {
            outline: 0;
            border: 0;
            border-radius: var(--slider-border-radius, 12px);
            width: var(--slider-height);
            margin: 0;
            transition: box-shadow 0.2s ease-in-out;
            -webkit-transform:rotate(270deg);
            -moz-transform:rotate(270deg);
            -o-transform:rotate(270deg);
            -ms-transform:rotate(270deg);
            transform:rotate(270deg);
            overflow: hidden;
            height: var(--slider-width);
            -webkit-appearance: none;
            background-color: var(--slider-track-color);
            position: absolute;
            top: calc(50% - (var(--slider-width) / 2));
            right: calc(50% - (var(--slider-height) / 2));
        }
        .range-holder input[type="range"]::-webkit-slider-runnable-track {
            height: var(--slider-width);
            -webkit-appearance: none;
            background-color: var(--slider-track-color);
            margin-top: -1px;
            transition: box-shadow 0.2s ease-in-out;
        }
        .range-holder input[type="range"]::-webkit-slider-thumb {
            width: 25px;
            border-right:10px solid var(--slider-color);
            border-left:10px solid var(--slider-color);
            border-top:20px solid var(--slider-color);
            border-bottom:20px solid var(--slider-color);
            -webkit-appearance: none;
            height: 80px;
            cursor: ew-resize;
            background: #fff;
            box-shadow: -350px 0 0 350px var(--slider-color), inset 0 0 0 80px var(--slider-thumb-color);
            border-radius: 0;
            transition: box-shadow 0.2s ease-in-out;
            position: relative;
            top: calc((var(--slider-width) - 80px) / 2);
        }
        .switch-holder {
            height: var(--switch-height);
            width: var(--switch-width);
            position:relative;
            display: block;
        }
        .switch-holder input[type="range"] {
            outline: 0;
            border: 0;
            border-radius: var(--slider-border-radius, 12px);
            width: calc(var(--switch-height) - 20px);
            margin: 0;
            transition: box-shadow 0.2s ease-in-out;
            -webkit-transform: rotate(270deg);
            -moz-transform: rotate(270deg);
            -o-transform: rotate(270deg);
            -ms-transform: rotate(270deg);
            transform: rotate(270deg);
            overflow: hidden;
            height: calc(var(--switch-width) - 20px);
            -webkit-appearance: none;
            background-color: #ddd;
            padding: 10px;
            position: absolute;
            top: calc(50% - (var(--switch-width) / 2));
            right: calc(50% - (var(--switch-height) / 2));
        }
        .switch-holder input[type="range"]::-webkit-slider-runnable-track {
            height: calc(var(--switch-width) - 20px);
            -webkit-appearance: none;
            color: #ddd;
            margin-top: -1px;
            transition: box-shadow 0.2s ease-in-out;
        }
        .switch-holder input[type="range"]::-webkit-slider-thumb {
            width: calc(var(--switch-height) / 2);
            -webkit-appearance: none;
            height: calc(var(--switch-width) - 20px);
            cursor: ew-resize;
            background: #fff;
            transition: box-shadow 0.2s ease-in-out;
            border: none;
            box-shadow: -1px 1px 20px 0px rgba(0,0,0,0.75);
            position: relative;
            top: 0;
            border-radius: var(--slider-border-radius, 12px);
        }
        
        .action-holder {
            display: flex;
            flex-direction: column;
            margin-top:20px;
        }
        .action-row {
            display:block;
            padding-bottom:10px;
        }
        .action-row:last-child {
            padding:0;
        }
        .action-holder .action {
            display:inline-block;
            margin-right:10px;
            cursor:pointer;
        }
        .action-holder .action:nth-child(4n) {
            margin-right:0;
        }
        .action-holder .action .color {
            width:var(--size);
            height:var(--size);
            border-radius:50%;
            display:block;
            border: 1px solid #FFF;
            line-height: var(--size);
            text-align: center;
            pointer-events: none;
        }
        .action-holder .action .color ha-icon {
          pointer-events: none;
        }
        .action-holder .action .name {
            width:var(--size);
            display:block;
            color: #FFF;
            font-size: 9px;
            margin-top:3px;
            text-align:center;
            pointer-events: none;
        }
    `}});
