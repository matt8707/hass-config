"use strict";function e(e,t){return o(e)||r(e,t)||u(e,t)||n()}function n(){throw new TypeError(
"Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}
function r(e,t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e)){var n=[],r=!0,o=!1,i=void 0;try{for(var a,s=e[Symbol.iterator]();!(r=(
a=s.next()).done)&&(n.push(a.value),!t||n.length!==t);r=!0);}catch(e){o=!0,i=e}finally{try{r||null==s.return||s.return()}finally{if(o)throw i}}
return n}}function o(e){if(Array.isArray(e))return e}function t(e){return s(e)||a(e)||u(e)||i()}function i(){throw new TypeError(
"Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function a(e){
if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}function s(e){if(Array.isArray(e))return l(e)}function c(e,t,n,r,o,i,
a){try{var s=e[i](a),c=s.value}catch(e){return void n(e)}s.done?t(c):Promise.resolve(c).then(r,o)}function d(s){return function(){var e=this,
a=arguments;return new Promise(function(t,n){var r=s.apply(e,a);function o(e){c(r,t,n,o,i,"next",e)}function i(e){c(r,t,n,o,i,"throw",e)}o(void 0)})}}
function _(e,t){var n;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(n=u(e))||t&&e&&"number"==typeof e.length){n&&(e=n
);var r=0,t=function(){};return{s:t,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:t}}throw new TypeError(
"Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,i=!0,
a=!1;return{s:function(){n=e[Symbol.iterator]()},n:function(){var e=n.next();return i=e.done,e},e:function(e){a=!0,o=e},f:function(){try{
i||null==n.return||n.return()}finally{if(a)throw o}}}}function u(e,t){if(e){if("string"==typeof e)return l(e,t);var n=Object.prototype.toString.call(e
).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e
):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?l(e,t):void 0}}function l(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,
r=new Array(t);n<t;n++)r[n]=e[n];return r}var g,h,f,S,x,E=0;function m(){var e,
t=0<arguments.length&&void 0!==arguments[0]?arguments[0]:h.querySelector("ha-panel-lovelace");!M("disable_km")&&t&&(e=g.hass.panelUrl,
window.kioskModeEntities[e]||(window.kioskModeEntities[e]=[]),y(t,e))}function y(t,n){E++;try{var e=t.lovelace.config.kiosk_mode||{};b(t,e,n)}catch(e
){E<40?setTimeout(function(){return y(t)},50):(console.log("Lovelace config not found, continuing with default configuration."),b(t,{},n))}}
function A(e){return Array.isArray(e)?e:[e]}function M(e){return A(e).some(function(e){return window.location.search.includes(e)})}function j(e,t){A(e
).forEach(function(e){return window.localStorage.setItem(e,t)})}function q(e){return"true"==window.localStorage.getItem(e)}function p(e){
return e.querySelector("#kiosk_mode_".concat(e.localName))}function I(e,t){var n;p(t)||((n=document.createElement("style")).setAttribute("id",
"kiosk_mode_".concat(t.localName)),n.innerHTML=e,t.appendChild(n))}function O(e){A(e).forEach(function(e){p(e)&&e.querySelector("#kiosk_mode_".concat(
e.localName)).remove()})}function b(e,t,n){E=0;var r=e.shadowRoot.querySelector("hui-root").shadowRoot,o=r.querySelector("app-toolbar"),
i=g.hass.states,a=t.admin_settings,s=t.non_admin_settings,c=t.entity_settings,d=t.user_settings,u=t.mobile_settings,l=!1,h=!1,f=q("kmHeader")||M([
"kiosk","hide_header"]),e=(m=q("kmSidebar")||M(["kiosk","hide_sidebar"]))||f,f=e?f:t.kiosk||t.hide_header,m=e?m:t.kiosk||t.hide_sidebar;if(
a&&x.is_admin&&(f=a.kiosk||a.hide_header,m=a.kiosk||a.hide_sidebar,l=a.ignore_entity_settings,h=a.ignore_mobile_settings),s&&!x.is_admin&&(
f=s.kiosk||s.hide_header,m=s.kiosk||s.hide_sidebar,l=s.ignore_entity_settings,h=s.ignore_mobile_settings),d){var y=_(A(d));try{for(y.s();!(p=y.n()
).done;){var p=p.value;A(p.users).some(function(e){return e.toLowerCase()==x.name.toLowerCase()})&&(f=p.kiosk||p.hide_header,m=p.kiosk||p.hide_sidebar
,l=p.ignore_entity_settings,h=p.ignore_mobile_settings)}}catch(e){y.e(e)}finally{y.f()}}if(u&&!h&&(d=u.custom_width||812,window.innerWidth<=d&&(
f=u.kiosk||u.hide_header,m=u.kiosk||u.hide_sidebar,l=u.ignore_entity_settings)),c&&!l){var b=_(c);try{for(b.s();!(w=b.n()).done;){var k=w.value,
v=Object.keys(k.entity)[0],w=k.entity[v];window.kioskModeEntities[n].includes(v)||window.kioskModeEntities[n].push(v),i[v].state==w&&(
"hide_header"in k&&(f=k.hide_header),"hide_sidebar"in k&&(m=k.hide_sidebar),"kiosk"in k&&(f=m=k.kiosk))}}catch(e){b.e(e)}finally{b.f()}}f?(I(
"#view{min-height:100vh !important;--header-height:0;}app-header{display:none;}",r),M("cache")&&j("kmHeader","true")):O(r),m?(I(
":host{--app-drawer-width:0 !important;}#drawer{display:none;}",S),I("ha-menu-button{display:none !important;}",o),M("cache")&&j("kmSidebar","true")
):O([o,S]),window.dispatchEvent(new Event("resize"))}function k(){return v.apply(this,arguments)}function v(){return(v=d(regeneratorRuntime.mark(
function e(){return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,window.hassConnection;case 2:
e.sent.conn.subscribeMessage(function(e){var t=window.kioskModeEntities[g.hass.panelUrl]||[];!t.length||"state_changed"!=e.event_type||!t.includes(
e.data.entity_id)||e.data.old_state&&e.data.new_state.state==e.data.old_state.state||m()},{type:"subscribe_events",event_type:"state_changed"})
;case 3:case"end":return e.stop()}},e)}))).apply(this,arguments)}function w(){new MutationObserver(function(e){e.forEach(function(e){
e.addedNodes.forEach(function(e){"ha-panel-lovelace"==e.localName&&m(e)})})}).observe(f,{childList:!0})}window.kioskModeEntities={},Promise.resolve(
customElements.whenDefined("hui-view")).then(function(){g=document.querySelector("home-assistant"),h=g.shadowRoot.querySelector("home-assistant-main"
).shadowRoot,f=h.querySelector("partial-panel-resolver"),S=h.querySelector("app-drawer-layout"),x=g.hass.user,m(),w(),k()}),M("clear_km_cache")&&j([
"kmHeader","kmSidebar"],"false");for(var R={header:"%c≡ kiosk-mode".padEnd(27),ver:"%cversion 1.6.5 "},C="%c\n",L=Math.max.apply(Math,t(Object.values(
R).map(function(e){return e.length}))),N=0,T=Object.entries(R);N<T.length;N++){var H=e(T[N],1),P=H[0];R[P].length<=L&&(R[P]=R[P].padEnd(L)),
"header"==P&&(R[P]="".concat(R[P].slice(0,-1),"⋮ "))}
var U="display:inline-block;border-width:1px 1px 0 1px;border-style:solid;border-color:#424242;color:white;background:#03a9f4;font-size:12px;padding:4px 4.5px 5px 6px;"
,z="border-width:0px 1px 1px 1px;padding:7px;background:white;color:#424242;line-height:0.7;";console.info(R.header+C+R.ver,U,"","".concat(U," "
).concat(z));