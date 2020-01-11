console.info(
  `%c COMPACT-CUSTOM-HEADER \n%c     Version 1.4.9     `,
  "color: orange; font-weight: bold; background: black",
  "color: white; font-weight: bold; background: dimgray"
);

class CompactCustomHeader {
  constructor() {
    this.LitElement = Object.getPrototypeOf(
      customElements.get("ha-panel-lovelace")
    );
    this.hass = document.querySelector("home-assistant").hass;
    this.fireEvent = (node, type, detail, options = {}) => {
      detail = detail === null || detail === undefined ? {} : detail;
      const event = new Event(type, {
        bubbles: options.bubbles === undefined ? true : options.bubbles,
        cancelable: Boolean(options.cancelable),
        composed: options.composed === undefined ? true : options.composed
      });
      event.detail = detail;
      node.dispatchEvent(event);
      return event;
    };

    let ll = document.querySelector("home-assistant");
    ll = ll && ll.shadowRoot;
    ll = ll && ll.querySelector("home-assistant-main");
    this.main = ll;
    ll = ll && ll.shadowRoot;
    ll = ll && ll.querySelector("app-drawer-layout partial-panel-resolver");
    this.panelResolver = ll;
    ll = (ll && ll.shadowRoot) || ll;
    ll = ll && ll.querySelector("ha-panel-lovelace");
    ll = ll && ll.shadowRoot;
    ll = ll && ll.querySelector("hui-root");
    this.lovelace = ll.lovelace;
    this.root = ll.shadowRoot;

    this.frontendVersion = Number(window.frontendVersion);
    this.newSidebar = this.frontendVersion >= 20190710;
    this.header = this.root.querySelector("app-header");
    this.editMode = this.header.className == "edit-mode";
    this.view = this.root.querySelector("ha-app-layout #view");

    this.sidebarClosed = false;
    this.firstRun = true;
    this.buttons = {};
    this.prevColor = {};

    this.defaultConfig = {
      header: true,
      disable: false,
      yaml_editor: false,
      menu: "show",
      voice: "show",
      notifications: "show",
      options: "show",
      clock_format: 12,
      clock_am_pm: true,
      clock_date: false,
      date_locale: this.hass.language,
      chevrons: false,
      redirect: true,
      background: "",
      hide_tabs: "",
      show_tabs: "",
      edit_mode_show_tabs: false,
      default_tab: "",
      default_tab_template: "",
      kiosk_mode: false,
      sidebar_swipe: true,
      sidebar_closed: false,
      disable_sidebar: false,
      hide_help: false,
      hide_config: false,
      hide_unused: false,
      tab_color: {},
      button_color: {},
      statusbar_color: "",
      swipe: false,
      swipe_amount: "15",
      swipe_animate: "none",
      swipe_skip: "",
      swipe_wrap: true,
      swipe_prevent_default: false,
      swipe_skip_hidden: true,
      warning: true,
      compact_header: true,
      view_css: "",
      time_css: "",
      date_css: "",
      header_css: "",
      tab_css: {},
      button_css: {}
    };

    this.cchConfig = this.buildConfig(
      this.lovelace.config.cch || {},
      this.hass.user.name
    );
  }

  run() {
    const tabContainer = this.root.querySelector("paper-tabs");
    const tabs = tabContainer
      ? Array.from(tabContainer.querySelectorAll("paper-tab"))
      : [];
    let disabled =
      window.location.href.includes("disable_cch") || this.cchConfig.disable;

    if (this.firstRun || this.buttons == undefined) {
      this.buttons = this.getButtonElements(tabContainer);
    }
    if (!this.buttons.menu || !this.buttons.options || this.editMode) return;
    if (!disabled) {
      this.insertEditMenu(tabs);
      this.hideMenuItems();
      this.styleHeader(tabContainer, tabs);
      this.styleButtons(tabs, tabContainer);
      if (this.firstRun) this.sidebarMod();
      this.hideTabs(tabContainer, tabs);
      for (let button in this.buttons) {
        if (this.cchConfig[button] == "clock") this.insertClock(button);
      }
      if (!this.editMode) this.tabContainerMargin(tabContainer);
      if (this.cchConfig.swipe) this.swipeNavigation(tabs, tabContainer);
      if (this.firstRun) this.defaultTab(tabs, tabContainer);
    }
    if (this.firstRun) {
      this.observers(tabContainer, tabs, disabled);
      this.breakingChangeNotification();
    }
    this.firstRun = false;
    this.fireEvent(this.header, "iron-resize");
  }

  buildConfig(config, user_name) {
    let exceptionConfig = {};
    let highestMatch = 0;
    // Count number of matching conditions and choose config with most matches.
    if (config.exceptions) {
      config.exceptions.forEach(exception => {
        const matches = countMatches(exception.conditions, user_name);
        if (matches > highestMatch) {
          highestMatch = matches;
          exceptionConfig = exception.config;
        }
      });
    }
    // If exception config uses hide_tabs and main config uses show_tabs,
    // delete show_tabs and vice versa.
    if (
      exceptionConfig.hide_tabs &&
      config.show_tabs &&
      exceptionConfig.hide_tabs.length &&
      config.show_tabs.length
    ) {
      delete config.show_tabs;
    } else if (
      exceptionConfig.show_tabs &&
      config.hide_tabs &&
      exceptionConfig.show_tabs.length &&
      config.hide_tabs.length
    ) {
      delete config.hide_tabs;
    }

    return { ...this.defaultConfig, ...config, ...exceptionConfig };

    function countMatches(conditions, user_name) {
      const userVars = {
        user: user_name,
        user_agent: navigator.userAgent
      };
      let count = 0;
      for (const cond in conditions) {
        if (cond == "user" && conditions[cond].includes(",")) {
          conditions[cond].split(/[ ,]+/).forEach(user => {
            if (userVars[cond] == user) count++;
          });
        } else {
          if (
            userVars[cond] == conditions[cond] ||
            (cond == "query_string" &&
              window.location.search.includes(conditions[cond])) ||
            (cond == "user_agent" &&
              userVars[cond].includes(conditions[cond])) ||
            (cond == "media_query" &&
              window.matchMedia(conditions[cond]).matches)
          ) {
            count++;
          } else {
            return 0;
          }
        }
      }
      return count;
    }
  }

  observers(tabContainer, tabs, disabled) {
    // Watch for changes in Lovelace.
    const callback = mutations => {
      // Theme changed.
      if (mutations[0].target.nodeName == "HTML") {
        mutations = [mutations[0]];
        this.styleHeader(tabContainer, tabs);
        this.conditionalStyling(tabs);
        return;
      }
      mutations.forEach(({ addedNodes, target }) => {
        if (addedNodes.length && target.nodeName == "PARTIAL-PANEL-RESOLVER") {
          // Navigated back to lovelace from elsewhere in HA.
          this.buttons = this.getButtonElements();
          this.run();
        } else if (target.className == "edit-mode" && addedNodes.length) {
          // Entered edit mode.
          this.editMode = true;
          if (!disabled) this.removeStyles(tabContainer, tabs, this.header);
          this.buttons.options = this.root.querySelector("paper-menu-button");
          this.insertEditMenu(tabs);
          this.fireEvent(this.header, "iron-resize");
        } else if (target.nodeName == "APP-HEADER" && addedNodes.length) {
          // Exited edit mode.
          let editor = this.root
            .querySelector("ha-app-layout")
            .querySelector("editor");
          if (editor) {
            this.root.querySelector("ha-app-layout").removeChild(editor);
          }
          for (let node of addedNodes) {
            if (node.nodeName == "APP-TOOLBAR") {
              this.editMode = false;
              this.buttons = this.getButtonElements();
              this.root.querySelectorAll("[id^='cch']").forEach(style => {
                style.remove();
              });
              setTimeout(() => {
                this.run();
                if (!disabled) this.conditionalStyling(tabs, this.header);
              }, 100);
            }
          }
        } else if (
          // Viewing unused entities
          this.frontendVersion < 20190911 &&
          addedNodes.length &&
          !addedNodes[0].nodeName == "HUI-UNUSED-ENTITIES"
        ) {
          let editor = this.root
            .querySelector("ha-app-layout")
            .querySelector("editor");
          if (editor) {
            this.root.querySelector("ha-app-layout").removeChild(editor);
          }
          if (this.cchConfig.conditional_styles) {
            this.buttons = this.getButtonElements(tabContainer);
            this.conditionalStyling(tabs, this.header);
          }
        } else if (target.id == "view" && addedNodes.length) {
          // Navigating to new tab/view.
          this.run();
          if (tabContainer) this.scrollTabIconIntoView();
        }
      });
    };
    let observer = new MutationObserver(callback);
    observer.observe(this.panelResolver, { childList: true });
    observer.observe(document.querySelector("html"), { attributes: true });
    observer.observe(this.view, { childList: true });
    observer.observe(this.root.querySelector("app-header"), {
      childList: true
    });

    if (!disabled) {
      // Watch for changes in entities.
      window.hassConnection.then(({ conn }) => {
        conn.socket.onmessage = () => {
          if (this.cchConfig.conditional_styles && !this.editMode) {
            this.conditionalStyling(tabs, this.header);
          }
        };
      });
    }
  }

  getButtonElements(disabled) {
    let buttons = {};
    buttons.options = this.root.querySelector("paper-menu-button");
    if (!this.editMode) {
      buttons.menu = this.root.querySelector("ha-menu-button");
      buttons.voice =
        this.root.querySelector("ha-start-voice-button") ||
        this.root.querySelector('[icon="hass:microphone"]');
      if (!this.newSidebar) {
        buttons.notifications = this.root.querySelector(
          "hui-notifications-button"
        );
      }
    }
    // Remove space taken up by "hidden" menu button anytime we get buttons.
    if (
      buttons.menu &&
      buttons.menu.style.visibility == "hidden" &&
      !disabled
    ) {
      buttons.menu.style.display = "none";
    } else if (buttons.menu) {
      buttons.menu.style.display = "";
    }
    return buttons;
  }

  tabContainerMargin(tabContainer) {
    let marginRight = 0;
    let marginLeft = 15;
    for (const button in this.buttons) {
      if (!this.buttons[button]) continue;
      let paperIconButton =
        this.buttons[button].querySelector("paper-icon-button") ||
        this.buttons[button].shadowRoot.querySelector("paper-icon-button");
      let visible = paperIconButton
        ? this.buttons[button].style.display !== "none" &&
          !paperIconButton.hasAttribute("hidden")
        : this.buttons[button].style.display !== "none";
      if (this.cchConfig[button] == "show" && visible) {
        if (button == "menu") marginLeft += 45;
        else marginRight += 45;
      } else if (this.cchConfig[button] == "clock" && visible) {
        const clockWidth =
          (this.cchConfig.clock_format == 12 && this.cchConfig.clock_am_pm) ||
          this.cchConfig.clock_date
            ? 110
            : 80;
        if (button == "menu") marginLeft += clockWidth + 15;
        else marginRight += clockWidth;
      }
    }
    if (tabContainer) {
      tabContainer.style.marginRight = `${marginRight}px`;
      tabContainer.style.marginLeft = `${marginLeft}px`;
    }
  }

  scrollTabIconIntoView() {
    let paperTabs = this.root.querySelector("paper-tabs");
    let currentTab = paperTabs.querySelector(".iron-selected");
    if (!paperTabs || !currentTab) return;
    let tab = currentTab.getBoundingClientRect();
    let container = paperTabs.shadowRoot
      .querySelector("#tabsContainer")
      .getBoundingClientRect();
    // If tab's icon isn't in view scroll it in.
    if (container.right < tab.right || container.left > tab.left) {
      if ("scrollMarginInline" in document.documentElement.style) {
        currentTab.scrollIntoView({ inline: "center" });
      } else if (Element.prototype.scrollIntoViewIfNeeded) {
        currentTab.scrollIntoViewIfNeeded(true);
      } else {
        currentTab.scrollIntoView();
      }
    }
  }

