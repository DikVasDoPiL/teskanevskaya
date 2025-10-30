let menu = document.getElementsByClassName("admin-menu--item");
let top_menu = document.getElementsByClassName("top-menu--item");
for (let item in menu) {
    if (menu[item].pathname == location.pathname)
        menu[item].classList.add("admin-menu--item__active");
};
for (let item in top_menu) {
    if (top_menu[item].pathname == location.pathname)
        top_menu[item].classList.add("top-menu--item__active");
};