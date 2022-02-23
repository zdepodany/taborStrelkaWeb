let images = document.querySelectorAll('.image');

images.forEach(function (image) {
    // On load
    image.is_selected = false;
    image.addEventListener('click', function () {
    // On click
    if (this.is_selected) {
        this.classList.remove('imagePicked');
        this.is_selected = false;
    } else {
        this.classList.add('imagePicked');
        this.is_selected = true;
    }
    })
})