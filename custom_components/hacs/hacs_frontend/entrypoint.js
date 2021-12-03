
try {
  new Function("import('/hacsfiles/frontend/main-ff32767d.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-ff32767d.js';
  document.body.appendChild(el);
}
  