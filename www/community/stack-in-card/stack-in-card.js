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
function t(t, e, n, s) {
  var i,
      r = arguments.length,
      o = r < 3 ? e : null === s ? s = Object.getOwnPropertyDescriptor(e, n) : s;if ("object" == typeof Reflect && "function" == typeof Reflect.decorate) o = Reflect.decorate(t, e, n, s);else for (var a = t.length - 1; a >= 0; a--) (i = t[a]) && (o = (r < 3 ? i(o) : r > 3 ? i(e, n, o) : i(e, n)) || o);return r > 3 && o && Object.defineProperty(e, n, o), o;
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
      n = (t, e, n = null) => {
  for (; e !== n;) {
    const n = e.nextSibling;t.removeChild(e), e = n;
  }
},
      s = `{{lit-${String(Math.random()).slice(2)}}}`,
      i = `\x3c!--${s}--\x3e`,
      r = new RegExp(`${s}|${i}`);class o {
  constructor(t, e) {
    this.parts = [], this.element = e;const n = [],
          i = [],
          o = document.createTreeWalker(e.content, 133, null, !1);let l = 0,
        u = -1,
        h = 0;const { strings: p, values: { length: m } } = t;for (; h < m;) {
      const t = o.nextNode();if (null !== t) {
        if (u++, 1 === t.nodeType) {
          if (t.hasAttributes()) {
            const e = t.attributes,
                  { length: n } = e;let s = 0;for (let t = 0; t < n; t++) a(e[t].name, "$lit$") && s++;for (; s-- > 0;) {
              const e = p[h],
                    n = c.exec(e)[2],
                    s = n.toLowerCase() + "$lit$",
                    i = t.getAttribute(s);t.removeAttribute(s);const o = i.split(r);this.parts.push({ type: "attribute", index: u, name: n, strings: o }), h += o.length - 1;
            }
          }"TEMPLATE" === t.tagName && (i.push(t), o.currentNode = t.content);
        } else if (3 === t.nodeType) {
          const e = t.data;if (e.indexOf(s) >= 0) {
            const s = t.parentNode,
                  i = e.split(r),
                  o = i.length - 1;for (let e = 0; e < o; e++) {
              let n,
                  r = i[e];if ("" === r) n = d();else {
                const t = c.exec(r);null !== t && a(t[2], "$lit$") && (r = r.slice(0, t.index) + t[1] + t[2].slice(0, -"$lit$".length) + t[3]), n = document.createTextNode(r);
              }s.insertBefore(n, t), this.parts.push({ type: "node", index: ++u });
            }"" === i[o] ? (s.insertBefore(d(), t), n.push(t)) : t.data = i[o], h += o;
          }
        } else if (8 === t.nodeType) if (t.data === s) {
          const e = t.parentNode;null !== t.previousSibling && u !== l || (u++, e.insertBefore(d(), t)), l = u, this.parts.push({ type: "node", index: u }), null === t.nextSibling ? t.data = "" : (n.push(t), u--), h++;
        } else {
          let e = -1;for (; -1 !== (e = t.data.indexOf(s, e + 1));) this.parts.push({ type: "node", index: -1 }), h++;
        }
      } else o.currentNode = i.pop();
    }for (const t of n) t.parentNode.removeChild(t);
  }
}const a = (t, e) => {
  const n = t.length - e.length;return n >= 0 && t.slice(n) === e;
},
      l = t => -1 !== t.index,
      d = () => document.createComment(""),
      c = /([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/;function u(t, e) {
  const { element: { content: n }, parts: s } = t,
        i = document.createTreeWalker(n, 133, null, !1);let r = p(s),
      o = s[r],
      a = -1,
      l = 0;const d = [];let c = null;for (; i.nextNode();) {
    a++;const t = i.currentNode;for (t.previousSibling === c && (c = null), e.has(t) && (d.push(t), null === c && (c = t)), null !== c && l++; void 0 !== o && o.index === a;) o.index = null !== c ? -1 : o.index - l, r = p(s, r), o = s[r];
  }d.forEach(t => t.parentNode.removeChild(t));
}const h = t => {
  let e = 11 === t.nodeType ? 0 : 1;const n = document.createTreeWalker(t, 133, null, !1);for (; n.nextNode();) e++;return e;
},
      p = (t, e = -1) => {
  for (let n = e + 1; n < t.length; n++) {
    const e = t[n];if (l(e)) return n;
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
const m = new WeakMap(),
      f = t => "function" == typeof t && m.has(t),
      g = {},
      _ = {};
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
  constructor(t, e, n) {
    this.__parts = [], this.template = t, this.processor = e, this.options = n;
  }update(t) {
    let e = 0;for (const n of this.__parts) void 0 !== n && n.setValue(t[e]), e++;for (const t of this.__parts) void 0 !== t && t.commit();
  }_clone() {
    const t = e ? this.template.element.content.cloneNode(!0) : document.importNode(this.template.element.content, !0),
          n = [],
          s = this.template.parts,
          i = document.createTreeWalker(t, 133, null, !1);let r,
        o = 0,
        a = 0,
        d = i.nextNode();for (; o < s.length;) if (r = s[o], l(r)) {
      for (; a < r.index;) a++, "TEMPLATE" === d.nodeName && (n.push(d), i.currentNode = d.content), null === (d = i.nextNode()) && (i.currentNode = n.pop(), d = i.nextNode());if ("node" === r.type) {
        const t = this.processor.handleTextExpression(this.options);t.insertAfterNode(d.previousSibling), this.__parts.push(t);
      } else this.__parts.push(...this.processor.handleAttributeExpressions(d, r.name, r.strings, this.options));o++;
    } else this.__parts.push(void 0), o++;return e && (document.adoptNode(t), customElements.upgrade(t)), t;
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
 */const v = ` ${s} `;class S {
  constructor(t, e, n, s) {
    this.strings = t, this.values = e, this.type = n, this.processor = s;
  }getHTML() {
    const t = this.strings.length - 1;let e = "",
        n = !1;for (let r = 0; r < t; r++) {
      const t = this.strings[r],
            o = t.lastIndexOf("\x3c!--");n = (o > -1 || n) && -1 === t.indexOf("--\x3e", o + 1);const a = c.exec(t);e += null === a ? t + (n ? v : i) : t.substr(0, a.index) + a[1] + a[2] + "$lit$" + a[3] + s;
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
 */const w = t => null === t || !("object" == typeof t || "function" == typeof t),
      b = t => Array.isArray(t) || !(!t || !t[Symbol.iterator]);class C {
  constructor(t, e, n) {
    this.dirty = !0, this.element = t, this.name = e, this.strings = n, this.parts = [];for (let t = 0; t < n.length - 1; t++) this.parts[t] = this._createPart();
  }_createPart() {
    return new x(this);
  }_getValue() {
    const t = this.strings,
          e = t.length - 1;let n = "";for (let s = 0; s < e; s++) {
      n += t[s];const e = this.parts[s];if (void 0 !== e) {
        const t = e.value;if (w(t) || !b(t)) n += "string" == typeof t ? t : String(t);else for (const e of t) n += "string" == typeof e ? e : String(e);
      }
    }return n += t[e], n;
  }commit() {
    this.dirty && (this.dirty = !1, this.element.setAttribute(this.name, this._getValue()));
  }
}class x {
  constructor(t) {
    this.value = void 0, this.committer = t;
  }setValue(t) {
    t === g || w(t) && t === this.value || (this.value = t, f(t) || (this.committer.dirty = !0));
  }commit() {
    for (; f(this.value);) {
      const t = this.value;this.value = g, t(this);
    }this.value !== g && this.committer.commit();
  }
}class P {
  constructor(t) {
    this.value = void 0, this.__pendingValue = void 0, this.options = t;
  }appendInto(t) {
    this.startNode = t.appendChild(d()), this.endNode = t.appendChild(d());
  }insertAfterNode(t) {
    this.startNode = t, this.endNode = t.nextSibling;
  }appendIntoPart(t) {
    t.__insert(this.startNode = d()), t.__insert(this.endNode = d());
  }insertAfterPart(t) {
    t.__insert(this.startNode = d()), this.endNode = t.endNode, t.endNode = this.startNode;
  }setValue(t) {
    this.__pendingValue = t;
  }commit() {
    if (null === this.startNode.parentNode) return;for (; f(this.__pendingValue);) {
      const t = this.__pendingValue;this.__pendingValue = g, t(this);
    }const t = this.__pendingValue;t !== g && (w(t) ? t !== this.value && this.__commitText(t) : t instanceof S ? this.__commitTemplateResult(t) : t instanceof Node ? this.__commitNode(t) : b(t) ? this.__commitIterable(t) : t === _ ? (this.value = _, this.clear()) : this.__commitText(t));
  }__insert(t) {
    this.endNode.parentNode.insertBefore(t, this.endNode);
  }__commitNode(t) {
    this.value !== t && (this.clear(), this.__insert(t), this.value = t);
  }__commitText(t) {
    const e = this.startNode.nextSibling,
          n = "string" == typeof (t = null == t ? "" : t) ? t : String(t);e === this.endNode.previousSibling && 3 === e.nodeType ? e.data = n : this.__commitNode(document.createTextNode(n)), this.value = t;
  }__commitTemplateResult(t) {
    const e = this.options.templateFactory(t);if (this.value instanceof y && this.value.template === e) this.value.update(t.values);else {
      const n = new y(e, t.processor, this.options),
            s = n._clone();n.update(t.values), this.__commitNode(s), this.value = n;
    }
  }__commitIterable(t) {
    Array.isArray(this.value) || (this.value = [], this.clear());const e = this.value;let n,
        s = 0;for (const i of t) n = e[s], void 0 === n && (n = new P(this.options), e.push(n), 0 === s ? n.appendIntoPart(this) : n.insertAfterPart(e[s - 1])), n.setValue(i), n.commit(), s++;s < e.length && (e.length = s, this.clear(n && n.endNode));
  }clear(t = this.startNode) {
    n(this.startNode.parentNode, t.nextSibling, this.endNode);
  }
}class N {
  constructor(t, e, n) {
    if (this.value = void 0, this.__pendingValue = void 0, 2 !== n.length || "" !== n[0] || "" !== n[1]) throw new Error("Boolean attributes can only contain a single expression");this.element = t, this.name = e, this.strings = n;
  }setValue(t) {
    this.__pendingValue = t;
  }commit() {
    for (; f(this.__pendingValue);) {
      const t = this.__pendingValue;this.__pendingValue = g, t(this);
    }if (this.__pendingValue === g) return;const t = !!this.__pendingValue;this.value !== t && (t ? this.element.setAttribute(this.name, "") : this.element.removeAttribute(this.name), this.value = t), this.__pendingValue = g;
  }
}class M extends C {
  constructor(t, e, n) {
    super(t, e, n), this.single = 2 === n.length && "" === n[0] && "" === n[1];
  }_createPart() {
    return new T(this);
  }_getValue() {
    return this.single ? this.parts[0].value : super._getValue();
  }commit() {
    this.dirty && (this.dirty = !1, this.element[this.name] = this._getValue());
  }
}class T extends x {}let E = !1;(() => {
  try {
    const t = { get capture() {
        return E = !0, !1;
      } };window.addEventListener("test", t, t), window.removeEventListener("test", t, t);
  } catch (t) {}
})();class k {
  constructor(t, e, n) {
    this.value = void 0, this.__pendingValue = void 0, this.element = t, this.eventName = e, this.eventContext = n, this.__boundHandleEvent = t => this.handleEvent(t);
  }setValue(t) {
    this.__pendingValue = t;
  }commit() {
    for (; f(this.__pendingValue);) {
      const t = this.__pendingValue;this.__pendingValue = g, t(this);
    }if (this.__pendingValue === g) return;const t = this.__pendingValue,
          e = this.value,
          n = null == t || null != e && (t.capture !== e.capture || t.once !== e.once || t.passive !== e.passive),
          s = null != t && (null == e || n);n && this.element.removeEventListener(this.eventName, this.__boundHandleEvent, this.__options), s && (this.__options = A(t), this.element.addEventListener(this.eventName, this.__boundHandleEvent, this.__options)), this.value = t, this.__pendingValue = g;
  }handleEvent(t) {
    "function" == typeof this.value ? this.value.call(this.eventContext || this.element, t) : this.value.handleEvent(t);
  }
}const A = t => t && (E ? { capture: t.capture, passive: t.passive, once: t.once } : t.capture)
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
 */;function D(t) {
  let e = V.get(t.type);void 0 === e && (e = { stringsArray: new WeakMap(), keyString: new Map() }, V.set(t.type, e));let n = e.stringsArray.get(t.strings);if (void 0 !== n) return n;const i = t.strings.join(s);return n = e.keyString.get(i), void 0 === n && (n = new o(t, t.getTemplateElement()), e.keyString.set(i, n)), e.stringsArray.set(t.strings, n), n;
}const V = new Map(),
      O = new WeakMap();
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
 */const R = new
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
  handleAttributeExpressions(t, e, n, s) {
    const i = e[0];if ("." === i) {
      return new M(t, e.slice(1), n).parts;
    }return "@" === i ? [new k(t, e.slice(1), s.eventContext)] : "?" === i ? [new N(t, e.slice(1), n)] : new C(t, e, n).parts;
  }handleTextExpression(t) {
    return new P(t);
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
 */"undefined" != typeof window && (window.litHtmlVersions || (window.litHtmlVersions = [])).push("1.2.1");const Y = (t, ...e) => new S(t, e, "html", R)
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
      U = (t, e) => `${t}--${e}`;let H = !0;void 0 === window.ShadyCSS ? H = !1 : void 0 === window.ShadyCSS.prepareTemplateDom && (console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."), H = !1);const j = t => e => {
  const n = U(e.type, t);let i = V.get(n);void 0 === i && (i = { stringsArray: new WeakMap(), keyString: new Map() }, V.set(n, i));let r = i.stringsArray.get(e.strings);if (void 0 !== r) return r;const a = e.strings.join(s);if (r = i.keyString.get(a), void 0 === r) {
    const n = e.getTemplateElement();H && window.ShadyCSS.prepareTemplateDom(n, t), r = new o(e, n), i.keyString.set(a, r);
  }return i.stringsArray.set(e.strings, r), r;
},
      F = ["html", "svg"],
      $ = new Set(),
      z = (t, e, n) => {
  $.add(t);const s = n ? n.element : document.createElement("template"),
        i = e.querySelectorAll("style"),
        { length: r } = i;if (0 === r) return void window.ShadyCSS.prepareTemplateStyles(s, t);const o = document.createElement("style");for (let t = 0; t < r; t++) {
    const e = i[t];e.parentNode.removeChild(e), o.textContent += e.textContent;
  }(t => {
    F.forEach(e => {
      const n = V.get(U(e, t));void 0 !== n && n.keyString.forEach(t => {
        const { element: { content: e } } = t,
              n = new Set();Array.from(e.querySelectorAll("style")).forEach(t => {
          n.add(t);
        }), u(t, n);
      });
    });
  })(t);const a = s.content;n ? function (t, e, n = null) {
    const { element: { content: s }, parts: i } = t;if (null == n) return void s.appendChild(e);const r = document.createTreeWalker(s, 133, null, !1);let o = p(i),
        a = 0,
        l = -1;for (; r.nextNode();) {
      for (l++, r.currentNode === n && (a = h(e), n.parentNode.insertBefore(e, n)); -1 !== o && i[o].index === l;) {
        if (a > 0) {
          for (; -1 !== o;) i[o].index += a, o = p(i, o);return;
        }o = p(i, o);
      }
    }
  }(n, o, a.firstChild) : a.insertBefore(o, a.firstChild), window.ShadyCSS.prepareTemplateStyles(s, t);const l = a.querySelector("style");if (window.ShadyCSS.nativeShadow && null !== l) e.insertBefore(l.cloneNode(!0), e.firstChild);else if (n) {
    a.insertBefore(o, a.firstChild);const t = new Set();t.add(o), u(n, t);
  }
};window.JSCompiler_renameProperty = (t, e) => t;const I = { toAttribute(t, e) {
    switch (e) {case Boolean:
        return t ? "" : null;case Object:case Array:
        return null == t ? t : JSON.stringify(t);}return t;
  }, fromAttribute(t, e) {
    switch (e) {case Boolean:
        return null !== t;case Number:
        return null === t ? null : Number(t);case Object:case Array:
        return JSON.parse(t);}return t;
  } },
      q = (t, e) => e !== t && (e == e || t == t),
      L = { attribute: !0, type: String, converter: I, reflect: !1, hasChanged: q };class B extends HTMLElement {
  constructor() {
    super(), this._updateState = 0, this._instanceProperties = void 0, this._updatePromise = new Promise(t => this._enableUpdatingResolver = t), this._changedProperties = new Map(), this._reflectingProperties = void 0, this.initialize();
  }static get observedAttributes() {
    this.finalize();const t = [];return this._classProperties.forEach((e, n) => {
      const s = this._attributeNameForProperty(n, e);void 0 !== s && (this._attributeToPropertyMap.set(s, n), t.push(s));
    }), t;
  }static _ensureClassProperties() {
    if (!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties", this))) {
      this._classProperties = new Map();const t = Object.getPrototypeOf(this)._classProperties;void 0 !== t && t.forEach((t, e) => this._classProperties.set(e, t));
    }
  }static createProperty(t, e = L) {
    if (this._ensureClassProperties(), this._classProperties.set(t, e), e.noAccessor || this.prototype.hasOwnProperty(t)) return;const n = "symbol" == typeof t ? Symbol() : `__${t}`,
          s = this.getPropertyDescriptor(t, n, e);void 0 !== s && Object.defineProperty(this.prototype, t, s);
  }static getPropertyDescriptor(t, e, n) {
    return { get() {
        return this[e];
      }, set(n) {
        const s = this[t];this[e] = n, this._requestUpdate(t, s);
      }, configurable: !0, enumerable: !0 };
  }static getPropertyOptions(t) {
    return this._classProperties && this._classProperties.get(t) || L;
  }static finalize() {
    const t = Object.getPrototypeOf(this);if (t.hasOwnProperty("finalized") || t.finalize(), this.finalized = !0, this._ensureClassProperties(), this._attributeToPropertyMap = new Map(), this.hasOwnProperty(JSCompiler_renameProperty("properties", this))) {
      const t = this.properties,
            e = [...Object.getOwnPropertyNames(t), ...("function" == typeof Object.getOwnPropertySymbols ? Object.getOwnPropertySymbols(t) : [])];for (const n of e) this.createProperty(n, t[n]);
    }
  }static _attributeNameForProperty(t, e) {
    const n = e.attribute;return !1 === n ? void 0 : "string" == typeof n ? n : "string" == typeof t ? t.toLowerCase() : void 0;
  }static _valueHasChanged(t, e, n = q) {
    return n(t, e);
  }static _propertyValueFromAttribute(t, e) {
    const n = e.type,
          s = e.converter || I,
          i = "function" == typeof s ? s : s.fromAttribute;return i ? i(t, n) : t;
  }static _propertyValueToAttribute(t, e) {
    if (void 0 === e.reflect) return;const n = e.type,
          s = e.converter;return (s && s.toAttribute || I.toAttribute)(t, n);
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
  }disconnectedCallback() {}attributeChangedCallback(t, e, n) {
    e !== n && this._attributeToProperty(t, n);
  }_propertyToAttribute(t, e, n = L) {
    const s = this.constructor,
          i = s._attributeNameForProperty(t, n);if (void 0 !== i) {
      const t = s._propertyValueToAttribute(e, n);if (void 0 === t) return;this._updateState = 8 | this._updateState, null == t ? this.removeAttribute(i) : this.setAttribute(i, t), this._updateState = -9 & this._updateState;
    }
  }_attributeToProperty(t, e) {
    if (8 & this._updateState) return;const n = this.constructor,
          s = n._attributeToPropertyMap.get(t);if (void 0 !== s) {
      const t = n.getPropertyOptions(s);this._updateState = 16 | this._updateState, this[s] = n._propertyValueFromAttribute(e, t), this._updateState = -17 & this._updateState;
    }
  }_requestUpdate(t, e) {
    let n = !0;if (void 0 !== t) {
      const s = this.constructor,
            i = s.getPropertyOptions(t);s._valueHasChanged(this[t], e, i.hasChanged) ? (this._changedProperties.has(t) || this._changedProperties.set(t, e), !0 !== i.reflect || 16 & this._updateState || (void 0 === this._reflectingProperties && (this._reflectingProperties = new Map()), this._reflectingProperties.set(t, i))) : n = !1;
    }!this._hasRequestedUpdate && n && (this._updatePromise = this._enqueueUpdate());
  }requestUpdate(t, e) {
    return this._requestUpdate(t, e), this.updateComplete;
  }async _enqueueUpdate() {
    this._updateState = 4 | this._updateState;try {
      await this._updatePromise;
    } catch (t) {}const t = this.performUpdate();return null != t && (await t), !this._hasRequestedUpdate;
  }get _hasRequestedUpdate() {
    return 4 & this._updateState;
  }get hasUpdated() {
    return 1 & this._updateState;
  }performUpdate() {
    this._instanceProperties && this._applyInstanceProperties();let t = !1;const e = this._changedProperties;try {
      t = this.shouldUpdate(e), t ? this.update(e) : this._markUpdated();
    } catch (e) {
      throw t = !1, this._markUpdated(), e;
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
}B.finalized = !0;
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
const W = (t, e) => "method" === e.kind && e.descriptor && !("value" in e.descriptor) ? Object.assign(Object.assign({}, e), { finisher(n) {
    n.createProperty(e.key, t);
  } }) : { kind: "field", key: Symbol(), placement: "own", descriptor: {}, initializer() {
    "function" == typeof e.initializer && (this[e.key] = e.initializer.call(this));
  }, finisher(n) {
    n.createProperty(e.key, t);
  } };function J(t) {
  return (e, n) => void 0 !== n ? ((t, e, n) => {
    e.constructor.createProperty(n, t);
  })(t, e, n) : W(t, e);
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
      K = Symbol();class G {
  constructor(t, e) {
    if (e !== K) throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText = t;
  }get styleSheet() {
    return void 0 === this._styleSheet && (Z ? (this._styleSheet = new CSSStyleSheet(), this._styleSheet.replaceSync(this.cssText)) : this._styleSheet = null), this._styleSheet;
  }toString() {
    return this.cssText;
  }
}const Q = (t, ...e) => {
  const n = e.reduce((e, n, s) => e + (t => {
    if (t instanceof G) return t.cssText;if ("number" == typeof t) return t;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${t}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`);
  })(n) + t[s + 1], t[0]);return new G(n, K);
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
(window.litElementVersions || (window.litElementVersions = [])).push("2.3.1");const X = {};class tt extends B {
  static getStyles() {
    return this.styles;
  }static _getUniqueStyles() {
    if (this.hasOwnProperty(JSCompiler_renameProperty("_styles", this))) return;const t = this.getStyles();if (void 0 === t) this._styles = [];else if (Array.isArray(t)) {
      const e = (t, n) => t.reduceRight((t, n) => Array.isArray(n) ? e(n, t) : (t.add(n), t), n),
            n = e(t, new Set()),
            s = [];n.forEach(t => s.unshift(t)), this._styles = s;
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
    const e = this.render();super.update(t), e !== X && this.constructor.render(e, this.renderRoot, { scopeName: this.localName, eventContext: this }), this._needsShimAdoptedStyleSheets && (this._needsShimAdoptedStyleSheets = !1, this.constructor._styles.forEach(t => {
      const e = document.createElement("style");e.textContent = t.cssText, this.renderRoot.appendChild(e);
    }));
  }render() {
    return X;
  }
}tt.finalized = !0, tt.render = (t, e, s) => {
  if (!s || "object" != typeof s || !s.scopeName) throw new Error("The `scopeName` option is required.");const i = s.scopeName,
        r = O.has(e),
        o = H && 11 === e.nodeType && !!e.host,
        a = o && !$.has(i),
        l = a ? document.createDocumentFragment() : e;if (((t, e, s) => {
    let i = O.get(e);void 0 === i && (n(e, e.firstChild), O.set(e, i = new P(Object.assign({ templateFactory: D }, s))), i.appendInto(e)), i.setValue(t), i.commit();
  })(t, l, Object.assign({ templateFactory: j(i) }, s)), a) {
    const t = O.get(l);O.delete(l);const s = t.value instanceof y ? t.value.template : void 0;z(i, l, s), n(e, e.firstChild), e.appendChild(l), O.set(e, t);
  }!r && o && window.ShadyCSS.styleElement(e.host);
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
      nt = (st = t => e => {
  const n = et.get(e);if (void 0 === t && e instanceof x) {
    if (void 0 !== n || !et.has(e)) {
      const t = e.committer.name;e.committer.element.removeAttribute(t);
    }
  } else t !== n && e.setValue(t);et.set(e, t);
}, (...t) => {
  const e = st(...t);return m.set(e, !0), e;
});var st,
    it = /d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,
    rt = "[^\\s]+",
    ot = /\[([^]*?)\]/gm;function at(t, e) {
  for (var n = [], s = 0, i = t.length; s < i; s++) n.push(t[s].substr(0, e));return n;
}var lt = function (t) {
  return function (e, n) {
    var s = n[t].map(function (t) {
      return t.toLowerCase();
    }).indexOf(e.toLowerCase());return s > -1 ? s : null;
  };
};function dt(t) {
  for (var e = [], n = 1; n < arguments.length; n++) e[n - 1] = arguments[n];for (var s = 0, i = e; s < i.length; s++) {
    var r = i[s];for (var o in r) t[o] = r[o];
  }return t;
}var ct = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    ut = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    ht = at(ut, 3),
    pt = { dayNamesShort: at(ct, 3), dayNames: ct, monthNamesShort: ht, monthNames: ut, amPm: ["am", "pm"], DoFn: function (t) {
    return t + ["th", "st", "nd", "rd"][t % 10 > 3 ? 0 : (t - t % 10 != 10 ? 1 : 0) * t % 10];
  } },
    mt = dt({}, pt),
    ft = function (t, e) {
  for (void 0 === e && (e = 2), t = String(t); t.length < e;) t = "0" + t;return t;
},
    gt = { D: function (t) {
    return String(t.getDate());
  }, DD: function (t) {
    return ft(t.getDate());
  }, Do: function (t, e) {
    return e.DoFn(t.getDate());
  }, d: function (t) {
    return String(t.getDay());
  }, dd: function (t) {
    return ft(t.getDay());
  }, ddd: function (t, e) {
    return e.dayNamesShort[t.getDay()];
  }, dddd: function (t, e) {
    return e.dayNames[t.getDay()];
  }, M: function (t) {
    return String(t.getMonth() + 1);
  }, MM: function (t) {
    return ft(t.getMonth() + 1);
  }, MMM: function (t, e) {
    return e.monthNamesShort[t.getMonth()];
  }, MMMM: function (t, e) {
    return e.monthNames[t.getMonth()];
  }, YY: function (t) {
    return ft(String(t.getFullYear()), 4).substr(2);
  }, YYYY: function (t) {
    return ft(t.getFullYear(), 4);
  }, h: function (t) {
    return String(t.getHours() % 12 || 12);
  }, hh: function (t) {
    return ft(t.getHours() % 12 || 12);
  }, H: function (t) {
    return String(t.getHours());
  }, HH: function (t) {
    return ft(t.getHours());
  }, m: function (t) {
    return String(t.getMinutes());
  }, mm: function (t) {
    return ft(t.getMinutes());
  }, s: function (t) {
    return String(t.getSeconds());
  }, ss: function (t) {
    return ft(t.getSeconds());
  }, S: function (t) {
    return String(Math.round(t.getMilliseconds() / 100));
  }, SS: function (t) {
    return ft(Math.round(t.getMilliseconds() / 10), 2);
  }, SSS: function (t) {
    return ft(t.getMilliseconds(), 3);
  }, a: function (t, e) {
    return t.getHours() < 12 ? e.amPm[0] : e.amPm[1];
  }, A: function (t, e) {
    return t.getHours() < 12 ? e.amPm[0].toUpperCase() : e.amPm[1].toUpperCase();
  }, ZZ: function (t) {
    var e = t.getTimezoneOffset();return (e > 0 ? "-" : "+") + ft(100 * Math.floor(Math.abs(e) / 60) + Math.abs(e) % 60, 4);
  }, Z: function (t) {
    var e = t.getTimezoneOffset();return (e > 0 ? "-" : "+") + ft(Math.floor(Math.abs(e) / 60), 2) + ":" + ft(Math.abs(e) % 60, 2);
  } },
    _t = function (t) {
  return +t - 1;
},
    yt = [null, "[1-9]\\d?"],
    vt = [null, rt],
    St = ["isPm", rt, function (t, e) {
  var n = t.toLowerCase();return n === e.amPm[0] ? 0 : n === e.amPm[1] ? 1 : null;
}],
    wt = ["timezoneOffset", "[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?", function (t) {
  var e = (t + "").match(/([+-]|\d\d)/gi);if (e) {
    var n = 60 * +e[1] + parseInt(e[2], 10);return "+" === e[0] ? n : -n;
  }return 0;
}],
    bt = (lt("monthNamesShort"), lt("monthNames"), { default: "ddd MMM DD YYYY HH:mm:ss", shortDate: "M/D/YY", mediumDate: "MMM D, YYYY", longDate: "MMMM D, YYYY", fullDate: "dddd, MMMM D, YYYY", isoDate: "YYYY-MM-DD", isoDateTime: "YYYY-MM-DDTHH:mm:ssZ", shortTime: "HH:mm", mediumTime: "HH:mm:ss", longTime: "HH:mm:ss.SSS" });var Ct = function (t, e, n) {
  if (void 0 === e && (e = bt.default), void 0 === n && (n = {}), "number" == typeof t && (t = new Date(t)), "[object Date]" !== Object.prototype.toString.call(t) || isNaN(t.getTime())) throw new Error("Invalid Date pass to format");var s = [];e = (e = bt[e] || e).replace(ot, function (t, e) {
    return s.push(e), "@@@";
  });var i = dt(dt({}, mt), n);return (e = e.replace(it, function (e) {
    return gt[e](t, i);
  })).replace(/@@@/g, function () {
    return s.shift();
  });
},
    xt = (function () {
  try {
    new Date().toLocaleDateString("i");
  } catch (t) {
    return "RangeError" === t.name;
  }
}(), function () {
  try {
    new Date().toLocaleString("i");
  } catch (t) {
    return "RangeError" === t.name;
  }
}(), function () {
  try {
    new Date().toLocaleTimeString("i");
  } catch (t) {
    return "RangeError" === t.name;
  }
}(), new Set(["call-service", "divider", "section", "weblink", "cast", "select"])),
    Pt = { alert: "toggle", automation: "toggle", climate: "climate", cover: "cover", fan: "toggle", group: "group", input_boolean: "toggle", input_number: "input-number", input_select: "input-select", input_text: "input-text", light: "toggle", lock: "lock", media_player: "media-player", remote: "toggle", scene: "scene", script: "script", sensor: "sensor", timer: "timer", switch: "toggle", vacuum: "toggle", water_heater: "climate", input_datetime: "input-datetime" },
    Nt = function (t, e) {
  void 0 === e && (e = !1);var n = function (t, e) {
    return s("hui-error-card", { type: "error", error: t, config: e });
  },
      s = function (t, e) {
    var s = window.document.createElement(t);try {
      s.setConfig(e);
    } catch (s) {
      return console.error(t, s), n(s.message, e);
    }return s;
  };if (!t || "object" != typeof t || !e && !t.type) return n("No type defined", t);var i = t.type;if (i && i.startsWith("custom:")) i = i.substr("custom:".length);else if (e) {
    if (xt.has(i)) i = "hui-" + i + "-row";else {
      if (!t.entity) return n("Invalid config given.", t);var r = t.entity.split(".", 1)[0];i = "hui-" + (Pt[r] || "text") + "-entity-row";
    }
  } else i = "hui-" + i + "-card";if (customElements.get(i)) return s(i, t);var o = n("Custom element doesn't exist: " + t.type + ".", t);o.style.display = "None";var a = setTimeout(function () {
    o.style.display = "";
  }, 2e3);return customElements.whenDefined(t.type).then(function () {
    clearTimeout(a), function (t, e, n, s) {
      s = s || {}, n = null == n ? {} : n;var i = new Event(e, { bubbles: void 0 === s.bubbles || s.bubbles, cancelable: Boolean(s.cancelable), composed: void 0 === s.composed || s.composed });i.detail = n, t.dispatchEvent(i);
    }(o, "ll-rebuild", {}, o);
  }), o;
};console.info("%c STACK-IN-CARD \n%c   Version 0.1.0   ", "color: orange; font-weight: bold; background: black", "color: white; font-weight: bold; background: dimgray");const Mt = window.loadCardHelpers ? window.loadCardHelpers() : void 0;let Tt = class extends tt {
  set hass(t) {
    this._hass = t, this._card && (this._card.hass = t);
  }static get styles() {
    return Q`
      ha-card {
        overflow: hidden;
      }
    `;
  }setConfig(t) {
    var e, n;if (!t.cards) throw new Error("There is no cards parameter defined");this._config = Object.assign(Object.assign({ mode: "vertical" }, t), { keep: Object.assign({ background: !1, margin: !1, box_shadow: !1, border_radius: !1 }, t.keep) }), (null === (e = this._config.keep) || void 0 === e ? void 0 : e.margin) && void 0 === (null === (n = this._config.keep) || void 0 === n ? void 0 : n.outer_padding) && (this._config.keep.outer_padding = !0), this._createCard({ type: `${this._config.mode}-stack`, cards: this._config.cards }).then(t => {
      this._card = t, this._waitForChildren(t, !1), window.setTimeout(() => {
        var e, n, s, i, r;if ((null === (n = null === (e = this._config) || void 0 === e ? void 0 : e.keep) || void 0 === n ? void 0 : n.background) || this._waitForChildren(t, !0), (null === (i = null === (s = this._config) || void 0 === s ? void 0 : s.keep) || void 0 === i ? void 0 : i.outer_padding) && (null === (r = this._card) || void 0 === r ? void 0 : r.shadowRoot)) {
          const t = this._card.shadowRoot.getElementById("root");t && (t.style.padding = "8px");
        }
      }, 500);
    });
  }render() {
    return this._hass && this._card && this._config ? Y`
      <ha-card header=${nt(this._config.title)}>
        <div>${this._card}</div>
      </ha-card>
    ` : Y``;
  }_updateStyle(t, e) {
    var n, s, i, r, o, a;t && ((null === (s = null === (n = this._config) || void 0 === n ? void 0 : n.keep) || void 0 === s ? void 0 : s.box_shadow) || (t.style.boxShadow = "none"), !(null === (r = null === (i = this._config) || void 0 === i ? void 0 : i.keep) || void 0 === r ? void 0 : r.background) && e && "true" !== getComputedStyle(t).getPropertyValue("--keep-background").trim() && (t.style.background = "transparent"), (null === (a = null === (o = this._config) || void 0 === o ? void 0 : o.keep) || void 0 === a ? void 0 : a.border_radius) || (t.style.borderRadius = "0"));
  }_loopChildren(t, e) {
    t.childNodes.forEach(t => {
      var n, s;"STACK-IN-CARD" !== t.tagName && (!(null === (s = null === (n = this._config) || void 0 === n ? void 0 : n.keep) || void 0 === s ? void 0 : s.margin) && t.style && (t.style.margin = "0px"), this._waitForChildren(t, e));
    });
  }_updateChildren(t, e) {
    if (t) if (t.shadowRoot) {
      const n = t.shadowRoot.querySelector("ha-card");if (n) this._updateStyle(n, e);else {
        const n = t.shadowRoot.getElementById("root") || t.shadowRoot.getElementById("card");if (!n) return;this._loopChildren(n, e);
      }
    } else "function" == typeof t.querySelector && t.querySelector("ha-card") && this._updateStyle(t.querySelector("ha-card"), e), this._loopChildren(t, e);
  }_waitForChildren(t, e) {
    t.updateComplete ? t.updateComplete.then(() => {
      this._updateChildren(t, e);
    }) : this._updateChildren(t, e);
  }async _createCard(t) {
    let e;return e = Mt ? (await Mt).createCardElement(t) : Nt(t), this._hass && (e.hass = this._hass), e && e.addEventListener("ll-rebuild", n => {
      n.stopPropagation(), this._rebuildCard(e, t);
    }, { once: !0 }), e;
  }async _rebuildCard(t, e) {
    const n = await this._createCard(e);return t.replaceWith(n), this._card = n, window.setTimeout(() => {
      var t, e, n, s, i;if ((null === (e = null === (t = this._config) || void 0 === t ? void 0 : t.keep) || void 0 === e ? void 0 : e.background) || this._waitForChildren(this._card, !0), (null === (s = null === (n = this._config) || void 0 === n ? void 0 : n.keep) || void 0 === s ? void 0 : s.outer_padding) && (null === (i = this._card) || void 0 === i ? void 0 : i.shadowRoot)) {
        const t = this._card.shadowRoot.getElementById("root");t && (t.style.padding = "8px");
      }
    }, 500), n;
  }getCardSize() {
    return this._card && "function" == typeof this._card.getCardSize ? this._card.getCardSize() : 1;
  }
};var Et;t([J()], Tt.prototype, "_card", void 0), t([J()], Tt.prototype, "_config", void 0), t([J()], Tt.prototype, "_hass", void 0), Tt = t([(Et = "stack-in-card", t => "function" == typeof t ? ((t, e) => (window.customElements.define(t, e), e))(Et, t) : ((t, e) => {
  const { kind: n, elements: s } = e;return { kind: n, elements: s, finisher(e) {
      window.customElements.define(t, e);
    } };
})(Et, t))], Tt);
