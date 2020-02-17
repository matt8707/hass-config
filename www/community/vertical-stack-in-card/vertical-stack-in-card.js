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
        
        const shadow = this.shadowRoot;
        while (shadow.hasChildNodes()) {
            shadow.removeChild(shadow.lastChild);
        }
        
        const card = document.createElement("ha-card");
        const cardContent = document.createElement("div");
        
        card.header = config.title;
        this._refCards = [];
        
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
                cardContent.appendChild(element);
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

                cardContent.appendChild(element);
                this._refCards.push(element);
            }
        });
        card.appendChild(cardContent);
        shadow.appendChild(card);
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
