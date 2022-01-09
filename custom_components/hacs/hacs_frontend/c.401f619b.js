import{_ as e,H as t,e as i,a,m as s,p as r,o,b as n,s as l,c,d,r as h,n as p}from"./main-25487c89.js";import"./c.1122ce3c.js";import{s as u}from"./c.cac1db56.js";import{f}from"./c.e579cfcf.js";import"./c.2963adcf.js";import"./c.b0c172e8.js";import"./c.7a168374.js";import"./c.9f27b448.js";import"./c.d0e4127a.js";import"./c.e4c27bcc.js";import"./c.e80b707a.js";import"./c.619fb63b.js";import"./c.0a038163.js";const m=["stars","last_updated","name"];let g=e([p("hacs-add-repository-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:()=>[]},{kind:"field",decorators:[i({type:Number})],key:"_load",value:()=>30},{kind:"field",decorators:[i({type:Number})],key:"_top",value:()=>0},{kind:"field",decorators:[i()],key:"_searchInput",value:()=>""},{kind:"field",decorators:[i()],key:"_sortBy",value:()=>m[0]},{kind:"field",decorators:[i()],key:"section",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return e.forEach((e,t)=>{"hass"===t&&(this.sidebarDocked='"docked"'===window.localStorage.getItem("dockedSidebar"))}),e.has("narrow")||e.has("filters")||e.has("active")||e.has("_searchInput")||e.has("_load")||e.has("_sortBy")}},{kind:"field",key:"_repositoriesInActiveCategory",value(){return(e,t)=>null==e?void 0:e.filter(e=>{var i,a;return!e.installed&&(null===(i=this.hacs.sections)||void 0===i||null===(a=i.find(e=>e.id===this.section).categories)||void 0===a?void 0:a.includes(e.category))&&!e.installed&&(null==t?void 0:t.includes(e.category))})}},{kind:"method",key:"firstUpdated",value:async function(){var e;if(this.addEventListener("filter-change",e=>this._updateFilters(e)),0===(null===(e=this.filters)||void 0===e?void 0:e.length)){var t;const e=null===(t=a(this.hacs.language,this.route))||void 0===t?void 0:t.categories;null==e||e.filter(e=>{var t;return null===(t=this.hacs.configuration)||void 0===t?void 0:t.categories.includes(e)}).forEach(e=>{this.filters.push({id:e,value:e,checked:!0})}),this.requestUpdate("filters")}}},{kind:"method",key:"_updateFilters",value:function(e){const t=this.filters.find(t=>t.id===e.detail.id);this.filters.find(e=>e.id===t.id).checked=!t.checked,this.requestUpdate("filters")}},{kind:"field",key:"_filterRepositories",value:()=>s(f)},{kind:"method",key:"render",value:function(){var e;if(!this.active)return r``;this._searchInput=window.localStorage.getItem("hacs-search")||"";let t=this._filterRepositories(this._repositoriesInActiveCategory(this.repositories,null===(e=this.hacs.configuration)||void 0===e?void 0:e.categories),this._searchInput);return 0!==this.filters.length&&(t=t.filter(e=>{var t;return null===(t=this.filters.find(t=>t.id===e.category))||void 0===t?void 0:t.checked})),r`
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
            @selected=${e=>this._sortBy=e.currentTarget.value}
            @closed=${u}
          >
            ${m.map(e=>r`<mwc-list-item .value=${e}>
                  ${this.hacs.localize("dialog_add_repo.sort_by_values."+e)||e}
                </mwc-list-item>`)}
          </mwc-select>
        </div>
        ${this.filters.length>1?r`<div class="filters">
              <hacs-filter .hacs=${this.hacs} .filters="${this.filters}"></hacs-filter>
            </div>`:""}
        <div class=${o({content:!0,narrow:this.narrow})} @scroll=${this._loadMore}>
          <div class=${o({list:!0,narrow:this.narrow})}>
            ${t.sort((e,t)=>"name"===this._sortBy?e.name.toLocaleLowerCase()<t.name.toLocaleLowerCase()?-1:1:e[this._sortBy]>t[this._sortBy]?-1:1).slice(0,this._load).map(e=>{return r` <ha-settings-row
                  class=${o({narrow:this.narrow})}
                  @click=${()=>this._openInformation(e)}
                >
                  ${this.narrow?"":"integration"===e.category?r`
                          <img
                            slot="prefix"
                            loading="lazy"
                            .src=${t={domain:e.domain,darkOptimized:this.hass.themes.darkMode,type:"icon"},`https://brands.home-assistant.io/${t.useFallback?"_/":""}${t.domain}/${t.darkOptimized?"dark_":""}${t.type}.png`}
                            referrerpolicy="no-referrer"
                            @error=${this._onImageError}
                            @load=${this._onImageLoad}
                          />
                        `:""}
                  <span slot="heading"> ${e.name} </span>
                  <span slot="description">${e.description}</span>
                  ${"integration"!==e.category?r`<ha-chip>${this.hacs.localize("common."+e.category)}</ha-chip> `:""}
                </ha-settings-row>`;var t})}
            ${0===t.length?r`<p>${this.hacs.localize("dialog_add_repo.no_match")}</p>`:""}
          </div>
        </div>
      </hacs-dialog>
    `}},{kind:"method",key:"_loadMore",value:function(e){const t=e.target.scrollTop;t>=this._top?this._load+=1:this._load-=1,this._top=t}},{kind:"method",key:"_inputValueChanged",value:function(e){this._searchInput=e.detail.value,window.localStorage.setItem("hacs-search",this._searchInput)}},{kind:"method",key:"_openInformation",value:function(e){this.dispatchEvent(new CustomEvent("hacs-dialog-secondary",{detail:{type:"repository-info",repository:e.id},bubbles:!0,composed:!0}))}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.visibility="initial"}},{kind:"method",key:"_onImageError",value:function(e){e.target&&(e.target.outerHTML=`<ha-svg-icon path="${n}" slot="prefix"></ha-svg-icon>`)}},{kind:"get",static:!0,key:"styles",value:function(){return[l,c,d,h`
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
      `]}}]}}),t);export{g as HacsAddRepositoryDialog};
