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

import {TemplateResult} from '/local/community/mod/circle-sensor-card-depends/lit-html//local/community/mod/circle-sensor-card-depends/lit-html.js';

import {
  classString,
  html,
  LitElement,
  renderAttributes,
  styleString,
} from '../lit-element.js';

import {stripExpressionDelimeters} from './test-helpers.js';

const assert = chai.assert;

suite('LitElement', () => {
  let container: HTMLElement;

  setup(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  teardown(() => {
    if (container && container.parentNode) {
      container.parentNode.removeChild(container);
    }
  });

  test('renders initial content into shadowRoot', () => {
    const rendered = `hello world`;
    customElements.define('x-1', class extends LitElement {
      _render() { return html`${rendered}`; }
    });
    const el = document.createElement('x-1');
    container.appendChild(el);
    assert.ok(el.shadowRoot);
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        rendered);
  });

  test('can set render target to light dom', () => {
    const rendered = `hello world`;
    customElements.define('x-1a', class extends LitElement {
      _render() { return html`${rendered}`; }

      _createRoot() { return this; }
    });
    const el = document.createElement('x-1a');
    container.appendChild(el);
    assert.notOk(el.shadowRoot);
    assert.equal(stripExpressionDelimeters(el.innerHTML), rendered);
  });

  test('renders when created via constructor', () => {
    const rendered = `hello world`;
    class E extends LitElement {
      _render() { return html`${rendered}`; }
    }
    customElements.define('x-2', E);
    const el = new E();
    container.appendChild(el);
    assert.ok(el.shadowRoot);
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        rendered);
  });

  test('renders changes when properties change', (done) => {
    class E extends LitElement {
      static get properties() { return {foo : String}; }

      foo = 'one';

      _render(props: {foo: string}) { return html`${props.foo}`; }
    }
    customElements.define('x-3', E);
    const el = new E();
    container.appendChild(el);
    assert.ok(el.shadowRoot);
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        'one');
    el.foo = 'changed';
    requestAnimationFrame(() => {
      assert.equal(
          stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
          'changed');
      done();
    });
  });

  test('renders changes when attributes change', (done) => {
    class E extends LitElement {
      static get properties() { return {foo : String}; }

      foo = 'one';

      _render(props: {foo: string}) { return html`${props.foo}`; }
    }
    customElements.define('x-4', E);
    const el = new E();
    container.appendChild(el);
    assert.ok(el.shadowRoot);
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        'one');
    el.setAttribute('foo', 'changed');
    requestAnimationFrame(() => {
      assert.equal(
          stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
          'changed');
      done();
    });
  });

  test('_firstRendered call after first render and not subsequent renders',
       async () => {
         class E extends LitElement {
           static get properties() { return {foo : String}; }

           foo = 'one';
           firstRenderedCount = 0;
           domAtFirstRendered = '';

           _firstRendered() {
             this.firstRenderedCount++;
             this.domAtFirstRendered =
                 stripExpressionDelimeters(this.shadowRoot!.innerHTML);
           }

           _render(props: {foo: string}) { return html`${props.foo}`; }
         }
         customElements.define('x-5', E);
         const el = new E();
         container.appendChild(el);
         assert.equal(el.firstRenderedCount, 1);
         assert.ok(el.shadowRoot);
         assert.equal(
             stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
             el.domAtFirstRendered);
         assert.equal(el.foo, el.domAtFirstRendered);
         el.foo = 'two';
         await el.renderComplete;
         assert.equal(el.firstRenderedCount, 1);
         assert.equal(
             stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
             el.foo);
         assert.notEqual(el.foo, el.domAtFirstRendered);
       });

  test('User defined accessor can trigger rendering', async () => {
    class E extends LitElement {
      __bar?: number;

      static get properties() { return {foo : Number, bar : Number}; }

      info: string[] = [];
      foo = 0;

      get bar() { return this._getProperty('bar'); }

      set bar(value) {
        this.__bar = value;
        this._setProperty('bar', value);
      }

      _render(props: {foo: string, bar: number}) {
        this.info.push('render');
        return html`${props.foo}${props.bar}`;
      }
    }
    customElements.define('x-6', E);
    const el = new E();
    container.appendChild(el);
    el.setAttribute('bar', '20');
    await el.renderComplete;
    assert.equal(el.bar, 20);
    assert.equal(el.__bar, 20);
    assert.equal(stripExpressionDelimeters(el.shadowRoot!.innerHTML), '020');
  });

  test('render attributes, properties, and event listeners via /local/community/mod/circle-sensor-card-depends/lit-html',
       function() {
         class E extends LitElement {
           _event?: Event;

           _render() {
             const attr = 'attr';
             const prop = 'prop';
             const event = (e: Event) => { this._event = e; };
             return html
             `<div attr$="${attr}" prop="${prop}" on-zug="${event}"></div>`;
           }
         }
         customElements.define('x-7', E);
         const el = new E();
         container.appendChild(el);
         const d = el.shadowRoot!.querySelector('div')! as (HTMLDivElement &
                                                            {prop: string});
         assert.equal(d.getAttribute('attr'), 'attr');
         assert.equal(d.prop, 'prop');
         const e = new Event('zug');
         d.dispatchEvent(e);
         assert.equal(el._event, e);
       });

  test('renderComplete waits until next rendering', async () => {
    class E extends LitElement {
      static get properties() { return {foo : Number}; }

      foo = 0;

      _render(props: {foo: string}) { return html`${props.foo}`; }
    }
    customElements.define('x-8', E);
    const el = new E();
    container.appendChild(el);
    el.foo++;
    await el.renderComplete;
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        '1');
    el.foo++;
    await el.renderComplete;
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        '2');
    el.foo++;
    await el.renderComplete;
    assert.equal(
        stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
        '3');
  });

  test('_shouldRender controls rendering', async () => {
    class E extends LitElement {
      static get properties() { return {foo : Number}; }

      foo = 0;
      renderCount = 0;
      allowRender = true;

      _render() {
        this.renderCount++;
        return html`hi`;
      }

      _shouldRender() { return this.allowRender; }
    }
    customElements.define('x-9', E);
    const el = new E();
    container.appendChild(el);
    assert.equal(el.renderCount, 1);
    el.foo++;
    await el.renderComplete;
    assert.equal(el.renderCount, 2);
    el.allowRender = false;
    el.foo++;
    await el.renderComplete;
    assert.equal(el.renderCount, 2);
    el.allowRender = true;
    el.foo++;
    await el.renderComplete;
    assert.equal(el.renderCount, 3);
  });

  test('renderComplete returns true if rendering happened and false otherwise',
       async () => {
         class E extends LitElement {

           needsRender = true;

           static get properties() { return {foo : Number}; }

           _shouldRender() { return this.needsRender; }

           foo = 0;

           _render(props: {foo: string}) { return html`${props.foo}`; }
         }
         customElements.define('x-9.1', E);
         const el = new E();
         container.appendChild(el);
         el.foo++;
         let rendered;
         rendered = await el.renderComplete;
         assert.equal(rendered, true);
         assert.equal(
             stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
             '1');
         el.needsRender = false;
         el.foo++;
         rendered = await el.renderComplete;
         assert.equal(rendered, false);
         assert.equal(
             stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
             '1');
         el.needsRender = true;
         el.foo++;
         rendered = await el.renderComplete;
         assert.equal(rendered, true);
         assert.equal(
             stripExpressionDelimeters((el.shadowRoot as ShadowRoot).innerHTML),
             '3');
         el.requestRender();
         rendered = await el.renderComplete;
         assert.equal(rendered, true);
         rendered = await el.renderComplete;
         assert.equal(rendered, false);
       });

  test(
      'render lifecycle order: _shouldRender, _render, _applyRender, _didRender',
      async () => {
        class E extends LitElement {
          static get properties() { return {foo : Number}; }

          info: Array<string> = [];

          _shouldRender() {
            this.info.push('_shouldRender');
            return true;
          }

          _render() {
            this.info.push('_render');
            return html`hi`;
          }

          _applyRender(result: TemplateResult, root: Element|DocumentFragment) {
            this.info.push('_applyRender');
            super._applyRender(result, root);
          }

          _didRender() { this.info.push('_didRender'); }
        }
        customElements.define('x-10', E);
        const el = new E();
        container.appendChild(el);
        await el.renderComplete;
        assert.deepEqual(
            el.info,
            [ '_shouldRender', '_render', '_applyRender', '_didRender' ]);
      });

  test('renderAttributes renders attributes on element', async () => {
    class E extends LitElement {
      static get properties() { return {foo : Number, bar : Boolean}; }

      foo = 0;
      bar = true;

      _render({foo, bar}: {foo: number, bar: boolean}) {
        renderAttributes(this, {foo, bar});
        return html`${foo}${bar}`;
      }
    }
    customElements.define('x-11', E);
    const el = new E();
    container.appendChild(el);
    assert.equal(el.getAttribute('foo'), '0');
    assert.equal(el.getAttribute('bar'), '');
    el.foo = 5;
    el.bar = false;
    await el.renderComplete;
    assert.equal(el.getAttribute('foo'), '5');
    assert.equal(el.hasAttribute('bar'), false);
  });

  test('classString updates classes', async () => {
    class E extends LitElement {
      static get properties() {
        return {foo : Number, bar : Boolean, baz : Boolean};
      }

      foo = 0;
      bar = true;
      baz = false;

      _render({foo, bar, baz}: {foo: number, bar: boolean, baz: boolean}) {
        return html
        `<div class$="${classString({foo, bar, zonk : baz})}"></div>`;
      }
    }
    customElements.define('x-12', E);
    const el = new E();
    container.appendChild(el);
    const d = el.shadowRoot!.querySelector('div')!;
    assert.include(d.className, 'bar');
    el.foo = 1;
    el.baz = true;
    await el.renderComplete;
    assert.include(d.className, 'foo bar zonk');
    el.bar = false;
    await el.renderComplete;
    assert.include(d.className, 'foo zonk');
    el.foo = 0;
    el.baz = false;
    await el.renderComplete;
    assert.notInclude(d.className, 'foo bar zonk');
  });

  test('styleString updates style', async () => {
    class E extends LitElement {
      static get properties() {
        return {
          marginTop : String,
          paddingTop : String,
          zug : String
        };
      }

      marginTop = ``;
      paddingTop = ``;
      zug = `0px`;

      _render(
          {marginTop, paddingTop, zug}:
              {marginTop: string, paddingTop: string, zug: string}) {
        return html`<div style$="${
            styleString(
                {marginTop, paddingTop, height : zug})}"></div>`;
      }
    }
    customElements.define('x-13', E);
    const el = new E();
    container.appendChild(el);
    const d = el.shadowRoot!.querySelector('div')!;
    let computed = getComputedStyle(d);
    assert.equal(computed.getPropertyValue('margin-top'), '0px');
    assert.equal(computed.getPropertyValue('height'), '0px');
    el.marginTop = `2px`;
    el.paddingTop = `5px`;
    await el.renderComplete;
    el.offsetWidth;
    computed = getComputedStyle(d);
    assert.equal(computed.getPropertyValue('margin-top'), '2px');
    assert.equal(computed.getPropertyValue('height'), '0px');
    assert.equal(computed.getPropertyValue('padding-top'), '5px');
    el.marginTop = ``;
    el.paddingTop = ``;
    el.zug = ``;
    await el.renderComplete;
    assert.equal(d.style.cssText, '');
  });

  test('warns when setting properties re-entrantly', async () => {
    class E extends LitElement {
      _toggle: boolean = false;

      _render() {
        this._setProperty('foo', this._toggle ? 'fooToggle' : 'foo');
        return html`hi`;
      }

      _didRender() {
        this._setProperty('zonk', this._toggle ? 'zonkToggle' : 'zonk');
      }

    }
    const calls: IArguments[] = [];
    const orig = console.trace;
    console.trace = function() { calls.push(arguments); };
    customElements.define('x-14', E);
    const el = new E();
    container.appendChild(el);
    assert.equal(calls.length, 2);
    el._toggle = true;
    el.requestRender();
    await el.renderComplete;
    assert.equal(calls.length, 4);
    console.trace = orig;
  });
});
