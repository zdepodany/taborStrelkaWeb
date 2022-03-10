function clickHidden(docName, buttonName) {
    let browseButtonID = '#' + docName + '_' + buttonName;
    hiddenInput = document.querySelector(browseButtonID);
    hiddenInput.click();
}
