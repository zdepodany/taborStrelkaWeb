let images = document.querySelectorAll('.image');
let pickedPhotos = [];
let photoId;
let indexToRemove;

images.forEach(function (image) {
    // On load
    image.is_selected = false;
    image.addEventListener('click', function () {
    // On click
    if (this.is_selected) {
        this.classList.remove('imagePicked');
        this.is_selected = false;
        photoId = this.getAttribute('id');
        photoId = parseInt(photoId, 10);
        indexToRemove = pickedPhotos.indexOf(photoId);
        pickedPhotos.splice(indexToRemove, 1);
    } else {
        this.classList.add('imagePicked');
        this.is_selected = true;
        photoId = this.getAttribute('id');
        photoId = parseInt(photoId, 10);
        pickedPhotos.push(photoId);
    }
    })
})