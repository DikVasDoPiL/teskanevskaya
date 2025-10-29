let menu = document.getElementsByClassName("admin-menu--item")
for (let item in menu) {
    if (menu[item].pathname == location.pathname)
        menu[item].classList.add("admin-menu--item__active");
};
