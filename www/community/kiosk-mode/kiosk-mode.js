const home_assistant_main = document
  .querySelector("body > home-assistant")
  .shadowRoot.querySelector("home-assistant-main");

const header = home_assistant_main.shadowRoot
  .querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-lovelace")
  .shadowRoot.querySelector("hui-root")
  .shadowRoot.querySelector("#layout > app-header");

const drawer = home_assistant_main.shadowRoot.querySelector("#drawer");

setTimeout(function () {
  try {
    if (window.location.href.includes("kiosk")) {
      header.style.display = "none";
      drawer.style.display = "none";
      home_assistant_main.style.setProperty("--app-drawer-width", 0);
      window.dispatchEvent(new Event("resize"));
    }
    if (window.location.href.includes("hide_header")) {
      header.style.display = "none";
      window.dispatchEvent(new Event("resize"));
    }
    if (window.location.href.includes("hide_sidebar")) {
      drawer.style.display = "none";
      home_assistant_main.style.setProperty("--app-drawer-width", 0);
      window.dispatchEvent(new Event("resize"));
    }
  } catch (e) {
    console.log(e);
  }
}, 200);

console.info(
  `%c  KIOSK-MODE   \n%c Version 1.1.0 `,
  "color: orange; font-weight: bold; background: black",
  "color: white; font-weight: bold; background: dimgray"
);
