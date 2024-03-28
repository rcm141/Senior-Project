// the list of HTML tags the user can hover over
// may want to allow user configure as an advanced setting
// 99.99% of the time we can predict which ones are actually relevant
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

document.addEventListener("mouseover", (e) => {
    if (!tags.includes(e.target.tagName)) {
        //console.log(e.target.tagName);
        return;
    }
    if (e.target === document.body || 
        curr && curr === e.target) {
        return;
    }
    if (curr) {
        curr.classList.remove("selector");
        curr = null;
    }
    if (e.target) {
        curr = e.target;
        curr.classList.add("selector");
        //console.log(e.target);
    }
    },
    false
);

document.addEventListener("click", async () => {
    //console.log(`${curr} is selected`);
    //console.dir(curr);
    //console.log(curr.tagName.toLowerCase());
    //console.log(curr.classList);
    
    const response = await chrome.runtime.sendMessage({
        type:       'element',
        id:         curr.id,
        name:       curr.className,
        tagname:    curr.tagName.toLowerCase(),
        classlist:  curr.classList
        });
    console.log(response);
});