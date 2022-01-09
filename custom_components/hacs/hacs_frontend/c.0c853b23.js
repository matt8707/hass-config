import{S as t,aD as e,aE as i,aF as o,P as s,Q as a,aG as n,aH as r,aI as l,_ as c,j as h,e as d,p,r as u,n as f,o as g,m as y,aJ as _,ah as m,aK as v,aL as b,aM as w,aN as k,d as T}from"./main-25487c89.js";import{I as x}from"./c.a06a99f1.js";import{P as S}from"./c.27392995.js";import"./c.e80b707a.js";import{i as C,s as E}from"./c.3570aec6.js";import{a as $}from"./c.0a038163.js";import"./c.a816d055.js";import"./c.e4c27bcc.js";import"./c.24698728.js";import"./c.988357e4.js";import"./c.bd24fdea.js";const z=[x,{listeners:{"app-reset-layout":"_appResetLayoutHandler","iron-resize":"resetLayout"},attached:function(){this.fire("app-reset-layout")},_appResetLayoutHandler:function(e){t(e).path[0]!==this&&(this.resetLayout(),e.stopPropagation())},_updateLayoutStates:function(){console.error("unimplemented")},resetLayout:function(){var t=this._updateLayoutStates.bind(this);this._layoutDebouncer=e.debounce(this._layoutDebouncer,i,t),o(this._layoutDebouncer),this._notifyDescendantResize()},_notifyLayoutChanged:function(){var t=this;requestAnimationFrame((function(){t.fire("app-reset-layout")}))},_notifyDescendantResize:function(){this.isAttached&&this._interestedResizables.forEach((function(t){this.resizerShouldNotify(t)&&this._notifyDescendant(t)}),this)}}],L={properties:{scrollTarget:{type:HTMLElement,value:function(){return this._defaultScrollTarget}}},observers:["_scrollTargetChanged(scrollTarget, isAttached)"],_shouldHaveListener:!0,_scrollTargetChanged:function(e,i){if(this._oldScrollTarget&&(this._toggleScrollListener(!1,this._oldScrollTarget),this._oldScrollTarget=null),i)if("document"===e)this.scrollTarget=this._doc;else if("string"==typeof e){var o=this.domHost;this.scrollTarget=o&&o.$?o.$[e]:t(this.ownerDocument).querySelector("#"+e)}else this._isValidScrollTarget()&&(this._oldScrollTarget=e,this._toggleScrollListener(this._shouldHaveListener,e))},_scrollHandler:function(){},get _defaultScrollTarget(){return this._doc},get _doc(){return this.ownerDocument.documentElement},get _scrollTop(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageYOffset:this.scrollTarget.scrollTop:0},get _scrollLeft(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.pageXOffset:this.scrollTarget.scrollLeft:0},set _scrollTop(t){this.scrollTarget===this._doc?window.scrollTo(window.pageXOffset,t):this._isValidScrollTarget()&&(this.scrollTarget.scrollTop=t)},set _scrollLeft(t){this.scrollTarget===this._doc?window.scrollTo(t,window.pageYOffset):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=t)},scroll:function(t,e){var i;"object"==typeof t?(i=t.left,e=t.top):i=t,i=i||0,e=e||0,this.scrollTarget===this._doc?window.scrollTo(i,e):this._isValidScrollTarget()&&(this.scrollTarget.scrollLeft=i,this.scrollTarget.scrollTop=e)},get _scrollTargetWidth(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerWidth:this.scrollTarget.offsetWidth:0},get _scrollTargetHeight(){return this._isValidScrollTarget()?this.scrollTarget===this._doc?window.innerHeight:this.scrollTarget.offsetHeight:0},_isValidScrollTarget:function(){return this.scrollTarget instanceof HTMLElement},_toggleScrollListener:function(t,e){var i=e===this._doc?window:e;t?this._boundScrollHandler||(this._boundScrollHandler=this._scrollHandler.bind(this),i.addEventListener("scroll",this._boundScrollHandler)):this._boundScrollHandler&&(i.removeEventListener("scroll",this._boundScrollHandler),this._boundScrollHandler=null)},toggleScrollListener:function(t){this._shouldHaveListener=t,this._toggleScrollListener(t,this.scrollTarget)}},H={},D=[L,{properties:{effects:{type:String},effectsConfig:{type:Object,value:function(){return{}}},disabled:{type:Boolean,reflectToAttribute:!0,value:!1},threshold:{type:Number,value:0},thresholdTriggered:{type:Boolean,notify:!0,readOnly:!0,reflectToAttribute:!0}},observers:["_effectsChanged(effects, effectsConfig, isAttached)"],_updateScrollState:function(t){},isOnScreen:function(){return!1},isContentBelow:function(){return!1},_effectsRunFn:null,_effects:null,get _clampedScrollTop(){return Math.max(0,this._scrollTop)},attached:function(){this._scrollStateChanged()},detached:function(){this._tearDownEffects()},createEffect:function(t,e){var i=H[t];if(!i)throw new ReferenceError(this._getUndefinedMsg(t));var o=this._boundEffect(i,e||{});return o.setUp(),o},_effectsChanged:function(t,e,i){this._tearDownEffects(),t&&i&&(t.split(" ").forEach((function(t){var i;""!==t&&((i=H[t])?this._effects.push(this._boundEffect(i,e[t])):console.warn(this._getUndefinedMsg(t)))}),this),this._setUpEffect())},_layoutIfDirty:function(){return this.offsetWidth},_boundEffect:function(t,e){e=e||{};var i=parseFloat(e.startsAt||0),o=parseFloat(e.endsAt||1),s=o-i,a=function(){},n=0===i&&1===o?t.run:function(e,o){t.run.call(this,Math.max(0,(e-i)/s),o)};return{setUp:t.setUp?t.setUp.bind(this,e):a,run:t.run?n.bind(this):a,tearDown:t.tearDown?t.tearDown.bind(this):a}},_setUpEffect:function(){this.isAttached&&this._effects&&(this._effectsRunFn=[],this._effects.forEach((function(t){!1!==t.setUp()&&this._effectsRunFn.push(t.run)}),this))},_tearDownEffects:function(){this._effects&&this._effects.forEach((function(t){t.tearDown()})),this._effectsRunFn=[],this._effects=[]},_runEffects:function(t,e){this._effectsRunFn&&this._effectsRunFn.forEach((function(i){i(t,e)}))},_scrollHandler:function(){this._scrollStateChanged()},_scrollStateChanged:function(){if(!this.disabled){var t=this._clampedScrollTop;this._updateScrollState(t),this.threshold>0&&this._setThresholdTriggered(t>=this.threshold)}},_getDOMRef:function(t){console.warn("_getDOMRef","`"+t+"` is undefined")},_getUndefinedMsg:function(t){return"Scroll effect `"+t+"` is undefined. Did you forget to import app-layout/app-scroll-effects/effects/"+t+".html ?"}}];s({_template:a`
    <style>
      :host {
        position: relative;
        display: block;
        transition-timing-function: linear;
        transition-property: -webkit-transform;
        transition-property: transform;
      }

      :host::before {
        position: absolute;
        right: 0px;
        bottom: -5px;
        left: 0px;
        width: 100%;
        height: 5px;
        content: "";
        transition: opacity 0.4s;
        pointer-events: none;
        opacity: 0;
        box-shadow: inset 0px 5px 6px -3px rgba(0, 0, 0, 0.4);
        will-change: opacity;
        @apply --app-header-shadow;
      }

      :host([shadow])::before {
        opacity: 1;
      }

      #background {
        @apply --layout-fit;
        overflow: hidden;
      }

      #backgroundFrontLayer,
      #backgroundRearLayer {
        @apply --layout-fit;
        height: 100%;
        pointer-events: none;
        background-size: cover;
      }

      #backgroundFrontLayer {
        @apply --app-header-background-front-layer;
      }

      #backgroundRearLayer {
        opacity: 0;
        @apply --app-header-background-rear-layer;
      }

      #contentContainer {
        position: relative;
        width: 100%;
        height: 100%;
      }

      :host([disabled]),
      :host([disabled])::after,
      :host([disabled]) #backgroundFrontLayer,
      :host([disabled]) #backgroundRearLayer,
      /* Silent scrolling should not run CSS transitions */
      :host([silent-scroll]),
      :host([silent-scroll])::after,
      :host([silent-scroll]) #backgroundFrontLayer,
      :host([silent-scroll]) #backgroundRearLayer {
        transition: none !important;
      }

      :host([disabled]) ::slotted(app-toolbar:first-of-type),
      :host([disabled]) ::slotted([sticky]),
      /* Silent scrolling should not run CSS transitions */
      :host([silent-scroll]) ::slotted(app-toolbar:first-of-type),
      :host([silent-scroll]) ::slotted([sticky]) {
        transition: none !important;
      }

    </style>
    <div id="contentContainer">
      <slot id="slot"></slot>
    </div>
`,is:"app-header",behaviors:[D,z],properties:{condenses:{type:Boolean,value:!1},fixed:{type:Boolean,value:!1},reveals:{type:Boolean,value:!1},shadow:{type:Boolean,reflectToAttribute:!0,value:!1}},observers:["_configChanged(isAttached, condenses, fixed)"],_height:0,_dHeight:0,_stickyElTop:0,_stickyElRef:null,_top:0,_progress:0,_wasScrollingDown:!1,_initScrollTop:0,_initTimestamp:0,_lastTimestamp:0,_lastScrollTop:0,get _maxHeaderTop(){return this.fixed?this._dHeight:this._height+5},get _stickyEl(){if(this._stickyElRef)return this._stickyElRef;for(var e,i=t(this.$.slot).getDistributedNodes(),o=0;e=i[o];o++)if(e.nodeType===Node.ELEMENT_NODE){if(e.hasAttribute("sticky")){this._stickyElRef=e;break}this._stickyElRef||(this._stickyElRef=e)}return this._stickyElRef},_configChanged:function(){this.resetLayout(),this._notifyLayoutChanged()},_updateLayoutStates:function(){if(0!==this.offsetWidth||0!==this.offsetHeight){var t=this._clampedScrollTop,e=0===this._height||0===t,i=this.disabled;this._height=this.offsetHeight,this._stickyElRef=null,this.disabled=!0,e||this._updateScrollState(0,!0),this._mayMove()?this._dHeight=this._stickyEl?this._height-this._stickyEl.offsetHeight:0:this._dHeight=0,this._stickyElTop=this._stickyEl?this._stickyEl.offsetTop:0,this._setUpEffect(),e?this._updateScrollState(t,!0):(this._updateScrollState(this._lastScrollTop,!0),this._layoutIfDirty()),this.disabled=i}},_updateScrollState:function(t,e){if(0!==this._height){var i=0,o=0,s=this._top;this._lastScrollTop;var a=this._maxHeaderTop,n=t-this._lastScrollTop,r=Math.abs(n),l=t>this._lastScrollTop,c=performance.now();if(this._mayMove()&&(o=this._clamp(this.reveals?s+n:t,0,a)),t>=this._dHeight&&(o=this.condenses&&!this.fixed?Math.max(this._dHeight,o):o,this.style.transitionDuration="0ms"),this.reveals&&!this.disabled&&r<100&&((c-this._initTimestamp>300||this._wasScrollingDown!==l)&&(this._initScrollTop=t,this._initTimestamp=c),t>=a))if(Math.abs(this._initScrollTop-t)>30||r>10){l&&t>=a?o=a:!l&&t>=this._dHeight&&(o=this.condenses&&!this.fixed?this._dHeight:0);var h=n/(c-this._lastTimestamp);this.style.transitionDuration=this._clamp((o-s)/h,0,300)+"ms"}else o=this._top;i=0===this._dHeight?t>0?1:0:o/this._dHeight,e||(this._lastScrollTop=t,this._top=o,this._wasScrollingDown=l,this._lastTimestamp=c),(e||i!==this._progress||s!==o||0===t)&&(this._progress=i,this._runEffects(i,o),this._transformHeader(o))}},_mayMove:function(){return this.condenses||!this.fixed},willCondense:function(){return this._dHeight>0&&this.condenses},isOnScreen:function(){return 0!==this._height&&this._top<this._height},isContentBelow:function(){return 0===this._top?this._clampedScrollTop>0:this._clampedScrollTop-this._maxHeaderTop>=0},_transformHeader:function(t){this.translate3d(0,-t+"px",0),this._stickyEl&&this.translate3d(0,this.condenses&&t>=this._stickyElTop?Math.min(t,this._dHeight)-this._stickyElTop+"px":0,0,this._stickyEl)},_clamp:function(t,e,i){return Math.min(i,Math.max(e,t))},_ensureBgContainers:function(){this._bgContainer||(this._bgContainer=document.createElement("div"),this._bgContainer.id="background",this._bgRear=document.createElement("div"),this._bgRear.id="backgroundRearLayer",this._bgContainer.appendChild(this._bgRear),this._bgFront=document.createElement("div"),this._bgFront.id="backgroundFrontLayer",this._bgContainer.appendChild(this._bgFront),t(this.root).insertBefore(this._bgContainer,this.$.contentContainer))},_getDOMRef:function(e){switch(e){case"backgroundFrontLayer":return this._ensureBgContainers(),this._bgFront;case"backgroundRearLayer":return this._ensureBgContainers(),this._bgRear;case"background":return this._ensureBgContainers(),this._bgContainer;case"mainTitle":return t(this).querySelector("[main-title]");case"condensedTitle":return t(this).querySelector("[condensed-title]")}return null},getScrollState:function(){return{progress:this._progress,top:this._top}}}),s({_template:a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[S]}),s({_template:a`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[z],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return t(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),i=document.documentElement.clientWidth-e.right;t.style.left=e.left+"px",t.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(i.marginTop=e+"px",i.paddingTop=""):(i.paddingTop=e+"px",i.marginTop="")}}});class R extends(customElements.get("app-header-layout")){static get template(){return a`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",R);const F=(t,e)=>e.component?C(t,e.component):!e.components||e.components.some(e=>C(t,e)),A=t=>t.core,M=(t,e)=>(t=>t.advancedOnly)(e)&&!(t=>{var e;return null===(e=t.userData)||void 0===e?void 0:e.showAdvanced})(t);customElements.define("ha-icon-next",class extends n{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.path="ltr"===window.getComputedStyle(this).direction?r:l},100)}}),c([f("ha-config-navigation")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[d()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[d()],key:"pages",value:void 0},{kind:"field",decorators:[d()],key:"externalConfig",value:void 0},{kind:"method",key:"render",value:function(){return p`
      ${this.pages.map(t=>{var e;return("#external-app-configuration"===t.path?null===(e=this.externalConfig)||void 0===e?void 0:e.hasSettingsScreen:((t,e)=>(A(e)||F(t,e))&&!M(t,e))(this.hass,t))?p`
              <a href=${t.path} role="option" tabindex="-1">
                <paper-icon-item @click=${this._entryClicked}>
                  <div
                    class=${t.iconColor?"icon-background":""}
                    slot="item-icon"
                    .style="background-color: ${t.iconColor||"undefined"}"
                  >
                    <ha-svg-icon .path=${t.iconPath}></ha-svg-icon>
                  </div>
                  <paper-item-body two-line>
                    ${t.name||this.hass.localize(`ui.panel.config.dashboard.${t.translationKey}.title`)}
                    ${"cloud"===t.component&&t.info?t.info.logged_in?p`
                            <div secondary>
                              ${this.hass.localize("ui.panel.config.cloud.description_login","email",t.info.email)}
                            </div>
                          `:p`
                            <div secondary>
                              ${this.hass.localize("ui.panel.config.cloud.description_features")}
                            </div>
                          `:p`
                          <div secondary>
                            ${t.description||this.hass.localize(`ui.panel.config.dashboard.${t.translationKey}.description`)}
                          </div>
                        `}
                  </paper-item-body>
                  ${this.narrow?"":p`<ha-icon-next></ha-icon-next>`}
                </paper-icon-item>
              </a>
            `:""})}
    `}},{kind:"method",key:"_entryClicked",value:function(t){t.currentTarget.blur(),t.currentTarget.parentElement.href.endsWith("#external-app-configuration")&&(t.preventDefault(),this.hass.auth.external.fireMessage({type:"config_screen/show"}))}},{kind:"get",static:!0,key:"styles",value:function(){return u`
      a {
        text-decoration: none;
        color: var(--primary-text-color);
        position: relative;
        display: block;
        outline: 0;
      }
      ha-svg-icon,
      ha-icon-next {
        color: var(--secondary-text-color);
        height: 24px;
        width: 24px;
      }
      ha-svg-icon {
        padding: 8px;
      }
      .iron-selected paper-item::before,
      a:not(.iron-selected):focus::before {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        pointer-events: none;
        content: "";
        transition: opacity 15ms linear;
        will-change: opacity;
      }
      a:not(.iron-selected):focus::before {
        background-color: currentColor;
        opacity: var(--dark-divider-opacity);
      }
      .iron-selected paper-item:focus::before,
      .iron-selected:focus paper-item::before {
        opacity: 0.2;
      }
      .icon-background {
        border-radius: 50%;
      }
      .icon-background ha-svg-icon {
        color: #fff;
      }
    `}}]}}),h),c([f("ha-config-section")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d()],key:"isWide",value:()=>!1},{kind:"field",decorators:[d({type:Boolean})],key:"vertical",value:()=>!1},{kind:"field",decorators:[d({type:Boolean,attribute:"full-width"})],key:"fullWidth",value:()=>!1},{kind:"method",key:"render",value:function(){return p`
      <div
        class="content ${g({narrow:!this.isWide,"full-width":this.fullWidth})}"
      >
        <div class="header"><slot name="header"></slot></div>
        <div
          class="together layout ${g({narrow:!this.isWide,vertical:this.vertical||!this.isWide,horizontal:!this.vertical&&this.isWide})}"
        >
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return u`
      :host {
        display: block;
      }
      .content {
        padding: 28px 20px 0;
        max-width: 1040px;
        margin: 0 auto;
      }

      .layout {
        display: flex;
      }

      .horizontal {
        flex-direction: row;
      }

      .vertical {
        flex-direction: column;
      }

      .flex-auto {
        flex: 1 1 auto;
      }

      .header {
        font-family: var(--paper-font-headline_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-headline_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        letter-spacing: var(--paper-font-headline_-_letter-spacing);
        line-height: var(--paper-font-headline_-_line-height);
        opacity: var(--dark-primary-opacity);
      }

      .together {
        margin-top: 32px;
      }

      .intro {
        font-family: var(--paper-font-subhead_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-subhead_-_-webkit-font-smoothing
        );
        font-weight: var(--paper-font-subhead_-_font-weight);
        line-height: var(--paper-font-subhead_-_line-height);
        width: 100%;
        opacity: var(--dark-primary-opacity);
        font-size: 14px;
        padding-bottom: 20px;
      }

      .horizontal .intro {
        max-width: 400px;
        margin-right: 40px;
      }

      .panel {
        margin-top: -24px;
      }

      .panel ::slotted(*) {
        margin-top: 24px;
        display: block;
      }

      .narrow.content {
        max-width: 640px;
      }
      .narrow .together {
        margin-top: 20px;
      }
      .narrow .intro {
        padding-bottom: 20px;
        margin-right: 0;
        max-width: 500px;
      }

      .full-width {
        padding: 0;
      }

      .full-width .layout {
        flex-direction: column;
      }
    `}}]}}),h);const B=y(t=>{var e,i,o;const s=[],a=[],n=[];var r,l;return t.repositories.forEach(e=>{var i;if("pending-restart"===e.status&&n.push(e),t.addedToLovelace(t,e)||a.push(e),e.installed&&null!==(i=t.removed.map(t=>t.repository))&&void 0!==i&&i.includes(e.full_name)){const i=t.removed.find(t=>t.repository===e.full_name);s.push({name:t.localize("entry.messages.removed_repository",{repository:i.repository}),info:i.reason,severity:"error",dialog:"remove",repository:e})}}),null!==(e=t.status)&&void 0!==e&&e.startup&&["setup","waiting","startup"].includes(t.status.stage)&&s.push({name:t.localize(`entry.messages.${t.status.stage}.title`),info:t.localize(`entry.messages.${t.status.stage}.content`),severity:"warning"}),null!==(i=t.status)&&void 0!==i&&i.has_pending_tasks&&s.push({name:t.localize("entry.messages.has_pending_tasks.title"),info:t.localize("entry.messages.has_pending_tasks.content"),severity:"warning"}),null!==(o=t.status)&&void 0!==o&&o.disabled?[{name:t.localize("entry.messages.disabled.title"),secondary:t.localize(`entry.messages.disabled.${null===(r=t.status)||void 0===r?void 0:r.disabled_reason}.title`),info:t.localize(`entry.messages.disabled.${null===(l=t.status)||void 0===l?void 0:l.disabled_reason}.description`),severity:"error"}]:(a.length>0&&s.push({name:t.localize("entry.messages.resources.title"),info:t.localize("entry.messages.resources.content",{number:a.length}),severity:"error"}),n.length>0&&s.push({name:t.localize("entry.messages.restart.title"),path:"/config/server_control",info:t.localize("entry.messages.restart.content",{number:n.length,pluralWording:1===n.length?t.localize("common.integration"):t.localize("common.integration_plural")}),severity:"error"}),s)});let W=c([f("hacs-entry-panel")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[d({attribute:!1})],key:"hacs",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[d({type:Boolean})],key:"narrow",value:void 0},{kind:"method",key:"render",value:function(){var t,e;const i=[],o=[],s=B(this.hacs);this.hacs.repositories.forEach(t=>{t.pending_upgrade&&i.push(t)}),s.forEach(t=>{o.push({iconPath:_,name:t.name,info:t.info,secondary:t.secondary,path:t.path||"",severity:t.severity,dialog:t.dialog,repository:t.repository})}),this.dispatchEvent(new CustomEvent("update-hacs",{detail:{messages:o,updates:i},bubbles:!0,composed:!0}));const a=p`
      <ha-config-section .narrow=${this.narrow} .isWide=${this.isWide}>
        <div slot="header">${this.narrow?"HACS":"Home Assistant Community Store"}</div>

        <div slot="introduction">
          ${0!==(null===(t=this.hacs.messages)||void 0===t?void 0:t.length)?this.hacs.messages.map(t=>p`
                    <ha-alert
                      .alertType=${t.severity}
                      .title=${t.secondary?`${t.name} - ${t.secondary}`:t.name}
                      .rtl=${$(this.hass)}
                    >
                      ${t.info}
                      <mwc-button
                        slot="action"
                        .label=${t.path?this.hacs.localize("common.navigate"):t.dialog?this.hacs.localize("common."+t.dialog):""}
                        @click=${()=>t.path?m(t.path):this._openDialog(t)}
                      >
                      </mwc-button>
                    </ha-alert>
                  `):this.narrow?"":this.hacs.localize("entry.intro")}
        </div>

        ${0!==(null===(e=this.hacs.updates)||void 0===e?void 0:e.length)?p` <ha-card>
              ${(n=this.hacs.updates,null==n?void 0:n.sort((t,e)=>t.name.toLowerCase()>e.name.toLowerCase()?1:-1)).map(t=>p`
                    <ha-alert .title=${t.name} .rtl=${$(this.hass)}>
                      ${this.hacs.localize("sections.pending_repository_upgrade",{downloaded:t.installed_version,available:t.available_version})}
                      <mwc-button
                        slot="action"
                        .label=${this.hacs.localize("common.update")}
                        @click=${()=>this._openUpdateDialog(t)}
                      >
                      </mwc-button>
                    </ha-alert>
                  `)}
            </ha-card>`:""}

        <ha-card>
          <ha-config-navigation .hass=${this.hass} .pages=${this.hacs.sections}>
          </ha-config-navigation>
        </ha-card>

        <ha-card>
          ${C(this.hass,"hassio")?p`
                <paper-icon-item @click=${this._openSupervisorDialog}>
                  <ha-svg-icon .path=${v} slot="item-icon"></ha-svg-icon>
                  <paper-item-body two-line>
                    ${this.hacs.localize("sections.addon.title")}
                    <div secondary>${this.hacs.localize("sections.addon.description")}</div>
                  </paper-item-body>
                  <ha-svg-icon right .path=${b}></ha-svg-icon>
                </paper-icon-item>
              `:""}
        </ha-card>

        <ha-card>
          <paper-icon-item @click=${this._openAboutDialog}>
            <ha-svg-icon .path=${w} slot="item-icon"></ha-svg-icon>
            <paper-item-body two-line>
              ${this.hacs.localize("sections.about.title")}
              <div secondary>${this.hacs.localize("sections.about.description")}</div>
            </paper-item-body>
          </paper-icon-item>
        </ha-card>
      </ha-config-section>
    `;var n;return this.narrow||"always_hidden"===this.hass.dockedSidebar?p`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button .hass=${this.hass} .narrow=${this.narrow}></ha-menu-button>
          </app-toolbar>
        </app-header>
        ${a}
      </ha-app-layout>
    `:a}},{kind:"method",key:"_openDialog",value:function(t){t.dialog&&("remove"==t.dialog&&(t.dialog="removed"),this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:t.dialog,repository:t.repository},bubbles:!0,composed:!0})))}},{kind:"method",key:"_openUpdateDialog",value:function(t){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"update",repository:t.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_openAboutDialog",value:async function(){E(this,this.hacs)}},{kind:"method",key:"_openSupervisorDialog",value:async function(){this.dispatchEvent(new CustomEvent("hacs-dialog",{detail:{type:"navigate",path:"/hassio"},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[k,T,u`
        paper-icon-item {
          cursor: pointer;
        }

        app-header {
          --app-header-background-color: var(--primary-background-color);
        }

        ha-svg-icon {
          color: var(--secondary-text-color);
        }

        ha-config-section {
          color: var(--primary-text-color);
          margin-top: -12px;
        }

        paper-item-body {
          width: 100%;
          min-height: var(--paper-item-body-two-line-min-height, 72px);
          display: var(--layout-vertical_-_display);
          flex-direction: var(--layout-vertical_-_flex-direction);
          justify-content: var(--layout-center-justified_-_justify-content);
        }
        paper-item-body,
        ha-menu-button {
          color: var(--hcv-text-color-primary);
        }
        paper-item-body div {
          font-size: 14px;
          color: var(--hcv-text-color-secondary);
        }
        div[secondary] {
          white-space: normal;
        }
      `]}}]}}),h);export{W as HacsEntryPanel};
