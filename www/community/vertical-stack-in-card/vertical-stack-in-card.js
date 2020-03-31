const vsinVersion = '0.3.2';
console.log(`%cvertical-stack-in-card\n%cVersion: ${vsinVersion}`, 'color: #1976d2; font-weight: bold;', '');

class VerticalStackInCard extends HTMLElement {
    constructor() {
        super();
    }

    async setConfig(config) {
        if (!config || !config.cards || !Array.isArray(config.cards)) {
            throw new Error('Card config incorrect');
        }
        this._config = config;
        this._refCards = [];

        if (window.loadCardHelpers) {
            this.helpers = await window.loadCardHelpers();
        }

        this.renderCard();
    }

    renderCard() {
        const config = this._config;
        const promises = config.cards.map(config => this.createCardElement(config));
        Promise.all(promises).then((cards) => {
            cards.forEach(card => {
                if (card.updateComplete) {
                    card.updateComplete.then(() => this.styleCard(card));
                } else {
                    this.styleCard(card);
                }
            });

            this._refCards = cards;
            const card = document.createElement('ha-card');
            const cardContent = document.createElement('div');
            card.header = config.title;
            cards.forEach(card => cardContent.appendChild(card));
            if (config.horizontal) {
                cardContent.style.display = 'flex';
                cardContent.childNodes.forEach(card => {
                    card.style.flex = '1 1 0';
                    card.style.minWidth = 0;
                });
            }
            card.appendChild(cardContent);
            
            while (this.hasChildNodes()) {
                this.removeChild(this.lastChild);
            }    
            this.appendChild(card);
        })
    }

    async createCardElement(cardConfig) {
        const createError = (error, config) => {
            return createThing('hui-error-card', {
                type: 'error',
                error,
                config,
            });
        };
        
        const createThing = (tag, config) => {
            if (this.helpers) {
                if (config.type === 'divider') {
                    return this.helpers.createRowElement(config)
                } else {
                    return this.helpers.createCardElement(config);
                }
            }
            
            const element = document.createElement(tag);
            try {
                element.setConfig(config);
            } catch (err) {
                console.error(tag, err);
                return createError(err.message, config);
            }
            return element;
        };

        let tag = cardConfig.type;
        if (tag.startsWith('divider')) {
            tag = `hui-divider-row`;
        } else if (tag.startsWith('custom:')) {
            tag = tag.substr('custom:'.length);
        } else {
            tag = `hui-${tag}-card`;
        }

        const element = createThing(tag, cardConfig);
        element.hass = this._hass;
        element.addEventListener(
            'll-rebuild',
            ev => {
                ev.stopPropagation();
                this.createCardElement(cardConfig).then(() => {
                    this.renderCard();
                });
            },
            { once: true },
        );     
        return element;     
    }

    set hass(hass) {
        this._hass = hass
        if (this._refCards) {
            this._refCards.forEach((card) => {
                card.hass = hass;
            });
        }
    }

    styleCard(element) {
        if (element.shadowRoot) {
            if (element.shadowRoot.querySelector('ha-card')) {
                let ele = element.shadowRoot.querySelector('ha-card')
                ele.style.boxShadow = 'none';
                // ele.style.borderRadius = '0';
            } else {
                let searchEles = element.shadowRoot.getElementById('root');
                if (!searchEles) {
                    searchEles = element.shadowRoot.getElementById('card');
                }
                if (!searchEles) return;
                searchEles = searchEles.childNodes;
                for (let i = 0; i < searchEles.length; i++) {
                    if (searchEles[i].style){
                        searchEles[i].style.margin = '0px';
                    }
                    this.styleCard(searchEles[i]);
                }
            }
        } else {
            if (typeof element.querySelector === 'function' && element.querySelector('ha-card')) {
                let ele = element.querySelector('ha-card')
                ele.style.boxShadow = 'none';
                // ele.style.borderRadius = '0';
            }
            let searchEles = element.childNodes;
            for (let i = 0; i < searchEles.length; i++) {
                if (searchEles[i] && searchEles[i].style) {
                    searchEles[i].style.margin = '0px';
                }
                this.styleCard(searchEles[i]);
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
