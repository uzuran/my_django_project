document.querySelectorAll('.menu__item').forEach(item => {
    item.addEventListener('click', () => {
      document.getElementById('menu__toggle').checked = false;
    });
  });