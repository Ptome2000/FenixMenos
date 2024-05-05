document.addEventListener('DOMContentLoaded', function() {
    // Toggle dropdown
    var dropdownToggle = document.getElementById('navbarDropdown');
    dropdownToggle.addEventListener('click', function(event) {
        event.preventDefault();  // Impede o link de navegar
        document.getElementById("myDropdown").classList.toggle("show");
    });

    // Fechar o dropdown clicando fora
    window.onclick = function(event) {
        if (!event.target.matches('.nav-link')) {
            var dropdowns = document.getElementsByClassName("dropdown-menu");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }

      $(".group-header ").click(function() {
    let element = $(this).next();
    element.fadeToggle(500);
  })

  $('#togglePostOptions').click(function() {
    $('#PostOptions').toggle();
  });

    document.querySelector('.form-inline').addEventListener('submit', function(e) {
    e.preventDefault(); // Impede o envio do formulário
    var searchValue = document.querySelector('.form-inline input[type="search"]').value;
    // Aqui você pode adicionar o código para realizar a pesquisa
    console.log("Pesquisando por:", searchValue);
    // Por exemplo, redirecionar para uma URL com o termo de pesquisa
    window.location.href = '/search/?q=' + encodeURIComponent(searchValue);
});

    document.addEventListener('DOMContentLoaded', function() {
    var submenus = document.querySelectorAll('.submenu > a');
    submenus.forEach(function(submenu) {
        submenu.addEventListener('click', function(e) {
            e.preventDefault();
            var childMenu = this.nextElementSibling;
            if (childMenu.style.display === 'block') {
                childMenu.style.display = 'none';
            } else {
                childMenu.style.display = 'block';
            }
        });
    });
});


});
