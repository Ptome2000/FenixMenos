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
        $(this).next().fadeToggle(500);
    })

    $('div').filter(function() {
        return $.trim($(this).text()) === '';
    }).each(function() {
        $(this).prev().remove();
        $(this).remove();
    });

    $('#toggleDark').click(function() {
        let elem = $('html')
        let mode = elem.attr('data-bs-theme');
        if (mode === undefined) {
            elem.attr('data-bs-theme', 'dark');
            $('#toggleDark').text('White Mode');
            localStorage.setItem('data-bs-theme', 'dark');
        } else {
            elem.removeAttr('data-bs-theme');
            $('#toggleDark').text('Dark Mode');
            localStorage.removeItem('data-bs-theme');

        }
    });



    let mode = localStorage.getItem('data-bs-theme');
    if (mode === 'dark') {
        $('html').attr('data-bs-theme', 'dark');
    }

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

    $('[id^="GradeStudent"]').click(function() {
        let buttonId = $(this).attr('id');
        let modalId = buttonId.replace('GradeStudent', 'GradingModal');
        $('#' + modalId).css('display', 'block');
    });

    $('[id^="closeGradingModal"]').click(function() {
            var buttonId = $(this).attr('id');
            var modalId = buttonId.replace('closeGradingModal', 'GradingModal');
            $('#' + modalId).css('display', 'none');
        });

    $('#DeleteComments').click(function() {
        $('#DeleteCommentsModal').css('display', 'block');
    })

    $('#closeDeleteCommentsModal').click(function() {
        $('#DeleteCommentsModal').css('display', 'none');
    })

    if ($('.alert-success').length) {

    }

    $('.btn-check').click(function() {
        let isChecked = $('.btn-check').is(':checked');
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

    $(document).ready(function () {
        $('.user-photo').hover(
            function () { // Mouse over
                $(this).next('.user-data').slideDown(400); // Usa slideDown para mostrar
            },
            function () { // Mouse out
                $(this).next('.user-data').slideUp(400); // Usa slideUp para ocultar
            }
        );
    });


});