  hideMenuItems() {
    // Hide items in options menu.
    if (
      this.cchConfig.hide_help ||
      this.cchConfig.hide_config ||
      this.cchConfig.hide_unused
    ) {
      const localized = (item, string) => {
        let localString = this.hass.localize(
          `ui.panel.lovelace.menu.${string}`
        );
        return (
          item.innerHTML.includes(localString) ||
          item.getAttribute("aria-label") == localString
        );
      };
      this.buttons.options
        .querySelector("paper-listbox")
        .querySelectorAll("paper-item")
        .forEach(item => {
          if (
            (this.cchConfig.hide_help && localized(item, "help")) ||
            (this.cchConfig.hide_unused &&
              localized(item, "unused_entities")) ||
            (this.cchConfig.hide_config && localized(item, "configure_ui"))
          ) {
            item.parentNode.removeChild(item);
          }
        });
    }
  }

  insertEditMenu(tabs, disabled) {
    if (
      this.buttons.options &&
      (this.editMode ||
        (this.lovelace.mode == "yaml" && this.cchConfig.yaml_editor))
    ) {
      // If any tabs are hidden, add "show all tabs" option.
      if (this.cchConfig.hide_tabs && !this.cchConfig.edit_mode_show_tabs) {
        let show_tabs = document.createElement("paper-item");
        show_tabs.setAttribute("id", "show_tabs");
        show_tabs.addEventListener("click", () => {
          for (let i = 0; i < tabs.length; i++) {
            tabs[i].style.removeProperty("display");
          }
        });
        show_tabs.innerHTML = "Show all tabs";
        this.insertMenuItem(
          this.buttons.options.querySelector("paper-listbox"),
          show_tabs
        );
      }

      // Add menu item to open CCH settings.
      let cchSettings = document.createElement("paper-item");
      cchSettings.setAttribute("id", "cch_settings");
      cchSettings.addEventListener("click", () => this.showEditor());
      cchSettings.innerHTML = "CCH Settings";
      this.insertMenuItem(
        this.buttons.options.querySelector("paper-listbox"),
        cchSettings
      );
      if (!disabled) this.hideMenuItems();
    }
  }

  removeStyles(tabContainer, tabs, { style }) {
    this.root.querySelector("app-header").style.backgroundColor = "#455a64";
    this.root.querySelectorAll("[id^='cch']").forEach(style => {
      style.remove();
    });
    if (this.cchConfig.tab_css) {
      for (let [key, value] of Object.entries(this.cchConfig.tab_css)) {
        key = this.getViewIndex(key);
        value = value.replace(/: /g, ":").replace(/; /g, ";");
        let css = tabs[key].style.cssText
          .replace(/: /g, ":")
          .replace(/; /g, ";");
        tabs[key].style.cssText = css.replace(value, "");
      }
    }
    if (this.cchConfig.header_css) {
      let value = this.cchConfig.header_css
        .replace(/: /g, ":")
        .replace(/; /g, ";");
      let css = style.cssText.replace(/: /g, ":").replace(/; /g, ";");
      style.cssText = css.replace(value, "");
    }
    if (tabContainer) {
      tabContainer.style.marginLeft = "";
      tabContainer.style.marginRight = "";
    }
    this.view.style = "";
    for (let i = 0; i < tabs.length; i++) {
      tabs[i].style.color = "";
    }
    if (this.cchConfig.edit_mode_show_tabs) {
      for (let i = 0; i < tabs.length; i++) {
        tabs[i].style.removeProperty("display");
      }
    }
    let viewStyle = document.createElement("style");
    viewStyle.setAttribute("id", "cch_view_styling");
    viewStyle.innerHTML = `
    hui-view {
      min-height: 100vh;
    }
    hui-panel-view {
      min-height: calc(100vh - 52px);
    }
    `;
    this.root.appendChild(viewStyle);
  }

  styleHeader(tabContainer, tabs) {
    // Fix for old background config option.
    if (typeof this.cchConfig.background == "boolean") {
      this.cchConfig.background = "";
    }
    this.prevColor.background =
      this.cchConfig.background ||
      getComputedStyle(document.body).getPropertyValue("--cch-background") ||
      getComputedStyle(document.body).getPropertyValue("--primary-color");
    let statusBarColor =
      this.cchConfig.statusbar_color || this.prevColor.background;
    // Match mobile status bar color to header color.
    let themeColor = document.querySelector('[name="theme-color"]');
    let themeColorApple =
      document.querySelector(
        '[name="apple-mobile-web-app-status-bar-style"]'
      ) || document.createElement("meta");
    colorStatusBar(statusBarColor);
    // If browser is idle or in background sometimes theme-color needs reset.
    let observeStatus = new MutationObserver(() => {
      if (themeColor.content != statusBarColor) colorStatusBar(statusBarColor);
    });
    if (this.firstRun) {
      observeStatus.observe(themeColor, {
        attributes: true,
        attributeFilter: ["content"]
      });
    }

    // Adjust view size & padding for new header size.
    if (!this.cchConfig.header || this.cchConfig.kiosk_mode) {
      this.header.style.display = "none";
      this.view.style.minHeight = "100vh";
      if (
        this.frontendVersion >= 20190911 &&
        !this.root.querySelector("#cch_view_styling")
      ) {
        let viewStyle = document.createElement("style");
        viewStyle.setAttribute("id", "cch_view_styling");
        viewStyle.innerHTML = `
        hui-view {
          ${this.cchConfig.view_css ? this.cchConfig.view_css : ""}
        }
        hui-panel-view {
          ${this.cchConfig.view_css ? this.cchConfig.view_css : ""}
        }
        `;
        this.root.appendChild(viewStyle);
      }
    } else {
      this.view.style.minHeight = "100vh";
      this.view.style.marginTop = "-48.5px";
      this.view.style.paddingTop = "48.5px";
      this.view.style.boxSizing = "border-box";
      this.header.style.background = this.prevColor.background;
      this.conditionalStyling(tabs, this.header);
      this.header.querySelector("app-toolbar").style.background = "transparent";
      if (
        this.frontendVersion >= 20190911 &&
        !this.root.querySelector("#cch_view_styling")
      ) {
        let viewStyle = document.createElement("style");
        viewStyle.setAttribute("id", "cch_view_styling");
        viewStyle.innerHTML = `
        hui-view {
          margin-top: -48.5px;
          padding-top: 52px;
          min-height: 100vh;
          ${this.cchConfig.view_css ? this.cchConfig.view_css : ""}
        }
        hui-panel-view {
          margin-top: -52px;
          padding-top: 52px;
          min-height: calc(100vh - 52px);
          ${this.cchConfig.view_css ? this.cchConfig.view_css : ""}
        }
        `;
        this.root.appendChild(viewStyle);
      }
    }

    // Match sidebar elements to header's size.
    if (this.newSidebar && this.cchConfig.compact_header) {
      let sidebar = this.main.shadowRoot.querySelector("ha-sidebar").shadowRoot;
      sidebar.querySelector(".menu").style = "height:49px;";
      sidebar.querySelector("paper-listbox").style =
        "height:calc(100% - 180px);";
    }

    // Current tab icon color.
    let conditionalTabs = this.cchConfig.conditional_styles
      ? JSON.stringify(this.cchConfig.conditional_styles).includes("tab")
      : false;
    if (
      !this.root.querySelector("#cch_iron_selected") &&
      !this.editMode &&
      !conditionalTabs &&
      tabContainer
    ) {
      let style = document.createElement("style");
      style.setAttribute("id", "cch_iron_selected");
      style.innerHTML = `
              .iron-selected {
                ${
                  this.cchConfig.active_tab_color
                    ? `color: ${`${
                        this.cchConfig.active_tab_color
                      } !important`}`
                    : "var(--cch-active-tab-color)"
                }
              }
            `;
      tabContainer.appendChild(style);
    }

    // Style current tab indicator.
    let indicator = this.cchConfig.tab_indicator_color;
    if (
      indicator &&
      !this.root.querySelector("#cch_header_colors") &&
      !this.editMode
    ) {
      let style = document.createElement("style");
      style.setAttribute("id", "cch_header_colors");
      style.innerHTML = `
            paper-tabs {
              ${
                indicator
                  ? `--paper-tabs-selection-bar-color: ${indicator} !important`
                  : "var(--cch-tab-indicator-color) !important"
              }
            }
          `;
      this.root.appendChild(style);
    }

    // Tab's icon color.
    let all_tabs_color =
      this.cchConfig.all_tabs_color || "var(--cch-all-tabs-color)";
    if (
      (this.cchConfig.tab_color &&
        Object.keys(this.cchConfig.tab_color).length) ||
      all_tabs_color
    ) {
      for (let i = 0; i < tabs.length; i++) {
        tabs[i].style.color = this.cchConfig.tab_color[i] || all_tabs_color;
      }
    }

    // Add custom css.
    if (this.cchConfig.tab_css) {
      for (let [key, value] of Object.entries(this.cchConfig.tab_css)) {
        key = this.getViewIndex(key);
        if (tabs[key]) tabs[key].style.cssText += value;
      }
    }
    if (this.cchConfig.header_css)
      this.header.style.cssText += this.cchConfig.header_css;
    if (this.cchConfig.view_css && this.frontendVersion < 20190911) {
      this.view.style.cssText += this.cchConfig.view_css;
    }

    if (tabContainer) {
      // Shift the header up to hide unused portion.
      this.root.querySelector("app-toolbar").style.marginTop = this.cchConfig
        .compact_header
        ? "-64px"
        : "";

      tabs.forEach(({ style }) => {
        style.marginTop = "-1px";
      });

      // Show/hide tab navigation chevrons.
      if (!this.cchConfig.chevrons) {
        let chevron = tabContainer.shadowRoot.querySelectorAll(
          '[icon^="paper-tabs:chevron"]'
        );
        chevron[0].style.display = "none";
        chevron[1].style.display = "none";
      } else {
        // Remove space taken up by "not-visible" chevron.
        let style = document.createElement("style");
        style.setAttribute("id", "cch_chevron");
        style.innerHTML = `
              .not-visible {
                display:none;
              }
            `;
        tabContainer.shadowRoot.appendChild(style);
      }
    }
    function colorStatusBar(statusBarColor) {
      themeColor = document.querySelector("meta[name=theme-color]");
      themeColor.setAttribute("content", statusBarColor);
      themeColor.setAttribute("default-content", statusBarColor);
      if (
        !document.querySelector(
          '[name="apple-mobile-web-app-status-bar-style"]'
        )
      ) {
        themeColorApple.name = "apple-mobile-web-app-status-bar-style";
        themeColorApple.content = statusBarColor;
        document.getElementsByTagName("head")[0].appendChild(themeColorApple);
      } else {
        themeColorApple.setAttribute("content", statusBarColor);
      }
    }
  }

