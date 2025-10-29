window.addEventListener("load", function () {
    const preloader = document.getElementById("preloader");
    if (preloader) {
        preloader.style.opacity = "0";
        preloader.style.transition = "opacity 0.5s ease";
        setTimeout(() => (preloader.style.display = "none"), 50);
    }
});
