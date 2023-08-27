'use strict'; 

/* Dropdown menu */

const sidebarNavigationItems = document.getElementsByClassName('navigation__item');

for (let i = 0; i < sidebarNavigationItems.length; i++) {
    sidebarNavigationItems[i].addEventListener('click', function() {
        if (sidebarNavigationItems[i].children[1]) {
            let dropdownConteinar = sidebarNavigationItems[i].children[1];
            let arrow = sidebarNavigationItems[i].children[0].children[0];
            arrow.classList.toggle('rotate');
            dropdownConteinar.classList.toggle('show');
        }  
    })
}

/* Top navigation */

const topNavigation = document.getElementsByClassName('top-navigation')[0];
const topNavigationTemplate = `<span class="material-symbols-outlined button-icon top-menu-icon" onclick="openSearch()">search</span>
<span class="material-symbols-outlined button-icon top-menu-icon" onclick="openSubscribe()">email</span>
<span class="material-symbols-outlined button-icon top-menu-icon" onclick="openMenu()">menu</span>`;

/* Open/close menu */

const menu = document.getElementsByClassName('menu')[0];

function openMenu() {
    menu.classList.add('show');
    topNavigation.innerHTML = '<span class="material-symbols-outlined button-icon middle-icon" onclick="closeMenu()">undo</span>';
}

function closeMenu() {
    menu.classList.remove('show');
    topNavigation.innerHTML = topNavigationTemplate;
}

/* Open/close search */

const search = document.getElementsByClassName('search')[0];
const closeSearchButton = '<span class="material-symbols-outlined button-icon middle-icon" id="close-search" onclick="closeSearch()">undo</span>';
const logo = document.getElementsByClassName('logo')[0];
const header = document.getElementsByTagName('header')[0];

function openSearch() {
    search.style.display = 'flex';
    header.classList.add('hide');
    logo.classList.add('hide');
    search.insertAdjacentHTML('afterbegin', closeSearchButton);
}

function closeSearch() {
    logo.classList.remove('hide');
    header.classList.remove('hide');
    search.style.display = 'none';
    document.getElementById('close-search').remove();
    topNavigation.innerHTML = topNavigationTemplate;
}

/* Open/close subscribe */

const subscribe = document.getElementsByClassName('subscribe')[0];

function openSubscribe() {
    subscribe.classList.add('show');
    topNavigation.innerHTML = '<span class="material-symbols-outlined button-icon middle-icon" onclick="closeSubscribe()">undo</span>';
}

function closeSubscribe() {
    subscribe.classList.remove('show');
    topNavigation.innerHTML = topNavigationTemplate;
}


const showOnPx = 100;
const backToTopButton = document.querySelector(".back-to-top");

const scrollContainer = () => {
  return document.documentElement || document.body;
};

document.addEventListener("scroll", () => {
    const scroll = document.documentElement.scrollTop
    if (scroll > 0) {
        backToTopButton.classList.remove("back-to-top_hide");
    } else {
        backToTopButton.classList.add("back-to-top_hide");
    }
});

backToTopButton.addEventListener("click", function() {
    document.body.scrollIntoView({
        behavior: "smooth"
      });
});
