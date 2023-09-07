'use strict'; 

// Открытие/закрытие верхнего меню в мобильной версии

const topNavigation = document.getElementsByClassName('top-navigation')[0];
const topNavigationTemplate = `<span class="material-symbols-outlined button-icon top-menu-icon" onclick="openSearch()">search</span>
<span class="material-symbols-outlined button-icon top-menu-icon" onclick="openMenu()">menu</span>`;
const menu = document.getElementsByClassName('menu')[0];

function openMenu() {
    menu.classList.add('show');
    topNavigation.innerHTML = '<span class="material-symbols-outlined button-icon top-icon" onclick="closeMenu()">undo</span>';
}

function closeMenu() {
    menu.classList.remove('show');
    topNavigation.innerHTML = topNavigationTemplate;
}

// Открытие/закрытие поиска в десктопной версии

const openSearchButton = document.getElementById("open-search-button")
const searchForm = document.getElementById("search-form")

function openTopSearch() {
    searchForm.style.display = "flex";
    openSearchButton.classList.add('hide')
}

function closeTopSearch() {
    searchForm.style.display = "none";
    openSearchButton.classList.remove('hide');
}

// Открытие/закрытие поиска в мобильной версии

const openMobileSearchButton = document.getElementById("open-mobile-search-button")
const search = document.getElementsByClassName('mobile-search')[0];
const logo = document.getElementsByClassName('logo')[0];

function openSearch() {
    search.style.display = 'flex';
    topNavigation.classList.add('hide');
    logo.classList.add('hide');
}

function closeSearch() {
    logo.classList.remove('hide');
    topNavigation.classList.remove('hide');
    search.style.display = 'none';
}

// Прокрутка к верху страницы

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
