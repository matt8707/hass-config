/*! *****************************************************************************
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
MERCHANTABLITY OR NON-INFRINGEMENT.

See the Apache Version 2.0 License for specific language governing permissions
and limitations under the License.
***************************************************************************** */
function t(t, e, i, n) {
  var s,
      r = arguments.length,
      a = r < 3 ? e : null === n ? n = Object.getOwnPropertyDescriptor(e, i) : n;if ("object" == typeof Reflect && "function" == typeof Reflect.decorate) a = Reflect.decorate(t, e, i, n);else for (var o = t.length - 1; o >= 0; o--) (s = t[o]) && (a = (r < 3 ? s(a) : r > 3 ? s(e, i, a) : s(e, i)) || a);return r > 3 && a && Object.defineProperty(e, i, a), a;
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
}const e = "undefined" != typeof window && null != window.customElements && void 0 !== window.customElements.polyfillWrapFlushCallback,
      i = (t, e, i = null) => {
  for (; e !== i;) {
    const i = e.nextSibling;t.removeChild(e), e = i;
  }
},
      n = `{{lit-${String(Math.random()).slice(2)}}}`,
      s = `\x3c!--${n}--\x3e`,
      r = new RegExp(`${n}|${s}`);class a {
  constructor(t, e) {
    this.parts = [], this.element = e;const i = [],
          s = [],
          a = document.createTreeWalker(e.content, 133, null, !1);let l = 0,
        u = -1,
        d = 0;const { strings: f, values: { length: p } } = t;for (; d < p;) {
      const t = a.nextNode();if (null !== t) {
        if (u++, 1 === t.nodeType) {
          if (t.hasAttributes()) {
            const e = t.attributes,
                  { length: i } = e;let n = 0;for (let t = 0; t < i; t++) o(e[t].name, "$lit$") && n++;for (; n-- > 0;) {
              const e = f[d],
                    i = h.exec(e)[2],
                    n = i.toLowerCase() + "$lit$",
                    s = t.getAttribute(n);t.removeAttribute(n);const a = s.split(r);this.parts.push({ type: "attribute", index: u, name: i, strings: a }), d += a.length - 1;
            }
          }"TEMPLATE" === t.tagName && (s.push(t), a.currentNode = t.content);
        } else if (3 === t.nodeType) {
          const e = t.data;if (e.indexOf(n) >= 0) {
            const n = t.parentNode,
                  s = e.split(r),
                  a = s.length - 1;for (let e = 0; e < a; e++) {
              let i,
                  r = s[e];if ("" === r) i = c();else {
                const t = h.exec(r);null !== t && o(t[2], "$lit$") && (r = r.slice(0, t.index) + t[1] + t[2].slice(0, -"$lit$".length) + t[3]), i = document.createTextNode(r);
              }n.insertBefore(i, t), this.parts.push({ type: "node", index: ++u });
            }"" === s[a] ? (n.insertBefore(c(), t), i.push(t)) : t.data = s[a], d += a;
          }
        } else if (8 === t.nodeType) if (t.data === n) {
          const e = t.parentNode;null !== t.previousSibling && u !== l || (u++, e.insertBefore(c(), t)), l = u, this.parts.push({ type: "node", index: u }), null === t.nextSibling ? t.data = "" : (i.push(t), u--), d++;
        } else {
          let e = -1;for (; -1 !== (e = t.data.indexOf(n, e + 1));) this.parts.push({ type: "node", index: -1 }), d++;
        }
      } else a.currentNode = s.pop();
    }for (const n of i) n.parentNode.removeChild(n);
  }
}const o = (t, e) => {
  const i = t.length - e.length;return i >= 0 && t.slice(i) === e;
},
      l = t => -1 !== t.index,
      c = () => document.createComment(""),
      h = /([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/;function u(t, e) {
  const { element: { content: i }, parts: n } = t,
        s = document.createTreeWalker(i, 133, null, !1);let r = f(n),
      a = n[r],
      o = -1,
      l = 0;const c = [];let h = null;for (; s.nextNode();) {
    o++;const t = s.currentNode;for (t.previousSibling === h && (h = null), e.has(t) && (c.push(t), null === h && (h = t)), null !== h && l++; void 0 !== a && a.index === o;) a.index = null !== h ? -1 : a.index - l, r = f(n, r), a = n[r];
  }c.forEach(t => t.parentNode.removeChild(t));
}const d = t => {
  let e = 11 === t.nodeType ? 0 : 1;const i = document.createTreeWalker(t, 133, null, !1);for (; i.nextNode();) e++;return e;
},
      f = (t, e = -1) => {
  for (let i = e + 1; i < t.length; i++) {
    const e = t[i];if (l(e)) return i;
  }return -1;
};
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
const p = new WeakMap(),
      m = t => (...e) => {
  const i = t(...e);return p.set(i, !0), i;
},
      g = t => "function" == typeof t && p.has(t),
      _ = {},
      b = {};
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
class y {
  constructor(t, e, i) {
    this.__parts = [], this.template = t, this.processor = e, this.options = i;
  }update(t) {
    let e = 0;for (const i of this.__parts) void 0 !== i && i.setValue(t[e]), e++;for (const i of this.__parts) void 0 !== i && i.commit();
  }_clone() {
    const t = e ? this.template.element.content.cloneNode(!0) : document.importNode(this.template.element.content, !0),
          i = [],
          n = this.template.parts,
          s = document.createTreeWalker(t, 133, null, !1);let r,
        a = 0,
        o = 0,
        c = s.nextNode();for (; a < n.length;) if (r = n[a], l(r)) {
      for (; o < r.index;) o++, "TEMPLATE" === c.nodeName && (i.push(c), s.currentNode = c.content), null === (c = s.nextNode()) && (s.currentNode = i.pop(), c = s.nextNode());if ("node" === r.type) {
        const t = this.processor.handleTextExpression(this.options);t.insertAfterNode(c.previousSibling), this.__parts.push(t);
      } else this.__parts.push(...this.processor.handleAttributeExpressions(c, r.name, r.strings, this.options));a++;
    } else this.__parts.push(void 0), a++;return e && (document.adoptNode(t), customElements.upgrade(t)), t;
  }
}
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
 */const v = ` ${n} `;class w {
  constructor(t, e, i, n) {
    this.strings = t, this.values = e, this.type = i, this.processor = n;
  }getHTML() {
    const t = this.strings.length - 1;let e = "",
        i = !1;for (let r = 0; r < t; r++) {
      const t = this.strings[r],
            a = t.lastIndexOf("\x3c!--");i = (a > -1 || i) && -1 === t.indexOf("--\x3e", a + 1);const o = h.exec(t);e += null === o ? t + (i ? v : s) : t.substr(0, o.index) + o[1] + o[2] + "$lit$" + o[3] + n;
    }return e += this.strings[t], e;
  }getTemplateElement() {
    const t = document.createElement("template");return t.innerHTML = this.getHTML(), t;
  }
}
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
 */const S = t => null === t || !("object" == typeof t || "function" == typeof t),
      x = t => Array.isArray(t) || !(!t || !t[Symbol.iterator]);class k {
  constructor(t, e, i) {
    this.dirty = !0, this.element = t, this.name = e, this.strings = i, this.parts = [];for (let n = 0; n < i.length - 1; n++) this.parts[n] = this._createPart();
  }_createPart() {
    return new T(this);
  }_getValue() {
    const t = this.strings,
          e = t.length - 1;let i = "";for (let n = 0; n < e; n++) {
      i += t[n];const e = this.parts[n];if (void 0 !== e) {
        const t = e.value;if (S(t) || !x(t)) i += "string" == typeof t ? t : String(t);else for (const e of t) i += "string" == typeof e ? e : String(e);
      }
    }return i += t[e], i;
  }commit() {
    this.dirty && (this.dirty = !1, this.element.setAttribute(this.name, this._getValue()));
  }
}class T {
  constructor(t) {
    this.value = void 0, this.committer = t;
  }setValue(t) {
    t === _ || S(t) && t === this.value || (this.value = t, g(t) || (this.committer.dirty = !0));
  }commit() {
    for (; g(this.value);) {
      const t = this.value;this.value = _, t(this);
    }this.value !== _ && this.committer.commit();
  }
}class M {
  constructor(t) {
    this.value = void 0, this.__pendingValue = void 0, this.options = t;
  }appendInto(t) {
    this.startNode = t.appendChild(c()), this.endNode = t.appendChild(c());
  }insertAfterNode(t) {
    this.startNode = t, this.endNode = t.nextSibling;
  }appendIntoPart(t) {
    t.__insert(this.startNode = c()), t.__insert(this.endNode = c());
  }insertAfterPart(t) {
    t.__insert(this.startNode = c()), this.endNode = t.endNode, t.endNode = this.startNode;
  }setValue(t) {
    this.__pendingValue = t;
  }commit() {
    if (null === this.startNode.parentNode) return;for (; g(this.__pendingValue);) {
      const t = this.__pendingValue;this.__pendingValue = _, t(this);
    }const t = this.__pendingValue;t !== _ && (S(t) ? t !== this.value && this.__commitText(t) : t instanceof w ? this.__commitTemplateResult(t) : t instanceof Node ? this.__commitNode(t) : x(t) ? this.__commitIterable(t) : t === b ? (this.value = b, this.clear()) : this.__commitText(t));
  }__insert(t) {
    this.endNode.parentNode.insertBefore(t, this.endNode);
  }__commitNode(t) {
    this.value !== t && (this.clear(), this.__insert(t), this.value = t);
  }__commitText(t) {
    const e = this.startNode.nextSibling,
          i = "string" == typeof (t = null == t ? "" : t) ? t : String(t);e === this.endNode.previousSibling && 3 === e.nodeType ? e.data = i : this.__commitNode(document.createTextNode(i)), this.value = t;
  }__commitTemplateResult(t) {
    const e = this.options.templateFactory(t);if (this.value instanceof y && this.value.template === e) this.value.update(t.values);else {
      const i = new y(e, t.processor, this.options),
            n = i._clone();i.update(t.values), this.__commitNode(n), this.value = i;
    }
  }__commitIterable(t) {
    Array.isArray(this.value) || (this.value = [], this.clear());const e = this.value;let i,
        n = 0;for (const s of t) i = e[n], void 0 === i && (i = new M(this.options), e.push(i), 0 === n ? i.appendIntoPart(this) : i.insertAfterPart(e[n - 1])), i.setValue(s), i.commit(), n++;n < e.length && (e.length = n, this.clear(i && i.endNode));
  }clear(t = this.startNode) {
    i(this.startNode.parentNode, t.nextSibling, this.endNode);
  }
}class N {
  constructor(t, e, i) {
    if (this.value = void 0, this.__pendingValue = void 0, 2 !== i.length || "" !== i[0] || "" !== i[1]) throw new Error("Boolean attributes can only contain a single expression");this.element = t, this.name = e, this.strings = i;
  }setValue(t) {
    this.__pendingValue = t;
  }commit() {
    for (; g(this.__pendingValue);) {
      const t = this.__pendingValue;this.__pendingValue = _, t(this);
    }if (this.__pendingValue === _) return;const t = !!this.__pendingValue;this.value !== t && (t ? this.element.setAttribute(this.name, "") : this.element.removeAttribute(this.name), this.value = t), this.__pendingValue = _;
  }
}class O extends k {
  constructor(t, e, i) {
    super(t, e, i), this.single = 2 === i.length && "" === i[0] && "" === i[1];
  }_createPart() {
    return new C(this);
  }_getValue() {
    return this.single ? this.parts[0].value : super._getValue();
  }commit() {
    this.dirty && (this.dirty = !1, this.element[this.name] = this._getValue());
  }
}class C extends T {}let E = !1;(() => {
  try {
    const t = { get capture() {
        return E = !0, !1;
      } };window.addEventListener("test", t, t), window.removeEventListener("test", t, t);
  } catch (t) {}
})();class A {
  constructor(t, e, i) {
    this.value = void 0, this.__pendingValue = void 0, this.element = t, this.eventName = e, this.eventContext = i, this.__boundHandleEvent = t => this.handleEvent(t);
  }setValue(t) {
    this.__pendingValue = t;
  }commit() {
    for (; g(this.__pendingValue);) {
      const t = this.__pendingValue;this.__pendingValue = _, t(this);
    }if (this.__pendingValue === _) return;const t = this.__pendingValue,
          e = this.value,
          i = null == t || null != e && (t.capture !== e.capture || t.once !== e.once || t.passive !== e.passive),
          n = null != t && (null == e || i);i && this.element.removeEventListener(this.eventName, this.__boundHandleEvent, this.__options), n && (this.__options = P(t), this.element.addEventListener(this.eventName, this.__boundHandleEvent, this.__options)), this.value = t, this.__pendingValue = _;
  }handleEvent(t) {
    "function" == typeof this.value ? this.value.call(this.eventContext || this.element, t) : this.value.handleEvent(t);
  }
}const P = t => t && (E ? { capture: t.capture, passive: t.passive, once: t.once } : t.capture)
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
 */;function $(t) {
  let e = j.get(t.type);void 0 === e && (e = { stringsArray: new WeakMap(), keyString: new Map() }, j.set(t.type, e));let i = e.stringsArray.get(t.strings);if (void 0 !== i) return i;const s = t.strings.join(n);return i = e.keyString.get(s), void 0 === i && (i = new a(t, t.getTemplateElement()), e.keyString.set(s, i)), e.stringsArray.set(t.strings, i), i;
}const j = new Map(),
      V = new WeakMap();
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
 */const H = new
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
class {
  handleAttributeExpressions(t, e, i, n) {
    const s = e[0];if ("." === s) {
      return new O(t, e.slice(1), i).parts;
    }return "@" === s ? [new A(t, e.slice(1), n.eventContext)] : "?" === s ? [new N(t, e.slice(1), i)] : new k(t, e, i).parts;
  }handleTextExpression(t) {
    return new M(t);
  }
}();
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
 */"undefined" != typeof window && (window.litHtmlVersions || (window.litHtmlVersions = [])).push("1.2.1");const R = (t, ...e) => new w(t, e, "html", H)
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
 */,
      D = (t, e) => `${t}--${e}`;let L = !0;void 0 === window.ShadyCSS ? L = !1 : void 0 === window.ShadyCSS.prepareTemplateDom && (console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."), L = !1);const F = t => e => {
  const i = D(e.type, t);let s = j.get(i);void 0 === s && (s = { stringsArray: new WeakMap(), keyString: new Map() }, j.set(i, s));let r = s.stringsArray.get(e.strings);if (void 0 !== r) return r;const o = e.strings.join(n);if (r = s.keyString.get(o), void 0 === r) {
    const i = e.getTemplateElement();L && window.ShadyCSS.prepareTemplateDom(i, t), r = new a(e, i), s.keyString.set(o, r);
  }return s.stringsArray.set(e.strings, r), r;
},
      I = ["html", "svg"],
      U = new Set(),
      q = (t, e, i) => {
  U.add(t);const n = i ? i.element : document.createElement("template"),
        s = e.querySelectorAll("style"),
        { length: r } = s;if (0 === r) return void window.ShadyCSS.prepareTemplateStyles(n, t);const a = document.createElement("style");for (let c = 0; c < r; c++) {
    const t = s[c];t.parentNode.removeChild(t), a.textContent += t.textContent;
  }(t => {
    I.forEach(e => {
      const i = j.get(D(e, t));void 0 !== i && i.keyString.forEach(t => {
        const { element: { content: e } } = t,
              i = new Set();Array.from(e.querySelectorAll("style")).forEach(t => {
          i.add(t);
        }), u(t, i);
      });
    });
  })(t);const o = n.content;i ? function (t, e, i = null) {
    const { element: { content: n }, parts: s } = t;if (null == i) return void n.appendChild(e);const r = document.createTreeWalker(n, 133, null, !1);let a = f(s),
        o = 0,
        l = -1;for (; r.nextNode();) {
      for (l++, r.currentNode === i && (o = d(e), i.parentNode.insertBefore(e, i)); -1 !== a && s[a].index === l;) {
        if (o > 0) {
          for (; -1 !== a;) s[a].index += o, a = f(s, a);return;
        }a = f(s, a);
      }
    }
  }(i, a, o.firstChild) : o.insertBefore(a, o.firstChild), window.ShadyCSS.prepareTemplateStyles(n, t);const l = o.querySelector("style");if (window.ShadyCSS.nativeShadow && null !== l) e.insertBefore(l.cloneNode(!0), e.firstChild);else if (i) {
    o.insertBefore(a, o.firstChild);const t = new Set();t.add(a), u(i, t);
  }
};window.JSCompiler_renameProperty = (t, e) => t;const z = { toAttribute(t, e) {
    switch (e) {case Boolean:
        return t ? "" : null;case Object:case Array:
        return null == t ? t : JSON.stringify(t);}return t;
  }, fromAttribute(t, e) {
    switch (e) {case Boolean:
        return null !== t;case Number:
        return null === t ? null : Number(t);case Object:case Array:
        return JSON.parse(t);}return t;
  } },
      Y = (t, e) => e !== t && (e == e || t == t),
      B = { attribute: !0, type: String, converter: z, reflect: !1, hasChanged: Y };class W extends HTMLElement {
  constructor() {
    super(), this._updateState = 0, this._instanceProperties = void 0, this._updatePromise = new Promise(t => this._enableUpdatingResolver = t), this._changedProperties = new Map(), this._reflectingProperties = void 0, this.initialize();
  }static get observedAttributes() {
    this.finalize();const t = [];return this._classProperties.forEach((e, i) => {
      const n = this._attributeNameForProperty(i, e);void 0 !== n && (this._attributeToPropertyMap.set(n, i), t.push(n));
    }), t;
  }static _ensureClassProperties() {
    if (!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties", this))) {
      this._classProperties = new Map();const t = Object.getPrototypeOf(this)._classProperties;void 0 !== t && t.forEach((t, e) => this._classProperties.set(e, t));
    }
  }static createProperty(t, e = B) {
    if (this._ensureClassProperties(), this._classProperties.set(t, e), e.noAccessor || this.prototype.hasOwnProperty(t)) return;const i = "symbol" == typeof t ? Symbol() : `__${t}`,
          n = this.getPropertyDescriptor(t, i, e);void 0 !== n && Object.defineProperty(this.prototype, t, n);
  }static getPropertyDescriptor(t, e, i) {
    return { get() {
        return this[e];
      }, set(i) {
        const n = this[t];this[e] = i, this._requestUpdate(t, n);
      }, configurable: !0, enumerable: !0 };
  }static getPropertyOptions(t) {
    return this._classProperties && this._classProperties.get(t) || B;
  }static finalize() {
    const t = Object.getPrototypeOf(this);if (t.hasOwnProperty("finalized") || t.finalize(), this.finalized = !0, this._ensureClassProperties(), this._attributeToPropertyMap = new Map(), this.hasOwnProperty(JSCompiler_renameProperty("properties", this))) {
      const t = this.properties,
            e = [...Object.getOwnPropertyNames(t), ...("function" == typeof Object.getOwnPropertySymbols ? Object.getOwnPropertySymbols(t) : [])];for (const i of e) this.createProperty(i, t[i]);
    }
  }static _attributeNameForProperty(t, e) {
    const i = e.attribute;return !1 === i ? void 0 : "string" == typeof i ? i : "string" == typeof t ? t.toLowerCase() : void 0;
  }static _valueHasChanged(t, e, i = Y) {
    return i(t, e);
  }static _propertyValueFromAttribute(t, e) {
    const i = e.type,
          n = e.converter || z,
          s = "function" == typeof n ? n : n.fromAttribute;return s ? s(t, i) : t;
  }static _propertyValueToAttribute(t, e) {
    if (void 0 === e.reflect) return;const i = e.type,
          n = e.converter;return (n && n.toAttribute || z.toAttribute)(t, i);
  }initialize() {
    this._saveInstanceProperties(), this._requestUpdate();
  }_saveInstanceProperties() {
    this.constructor._classProperties.forEach((t, e) => {
      if (this.hasOwnProperty(e)) {
        const t = this[e];delete this[e], this._instanceProperties || (this._instanceProperties = new Map()), this._instanceProperties.set(e, t);
      }
    });
  }_applyInstanceProperties() {
    this._instanceProperties.forEach((t, e) => this[e] = t), this._instanceProperties = void 0;
  }connectedCallback() {
    this.enableUpdating();
  }enableUpdating() {
    void 0 !== this._enableUpdatingResolver && (this._enableUpdatingResolver(), this._enableUpdatingResolver = void 0);
  }disconnectedCallback() {}attributeChangedCallback(t, e, i) {
    e !== i && this._attributeToProperty(t, i);
  }_propertyToAttribute(t, e, i = B) {
    const n = this.constructor,
          s = n._attributeNameForProperty(t, i);if (void 0 !== s) {
      const t = n._propertyValueToAttribute(e, i);if (void 0 === t) return;this._updateState = 8 | this._updateState, null == t ? this.removeAttribute(s) : this.setAttribute(s, t), this._updateState = -9 & this._updateState;
    }
  }_attributeToProperty(t, e) {
    if (8 & this._updateState) return;const i = this.constructor,
          n = i._attributeToPropertyMap.get(t);if (void 0 !== n) {
      const t = i.getPropertyOptions(n);this._updateState = 16 | this._updateState, this[n] = i._propertyValueFromAttribute(e, t), this._updateState = -17 & this._updateState;
    }
  }_requestUpdate(t, e) {
    let i = !0;if (void 0 !== t) {
      const n = this.constructor,
            s = n.getPropertyOptions(t);n._valueHasChanged(this[t], e, s.hasChanged) ? (this._changedProperties.has(t) || this._changedProperties.set(t, e), !0 !== s.reflect || 16 & this._updateState || (void 0 === this._reflectingProperties && (this._reflectingProperties = new Map()), this._reflectingProperties.set(t, s))) : i = !1;
    }!this._hasRequestedUpdate && i && (this._updatePromise = this._enqueueUpdate());
  }requestUpdate(t, e) {
    return this._requestUpdate(t, e), this.updateComplete;
  }async _enqueueUpdate() {
    this._updateState = 4 | this._updateState;try {
      await this._updatePromise;
    } catch (e) {}const t = this.performUpdate();return null != t && (await t), !this._hasRequestedUpdate;
  }get _hasRequestedUpdate() {
    return 4 & this._updateState;
  }get hasUpdated() {
    return 1 & this._updateState;
  }performUpdate() {
    this._instanceProperties && this._applyInstanceProperties();let t = !1;const e = this._changedProperties;try {
      t = this.shouldUpdate(e), t ? this.update(e) : this._markUpdated();
    } catch (i) {
      throw t = !1, this._markUpdated(), i;
    }t && (1 & this._updateState || (this._updateState = 1 | this._updateState, this.firstUpdated(e)), this.updated(e));
  }_markUpdated() {
    this._changedProperties = new Map(), this._updateState = -5 & this._updateState;
  }get updateComplete() {
    return this._getUpdateComplete();
  }_getUpdateComplete() {
    return this._updatePromise;
  }shouldUpdate(t) {
    return !0;
  }update(t) {
    void 0 !== this._reflectingProperties && this._reflectingProperties.size > 0 && (this._reflectingProperties.forEach((t, e) => this._propertyToAttribute(e, this[e], t)), this._reflectingProperties = void 0), this._markUpdated();
  }updated(t) {}firstUpdated(t) {}
}W.finalized = !0;
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
const J = (t, e) => "method" === e.kind && e.descriptor && !("value" in e.descriptor) ? Object.assign(Object.assign({}, e), { finisher(i) {
    i.createProperty(e.key, t);
  } }) : { kind: "field", key: Symbol(), placement: "own", descriptor: {}, initializer() {
    "function" == typeof e.initializer && (this[e.key] = e.initializer.call(this));
  }, finisher(i) {
    i.createProperty(e.key, t);
  } };function G(t) {
  return (e, i) => void 0 !== i ? ((t, e, i) => {
    e.constructor.createProperty(i, t);
  })(t, e, i) : J(t, e);
}
/**
@license
Copyright (c) 2019 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const Z = "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype,
      X = Symbol();class K {
  constructor(t, e) {
    if (e !== X) throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText = t;
  }get styleSheet() {
    return void 0 === this._styleSheet && (Z ? (this._styleSheet = new CSSStyleSheet(), this._styleSheet.replaceSync(this.cssText)) : this._styleSheet = null), this._styleSheet;
  }toString() {
    return this.cssText;
  }
}
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
(window.litElementVersions || (window.litElementVersions = [])).push("2.3.1");const Q = {};class tt extends W {
  static getStyles() {
    return this.styles;
  }static _getUniqueStyles() {
    if (this.hasOwnProperty(JSCompiler_renameProperty("_styles", this))) return;const t = this.getStyles();if (void 0 === t) this._styles = [];else if (Array.isArray(t)) {
      const e = (t, i) => t.reduceRight((t, i) => Array.isArray(i) ? e(i, t) : (t.add(i), t), i),
            i = e(t, new Set()),
            n = [];i.forEach(t => n.unshift(t)), this._styles = n;
    } else this._styles = [t];
  }initialize() {
    super.initialize(), this.constructor._getUniqueStyles(), this.renderRoot = this.createRenderRoot(), window.ShadowRoot && this.renderRoot instanceof window.ShadowRoot && this.adoptStyles();
  }createRenderRoot() {
    return this.attachShadow({ mode: "open" });
  }adoptStyles() {
    const t = this.constructor._styles;0 !== t.length && (void 0 === window.ShadyCSS || window.ShadyCSS.nativeShadow ? Z ? this.renderRoot.adoptedStyleSheets = t.map(t => t.styleSheet) : this._needsShimAdoptedStyleSheets = !0 : window.ShadyCSS.ScopingShim.prepareAdoptedCssText(t.map(t => t.cssText), this.localName));
  }connectedCallback() {
    super.connectedCallback(), this.hasUpdated && void 0 !== window.ShadyCSS && window.ShadyCSS.styleElement(this);
  }update(t) {
    const e = this.render();super.update(t), e !== Q && this.constructor.render(e, this.renderRoot, { scopeName: this.localName, eventContext: this }), this._needsShimAdoptedStyleSheets && (this._needsShimAdoptedStyleSheets = !1, this.constructor._styles.forEach(t => {
      const e = document.createElement("style");e.textContent = t.cssText, this.renderRoot.appendChild(e);
    }));
  }render() {
    return Q;
  }
}tt.finalized = !0, tt.render = (t, e, n) => {
  if (!n || "object" != typeof n || !n.scopeName) throw new Error("The `scopeName` option is required.");const s = n.scopeName,
        r = V.has(e),
        a = L && 11 === e.nodeType && !!e.host,
        o = a && !U.has(s),
        l = o ? document.createDocumentFragment() : e;if (((t, e, n) => {
    let s = V.get(e);void 0 === s && (i(e, e.firstChild), V.set(e, s = new M(Object.assign({ templateFactory: $ }, n))), s.appendInto(e)), s.setValue(t), s.commit();
  })(t, l, Object.assign({ templateFactory: F(s) }, n)), o) {
    const t = V.get(l);V.delete(l);const n = t.value instanceof y ? t.value.template : void 0;q(s, l, n), i(e, e.firstChild), e.appendChild(l), V.set(e, t);
  }!r && a && window.ShadyCSS.styleElement(e.host);
};
/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
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
const et = new WeakMap(),
      it = m(t => e => {
  if (!(e instanceof T) || e instanceof C || "style" !== e.committer.name || e.committer.parts.length > 1) throw new Error("The `styleMap` directive must be used in the style attribute and must be the only part in the attribute.");const { committer: i } = e,
        { style: n } = i.element;let s = et.get(e);void 0 === s && (n.cssText = i.strings.join(" "), et.set(e, s = new Set())), s.forEach(e => {
    e in t || (s.delete(e), -1 === e.indexOf("-") ? n[e] = null : n.removeProperty(e));
  });for (const r in t) s.add(r), -1 === r.indexOf("-") ? n[r] = t[r] : n.setProperty(r, t[r]);
}),
      nt = new WeakMap(),
      st = m(t => e => {
  if (!(e instanceof M)) throw new Error("unsafeHTML can only be used in text bindings");const i = nt.get(e);if (void 0 !== i && S(t) && t === i.value && e.value === i.fragment) return;const n = document.createElement("template");n.innerHTML = t;const s = document.importNode(n.content, !0);e.setValue(s), nt.set(e, { value: t, fragment: s });
});
/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
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
class rt {
  constructor(t) {
    this.classes = new Set(), this.changed = !1, this.element = t;const e = (t.getAttribute("class") || "").split(/\s+/);for (const i of e) this.classes.add(i);
  }add(t) {
    this.classes.add(t), this.changed = !0;
  }remove(t) {
    this.classes.delete(t), this.changed = !0;
  }commit() {
    if (this.changed) {
      let t = "";this.classes.forEach(e => t += e + " "), this.element.setAttribute("class", t);
    }
  }
}const at = new WeakMap(),
      ot = m(t => e => {
  if (!(e instanceof T) || e instanceof C || "class" !== e.committer.name || e.committer.parts.length > 1) throw new Error("The `classMap` directive must be used in the `class` attribute and must be the only part in the attribute.");const { committer: i } = e,
        { element: n } = i;let s = at.get(e);void 0 === s && (n.setAttribute("class", i.strings.join(" ")), at.set(e, s = new Set()));const r = n.classList || new rt(n);s.forEach(e => {
    e in t || (r.remove(e), s.delete(e));
  });for (const a in t) {
    const e = t[a];e != s.has(a) && (e ? (r.add(a), s.add(a)) : (r.remove(a), s.delete(a)));
  }"function" == typeof r.commit && r.commit();
});var lt = /d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,
    ct = "[^\\s]+",
    ht = /\[([^]*?)\]/gm;function ut(t, e) {
  for (var i = [], n = 0, s = t.length; n < s; n++) i.push(t[n].substr(0, e));return i;
}var dt = function (t) {
  return function (e, i) {
    var n = i[t].map(function (t) {
      return t.toLowerCase();
    }).indexOf(e.toLowerCase());return n > -1 ? n : null;
  };
};function ft(t) {
  for (var e = [], i = 1; i < arguments.length; i++) e[i - 1] = arguments[i];for (var n = 0, s = e; n < s.length; n++) {
    var r = s[n];for (var a in r) t[a] = r[a];
  }return t;
}var pt = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    mt = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    gt = ut(mt, 3),
    _t = { dayNamesShort: ut(pt, 3), dayNames: pt, monthNamesShort: gt, monthNames: mt, amPm: ["am", "pm"], DoFn: function (t) {
    return t + ["th", "st", "nd", "rd"][t % 10 > 3 ? 0 : (t - t % 10 != 10 ? 1 : 0) * t % 10];
  } },
    bt = ft({}, _t),
    yt = function (t, e) {
  for (void 0 === e && (e = 2), t = String(t); t.length < e;) t = "0" + t;return t;
},
    vt = { D: function (t) {
    return String(t.getDate());
  }, DD: function (t) {
    return yt(t.getDate());
  }, Do: function (t, e) {
    return e.DoFn(t.getDate());
  }, d: function (t) {
    return String(t.getDay());
  }, dd: function (t) {
    return yt(t.getDay());
  }, ddd: function (t, e) {
    return e.dayNamesShort[t.getDay()];
  }, dddd: function (t, e) {
    return e.dayNames[t.getDay()];
  }, M: function (t) {
    return String(t.getMonth() + 1);
  }, MM: function (t) {
    return yt(t.getMonth() + 1);
  }, MMM: function (t, e) {
    return e.monthNamesShort[t.getMonth()];
  }, MMMM: function (t, e) {
    return e.monthNames[t.getMonth()];
  }, YY: function (t) {
    return yt(String(t.getFullYear()), 4).substr(2);
  }, YYYY: function (t) {
    return yt(t.getFullYear(), 4);
  }, h: function (t) {
    return String(t.getHours() % 12 || 12);
  }, hh: function (t) {
    return yt(t.getHours() % 12 || 12);
  }, H: function (t) {
    return String(t.getHours());
  }, HH: function (t) {
    return yt(t.getHours());
  }, m: function (t) {
    return String(t.getMinutes());
  }, mm: function (t) {
    return yt(t.getMinutes());
  }, s: function (t) {
    return String(t.getSeconds());
  }, ss: function (t) {
    return yt(t.getSeconds());
  }, S: function (t) {
    return String(Math.round(t.getMilliseconds() / 100));
  }, SS: function (t) {
    return yt(Math.round(t.getMilliseconds() / 10), 2);
  }, SSS: function (t) {
    return yt(t.getMilliseconds(), 3);
  }, a: function (t, e) {
    return t.getHours() < 12 ? e.amPm[0] : e.amPm[1];
  }, A: function (t, e) {
    return t.getHours() < 12 ? e.amPm[0].toUpperCase() : e.amPm[1].toUpperCase();
  }, ZZ: function (t) {
    var e = t.getTimezoneOffset();return (e > 0 ? "-" : "+") + yt(100 * Math.floor(Math.abs(e) / 60) + Math.abs(e) % 60, 4);
  }, Z: function (t) {
    var e = t.getTimezoneOffset();return (e > 0 ? "-" : "+") + yt(Math.floor(Math.abs(e) / 60), 2) + ":" + yt(Math.abs(e) % 60, 2);
  } },
    wt = function (t) {
  return +t - 1;
},
    St = [null, "[1-9]\\d?"],
    xt = [null, ct],
    kt = ["isPm", ct, function (t, e) {
  var i = t.toLowerCase();return i === e.amPm[0] ? 0 : i === e.amPm[1] ? 1 : null;
}],
    Tt = ["timezoneOffset", "[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?", function (t) {
  var e = (t + "").match(/([+-]|\d\d)/gi);if (e) {
    var i = 60 * +e[1] + parseInt(e[2], 10);return "+" === e[0] ? i : -i;
  }return 0;
}],
    Mt = (dt("monthNamesShort"), dt("monthNames"), { default: "ddd MMM DD YYYY HH:mm:ss", shortDate: "M/D/YY", mediumDate: "MMM D, YYYY", longDate: "MMMM D, YYYY", fullDate: "dddd, MMMM D, YYYY", isoDate: "YYYY-MM-DD", isoDateTime: "YYYY-MM-DDTHH:mm:ssZ", shortTime: "HH:mm", mediumTime: "HH:mm:ss", longTime: "HH:mm:ss.SSS" });var Nt = function (t, e, i) {
  if (void 0 === e && (e = Mt.default), void 0 === i && (i = {}), "number" == typeof t && (t = new Date(t)), "[object Date]" !== Object.prototype.toString.call(t) || isNaN(t.getTime())) throw new Error("Invalid Date pass to format");var n = [];e = (e = Mt[e] || e).replace(ht, function (t, e) {
    return n.push(e), "@@@";
  });var s = ft(ft({}, bt), i);return (e = e.replace(lt, function (e) {
    return vt[e](t, s);
  })).replace(/@@@/g, function () {
    return n.shift();
  });
};function Ot(t) {
  var e = t.split(":").map(Number);return 3600 * e[0] + 60 * e[1] + e[2];
}var Ct = function () {
  try {
    new Date().toLocaleDateString("i");
  } catch (t) {
    return "RangeError" === t.name;
  }return !1;
}() ? function (t, e) {
  return t.toLocaleDateString(e, { year: "numeric", month: "long", day: "numeric" });
} : function (t) {
  return Nt(t, "mediumDate");
},
    Et = function () {
  try {
    new Date().toLocaleString("i");
  } catch (t) {
    return "RangeError" === t.name;
  }return !1;
}() ? function (t, e) {
  return t.toLocaleString(e, { year: "numeric", month: "long", day: "numeric", hour: "numeric", minute: "2-digit" });
} : function (t) {
  return Nt(t, "haDateTime");
},
    At = function () {
  try {
    new Date().toLocaleTimeString("i");
  } catch (t) {
    return "RangeError" === t.name;
  }return !1;
}() ? function (t, e) {
  return t.toLocaleTimeString(e, { hour: "numeric", minute: "2-digit" });
} : function (t) {
  return Nt(t, "shortTime");
},
    Pt = function (t) {
  return t < 10 ? "0" + t : t;
};function $t(t) {
  return t.substr(0, t.indexOf("."));
}var jt = "hass:bookmark",
    Vt = ["closed", "locked", "off"],
    Ht = new Set(["fan", "input_boolean", "light", "switch", "group", "automation"]),
    Rt = function (t, e, i, n) {
  n = n || {}, i = null == i ? {} : i;var s = new Event(e, { bubbles: void 0 === n.bubbles || n.bubbles, cancelable: Boolean(n.cancelable), composed: void 0 === n.composed || n.composed });return s.detail = i, t.dispatchEvent(s), s;
},
    Dt = new Set(["call-service", "divider", "section", "weblink", "cast", "select"]),
    Lt = { alert: "toggle", automation: "toggle", climate: "climate", cover: "cover", fan: "toggle", group: "group", input_boolean: "toggle", input_number: "input-number", input_select: "input-select", input_text: "input-text", light: "toggle", lock: "lock", media_player: "media-player", remote: "toggle", scene: "scene", script: "script", sensor: "sensor", timer: "timer", switch: "toggle", vacuum: "toggle", water_heater: "climate", input_datetime: "input-datetime" },
    Ft = { alert: "hass:alert", automation: "hass:playlist-play", calendar: "hass:calendar", camera: "hass:video", climate: "hass:thermostat", configurator: "hass:settings", conversation: "hass:text-to-speech", device_tracker: "hass:account", fan: "hass:fan", group: "hass:google-circles-communities", history_graph: "hass:chart-line", homeassistant: "hass:home-assistant", homekit: "hass:home-automation", image_processing: "hass:image-filter-frames", input_boolean: "hass:drawing", input_datetime: "hass:calendar-clock", input_number: "hass:ray-vertex", input_select: "hass:format-list-bulleted", input_text: "hass:textbox", light: "hass:lightbulb", mailbox: "hass:mailbox", notify: "hass:comment-alert", person: "hass:account", plant: "hass:flower", proximity: "hass:apple-safari", remote: "hass:remote", scene: "hass:google-pages", script: "hass:file-document", sensor: "hass:eye", simple_alarm: "hass:bell", sun: "hass:white-balance-sunny", switch: "hass:flash", timer: "hass:timer", updater: "hass:cloud-upload", vacuum: "hass:robot-vacuum", water_heater: "hass:thermometer", weblink: "hass:open-in-new" };function It(t, e) {
  if (t in Ft) return Ft[t];switch (t) {case "alarm_control_panel":
      switch (e) {case "armed_home":
          return "hass:bell-plus";case "armed_night":
          return "hass:bell-sleep";case "disarmed":
          return "hass:bell-outline";case "triggered":
          return "hass:bell-ring";default:
          return "hass:bell";}case "binary_sensor":
      return e && "off" === e ? "hass:radiobox-blank" : "hass:checkbox-marked-circle";case "cover":
      return "closed" === e ? "hass:window-closed" : "hass:window-open";case "lock":
      return e && "unlocked" === e ? "hass:lock-open" : "hass:lock";case "media_player":
      return e && "off" !== e && "idle" !== e ? "hass:cast-connected" : "hass:cast";case "zwave":
      switch (e) {case "dead":
          return "hass:emoticon-dead";case "sleeping":
          return "hass:sleep";case "initializing":
          return "hass:timer-sand";default:
          return "hass:z-wave";}default:
      return console.warn("Unable to find icon for domain " + t + " (" + e + ")"), jt;}
}var Ut = function (t) {
  Rt(window, "haptic", t);
},
    qt = function (t, e) {
  return function (t, e, i) {
    void 0 === i && (i = !0);var n,
        s = $t(e),
        r = "group" === s ? "homeassistant" : s;switch (s) {case "lock":
        n = i ? "unlock" : "lock";break;case "cover":
        n = i ? "open_cover" : "close_cover";break;default:
        n = i ? "turn_on" : "turn_off";}return t.callService(r, n, { entity_id: e });
  }(t, e, Vt.includes(t.states[e].state));
},
    zt = function (t, e, i, n, s) {
  var r;if (s && i.double_tap_action ? r = i.double_tap_action : n && i.hold_action ? r = i.hold_action : !n && i.tap_action && (r = i.tap_action), r || (r = { action: "more-info" }), !r.confirmation || r.confirmation.exemptions && r.confirmation.exemptions.some(function (t) {
    return t.user === e.user.id;
  }) || confirm(r.confirmation.text || "Are you sure you want to " + r.action + "?")) switch (r.action) {case "more-info":
      (r.entity || i.entity || i.camera_image) && (Rt(t, "hass-more-info", { entityId: r.entity ? r.entity : i.entity ? i.entity : i.camera_image }), r.haptic && Ut(r.haptic));break;case "navigate":
      r.navigation_path && (function (t, e, i) {
        void 0 === i && (i = !1), i ? history.replaceState(null, "", e) : history.pushState(null, "", e), Rt(window, "location-changed", { replace: i });
      }(0, r.navigation_path), r.haptic && Ut(r.haptic));break;case "url":
      r.url_path && window.open(r.url_path), r.haptic && Ut(r.haptic);break;case "toggle":
      i.entity && (qt(e, i.entity), r.haptic && Ut(r.haptic));break;case "call-service":
      if (!r.service) return;var a = r.service.split(".", 2),
          o = a[0],
          l = a[1],
          c = Object.assign({}, r.service_data);"entity" === c.entity_id && (c.entity_id = i.entity), e.callService(o, l, c), r.haptic && Ut(r.haptic);}
},
    Yt = { humidity: "hass:water-percent", illuminance: "hass:brightness-5", temperature: "hass:thermometer", pressure: "hass:gauge", power: "hass:flash", signal_strength: "hass:wifi" },
    Bt = { binary_sensor: function (t) {
    var e = t.state && "off" === t.state;switch (t.attributes.device_class) {case "battery":
        return e ? "hass:battery" : "hass:battery-outline";case "cold":
        return e ? "hass:thermometer" : "hass:snowflake";case "connectivity":
        return e ? "hass:server-network-off" : "hass:server-network";case "door":
        return e ? "hass:door-closed" : "hass:door-open";case "garage_door":
        return e ? "hass:garage" : "hass:garage-open";case "gas":case "power":case "problem":case "safety":case "smoke":
        return e ? "hass:shield-check" : "hass:alert";case "heat":
        return e ? "hass:thermometer" : "hass:fire";case "light":
        return e ? "hass:brightness-5" : "hass:brightness-7";case "lock":
        return e ? "hass:lock" : "hass:lock-open";case "moisture":
        return e ? "hass:water-off" : "hass:water";case "motion":
        return e ? "hass:walk" : "hass:run";case "occupancy":
        return e ? "hass:home-outline" : "hass:home";case "opening":
        return e ? "hass:square" : "hass:square-outline";case "plug":
        return e ? "hass:power-plug-off" : "hass:power-plug";case "presence":
        return e ? "hass:home-outline" : "hass:home";case "sound":
        return e ? "hass:music-note-off" : "hass:music-note";case "vibration":
        return e ? "hass:crop-portrait" : "hass:vibrate";case "window":
        return e ? "hass:window-closed" : "hass:window-open";default:
        return e ? "hass:radiobox-blank" : "hass:checkbox-marked-circle";}
  }, cover: function (t) {
    var e = "closed" !== t.state;switch (t.attributes.device_class) {case "garage":
        return e ? "hass:garage-open" : "hass:garage";case "door":
        return e ? "hass:door-open" : "hass:door-closed";case "shutter":
        return e ? "hass:window-shutter-open" : "hass:window-shutter";case "blind":
        return e ? "hass:blinds-open" : "hass:blinds";case "window":
        return e ? "hass:window-open" : "hass:window-closed";default:
        return It("cover", t.state);}
  }, sensor: function (t) {
    var e = t.attributes.device_class;if (e && e in Yt) return Yt[e];if ("battery" === e) {
      var i = Number(t.state);if (isNaN(i)) return "hass:battery-unknown";var n = 10 * Math.round(i / 10);return n >= 100 ? "hass:battery" : n <= 0 ? "hass:battery-alert" : "hass:battery-" + n;
    }var s = t.attributes.unit_of_measurement;return "°C" === s || "°F" === s ? "hass:thermometer" : It("sensor");
  }, input_datetime: function (t) {
    return t.attributes.has_date ? t.attributes.has_time ? It("input_datetime") : "hass:calendar" : "hass:clock";
  } };const Wt = (t, e, i, n) => {
  n = n || {}, i = null == i ? {} : i;const s = new Event(e, { bubbles: void 0 === n.bubbles || n.bubbles, cancelable: Boolean(n.cancelable), composed: void 0 === n.composed || n.composed });return s.detail = i, t.dispatchEvent(s), s;
},
      Jt = "ontouchstart" in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;class Gt extends HTMLElement {
  constructor() {
    super(), this.holdTime = 500, this.held = !1, this.isRepeating = !1, this.ripple = document.createElement("mwc-ripple");
  }connectedCallback() {
    Object.assign(this.style, { position: "absolute", width: Jt ? "100px" : "50px", height: Jt ? "100px" : "50px", transform: "translate(-50%, -50%)", pointerEvents: "none" }), this.appendChild(this.ripple), this.ripple.primary = !0, ["touchcancel", "mouseout", "mouseup", "touchmove", "mousewheel", "wheel", "scroll"].forEach(t => {
      document.addEventListener(t, () => {
        clearTimeout(this.timer), this.stopAnimation(), this.timer = void 0;
      }, { passive: !0 });
    });
  }bind(t, e) {
    if (t.actionHandler) return;t.actionHandler = !0, t.addEventListener("contextmenu", t => {
      const e = t || window.event;return e.preventDefault && e.preventDefault(), e.stopPropagation && e.stopPropagation(), e.cancelBubble = !0, e.returnValue = !1, !1;
    });const i = i => {
      let n, s;this.held = !1, i.touches ? (n = i.touches[0].pageX, s = i.touches[0].pageY) : (n = i.pageX, s = i.pageY), this.timer = window.setTimeout(() => {
        this.startAnimation(n, s), this.held = !0, e.repeat && !this.isRepeating && (this.isRepeating = !0, this.repeatTimeout = setInterval(() => {
          Wt(t, "action", { action: "hold" });
        }, e.repeat));
      }, this.holdTime);
    },
          n = i => {
      i.preventDefault(), ["touchend", "touchcancel"].includes(i.type) && void 0 === this.timer ? this.isRepeating && this.repeatTimeout && (clearInterval(this.repeatTimeout), this.isRepeating = !1) : (clearTimeout(this.timer), this.isRepeating && this.repeatTimeout && clearInterval(this.repeatTimeout), this.isRepeating = !1, this.stopAnimation(), this.timer = void 0, this.held ? e.repeat || Wt(t, "action", { action: "hold" }) : e.hasDoubleClick ? "click" === i.type && i.detail < 2 || !this.dblClickTimeout ? this.dblClickTimeout = window.setTimeout(() => {
        this.dblClickTimeout = void 0, Wt(t, "action", { action: "tap" });
      }, 250) : (clearTimeout(this.dblClickTimeout), this.dblClickTimeout = void 0, Wt(t, "action", { action: "double_tap" })) : Wt(t, "action", { action: "tap" }));
    };t.addEventListener("touchstart", i, { passive: !0 }), t.addEventListener("touchend", n), t.addEventListener("touchcancel", n), t.addEventListener("mousedown", i, { passive: !0 }), t.addEventListener("click", n), t.addEventListener("keyup", t => {
      13 === t.keyCode && n(t);
    });
  }startAnimation(t, e) {
    Object.assign(this.style, { left: `${t}px`, top: `${e}px`, display: null }), this.ripple.disabled = !1, this.ripple.active = !0, this.ripple.unbounded = !0;
  }stopAnimation() {
    this.ripple.active = !1, this.ripple.disabled = !0, this.style.display = "none";
  }
}customElements.define("button-card-action-handler", Gt);const Zt = (t, e) => {
  const i = (() => {
    const t = document.body;if (t.querySelector("button-card-action-handler")) return t.querySelector("button-card-action-handler");const e = document.createElement("button-card-action-handler");return t.appendChild(e), e;
  })();i && i.bind(t, e);
},
      Xt = m((t = {}) => e => {
  Zt(e.committer.element, t);
});function Kt(t, e) {
  (function (t) {
    return "string" == typeof t && t.includes(".") && 1 === parseFloat(t);
  })(t) && (t = "100%");var i = function (t) {
    return "string" == typeof t && t.includes("%");
  }(t);return t = 360 === e ? t : Math.min(e, Math.max(0, parseFloat(t))), i && (t = parseInt(String(t * e), 10) / 100), Math.abs(t - e) < 1e-6 ? 1 : t = 360 === e ? (t < 0 ? t % e + e : t % e) / parseFloat(String(e)) : t % e / parseFloat(String(e));
}function Qt(t) {
  return Math.min(1, Math.max(0, t));
}function te(t) {
  return t = parseFloat(t), (isNaN(t) || t < 0 || t > 1) && (t = 1), t;
}function ee(t) {
  return t <= 1 ? 100 * Number(t) + "%" : t;
}function ie(t) {
  return 1 === t.length ? "0" + t : String(t);
}function ne(t, e, i) {
  t = Kt(t, 255), e = Kt(e, 255), i = Kt(i, 255);var n = Math.max(t, e, i),
      s = Math.min(t, e, i),
      r = 0,
      a = 0,
      o = (n + s) / 2;if (n === s) a = 0, r = 0;else {
    var l = n - s;switch (a = o > .5 ? l / (2 - n - s) : l / (n + s), n) {case t:
        r = (e - i) / l + (e < i ? 6 : 0);break;case e:
        r = (i - t) / l + 2;break;case i:
        r = (t - e) / l + 4;}r /= 6;
  }return { h: r, s: a, l: o };
}function se(t, e, i) {
  return i < 0 && (i += 1), i > 1 && (i -= 1), i < 1 / 6 ? t + 6 * i * (e - t) : i < .5 ? e : i < 2 / 3 ? t + (e - t) * (2 / 3 - i) * 6 : t;
}function re(t, e, i) {
  t = Kt(t, 255), e = Kt(e, 255), i = Kt(i, 255);var n = Math.max(t, e, i),
      s = Math.min(t, e, i),
      r = 0,
      a = n,
      o = n - s,
      l = 0 === n ? 0 : o / n;if (n === s) r = 0;else {
    switch (n) {case t:
        r = (e - i) / o + (e < i ? 6 : 0);break;case e:
        r = (i - t) / o + 2;break;case i:
        r = (t - e) / o + 4;}r /= 6;
  }return { h: r, s: l, v: a };
}function ae(t, e, i, n) {
  var s = [ie(Math.round(t).toString(16)), ie(Math.round(e).toString(16)), ie(Math.round(i).toString(16))];return n && s[0].startsWith(s[0].charAt(1)) && s[1].startsWith(s[1].charAt(1)) && s[2].startsWith(s[2].charAt(1)) ? s[0].charAt(0) + s[1].charAt(0) + s[2].charAt(0) : s.join("");
}function oe(t) {
  return Math.round(255 * parseFloat(t)).toString(16);
}function le(t) {
  return ce(t) / 255;
}function ce(t) {
  return parseInt(t, 16);
}var he = { aliceblue: "#f0f8ff", antiquewhite: "#faebd7", aqua: "#00ffff", aquamarine: "#7fffd4", azure: "#f0ffff", beige: "#f5f5dc", bisque: "#ffe4c4", black: "#000000", blanchedalmond: "#ffebcd", blue: "#0000ff", blueviolet: "#8a2be2", brown: "#a52a2a", burlywood: "#deb887", cadetblue: "#5f9ea0", chartreuse: "#7fff00", chocolate: "#d2691e", coral: "#ff7f50", cornflowerblue: "#6495ed", cornsilk: "#fff8dc", crimson: "#dc143c", cyan: "#00ffff", darkblue: "#00008b", darkcyan: "#008b8b", darkgoldenrod: "#b8860b", darkgray: "#a9a9a9", darkgreen: "#006400", darkgrey: "#a9a9a9", darkkhaki: "#bdb76b", darkmagenta: "#8b008b", darkolivegreen: "#556b2f", darkorange: "#ff8c00", darkorchid: "#9932cc", darkred: "#8b0000", darksalmon: "#e9967a", darkseagreen: "#8fbc8f", darkslateblue: "#483d8b", darkslategray: "#2f4f4f", darkslategrey: "#2f4f4f", darkturquoise: "#00ced1", darkviolet: "#9400d3", deeppink: "#ff1493", deepskyblue: "#00bfff", dimgray: "#696969", dimgrey: "#696969", dodgerblue: "#1e90ff", firebrick: "#b22222", floralwhite: "#fffaf0", forestgreen: "#228b22", fuchsia: "#ff00ff", gainsboro: "#dcdcdc", ghostwhite: "#f8f8ff", gold: "#ffd700", goldenrod: "#daa520", gray: "#808080", green: "#008000", greenyellow: "#adff2f", grey: "#808080", honeydew: "#f0fff0", hotpink: "#ff69b4", indianred: "#cd5c5c", indigo: "#4b0082", ivory: "#fffff0", khaki: "#f0e68c", lavender: "#e6e6fa", lavenderblush: "#fff0f5", lawngreen: "#7cfc00", lemonchiffon: "#fffacd", lightblue: "#add8e6", lightcoral: "#f08080", lightcyan: "#e0ffff", lightgoldenrodyellow: "#fafad2", lightgray: "#d3d3d3", lightgreen: "#90ee90", lightgrey: "#d3d3d3", lightpink: "#ffb6c1", lightsalmon: "#ffa07a", lightseagreen: "#20b2aa", lightskyblue: "#87cefa", lightslategray: "#778899", lightslategrey: "#778899", lightsteelblue: "#b0c4de", lightyellow: "#ffffe0", lime: "#00ff00", limegreen: "#32cd32", linen: "#faf0e6", magenta: "#ff00ff", maroon: "#800000", mediumaquamarine: "#66cdaa", mediumblue: "#0000cd", mediumorchid: "#ba55d3", mediumpurple: "#9370db", mediumseagreen: "#3cb371", mediumslateblue: "#7b68ee", mediumspringgreen: "#00fa9a", mediumturquoise: "#48d1cc", mediumvioletred: "#c71585", midnightblue: "#191970", mintcream: "#f5fffa", mistyrose: "#ffe4e1", moccasin: "#ffe4b5", navajowhite: "#ffdead", navy: "#000080", oldlace: "#fdf5e6", olive: "#808000", olivedrab: "#6b8e23", orange: "#ffa500", orangered: "#ff4500", orchid: "#da70d6", palegoldenrod: "#eee8aa", palegreen: "#98fb98", paleturquoise: "#afeeee", palevioletred: "#db7093", papayawhip: "#ffefd5", peachpuff: "#ffdab9", peru: "#cd853f", pink: "#ffc0cb", plum: "#dda0dd", powderblue: "#b0e0e6", purple: "#800080", rebeccapurple: "#663399", red: "#ff0000", rosybrown: "#bc8f8f", royalblue: "#4169e1", saddlebrown: "#8b4513", salmon: "#fa8072", sandybrown: "#f4a460", seagreen: "#2e8b57", seashell: "#fff5ee", sienna: "#a0522d", silver: "#c0c0c0", skyblue: "#87ceeb", slateblue: "#6a5acd", slategray: "#708090", slategrey: "#708090", snow: "#fffafa", springgreen: "#00ff7f", steelblue: "#4682b4", tan: "#d2b48c", teal: "#008080", thistle: "#d8bfd8", tomato: "#ff6347", turquoise: "#40e0d0", violet: "#ee82ee", wheat: "#f5deb3", white: "#ffffff", whitesmoke: "#f5f5f5", yellow: "#ffff00", yellowgreen: "#9acd32" };function ue(t) {
  var e = { r: 0, g: 0, b: 0 },
      i = 1,
      n = null,
      s = null,
      r = null,
      a = !1,
      o = !1;return "string" == typeof t && (t = function (t) {
    if (0 === (t = t.trim().toLowerCase()).length) return !1;var e = !1;if (he[t]) t = he[t], e = !0;else if ("transparent" === t) return { r: 0, g: 0, b: 0, a: 0, format: "name" };var i = me.rgb.exec(t);if (i) return { r: i[1], g: i[2], b: i[3] };if (i = me.rgba.exec(t)) return { r: i[1], g: i[2], b: i[3], a: i[4] };if (i = me.hsl.exec(t)) return { h: i[1], s: i[2], l: i[3] };if (i = me.hsla.exec(t)) return { h: i[1], s: i[2], l: i[3], a: i[4] };if (i = me.hsv.exec(t)) return { h: i[1], s: i[2], v: i[3] };if (i = me.hsva.exec(t)) return { h: i[1], s: i[2], v: i[3], a: i[4] };if (i = me.hex8.exec(t)) return { r: ce(i[1]), g: ce(i[2]), b: ce(i[3]), a: le(i[4]), format: e ? "name" : "hex8" };if (i = me.hex6.exec(t)) return { r: ce(i[1]), g: ce(i[2]), b: ce(i[3]), format: e ? "name" : "hex" };if (i = me.hex4.exec(t)) return { r: ce(i[1] + i[1]), g: ce(i[2] + i[2]), b: ce(i[3] + i[3]), a: le(i[4] + i[4]), format: e ? "name" : "hex8" };if (i = me.hex3.exec(t)) return { r: ce(i[1] + i[1]), g: ce(i[2] + i[2]), b: ce(i[3] + i[3]), format: e ? "name" : "hex" };return !1;
  }(t)), "object" == typeof t && (ge(t.r) && ge(t.g) && ge(t.b) ? (e = function (t, e, i) {
    return { r: 255 * Kt(t, 255), g: 255 * Kt(e, 255), b: 255 * Kt(i, 255) };
  }(t.r, t.g, t.b), a = !0, o = "%" === String(t.r).substr(-1) ? "prgb" : "rgb") : ge(t.h) && ge(t.s) && ge(t.v) ? (n = ee(t.s), s = ee(t.v), e = function (t, e, i) {
    t = 6 * Kt(t, 360), e = Kt(e, 100), i = Kt(i, 100);var n = Math.floor(t),
        s = t - n,
        r = i * (1 - e),
        a = i * (1 - s * e),
        o = i * (1 - (1 - s) * e),
        l = n % 6;return { r: 255 * [i, a, r, r, o, i][l], g: 255 * [o, i, i, a, r, r][l], b: 255 * [r, r, o, i, i, a][l] };
  }(t.h, n, s), a = !0, o = "hsv") : ge(t.h) && ge(t.s) && ge(t.l) && (n = ee(t.s), r = ee(t.l), e = function (t, e, i) {
    var n, s, r;if (t = Kt(t, 360), e = Kt(e, 100), i = Kt(i, 100), 0 === e) s = i, r = i, n = i;else {
      var a = i < .5 ? i * (1 + e) : i + e - i * e,
          o = 2 * i - a;n = se(o, a, t + 1 / 3), s = se(o, a, t), r = se(o, a, t - 1 / 3);
    }return { r: 255 * n, g: 255 * s, b: 255 * r };
  }(t.h, n, r), a = !0, o = "hsl"), Object.prototype.hasOwnProperty.call(t, "a") && (i = t.a)), i = te(i), { ok: a, format: t.format || o, r: Math.min(255, Math.max(e.r, 0)), g: Math.min(255, Math.max(e.g, 0)), b: Math.min(255, Math.max(e.b, 0)), a: i };
}var de = "(?:[-\\+]?\\d*\\.\\d+%?)|(?:[-\\+]?\\d+%?)",
    fe = "[\\s|\\(]+(" + de + ")[,|\\s]+(" + de + ")[,|\\s]+(" + de + ")\\s*\\)?",
    pe = "[\\s|\\(]+(" + de + ")[,|\\s]+(" + de + ")[,|\\s]+(" + de + ")[,|\\s]+(" + de + ")\\s*\\)?",
    me = { CSS_UNIT: new RegExp(de), rgb: new RegExp("rgb" + fe), rgba: new RegExp("rgba" + pe), hsl: new RegExp("hsl" + fe), hsla: new RegExp("hsla" + pe), hsv: new RegExp("hsv" + fe), hsva: new RegExp("hsva" + pe), hex3: /^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/, hex6: /^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/, hex4: /^#?([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})([0-9a-fA-F]{1})$/, hex8: /^#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/ };function ge(t) {
  return Boolean(me.CSS_UNIT.exec(String(t)));
}var _e = function () {
  function t(e, i) {
    var n;if (void 0 === e && (e = ""), void 0 === i && (i = {}), e instanceof t) return e;this.originalInput = e;var s = ue(e);this.originalInput = e, this.r = s.r, this.g = s.g, this.b = s.b, this.a = s.a, this.roundA = Math.round(100 * this.a) / 100, this.format = null !== (n = i.format) && void 0 !== n ? n : s.format, this.gradientType = i.gradientType, this.r < 1 && (this.r = Math.round(this.r)), this.g < 1 && (this.g = Math.round(this.g)), this.b < 1 && (this.b = Math.round(this.b)), this.isValid = s.ok;
  }return t.prototype.isDark = function () {
    return this.getBrightness() < 128;
  }, t.prototype.isLight = function () {
    return !this.isDark();
  }, t.prototype.getBrightness = function () {
    var t = this.toRgb();return (299 * t.r + 587 * t.g + 114 * t.b) / 1e3;
  }, t.prototype.getLuminance = function () {
    var t = this.toRgb(),
        e = t.r / 255,
        i = t.g / 255,
        n = t.b / 255;return .2126 * (e <= .03928 ? e / 12.92 : Math.pow((e + .055) / 1.055, 2.4)) + .7152 * (i <= .03928 ? i / 12.92 : Math.pow((i + .055) / 1.055, 2.4)) + .0722 * (n <= .03928 ? n / 12.92 : Math.pow((n + .055) / 1.055, 2.4));
  }, t.prototype.getAlpha = function () {
    return this.a;
  }, t.prototype.setAlpha = function (t) {
    return this.a = te(t), this.roundA = Math.round(100 * this.a) / 100, this;
  }, t.prototype.toHsv = function () {
    var t = re(this.r, this.g, this.b);return { h: 360 * t.h, s: t.s, v: t.v, a: this.a };
  }, t.prototype.toHsvString = function () {
    var t = re(this.r, this.g, this.b),
        e = Math.round(360 * t.h),
        i = Math.round(100 * t.s),
        n = Math.round(100 * t.v);return 1 === this.a ? "hsv(" + e + ", " + i + "%, " + n + "%)" : "hsva(" + e + ", " + i + "%, " + n + "%, " + this.roundA + ")";
  }, t.prototype.toHsl = function () {
    var t = ne(this.r, this.g, this.b);return { h: 360 * t.h, s: t.s, l: t.l, a: this.a };
  }, t.prototype.toHslString = function () {
    var t = ne(this.r, this.g, this.b),
        e = Math.round(360 * t.h),
        i = Math.round(100 * t.s),
        n = Math.round(100 * t.l);return 1 === this.a ? "hsl(" + e + ", " + i + "%, " + n + "%)" : "hsla(" + e + ", " + i + "%, " + n + "%, " + this.roundA + ")";
  }, t.prototype.toHex = function (t) {
    return void 0 === t && (t = !1), ae(this.r, this.g, this.b, t);
  }, t.prototype.toHexString = function (t) {
    return void 0 === t && (t = !1), "#" + this.toHex(t);
  }, t.prototype.toHex8 = function (t) {
    return void 0 === t && (t = !1), function (t, e, i, n, s) {
      var r = [ie(Math.round(t).toString(16)), ie(Math.round(e).toString(16)), ie(Math.round(i).toString(16)), ie(oe(n))];return s && r[0].startsWith(r[0].charAt(1)) && r[1].startsWith(r[1].charAt(1)) && r[2].startsWith(r[2].charAt(1)) && r[3].startsWith(r[3].charAt(1)) ? r[0].charAt(0) + r[1].charAt(0) + r[2].charAt(0) + r[3].charAt(0) : r.join("");
    }(this.r, this.g, this.b, this.a, t);
  }, t.prototype.toHex8String = function (t) {
    return void 0 === t && (t = !1), "#" + this.toHex8(t);
  }, t.prototype.toRgb = function () {
    return { r: Math.round(this.r), g: Math.round(this.g), b: Math.round(this.b), a: this.a };
  }, t.prototype.toRgbString = function () {
    var t = Math.round(this.r),
        e = Math.round(this.g),
        i = Math.round(this.b);return 1 === this.a ? "rgb(" + t + ", " + e + ", " + i + ")" : "rgba(" + t + ", " + e + ", " + i + ", " + this.roundA + ")";
  }, t.prototype.toPercentageRgb = function () {
    var t = function (t) {
      return Math.round(100 * Kt(t, 255)) + "%";
    };return { r: t(this.r), g: t(this.g), b: t(this.b), a: this.a };
  }, t.prototype.toPercentageRgbString = function () {
    var t = function (t) {
      return Math.round(100 * Kt(t, 255));
    };return 1 === this.a ? "rgb(" + t(this.r) + "%, " + t(this.g) + "%, " + t(this.b) + "%)" : "rgba(" + t(this.r) + "%, " + t(this.g) + "%, " + t(this.b) + "%, " + this.roundA + ")";
  }, t.prototype.toName = function () {
    if (0 === this.a) return "transparent";if (this.a < 1) return !1;for (var t = "#" + ae(this.r, this.g, this.b, !1), e = 0, i = Object.keys(he); e < i.length; e++) {
      var n = i[e];if (he[n] === t) return n;
    }return !1;
  }, t.prototype.toString = function (t) {
    var e = Boolean(t);t = null != t ? t : this.format;var i = !1,
        n = this.a < 1 && this.a >= 0;return e || !n || !t.startsWith("hex") && "name" !== t ? ("rgb" === t && (i = this.toRgbString()), "prgb" === t && (i = this.toPercentageRgbString()), "hex" !== t && "hex6" !== t || (i = this.toHexString()), "hex3" === t && (i = this.toHexString(!0)), "hex4" === t && (i = this.toHex8String(!0)), "hex8" === t && (i = this.toHex8String()), "name" === t && (i = this.toName()), "hsl" === t && (i = this.toHslString()), "hsv" === t && (i = this.toHsvString()), i || this.toHexString()) : "name" === t && 0 === this.a ? this.toName() : this.toRgbString();
  }, t.prototype.clone = function () {
    return new t(this.toString());
  }, t.prototype.lighten = function (e) {
    void 0 === e && (e = 10);var i = this.toHsl();return i.l += e / 100, i.l = Qt(i.l), new t(i);
  }, t.prototype.brighten = function (e) {
    void 0 === e && (e = 10);var i = this.toRgb();return i.r = Math.max(0, Math.min(255, i.r - Math.round(-e / 100 * 255))), i.g = Math.max(0, Math.min(255, i.g - Math.round(-e / 100 * 255))), i.b = Math.max(0, Math.min(255, i.b - Math.round(-e / 100 * 255))), new t(i);
  }, t.prototype.darken = function (e) {
    void 0 === e && (e = 10);var i = this.toHsl();return i.l -= e / 100, i.l = Qt(i.l), new t(i);
  }, t.prototype.tint = function (t) {
    return void 0 === t && (t = 10), this.mix("white", t);
  }, t.prototype.shade = function (t) {
    return void 0 === t && (t = 10), this.mix("black", t);
  }, t.prototype.desaturate = function (e) {
    void 0 === e && (e = 10);var i = this.toHsl();return i.s -= e / 100, i.s = Qt(i.s), new t(i);
  }, t.prototype.saturate = function (e) {
    void 0 === e && (e = 10);var i = this.toHsl();return i.s += e / 100, i.s = Qt(i.s), new t(i);
  }, t.prototype.greyscale = function () {
    return this.desaturate(100);
  }, t.prototype.spin = function (e) {
    var i = this.toHsl(),
        n = (i.h + e) % 360;return i.h = n < 0 ? 360 + n : n, new t(i);
  }, t.prototype.mix = function (e, i) {
    void 0 === i && (i = 50);var n = this.toRgb(),
        s = new t(e).toRgb(),
        r = i / 100;return new t({ r: (s.r - n.r) * r + n.r, g: (s.g - n.g) * r + n.g, b: (s.b - n.b) * r + n.b, a: (s.a - n.a) * r + n.a });
  }, t.prototype.analogous = function (e, i) {
    void 0 === e && (e = 6), void 0 === i && (i = 30);var n = this.toHsl(),
        s = 360 / i,
        r = [this];for (n.h = (n.h - (s * e >> 1) + 720) % 360; --e;) n.h = (n.h + s) % 360, r.push(new t(n));return r;
  }, t.prototype.complement = function () {
    var e = this.toHsl();return e.h = (e.h + 180) % 360, new t(e);
  }, t.prototype.monochromatic = function (e) {
    void 0 === e && (e = 6);for (var i = this.toHsv(), n = i.h, s = i.s, r = i.v, a = [], o = 1 / e; e--;) a.push(new t({ h: n, s: s, v: r })), r = (r + o) % 1;return a;
  }, t.prototype.splitcomplement = function () {
    var e = this.toHsl(),
        i = e.h;return [this, new t({ h: (i + 72) % 360, s: e.s, l: e.l }), new t({ h: (i + 216) % 360, s: e.s, l: e.l })];
  }, t.prototype.triad = function () {
    return this.polyad(3);
  }, t.prototype.tetrad = function () {
    return this.polyad(4);
  }, t.prototype.polyad = function (e) {
    for (var i = this.toHsl(), n = i.h, s = [this], r = 360 / e, a = 1; a < e; a++) s.push(new t({ h: (n + a * r) % 360, s: i.s, l: i.l }));return s;
  }, t.prototype.equals = function (e) {
    return this.toRgbString() === new t(e).toRgbString();
  }, t;
}();function be(t, e) {
  return void 0 === t && (t = ""), void 0 === e && (e = {}), new _e(t, e);
}function ye(t) {
  return t.substr(0, t.indexOf("."));
}function ve(t) {
  return "var" === t.substring(0, 3) ? window.getComputedStyle(document.documentElement).getPropertyValue(t.substring(4).slice(0, -1)).trim() : t;
}function we(t, e) {
  const i = new _e(ve(t));if (i.isValid) {
    const t = i.mix("black", 100 - e).toString();if (t) return t;
  }return t;
}function Se(...t) {
  const e = t => t && "object" == typeof t;return t.reduce((t, i) => (Object.keys(i).forEach(n => {
    const s = t[n],
          r = i[n];Array.isArray(s) && Array.isArray(r) ? t[n] = s.concat(...r) : e(s) && e(r) ? t[n] = Se(s, r) : t[n] = r;
  }), t), {});
}function xe(t, e) {
  let i = [];return t && t.forEach(t => {
    let n = t;e && e.forEach(e => {
      e.id && t.id && e.id == t.id && (n = Se(n, e));
    }), i.push(n);
  }), e && (i = i.concat(e.filter(e => !t || !t.find(t => !(!t.id || !e.id) && t.id == e.id)))), i;
}const ke = ((t, ...e) => {
  const i = e.reduce((e, i, n) => e + (t => {
    if (t instanceof K) return t.cssText;if ("number" == typeof t) return t;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${t}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`);
  })(i) + t[n + 1], t[0]);return new K(i, X);
})`
  :host {
    position: relative;
    display: block;
  }
  ha-card {
    cursor: pointer;
    overflow: hidden;
    box-sizing: border-box;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    line-height: normal;

    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Old versions of Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    user-select: none; /* Non-prefixed version, currently
                          supported by Chrome, Opera and Firefox */
  }
  ha-card.disabled {
    pointer-events: none;
    cursor: default;
  }
  ha-icon {
    display: inline-block;
    margin: auto;
  }
  ha-card.button-card-main {
    padding: 4% 0px;
    text-transform: none;
    font-weight: 400;
    font-size: 1.2rem;
    align-items: center;
    text-align: center;
    letter-spacing: normal;
    width: 100%;
  }
  .ellipsis {
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
  }
  #overlay {
    align-items: flex-start;
    justify-content: flex-end;
    padding: 8px 7px;
    opacity: 0.5;
    /* DO NOT override items below */
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 50;
    display: flex;
  }
  #lock {
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
    margin: unset;
  }
  .invalid {
    animation: blink 1s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
  }
  .hidden {
    visibility: hidden;
    opacity: 0;
    transition: visibility 0s 1s, opacity 1s linear;
  }
  @keyframes blink {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }
  @-webkit-keyframes rotating /* Safari and Chrome */ {
    from {
      -webkit-transform: rotate(0deg);
      -o-transform: rotate(0deg);
      transform: rotate(0deg);
    }
    to {
      -webkit-transform: rotate(360deg);
      -o-transform: rotate(360deg);
      transform: rotate(360deg);
    }
  }
  @keyframes rotating {
    from {
      -ms-transform: rotate(0deg);
      -moz-transform: rotate(0deg);
      -webkit-transform: rotate(0deg);
      -o-transform: rotate(0deg);
      transform: rotate(0deg);
    }
    to {
      -ms-transform: rotate(360deg);
      -moz-transform: rotate(360deg);
      -webkit-transform: rotate(360deg);
      -o-transform: rotate(360deg);
      transform: rotate(360deg);
    }
  }
  [rotating] {
    -webkit-animation: rotating 2s linear infinite;
    -moz-animation: rotating 2s linear infinite;
    -ms-animation: rotating 2s linear infinite;
    -o-animation: rotating 2s linear infinite;
    animation: rotating 2s linear infinite;
  }

  #container {
    display: grid;
    width: 100%;
    height: 100%;
    text-align: center;
    align-items: center;
  }
  #img-cell {
    display: flex;
    grid-area: i;
    height: 100%;
    width: 100%;
    max-width: 100%;
    max-height: 100%;
    align-self: center;
    justify-self: center;
    overflow: hidden;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  ha-icon#icon {
    height: 100%;
    width: 100%;
    max-height: 100%;
    position: absolute;
  }
  img#icon {
    display: block;
    height: auto;
    width: 100%;
    position: absolute;
  }
  #name {
    grid-area: n;
    max-width: 100%;
    align-self: center;
    justify-self: center;
    /* margin: auto; */
  }
  #state {
    grid-area: s;
    max-width: 100%;
    align-self: center;
    justify-self: center;
    /* margin: auto; */
  }

  #label {
    grid-area: l;
    max-width: 100%;
    align-self: center;
    justify-self: center;
  }

  #container.vertical {
    grid-template-areas: 'i' 'n' 's' 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr min-content min-content min-content;
  }
  /* Vertical No Icon */
  #container.vertical.no-icon {
    grid-template-areas: 'n' 's' 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr min-content 1fr;
  }
  #container.vertical.no-icon #state {
    align-self: center;
  }
  #container.vertical.no-icon #name {
    align-self: end;
  }
  #container.vertical.no-icon #label {
    align-self: start;
  }

  /* Vertical No Icon No Name */
  #container.vertical.no-icon.no-name {
    grid-template-areas: 's' 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  #container.vertical.no-icon.no-name #state {
    align-self: end;
  }
  #container.vertical.no-icon.no-name #label {
    align-self: start;
  }

  /* Vertical No Icon No State */
  #container.vertical.no-icon.no-state {
    grid-template-areas: 'n' 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  #container.vertical.no-icon.no-state #name {
    align-self: end;
  }
  #container.vertical.no-icon.no-state #label {
    align-self: start;
  }

  /* Vertical No Icon No Label */
  #container.vertical.no-icon.no-label {
    grid-template-areas: 'n' 's';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  #container.vertical.no-icon.no-label #name {
    align-self: end;
  }
  #container.vertical.no-icon.no-label #state {
    align-self: start;
  }

  /* Vertical No Icon No Label No Name */
  #container.vertical.no-icon.no-label.no-name {
    grid-template-areas: 's';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
  }
  #container.vertical.no-icon.no-label.no-name #state {
    align-self: center;
  }
  /* Vertical No Icon No Label No State */
  #container.vertical.no-icon.no-label.no-state {
    grid-template-areas: 'n';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
  }
  #container.vertical.no-icon.no-label.no-state #name {
    align-self: center;
  }

  /* Vertical No Icon No Name No State */
  #container.vertical.no-icon.no-name.no-state {
    grid-template-areas: 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
  }
  #container.vertical.no-icon.no-name.no-state #label {
    align-self: center;
  }

  #container.icon_name_state {
    grid-template-areas: 'i n' 'l l';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr min-content;
  }

  #container.icon_name {
    grid-template-areas: 'i n' 's s' 'l l';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr min-content min-content;
  }

  #container.icon_state {
    grid-template-areas: 'i s' 'n n' 'l l';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr min-content min-content;
  }

  #container.name_state {
    grid-template-areas: 'i' 'n' 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr min-content min-content;
  }
  #container.name_state.no-icon {
    grid-template-areas: 'n' 'l';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  #container.name_state.no-icon #name {
    align-self: end;
  }
  #container.name_state.no-icon #label {
    align-self: start;
  }

  #container.name_state.no-icon.no-label {
    grid-template-areas: 'n';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
  }
  #container.name_state.no-icon.no-label #name {
    align-self: center;
  }

  /* icon_name_state2nd default */
  #container.icon_name_state2nd {
    grid-template-areas: 'i n' 'i s' 'i l';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr min-content 1fr;
  }
  #container.icon_name_state2nd #name {
    align-self: end;
  }
  #container.icon_name_state2nd #state {
    align-self: center;
  }
  #container.icon_name_state2nd #label {
    align-self: start;
  }

  /* icon_name_state2nd No Label */
  #container.icon_name_state2nd.no-label {
    grid-template-areas: 'i n' 'i s';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr 1fr;
  }
  #container.icon_name_state2nd #name {
    align-self: end;
  }
  #container.icon_name_state2nd #state {
    align-self: start;
  }

  /* icon_state_name2nd Default */
  #container.icon_state_name2nd {
    grid-template-areas: 'i s' 'i n' 'i l';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr min-content 1fr;
  }
  #container.icon_state_name2nd #state {
    align-self: end;
  }
  #container.icon_state_name2nd #name {
    align-self: center;
  }
  #container.icon_state_name2nd #label {
    align-self: start;
  }

  /* icon_state_name2nd No Label */
  #container.icon_state_name2nd.no-label {
    grid-template-areas: 'i s' 'i n';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr 1fr;
  }
  #container.icon_state_name2nd #state {
    align-self: end;
  }
  #container.icon_state_name2nd #name {
    align-self: start;
  }

  #container.icon_label {
    grid-template-areas: 'i l' 'n n' 's s';
    grid-template-columns: 40% 1fr;
    grid-template-rows: 1fr min-content min-content;
  }

  [style*='--aspect-ratio'] > :first-child {
    width: 100%;
  }
  [style*='--aspect-ratio'] > img {
    height: auto;
  }
  @supports (--custom: property) {
    [style*='--aspect-ratio'] {
      position: relative;
    }
    [style*='--aspect-ratio']::before {
      content: '';
      display: block;
      padding-bottom: calc(100% / (var(--aspect-ratio)));
    }
    [style*='--aspect-ratio'] > :first-child {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
    }
  }
