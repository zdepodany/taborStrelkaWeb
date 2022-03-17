
function clickHidden(buttonID) {
    buttonID = '#' + buttonID;
    const hiddenInput = document.querySelector(buttonID);
    hiddenInput.click();
}

// On load
function init() {
    let docButtons = document.querySelectorAll('.realDocBrowse');

    docButtons.forEach((docButton, i) => {
        let numID = i
        if (i > 3) {
            numID = 1024 + (i-4)
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
        if (i > 3) {
            numID = 1024 + (i-4)
        }
        docValue.value = numID;
    });
}
window.onload = init;

