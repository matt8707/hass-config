const LitElement = Object.getPrototypeOf(
    customElements.get("ha-panel-lovelace")
);
const html = LitElement.prototype.html;

const style = html`
    <style>
        #xiaomiCard {
            overflow: hidden;
        }
        #mapWrapper {
            width: auto;
        }
        #map {
            position: relative;
            display: block;
            width: 100%;
            height: 100%;
        }
        #mapBackground {
            position: absolute;
            z-index: 1;
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
        }
        #mapDrawing {
            width: 100%;
            height: 100%;
            position: absolute;
            z-index: 2;
            left: 0;
            top: 0;
        }
        .dropdownWrapper {
            margin-left: 10px;
            margin-right: 10px;
        }
        .vacuumDropdown {
            width: 100%;
        }
        .buttonsWrapper {
            margin: 5px;
        }
        .vacuumRunButton {
            margin: 5px;
            float: right;
        }
        #increaseButton {
            margin: 5px;
            float: left;
        }

        #toast {
            visibility: hidden;
            width: 100%;
            height: 50px;
            max-height: 50px;
            color: var(--primary-text-color);
            text-align: center;
            border-radius: 2px;
            padding-left: 30px;

            position: absolute;
            z-index: 1;
            bottom: 30px;
            font-size: 17px;
            white-space: nowrap;
        }
        #toast #img{
            display: table-cell;
            width: 50px;
            height: 50px;
            float: left;
            padding-top: 16px;
            padding-bottom: 16px;
            box-sizing: border-box;
            background-color: var(--primary-color);
            color: #0F0;
        }
        #toast #desc{
            box-sizing: border-box;
            display: table-cell;
            padding-left: 10px;
            padding-right: 10px;
            -moz-box-sizing: border-box;
            -webkit-box-sizing: border-box;
            background-color: var(--paper-listbox-background-color);
            color: var(--primary-text-color);
            vertical-align: middle;
            height: 50px;
            overflow: hidden;
            white-space: nowrap;
            border-color: var(--primary-color);
            border-style: solid;
            border-width: 1px;
        }

        #toast.show {
            visibility: visible;
            -webkit-animation:  fadein 0.5s, stay 1s 1s, fadeout 0.5s 1.5s;
            animation: fadein 0.5s, stay 1s 1s, fadeout 0.5s 1.5s;
        }

        @-webkit-keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }
        @-webkit-keyframes stay {
            from {width: 100%}
            to {width: 100%}
        }
        @keyframes stay {
            from {width: 100%}
            to {width: 100%}
        }
        @-webkit-keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 60px; opacity: 0;}
        }
        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 60px; opacity: 0;}
        }
    </style>`;

export default style;