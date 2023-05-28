
$(document).ready(function () {
    $('#deleteBtn').click(function () {
        Swal.fire({
            title: 'Ta bort bekräftelse',
            text: 'Är du säker på att du vill ta bort ditt konto?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Ja',
            cancelButtonText: 'Avbryt'
        }).then(function (result) {
            if (result.isConfirmed) {
                deleteAccount();
            }
        });
    });

    function deleteAccount() {
        var username = $('#deleteBtn').data('username');
        $.ajax({
            url: '/delete_user/' + username,
            type: 'POST',
            success: function (response) {
                if (response.status === 'success') {
                    Swal.fire({
                        title: 'Kontot raderat',
                        text: 'Ditt konto har raderats!',
                        icon: 'success'
                    }).then(function () {
                        window.location.href = response.redirect;
                    });
                } else {
                    Swal.fire({
                        title: 'Fel',
                        text: response.message,
                        icon: 'error'
                    });
                }
            }
        });
    }
});
