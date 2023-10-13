import { app } from "../../scripts/app.js";
import { ComfyDialog, $el } from "../../scripts/ui.js";
import { ComfyApp } from "../../scripts/app.js";

const images = {
cute_comfy_logo: 'data:image/png;base64,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'
}

const cuteCustomStyles = `
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;500;600;700&family=Noto+Color+Emoji&display=swap');

:root
{
    --cute-comfy-text: #E1D5E8;
    --cute-comfy-bar-height: 50px;
    --cute-comfy-sidebar-width: 200px;
    --cute-comfy-sidebar-bg: #49355a;
}

#cute-comfy,
#cute-comfy *
{
    font-family: 'Comfortaa', sans-serif !important;
    font-size: 1rem;
}

#cute-comfy
{
    color: var(--cute-comfy-text);
}

#cute-comfy #batchCountInputNumber
{
    width: 50px;
    height: 26px;
    text-align: center;
    background-color: #d4c4e3;
    border: none;
    color: #241a2d;
}

.emoji
{
    font-family: 'Noto Color Emoji', sans-serif !important;
}

.cute-comfy-top-bar
{
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: var(--cute-comfy-bar-height);
    justify-content: space-between;
    align-items: center;
    background: rgb(119, 86, 148);
    background: linear-gradient(135deg, rgba(119, 86, 148, 1) 20%, rgba(36, 26, 45, 1) 100%);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.cute-comfy-top-bar-left
{
    display: flex;
    align-items: center;
    height: 100%;
    padding-left: 10px;
}

.cute-comfy-top-bar-right
{
    display: flex;
    align-items: center;
    height: 100%;
    padding-right: 10px;
}

.cute-comfy-top-bar-right > *,
.cute-comfy-top-bar-left > *,
.cute-comfy-top-bar-right button.comfy-queue-btn
{
    margin-left: 1rem !important;
}

.cute-comfy-top-bar-right > *:last-child
{
    margin-left: 0;
}

.cute-comfy-top-bar-left > *:first-child
{
    margin-left: 0;
}

.cute-comfy-logo
{
    position: relative;
    height: 100%;
}

.cute-comfy-logo img
{
    height: 100%;
}

.cute-comfy-button
{
    background-color: #b382e0;
    border: none;
    color: #241a2d;
    font-weight: bold;
    padding: 5px 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    width: auto;
    height: 28px;
    line-height: 1.25rem;
    cursor: pointer;

    box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
}

.cute-comfy-button:hover
{
    background-color: #a66ed8;
    color: #241a2d;
}

button.cute-comfy-button > svg
{
    margin: 0 0.2rem;
}

.cute-comfy-menu-button:hover
{
    color: #999;
}

.cute-comfy-menu-button:active
{
    color: #666;
}

div.cute-comfy-menu
{
    position: absolute;
    top: var(--cute-comfy-bar-height);
    right: 0;
    bottom: 0;

    background-color: var(--cute-comfy-sidebar-bg);
    border: none;
    box-shadow: none;
    border-radius: 0;
    width: var(--cute-comfy-sidebar-width);

    padding: 0 !important;
}

div.cute-comfy-menu button,
div.cute-comfy-menu .cute-queue-button
{
    border: 0;
    border-radius: 0;

    display: inline-flex;
    flex-flow: row nowrap;
    justify-content: center;
    align-items: center;

    min-height: 33px;

    background-color: #251b2e;
    color: #eed7eb !important
}

div.cute-comfy-menu hr
{
    height: 1px !important;
    background-color: #ed8def;
    border: 0;
}

div.cute-comfy-menu .cute-queue-button
{
    padding: 0.25rem 1rem;
    font-size: 1.25rem;
}

div.cute-comfy-list
{
    margin: 0;
    padding: 0;
    border: 0;
    background-color: initial;
    display: flex;
    flex-flow: column nowrap;
    align-items: center;
    justify-content: stretch;
}

div.cute-comfy-list h4
{
    font-family: 'Comfortaa', sans-serif !important;
    color: #eed7eb !important;
    font-size: 1.3rem;
    margin: 0.5rem 0;
}

div.cute-comfy-list .comfy-list-items:first-of-type:empty:before
{
    font-size: 0.7rem;
    content: 'Nothing!';
    color: #eed7eb !important;
    opacity: 0.6;
    font-style: italic;
}

div.cute-comfy-menu .cute-comfy-spacer
{
    flex-grow: 1;
}

div.cute-comfy-list
{
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    flex-grow: 10;
}


div.cute-comfy-list .comfy-list-items
{
    overflow: auto;
    min-height: 0;
    width: 100%;
    background: initial;
    max-height: unset;
    max-height: unset;
    flex-basis: 0;
    padding: 0;
}

div.cute-comfy-list .comfy-list-items:not(:first-of-type)
{
    flex-grow: 1;
    height: 100%;
}

div.cute-comfy-list .comfy-list-items:first-of-type
{
    flex-grow: 0;
    min-height: 32px;
    overflow: hidden;
}

div.cute-comfy-list ~ div.cute-comfy-list .comfy-list-items
{
    flex-grow: 1;
    overflow: auto;
}

div.cute-comfy-list .comfy-list-items > div
{
    width: 100%;

    position: relative;
    display: flex;
    flex-flow: row nowrap;

    justify-content: flex-start;
    align-items: center;

    background-color: #382747;
}

div.cute-comfy-list .comfy-list-items > div > span
{
    display: inline-block;
    font-size: 1rem;
    color: #eed7eb !important;
    flex-grow: 1;
    text-align: left;
    padding: 0 0.75rem;
    order: -2;
}

div.cute-comfy-list .comfy-list-items > div > svg
{
    order: -1;
    color: #ff30c5;
}

div.cute-comfy-list .comfy-list-items > div > span:before
{
    content: '#';
}

div.cute-comfy-list .comfy-list-items > div > button
{
    flex-grow: 0;
    justify-self: flex-end;
    background: none;
    min-height: unset;
    min-width: unset;
    height: 100%;
}

div.cute-comfy-list .comfy-list-items > div .cute-queue-button
{
    padding: 0.25rem 0.6rem !important;
}

/* Hover effects */
button:hover > .cute-hover-red
{
    color: #e5586a;
}

button:hover > .cute-hover-blue
{
    color: #5890e5;
}

button:hover > .cute-hover-green
{
    color: #58e57a;
}

.cute-comfy-pop-menu
{
    position: absolute;
    right: -7.5em;
    top: 50px;

    display: flex;
    flex-flow: column nowrap;
}

.cute-comfy-pop-menu > *
{
    height: unset;
    text-align: left;
    padding: 0.75rem 1rem;
}

.cute-comfy-top-bar-left
{
    position: relative;
}

/* Overrides the built-in media query for small screens, argh...! */
@media only screen and (max-height: 850px)
{
    .comfy-menu.cute-comfy-menu
    {
        top: var(--cute-comfy-bar-height) !important;
    }
}
`;

