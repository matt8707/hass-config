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
export declare const templateCaches: Map<string, Map<TemplateStringsArray, Template>>;
/**
 * Interprets a template literal as an HTML template that can efficiently
 * render to and update a container.
 */
export declare const html: (strings: TemplateStringsArray, ...values: any[]) => TemplateResult;
/**
 * Interprets a template literal as an SVG template that can efficiently
 * render to and update a container.
 */
export declare const svg: (strings: TemplateStringsArray, ...values: any[]) => SVGTemplateResult;
/**
 * The return type of `html`, which holds a Template and the values from
 * interpolated expressions.
 */
export declare class TemplateResult {
    strings: TemplateStringsArray;
    values: any[];
    type: string;
    partCallback: PartCallback;
    constructor(strings: TemplateStringsArray, values: any[], type: string, partCallback?: PartCallback);
    /**
     * Returns a string of HTML used to create a <template> element.
     */
    getHTML(): string;
    getTemplateElement(): HTMLTemplateElement;
}
/**
 * A TemplateResult for SVG fragments.
 *
 * This class wraps HTMl in an <svg> tag in order to parse its contents in the
 * SVG namespace, then modifies the template to remove the <svg> tag so that
 * clones only container the original fragment.
 */
export declare class SVGTemplateResult extends TemplateResult {
    getHTML(): string;
    getTemplateElement(): HTMLTemplateElement;
}
/**
 * A function type that creates a Template from a TemplateResult.
 *
 * This is a hook into the template-creation process for rendering that
 * requires some modification of templates before they're used, like ShadyCSS,
 * which must add classes to elements and remove styles.
 *
 * Templates should be cached as aggressively as possible, so that many
 * TemplateResults produced from the same expression only do the work of
 * creating the Template the first time.
 *
 * Templates are usually cached by TemplateResult.strings and
 * TemplateResult.type, but may be cached by other keys if this function
 * modifies the template.
 *
 * Note that currently TemplateFactories must not add, remove, or reorder
 * expressions, because there is no way to describe such a modification
 * to render() so that values are interpolated to the correct place in the
 * template instances.
 */
export declare type TemplateFactory = (result: TemplateResult) => Template;
/**
 * The default TemplateFactory which caches Templates keyed on
 * result.type and result.strings.
 */
export declare function defaultTemplateFactory(result: TemplateResult): Template;
export declare type TemplateContainer = (Element | DocumentFragment) & {
    __templateInstance?: TemplateInstance;
};
/**
 * Renders a template to a container.
 *
 * To update a container with new values, reevaluate the template literal and
 * call `render` with the new result.
 *
 * @param result a TemplateResult created by evaluating a template tag like
 *     `html` or `svg`.
 * @param container A DOM parent to render to. The entire contents are either
 *     replaced, or efficiently updated if the same result type was previous
 *     rendered there.
 * @param templateFactory a function to create a Template or retreive one from
 *     cache.
 */
export declare function render(result: TemplateResult, container: Element | DocumentFragment, templateFactory?: TemplateFactory): void;
/**
 * A placeholder for a dynamic expression in an HTML template.
 *
 * There are two built-in part types: AttributePart and NodePart. NodeParts
 * always represent a single dynamic expression, while AttributeParts may
 * represent as many expressions are contained in the attribute.
 *
 * A Template's parts are mutable, so parts can be replaced or modified
 * (possibly to implement different template semantics). The contract is that
 * parts can only be replaced, not removed, added or reordered, and parts must
 * always consume the correct number of values in their `update()` method.
 *
 * TODO(justinfagnani): That requirement is a little fragile. A
 * TemplateInstance could instead be more careful about which values it gives
 * to Part.update().
 */
export declare class TemplatePart {
    type: string;
    index: number;
    name?: string | undefined;
    rawName?: string | undefined;
    strings?: string[] | undefined;
    constructor(type: string, index: number, name?: string | undefined, rawName?: string | undefined, strings?: string[] | undefined);
}
export declare const isTemplatePartActive: (part: TemplatePart) => boolean;
/**
 * An updateable Template that tracks the location of dynamic parts.
 */
export declare class Template {
    parts: TemplatePart[];
    element: HTMLTemplateElement;
    constructor(result: TemplateResult, element: HTMLTemplateElement);
}
/**
 * Returns a value ready to be inserted into a Part from a user-provided value.
 *
 * If the user value is a directive, this invokes the directive with the given
 * part. If the value is null, it's converted to undefined to work better
 * with certain DOM APIs, like textContent.
 */
export declare const getValue: (part: Part, value: any) => any;
export interface DirectiveFn<P = Part> {
    (part: P): void;
    __litDirective?: true;
}
export declare const directive: <P = Part>(f: DirectiveFn<P>) => DirectiveFn<P>;
/**
 * A sentinel value that signals that a value was handled by a directive and
 * should not be written to the DOM.
 */
export declare const noChange: {};
/**
 * @deprecated Use `noChange` instead.
 */
export { noChange as directiveValue };
export interface Part {
    instance: TemplateInstance;
    size?: number;
}
export interface SinglePart extends Part {
    setValue(value: any): void;
}
export interface MultiPart extends Part {
    setValue(values: any[], startIndex: number): void;
}
export declare class AttributePart implements MultiPart {
    instance: TemplateInstance;
    element: Element;
    name: string;
    strings: string[];
    size: number;
    _previousValues: any;
    constructor(instance: TemplateInstance, element: Element, name: string, strings: string[]);
    protected _interpolate(values: any[], startIndex: number): string;
    protected _equalToPreviousValues(values: any[], startIndex: number): boolean;
    setValue(values: any[], startIndex: number): void;
}
export declare class NodePart implements SinglePart {
    instance: TemplateInstance;
    startNode: Node;
    endNode: Node;
    _previousValue: any;
    constructor(instance: TemplateInstance, startNode: Node, endNode: Node);
    setValue(value: any): void;
    private _insert;
    private _setNode;
    private _setText;
    private _setTemplateResult;
    private _setIterable;
    private _setPromise;
    clear(startNode?: Node): void;
}
export declare type PartCallback = (instance: TemplateInstance, templatePart: TemplatePart, node: Node) => Part;
export declare const defaultPartCallback: (instance: TemplateInstance, templatePart: TemplatePart, node: Node) => Part;
/**
 * An instance of a `Template` that can be attached to the DOM and updated
 * with new values.
 */
export declare class TemplateInstance {
    _parts: Array<Part | undefined>;
    _partCallback: PartCallback;
    _getTemplate: TemplateFactory;
    template: Template;
    constructor(template: Template, partCallback: PartCallback, getTemplate: TemplateFactory);
    update(values: any[]): void;
    _clone(): DocumentFragment;
}
/**
 * Reparents nodes, starting from `startNode` (inclusive) to `endNode`
 * (exclusive), into another container (could be the same container), before
 * `beforeNode`. If `beforeNode` is null, it appends the nodes to the
 * container.
 */
export declare const reparentNodes: (container: Node, start: Node | null, end?: Node | null, before?: Node | null) => void;
/**
 * Removes nodes, starting from `startNode` (inclusive) to `endNode`
 * (exclusive), from `container`.
 */
export declare const removeNodes: (container: Node, startNode: Node | null, endNode?: Node | null) => void;