  styleButtons({ length }, tabContainer) {
    let topMargin =
      length > 0 && this.cchConfig.compact_header ? "margin-top:111px;" : "";
    let topMarginMenu =
      length > 0 && this.cchConfig.compact_header ? "margin-top:115px;" : "";
    // Reverse buttons object so "menu" is first in the overflow menu.
    this.buttons = this.reverseObject(this.buttons);
    for (const button in this.buttons) {
      if (!this.buttons[button]) continue;
      if (button == "options" && this.cchConfig[button] == "overflow") {
        this.cchConfig[button] = "show";
      }
      let buttonStyle = `
        z-index:1;
        ${
          button == "menu"
            ? `padding: 8px 0; margin-bottom:5px; ${topMarginMenu}`
            : "padding: 8px;"
        }
        ${
          button == "voice" && this.cchConfig["voice"] == "clock"
            ? "width: 100px; padding:4px;"
            : ""
        }
        ${button == "menu" ? "" : topMargin}
        ${button == "options" ? "margin-right:-5px;" : ""}
      `;
      if (
        this.cchConfig[button] == "show" ||
        this.cchConfig[button] == "clock"
      ) {
        if (button == "menu") {
          let paperIconButton = this.buttons[button].querySelector(
            "paper-icon-button"
          )
            ? this.buttons[button].querySelector("paper-icon-button")
            : this.buttons[button].shadowRoot.querySelector(
                "paper-icon-button"
              );
          if (!paperIconButton) continue;
          paperIconButton.style.cssText = buttonStyle;
        } else {
          this.buttons[button].style.cssText = buttonStyle;
        }
      } else if (this.cchConfig[button] == "overflow") {
        const menu_items = this.buttons.options.querySelector("paper-listbox");
        let paperIconButton = this.buttons[button].querySelector(
          "paper-icon-button"
        )
          ? this.buttons[button].querySelector("paper-icon-button")
          : this.buttons[button].shadowRoot.querySelector("paper-icon-button");
        if (paperIconButton && paperIconButton.hasAttribute("hidden")) {
          continue;
        }
        const id = `menu_item_${button}`;
        if (!menu_items.querySelector(`#${id}`)) {
          const wrapper = document.createElement("paper-item");
          wrapper.setAttribute("id", id);
          wrapper.innerText = this.getTranslation(button);
          wrapper.appendChild(this.buttons[button]);
          wrapper.addEventListener("click", () => {
            paperIconButton.click();
          });
          paperIconButton.style.pointerEvents = "none";
          this.insertMenuItem(menu_items, wrapper);
          if (button == "notifications" && !this.newSidebar) {
            let style = document.createElement("style");
            style.innerHTML = `
                  .indicator {
                    top: 5px;
                    right: 0px;
                    width: 10px;
                    height: 10px;
                    ${
                      this.cchConfig.notify_indicator_color
                        ? `background-color:${
                            this.cchConfig.notify_indicator_color
                          }`
                        : ""
                    }
                  }
                  .indicator > div{
                    display:none;
                  }
                `;
            paperIconButton.parentNode.appendChild(style);
          }
        }
      } else if (this.cchConfig[button] == "hide") {
        this.buttons[button].style.display = "none";
      }
      // Hide menu button if hiding the sidebar.
      if (
        this.newSidebar &&
        (this.cchConfig.kiosk_mode || this.cchConfig.disable_sidebar)
      ) {
        this.buttons.menu.style.display = "none";
      }
    }

    // Remove empty space taken up by hidden menu button.
    if (this.buttons.menu && this.newSidebar && this.firstRun) {
      new MutationObserver(() => {
        if (this.buttons.menu.style.visibility == "hidden") {
          this.buttons.menu.style.display = "none";
        } else {
          this.buttons.menu.style.display = "";
        }
        this.tabContainerMargin(tabContainer);
      }).observe(this.buttons.menu, {
        attributes: true,
        attributeFilter: ["style"]
      });
    }

    // Use color vars set in HA theme.
    this.buttons.menu.style.color = "var(--cch-button-color-menu)";
    if (!this.newSidebar) {
      this.buttons.notifications.style.color =
        "var(--cch-button-color-notifications)";
    }
    if (this.buttons.voice) this.buttons.voice.style.color = "var(--cch-button-color-voice)";
    this.buttons.options.style.color = "var(--cch-button-color-options)";
    if (this.cchConfig.all_buttons_color) {
      this.root.querySelector("app-toolbar").style.color =
        this.cchConfig.all_buttons_color || "var(--cch-all-buttons-color)";
    }

    // Use colors set in CCH config.
    for (const button in this.buttons) {
      if (this.cchConfig.button_color[button]) {
        this.buttons[button].style.color = this.cchConfig.button_color[button];
      }
    }

    // Notification indicator's color for HA 0.96 and above.
    if (
      this.newSidebar &&
      this.cchConfig.menu != "hide" &&
      !this.buttons.menu.shadowRoot.querySelector("#cch_dot")
    ) {
      let style = document.createElement("style");
      style.setAttribute("id", "cch_dot");
      let indicator =
        this.cchConfig.notify_indicator_color ||
        getComputedStyle(this.header).getPropertyValue(
          "--cch-tab-indicator-color"
        ) ||
        "";
      let border = getComputedStyle(this.header)
        .getPropertyValue("background")
        .includes("url")
        ? "border-color: transparent !important"
        : `border-color: ${getComputedStyle(this.header).getPropertyValue(
            "background-color"
          )} !important;`;
      style.innerHTML = `
          .dot {
            ${topMargin}
            z-index: 2;
            ${indicator ? `background: ${indicator} !important` : ""}
            ${border}
          }
      `;
      this.buttons.menu.shadowRoot.appendChild(style);
    } else if (
      // Notification indicator's color for HA 0.95 and below.
      this.cchConfig.notify_indicator_color &&
      this.cchConfig.notifications == "show" &&
      !this.newSidebar
    ) {
      let style = document.createElement("style");
      style.innerHTML = `
            .indicator {
              background-color:${this.cchConfig.notify_indicator_color ||
                "var(--cch-notify-indicator-color)"} !important;
              color: ${this.cchConfig.notify_text_color ||
                "var(--cch-notify-text-color), var(--primary-text-color)"};
            }
          `;
      this.buttons.notifications.shadowRoot.appendChild(style);
    }

    // Add buttons's custom css.
    let buttonCss = this.cchConfig.button_css;
    if (buttonCss) {
      for (const [key, value] of Object.entries(buttonCss)) {
        if (!this.buttons[key]) {
          continue;
        } else {
          this.buttons[key].style.cssText += value;
        }
      }
    }
  }

  getTranslation(button) {
    switch (button) {
      case "notifications":
        return this.hass.localize("ui.notification_drawer.title");
      default:
        return button.charAt(0).toUpperCase() + button.slice(1);
    }
  }

  defaultTab(tabs, tabContainer) {
    let firstTab = tabs.indexOf(tabs.filter(tab => tab.style.display == "")[0]);
    let default_tab = this.cchConfig.default_tab;
    if (typeof default_tab == "object" && !default_tab.length) return;
    let template = this.cchConfig.default_tab_template;
    if ((default_tab || template) && tabContainer) {
      if (template) default_tab = this.templateEval(template, this.hass.states);
      default_tab = this.getViewIndex(default_tab);
      let activeTab = tabs.indexOf(
        tabContainer.querySelector(".iron-selected")
      );
      if (
        activeTab != default_tab &&
        activeTab == firstTab &&
        (!this.cchConfig.redirect ||
          (this.cchConfig.redirect &&
            tabs[default_tab].style.display != "none"))
      ) {
        tabs[default_tab].click();
      }
    }
  }

  sidebarMod() {
    let menu = this.buttons.menu.querySelector("paper-icon-button");
    let sidebar = this.main.shadowRoot.querySelector("app-drawer");

    // HA 0.95 and below
    if (!this.newSidebar) {
      if (!this.cchConfig.sidebar_swipe || this.cchConfig.kiosk_mode) {
        sidebar.removeAttribute("swipe-open");
      }
      if (
        (this.cchConfig.sidebar_closed || this.cchConfig.kiosk_mode) &&
        !this.sidebarClosed
      ) {
        if (sidebar.hasAttribute("opened")) menu.click();
        this.sidebarClosed = true;
      }
      // HA 0.96 and above
    } else if (this.cchConfig.disable_sidebar || this.cchConfig.kiosk_mode) {
      sidebar.style.display = "none";
      sidebar.addEventListener(
        "mouseenter",
        event => {
          event.stopPropagation();
        },
        true
      );
      let style = document.createElement("style");
      style.type = "text/css";
      style.appendChild(
        document.createTextNode(
          ":host(:not([expanded])) {width: 0px !important;}"
        )
      );
      this.main.shadowRoot
        .querySelector("ha-sidebar")
        .shadowRoot.appendChild(style);

      style = document.createElement("style");
      style.type = "text/css";
      style.appendChild(
        document.createTextNode(":host {--app-drawer-width: 0px !important;}")
      );
      this.main.shadowRoot.appendChild(style);
    }
  }

  hideTabs(tabContainer, tabs) {
    let hidden_tabs = String(this.cchConfig.hide_tabs).length
      ? String(this.cchConfig.hide_tabs)
          .replace(/\s+/g, "")
          .split(",")
      : null;
    let shown_tabs = String(this.cchConfig.show_tabs).length
      ? String(this.cchConfig.show_tabs)
          .replace(/\s+/g, "")
          .split(",")
      : null;

    // Set the tab config source.
    if (!hidden_tabs && shown_tabs) {
      let all_tabs = [];
      shown_tabs = this.buildRanges(shown_tabs);
      for (let i = 0; i < tabs.length; i++) all_tabs.push(i);
      // Invert shown_tabs to hidden_tabs.
      hidden_tabs = all_tabs.filter(el => !shown_tabs.includes(el));
    } else {
      hidden_tabs = this.buildRanges(hidden_tabs);
    }

    // Hide tabs.
    for (const tab of hidden_tabs) {
      if (!tabs[tab]) continue;
      tabs[tab].style.display = "none";
    }

    if (this.cchConfig.redirect && tabContainer) {
      const activeTab = tabContainer.querySelector("paper-tab.iron-selected");
      const activeTabIndex = tabs.indexOf(activeTab);
      // Is the current tab hidden and is there at least one tab is visible.
      if (
        hidden_tabs.includes(activeTabIndex) &&
        hidden_tabs.length != tabs.length
      ) {
        let i = 0;
        // Find the first visible tab and navigate.
        while (hidden_tabs.includes(i)) {
          i++;
        }
        tabs[i].click();
      }
    }
    return hidden_tabs;
  }

  insertMenuItem(menu_items, element) {
    let first_item = menu_items.querySelector("paper-item");
    if (!menu_items.querySelector(`#${element.id}`)) {
      first_item.parentNode.insertBefore(element, first_item);
    }
  }

  insertClock(button) {
    if (!this.buttons[button]) return;
    const clock_button = this.buttons[button].querySelector("paper-icon-button")
      ? this.buttons[button]
      : this.buttons[button].shadowRoot;
    const clockIcon =
      clock_button.querySelector("paper-icon-button") || this.buttons[button];
    const clockIronIcon =
      clockIcon.querySelector("iron-icon") ||
      clockIcon.shadowRoot.querySelector("iron-icon");
    const clockWidth =
      (this.cchConfig.clock_format == 12 && this.cchConfig.clock_am_pm) ||
      this.cchConfig.clock_date
        ? 105
        : 80;

    if (
      !this.newSidebar &&
      this.cchConfig.notifications == "clock" &&
      this.cchConfig.clock_date &&
      !this.buttons.notifications.shadowRoot.querySelector("#cch_indicator")
    ) {
      let style = document.createElement("style");
      style.setAttribute("id", "cch_indicator");
      style.innerHTML = `
            .indicator {
              top: unset;
              bottom: -3px;
              right: 0px;
              width: 90%;
              height: 3px;
              border-radius: 0;
              ${
                this.cchConfig.notify_indicator_color
                  ? `background-color:${this.cchConfig.notify_indicator_color}`
                  : ""
              }
            }
            .indicator > div{
              display:none;
            }
          `;
      this.buttons.notifications.shadowRoot.appendChild(style);
    }

    let clockElement = clockIronIcon.parentNode.getElementById("cch_clock");
    if (this.cchConfig.menu == "clock") {
      this.buttons.menu.style.marginTop = this.cchConfig.compact_header
        ? "111px"
        : "";
      this.buttons.menu.style.zIndex = "1";
    }
    if (!clockElement) {
      clockIcon.style.cssText = `
                margin-right:-5px;
                width:${clockWidth}px;
                text-align: center;
              `;
      clockElement = document.createElement("p");
      clockElement.setAttribute("id", "cch_clock");
      let clockAlign = "center";
      let padding = "";
      let fontSize = "";
      if (this.cchConfig.clock_date && this.cchConfig.menu == "clock") {
        clockAlign = "left";
        padding = "margin-right:-20px";
        fontSize = "font-size:12pt";
      } else if (this.cchConfig.clock_date) {
        clockAlign = "right";
        padding = "margin-left:-20px";
        fontSize = "font-size:12pt";
      }
      clockElement.style.cssText = `
                margin-top: ${this.cchConfig.clock_date ? "-4px" : "2px"};
                text-align: ${clockAlign};
                ${padding};
                ${fontSize};
              `;
      clockIronIcon.parentNode.insertBefore(clockElement, clockIronIcon);
      clockIronIcon.style.display = "none";
      let style = document.createElement("style");
      style.setAttribute("id", "cch_clock");
      style.innerHTML = `
            time {
              ${this.cchConfig.time_css}
            }
            date {
              ${this.cchConfig.date_css}
            }
          `;
      clockIronIcon.parentNode.insertBefore(style, clockIronIcon);
    }

    const clockFormat = {
      hour12: this.cchConfig.clock_format != 24,
      hour: "2-digit",
      minute: "2-digit"
    };
    this.updateClock(clockElement, clockFormat);
  }

