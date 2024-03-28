
// sends message to background.js on event inside document body
// document.addEventListener("click", (event) => {
//     chrome.runtime.sendMessage({
//         click: true,
//       },
//       response => {
//         console.log("Received response", response);
//       }
//     );
// });

/* selector code */
const tags = [
    'DIV',
    'SECTION',
    'TABLE',
    'TD',
    'IFRAME',
    'LINK',
    'A',
    'IMG',
]

let curr = null;
let selectorEnabled = false;

document.addEventListener('mouseover', (e) => {

    if (!selectorEnabled) {
        // reset if needed
        if (curr != null) {
            curr.classList.remove("selector");
            curr = null;
        }
        return;
    }

    if (!tags.includes(e.target.tagName)) {
        //console.log(e.target.tagName);
        return;
    }
    if (e.target === document.body || 
        curr && curr === e.target) {
        return;
    }
    if (curr) {
        curr.classList.remove('selector');
        curr = null;
    }
    if (e.target) {
        curr = e.target;
        curr.classList.add('selector');
        //console.log(e.target);
    }
    },
    false
);

document.addEventListener('click', async () => {
    console.log('you clicked content while selector was %s', selectorEnabled);
    if (!selectorEnabled) return;

    chrome.runtime.sendMessage({
        type:       'element',
        id:         curr.id,
        name:       curr.className,
        tagname:    curr.tagName.toLowerCase(),
        classlist:  curr.classList,
        },
        response => {
            console.log("content got response", response);
        });
});

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

        if (request.name === 'selectToggle') {
            selectorEnabled = !selectorEnabled;
            sendResponse({
                selectStatus:   selectorEnabled,
            })
        }
    }
)