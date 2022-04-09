
function clickHidden(buttonID) {
    buttonID = '#' + buttonID;
    const hiddenInput = document.querySelector(buttonID);
    hiddenInput.click();
}

// On load
function init() {
    // TODO: replace hardcoded docs length with AJAX requested values
    let docButtons = document.querySelectorAll('.realDocBrowse');

    docButtons.forEach((docButton, i) => {
        let numID = i
        // AJAX
        if (i > 5) {
            numID = 1024 + (i-6)
        }
        let id = "doc" + numID + "_browse";
        docButton.id = id
        const buttonID = id.replace("browse", "submit");
        docButton.addEventListener('change', () => {
            clickHidden(buttonID);
        });
    });

    let docValues = document.querySelectorAll('.realDocValue');

    docValues.forEach((docValue, i) => {
        let numID = i
        // AJAX
        if (i > 5) {
            numID = 1024 + (i-6)
        }
        docValue.value = numID;
    });
}
window.onload = init;

