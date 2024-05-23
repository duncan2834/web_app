// script.js
document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.nav-item.dropdown');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseover', () => {
            dropdown.querySelector('.nav-link').setAttribute('aria-expanded', true);
            dropdown.querySelector('.nav-link').classList.add("show");
            dropdown.querySelector('.dropdown-menu').classList.add("show");
            
        });

        dropdown.addEventListener('mouseout', () => {
            dropdown.querySelector('.nav-link').setAttribute('aria-expanded', false);
            dropdown.querySelector('.nav-link').classList.remove("show");
            dropdown.querySelector('.dropdown-menu').classList.remove("show");
        });
    });
});

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
  if (window.scrollY > 85) { // Change 100 to the desired scroll position
    navbar.classList.add('hidden');
  } else {
    navbar.classList.remove('hidden');
  }
});

