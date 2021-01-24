const ha = document.querySelector('home-assistant');
const main = ha.shadowRoot.querySelector('home-assistant-main').shadowRoot;
const panel = main.querySelector('partial-panel-resolver');
const drawerLayout = main.querySelector('app-drawer-layout');
let llAttempts = 1;
let interv;

function getConfigObj() {
  const ll = main.querySelector('ha-panel-lovelace');

  if (!ll || !ll.lovelace || !ll.lovelace.config) {
    return;
  } else {
    return ll && ll.lovelace.config.kiosk_mode
      ? ll.lovelace.config.kiosk_mode
      : {};
  }
}

function getConfig() {
  return new Promise((resolve, reject) => {
    interv = setInterval(() => {
      console.log('Attempt #%s', llAttempts);
      if (getConfigObj()) {
        interv = clearInterval(interv);
        resolve(getConfigObj());
      } else {
        llAttempts++;
        if (llAttempts == 10) {
          interv = clearInterval(interv);
          resolve(null);
        }
      }
    }, 100);
  });
}

// Return true if any keyword is found in location.
function locIncludes(keywords) {
  const url = window.location.search;
  return keywords.some((x) => url.includes(x));
}

// Check if element exists and if style element already exists.
function styleCheck(elem) {
  return elem && !elem.querySelector('#kiosk_mode');
}

// Insert style element.
function addStyles(css, elem) {
  const style = document.createElement('style');
  style.setAttribute('id', 'kiosk_mode');
  style.innerHTML = css;
  elem.appendChild(style);
  window.dispatchEvent(new Event('resize'));
}

// Set localStorage item.
function setCache(k, v) {
  window.localStorage.setItem(k, v);
}

// Retrieve localStorage item as bool.
function cacheAsBool(k) {
  return window.localStorage.getItem(k) == 'true';
}

// Clear cache if requested.
if (window.location.search.includes('clear_km_cache')) {
  ['kmHeader', 'kmSidebar'].forEach((k) => setCache(k, 'false'));
}

function kiosk_mode() {
  const url = window.location.search;
  const hass = ha.hass;

  // Disable styling if "disable_km" in URL.
  if (url.includes('disable_km')) return;

  // Retrieve localStorage values & query string options.
  let hide_header =
    cacheAsBool('kmHeader') || locIncludes(['kiosk', 'hide_header']);
  let hide_sidebar =
    cacheAsBool('kmSidebar') || locIncludes(['kiosk', 'hide_sidebar']);

  getConfig().then((config) => {
    if (!config) {
      return;
    }

    const adminConf = config.admin_settings;
    const nonAdminConf = config.non_admin_settings;
    let userConf = config.user_settings;
    const queryStringsSet = hide_sidebar || hide_header;

    // Use config values only if config strings and cache aren't used.
    hide_header = queryStringsSet
      ? hide_header
      : config.kiosk || config.hide_header;
    hide_sidebar = queryStringsSet
      ? hide_sidebar
      : config.kiosk || config.hide_sidebar;

    if (adminConf && hass.user.is_admin) {
      hide_header = adminConf.kiosk || adminConf.hide_header;
      hide_sidebar = adminConf.kiosk || adminConf.hide_sidebar;
    }

    if (nonAdminConf && !hass.user.is_admin) {
      hide_header = nonAdminConf.kiosk || nonAdminConf.hide_header;
      hide_sidebar = nonAdminConf.kiosk || nonAdminConf.hide_sidebar;
    }

    if (userConf) {
      if (!Array.isArray(userConf)) userConf = [userConf];
      for (let conf of userConf) {
        let users = conf.users;
        if (!Array.isArray(conf.users)) users = [users];
        if (
          users.some((x) => x.toLowerCase() == hass.user.name.toLowerCase())
        ) {
          hide_header = conf.kiosk || conf.hide_header;
          hide_sidebar = conf.kiosk || conf.hide_sidebar;
        }
      }
    }

    // Only run if needed.
    if (hide_sidebar || hide_header) {
      const lovelace = main.querySelector('ha-panel-lovelace');
      const huiRoot = lovelace
        ? lovelace.shadowRoot.querySelector('hui-root').shadowRoot
        : null;
      const toolbar = huiRoot ? huiRoot.querySelector('app-toolbar') : null;

      // Insert style element for kiosk or hide_header options.
      if (hide_header && styleCheck(huiRoot)) {
        const css =
          '#view { min-height: 100vh !important } app-header { display: none }';
        addStyles(css, huiRoot);

        // Set localStorage cache for hiding header.
        if (url.includes('cache')) setCache('kmHeader', 'true');
      }

      // Insert style element for kiosk or hide_sidebar options.
      if (hide_sidebar && styleCheck(drawerLayout)) {
        const css =
          ':host { --app-drawer-width: 0 !important } #drawer { display: none }';
        addStyles(css, drawerLayout);

        // Hide menu button.
        if (styleCheck(toolbar))
          addStyles('ha-menu-button { display:none !important } ', toolbar);

        // Set localStorage cache for hiding sidebar.
        if (url.includes('cache')) setCache('kmSidebar', 'true');
      }
    }
  });
}

// Initial run.
kiosk_mode();

// Watch for changes in partial-panel-resolver's children.
new MutationObserver(lovelaceWatch).observe(panel, {childList: true});

// If new lovelace panel was added watch for hui-root to appear.
function lovelaceWatch(mutations) {
  for (let mutation of mutations) {
    for (let node of mutation.addedNodes) {
      if (node.localName == 'ha-panel-lovelace') {
        new MutationObserver(rootWatch).observe(node.shadowRoot, {
          childList: true,
        });
        return;
      }
    }
  }
}

// When hui-root appears watch it's children.
function rootWatch(mutations) {
  for (let mutation of mutations) {
    for (let node of mutation.addedNodes) {
      if (node.localName == 'hui-root') {
        new MutationObserver(appLayoutWatch).observe(node.shadowRoot, {
          childList: true,
        });
        return;
      }
    }
  }
}

// When ha-app-layout appears we can run.
function appLayoutWatch(mutations) {
  for (let mutation of mutations) {
    for (let node of mutation.addedNodes) {
      if (node.localName == 'ha-app-layout') {
        kiosk_mode();
        return;
      }
    }
  }
}

// Overly complicated console tag.
const conInfo = {header: '%c≡ kiosk-mode'.padEnd(27), ver: '%cversion *DEV '};
const br = '%c\n';
const maxLen = Math.max(...Object.values(conInfo).map((el) => el.length));
for (const [key] of Object.entries(conInfo)) {
  if (conInfo[key].length <= maxLen) conInfo[key] = conInfo[key].padEnd(maxLen);
  if (key == 'header') conInfo[key] = `${conInfo[key].slice(0, -1)}⋮ `;
}
const header =
  'display:inline-block;border-width:1px 1px 0 1px;border-style:solid;border-color:#424242;color:white;background:#03a9f4;font-size:12px;padding:4px 4.5px 5px 6px;';
const info =
  'border-width:0px 1px 1px 1px;padding:7px;background:white;color:#424242;line-height:0.7;';
console.info(
  conInfo.header + br + conInfo.ver,
  header,
  '',
  `${header} ${info}`
);
