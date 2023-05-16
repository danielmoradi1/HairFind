$(document).ready(function () {
    $('form').on('submit', function (event) {
        $.ajax({
            data: {
                username: $('#username').val(),
                password: $('#password').val()
            },
            type: 'POST',
            url: '/login_customer'
        })
            .done(function (data) {
                if (data.error) {
                    $('#errorAlert').text(data.error).show();
                    $('#successAlert').hide();
                } else {
                    $('#successAlert').text(data['you are successfuly logged in ']).show();
                    $('#errorAlert').hide();
                }
            });
    });
});


