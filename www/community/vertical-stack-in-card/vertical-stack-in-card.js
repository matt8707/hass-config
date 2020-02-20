class VerticalStackInCard extends HTMLElement {
    constructor() {
        super();
        // Make use of shadowRoot to avoid conflicts when reusing
        this.attachShadow({ mode: 'open' });
    }

    setConfig(config) {
        if (!config || !config.cards || !Array.isArray(config.cards)) {
            throw new Error('Card config incorrect');
        }

        this.style.boxShadow = "var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12), 0 3px 1px -2px rgba(0, 0, 0, 0.2))";
        this.style.borderRadius = "var(--ha-card-border-radius, 2px)";
        this.style.background = "var(--paper-card-background-color)";
        this.style.display = "block";
        this.style.overflow = "hidden";

        const root = this.shadowRoot;
        while (root.hasChildNodes()) {
            root.removeChild(root.lastChild);
        }

        this._refCards = [];
        if (config.title) {
            const title = document.createElement("div");
            title.className = "header";
            title.style = "font-family: var(--paper-font-headline_-_font-family); color: var(--paper-card-header-color); -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing); font-size: var(--paper-font-headline_-_font-size); font-weight: var(--paper-font-headline_-_font-weight); letter-spacing: var(--paper-font-headline_-_letter-spacing); line-height: var(--paper-font-headline_-_line-height);text-rendering: var(--paper-font-common-expensive-kerning_-_text-rendering);opacity: var(--dark-primary-opacity);padding: 24px 16px 0px 16px";
            title.innerHTML = '<div class="name">' + config.title + '</div>';
            root.appendChild(title);
        }

        const _createThing = (tag, config) => {
            const element = document.createElement(tag);
            try {
                element.setConfig(config);
            } catch (err) {
                console.error(tag, err);
                return _createError(err.message, config);
            }
            return element;
        };

        const _createError = (error, config) => {
            return _createThing("hui-error-card", {
                type: "error",
                error,
                config,
            });
        };

        const _fireEvent = (ev, detail, entity=null) => {
            ev = new Event(ev, {
                bubbles: true,
                cancelable: false,
                composed: true,
            });
            ev.detail = detail || {};

            if (entity) {
                entity.dispatchEvent(ev);
            } else {
                document
                    .querySelector("home-assistant")
                    .shadowRoot.querySelector("home-assistant-main")
                    .shadowRoot.querySelector("app-drawer-layout partial-panel-resolver")
                    .shadowRoot.querySelector("ha-panel-lovelace")
                    .shadowRoot.querySelector("hui-root")
                    .shadowRoot.querySelector("ha-app-layout #view")
                    .firstElementChild
                    .dispatchEvent(ev);
            }
        }

        config.cards.forEach((item) => {
            let tag = item.type;

            if (tag.startsWith("divider")) {
                tag = `hui-divider-row`;
            } else if (tag.startsWith("custom:")) {
                tag = tag.substr("custom:".length);
            } else {
                tag = `hui-${tag}-card`;
            }

            if (customElements.get(tag)) {
                const element = _createThing(tag, item);
                root.appendChild(element);
                this._refCards.push(element);
            } else {
                // If element doesn't exist (yet) create an error
                const element = _createError(
                    `Custom element doesn't exist: ${tag}.`,
                    item
                );
                element.style.display = "None";

                const time = setTimeout(() => {
                    element.style.display = "";
                }, 2000);

                // Remove error if element is defined later
                customElements.whenDefined(tag).then(() => {
                    clearTimeout(time);
                    _fireEvent("ll-rebuild", {}, element);
                });

                root.appendChild(element);
                this._refCards.push(element);
            }
        });
    }

    set hass(hass) {
        if (this._refCards) {
            this._refCards.forEach((card) => {
                card.hass = hass;
            });
        }
    }

    connectedCallback() {
        this._refCards.forEach((element) => {
            let fn = () => {
                this._card(element);
            };

            if(element.updateComplete) {
                element.updateComplete.then(fn);
            } else {
                fn();
            }
        });
    }

    _card(element) {
        if (element.shadowRoot) {
            if (!element.shadowRoot.querySelector('ha-card')) {
                let searchEles = element.shadowRoot.getElementById("root");
                if (!searchEles) {
                    searchEles = element.shadowRoot.getElementById("card");
                }
                if (!searchEles) return;
                searchEles = searchEles.childNodes;
                for (let i = 0; i < searchEles.length; i++) {
                    if(searchEles[i].style !== undefined){
                        searchEles[i].style.margin = "0px";
                    }
                    this._card(searchEles[i]);
                }
            } else {
                let ele = element.shadowRoot.querySelector('ha-card')
                ele.style.boxShadow = 'none';
                ele.style.background = 'transparent';
                ele.style.borderRadius = '0';
            }
        } else {
            if (typeof element.querySelector === 'function' && element.querySelector('ha-card')) {
                let ele = element.querySelector('ha-card')
                ele.style.boxShadow = 'none';
                ele.style.background = 'transparent';
                ele.style.borderRadius = '0';
            }
            let searchEles = element.childNodes;
            for (let i = 0; i < searchEles.length; i++) {
                if (searchEles[i] && searchEles[i].style) {
                    searchEles[i].style.margin = "0px";
                }
                this._card(searchEles[i]);
            }
        }
    }

    getCardSize() {
        let totalSize = 0;
        this._refCards.forEach((element) => {
            totalSize += typeof element.getCardSize === 'function' ? element.getCardSize() : 1;
        });
        return totalSize;
    }
}

customElements.define('vertical-stack-in-card', VerticalStackInCard);