  updateClock(clock, clockFormat) {
    let date = new Date();
    let seconds = date.getSeconds();
    let locale = this.cchConfig.date_locale || this.hass.language;
    let time = date.toLocaleTimeString([], clockFormat);
    let options = {
      weekday: "short",
      month: "2-digit",
      day: "2-digit"
    };
    date = this.cchConfig.clock_date
      ? `</br><date>${date.toLocaleDateString(locale, options)}</date>`
      : "";
    if (!this.cchConfig.clock_am_pm && this.cchConfig.clock_format == 12) {
      clock.innerHTML = `<time>${time.slice(0, -3)}</time>${date}`;
    } else {
      clock.innerHTML = `<time>${time}</time>${date}`;
    }
    window.setTimeout(() => {
      this.updateClock(clock, clockFormat);
    }, (60 - seconds) * 1000);
  }

  // Abandon all hope, ye who enter here.
  conditionalStyling(tabs) {
    let _hass = document.querySelector("home-assistant").hass;
    const conditional_styles = this.cchConfig.conditional_styles;
    let tabContainer = tabs[0] ? tabs[0].parentNode : "";
    let styling = [];

    if (Array.isArray(conditional_styles)) {
      for (let i = 0; i < conditional_styles.length; i++) {
        styling.push(Object.assign({}, conditional_styles[i]));
      }
    } else {
      styling.push(Object.assign({}, conditional_styles));
    }

    function exists(configItem) {
      return configItem !== undefined && configItem !== null;
    }

    function notificationCount() {
      if (this.newSidebar) {
        let badge = this.main.shadowRoot
          .querySelector("ha-sidebar")
          .shadowRoot.querySelector("span.notification-badge");
        if (!badge) return 0;
        else return parseInt(badge.innerHTML);
      }
      let i = 0;
      let drawer = this.root
        .querySelector("hui-notification-drawer")
        .shadowRoot.querySelector(".notifications");
      for (let notification of drawer.querySelectorAll(".notification")) {
        if (notification.style.display !== "none") i++;
      }
      return i;
    }

    for (let i = 0; i < styling.length; i++) {
      let template = styling[i].template;
      let condition = styling[i].condition;

      if (template) {
        if (!template.length) template = [template];
        template.forEach(template => {
          this.templates(template, tabs, _hass, this.header);
        });
      } else if (condition) {
        let entity = styling[i].entity;
        if (_hass.states[entity] == undefined && entity !== "notifications") {
          console.log(`CCH conditional styling: ${entity} does not exist.`);
          continue;
        }
        let entState =
          entity == "notifications"
            ? notificationCount()
            : _hass.states[entity].state;
        let condState = condition.state;
        let above = condition.above;
        let below = condition.below;

        let toStyle =
          (exists(condState) && entState == condState) ||
          (exists(above) &&
            exists(below) &&
            entState > above &&
            entState < below) ||
          (exists(above) && entState > above) ||
          (exists(below) && entState < below);

        let tabIndex = styling[i].tab ? Object.keys(styling[i].tab)[0] : null;
        let tabCondition = styling[i].tab ? styling[i].tab[tabIndex] : null;
        let tabElem = tabs[this.getViewIndex(tabIndex)];
        let tabkey = `tab_${this.getViewIndex(tabIndex)}`;
        let button = styling[i].button
          ? Object.keys(styling[i].button)[0]
          : null;
        let background = styling[i].background;

        // Conditionally style tabs.
        if (toStyle && exists(tabIndex) && tabElem) {
          if (tabCondition.hide) tabElem.style.display = "none";
          if (tabCondition.color) {
            if (this.prevColor[tabkey] == undefined) {
              Object.assign(this.prevColor, {
                [tabkey]: window
                  .getComputedStyle(tabElem, null)
                  .getPropertyValue("color")
              });
            }
            tabElem.style.color = tabCondition.color;
          }
          if (tabCondition.on_icon) {
            tabElem
              .querySelector("ha-icon")
              .setAttribute("icon", tabCondition.on_icon);
          }
        } else if (!toStyle && exists(tabIndex) && tabElem) {
          if (tabCondition.hide) {
            tabElem.style.display = "";
          }
          if (tabCondition.color && this.prevColor[tabkey]) {
            tabElem.style.color = this.prevColor[tabkey];
          }
          if (tabCondition.off_icon) {
            tabElem
              .querySelector("ha-icon")
              .setAttribute("icon", tabCondition.off_icon);
          }
        }

        if (toStyle && button) {
          if (!this.buttons[button]) continue;
          let buttonCondition = styling[i].button[button];
          let buttonElem = this.buttons[button].querySelector(
            "paper-icon-button"
          )
            ? this.buttons[button].querySelector("paper-icon-button")
            : this.buttons[button].shadowRoot.querySelector(
                "paper-icon-button"
              );
          if (buttonCondition.hide) {
            buttonElem.style.display = "none";
          }
          if (buttonCondition.color) {
            if (this.prevColor.button == undefined) this.prevColor.button = {};
            if (this.prevColor.button[button] == undefined) {
              this.prevColor.button[button] = window
                .getComputedStyle(buttonElem, null)
                .getPropertyValue("color");
            }
            buttonElem.style.color = buttonCondition.color;
          }
          if (buttonCondition.on_icon) {
            let icon =
              buttonElem.querySelector("iron-icon") ||
              buttonElem.shadowRoot.querySelector("iron-icon");
            icon.setAttribute("icon", buttonCondition.on_icon);
          }
        } else if (!toStyle && button) {
          let buttonCondition = styling[i].button[button];
          let buttonElem = this.buttons[button].querySelector(
            "paper-icon-button"
          )
            ? this.buttons[button].querySelector("paper-icon-button")
            : this.buttons[button].shadowRoot.querySelector(
                "paper-icon-button"
              );
          if (buttonCondition.hide) {
            buttonElem.style.display = "";
          }
          if (
            buttonCondition.color &&
            this.prevColor.button &&
            this.prevColor.button[button]
          ) {
            buttonElem.style.color = this.prevColor.button[button];
          }
          if (buttonCondition.off_icon) {
            let icon =
              buttonElem.querySelector("iron-icon") ||
              buttonElem.shadowRoot.querySelector("iron-icon");
            icon.setAttribute("icon", buttonCondition.off_icon);
          }
        }

        // Conditionally style background.
        if (toStyle && background) {
          if (this.prevColor.background == undefined) {
            this.prevColor.background = window
              .getComputedStyle(this.header, null)
              .getPropertyValue("background");
          }
          this.header.style.background = styling[i].background;
        } else if (!toStyle && background) {
          this.header.style.background = this.prevColor.background;
        }
      }
    }
    this.tabContainerMargin(tabContainer);
  }

  templates(template, tabs, _hass, { style }) {
    let states = _hass.states;
    for (const condition in template) {
      if (condition == "tab") {
        for (const tab in template[condition]) {
          let tempCond = template[condition][tab];
          if (!tempCond.length) tempCond = [tempCond];
          tempCond.forEach(templateObj => {
            let tabIndex = this.getViewIndex(Object.keys(template[condition]));
            let styleTarget = Object.keys(templateObj);
            let tabTemplate = templateObj[styleTarget];
            let tabElement = tabs[tabIndex];
            if (styleTarget == "icon") {
              tabElement
                .querySelector("ha-icon")
                .setAttribute("icon", this.templateEval(tabTemplate, states));
            } else if (styleTarget == "color") {
              tabElement.style.color = this.templateEval(tabTemplate, states);
            } else if (styleTarget == "display") {
              this.templateEval(tabTemplate, states) == "show"
                ? (tabElement.style.display = "")
                : (tabElement.style.display = "none");
            }
          });
        }
      } else if (condition == "button") {
        for (const button in template[condition]) {
          let tempCond = template[condition][button];
          if (!tempCond.length) tempCond = [tempCond];
          tempCond.forEach(templateObj => {
            let buttonName = Object.keys(template[condition]);
            if (this.newSidebar && buttonName == "notifications") return;
            let styleTarget = Object.keys(templateObj);
            let buttonElem = this.buttons[buttonName];
            let tempCond = templateObj[styleTarget];
            let iconTarget = buttonElem.querySelector("paper-icon-button")
              ? buttonElem.querySelector("paper-icon-button")
              : buttonElem.shadowRoot.querySelector("paper-icon-button");
            if (styleTarget == "icon") {
              iconTarget.setAttribute(
                "icon",
                this.templateEval(tempCond, states)
              );
            } else if (styleTarget == "color") {
              let tar =
                iconTarget.querySelector("iron-icon") ||
                iconTarget.shadowRoot.querySelector("iron-icon");
              tar.style.color = this.templateEval(tempCond, states);
            } else if (styleTarget == "display") {
              this.templateEval(tempCond, states) == "show"
                ? (buttonElem.style.display = "")
                : (buttonElem.style.display = "none");
            }
          });
        }
      } else if (condition == "background") {
        style.background = this.templateEval(template[condition], states);
      }
    }
  }

  // Get range (e.g., "5 to 9") and build (5,6,7,8,9).
  buildRanges(array) {
    let ranges = [];
    if (!array) return [];
    const sortNumber = (a, b) => a - b;
    const range = (start, end) =>
      new Array(end - start + 1).fill(undefined).map((_, i) => i + start);
    for (let i in array) {
      if (typeof array[i] == "string" && array[i].includes("to")) {
        let split = array[i].split("to");
        if (parseInt(split[1]) > parseInt(split[0])) {
          ranges.push(range(parseInt(split[0]), parseInt(split[1])));
        } else {
          ranges.push(range(parseInt(split[1]), parseInt(split[0])));
        }
      } else if (isNaN(array[i])) {
        let views = this.lovelace.config.views;
        for (let view in views) {
          if (
            views[view]["title"] == array[i] ||
            views[view]["path"] == array[i]
          ) {
            ranges.push(parseInt(view));
          }
        }
      } else {
        ranges.push(parseInt(array[i]));
      }
    }
    return ranges.flat().sort(sortNumber);
  }

