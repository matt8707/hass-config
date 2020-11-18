"use strict";function e(e,r){return o(e)||n(e,r)||d(e,r)||t()}function t(){throw new TypeError(
"Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}
function n(e,r){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e)){var t=[],n=!0,o=!1,a=void 0;try{for(var i,l=e[Symbol.iterator]();!(n=(
i=l.next()).done)&&(t.push(i.value),!r||t.length!==r);n=!0);}catch(e){o=!0,a=e}finally{try{n||null==l.return||l.return()}finally{if(o)throw a}}
return t}}function o(e){if(Array.isArray(e))return e}function r(e){return l(e)||i(e)||d(e)||a()}function a(){throw new TypeError(
"Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function i(e){
if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}function l(e){if(Array.isArray(e))return c(e)}function f(e,r){var t
;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(t=d(e))||r&&e&&"number"==typeof e.length){t&&(e=t);var n=0,r=function(
){};return{s:r,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:r}}throw new TypeError(
"Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,
i=!1;return{s:function(){t=e[Symbol.iterator]()},n:function(){var e=t.next();return a=e.done,e},e:function(e){i=!0,o=e},f:function(){try{
a||null==t.return||t.return()}finally{if(i)throw o}}}}function d(e,r){if(e){if("string"==typeof e)return c(e,r);var t=Object.prototype.toString.call(e
).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e
):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?c(e,r):void 0}}function c(e,r){(null==r||r>e.length)&&(r=e.length);for(var t=0,
n=new Array(r);t<r;t++)n[t]=e[t];return n}var h=document.querySelector("home-assistant"),y=h.shadowRoot.querySelector("home-assistant-main"
).shadowRoot,s=y.querySelector("partial-panel-resolver"),v=y.querySelector("app-drawer-layout");function m(){var e=y.querySelector("ha-panel-lovelace"
);return e&&e.lovelace.config.kiosk_mode?e.lovelace.config.kiosk_mode:{}}function p(e){var r=window.location.search;return e.some(function(e){
return r.includes(e)})}function b(e){return e&&!e.querySelector("#kiosk_mode")}function w(e,r){var t=document.createElement("style");t.setAttribute(
"id","kiosk_mode"),t.innerHTML=e,r.appendChild(t),window.dispatchEvent(new Event("resize"))}function k(e,r){window.localStorage.setItem(e,r)}
function S(e){return"true"==window.localStorage.getItem(e)}function u(){var e=window.location.search,r=h.hass;if(!e.includes("disable_km")){var t=S(
"kmHeader")||p(["kiosk","hide_header"]),n=S("kmSidebar")||p(["kiosk","hide_sidebar"]),o=m(),a=o.admin_settings,i=o.non_admin_settings,
l=o.user_settings,d=n||t,t=d?t:o.kiosk||o.hide_header,n=d?n:o.kiosk||o.hide_sidebar;if(a&&r.user.is_admin&&(t=a.kiosk||a.hide_header,
n=a.kiosk||a.hide_sidebar),i&&!r.user.is_admin&&(t=i.kiosk||i.hide_header,n=i.kiosk||i.hide_sidebar),l){Array.isArray(l)||(l=[l]);var c=f(l);try{for(
c.s();!(u=c.n()).done;){var s=u.value,u=s.users;Array.isArray(s.users)||(u=[u]),u.some(function(e){return e.toLowerCase()==r.user.name.toLowerCase()}
)&&(t=s.kiosk||s.hide_header,n=s.kiosk||s.hide_sidebar)}}catch(e){c.e(e)}finally{c.f()}}(n||t)&&(i=(l=(i=y.querySelector("ha-panel-lovelace")
)?i.shadowRoot.querySelector("hui-root").shadowRoot:null)?l.querySelector("app-toolbar"):null,t&&b(l)&&(w(
"#view { min-height: 100vh !important } app-header { display: none }",l),e.includes("cache")&&k("kmHeader","true")),n&&b(v)&&(w(
":host { --app-drawer-width: 0 !important } #drawer { display: none }",v),b(i)&&w("ha-menu-button { display:none !important } ",i),e.includes("cache"
)&&k("kmSidebar","true")))}}function g(e){var r,t=f(e);try{for(t.s();!(r=t.n()).done;){var n=f(r.value.addedNodes);try{for(n.s();!(o=n.n()).done;){
var o=o.value;if("ha-panel-lovelace"==o.localName)return void new MutationObserver(_).observe(o.shadowRoot,{childList:!0})}}catch(e){n.e(e)}finally{
n.f()}}}catch(e){t.e(e)}finally{t.f()}}function _(e){var r,t=f(e);try{for(t.s();!(r=t.n()).done;){var n=f(r.value.addedNodes);try{for(n.s();!(o=n.n()
).done;){var o=o.value;if("hui-root"==o.localName)return void new MutationObserver(x).observe(o.shadowRoot,{childList:!0})}}catch(e){n.e(e)}finally{
n.f()}}}catch(e){t.e(e)}finally{t.f()}}function x(e){var r,t=f(e);try{for(t.s();!(r=t.n()).done;){var n,o=f(r.value.addedNodes);try{for(o.s();!(n=o.n(
)).done;)if("ha-app-layout"==n.value.localName)return void u()}catch(e){o.e(e)}finally{o.f()}}}catch(e){t.e(e)}finally{t.f()}}
window.location.search.includes("clear_km_cache")&&["kmHeader","kmSidebar"].forEach(function(e){return k(e,"false")}),u(),new MutationObserver(g
).observe(s,{childList:!0});for(var A={header:"%c≡ kiosk-mode".padEnd(27),ver:"%cversion 1.4.5 "},j="%c\n",q=Math.max.apply(Math,r(Object.values(A
).map(function(e){return e.length}))),E=0,I=Object.entries(A);E<I.length;E++){var O=e(I[E],1),M=O[0];A[M].length<=q&&(A[M]=A[M].padEnd(q)),
"header"==M&&(A[M]="".concat(A[M].slice(0,-1),"⋮ "))}
var L="display:inline-block;border-width:1px 1px 0 1px;border-style:solid;border-color:#424242;color:white;background:#03a9f4;font-size:12px;padding:4px 4.5px 5px 6px;"
,N="border-width:0px 1px 1px 1px;padding:7px;background:white;color:#424242;line-height:0.7;";console.info(A.header+j+A.ver,L,"","".concat(L," "
).concat(N));