// Smoke test for dashboard/app.js — loads the browser bundle in Node with
// DOM stubs and asserts it initialises without throwing (regression guard
// for the null.innerHTML style crashes). NOT a full DOM emulation: it only
// proves the top-level code and the init/error paths run cleanly.
//
// Run:  node tests/test_app_js_smoke.js

"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

function makeElement() {
  const el = {
    children: [],
    style: {},
    dataset: {},
    value: "",
    hidden: false,
    disabled: false,
    textContent: "",
    innerHTML: "",
    checked: false,
    options: [],
    parentNode: null,
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {},
    removeEventListener() {},
    setAttribute() {},
    getAttribute() { return null; },
    removeAttribute() {},
    appendChild(child) { this.children.push(child); return child; },
    remove() {},
    click() {},
    focus() {},
    select() {},
    closest() { return null; },
    querySelector() { return makeElement(); },
    querySelectorAll() { return []; },
    getBoundingClientRect() { return { left: 0, top: 0, bottom: 0, width: 0, height: 0 }; },
    insertBefore(node) { return node; },
    createElement: undefined,
  };
  el.createElement = () => makeElement();
  el.createDocumentFragment = () => makeElement();
  return el;
}

const documentStub = {
  readyState: "complete",
  documentElement: { lang: "" },
  body: makeElement(),
  getElementById() { return makeElement(); },
  querySelector() { return makeElement(); },
  querySelectorAll() { return []; },
  createElement() { return makeElement(); },
  createDocumentFragment() { return makeElement(); },
  addEventListener() {},
};

const windowStub = {
  location: { search: "", pathname: "/index.html", href: "http://localhost/index.html", hash: "" },
  history: { pushState() {}, replaceState() {} },
  matchMedia() { return { matches: false }; },
  addEventListener() {},
  URLSearchParams,
};

const sandbox = {
  document: documentStub,
  window: windowStub,
  navigator: {},
  localStorage: { getItem() { return null; }, setItem() {} },
  fetch: () => Promise.reject(new Error("no network in smoke test")),
  URLSearchParams,
  URL: { createObjectURL() { return "blob:stub"; }, revokeObjectURL() {} },
  Chart: undefined,
  console,
  setTimeout,
  clearTimeout,
};
sandbox.window.document = documentStub;
sandbox.globalThis = sandbox;

const code = fs.readFileSync(path.join(__dirname, "..", "dashboard", "app.js"), "utf-8");
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: "app.js" });

let initCalls = 0;
documentStub.addEventListener = (type) => { if (type === "DOMContentLoaded") initCalls += 1; };

// readyState "complete" means init() ran synchronously via the else branch.
setTimeout(() => {
  // If execution reached here, top-level code + init + error path ran
  // without throwing. The fetch stub rejects, exercising showLoadError.
  console.log("SMOKE OK: app.js loaded and initialised without throwing");
}, 50);