  showEditor() {
    window.scrollTo(0, 0);
    if (!this.root.querySelector("ha-app-layout editor")) {
      const container = document.createElement("editor");
      const nest = document.createElement("div");
      nest.style.cssText = `
        padding: 20px;
        max-width: 600px;
        margin: 15px auto;
        background: var(--paper-card-background-color);
        border: 6px solid var(--paper-card-background-color);
      `;
      container.style.cssText = `
        width: 100%;
        min-height: 100%;
        box-sizing: border-box;
        position: absolute;
        background: var(--background-color, grey);
        z-index: 2;
        padding: 5px;
      `;
      this.root
        .querySelector("ha-app-layout")
        .insertBefore(container, this.view);
      container.appendChild(nest);
      nest.appendChild(document.createElement("compact-custom-header-editor"));
    }
  }

  getViewIndex(viewString) {
    let views = this.lovelace.config.views;
    if (isNaN(viewString)) {
      for (let view in views) {
        if (
          views[view]["title"] == viewString ||
          views[view]["path"] == viewString
        ) {
          return view;
        }
      }
    } else {
      return parseInt(viewString);
    }
  }

  reverseObject(object) {
    let newObject = {};
    let keys = [];
    for (let key in object) keys.push(key);
    for (let i = keys.length - 1; i >= 0; i--) {
      let value = object[keys[i]];
      newObject[keys[i]] = value;
    }
    return newObject;
  }

  templateEval(template, states) {
    let entity = states;
    try {
      if (template.includes("return")) {
        return eval(`(function() {${template}}())`);
      } else {
        return eval(template);
      }
    } catch (e) {
      console.log(
        `%cCCH Template Failed:%c\n${template}\n%c${e}`,
        "text-decoration: underline;",
        "",
        "color: red;"
      );
    }
  }

  swipeNavigation(tabs, tabContainer) {
    // To make it easier to update lovelace-swipe-navigation
    // keep this as close to the standalone lovelace addon as possible.
    if (!tabContainer) return;
    let swipe_amount = this.cchConfig.swipe_amount || 15;
    let swipe_groups = this.cchConfig.swipe_groups;
    let animate = this.cchConfig.swipe_animate || "none";
    let skip_tabs = this.cchConfig.swipe_skip
      ? this.buildRanges(this.cchConfig.swipe_skip.split(","))
      : [];
    let wrap =
      this.cchConfig.swipe_wrap != undefined ? this.cchConfig.swipe_wrap : true;
    let prevent_default =
      this.cchConfig.swipe_prevent_default != undefined
        ? this.cchConfig.swipe_prevent_default
        : false;

    swipe_amount /= 10 ** 2;
    const appLayout = this.root.querySelector("ha-app-layout");
    let inGroup = true;
    let xDown;
    let yDown;
    let xDiff;
    let yDiff;
    let activeTab;
    let firstTab;
    let lastTab;
    let left;
    let fTabs;

    appLayout.addEventListener("touchstart", handleTouchStart.bind(this), {
      passive: true
    });
    appLayout.addEventListener("touchmove", handleTouchMove, {
      passive: false
    });
    appLayout.addEventListener("touchend", handleTouchEnd, { passive: true });

    click = click.bind(this);
    clearClassNames = clearClassNames.bind(this);
    animation = animation.bind(this);

    if (!this.root.querySelector("#cch_swipe_animation")) {
      let swipeAnimations = document.createElement("style");
      swipeAnimations.setAttribute("id", "cch_swipe_animation");
      swipeAnimations.innerHTML = `
        @keyframes swipeOutRight, swipeOutLeft {
          0% { transform: translateX(0px); opacity: 1; }
        }
        @keyframes swipeOutRight {
          100% { transform: translateX(${screen.width / 1.5}px); opacity: 0; }
        }
        @keyframes swipeOutLeft {
          100% { transform: translateX(-${screen.width / 1.5}px); opacity: 0; }
        }
        @keyframes swipeInRight, swipeInLeft {
          100% { transform: translateX(0px); opacity: 1; }
        }
        @keyframes swipeInRight {
          0% { transform: translateX(${screen.width / 1.5}px); opacity: 0; }
        }
        @keyframes swipeInLeft {
          0% { transform: translateX(-${screen.width / 1.5}px); opacity: 0; }
        }
        @keyframes fadeOut {
          0% { opacity: 1; }
          100% { opacity: 0; }
        }
        @keyframes fadeIn {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
        @keyframes flipOut {
          0% { transform: rotatey(0deg); opacity: 1; }
          100% { transform: rotatey(90deg); opacity: 0; }
        }
        @keyframes flipIn{
          0% { transform: rotatey(90deg); opacity: 0; }
          100% { transform: rotatey(0deg); opacity: 1; }
        }
        .swipeOutRight { animation: swipeOutRight .20s 1; }
        .swipeOutLeft { animation: swipeOutLeft .20s 1; }
        .swipeInRight { animation: swipeInRight .20s 1; }
        .swipeInLeft { animation: swipeInLeft .20s 1; }
        .fadeIn { animation: fadeIn .20s 1; }
        .fadeOut { animation: fadeOut .20s 1; }
        .flipIn { animation: flipIn .20s 1; }
        .flipOut { animation: flipOut .20s 1; }
        .swipeOutRight,
        .swipeOutLeft,
        .swipeInRight,
        .swipeInLeft,
        .fadeIn,
        .fadeOut,
        .flipIn,
        .flipOut {
          animation-fill-mode: forwards;
        }
    `;
      this.view.parentNode.appendChild(swipeAnimations);
    }

    function handleTouchStart(event) {
      filterTabs(this.cchConfig);
      if (swipe_groups && !inGroup) return;
      let ignored = [
        "APP-HEADER",
        "HA-SLIDER",
        "SWIPE-CARD",
        "HUI-MAP-CARD",
        "ROUND-SLIDER",
        "HUI-THERMOSTAT-CARD"
      ];
      let path = (event.composedPath && event.composedPath()) || event.path;
      if (path) {
        for (let element of path) {
          if (element.nodeName == "HUI-VIEW") break;
          else if (ignored.includes(element.nodeName)) return;
        }
      }
      xDown = event.touches[0].clientX;
      yDown = event.touches[0].clientY;
    }

    function handleTouchMove(event) {
      if (xDown && yDown) {
        xDiff = xDown - event.touches[0].clientX;
        yDiff = yDown - event.touches[0].clientY;
        if (Math.abs(xDiff) > Math.abs(yDiff) && prevent_default) {
          event.preventDefault();
        }
      }
    }

    function handleTouchEnd() {
      if (activeTab < 0 || Math.abs(xDiff) < Math.abs(yDiff)) {
        xDown = yDown = xDiff = yDiff = null;
        return;
      }
      if (xDiff > Math.abs(screen.width * swipe_amount)) {
        left = false;
        if (!wrap && fTabs[activeTab] == lastTab) return;
        else if (fTabs[activeTab] == lastTab && wrap) click(firstTab);
        else click(fTabs[activeTab + 1]);
      } else if (xDiff < -Math.abs(screen.width * swipe_amount)) {
        left = true;
        if (!wrap && fTabs[activeTab] == firstTab) return;
        else if (fTabs[activeTab] == firstTab && wrap) click(lastTab);
        else click(fTabs[activeTab - 1]);
      }
      xDown = yDown = xDiff = yDiff = null;
    }

    function filterTabs(config) {
      let currentTab = tabs.indexOf(
        tabContainer.querySelector(".iron-selected")
      );
      if (swipe_groups) {
        let groups = swipe_groups.replace(/, /g, ",").split(",");
        for (let group in groups) {
          let firstLast = groups[group].replace(/ /g, "").split("to");
          if (
            wrap &&
            currentTab >= firstLast[0] &&
            currentTab <= firstLast[1]
          ) {
            inGroup = true;
            firstTab = tabs[parseInt(firstLast[0])];
            lastTab = tabs[parseInt(firstLast[1])];
            fTabs = tabs.filter(
              element =>
                tabs.indexOf(element) >= firstLast[0] &&
                tabs.indexOf(element) <= firstLast[1]
            );
            break;
          } else {
            inGroup = false;
          }
        }
      }
      if (config.swipe_skip_hidden) {
        fTabs = tabs.filter(
          element =>
            !skip_tabs.includes(tabs.indexOf(element)) &&
            getComputedStyle(element, null).display != "none"
        );
      } else {
        fTabs = tabs.filter(
          element => !skip_tabs.includes(tabs.indexOf(element))
        );
      }
      if (!swipe_groups) {
        firstTab = fTabs[0];
        lastTab = fTabs[fTabs.length - 1];
      }
      activeTab = fTabs.indexOf(tabContainer.querySelector(".iron-selected"));
    }

    function animation(secs, transform, opacity, timeout) {
      setTimeout(() => {
        this.view.style.transition = `transform ${secs}s, opacity ${secs}s`;
        this.view.style.transform = transform ? transform : "";
        this.view.style.opacity = opacity;
      }, timeout);
    }

    function clearClassNames(huiView) {
      [
        "swipeOutRight",
        "swipeOutLeft",
        "swipeInRight",
        "swipeInLeft",
        "fadeIn",
        "fadeOut",
        "flipIn",
        "flipOut"
      ].forEach(name => {
        if (huiView.classList.contains(name)) {
          huiView.classList.remove(name);
        }
        if (this.view.classList.contains(name)) {
          this.view.classList.remove(name);
        }
      });
      huiView.style.overflowX = "";
      this.view.style.overflowX = "";
    }

    function navigate(tab, timeout) {
      setTimeout(() => {
        tab.dispatchEvent(
          new MouseEvent("click", { bubbles: false, cancelable: true })
        );
      }, timeout);
    }

    function click(tab) {
      if (
        !tab ||
        this.animation_running ||
        (tab.style.display == "none" && this.cchConfig.swipe_skip_hidden)
      ) {
        return;
      }
      if (animate)
        if (
          !wrap &&
          ((activeTab == firstTab && left) || (activeTab == lastTab && !left))
        ) {
          return;
        } else if (animate == "swipe") {
          const getHuiView = () => {
            return (
              this.view.querySelector("hui-view") ||
              this.view.querySelector("hui-panel-view")
            );
          };
          this.animation_running = true;
          let huiView = getHuiView();
          clearClassNames(huiView);
          huiView.style.overflowX = "hidden";
          this.view.style.overflowX = "hidden";
          // Swipe view off screen and fade out.
          huiView.classList.add(left ? "swipeOutRight" : "swipeOutLeft");
          this.view.classList.add("fadeOut");
          setTimeout(() => {
            this.view.style.opacity = "0";
            clearClassNames(huiView);
          }, 210);
          // Watch for destination view to load.
          const observer = new MutationObserver(mutations => {
            mutations.forEach(({ addedNodes }) => {
              addedNodes.forEach(({ nodeName }) => {
                if (nodeName) {
                  // Swipe view on screen and fade in.
                  huiView = getHuiView();
                  huiView.style.overflowX = "hidden";
                  this.view.style.overflowX = "hidden";
                  this.view.classList.add("fadeIn");
                  huiView.classList.add(left ? "swipeInLeft" : "swipeInRight");
                  setTimeout(() => {
                    this.view.style.opacity = "1";
                    clearClassNames(huiView);
                  }, 210);
                  observer.disconnect();
                  return;
                }
              });
            });
          });
          observer.observe(this.view, { childList: true });
          // Navigate to next view and trigger the observer.
          navigate(tab, 220);
        } else if (animate == "fade") {
          animation(0.16, "", 0, 0);
          const observer = new MutationObserver(mutations => {
            mutations.forEach(({ addedNodes }) => {
              addedNodes.forEach(({ nodeName }) => {
                if (nodeName == "HUI-VIEW" || nodeName == "HUI-PANEL-VIEW") {
                  animation(0.16, "", 1, 0);
                  observer.disconnect();
                }
              });
            });
          });
          observer.observe(this.view, { childList: true });
          navigate(tab, 170);
        } else if (animate == "flip") {
          animation(0.25, "rotatey(90deg)", 0.25, 0);
          const observer = new MutationObserver(mutations => {
            mutations.forEach(({ addedNodes }) => {
              addedNodes.forEach(({ nodeName }) => {
                if (nodeName == "HUI-VIEW" || nodeName == "HUI-PANEL-VIEW") {
                  animation(0.25, "rotatey(0deg)", 1, 50);
                  observer.disconnect();
                }
              });
            });
          });
          observer.observe(this.view, { childList: true });
          navigate(tab, 270);
        } else {
          navigate(tab, 0);
        }
      this.animation_running = false;
    }
  }

