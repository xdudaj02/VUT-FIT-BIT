function scrollSmoothTo(elementId){
    var element = document.getElementById(elementId);
    let headerOffset = 0;
    if (window.innerWidth <= 576) {
        if (window.pageYOffset >= sticky) {
            headerOffset = 58;
        } else {
            headerOffset = 116;
        }
    }
    var elementPosition = element.getBoundingClientRect().top;
    var offsetPosition = elementPosition - headerOffset;

    window.scrollBy({
        top: offsetPosition,
        left: 0,
        behavior: "smooth"
    });
}

function doDropDown() {
    if (window.innerWidth <= 576) {
        document.getElementById("dropdown-menu").classList.toggle("show-menu");
    }
}