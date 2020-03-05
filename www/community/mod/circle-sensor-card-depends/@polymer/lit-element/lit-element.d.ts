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
import { PropertiesChangedConstructor } from '/local/community/mod/circle-sensor-card-depends/@polymer/polymer/lib/mixins/properties-changed.js';
import { PropertiesMixinConstructor } from '/local/community/mod/circle-sensor-card-depends/@polymer/polymer/lib/mixins/properties-mixin.js';
import { TemplateResult } from '/local/community/mod/circle-sensor-card-depends/lit-html//local/community/mod/circle-sensor-card-depends/lit-html.js';
export { PropertiesChangedConstructor } from '/local/community/mod/circle-sensor-card-depends/@polymer/polymer/lib/mixins/properties-changed.js';
export { PropertiesMixinConstructor } from '/local/community/mod/circle-sensor-card-depends/@polymer/polymer/lib/mixins/properties-mixin.js';
export { html, svg } from '/local/community/mod/circle-sensor-card-depends/lit-html/lib/lit-extended.js';
export declare type __unused = PropertiesChangedConstructor & PropertiesMixinConstructor;
/**
 * Renders attributes to the given element based on the `attrInfo` object where
 * boolean values are added/removed as attributes.
 * @param element Element on which to set attributes.
 * @param attrInfo Object describing attributes.
 */
export declare function renderAttributes(element: HTMLElement, attrInfo: {
    [name: string]: string | boolean | number;
}): void;
/**
 * Returns a string of css class names formed by taking the properties
 * in the `classInfo` object and appending the property name to the string of
 * class names if the property value is truthy.
 * @param classInfo
 */
export declare function classString(classInfo: {
    [name: string]: string | boolean | number;
}): string;
/**
 * Returns a css style string formed by taking the properties in the `styleInfo`
 * object and appending the property name (dash-cased) colon the
 * property value. Properties are separated by a semi-colon.
 * @param styleInfo
 */
export declare function styleString(styleInfo: {
    [name: string]: string | boolean | number;
}): string;
declare const LitElement_base: {
    new (): HTMLElement;
    prototype: HTMLElement;
} & PropertiesMixinConstructor & PropertiesChangedConstructor;
export declare class LitElement extends LitElement_base {
    private __renderComplete;
    private __resolveRenderComplete;
    private __isInvalid;
    private __isChanging;
    private _root?;
    /**
     * Override which sets up element rendering by calling* `_createRoot`
     * and `_firstRendered`.
     */
    ready(): void;
    connectedCallback(): void;
    /**
     * Called after the element DOM is rendered for the first time.
     * Implement to perform tasks after first rendering like capturing a
     * reference to a static node which must be directly manipulated.
     * This should not be commonly needed. For tasks which should be performed
     * before first render, use the element constructor.
     */
    _firstRendered(): void;
    /**
     * Implement to customize where the element's template is rendered by
     * returning an element into which to render. By default this creates
     * a shadowRoot for the element. To render into the element's childNodes,
     * return `this`.
     * @returns {Element|DocumentFragment} Returns a node into which to render.
     */
    protected _createRoot(): Element | DocumentFragment;
    /**
     * Override which returns the value of `_shouldRender` which users
     * should implement to control rendering. If this method returns false,
     * _propertiesChanged will not be called and no rendering will occur even
     * if property values change or `requestRender` is called.
     * @param _props Current element properties
     * @param _changedProps Changing element properties
     * @param _prevProps Previous element properties
     * @returns {boolean} Default implementation always returns true.
     */
    _shouldPropertiesChange(_props: object, _changedProps: object, _prevProps: object): boolean;
    /**
     * Implement to control if rendering should occur when property values
     * change or `requestRender` is called. By default, this method always
     * returns true, but this can be customized as an optimization to avoid
     * rendering work when changes occur which should not be rendered.
     * @param _props Current element properties
     * @param _changedProps Changing element properties
     * @param _prevProps Previous element properties
     * @returns {boolean} Default implementation always returns true.
     */
    protected _shouldRender(_props: object, _changedProps: object, _prevProps: object): boolean;
    /**
     * Override which performs element rendering by calling
     * `_render`, `_applyRender`, and finally `_didRender`.
     * @param props Current element properties
     * @param changedProps Changing element properties
     * @param prevProps Previous element properties
     */
    _propertiesChanged(props: object, changedProps: object, prevProps: object): void;
    _flushProperties(): void;
    /**
     * Override which warns when a user attempts to change a property during
     * the rendering lifecycle. This is an anti-pattern and should be avoided.
     * @param property {string}
     * @param value {any}
     * @param old {any}
     */
    _shouldPropertyChange(property: string, value: any, old: any): boolean;
    /**
     * Implement to describe the DOM which should be rendered in the element.
     * Ideally, the implementation is a pure function using only props to describe
     * the element template. The implementation must return a `/local/community/mod/circle-sensor-card-depends/lit-html`
     * TemplateResult. By default this template is rendered into the element's
     * shadowRoot. This can be customized by implementing `_createRoot`. This
     * method must be implemented.
     * @param {*} _props Current element properties
     * @returns {TemplateResult} Must return a /local/community/mod/circle-sensor-card-depends/lit-html TemplateResult.
     */
    protected _render(_props: object): TemplateResult;
    /**
     * Renders the given /local/community/mod/circle-sensor-card-depends/lit-html template `result` into the given `node`.
     * Implement to customize the way rendering is applied. This is should not
     * typically be needed and is provided for advanced use cases.
     * @param result {TemplateResult} `/local/community/mod/circle-sensor-card-depends/lit-html` template result to render
     * @param node {Element|DocumentFragment} node into which to render
     */
    protected _applyRender(result: TemplateResult, node: Element | DocumentFragment): void;
    /**
     * Called after element DOM has been rendered. Implement to
     * directly control rendered DOM. Typically this is not needed as `/local/community/mod/circle-sensor-card-depends/lit-html`
     * can be used in the `_render` method to set properties, attributes, and
     * event listeners. However, it is sometimes useful for calling methods on
     * rendered elements, like calling `focus()` on an element to focus it.
     * @param _props Current element properties
     * @param _changedProps Changing element properties
     * @param _prevProps Previous element properties
     */
    protected _didRender(_props: object, _changedProps: object, _prevProps: object): void;
    /**
     * Call to request the element to asynchronously re-render regardless
     * of whether or not any property changes are pending.
     */
    requestRender(): void;
    /**
     * Override which provides tracking of invalidated state.
     */
    _invalidateProperties(): void;
    /**
     * Returns a promise which resolves after the element next renders.
     * The promise resolves to `true` if the element rendered and `false` if the
     * element did not render.
     * This is useful when users (e.g. tests) need to react to the rendered state
     * of the element after a change is made.
     * This can also be useful in event handlers if it is desireable to wait
     * to send an event until after rendering. If possible implement the
     * `_didRender` method to directly respond to rendering within the
     * rendering lifecycle.
     */
    readonly renderComplete: Promise<boolean>;
}
