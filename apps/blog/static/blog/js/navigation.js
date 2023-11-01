'use strict'; 

// Показать/скрыть содержание подкатегории

let subcategories = document.getElementsByClassName('content__title');

for (let i = 0; i < subcategories.length; i++) {
    subcategories[i].addEventListener('click', function() {
        this.classList.toggle('active');
        let linksArticles = this.nextElementSibling;
        if (linksArticles.classList.contains('show')) {
            linksArticles.classList.remove('show');
        } else {
            linksArticles.classList.add('show');
        }
  });
} 

// Открытие/закрытие верхнего меню в мобильной версии

const topNavigation = document.getElementsByClassName('top-navigation')[0];
const menu = document.getElementsByClassName('menu')[0];
const openMenuButton = document.getElementById('menuOpen')
const closeMenuButton = document.getElementById('menuClose')

function openMenu() {
    menu.classList.add('show');
    openMenuButton.style.display = 'none'
    closeMenuButton.style.display = 'inline'
}

function closeMenu() {
    menu.classList.remove('show');
    openMenuButton.style.display = 'inline'
    closeMenuButton.style.display = 'none'
}

// Открытие/закрытие поиска в мобильной версии

const openMobileSearchButton = document.getElementById('mobile-search_open')
const search = document.getElementsByClassName('mobile-search_wrapper')[0];
const logo = document.getElementsByClassName('logo')[0];

function openSearch() {
    search.style.display = 'flex';
    logo.classList.add('hide');
    openMobileSearchButton.style.display = 'none';
}

function closeSearch() {
    logo.classList.remove('hide');
    search.style.display = 'none';
    openMobileSearchButton.style.display = 'block';
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
