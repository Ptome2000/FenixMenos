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


});