  breakingChangeNotification() {
    if (
      this.lovelace.config.cch == undefined &&
      JSON.stringify(this.lovelace.config.views).includes(
        "custom:compact-custom-header"
      )
    ) {
      this.hass.callService("persistent_notification", "create", {
        title: "CCH Breaking Change",
        notification_id: "CCH_Breaking_Change",
        message:
          "Compact-Custom-Header's configuration method has changed. You are " +
          "receiving this notification because you have updated CCH, but are " +
          "using the old config method. Please, visit the [upgrade guide]" +
          "(https://maykar.github.io/compact-custom-header/1_1_0_upgrade/) " +
          "for more info."
      });
    }
  }
}

const cch = new CompactCustomHeader();
cch.run();

class CompactCustomHeaderEditor extends cch.LitElement {
  static get properties() {
    return { _config: {} };
  }

  firstUpdated() {
    this.html = cch.LitElement.prototype.html;
    if (
      !customElements.get("paper-toggle-button") &&
      customElements.get("ha-switch")
    ) {
      customElements.define(
        "paper-toggle-button",
        class extends customElements.get("ha-switch") {}
      );
    }

    let ll = document.querySelector("home-assistant");
    ll = ll && ll.shadowRoot;
    ll = ll && ll.querySelector("home-assistant-main");
    ll = ll && ll.shadowRoot;
    ll = ll && ll.querySelector("app-drawer-layout partial-panel-resolver");
    ll = (ll && ll.shadowRoot) || ll;
    ll = ll && ll.querySelector("ha-panel-lovelace");
    ll = ll && ll.shadowRoot;
    this._lovelace = ll && ll.querySelector("hui-root").lovelace;

    this.deepcopy = this.deepcopy.bind(this);
    this._config = this._lovelace.config.cch
      ? this.deepcopy(this._lovelace.config.cch)
      : {};
  }

  render() {
    if (!this._config || !this._lovelace) return this.html``;
    return this.html`
      <div @click="${this._close}" class="title_control">
        X
      </div>
      ${this.renderStyle()}
      <cch-config-editor
        .defaultConfig="${cch.defaultConfig}"
        .config="${this._config}"
        @cch-config-changed="${this._configChanged}"
      >
      </cch-config-editor>
      <h4 class="underline">Exceptions</h4>
      <br />
      ${
        this._config.exceptions
          ? this._config.exceptions.map(
              (exception, index) => this.html`
              <cch-exception-editor
                .config="${this._config}"
                .exception="${exception}"
                .index="${index}"
                @cch-exception-changed="${this._exceptionChanged}"
                @cch-exception-delete="${this._exceptionDelete}"
              >
              </cch-exception-editor>
            `
            )
          : ""
      }
      <br />
      ${
        this._mwc_button
          ? this.html`
            <mwc-button @click="${this._addException}"
              >Add Exception
            </mwc-button>
          `
          : this.html`
            <paper-button @click="${this._addException}"
              >Add Exception
            </paper-button>
          `
      }

      <h4 class="underline">Current User</h4>
      <p style="font-size:16pt">${cch.hass.user.name}</p>
      <h4 class="underline">Current User Agent</h4>
      <br />
      ${navigator.userAgent}
      <br />
      <h4
        style="background:var(--paper-card-background-color);
        margin-bottom:-20px;"
        class="underline"
      >
        ${
          !this.exception
            ? this.html`
              ${this._save_button}
            `
            : ""
        }
        ${
          !this.exception
            ? this.html`
              ${this._cancel_button}
            `
            : ""
        }
      </h4>
    `;
  }

  get _mwc_button() {
    return customElements.get("mwc-button") ? true : false;
  }

  _close() {
    let editor = this.parentNode.parentNode.parentNode.querySelector("editor");
    this.parentNode.parentNode.parentNode.removeChild(editor);
  }

  _save() {
    for (const key in this._config) {
      if (this._config[key] == cch.defaultConfig[key]) delete this._config[key];
      // Remove old config option.
      if (typeof this._config.background == "boolean") {
        this._config.background = "";
      }
    }
    let newConfig = { ...this._lovelace.config, ...{ cch: this._config } };
    if (cch.lovelace.mode == "storage") {
      try {
        this._lovelace.saveConfig(newConfig).then(() => {
          window.location.href = window.location.href;
        });
      } catch (e) {
        alert(`Save failed: ${e}`);
      }
    } else {
      window.prompt(
        "Copy to clipboard: Ctrl+C, Enter\n" +
          "This option is experimental, check the copied config and backup.",
        this.obj2yaml({ cch: newConfig.cch })
      );
    }
  }

  get _save_button() {
    let text = cch.lovelace.mode == "storage" ? "Save and Reload" : "Copy YAML";
    return this._mwc_button
      ? this.html`
          <mwc-button raised @click="${this._save}">${text}</mwc-button>
        `
      : this.html`
          <paper-button raised @click="${this._save}"
            >${text}</paper-button
          >
        `;
  }
  get _cancel_button() {
    return this._mwc_button
      ? this.html`
          <mwc-button raised @click="${this._close}">Cancel</mwc-button>
        `
      : this.html`
          <paper-button raised @click="${this._close}">Cancel</paper-button>
        `;
  }

  _addException() {
    let newExceptions;
    if (this._config.exceptions) {
      newExceptions = this._config.exceptions.slice(0);
      newExceptions.push({ conditions: {}, config: {} });
    } else {
      newExceptions = [{ conditions: {}, config: {} }];
    }
    this._config = { ...this._config, exceptions: newExceptions };

    cch.fireEvent(this, "config-changed", { config: this._config });
  }

  _configChanged({ detail }) {
    if (!this._config) return;
    this._config = { ...this._config, ...detail.config };
    cch.fireEvent(this, "config-changed", { config: this._config });
  }

  _exceptionChanged(ev) {
    if (!this._config) return;
    const target = ev.target.index;
    const newExceptions = this._config.exceptions.slice(0);
    newExceptions[target] = ev.detail.exception;
    this._config = { ...this._config, exceptions: newExceptions };

    cch.fireEvent(this, "config-changed", { config: this._config });
  }

  _exceptionDelete(ev) {
    if (!this._config) return;
    const target = ev.target;
    const newExceptions = this._config.exceptions.slice(0);
    newExceptions.splice(target.index, 1);
    this._config = { ...this._config, exceptions: newExceptions };

    cch.fireEvent(this, "config-changed", { config: this._config });
    this.requestUpdate();
  }

  deepcopy(value) {
    if (!(!!value && typeof value == "object")) return value;
    if (Object.prototype.toString.call(value) == "[object Date]") {
      return new Date(value.getTime());
    }
    if (Array.isArray(value)) return value.map(this.deepcopy);
    const result = {};
    Object.keys(value).forEach(key => {
      result[key] = this.deepcopy(value[key]);
    });
    return result;
  }

  obj2yaml(obj) {
    if (typeof obj == "string") obj = JSON.parse(obj);
    const ret = [];
    convert(obj, ret);
    return ret.join("\n");
    function getType(obj) {
      if (obj instanceof Array) {
        return "array";
      } else if (typeof obj == "string") {
        return "string";
      } else if (typeof obj == "boolean") {
        return "boolean";
      } else if (typeof obj == "number") {
        return "number";
      } else if (typeof obj == "undefined" || obj === null) {
        return "null";
      } else {
        return "hash";
      }
    }
    function convert(obj, ret) {
      const type = getType(obj);
      switch (getType(obj)) {
        case "array":
          convertArray(obj, ret);
          break;
        case "hash":
          convertHash(obj, ret);
          break;
        case "string":
          convertString(obj, ret);
          break;
        case "null":
          ret.push("null");
          break;
        case "number":
          ret.push(obj.toString());
          break;
        case "boolean":
          ret.push(obj ? "true" : "false");
          break;
      }
    }
    function convertArray(obj, ret) {
      if (obj.length === 0) ret.push("[]");
      for (let i = 0; i < obj.length; i++) {
        const ele = obj[i];
        const recurse = [];
        convert(ele, recurse);
        for (let j = 0; j < recurse.length; j++) {
          ret.push((j == 0 ? "- " : "  ") + recurse[j]);
        }
      }
    }
    function convertHash(obj, ret) {
      for (const k in obj) {
        const recurse = [];
        if (obj.hasOwnProperty(k)) {
          const ele = obj[k];
          convert(ele, recurse);
          const type = getType(ele);
          if (
            type == "string" ||
            type == "null" ||
            type == "number" ||
            type == "boolean"
          ) {
            ret.push(`${k}: ${recurse[0]}`);
          } else {
            ret.push(`${k}: `);
            for (let i = 0; i < recurse.length; i++) {
              ret.push(`  ${recurse[i]}`);
            }
          }
        }
      }
    }
    function convertString(obj, ret) {
      if ((obj.includes("'") && obj.includes('"')) || obj.length > 45) {
        if (obj.includes(";")) {
          obj = obj.includes("; ") ? obj.split("; ") : obj.split(";");
          obj[0] = `>\n            ${obj[0]}`;
          if (obj[obj.length - 1].trim() == "") obj.pop();
          obj = obj.join(";\n            ");
          obj = obj.replace(/\n$/, "");
          ret.push(obj);
        } else {
          ret.push(`>\n            ${obj}`);
        }
      } else if (obj.includes('"')) {
        obj = obj.replace(/\n$/, "");
        ret.push(`'${obj}'`);
      } else {
        obj = obj.replace(/\n$/, "");
        ret.push(`"${obj}"`);
      }
    }
  }

  renderStyle() {
    return this.html`
      <style>
        h3,
        h4 {
          font-size: 16pt;
          margin-bottom: 5px;
          width: 100%;
        }
        paper-button {
          margin: 0;
          background-color: var(--primary-color);
          color: var(--text-primary-color, #fff);
        }
        .toggle-button {
          margin: 4px;
          background-color: transparent;
          color: var(--primary-color);
        }
        .title_control {
          color: var(--text-dark-color);
          font-weight: bold;
          font-size: 22px;
          float: right;
          cursor: pointer;
          margin: -10px -5px -5px -5px;
        }
        .user_agent {
          display: block;
          margin-left: auto;
          margin-right: auto;
          padding: 5px;
          border: 0;
          resize: none;
          width: 100%;
        }
        .underline {
          width: 100%;
          background: var(--dark-color);
          color: var(--text-dark-color);
          padding: 5px;
          width: calc(100% + 30px);
          margin-left: calc(0% - 20px);
        }
      </style>
    `;
  }
}

customElements.define(
  "compact-custom-header-editor",
  CompactCustomHeaderEditor
);

class CchConfigEditor extends cch.LitElement {
  static get properties() {
    return {
      defaultConfig: {},
      config: {},
      exception: {},
      _closed: {}
    };
  }

  constructor() {
    super();
    this.buttonOptions = ["show", "hide", "clock", "overflow"];
    this.overflowOptions = ["show", "hide", "clock"];
    this.swipeAnimation = ["none", "swipe", "fade", "flip"];
  }

