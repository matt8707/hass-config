!function n(o,i,a){function s(t,e){if(!i[t]){if(!o[t]){var r="function"==typeof require&&require;if(!e&&r)return r(t,!0);if(u)return u(t,!0);throw(
r=new Error("Cannot find module '"+t+"'")).code="MODULE_NOT_FOUND",r}r=i[t]={exports:{}},o[t][0].call(r.exports,function(e){return s(o[t][1][e]||e)},r
,r.exports,n,o,i,a)}return i[t].exports}for(var u="function"==typeof require&&require,e=0;e<a.length;e++)s(a[e]);return s}({1:[function(e,t,r){
"use strict";var n=e("@babel/runtime/helpers/interopRequireDefault"),o=n(e("@babel/runtime/regenerator")),i=n(e("@babel/runtime/helpers/slicedToArray"
)),a=n(e("@babel/runtime/helpers/toConsumableArray")),s=n(e("@babel/runtime/helpers/asyncToGenerator")),u=n(e("@babel/runtime/helpers/classCallCheck")
),l=n(e("@babel/runtime/helpers/createClass"));function f(e,t){var r="undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(!r){if(
Array.isArray(e)||(r=function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Map"===(
r="Object"===r&&e.constructor?e.constructor.name:r)||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t
):void 0}}(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,t=function(){};return{s:t,n:function(){return n>=e.length?{done:!0}:{done:!1,
value:e[n++]}},e:function(e){throw e},f:t}}throw new TypeError(
"Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,i=!0,
a=!1;return{s:function(){r=r.call(e)},n:function(){var e=r.next();return i=e.done,e},e:function(e){a=!0,o=e},f:function(){try{
i||null==r.return||r.return()}finally{if(a)throw o}}}}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r]
;return n}for(var c=function(){function e(){(0,u.default)(this,e),window.kioskModeEntities={},this.queryString("clear_km_cache")&&this.setCache([
"kmHeader","kmSidebar","kmOverflow","kmMenuButton"],"false"),this.ha=document.querySelector("home-assistant"),
this.main=this.ha.shadowRoot.querySelector("home-assistant-main").shadowRoot,this.user=this.ha.hass.user,this.llAttempts=0,this.run(),
this.entityWatch(),new MutationObserver(this.watchDashboards).observe(this.main.querySelector("partial-panel-resolver"),{childList:!0})}var t;return(0
,l.default)(e,[{key:"run",value:function(){var e=0<arguments.length&&void 0!==arguments[0]?arguments[0]:this.main.querySelector("ha-panel-lovelace")
;!this.queryString("disable_km")&&e&&this.getConfig(e)}},{key:"getConfig",value:function(t){var r=this;this.llAttempts++;try{
var e=t.lovelace.config.kiosk_mode||{};this.processConfig(t,e)}catch(e){this.llAttempts<200?setTimeout(function(){return r.getConfig(t)},50):(
console.log("Lovelace config not found, continuing with default configuration."),console.log(e),this.processConfig(t,{}))}}},{key:"processConfig",
value:function(e,t){var r=this,n=this.ha.hass.panelUrl;window.kioskModeEntities[n]||(window.kioskModeEntities[n]=[]),
this.hideHeader=this.hideSidebar=this.hideOverflow=this.ignoreEntity=this.ignoreMobile=!1;var o=this.cached(["kmHeader","kmSidebar","kmOverflow",
"kmMenuButton"])||this.queryString(["kiosk","hide_sidebar","hide_header","hide_overflow","hide_menubutton"]);o&&(this.hideHeader=this.cached(
"kmHeader")||this.queryString(["kiosk","hide_header"]),this.hideSidebar=this.cached("kmSidebar")||this.queryString(["kiosk","hide_sidebar"]),
this.hideOverflow=this.cached("kmOverflow")||this.queryString(["kiosk","hide_overflow"]),this.hideMenuButton=this.cached("kmMenuButton"
)||this.queryString(["kiosk","hide_menubutton"])),this.hideHeader=o?this.hideHeader:t.kiosk||t.hide_header,
this.hideSidebar=o?this.hideSidebar:t.kiosk||t.hide_sidebar,this.hideOverflow=o?this.hideOverflow:t.kiosk||t.hide_overflow,
this.hideMenuButton=o?this.hideMenuButton:t.kiosk||t.hide_menubutton;var i=this.user.is_admin?t.admin_settings:t.non_admin_settings;if(
i&&this.setOptions(i),t.user_settings){var a,s=f(this.array(t.user_settings));try{for(s.s();!(a=s.n()).done;){var u=a.value;this.array(u.users).some(
function(e){return e.toLowerCase()==r.user.name.toLowerCase()})&&this.setOptions(u)}}catch(e){s.e(e)}finally{s.f()}}
o=this.ignoreMobile?null:t.mobile_settings;o&&(i=o.custom_width||812,window.innerWidth<=i&&this.setOptions(o))
;t=this.ignoreEntity?null:t.entity_settings;if(t){var l,h=f(t);try{for(h.s();!(l=h.n()).done;){var c=l.value,d=Object.keys(c.entity)[0]
;window.kioskModeEntities[n].includes(d)||window.kioskModeEntities[n].push(d),this.ha.hass.states[d].state==c.entity[d]&&("hide_header"in c&&(
this.hideHeader=c.hide_header),"hide_sidebar"in c&&(this.hideSidebar=c.hide_sidebar),"hide_overflow"in c&&(this.hideOverflow=c.hide_overflow),
"hide_menubutton"in c&&(this.hideMenuButton=c.hide_menubutton),"kiosk"in c&&(this.hideHeader=this.hideSidebar=c.kiosk))}}catch(e){h.e(e)}finally{h.f()
}}this.insertStyles(e)}},{key:"insertStyles",value:function(e){var t=e.shadowRoot.querySelector("hui-root").shadowRoot,r=this.main.querySelector(
"app-drawer-layout"),e=t.querySelector("app-toolbar");this.hideHeader||this.hideOverflow?(this.addStyle("".concat(
this.hideHeader?"#view{min-height:100vh !important;--header-height:0;}app-header{display:none;}":"").concat(
this.hideOverflow?"ha-button-menu{display:none !important;}":""),t),this.queryString("cache")&&(this.hideHeader&&this.setCache("kmHeader","true"),
this.hideOverflow&&this.setCache("kmOverflow","true"))):this.removeStyle(t),this.hideSidebar?(this.addStyle(
":host{--app-drawer-width:0 !important;}#drawer{display:none;}",r),this.addStyle("ha-menu-button{display:none !important;}",e),this.queryString(
"cache")&&this.setCache("kmSidebar","true")):this.removeStyle([e,r]),this.hideMenuButton?(this.addStyle("ha-menu-button{display:none !important;}",e),
this.queryString("cache")&&this.setCache("kmMenuButton","true")):this.removeStyle(e),window.dispatchEvent(new Event("resize")),this.llAttempts=0}},{
key:"watchDashboards",value:function(e){e.forEach(function(e){var t,r=f(e.addedNodes);try{for(r.s();!(t=r.n()).done;){var n=t.value
;"ha-panel-lovelace"==n.localName&&window.KioskMode.run(n)}}catch(e){r.e(e)}finally{r.f()}})}},{key:"entityWatch",value:(t=(0,s.default)(
o.default.mark(function e(){var t=this;return o.default.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,window.hassConnection
;case 2:e.sent.conn.subscribeMessage(function(e){return t.entityWatchCallback(e)},{type:"subscribe_events",event_type:"state_changed"});case 3:
case"end":return e.stop()}},e)})),function(){return t.apply(this,arguments)})},{key:"entityWatchCallback",value:function(e){
var t=window.kioskModeEntities[this.ha.hass.panelUrl]||[];!t.length||"state_changed"!=e.event_type||!t.includes(e.data.entity_id
)||e.data.old_state&&e.data.new_state.state==e.data.old_state.state||this.run()}},{key:"setOptions",value:function(e){
this.hideHeader=e.kiosk||e.hide_header,this.hideSidebar=e.kiosk||e.hide_sidebar,this.hideOverflow=e.kiosk||e.hide_overflow,
this.hideMenuButton=e.kiosk||e.hide_menubutton,this.ignoreEntity=e.ignore_entity_settings,this.ignoreMobile=e.ignore_mobile_settings}},{key:"array",
value:function(e){return Array.isArray(e)?e:[e]}},{key:"queryString",value:function(e){return this.array(e).some(function(e){
return window.location.search.includes(e)})}},{key:"setCache",value:function(e,t){this.array(e).forEach(function(e){
return window.localStorage.setItem(e,t)})}},{key:"cached",value:function(e){return this.array(e).some(function(e){
return"true"==window.localStorage.getItem(e)})}},{key:"styleExists",value:function(e){return e.querySelector("#kiosk_mode_".concat(e.localName))}},{
key:"addStyle",value:function(e,t){var r;this.styleExists(t)||((r=document.createElement("style")).setAttribute("id","kiosk_mode_".concat(t.localName)
),r.innerHTML=e,t.appendChild(r))}},{key:"removeStyle",value:function(e){var t=this;this.array(e).forEach(function(e){t.styleExists(e
)&&e.querySelector("#kiosk_mode_".concat(e.localName)).remove()})}}]),e}(),d={header:"%c≡ kiosk-mode".padEnd(27),ver:"%cversion 1.7.2 "},
p=Math.max.apply(Math,(0,a.default)(Object.values(d).map(function(e){return e.length}))),y=0,m=Object.entries(d);y<m.length;y++){var v=(0,i.default)(
m[y],1)[0];d[v].length<=p&&(d[v]=d[v].padEnd(p)),"header"==v&&(d[v]="".concat(d[v].slice(0,-1),"⋮ "))}
a="display:inline-block;border-width:1px 1px 0 1px;border-style:solid;border-color:#424242;color:white;background:#03a9f4;font-size:12px;padding:4px 4.5px 5px 6px;"
;console.info(d.header+"%c\n"+d.ver,a,"","".concat(a," ").concat(
"border-width:0px 1px 1px 1px;padding:7px;background:white;color:#424242;line-height:0.7;")),Promise.resolve(customElements.whenDefined("hui-view")
).then(function(){window.KioskMode=new c})},{"@babel/runtime/helpers/asyncToGenerator":5,"@babel/runtime/helpers/classCallCheck":6,
"@babel/runtime/helpers/createClass":7,"@babel/runtime/helpers/interopRequireDefault":8,"@babel/runtime/helpers/slicedToArray":13,
"@babel/runtime/helpers/toConsumableArray":14,"@babel/runtime/regenerator":16}],2:[function(e,t,r){t.exports=function(e,t){(null==t||t>e.length)&&(
t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n},t.exports.default=t.exports,t.exports.__esModule=!0},{}],3:[function(e,t,r){
t.exports=function(e){if(Array.isArray(e))return e},t.exports.default=t.exports,t.exports.__esModule=!0},{}],4:[function(e,t,r){var n=e(
"./arrayLikeToArray.js");t.exports=function(e){if(Array.isArray(e))return n(e)},t.exports.default=t.exports,t.exports.__esModule=!0},{
"./arrayLikeToArray.js":2}],5:[function(e,t,r){function u(e,t,r,n,o,i,a){try{var s=e[i](a),u=s.value}catch(e){return void r(e)}s.done?t(u
):Promise.resolve(u).then(n,o)}t.exports=function(s){return function(){var e=this,a=arguments;return new Promise(function(t,r){var n=s.apply(e,a)
;function o(e){u(n,t,r,o,i,"next",e)}function i(e){u(n,t,r,o,i,"throw",e)}o(void 0)})}},t.exports.default=t.exports,t.exports.__esModule=!0},{}],6:[
function(e,t,r){t.exports=function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")},t.exports.default=t.exports,
t.exports.__esModule=!0},{}],7:[function(e,t,r){function n(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0
,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}t.exports=function(e,t,r){return t&&n(e.prototype,t),r&&n(e,r),e},
t.exports.default=t.exports,t.exports.__esModule=!0},{}],8:[function(e,t,r){t.exports=function(e){return e&&e.__esModule?e:{default:e}},
t.exports.default=t.exports,t.exports.__esModule=!0},{}],9:[function(e,t,r){t.exports=function(e){if(
"undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)},t.exports.default=t.exports,t.exports.__esModule=!0}
,{}],10:[function(e,t,r){t.exports=function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,
o,i=[],a=!0,s=!1;try{for(r=r.call(e);!(a=(n=r.next()).done)&&(i.push(n.value),!t||i.length!==t);a=!0);}catch(e){s=!0,o=e}finally{try{
a||null==r.return||r.return()}finally{if(s)throw o}}return i}},t.exports.default=t.exports,t.exports.__esModule=!0},{}],11:[function(e,t,r){
t.exports=function(){throw new TypeError(
"Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")},
t.exports.default=t.exports,t.exports.__esModule=!0},{}],12:[function(e,t,r){t.exports=function(){throw new TypeError(
"Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")},
t.exports.default=t.exports,t.exports.__esModule=!0},{}],13:[function(e,t,r){var n=e("./arrayWithHoles.js"),o=e("./iterableToArrayLimit.js"),i=e(
"./unsupportedIterableToArray.js"),a=e("./nonIterableRest.js");t.exports=function(e,t){return n(e)||o(e,t)||i(e,t)||a()},t.exports.default=t.exports,
t.exports.__esModule=!0},{"./arrayWithHoles.js":3,"./iterableToArrayLimit.js":10,"./nonIterableRest.js":11,"./unsupportedIterableToArray.js":15}],14:[
function(e,t,r){var n=e("./arrayWithoutHoles.js"),o=e("./iterableToArray.js"),i=e("./unsupportedIterableToArray.js"),a=e("./nonIterableSpread.js")
;t.exports=function(e){return n(e)||o(e)||i(e)||a()},t.exports.default=t.exports,t.exports.__esModule=!0},{"./arrayWithoutHoles.js":4,
"./iterableToArray.js":9,"./nonIterableSpread.js":12,"./unsupportedIterableToArray.js":15}],15:[function(e,t,r){var n=e("./arrayLikeToArray.js")
;t.exports=function(e,t){if(e){if("string"==typeof e)return n(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Map"===(
r="Object"===r&&e.constructor?e.constructor.name:r)||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?n(e,t
):void 0}},t.exports.default=t.exports,t.exports.__esModule=!0},{"./arrayLikeToArray.js":2}],16:[function(e,t,r){t.exports=e("regenerator-runtime")},{
"regenerator-runtime":17}],17:[function(e,t,r){t=function(a){"use strict";var u,e=Object.prototype,l=e.hasOwnProperty,
t="function"==typeof Symbol?Symbol:{},n=t.iterator||"@@iterator",r=t.asyncIterator||"@@asyncIterator",o=t.toStringTag||"@@toStringTag";function i(e,t,
r){return Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}),e[t]}try{i({},"")}catch(e){i=function(e,t,r){return e[t]=r}}
function s(e,t,r,n){var o,i,a,s,t=t&&t.prototype instanceof m?t:m,t=Object.create(t.prototype),n=new E(n||[]);return t._invoke=(o=e,i=r,a=n,s=c,
function(e,t){if(s===f)throw new Error("Generator is already running");if(s===p){if("throw"===e)throw t;return M()}for(a.method=e,a.arg=t;;){
var r=a.delegate;if(r){var n=function e(t,r){var n=t.iterator[r.method];if(n===u){if(r.delegate=null,"throw"===r.method){if(t.iterator.return&&(
r.method="return",r.arg=u,e(t,r),"throw"===r.method))return y;r.method="throw",r.arg=new TypeError("The iterator does not provide a 'throw' method")}
return y}var n=h(n,t.iterator,r.arg);if("throw"===n.type)return r.method="throw",r.arg=n.arg,r.delegate=null,y;n=n.arg;if(!n)return r.method="throw",
r.arg=new TypeError("iterator result is not an object"),r.delegate=null,y;{if(!n.done)return n;r[t.resultName]=n.value,r.next=t.nextLoc,
"return"!==r.method&&(r.method="next",r.arg=u)}r.delegate=null;return y}(r,a);if(n){if(n===y)continue;return n}}if("next"===a.method
)a.sent=a._sent=a.arg;else if("throw"===a.method){if(s===c)throw s=p,a.arg;a.dispatchException(a.arg)}else"return"===a.method&&a.abrupt("return",a.arg
);s=f;n=h(o,i,a);if("normal"===n.type){if(s=a.done?p:d,n.arg!==y)return{value:n.arg,done:a.done}}else"throw"===n.type&&(s=p,a.method="throw",
a.arg=n.arg)}}),t}function h(e,t,r){try{return{type:"normal",arg:e.call(t,r)}}catch(e){return{type:"throw",arg:e}}}a.wrap=s;var c="suspendedStart",
d="suspendedYield",f="executing",p="completed",y={};function m(){}function v(){}function b(){}var g={};i(g,n,function(){return this})
;t=Object.getPrototypeOf,t=t&&t(t(j([])));t&&t!==e&&l.call(t,n)&&(g=t);var w=b.prototype=m.prototype=Object.create(g);function k(e){["next","throw",
"return"].forEach(function(t){i(e,t,function(e){return this._invoke(t,e)})})}function x(a,s){var t;this._invoke=function(r,n){function e(){
return new s(function(e,t){!function t(e,r,n,o){e=h(a[e],a,r);if("throw"!==e.type){var i=e.arg;return(r=i.value)&&"object"==typeof r&&l.call(r,
"__await")?s.resolve(r.__await).then(function(e){t("next",e,n,o)},function(e){t("throw",e,n,o)}):s.resolve(r).then(function(e){i.value=e,n(i)},
function(e){return t("throw",e,n,o)})}o(e.arg)}(r,n,e,t)})}return t=t?t.then(e,e):e()}}function _(e){var t={tryLoc:e[0]};1 in e&&(t.catchLoc=e[1]),
2 in e&&(t.finallyLoc=e[2],t.afterLoc=e[3]),this.tryEntries.push(t)}function S(e){var t=e.completion||{};t.type="normal",delete t.arg,e.completion=t}
function E(e){this.tryEntries=[{tryLoc:"root"}],e.forEach(_,this),this.reset(!0)}function j(t){if(t){var e=t[n];if(e)return e.call(t);if(
"function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,e=function e(){for(;++r<t.length;)if(l.call(t,r))return e.value=t[r],e.done=!1,e
;return e.value=u,e.done=!0,e};return e.next=e}}return{next:M}}function M(){return{value:u,done:!0}}return i(w,"constructor",v.prototype=b),i(b,
"constructor",v),v.displayName=i(b,o,"GeneratorFunction"),a.isGeneratorFunction=function(e){e="function"==typeof e&&e.constructor;return!!e&&(
e===v||"GeneratorFunction"===(e.displayName||e.name))},a.mark=function(e){return Object.setPrototypeOf?Object.setPrototypeOf(e,b):(e.__proto__=b,i(e,o
,"GeneratorFunction")),e.prototype=Object.create(w),e},a.awrap=function(e){return{__await:e}},k(x.prototype),i(x.prototype,r,function(){return this}),
a.AsyncIterator=x,a.async=function(e,t,r,n,o){void 0===o&&(o=Promise);var i=new x(s(e,t,r,n),o);return a.isGeneratorFunction(t)?i:i.next().then(
function(e){return e.done?e.value:i.next()})},k(w),i(w,o,"Generator"),i(w,n,function(){return this}),i(w,"toString",function(){
return"[object Generator]"}),a.keys=function(r){var e,n=[];for(e in r)n.push(e);return n.reverse(),function e(){for(;n.length;){var t=n.pop();if(
t in r)return e.value=t,e.done=!1,e}return e.done=!0,e}},a.values=j,E.prototype={constructor:E,reset:function(e){if(this.prev=0,this.next=0,
this.sent=this._sent=u,this.done=!1,this.delegate=null,this.method="next",this.arg=u,this.tryEntries.forEach(S),!e)for(var t in this)"t"===t.charAt(0
)&&l.call(this,t)&&!isNaN(+t.slice(1))&&(this[t]=u)},stop:function(){this.done=!0;var e=this.tryEntries[0].completion;if("throw"===e.type)throw e.arg
;return this.rval},dispatchException:function(r){if(this.done)throw r;var n=this;function e(e,t){return i.type="throw",i.arg=r,n.next=e,t&&(
n.method="next",n.arg=u),!!t}for(var t=this.tryEntries.length-1;0<=t;--t){var o=this.tryEntries[t],i=o.completion;if("root"===o.tryLoc)return e("end")
;if(o.tryLoc<=this.prev){var a=l.call(o,"catchLoc"),s=l.call(o,"finallyLoc");if(a&&s){if(this.prev<o.catchLoc)return e(o.catchLoc,!0);if(
this.prev<o.finallyLoc)return e(o.finallyLoc)}else if(a){if(this.prev<o.catchLoc)return e(o.catchLoc,!0)}else{if(!s)throw new Error(
"try statement without catch or finally");if(this.prev<o.finallyLoc)return e(o.finallyLoc)}}}},abrupt:function(e,t){for(
var r=this.tryEntries.length-1;0<=r;--r){var n=this.tryEntries[r];if(n.tryLoc<=this.prev&&l.call(n,"finallyLoc")&&this.prev<n.finallyLoc){var o=n
;break}}var i=(o=o&&("break"===e||"continue"===e)&&o.tryLoc<=t&&t<=o.finallyLoc?null:o)?o.completion:{};return i.type=e,i.arg=t,o?(this.method="next",
this.next=o.finallyLoc,y):this.complete(i)},complete:function(e,t){if("throw"===e.type)throw e.arg
;return"break"===e.type||"continue"===e.type?this.next=e.arg:"return"===e.type?(this.rval=this.arg=e.arg,this.method="return",this.next="end"
):"normal"===e.type&&t&&(this.next=t),y},finish:function(e){for(var t=this.tryEntries.length-1;0<=t;--t){var r=this.tryEntries[t];if(r.finallyLoc===e
)return this.complete(r.completion,r.afterLoc),S(r),y}},catch:function(e){for(var t=this.tryEntries.length-1;0<=t;--t){var r=this.tryEntries[t];if(
r.tryLoc===e){var n,o=r.completion;return"throw"===o.type&&(n=o.arg,S(r)),n}}throw new Error("illegal catch attempt")},delegateYield:function(e,t,r){
return this.delegate={iterator:j(e),resultName:t,nextLoc:r},"next"===this.method&&(this.arg=u),y}},a}("object"==typeof t?t.exports:{});try{
regeneratorRuntime=t}catch(e){"object"==typeof globalThis?globalThis.regeneratorRuntime=t:Function("r","regeneratorRuntime = r")(t)}},{}]},{},[1]);