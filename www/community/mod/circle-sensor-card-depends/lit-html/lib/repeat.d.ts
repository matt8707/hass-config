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
import { DirectiveFn, NodePart } from '/local/community/mod/circle-sensor-card-depends/lit-html/lit-html.js';
export declare type KeyFn<T> = (item: T) => any;
export declare type ItemTemplate<T> = (item: T, index: number) => any;
export declare function repeat<T>(items: T[], keyFn: KeyFn<T>, template: ItemTemplate<T>): DirectiveFn<NodePart>;
export declare function repeat<T>(items: T[], template: ItemTemplate<T>): DirectiveFn<NodePart>;