`;const Te = (t, e, i, n) => {
  if (!((t, e, i) => {
    const [n, s] = t.split(".", 2);return Number(n) > e || Number(n) === e && Number(s) >= i;
  })(t.connection.haVersion, 0, 109)) return function (t, e) {
    let i;const n = ye(e.entity_id);return "binary_sensor" === n ? (e.attributes.device_class && (i = t(`state.${n}.${e.attributes.device_class}.${e.state}`)), i || (i = t(`state.${n}.default.${e.state}`))) : i = e.attributes.unit_of_measurement && !["unknown", "unavailable"].includes(e.state) ? e.state : "zwave" === n ? ["initializing", "dead"].includes(e.state) ? t(`state.zwave.query_stage.${e.state}`, "query_stage", e.attributes.query_stage) : t(`state.zwave.default.${e.state}`) : t(`state.${n}.${e.state}`), i || (i = t(`state.default.${e.state}`) || t(`component.${n}.state.${e.state}`) || e.state), i;
  }(e, i);if ("unknown" === i.state || "unavailable" === i.state) return e(`state.default.${i.state}`);if (i.attributes.unit_of_measurement) return `${i.state} ${i.attributes.unit_of_measurement}`;const s = ye(i.entity_id);if ("input_datetime" === s) {
    let t;if (!i.attributes.has_time) return t = new Date(i.attributes.year, i.attributes.month - 1, i.attributes.day), Ct(t, n);if (!i.attributes.has_date) {
      const e = new Date();return t = new Date(e.getFullYear(), e.getMonth(), e.getDay(), i.attributes.hour, i.attributes.minute), At(t, n);
    }return t = new Date(i.attributes.year, i.attributes.month - 1, i.attributes.day, i.attributes.hour, i.attributes.minute), Et(t, n);
  }return i.attributes.device_class && e(`component.${s}.state.${i.attributes.device_class}.${i.state}`) || e(`component.${s}.state._.${i.state}`) || i.state;
};let Me = window.cardHelpers;const Ne = new Promise(async t => {
  Me && t(), window.loadCardHelpers && (Me = await window.loadCardHelpers(), window.cardHelpers = Me, t());
});console.info("%c  BUTTON-CARD  \n%c Version 3.3.2 ", "color: orange; font-weight: bold; background: black", "color: white; font-weight: bold; background: dimgray");let Oe = class extends tt {
  constructor() {
    super(...arguments), this._cards = [], this._entities = [];
  }set hass(t) {
    this._hass = t;for (const e of this._cards) {
      e.hass = this._hass;
    }
  }disconnectedCallback() {
    super.disconnectedCallback(), this._clearInterval();
  }connectedCallback() {
    if (super.connectedCallback(), this._hass && this._config && this._config.entity && "timer" === ye(this._config.entity)) {
      const t = this._hass.states[this._config.entity];this._startInterval(t);
    }
  }_createCard(t) {
    if (Me) return Me.createCardElement(t);{
      const e = function (t, e) {
        void 0 === e && (e = !1);var i = function (t, e) {
          return n("hui-error-card", { type: "error", error: t, config: e });
        },
            n = function (t, e) {
          var n = window.document.createElement(t);try {
            n.setConfig(e);
          } catch (n) {
            return console.error(t, n), i(n.message, e);
          }return n;
        };if (!t || "object" != typeof t || !e && !t.type) return i("No type defined", t);var s = t.type;if (s && s.startsWith("custom:")) s = s.substr("custom:".length);else if (e) {
          if (Dt.has(s)) s = "hui-" + s + "-row";else {
            if (!t.entity) return i("Invalid config given.", t);var r = t.entity.split(".", 1)[0];s = "hui-" + (Lt[r] || "text") + "-entity-row";
          }
        } else s = "hui-" + s + "-card";if (customElements.get(s)) return n(s, t);var a = i("Custom element doesn't exist: " + t.type + ".", t);a.style.display = "None";var o = setTimeout(function () {
          a.style.display = "";
        }, 2e3);return customElements.whenDefined(t.type).then(function () {
          clearTimeout(o), Rt(a, "ll-rebuild", {}, a);
        }), a;
      }(t);return Ne.then(() => {
        Rt(e, "ll-rebuild", {});
      }), e;
    }
  }static get styles() {
    return ke;
  }render() {
    this._stateObj = this._config.entity ? this._hass.states[this._config.entity] : void 0;try {
      return this._cards = [], this._evaledVariables = this._config.variables ? this._objectEvalTemplate(this._stateObj, this._config.variables) : void 0, this._config && this._hass ? this._cardHtml() : R``;
    } catch (t) {
      t.stack ? console.error(t.stack) : console.error(t);const e = document.createElement("hui-error-card");return e.setConfig({ type: "error", error: t.toString(), origConfig: this._config }), R`
        ${e}
      `;
    }
  }shouldUpdate(t) {
    return !(!this._hasTemplate && !t.has("_timeRemaining")) || function (t, e) {
      if (e.has("_config")) return !0;const i = e.get("_hass");if (i) {
        return t._entities.some(function (e) {
          return (null == i ? void 0 : i.states[e]) !== t._hass.states[e];
        });
      }return !1;
    }(this, t);
  }updated(t) {
    if (super.updated(t), this._config && this._config.entity && "timer" === ye(this._config.entity) && t.has("_hass")) {
      const e = this._hass.states[this._config.entity],
            i = t.get("_hass");(i ? i.states[this._config.entity] : void 0) !== e ? this._startInterval(e) : e || this._clearInterval();
    }
  }_clearInterval() {
    this._interval && (window.clearInterval(this._interval), this._interval = void 0);
  }_startInterval(t) {
    this._clearInterval(), this._calculateRemaining(t), "active" === t.state && (this._interval = window.setInterval(() => this._calculateRemaining(t), 1e3));
  }_calculateRemaining(t) {
    this._timeRemaining = function (t) {
      var e = Ot(t.attributes.remaining);if ("active" === t.state) {
        var i = new Date().getTime(),
            n = new Date(t.last_changed).getTime();e = Math.max(e - (i - n) / 1e3, 0);
      }return e;
    }(t);
  }_computeTimeDisplay(t) {
    if (t) return function (t) {
      var e = Math.floor(t / 3600),
          i = Math.floor(t % 3600 / 60),
          n = Math.floor(t % 3600 % 60);return e > 0 ? e + ":" + Pt(i) + ":" + Pt(n) : i > 0 ? i + ":" + Pt(n) : n > 0 ? "" + n : null;
    }(this._timeRemaining || Ot(t.attributes.duration));
  }_getMatchingConfigState(t) {
    if (!this._config.state) return;const e = this._config.state.find(t => "template" === t.operator);if (!t && !e) return;let i;const n = this._config.state.find(e => {
      if (!e.operator) return t && this._getTemplateOrValue(t, e.value) == t.state;switch (e.operator) {case "==":
          return t && t.state == this._getTemplateOrValue(t, e.value);case "<=":
          return t && t.state <= this._getTemplateOrValue(t, e.value);case "<":
          return t && t.state < this._getTemplateOrValue(t, e.value);case ">=":
          return t && t.state >= this._getTemplateOrValue(t, e.value);case ">":
          return t && t.state > this._getTemplateOrValue(t, e.value);case "!=":
          return t && t.state != this._getTemplateOrValue(t, e.value);case "regex":
          return !(!t || !t.state.match(this._getTemplateOrValue(t, e.value)));case "template":
          return this._getTemplateOrValue(t, e.value);case "default":
          return i = e, !1;default:
          return !1;}
    });return !n && i ? i : n;
  }_evalTemplate(t, e) {
    try {
      return new Function("states", "entity", "user", "hass", "variables", "html", `'use strict'; ${e}`).call(this, this._hass.states, t, this._hass.user, this._hass, this._evaledVariables, R);
    } catch (i) {
      const t = e.length <= 100 ? e.trim() : `${e.trim().substring(0, 98)}...`;throw i.message = `${i.name}: ${i.message} in '${t}'`, i.name = "ButtonCardJSTemplateError", i;
    }
  }_objectEvalTemplate(t, e) {
    const i = JSON.parse(JSON.stringify(e));return this._getTemplateOrValue(t, i);
  }_getTemplateOrValue(t, e) {
    if (["number", "boolean"].includes(typeof e)) return e;if (!e) return e;if (["object"].includes(typeof e)) return Object.keys(e).forEach(i => {
      e[i] = this._getTemplateOrValue(t, e[i]);
    }), e;const i = e.trim();return "[[[" === i.substring(0, 3) && "]]]" === i.slice(-3) ? this._evalTemplate(t, i.slice(3, -3)) : e;
  }_getDefaultColorForState(t) {
    switch (t.state) {case "on":
        return this._config.color_on;case "off":
        return this._config.color_off;default:
        return this._config.default_color;}
  }_getColorForLightEntity(t, e) {
    let i = this._config.default_color;return t && (t.attributes.rgb_color ? (i = `rgb(${t.attributes.rgb_color.join(",")})`, t.attributes.brightness && (i = we(i, (t.attributes.brightness + 245) / 5))) : e && t.attributes.color_temp && t.attributes.min_mireds && t.attributes.max_mireds ? (i = function (t, e, i) {
      const n = new _e("rgb(255, 160, 0)"),
            s = new _e("rgb(166, 209, 255)"),
            r = new _e("white"),
            a = (t - e) / (i - e) * 100;return a < 50 ? be(s).mix(r, 2 * a).toRgbString() : be(r).mix(n, 2 * (a - 50)).toRgbString();
    }(t.attributes.color_temp, t.attributes.min_mireds, t.attributes.max_mireds), t.attributes.brightness && (i = we(i, (t.attributes.brightness + 245) / 5))) : i = t.attributes.brightness ? we(this._getDefaultColorForState(t), (t.attributes.brightness + 245) / 5) : this._getDefaultColorForState(t)), i;
  }_buildCssColorAttribute(t, e) {
    let i,
        n = "";return e && e.color ? n = e.color : "auto" !== this._config.color && t && "off" === t.state ? n = this._config.color_off : this._config.color && (n = this._config.color), i = "auto" == n || "auto-no-temperature" == n ? this._getColorForLightEntity(t, "auto-no-temperature" !== n) : n || (t ? this._getDefaultColorForState(t) : this._config.default_color), i;
  }_buildIcon(t, e) {
    if (!this._config.show_icon) return;let i;if (e && e.icon) i = e.icon;else if (this._config.icon) i = this._config.icon;else {
      if (!t) return;i = function (t) {
        if (!t) return jt;if (t.attributes.icon) return t.attributes.icon;var e = $t(t.entity_id);return e in Bt ? Bt[e](t) : It(e, t.state);
      }(t);
    }return this._getTemplateOrValue(t, i);
  }_buildEntityPicture(t, e) {
    if (!this._config.show_entity_picture || !t && !e && !this._config.entity_picture) return;let i;return e && e.entity_picture ? i = e.entity_picture : this._config.entity_picture ? i = this._config.entity_picture : t && (i = t.attributes && t.attributes.entity_picture ? t.attributes.entity_picture : void 0), this._getTemplateOrValue(t, i);
  }_buildStyleGeneric(t, e, i) {
    let n = {};if (this._config.styles && this._config.styles[i] && (n = Object.assign(n, ...this._config.styles[i])), e && e.styles && e.styles[i]) {
      let t = {};t = Object.assign(t, ...e.styles[i]), n = Object.assign(Object.assign({}, n), t);
    }return Object.keys(n).forEach(e => {
      n[e] = this._getTemplateOrValue(t, n[e]);
    }), n;
  }_buildCustomStyleGeneric(t, e, i) {
    let n = {};if (this._config.styles && this._config.styles.custom_fields && this._config.styles.custom_fields[i] && (n = Object.assign(n, ...this._config.styles.custom_fields[i])), e && e.styles && e.styles.custom_fields && e.styles.custom_fields[i]) {
      let t = {};t = Object.assign(t, ...e.styles.custom_fields[i]), n = Object.assign(Object.assign({}, n), t);
    }return Object.keys(n).forEach(e => {
      n[e] = this._getTemplateOrValue(t, n[e]);
    }), n;
  }_buildName(t, e) {
    if (!1 === this._config.show_name) return;let i;var n;return e && e.name ? i = e.name : this._config.name ? i = this._config.name : t && (i = t.attributes && t.attributes.friendly_name ? t.attributes.friendly_name : (n = t.entity_id).substr(n.indexOf(".") + 1)), this._getTemplateOrValue(t, i);
  }_buildStateString(t) {
    let e;if (this._config.show_state && t && t.state) {
      const i = Te(this._hass, this._hass.localize, t, this._hass.language),
            n = this._buildUnits(t);n ? e = `${t.state} ${n}` : "timer" === ye(t.entity_id) ? "idle" === t.state || 0 === this._timeRemaining ? e = i : (e = this._computeTimeDisplay(t), "paused" === t.state && (e += ` (${i})`)) : e = i;
    }return e;
  }_buildUnits(t) {
    let e;return t && this._config.show_units && (e = t.attributes && t.attributes.unit_of_measurement && !this._config.units ? t.attributes.unit_of_measurement : this._config.units ? this._config.units : void 0), e;
  }_buildLastChanged(t, e) {
    return this._config.show_last_changed && t ? R`
          <ha-relative-time
            id="label"
            class="ellipsis"
            .hass="${this._hass}"
            .datetime="${t.last_changed}"
            style=${it(e)}
          ></ha-relative-time>
        ` : void 0;
  }_buildLabel(t, e) {
    if (!this._config.show_label) return;let i;return i = e && e.label ? e.label : this._config.label, this._getTemplateOrValue(t, i);
  }_buildCustomFields(t, e) {
    let i = R``;const n = {},
          s = {};return this._config.custom_fields && Object.keys(this._config.custom_fields).forEach(e => {
      const i = this._config.custom_fields[e];i.card ? s[e] = this._objectEvalTemplate(t, i.card) : n[e] = this._getTemplateOrValue(t, i);
    }), e && e.custom_fields && Object.keys(e.custom_fields).forEach(i => {
      const r = e.custom_fields[i];r.card ? s[i] = this._objectEvalTemplate(t, r.card) : n[i] = this._getTemplateOrValue(t, r);
    }), Object.keys(n).forEach(s => {
      if (null != n[s]) {
        const r = Object.assign(Object.assign({}, this._buildCustomStyleGeneric(t, e, s)), { "grid-area": s });i = R`
          ${i}
          <div id=${s} class="ellipsis" style=${it(r)}>
            ${n[s] && "html" === n[s].type ? n[s] : st(n[s])}
          </div>
        `;
      }
    }), Object.keys(s).forEach(n => {
      if (null != s[n]) {
        const r = Object.assign(Object.assign({}, this._buildCustomStyleGeneric(t, e, n)), { "grid-area": n }),
              a = this._createCard(s[n]);this._cards.push(a), a.hass = this._hass, i = R`
          ${i}
          <div
            id=${n}
            class="ellipsis"
            @click=${this._stopPropagation}
            @touchstart=${this._stopPropagation}
            style=${it(r)}
          >
            ${a}
          </div>
        `;
      }
    }), i;
  }_isClickable(t) {
    let e = !0;const i = this._getTemplateOrValue(t, this._config.tap_action.action),
          n = this._getTemplateOrValue(t, this._config.hold_action.action),
          s = this._getTemplateOrValue(t, this._config.double_tap_action.action);return e = "none" != i || "none" != n || "none" != s, e;
  }_rotate(t) {
    return !(!t || !t.spin);
  }_blankCardColoredHtml(t) {
    const e = Object.assign({ background: "none", "box-shadow": "none" }, t);return R`
      <ha-card class="disabled" style=${it(e)}>
        <div></div>
      </ha-card>
    `;
  }_cardHtml() {
    const t = this._getMatchingConfigState(this._stateObj),
          e = this._buildCssColorAttribute(this._stateObj, t);let i = e,
        n = {},
        s = {};const r = {},
          a = this._buildStyleGeneric(this._stateObj, t, "lock"),
          o = this._buildStyleGeneric(this._stateObj, t, "card"),
          l = { "button-card-main": !0, disabled: !this._isClickable(this._stateObj) };switch (o.width && (this.style.setProperty("flex", "0 0 auto"), this.style.setProperty("max-width", "fit-content")), this._config.color_type) {case "blank-card":
        return this._blankCardColoredHtml(o);case "card":case "label-card":
        {
          const t = function (t) {
            const e = new _e(ve(t));return e.isValid && e.getLuminance() > .5 ? "rgb(62, 62, 62)" : "rgb(234, 234, 234)";
          }(e);n.color = t, s.color = t, n["background-color"] = e, n = Object.assign(Object.assign({}, n), o), i = "inherit";break;
        }default:
        n = o;}this._config.aspect_ratio ? (r["--aspect-ratio"] = this._config.aspect_ratio, n.position = "absolute") : r.display = "inline", this.style.setProperty("--button-card-light-color", this._getColorForLightEntity(this._stateObj, !0)), this.style.setProperty("--button-card-light-color-no-temperature", this._getColorForLightEntity(this._stateObj, !1)), s = Object.assign(Object.assign({}, s), a);const c = this._config.extra_styles ? R`
          <style>
            ${this._getTemplateOrValue(this._stateObj, this._config.extra_styles)}
          </style>
        ` : R``;return R`
      ${c}
      <div id="aspect-ratio" style=${it(r)}>
        <ha-card
          id="card"
          class=${ot(l)}
          style=${it(n)}
          @action=${this._handleAction}
          .actionHandler=${Xt({ hasDoubleClick: "none" !== this._config.double_tap_action.action, hasHold: "none" !== this._config.hold_action.action, repeat: this._config.hold_action.repeat })}
          .config="${this._config}"
        >
          ${this._buttonContent(this._stateObj, t, i)}
          ${this._config.lock && this._getTemplateOrValue(this._stateObj, this._config.lock.enabled) ? "" : R`
                <mwc-ripple id="ripple"></mwc-ripple>
              `}
        </ha-card>
      </div>
      ${this._getLock(s)}
    `;
  }_getLock(t) {
    return this._config.lock && this._getTemplateOrValue(this._stateObj, this._config.lock.enabled) ? R`
        <div
          id="overlay"
          style=${it(t)}
          @action=${this._handleUnlockType}
          .actionHandler=${Xt({ hasDoubleClick: "double_tap" === this._config.lock.unlock, hasHold: "hold" === this._config.lock.unlock })}
          .config="${this._config}"
        >
          <ha-icon id="lock" icon="mdi:lock-outline"></ha-icon>
        </div>
      ` : R``;
  }_buttonContent(t, e, i) {
    const n = this._buildName(t, e),
          s = this._config.show_state && this._config.state_display ? this._getTemplateOrValue(t, this._config.state_display) : void 0,
          r = s || this._buildStateString(t),
          a = function (t, e) {
      if (!t && !e) return;let i;return i = e ? t ? `${t}: ${e}` : e : t, i;
    }(n, r);switch (this._config.layout) {case "icon_name_state":case "name_state":
        return this._gridHtml(t, e, this._config.layout, i, a, void 0);default:
        return this._gridHtml(t, e, this._config.layout, i, n, r);}
  }_gridHtml(t, e, i, n, s, r) {
    const a = this._getIconHtml(t, e, n),
          o = [i],
          l = this._buildLabel(t, e),
          c = this._buildStyleGeneric(t, e, "name"),
          h = this._buildStyleGeneric(t, e, "state"),
          u = this._buildStyleGeneric(t, e, "label"),
          d = this._buildLastChanged(t, u),
          f = this._buildStyleGeneric(t, e, "grid");return a || o.push("no-icon"), s || o.push("no-name"), r || o.push("no-state"), l || d || o.push("no-label"), R`
      <div id="container" class=${o.join(" ")} style=${it(f)}>
        ${a || ""}
        ${s ? R`
              <div id="name" class="ellipsis" style=${it(c)}>
                ${"html" === s.type ? s : st(s)}
              </div>
            ` : ""}
        ${r ? R`
              <div id="state" class="ellipsis" style=${it(h)}>
                ${"html" === r.type ? r : st(r)}
              </div>
            ` : ""}
        ${l && !d ? R`
              <div id="label" class="ellipsis" style=${it(u)}>
                ${"html" === l.type ? l : st(l)}
              </div>
            ` : ""}
        ${d || ""} ${this._buildCustomFields(t, e)}
      </div>
    `;
  }_getIconHtml(t, e, i) {
    const n = this._buildIcon(t, e),
          s = this._buildEntityPicture(t, e),
          r = this._buildStyleGeneric(t, e, "entity_picture"),
          a = this._buildStyleGeneric(t, e, "icon"),
          o = this._buildStyleGeneric(t, e, "img_cell"),
          l = this._buildStyleGeneric(t, e, "card"),
          c = Object.assign({ color: i, width: this._config.size, position: this._config.aspect_ratio || l.height ? "absolute" : "relative" }, a),
          h = Object.assign(Object.assign({}, c), r),
          u = this._buildLiveStream(h);return n || s ? R`
        <div id="img-cell" style=${it(o)}>
          ${!n || s || u ? "" : R`
                <ha-icon
                  style=${it(c)}
                  .icon="${n}"
                  id="icon"
                  ?rotating=${this._rotate(e)}
                ></ha-icon>
              `}
          ${u || ""}
          ${s && !u ? R`
                <img
                  src="${s}"
                  style=${it(h)}
                  id="icon"
                  ?rotating=${this._rotate(e)}
                />
              ` : ""}
        </div>
      ` : void 0;
  }_buildLiveStream(t) {
    return this._config.show_live_stream && this._config.entity && "camera" === ye(this._config.entity) ? R`
        <hui-image
          .hass=${this._hass}
          .cameraImage=${this._config.entity}
          .entity=${this._config.entity}
          cameraView="live"
          style=${it(t)}
        ></hui-image>
      ` : void 0;
  }_configFromLLTemplates(t, e) {
    const i = e.template;if (!i) return e;let n,
        s = {};const r = i && Array.isArray(i) ? i : [i];return null == r || r.forEach(e => {
      if (!t.config.button_card_templates || !t.config.button_card_templates[e]) throw new Error(`Button-card template '${e}' is missing!`);const i = this._configFromLLTemplates(t, t.config.button_card_templates[e]);s = Se(s, i), n = xe(n, i.state);
    }), s = Se(s, e), s.state = xe(n, e.state), s;
  }setConfig(t) {
    if (!t) throw new Error("Invalid configuration");const e = function () {
      var t = document.querySelector("home-assistant");if (t = (t = (t = (t = (t = (t = (t = (t = t && t.shadowRoot) && t.querySelector("home-assistant-main")) && t.shadowRoot) && t.querySelector("app-drawer-layout partial-panel-resolver")) && t.shadowRoot || t) && t.querySelector("ha-panel-lovelace")) && t.shadowRoot) && t.querySelector("hui-root")) {
        var e = t.lovelace;return e.current_view = t.___curView, e;
      }return null;
    }() || function () {
      let t = document.querySelector("hc-main");if (t = t && t.shadowRoot, t = t && t.querySelector("hc-lovelace"), t = t && t.shadowRoot, t = t && (t.querySelector("hui-view") || t.querySelector("hui-panel-view")), t) {
        const e = t.lovelace;return e.current_view = t.___curView, e;
      }return null;
    }();let i = JSON.parse(JSON.stringify(t));i = this._configFromLLTemplates(e, i), this._config = Object.assign({ hold_action: { action: "none" }, double_tap_action: { action: "none" }, layout: "vertical", size: "40%", color_type: "icon", show_name: !0, show_state: !1, show_icon: !0, show_units: !0, show_label: !1, show_entity_picture: !1, show_live_stream: !1 }, i), this._config.entity && Ht.has(ye(this._config.entity)) ? this._config = Object.assign({ tap_action: { action: "toggle" } }, this._config) : this._config = Object.assign({ tap_action: { action: "more-info" } }, this._config), this._config.lock = Object.assign({ enabled: !1, duration: 5, unlock: "tap" }, this._config.lock), this._config.default_color = "var(--primary-text-color)", "icon" !== this._config.color_type ? this._config.color_off = "var(--paper-card-background-color)" : this._config.color_off = "var(--paper-item-icon-color)", this._config.color_on = "var(--paper-item-icon-active-color)";const n = JSON.stringify(this._config);if (this._entities = [], Array.isArray(this._config.triggers_update) ? this._entities = [...this._config.triggers_update] : "string" == typeof this._config.triggers_update && "all" !== this._config.triggers_update && this._entities.push(this._config.triggers_update), "all" !== this._config.triggers_update) {
      const t = new RegExp(/states\[\s*('|\\")([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)\1\s*\]/, "gm"),
            e = new RegExp(/states\[\s*('|\\")([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)\1\s*\]/, "m"),
            i = n.match(t);null == i || i.forEach(t => {
        const i = t.match(e);i && !this._entities.includes(i[2]) && this._entities.push(i[2]);
      });
    }this._config.entity && !this._entities.includes(this._config.entity) && this._entities.push(this._config.entity);const s = new RegExp("\\[\\[\\[.*\\]\\]\\]", "gm");this._hasTemplate = !("all" !== this._config.triggers_update || !n.match(s));
  }getCardSize() {
    return 3;
  }_evalActions(t, e) {
    const i = JSON.parse(JSON.stringify(t)),
          n = t => t ? (Object.keys(t).forEach(e => {
      "object" == typeof t[e] ? t[e] = n(t[e]) : t[e] = this._getTemplateOrValue(this._stateObj, t[e]);
    }), t) : t;return i[e] = n(i[e]), !i[e].confirmation && i.confirmation && (i[e].confirmation = n(i.confirmation)), i;
  }_handleAction(t) {
    if (t.detail && t.detail.action) switch (t.detail.action) {case "tap":
        this._handleTap(t);break;case "hold":
        this._handleHold(t);break;case "double_tap":
        this._handleDblTap(t);}
  }_handleTap(t) {
    const e = t.target.config;e && zt(this, this._hass, this._evalActions(e, "tap_action"), !1, !1);
  }_handleHold(t) {
    const e = t.target.config;e && zt(this, this._hass, this._evalActions(e, "hold_action"), !0, !1);
  }_handleDblTap(t) {
    const e = t.target.config;e && zt(this, this._hass, this._evalActions(e, "double_tap_action"), !1, !0);
  }_handleUnlockType(t) {
    const e = t.target.config;e && e.lock.unlock === t.detail.action && this._handleLock();
  }_handleLock() {
    const t = this.shadowRoot.getElementById("lock");if (!t) return;if (this._config.lock.exemptions) {
      if (!this._hass.user.name || !this._hass.user.id) return;let e = !1;if (this._config.lock.exemptions.forEach(t => {
        (!e && t.user === this._hass.user.id || t.username === this._hass.user.name) && (e = !0);
      }), !e) return t.classList.add("invalid"), void window.setTimeout(() => {
        t && t.classList.remove("invalid");
      }, 3e3);
    }const e = this.shadowRoot.getElementById("overlay"),
          i = this.shadowRoot.getElementById("card");e.style.setProperty("pointer-events", "none");const n = document.createElement("paper-ripple");if (t) {
      i.appendChild(n);const e = document.createAttribute("icon");e.value = "mdi:lock-open-outline", t.attributes.setNamedItem(e), t.classList.add("hidden");
    }window.setTimeout(() => {
      if (e.style.setProperty("pointer-events", ""), t) {
        t.classList.remove("hidden");const e = document.createAttribute("icon");e.value = "mdi:lock-outline", t.attributes.setNamedItem(e), i.removeChild(n);
      }
    }, 1e3 * this._config.lock.duration);
  }_stopPropagation(t) {
    t.stopPropagation();
  }
};var Ce;t([G()], Oe.prototype, "_hass", void 0), t([G()], Oe.prototype, "_config", void 0), t([G()], Oe.prototype, "_timeRemaining", void 0), Oe = t([(Ce = "button-card", t => "function" == typeof t ? ((t, e) => (window.customElements.define(t, e), e))(Ce, t) : ((t, e) => {
  const { kind: i, elements: n } = e;return { kind: i, elements: n, finisher(e) {
      window.customElements.define(t, e);
    } };
})(Ce, t))], Oe);
