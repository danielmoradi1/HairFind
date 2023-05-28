$('#deleteBtn').click(function (event) {
    event.preventDefault(); // Prevent form submission

    Swal.fire({
        title: 'Ta bort bekräftelse',
        text: 'Är du säker på att du vill ta bort ditt konto?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Ja',
        cancelButtonText: 'Avbryt'
    }).then(function (result) {
        if (result.isConfirmed) {
            var orgNumber = $('#orgNumberInput').val();
            var username = $('#usernameInput').val();

            $.ajax({
                url: '/delete_salon_account',
                type: 'POST',
                data: {
                    org_number: orgNumber,
                    username: username
                },
                success: function (response) {
                    if (response.status === 'success') {
                        Swal.fire({
                            title: 'Kontot raderat',
                            text: 'Ditt konto har raderats!',
                            icon: 'success'
                        }).then(function () {
                            window.location.href = response.redirect;
                        });
                    } else if (response.status === 'error') {
                        Swal.fire({
                            title: 'Fel',
                            text: response.message,
                            icon: 'error'
                        });
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    Swal.fire({
                        title: 'Fel',
                        text: 'Radera först tjänster!',
                        icon: 'error'
                    });
                }
            });
        }
    });
});
