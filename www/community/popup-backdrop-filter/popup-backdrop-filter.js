const style = document.createElement('style');
style.appendChild(document.createTextNode(''));
document.head.appendChild(style);

style.sheet.insertRule(`
    :root {
        --iron-overlay-backdrop-opacity: 1;
        --iron-overlay-backdrop-background-color: rgba(0,0,0,.25);
    }
    `, 0);

style.sheet.insertRule(`
    iron-overlay-backdrop {
        backdrop-filter: var(--iron-overlay-backdrop-filter, blur(10px));
        -webkit-backdrop-filter: var(--iron-overlay-backdrop-filter, blur(10px));
    }
    `, 1);

