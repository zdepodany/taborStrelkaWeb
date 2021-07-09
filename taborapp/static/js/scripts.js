// OPENING & CLOSING MODAL WINDOW FOR PHOTO GALLERY

function openModal(index, max) {
    let imgTag;
    let modal;
    let photoWrap;
    let strIndex;
    modal = document.getElementById('modalBG');
    modal.style.display = 'flex';

    strIndex = 'photo'.concat(index.toString())
    imgTag = document.getElementById(strIndex);
    photoWrap = document.getElementById('photoWrap');
    photoWrap.state = new Object();
    photoWrap.src = imgTag.src;
    photoWrap.state.index = index;
}

function closeModal() {
    let photoWrap;
    let modal;
    modal = document.getElementById('modalBG');
    modal.style.display = 'none';

    photoWrap = document.getElementById('photoWrap');
    photoWrap.src = '';
}

// LISTING IN MODAL

function modalPrev() {
    let photoWrap;
    let index;
    let strIndex;
    let ourPhoto;

    photoWrap = document.getElementById('photoWrap');
    index = photoWrap.state.index;

    if (index > 0) {
        index--;
        strIndex = 'photo'.concat(index.toString());
        ourPhoto = document.getElementById(strIndex);
        photoWrap.src = ourPhoto.src;
        photoWrap.state.index = index;
    }
}

function modalNext(max) {
    let photoWrap;
    let index;
    let strIndex;
    let ourPhoto;

    photoWrap = document.getElementById('photoWrap');
    index = photoWrap.state.index;
    if (index < max) {
        index++;
        strIndex = 'photo'.concat(index.toString());
        ourPhoto = document.getElementById(strIndex);
        photoWrap.src = ourPhoto.src;
        photoWrap.state.index = index;
    }
}