  get _clock() {
    return (
      this.getConfig("menu") == "clock" ||
      this.getConfig("voice") == "clock" ||
      this.getConfig("notifications") == "clock" ||
      this.getConfig("options") == "clock"
    );
  }

  getConfig(item) {
    return this.config[item] !== undefined
      ? this.config[item]
      : cch.defaultConfig[item];
  }

  render() {
    this.exception = this.exception !== undefined && this.exception !== false;
    return this.html`
      <custom-style>
        <style is="custom-style">
          a {
            color: var(--text-dark-color);
            text-decoration: none;
          }
          .card-header {
            margin-top: -5px;
            @apply --paper-font-headline;
          }
          .card-header paper-icon-button {
            margin-top: -5px;
            float: right;
          }
        </style>
      </custom-style>
      ${
        !this.exception
          ? this.html`
            <h1 style="margin-top:-20px;margin-bottom:0;" class="underline">
              Compact Custom Header &nbsp;₁.₄.₉
            </h1>
            <h4
              style="margin-top:-5px;padding-top:10px;font-size:12pt;"
              class="underline"
            >
              <a
                href="https://maykar.github.io/compact-custom-header/"
                target="_blank"
              >
                <ha-icon icon="mdi:help-circle" style="margin-top:-5px;">
                </ha-icon>
                Docs&nbsp;&nbsp;&nbsp;</a
              >
              <a
                href="https://github.com/maykar/compact-custom-header"
                target="_blank"
              >
                <ha-icon icon="mdi:github-circle" style="margin-top:-5px;">
                </ha-icon>
                Github&nbsp;&nbsp;&nbsp;</a
              >
              <a
                href="https://community.home-assistant.io/t/compact-custom-header"
                target="_blank"
              >
                <ha-icon icon="hass:home-assistant" style="margin-top:-5px;">
                </ha-icon>
                Forums</a
              >
            </h4>
            ${
              this.getConfig("warning")
                ? this.html`
                  <br />
                  <div class="warning">
                    Modifying options marked with a
                    <iron-icon
                      icon="hass:alert"
                      style="width:20px;margin-top:-6px;"
                    ></iron-icon
                    >or hiding the options button will remove your ability to
                    edit from the UI. You can disable CCH by adding
                    "?disable_cch" to the end of your URL to temporarily restore
                    the default header.
                  </div>
                  <br />
                `
                : ""
            }
          `
          : ""
      }
      ${this.renderStyle()}
      <div class="side-by-side">
        <paper-toggle-button
          class="${
            this.exception && this.config.disable === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("disable") !== false}"
          .configValue="${"disable"}"
          @change="${this._valueChanged}"
          title="Completely disable CCH. Useful for exceptions."
        >
          Disable CCH
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.compact_header === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("compact_header") !== false}"
          .configValue="${"compact_header"}"
          @change="${this._valueChanged}"
          title="Make header compact."
        >
          Compact Header
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.kiosk_mode === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("kiosk_mode") !== false}"
          .configValue="${"kiosk_mode"}"
          @change="${this._valueChanged}"
          title="Hide the header, close the sidebar, and disable sidebar swipe."
        >
          Kiosk Mode
          ${
            this.getConfig("warning")
              ? this.html`
                <iron-icon icon="hass:alert" class="alert"></iron-icon>
              `
              : ""
          }
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.header === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("header") !== false &&
            this.getConfig("kiosk_mode") == false}"
          .configValue="${"header"}"
          @change="${this._valueChanged}"
          title="Turn off to hide the header completely."
        >
          Display Header
          ${
            this.getConfig("warning")
              ? this.html`
                <iron-icon icon="hass:alert" class="alert"></iron-icon>
              `
              : ""
          }
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.chevrons === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("chevrons") !== false}"
          .configValue="${"chevrons"}"
          @change="${this._valueChanged}"
          title="View scrolling controls in header."
        >
          Display Tab Chevrons
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.redirect === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("redirect") !== false}"
          .configValue="${"redirect"}"
          @change="${this._valueChanged}"
          title="Auto-redirect away from hidden tabs."
        >
          Hidden Tab Redirect
        </paper-toggle-button>
        <paper-toggle-button
          style="${cch.newSidebar ? "" : "display:none;"}"
          class="${
            this.exception && this.config.disable_sidebar === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("disable_sidebar") !== false ||
            this.getConfig("kiosk_mode") !== false}"
          .configValue="${"disable_sidebar"}"
          @change="${this._valueChanged}"
          title="Hides and prevents sidebar from opening."
        >
          Hide & Disable Sidebar
        </paper-toggle-button>
        <paper-toggle-button
          style="${cch.newSidebar ? "display:none;" : ""}"
          class="${
            this.exception && this.config.sidebar_closed === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("sidebar_closed") !== false ||
            this.getConfig("kiosk_mode") !== false}"
          .configValue="${"sidebar_closed"}"
          @change="${this._valueChanged}"
          title="Closes the sidebar on page load."
        >
          Close Sidebar
        </paper-toggle-button>
        ${
          !this.exception
            ? this.html`
              <paper-toggle-button
                class="${
                  this.exception && this.config.warning === undefined
                    ? "inherited"
                    : ""
                }"
                ?checked="${this.getConfig("warning") !== false}"
                .configValue="${"warning"}"
                @change="${this._valueChanged}"
                title="Toggle warnings in this editor."
              >
                Display CCH Warnings
              </paper-toggle-button>
            `
            : ""
        }
        <paper-toggle-button
          style="${cch.newSidebar ? "display:none;" : ""}"
          class="${
            this.exception && this.config.sidebar_swipe === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("sidebar_swipe") !== false &&
            this.getConfig("kiosk_mode") == false}"
          .configValue="${"sidebar_swipe"}"
          @change="${this._valueChanged}"
          title="Swipe to open sidebar on mobile devices."
        >
          Swipe Open Sidebar
        </paper-toggle-button>
      </div>
      <h4 class="underline">Menu Items</h4>
      <div class="side-by-side">
        <paper-toggle-button
          class="${
            this.exception && this.config.hide_config === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("hide_config") !== false}"
          .configValue="${"hide_config"}"
          @change="${this._valueChanged}"
          title='Hide "Configure UI" in options menu.'
        >
          Hide "Configure UI"
          ${
            this.getConfig("warning")
              ? this.html`
                <iron-icon icon="hass:alert" class="alert"></iron-icon>
              `
              : ""
          }
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.hide_help === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("hide_help") !== false}"
          .configValue="${"hide_help"}"
          @change="${this._valueChanged}"
          title='Hide "Help" in options menu.'
        >
          Hide "Help"
        </paper-toggle-button>
        <paper-toggle-button
          class="${
            this.exception && this.config.hide_unused === undefined
              ? "inherited"
              : ""
          }"
          ?checked="${this.getConfig("hide_unused") !== false}"
          .configValue="${"hide_unused"}"
          @change="${this._valueChanged}"
          title='Hide "Help" in options menu.'
        >
          Hide "Unused Entities"
        </paper-toggle-button>
      </div>
      <h4 class="underline">Buttons</h4>
      <div class="buttons side-by-side">
        <div
          class="${
            this.exception && this.config.menu === undefined ? "inherited" : ""
          }"
        >
          <iron-icon icon="hass:menu"></iron-icon>
          <paper-dropdown-menu
            @value-changed="${this._valueChanged}"
            label="Menu Button:"
            .configValue="${"menu"}"
          >
            <paper-listbox
              slot="dropdown-content"
              .selected="${this.buttonOptions.indexOf(this.getConfig("menu"))}"
            >
              ${this.buttonOptions.map(
                option => this.html`
                  <paper-item>${option}</paper-item>
                `
              )}
            </paper-listbox>
          </paper-dropdown-menu>
        </div>
        <div
          class="${
            this.exception && this.config.voice === undefined ? "inherited" : ""
          }"
        >
          <iron-icon icon="hass:microphone"></iron-icon>
          <paper-dropdown-menu
            @value-changed="${this._valueChanged}"
            label="Voice Button:"
            .configValue="${"voice"}"
          >
            <paper-listbox
              slot="dropdown-content"
              .selected="${this.buttonOptions.indexOf(this.getConfig("voice"))}"
            >
              ${this.buttonOptions.map(
                option => this.html`
                  <paper-item>${option}</paper-item>
                `
              )}
            </paper-listbox>
          </paper-dropdown-menu>
        </div>
      </div>
      <div
        class="buttons side-by-side"
        style="${cch.newSidebar ? "width:50%;" : ""}"
      >
        <div
          class="${
            this.exception && this.config.options === undefined
              ? "inherited"
              : ""
          }"
        >
          <iron-icon icon="hass:dots-vertical"></iron-icon>
          <paper-dropdown-menu
            @value-changed="${this._valueChanged}"
            label="Options Button:"
            .configValue="${"options"}"
          >
            <paper-listbox
              slot="dropdown-content"
              .selected="${this.overflowOptions.indexOf(
                this.getConfig("options")
              )}"
            >
              ${this.overflowOptions.map(
                option => this.html`
                  <paper-item>${option}</paper-item>
                `
              )}
            </paper-listbox>
          </paper-dropdown-menu>
        </div>
        <div
          style="${cch.newSidebar ? "display:none;" : ""}"
          class="${
            this.exception && this.config.notifications === undefined
              ? "inherited"
              : ""
          }"
        >
          <iron-icon icon="hass:bell"></iron-icon>
          <paper-dropdown-menu
            @value-changed="${this._valueChanged}"
            label="Notifications Button:"
            .configValue="${"notifications"}"
          >
            <paper-listbox
              slot="dropdown-content"
              .selected="${this.buttonOptions.indexOf(
                this.getConfig("notifications")
              )}"
            >
              ${this.buttonOptions.map(
                option => this.html`
                  <paper-item>${option}</paper-item>
                `
              )}
            </paper-listbox>
          </paper-dropdown-menu>
        </div>
      </div>
      ${
        this._clock
          ? this.html`
            <h4 class="underline">Clock Options</h4>
            <div class="side-by-side">
              <paper-dropdown-menu
                class="${
                  this.exception && this.getConfig("clock_format") === undefined
                    ? "inherited"
                    : ""
                }"
                label="Clock format"
                @value-changed="${this._valueChanged}"
                .configValue="${"clock_format"}"
              >
                <paper-listbox
                  slot="dropdown-content"
                  .selected="${this.getConfig("clock_format") === "24" ? 1 : 0}"
                >
                  <paper-item>12</paper-item>
                  <paper-item>24</paper-item>
                </paper-listbox>
              </paper-dropdown-menu>
              <paper-input
                class="${
                  this.exception && this.config.date_locale === undefined
                    ? "inherited"
                    : ""
                }"
                label="Date Locale:"
                .value="${this.getConfig("date_locale")}"
                .configValue="${"date_locale"}"
                @value-changed="${this._valueChanged}"
              >
              </paper-input>

              <div class="side-by-side">
                <paper-toggle-button
                  class="${
                    this.exception && this.config.clock_am_pm === undefined
                      ? "inherited"
                      : ""
                  }"
                  ?checked="${this.getConfig("clock_am_pm") !== false}"
                  .configValue="${"clock_am_pm"}"
                  @change="${this._valueChanged}"
                >
                  AM / PM</paper-toggle-button
                >
                <paper-toggle-button
                  class="${
                    this.exception && this.config.clock_date === undefined
                      ? "inherited"
                      : ""
                  }"
                  ?checked="${this.getConfig("clock_date") !== false}"
                  .configValue="${"clock_date"}"
                  @change="${this._valueChanged}"
                >
                  Date</paper-toggle-button
                >
              </div>
            </div>
          `
          : ""
      }
      <h4 class="underline">Tabs</h4>
      <paper-dropdown-menu id="tabs" @value-changed="${this._tabVisibility}">
        <paper-listbox
          slot="dropdown-content"
          .selected="${this.getConfig("show_tabs").length > 0 ? "1" : "0"}"
        >
          <paper-item>Hide Tabs</paper-item>
          <paper-item>Show Tabs</paper-item>
        </paper-listbox>
      </paper-dropdown-menu>
      <div class="side-by-side">
        <div
          id="show"
          style="display:${
            this.getConfig("show_tabs").length > 0 ? "initial" : "none"
          }"
        >
          <paper-input
            class="${
              this.exception && this.config.show_tabs === undefined
                ? "inherited"
                : ""
            }"
            label="Comma-separated list of tab numbers to show:"
            .value="${this.getConfig("show_tabs")}"
            .configValue="${"show_tabs"}"
            @value-changed="${this._valueChanged}"
          >
          </paper-input>
        </div>
        <div
          id="hide"
          style="display:${
            this.getConfig("show_tabs").length > 0 ? "none" : "initial"
          }"
        >
          <paper-input
            class="${
              this.exception && this.config.hide_tabs === undefined
                ? "inherited"
                : ""
            }"
            label="Comma-separated list of tab numbers to hide:"
            .value="${this.getConfig("hide_tabs")}"
            .configValue="${"hide_tabs"}"
            @value-changed="${this._valueChanged}"
          >
          </paper-input>
        </div>
        <paper-input
          class="${
            this.exception && this.config.default_tab === undefined
              ? "inherited"
              : ""
          }"
          label="Default tab:"
          .value="${this.getConfig("default_tab")}"
          .configValue="${"default_tab"}"
          @value-changed="${this._valueChanged}"
        >
        </paper-input>
      </div>
      <h4 class="underline">Swipe Navigation</h4>
      <div class="side-by-side">
        <paper-toggle-button
          class="${
            this.exception && this.config.swipe === undefined ? "inherited" : ""
          }"
          ?checked="${this.getConfig("swipe") !== false}"
          .configValue="${"swipe"}"
          @change="${this._valueChanged}"
          title="Toggle Swipe Navigation"
        >
          Swipe Navigation
        </paper-toggle-button>
        ${
          this.config.swipe
            ? this.html`
          <paper-toggle-button
            class="${
              this.exception && this.config.swipe_wrap === undefined
                ? "inherited"
                : ""
            }"
            ?checked="${this.getConfig("swipe_wrap") !== false}"
            .configValue="${"swipe_wrap"}"
            @change="${this._valueChanged}"
            title="Wrap from first to last tab and vice versa."
          >
            Wrapping
          </paper-toggle-button>
          <paper-toggle-button
            class="${
              this.exception && this.config.swipe_prevent_default === undefined
                ? "inherited"
                : ""
            }"
            ?checked="${this.getConfig("swipe_prevent_default") !== false}"
            .configValue="${"swipe_prevent_default"}"
            @change="${this._valueChanged}"
            title="Prevent browsers default horizontal swipe action."
          >
            Prevent Default
          </paper-toggle-button>
          <div
          class="${
            this.exception && this.config.swipe_animate === undefined
              ? "inherited"
              : ""
          }"
        >
        </div>
        <div class="side-by-side">
          <paper-dropdown-menu
            @value-changed="${this._valueChanged}"
            label="Swipe Animation:"
            .configValue="${"swipe_animate"}"
          >
            <paper-listbox
              slot="dropdown-content"
              .selected="${this.swipeAnimation.indexOf(
                this.getConfig("swipe_animate")
              )}"
            >
              ${this.swipeAnimation.map(
                option => this.html`
                  <paper-item>${option}</paper-item>
                `
              )}
            </paper-listbox>
          </paper-dropdown-menu>
        </div>
        <paper-input
        class="${
          this.exception && this.config.swipe_amount === undefined
            ? "inherited"
            : ""
        }"
        label="Percentage of screen width needed for swipe:"
        .value="${this.getConfig("swipe_amount")}"
        .configValue="${"swipe_amount"}"
        @value-changed="${this._valueChanged}"
      >
      </paper-input>
          </div>
          <paper-input
          class="${
            this.exception && this.config.swipe_skip === undefined
              ? "inherited"
              : ""
          }"
          label="Comma-separated list of tabs to skip over on swipe:"
          .value="${this.getConfig("swipe_skip")}"
          .configValue="${"swipe_skip"}"
          @value-changed="${this._valueChanged}"
        >
        </paper-input>
        </div>
      `
            : ""
        }
      </div>
    `;
  }

  _toggleCard() {
    this._closed = !this._closed;
    cch.fireEvent(this, "iron-resize");
  }

  _tabVisibility() {
    let show = this.shadowRoot.querySelector("#show");
    let hide = this.shadowRoot.querySelector("#hide");
    if (this.shadowRoot.querySelector("#tabs").value == "Hide Tabs") {
      show.style.display = "none";
      hide.style.display = "initial";
    } else {
      hide.style.display = "none";
      show.style.display = "initial";
    }
  }

  _valueChanged(ev) {
    if (!this.config) return;
    if (ev.target.configValue) {
      if (ev.target.value === "") {
        delete this.config[ev.target.configValue];
      } else {
        this.config = {
          ...this.config,
          [ev.target.configValue]:
            ev.target.checked !== undefined
              ? ev.target.checked
              : ev.target.value
        };
      }
    }
    cch.fireEvent(this, "cch-config-changed", { config: this.config });
  }

  renderStyle() {
    return this.html`
      <style>
        h3,
        h4 {
          font-size: 16pt;
          margin-bottom: 5px;
          width: 100%;
        }
        paper-toggle-button {
          padding-top: 16px;
        }
        iron-icon {
          padding-right: 5px;
        }
        iron-input {
          max-width: 115px;
        }
        .inherited {
          opacity: 0.4;
        }
        .inherited:hover {
          opacity: 1;
        }
        .side-by-side {
          display: flex;
          flex-wrap: wrap;
        }
        .side-by-side > * {
          flex: 1;
          padding-right: 4px;
          flex-basis: 33%;
        }
        .buttons > div {
          display: flex;
          align-items: center;
        }
        .buttons > div paper-dropdown-menu {
          flex-grow: 1;
        }
        .buttons > div iron-icon {
          padding-right: 15px;
          padding-top: 20px;
          margin-left: -3px;
        }
        .buttons > div:nth-of-type(2n) iron-icon {
          padding-left: 20px;
        }
        .warning {
          background-color: #455a64;
          padding: 10px;
          color: #ffcd4c;
          border-radius: 5px;
        }
        .alert {
          color: #ffcd4c;
          width: 20px;
          margin-top: -6px;
        }
        [closed] {
          overflow: hidden;
          height: 52px;
        }
        paper-card {
          margin-top: 10px;
          width: 100%;
          transition: all 0.5s ease;
        }
        .underline {
          width: 100%;
          background: var(--dark-color);
          color: var(--text-dark-color);
          padding: 5px;
          width: calc(100% + 30px);
          margin-left: calc(0% - 20px);
        }
      </style>
    `;
  }
}

