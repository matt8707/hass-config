import{_ as t,H as e,e as i,a as s,m as a,p as r,o,b as n,s as l,c as d,d as c,r as h,n as p}from"./main-8113c4f2.js";import"./c.503c02b0.js";import{s as u}from"./c.49d907c6.js";import{f}from"./c.e55b72cd.js";import"./c.e18d1287.js";import"./c.214dd6fa.js";import"./c.868d2b7c.js";import"./c.9f27b448.js";import"./c.58dcfe74.js";import"./c.33d2c1b4.js";import"./c.7b6b3e8b.js";import"./c.e709cbfb.js";import"./c.0a038163.js";const m=["stars","last_updated","name"];let g=t([p("hacs-add-repository-dialog")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[i({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[i({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[i()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[i()],key:"_sortBy",value:()=>m[0]},{kind:"field",decorators:[i()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(t){return t.forEach((t,e)=>{"hass"===e&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))}),t.has("narrow")||t.has("filters")||t.has("active")||t.has("_searchInput")||t.has("_load")||t.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(t,e)=>null==t?void 0:t.filter(t=>{var i,s;return!t.installed&&(null===(i=this.hacs.sections)||void 0===i||null===(s=i.find(t=>t.id===this.section).categories)||void 0===s?void 0:s.includes(t.category))&&!t.installed&&(null==e?void 0:e.includes(t.category))})}},{kind:"method",key:"firstUpdated",value:async function(){var t;if(this.addEventListener("filter-change",t=>this._updateFilters(t)),0===(null===(t=this.filters)||void 0===t?void 0:t.length)){var e;const t=null===(e=s(this.hacs.language,this.route))||void 0===e?void 0:e.categories;null==t||t.filter(t=>{var e;return null===(e=this.hacs.configuration)||void 0===e?void 0:e.categories.includes(t)}).forEach(t=>{this.filters.push({id:t,value:t,checked:!0})}),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(t){const e=this.filters.find(e=>e.id===t.detail.id);this.filters.find(t=>t.id===e.id).checked=!e.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>a(f)},{kind:"method",key:"render",value:function(){var t;if(!this.active)return r``;this._searchInput=window.localStorage.getItem("hacs-search")||"";let e=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(t=this.hacs.configuration)||void 0===t?void 0:t.categories),this._searchInput);return 0!==this.filters.length&&(e=e.filter(t=>{var e;return null===(e=this.filters.find(e=>e.id===t.category))||void 0===e?void 0:e.checked})),r`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.hacs.localize("dialog_add_repo.title")}
        hideActions
        scrimClickAction
        escapeKeyAction
        maxWidth
      >
        <div class="searchandfilter" ?narrow=${this.narrow}>
          <search-input
            .hass=${this.hass}
            no-label-float
            .label=${this.hacs.localize("search.placeholder")}
            .filter=${this._searchInput}
            @value-changed=${this._inputValueChanged}
            ?narrow=${this.narrow}
          ></search-input>
          <mwc-select
            ?narrow=${this.narrow}
            .label=${this.hacs.localize("dialog_add_repo.sort_by")}
            .value=${this._sortBy}
            @selected=${t=>this._sortBy=t.currentTarget.value}
            @closed=${u}
          >
            ${m.map(t=>r`<mwc-list-item .value=${t}>
                  ${this.hacs.localize("store."+t)}
                </mwc-list-item>`)}
          </mwc-select>
        </div>
        ${this.filters.length>1?r`<div class="filters">
              <hacs-filter .hacs=${this.hacs} .filters="${this.filters}"></hacs-filter>
            </div>`:""}
        <div class=${o({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${o({list:!0,narrow:this.narrow})}>
            ${e.sort((t,e)=>"name"===this._sortBy?t.name.toLocaleLowerCase()<e.name.toLocaleLowerCase()?-1:1:t[this._sortBy]>e[this._sortBy]?-1:1).slice(0,this._load).map(t=>{return r` <ha-settings-row
                  class=${o({narrow:this.narrow})}
                  @click=${()=>this._openInformation(t)}
                >
                  ${this.narrow?"":"integration"===t.category?r`
                          <img
                            slot="prefix"
                            loading="lazy"
                            .src=${e={domain:t.domain,darkOptimized:this.hass.themes.darkMode,type:"icon"},`https://brands.home-assistant.io/${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`}
                            referrerpolicy="no-referrer"
                            @error=${this._onImageError}
                            @load=${this._onImageLoad}
                          />
                        `:""}
                  <span slot="heading"> ${t.name} </span>
                  <span slot="description">${t.description}</span>
                  ${"integration"!==t.category?r`<ha-chip>${this.hacs.localize("common."+t.category)}</ha-chip> `:""}
                </ha-settings-row>`;var e})}
            ${0===e.length?r`<p>${this.hacs.localize("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(t){const e=t.target.scrollTop;e>=this._top?this._load+=1:this._load-=1,this._top=e}},{kind:"method",key:"_inputValueChanged",value:function(t){this._searchInput=t.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(t){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:t.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(t){t.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(t){t.target&&(t.target.outerHTML=`<ha-svg-icon path="${n}" slot="prefix"></ha-svg-icon>`)}},{kind:"get",static:!0,key:"styles",value:function(){return[l,d,c,h`
        .content {
          width: 100%;
          overflow: auto;
          max-height: 70vh;
        }

        .filter {
          margin-top: -12px;
          display: flex;
          width: 200px;
          float: right;
        }

        .list {
          margin-top: 16px;
          width: 1024px;
          max-width: 100%;
        }
        ha-svg-icon {
          --mdc-icon-size: 36px;
          margin-right: 6px;
        }
        search-input {
          float: left;
          width: 75%;
          border-bottom: 1px var(--mdc-theme-primary) solid;
        }
        search-input[narrow],
        mwc-select[narrow] {
          width: 100%;
          margin: 4px 0;
        }
        img {
          align-items: center;
          display: block;
          justify-content: center;
          margin-right: 6px;
          margin-bottom: 16px;
          max-height: 36px;
          max-width: 36px;
        }

        .filters {
          width: 100%;
          display: flex;
        }

        hacs-filter {
          width: 100%;
          margin-left: -32px;
        }

        ha-settings-row {
          padding: 0px 16px 0 0;
          cursor: pointer;
        }

        .searchandfilter {
          display: flex;
          justify-content: space-between;
          align-items: self-end;
        }

        .searchandfilter[narrow] {
          flex-direction: column;
        }
      `]}}]}}),e);export{g as HacsAddRepositoryDialog};
