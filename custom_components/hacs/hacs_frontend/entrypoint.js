
try {
  new Function("import('/hacsfiles/frontend/main-25487c89.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-25487c89.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  