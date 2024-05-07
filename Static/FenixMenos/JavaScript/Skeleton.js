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
        let content = $(this).next();
        content.fadeToggle(500);
    })

    $('.group-content').each(function() {
        console.log(!this.hasChildNodes());
        if (!this.hasChildNodes()) {
            let header = $(this).attr('id').replace('content', 'header');
            header.remove();
            $(this).remove();
        }
    })

    $('#togglePostOptions').click(function() {
        $('#PostOptions').toggle();
    });

    $('#AnswerPost').click(function() {
        $('#AnswerModal').css('display', 'block');
    })

    $('#closeAnswerModal').click(function() {
        $('#AnswerModal').css('display', 'none');
    })

    $('#DeletePost').click(function() {
        $('#DeleteModal').css('display', 'block');
    })

    $('#closeDeleteModal').click(function() {
        $('#DeleteModal').css('display', 'none');
    })

    $('#DeleteComments').click(function() {
        $('#DeleteCommentsModal').css('display', 'block');
    })

    $('#closeDeleteCommentsModal').click(function() {
        $('#DeleteCommentsModal').css('display', 'none');
    })

    $('.btn-check').click(function() {
        // Check if any element with class "btn-check" is checked
        let isChecked = $('.btn-check').is(':checked');

        // Check the result
        if (isChecked) {
            $('#DeleteComments').css('display', 'block');
        } else {
            $('#DeleteComments').css('display', 'none');
        }
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