customElements.define("cch-config-editor", CchConfigEditor);

class CchExceptionEditor extends cch.LitElement {
  static get properties() {
    return { config: {}, exception: {}, _closed: {} };
  }

  constructor() {
    super();
    this._closed = true;
  }

  render() {
    if (!this.exception) {
      return this.html``;
    }
    return this.html`
      ${this.renderStyle()}
      <custom-style>
        <style is="custom-style">
          .card-header {
            margin-top: -5px;
            @apply --paper-font-headline;
          }
          .card-header paper-icon-button {
            margin-top: -5px;
            float: right;
          }
        </style>
      </custom-style>
      <paper-card ?closed=${this._closed}>
        <div class="card-content">
          <div class="card-header">
            ${Object.values(this.exception.conditions)
              .join(", ")
              .substring(0, 40) || "New Exception"}
            <paper-icon-button
              icon="${this._closed ? "mdi:chevron-down" : "mdi:chevron-up"}"
              @click="${this._toggleCard}"
            >
            </paper-icon-button>
            <paper-icon-button
              ?hidden=${this._closed}
              icon="mdi:delete"
              @click="${this._deleteException}"
            >
            </paper-icon-button>
          </div>
          <h4 class="underline">Conditions</h4>
          <cch-conditions-editor
            .conditions="${this.exception.conditions}"
            @cch-conditions-changed="${this._conditionsChanged}"
          >
          </cch-conditions-editor>
          <h4 class="underline">Config</h4>
          <cch-config-editor
            exception
            .defaultConfig="${{ ...cch.defaultConfig, ...this.config }}"
            .config="${this.exception.config}"
            @cch-config-changed="${this._configChanged}"
          >
          </cch-config-editor>
        </div>
      </paper-card>
    `;
  }

  renderStyle() {
    return this.html`
      <style>
        h3,
        h4 {
          font-size: 16pt;
          margin-bottom: 5px;
          width: 100%;
        }
        [closed] {
          overflow: hidden;
          height: 52px;
        }
        paper-card {
          margin-top: 10px;
          width: 100%;
          transition: all 0.5s ease;
        }
        .underline {
          width: 100%;
          background: var(--dark-color);
          color: var(--text-dark-color);
          padding: 5px;
          width: calc(100% + 30px);
          margin-left: calc(0% - 20px);
        }
      </style>
    `;
  }

  _toggleCard() {
    this._closed = !this._closed;
    cch.fireEvent(this, "iron-resize");
  }

  _deleteException() {
    cch.fireEvent(this, "cch-exception-delete");
  }

  _conditionsChanged({ detail }) {
    if (!this.exception) return;
    const newException = { ...this.exception, conditions: detail.conditions };
    cch.fireEvent(this, "cch-exception-changed", { exception: newException });
  }

  _configChanged(ev) {
    ev.stopPropagation();
    if (!this.exception) return;
    const newException = { ...this.exception, config: ev.detail.config };
    cch.fireEvent(this, "cch-exception-changed", { exception: newException });
  }
}

customElements.define("cch-exception-editor", CchExceptionEditor);

class CchConditionsEditor extends cch.LitElement {
  static get properties() {
    return { conditions: {} };
  }
  get _user() {
    return this.conditions.user || "";
  }
  get _user_agent() {
    return this.conditions.user_agent || "";
  }
  get _media_query() {
    return this.conditions.media_query || "";
  }
  get _query_string() {
    return this.conditions.query_string || "";
  }

  render() {
    if (!this.conditions) return this.html``;
    return this.html`
      <paper-input
        label="User (Seperate multiple users with a comma.)"
        .value="${this._user}"
        .configValue="${"user"}"
        @value-changed="${this._valueChanged}"
      >
      </paper-input>
      <paper-input
        label="User Agent"
        .value="${this._user_agent}"
        .configValue="${"user_agent"}"
        @value-changed="${this._valueChanged}"
      >
      </paper-input>
      <paper-input
        label="Media Query"
        .value="${this._media_query}"
        .configValue="${"media_query"}"
        @value-changed="${this._valueChanged}"
      >
      </paper-input>
      <paper-input
        label="Query String"
        .value="${this._query_string}"
        .configValue="${"query_string"}"
        @value-changed="${this._valueChanged}"
      >
      </paper-input>
    `;
  }

  _valueChanged(ev) {
    if (!this.conditions) return;
    const target = ev.target;
    if (this[`_${target.configValue}`] === target.value) return;
    if (target.configValue) {
      if (target.value === "") {
        delete this.conditions[target.configValue];
      } else {
        this.conditions = {
          ...this.conditions,
          [target.configValue]: target.value
        };
      }
    }
    cch.fireEvent(this, "cch-conditions-changed", {
      conditions: this.conditions
    });
  }
}

customElements.define("cch-conditions-editor", CchConditionsEditor);
