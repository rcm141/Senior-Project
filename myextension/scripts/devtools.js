
let surprise;

chrome.devtools.panels.create("Senior Project", "icon.png", "panel.html", panel => {
    // code invoked on panel creation
    
    panel.onShown.addListener( (extpanel) => {
        // do magic with the panel
        let clickme = extpanel.document.querySelector('#clickme');
        let select = extpanel.document.querySelector('#select');
        surprise    = extpanel.document.querySelector('#surprise');

        clickme.addEventListener('click', () => {
            chrome.devtools.inspectedWindow.eval('alert("why did you click me");');
        });
        select.addEventListener('click', () => {
            console.log("you clicked the select button");
            // we send the active window tabid to the background
            // this way the background can find its content script
            backgroundConnection.postMessage({
                name:   'selectToggle',
                tabId: chrome.devtools.inspectedWindow.tabId,
            })
        });
    });
});

// on message from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    
    if (request.type == 'element') {
        element = request.element;
        console.log("devtools got %O from content", element);
        chrome.devtools.inspectedWindow.eval('alert(request.classlist);');
        if (surprise) {
            surprise.innerHTML = `look it's ${JSON.stringify(request)}`;
        };
        sendResponse('got element');
      }
});

// connection to background.js
const backgroundConnection = chrome.runtime.connect({
    name: "devtools-page"
});

// on message from background.js
// idk

// send current tabid to background.js
backgroundConnection.postMessage({
    name: 'init',
    tabId: chrome.devtools.inspectedWindow.tabId,
});