
try {
  new Function("import('/hacsfiles/frontend/main-8113c4f2.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-8113c4f2.js';
  document.body.appendChild(el);
}
  