function moveElement(elementSelector, destinationParentSelector, newClass, append = false)
{
    let element = document.querySelector(elementSelector);
    if (newClass)
    {
        element.classList.add(newClass);
    }
    // Clear inline styles from the element
    element.removeAttribute("style");
    let elementParent = element.parentNode;
    elementParent.removeChild(element);
    let destinationParent = document.querySelector(destinationParentSelector);
    if (append) {
        destinationParent.appendChild(element);
    } else {
        destinationParent.insertBefore(element, destinationParent.firstChild);
    }

    return element;
}

function surroundElement(elementSelector, surroundElementName)
{
    let element = document.querySelector(elementSelector);
    let surroundElement = document.createElement(surroundElementName);
    let elementParent = element.parentNode;
    elementParent.removeChild(element);
    surroundElement.appendChild(element);
    elementParent.appendChild(surroundElement);

    return surroundElement;
}

// Blocks until the element is visible
function waitForElementVisibility(selector, timeout = 5000)
{
    let start = Date.now();
    let element = document.querySelector(selector);
    while (element == null || element.offsetParent === null)
    {
        if (Date.now() - start > timeout)
        {
            throw new Error(`Timed out waiting for element ${selector} to appear.`);
        }
        element = document.querySelector(selector);
    }
}

async function initCuteness() {
    console.group('💜 Cute Comfy 💜 ');
    console.log("🟣 I'm going to make things CUTE! ^_^");

    // Add a link tag to the header to add Font Awesome
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css";
    document.head.appendChild(link);

    // Add a script tag for Font Awesome
    var script = document.createElement("script");
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/js/all.min.js";
    document.head.appendChild(script);

    // Inject custom style tag into the header
    var style = document.createElement("style");
    style.innerHTML = cuteCustomStyles;
    document.head.appendChild(style);
    
    //import { app } from "../../scripts/app.js";
    
    // Find the drag-handle div inside the comfy-menu div, and hide it.
    document.querySelector(".comfy-menu .drag-handle").style.display = "none";
    
    // Inject a "cute comfy" top bar
    var template = `
        <div class="cute-comfy-top-bar">
            <div class="cute-comfy-top-bar-left">
                <div class="cute-comfy-logo">
                    <img src="${images.cute_comfy_logo}" alt="cute comfy logo" />
                </div>
            </div>
            <div class="cute-comfy-top-bar-right">
            </div>
        </div>
    `

    // Init menu
    var topBar = document.createElement("div");
    topBar.id = "cute-comfy";
    topBar.innerHTML = template;
    
    var menu = document.querySelector(".comfy-menu");
    menu.style.top = "var(--cute-comfy-bar-height)";
    menu.classList.add("cute-comfy-menu");
    menu.parentNode.insertBefore(topBar, menu);

    // Hide useless "Extra Options" / "View Queue" / "View History"
    document.querySelector(".comfy-menu label").parentNode.style.display = "none";
    document.querySelector(".comfy-menu-btns").style.display = "none";

    // Right Side
    var infiniteCheck = moveElement('#autoQueueCheckbox', ".cute-comfy-top-bar-right", null, true);
    surroundElement('#autoQueueCheckbox', "div");
    infiniteCheck.title = "Infinite Queue";
    var infLabel = document.createElement("label");
    infLabel.htmlFor = "autoQueueCheckbox";
    infLabel.innerHTML = "Infinite Gen";
    infiniteCheck.after(infLabel);

    var bcount = moveElement('#batchCountInputNumber', ".cute-comfy-top-bar-right", null, true);
    var bcountLabeal = document.createElement("label");
    bcountLabeal.htmlFor = "batchCountInputNumber";
    bcountLabeal.innerHTML = '<i class="fas fa-layer-group"></i> Batch Count:';
    bcount.before(bcountLabeal);
    surroundElement('#batchCountInputNumber', "div");
    
    var queue = moveElement("#queue-button", ".cute-comfy-top-bar-right", "cute-comfy-button", true);
    queue.innerHTML = `<i class="fas fa-play"></i> Queue`;
    queue.title = "Queue Workflow";

    var queueTop = moveElement("#queue-front-button", ".cute-comfy-top-bar-right", "cute-comfy-button", true);
    queueTop.innerHTML = `<i class="fas fa-arrow-up-wide-short"></i>`;
    queueTop.title = "Queue Next";
    queueTop.classList.add("emoji");

    // Popup menu
    var menu = document.createElement("div");
    menu.classList.add("cute-comfy-pop-menu");
    menu.style.display = "none";    
    
    // Left Side
    let btn = moveElement('#comfy-save-button', ".cute-comfy-top-bar-left", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-save"></i> Save`;
    btn.title = "Download the current workflow as JSON.";
    btn = moveElement('#comfy-load-button', ".cute-comfy-top-bar-left", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-folder-open"></i> Load`;
    btn.title = "Upload a workflow JSON file. Will replace the current workflow.";
    btn = moveElement('#comfy-clear-button', ".cute-comfy-top-bar-left", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-trash"></i> Clear`;
    btn.title = "Clears the canvas. Be sure to save your workflow first!";

    // Append the menu
    document.querySelector(".cute-comfy-top-bar-left").appendChild(menu);

    // Menu items
    btn = moveElement('#comfy-dev-save-api-button', ".cute-comfy-pop-menu", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-code"></i> Save (API)`;
    btn.title = "Download the current workflow in API (JSON) format.";
    btn = moveElement('#comfy-refresh-button', ".cute-comfy-pop-menu", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-sync"></i> Refresh`;
    btn.title = "Refreshes  metadatata (selection lists, etc) inside nodes.";
    btn = moveElement('#comfy-clipspace-button', ".cute-comfy-pop-menu", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-vector-square"></i> Clip Space`;
    btn.title = "Inspect any images currently in clip space.";
    btn = moveElement('#comfy-load-default-button', ".cute-comfy-pop-menu", "cute-comfy-button", true);
    btn.innerHTML = `<i class="fas fa-undo"></i> Load Default`;
    btn.title = "Loads the default workflow.";

    // Append the menu button
    btn = document.createElement("button");
    btn.classList.add("cute-comfy-button");
    btn.innerHTML = `<i class="fas fa-bars"></i>`;
    document.querySelector(".cute-comfy-top-bar-left").appendChild(btn);
    
    // When the button is clicked, toggle the visibility of the .cute-comfy-pop-menu
    btn.addEventListener("click", (e) => {
        let menu = document.querySelector(".cute-comfy-pop-menu");
        if (menu.style.display == "none") {
            menu.style.display = "flex";
        } else {
            menu.style.display = "none";
        }
    });

    // When any buttons inside .cute-comfy-pop-menu are clicked, hide the menu
    document.querySelectorAll(".cute-comfy-pop-menu button").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            document.querySelector(".cute-comfy-pop-menu").style.display = "none";
        });
    });

    var list = document.querySelectorAll(".comfy-list");
    for (let i = 0; i < list.length; i++) {
        list[i].removeAttribute("style");
        list[i].classList.add("cute-comfy-list");
    }

    var spacer = document.createElement('div');
    spacer.classList.add('cute-comfy-spacer');
    document.querySelectorAll('.cute-comfy-list')[1].after(spacer);

    function applyMutableChanges(mutations, observer, selector)
    {
        observer.disconnect();
        observer.takeRecords();

        // Stop adding inline styling to the menu
        let menu = document.querySelector(".cute-comfy-menu");
        if (menu.hasAttribute("style"))
        {
            menu.removeAttribute("style");
        }

        // Handle "refreshes" of the running/pending queues
        var headers = document.querySelectorAll(".cute-comfy-list h4");
        for (let i = 0; i < headers.length; i++) {
            if (headers[i].innerHTML.includes("Running")) {
                headers[i].innerHTML = "Queue";
            }
            else if (headers[i].innerHTML.includes("Pending")) {
                headers[i].style.display = "none";
            }
        }

        var buttonGroups = document.querySelectorAll(".cute-comfy-list .comfy-list-actions button");
        for (let i = 0; i < buttonGroups.length; i++) {
            if (buttonGroups[i].innerHTML.includes("Clear Queue")) {
                buttonGroups[i].innerHTML = '<i class="fas fa-trash cute-hover-red"></i>';
                buttonGroups[i].title = "Clear the queue";
                buttonGroups[i].classList.add("cute-queue-button");
            }
            if (buttonGroups[i].innerHTML.includes("Clear History")) {
                buttonGroups[i].innerHTML = '<i class="fas fa-trash cute-hover-red"></i>';
                buttonGroups[i].title = "Clear your history";
                buttonGroups[i].classList.add("cute-queue-button");
            }
            else if (buttonGroups[i].innerHTML.includes("Refresh")) {
                buttonGroups[i].innerHTML = '<i class="fas fa-sync cute-hover-green"></i>';
                buttonGroups[i].title = "Refresh this list";
                buttonGroups[i].classList.add("cute-queue-button");
            }
        }

        // If we have some list items, then hook up an observer to watch for changes
        if (document.querySelectorAll(".cute-comfy-list .comfy-list-items > div").length)
        {
            var firstItem = document.querySelector(".cute-comfy-list .comfy-list-items:first-of-type > div:first-child");
            
            // Append the spinner if it's not already there
            if (firstItem.querySelectorAll("svg").length == 0 && firstItem.querySelectorAll("i").length == 0)
            {
                var ic = document.createElement("i");

                ic.classList.add("fas");
                ic.classList.add("fa-lg");
                ic.classList.add("fa-spinner");
                ic.classList.add("fa-spin-pulse");

                firstItem.appendChild(ic);
            }

            var listItems = document.querySelectorAll(".cute-comfy-list .comfy-list-items > div");
            for (let i = 0; i < listItems.length; i++) {
                var el = listItems[i];

                // If this element does not contain any span children
                if (el.querySelectorAll("span").length == 0)
                {
                    setInnerText(el, getInnerText(el).replace(":", ""));

                    // Wrap the inner text of the element in a span without affecting its children
                    var span = document.createElement("span");
                    span.innerHTML = getInnerText(el);
                    setInnerText(el, "");
                    el.appendChild(span);
                }
                var btns = el.querySelectorAll("button");
                for (let j = 0; j < btns.length; j++) {
                    btns[j].classList.add("cute-queue-button");
                    if (btns[j].innerText.includes("Load"))
                    {
                        // Set the inner HTML to an icon of an undo button
                        btns[j].innerHTML = `<i class="fas fa-file-import cute-hover-blue"></i>`;
                        btns[j].title = "Load the workflow state from this run";
                    }
                    if (btns[j].innerText.includes("Cancel"))
                    {
                        // Set the inner HTML to an icon of a stop button
                        btns[j].innerHTML = `<i class="fas fa-delete-left cute-hover-red"></i>`;
                        btns[j].title = "Stop this run";
                    }
                    if (btns[j].innerText.includes("Delete"))
                    {
                        // Set the inner HTML to an icon of a trash can
                        btns[j].innerHTML = `<i class="fas fa-circle-minus cute-hover-red"></i>`;
                        btns[j].title = "Cancel this queued item";
                    }
                }
            }    
        }

        // Start observing again
        observer.observe(document.querySelector(selector), {
            childList: true,
            subtree: true
        });
    }

    var observer1 = new MutationObserver((m, o) => applyMutableChanges(m, o, "#cute-comfy"));
    var observer2 = new MutationObserver((m, o) => applyMutableChanges(m, o, ".cute-comfy-menu"));

    observer1.observe(document.getElementById('cute-comfy'), {
        childList: true,
        subtree: true
    });
    observer2.observe(document.querySelector('.cute-comfy-menu'), {
        childList: true,
        subtree: true
    });

    console.log("🟣 ALL DONE! ^_^");
    console.groupEnd();
}

// Function to get the inner text of an element without the text from its children
// https://stackoverflow.com/a/5002619
function getInnerText(element) {
    return element.childNodes[0].nodeValue;
}

// Function to update the inner text of an element without affecting its children
// https://stackoverflow.com/a/5002619
function setInnerText(element, text) {
    element.childNodes[0].nodeValue = text;
}

app.registerExtension({
	name: "cute.comfy",
	
	async setup(app) {
        await initCuteness();
    },


});
