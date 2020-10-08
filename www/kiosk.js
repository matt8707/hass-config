// https://gist.github.com/corrafig/c8288df960e7f59e82c12d14de26fde8

if (window.location.href.indexOf('kiosk') > 0) {
    setTimeout(function () {
        try {
            const home_assistant_main =  document
                  .querySelector("body > home-assistant").shadowRoot
                  .querySelector("home-assistant-main");
            
            const header = home_assistant_main.shadowRoot
                  .querySelector("app-drawer-layout > partial-panel-resolver > ha-panel-lovelace").shadowRoot
                  .querySelector("hui-root").shadowRoot
                  .querySelector("#layout > app-header")
                  .style.display = "none";
            
            const drawer = home_assistant_main.shadowRoot
                  .querySelector("#drawer")
                  .style.display = 'none';
            
            home_assistant_main.style.setProperty("--app-drawer-width", 0);
            home_assistant_main.shadowRoot
                .querySelector("#drawer > ha-sidebar").shadowRoot
                .querySelector("div.menu > paper-icon-button")
                .click();
            window.dispatchEvent(new Event('resize'));
        }
        catch (e) {
            console.log(e);
        }
    }, 200);
}
