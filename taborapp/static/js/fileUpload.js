document.querySelectorAll('#fakeFileUploadButton').forEach(function (button) {
    let hiddenInput = button.parentElement.querySelector('#realFileUpload');
    let label = button.parentElement.querySelector('#fakeFileUploadText');
    let defaultLabelText = 'Nevybráno';

    // Set default text for label
    label.textContent = defaultLabelText;
    label.title = defaultLabelText;

    // Click on hidden "Browse button"
    button.addEventListener('click', function () {
        hiddenInput.click();
    });

    // Show number of chosen files
    hiddenInput.addEventListener('change', function () {
        let fileNumberList = hiddenInput.files.length;
        label.textContent = 'Vybráno fotek: ' + fileNumberList.toString();
    });

});
