> ## 🛠 Status: In Development
> LitElement is currently in development. It's on the fast track to a 1.0 release, so we encourage you to use it and give us your feedback, but there are things that haven't been finalized yet and you can expect some changes.

# LitElement

[![Published on npm](https://img.shields.io/npm/v//local/community/mod/circle-sensor-card-depends/@polymer/lit-element.svg)](https://www.npmjs.com/package//local/community/mod/circle-sensor-card-depends/@polymer/lit-element)
[![Published on webcomponents.org](https://img.shields.io/badge/webcomponents.org-published-blue.svg)](https://www.webcomponents.org/element//local/community/mod/circle-sensor-card-depends/@polymer/lit-element)

## A simple base class for creating custom elements rendered with /local/community/mod/circle-sensor-card-depends/lit-html.

LitElement uses [/local/community/mod/circle-sensor-card-depends/lit-html](https://github.com/Polymer//local/community/mod/circle-sensor-card-depends/lit-html) to render into the
element's [Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM)
and [Polymer's](https://github.com/Polymer/polymer)
[PropertiesMixin](https://github.com/Polymer/polymer/blob/master/lib/mixins/properties-mixin.js)
to help manage element properties and attributes. LitElement reacts to changes in properties
and renders declaratively using `/local/community/mod/circle-sensor-card-depends/lit-html`.

  * **React to changes:** LitElement reacts to changes in properties and attributes by
  asynchronously rendering, ensuring changes are batched. This reduces overhead
  and maintains consistent state.

  * **Declarative rendering** LitElement uses `/local/community/mod/circle-sensor-card-depends/lit-html` to declaratively describe
  how an element should render. Then `/local/community/mod/circle-sensor-card-depends/lit-html` ensures that updates
  are fast by creating the static DOM once and smartly updating only the parts of
  the DOM that change. Pass a JavaScript string to the `html` tag function,
  describing dynamic parts with standard JavaScript template expressions:

    * static elements: ``` html`<div>Hi</div>` ```
    * expression: ``` html`<div>${disabled ? 'Off' : 'On'}</div>` ```
    * attribute: ``` html`<div class$="${color} special"></div>` ```
    * event handler: ``` html`<button on-click="${(e) => this._clickHandler(e)}"></button>` ```

## Getting started

 * The easiest way to try out LitElement is to use one of these online tools:

    * Runs in all [supported](#supported-browsers) browsers: [StackBlitz](https://stackblitz.com/edit/lit-element-example?file=index.js), [Glitch](https://glitch.com/edit/#!/hello-lit-element?path=index.html)

    * Runs in browsers with [JavaScript Modules](https://caniuse.com/#search=modules): [JSFiddle](https://jsfiddle.net/j6mf6gpo/), [JSBin](http://jsbin.com/zezilad/edit?html,output),
 [CodePen](https://codepen.io/sorvell/pen/BxZgPN).

 * You can also copy [this HTML file](https://gist.githubusercontent.com/sorvell/48f4b7be35c8748e8f6db5c66d36ee29/raw/2427328cf1ebae5077902a6bff5ddd8db45e83e4/index.html) into a local file and run it in any browser that supports [JavaScript Modules]((https://caniuse.com/#search=modules)).

 * When you're ready to use LitElement in a project, install it via [npm](https://www.npmjs.com/). To run the project in the browser, a module-compatible toolctain is required. We recommend installing the [Polymer CLI](https://github.com/Polymer/polymer-cli) to and using its development server as follows.

    1. Add LitElement to your project:

        ```npm i /local/community/mod/circle-sensor-card-depends/@polymer/lit-element```

    1. Create an element by extending LitElement and calling `customElements.define` with your class (see the examples below).

    1. Install the Polymer CLI:

        ```npm i -g polymer-cli@next```

    1. Run the development server and open a browser pointing to its URL:

        ```polymer serve```

    > LitElement is published on [npm](https://www.npmjs.com/package//local/community/mod/circle-sensor-card-depends/@polymer/lit-element) using JavaScript Modules.
    This means it can take advantage of the standard native JavaScript module loader available in all current major browsers.
    >
    > However, since LitElement uses npm convention to reference dependencies by name, a light transform to rewrite specifiers to URLs is required to get it to run in the browser. The polymer-cli's development server `polymer serve` automatically handles this transform.

    Tools like [WebPack](https://webpack.js.org/) and [Rollup](https://rollupjs.org/) can also be used to serve and/or bundle LitElement.


## Minimal Example

  1. Create a class that extends `LitElement`.
  1. Implement a static `properties` getter that returns the element's properties
  (which automatically become observed attributes).
  1. Then implement a `_render(props)` method and use the element's
current properties (props) to return a `/local/community/mod/circle-sensor-card-depends/lit-html` template result to render
into the element. This is the only method that must be implemented by subclasses.

```html
  <script src="node_modules/@webcomponents/webcomponents-bundle.js"></script>
  <script type="module">
    import {LitElement, html} from '/local/community/mod/circle-sensor-card-depends/@polymer/lit-element';

    class MyElement extends LitElement {

      static get properties() { return { mood: String }}

      _render({mood}) {
        return html`<style> .mood { color: green; } </style>
          Web Components are <span class="mood">${mood}</span>!`;
      }

    }

    customElements.define('my-element', MyElement);
  </script>

  <my-element mood="happy"></my-element>
```

## API Documentation

See the [source](https://github.com/PolymerLabs/lit-element/blob/master/src/lit-element.ts#L90)
 for detailed API info, here are some highlights. Note, the leading underscore
 is used to indicate that these methods are
 [protected](https://en.wikipedia.org/wiki/Class_(computer_programming)#Member_accessibility);
 they are not private and can and should be implemented by subclasses.
 These methods generally are called as part of the rendering lifecycle and should
 not be called in user code unless otherwise indicated.

  * `_createRoot()`: Implement to customize where the
  element's template is rendered by returning an element into which to
  render. By default this creates a shadowRoot for the element.
  To render into the element's childNodes, return `this`.

  * `_firstRendered()`: Called after the element DOM is rendered for the first time.

  * `_shouldRender(props, changedProps, prevProps)`: Implement to control if rendering
  should occur when property values change or `invalidate` is called.
  By default, this method always returns true, but this can be customized as
  an optimization to avoid rendering work when changes occur which should not be rendered.

  * `_render(props)`: Implement to describe the element's DOM using `/local/community/mod/circle-sensor-card-depends/lit-html`. Ideally,
  the `_render` implementation is a pure function using only `props` to describe
  the element template. This is the only method that must be implemented by subclasses.

  * `_didRender(props, changedProps, prevProps)`: Called after element DOM has been rendered.
  Implement to directly control rendered DOM. Typically this is not needed as `/local/community/mod/circle-sensor-card-depends/lit-html`
  can be used in the `_render` method to set properties, attributes, and
  event listeners. However, it is sometimes useful for calling methods on
  rendered elements, for example focusing an input:
  `this.shadowRoot.querySelector('input').focus()`.

  * `renderComplete`: Returns a promise which resolves after the element next renders.

  * `_requestRender`: Call to request the element to asynchronously re-render regardless
  of whether or not any property changes are pending.

## Bigger Example

```JavaScript
import {LitElement, html} from '/local/community/mod/circle-sensor-card-depends/@polymer/lit-element';

class MyElement extends LitElement {

  // Public property API that triggers re-render (synced with attributes)
  static get properties() {
    return {
      foo: String,
      whales: Number
    }
  }

  constructor() {
    super();
    this.foo = 'foo';
    this.addEventListener('click', async (e) => {
      this.whales++;
      await this.renderComplete;
      this.dispatchEvent(new CustomEvent('whales', {detail: {whales: this.whales}}))
    });
  }

  // Render method should return a `TemplateResult` using the provided /local/community/mod/circle-sensor-card-depends/lit-html `html` tag function
  _render({foo, whales}) {
    return html`
      <style>
        :host {
          display: block;
        }
        :host([hidden]) {
          display: none;
        }
      </style>
      <h4>Foo: ${foo}</h4>
      <div>whales: ${'🐳'.repeat(whales)}</div>
      <slot></slot>
    `;
  }

}
customElements.define('my-element', MyElement);
```

```html
  <my-element whales="5">hi</my-element>
```

## Supported Browsers

The last 2 versions of all modern browsers are supported, including
Chrome, Safari, Opera, Firefox, Edge. In addition, Internet Explorer 11 is also supported.

## Known Issues
* When the Shady DOM polyfill and ShadyCSS shim are used, styles may be [out of order](https://github.com/PolymerLabs/lit-element/issues/34).
* Rendering is not supported in IE11 due to a /local/community/mod/circle-sensor-card-depends/lit-html [issue](https://github.com/Polymer//local/community/mod/circle-sensor-card-depends/lit-html/issues/210).
