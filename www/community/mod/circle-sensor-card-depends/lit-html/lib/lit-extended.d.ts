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
import { AttributePart, Part, SVGTemplateResult, TemplateInstance, TemplatePart, TemplateResult } from '/local/community/mod/circle-sensor-card-depends/lit-html/lit-html.js';
export { render } from '/local/community/mod/circle-sensor-card-depends/lit-html/lit-html.js';
/**
 * Interprets a template literal as a lit-extended HTML template.
 */
export declare const html: (strings: TemplateStringsArray, ...values: any[]) => TemplateResult;
/**
 * Interprets a template literal as a lit-extended SVG template.
 */
export declare const svg: (strings: TemplateStringsArray, ...values: any[]) => SVGTemplateResult;
/**
 * A PartCallback which allows templates to set properties and declarative
 * event handlers.
 *
 * Properties are set by default, instead of attributes. Attribute names in
 * /local/community/mod/circle-sensor-card-depends/lit-html templates preserve case, so properties are case sensitive. If an
 * expression takes up an entire attribute value, then the property is set to
 * that value. If an expression is interpolated with a string or other
 * expressions then the property is set to the string result of the
 * interpolation.
 *
 * To set an attribute instead of a property, append a `$` suffix to the
 * attribute name.
 *
 * Example:
 *
 *     html`<button class$="primary">Buy Now</button>`
 *
 * To set an event handler, prefix the attribute name with `on-`:
 *
 * Example:
 *
 *     html`<button on-click=${(e)=> this.onClickHandler(e)}>Buy Now</button>`
 *
 */
export declare const extendedPartCallback: (instance: TemplateInstance, templatePart: TemplatePart, node: Node) => Part;
/**
 * Implements a boolean attribute, roughly as defined in the HTML
 * specification.
 *
 * If the value is truthy, then the attribute is present with a value of
 * ''. If the value is falsey, the attribute is removed.
 */
export declare class BooleanAttributePart extends AttributePart {
    setValue(values: any[], startIndex: number): void;
}
export declare class PropertyPart extends AttributePart {
    setValue(values: any[], startIndex: number): void;
}
export declare class EventPart implements Part {
    instance: TemplateInstance;
    element: Element;
    eventName: string;
    private _listener;
    constructor(instance: TemplateInstance, element: Element, eventName: string);
    setValue(value: any): void;
    handleEvent(event: Event): void;
}
