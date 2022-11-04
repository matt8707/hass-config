// browser_mod_icon.js
// hide browser_mod "require interaction" icon

const style = document.createElement('style');

style.textContent = `
  .browser-mod-require-interaction {
    display: none;
  }
`;

document.head.appendChild(style);

// preload disabled card border in popups

const popup = document.querySelector("body > browser-mod-popup");

if (popup) {
  popup.style.cssText += `
    --ha-card-border-width: 0;
  `;
}
