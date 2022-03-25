let modal = document.querySelector('.modalWrapper');
let modalOpened = false;

// OPENING & CLOSING MODAL WINDOW FOR PHOTO GALLERY

// Click on photo
function openModal(index, max) {
    let imgTag;
    let modal;
    let photoWrap;
    let strIndex;
    let downloadPhoto;
    modal = document.getElementById('modalBG');
    modal.style.display = 'flex';

    strIndex = 'photo'.concat(index.toString())
    imgTag = document.getElementById(strIndex);
    photoWrap = document.getElementById('photoWrap');
    photoWrap.state = new Object();
    photoWrap.src = imgTag.src.replace("thumbnails", "photos");
    photoWrap.state.index = index;

    downloadPhoto = document.getElementById('downloadPhoto');
    downloadPhoto.href = photoWrap.src;
    modalOpened = true;
}

// Click on 'Close' btn
function closeModal() {
    let photoWrap;
    let modal;
    modal = document.getElementById('modalBG');
    modal.style.display = 'none';

    photoWrap = document.getElementById('photoWrap');
    photoWrap.src = '';
    modalOpened = false;
}

// Click 'Escape' key
document.addEventListener('keydown', (e) => {
    if (e.key == 'Escape' && modalOpened == true) {
        closeModal();
    }
})

// Click on background
modal.addEventListener('click', (e) => {
    if (!e.target.className.includes('noClose')) {
        closeModal();
    }
})


// LISTING IN MODAL

function modalPrev() {
    let photoWrap;
    let index;
    let strIndex;
    let ourPhoto;
    let downloadPhoto;

    photoWrap = document.getElementById('photoWrap');
    index = photoWrap.state.index;

    if (index > 0) {
        index--;
        strIndex = 'photo'.concat(index.toString());
        ourPhoto = document.getElementById(strIndex);
        photoWrap.src = ourPhoto.src.replace("thumbnails", "photos");
        photoWrap.state.index = index;
    }

    downloadPhoto = document.getElementById('downloadPhoto');
    downloadPhoto.href = photoWrap.src;
}

function modalNext(max) {
    let photoWrap;
    let index;
    let strIndex;
    let ourPhoto;
    let downloadPhoto;

    photoWrap = document.getElementById('photoWrap');
    index = photoWrap.state.index;
    if (index < max) {
        index++;
        strIndex = 'photo'.concat(index.toString());
        ourPhoto = document.getElementById(strIndex);
        photoWrap.src = ourPhoto.src.replace("thumbnails", "photos");
        photoWrap.state.index = index;
    }

    downloadPhoto = document.getElementById('downloadPhoto');
    downloadPhoto.href = photoWrap.src;
}
