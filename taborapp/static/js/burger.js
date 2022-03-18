let burgerButton = document.querySelector('#burger');
let burgerMenu = document.querySelector('.burgerMenuWrapper');

//Onload
burgerButton.isClicked = false;

burgerButton.addEventListener('click', () => {
    //Onclick
    if (this.isClicked) {
        burgerMenu.classList.remove('burgerMenuWrapperShow');
        this.isClicked = false;
    } else {
        burgerMenu.classList.add('burgerMenuWrapperShow');
        this.isClicked = true;
    }
})