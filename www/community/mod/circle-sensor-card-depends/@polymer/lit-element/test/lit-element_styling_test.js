/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
import '@webcomponents/shadycss/apply-shim.min.js';
import { html, LitElement, } from '../lit-element.js';
const assert = chai.assert;
suite('Styling', () => {
    let container;
    setup(() => {
        container = document.createElement('div');
        document.body.appendChild(container);
    });
    teardown(() => {
        if (container && container.parentNode) {
            container.parentNode.removeChild(container);
        }
    });
    test('content shadowRoot is styled', () => {
        customElements.define('s-1', class extends LitElement {
            _render() {
                return html `
        <style>
          div {
            border: 2px solid blue;
          }
        </style>
        <div>Testing...</div>`;
            }
        });
        const el = document.createElement('s-1');
        container.appendChild(el);
        const div = el.shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '2px');
    });
    test('shared styling rendered into shadowRoot is styled', () => {
        const style = html `<style>
      div {
        border: 4px solid blue;
      }
    </style>`;
        customElements.define('s-2', class extends LitElement {
            _render() {
                return html `
        <style>
          div {
            border: 2px solid blue;
          }
        </style>
        ${style}
        <div>Testing...</div>`;
            }
        });
        const el = document.createElement('s-2');
        container.appendChild(el);
        const div = el.shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '4px');
    });
    test('custom properties render', () => {
        customElements.define('s-3', class extends LitElement {
            _render() {
                return html `
        <style>
          :host {
            --border: 8px solid red;
          }
          div {
            border: var(--border);
          }
        </style>
        <div>Testing...</div>`;
            }
        });
        const el = document.createElement('s-3');
        container.appendChild(el);
        const div = el.shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '8px');
    });
    test('custom properties flow to nested elements', () => {
        customElements.define('s-4-inner', class extends LitElement {
            _render() {
                return html `
        <style>
          div {
            border: var(--border);
          }
        </style>
        <div>Testing...</div>`;
            }
        });
        customElements.define('s-4', class extends LitElement {
            _render() {
                return html `
        <style>
          s-4-inner {
            --border: 8px solid red;
          }
        </style>
        <s-4-inner></s-4-inner>`;
            }
        });
        const el = document.createElement('s-4');
        container.appendChild(el);
        const div = el.shadowRoot.querySelector('s-4-inner').shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '8px');
    });
    test('elements with custom properties can move between elements', (done) => {
        customElements.define('s-5-inner', class extends LitElement {
            _render() {
                return html `
        <style>
          div {
            border: var(--border);
          }
        </style>
        <div>Testing...</div>`;
            }
        });
        customElements.define('s-5', class extends LitElement {
            _render() {
                return html `
        <style>
          s-5-inner {
            --border: 2px solid red;
          }
        </style>
        <s-5-inner></s-5-inner>`;
            }
        });
        customElements.define('s-6', class extends LitElement {
            _render() {
                return html `
        <style>
          s-5-inner {
            --border: 8px solid red;
          }
        </style>`;
            }
        });
        const el = document.createElement('s-5');
        const el2 = document.createElement('s-6');
        container.appendChild(el);
        container.appendChild(el2);
        const inner = el.shadowRoot.querySelector('s-5-inner');
        const div = inner.shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '2px');
        el2.shadowRoot.appendChild(inner);
        requestAnimationFrame(() => {
            assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '8px');
            done();
        });
    });
    test('@apply renders in nested elements', () => {
        customElements.define('s-7-inner', class extends LitElement {
            _render() {
                return html `
        <style>
          div {
            @apply --bag;
          }
        </style>
        <div>Testing...</div>`;
            }
        });
        customElements.define('s-7', class extends LitElement {
            _render() {
                return html `
        <style>
          s-7-inner {
            --bag: {
              border: 10px solid red;
            }
          }
        </style>
        <s-7-inner></s-7-inner>`;
            }
        });
        const el = document.createElement('s-7');
        container.appendChild(el);
        const div = el.shadowRoot.querySelector('s-7-inner').shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '10px');
    });
});
suite('ShadyDOM', () => {
    let container;
    setup(function () {
        if (!window.ShadyDOM) {
            this.skip();
        }
        else {
            container = document.createElement('div');
            document.body.appendChild(container);
        }
    });
    teardown(() => {
        if (container && container.parentNode) {
            container.parentNode.removeChild(container);
        }
    });
    test('properties in styles render with initial value and cannot be changed', async () => {
        let border = `6px solid blue`;
        customElements.define('shady-1', class extends LitElement {
            _render() {
                return html `
        <style>
          div {
            border: ${border};
          }
        </style>
        <div>Testing...</div>`;
            }
        });
        const el = document.createElement('shady-1');
        container.appendChild(el);
        const div = el.shadowRoot.querySelector('div');
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '6px');
        border = `4px solid orange`;
        el.requestRender();
        await el.renderComplete;
        assert.equal(getComputedStyle(div).getPropertyValue('border-top-width').trim(), '6px');
    });
});
//# sourceMappingURL=lit-element_styling_test.js.map