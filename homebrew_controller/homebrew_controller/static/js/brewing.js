$(document).ready(function () {
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    //Ajax call
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.next').click(function() {
        var select = $('.step-list form').find('select');
        $.ajax({
            type: 'GET',
            url: '/set_step/',
            success: function(data) {
                var brew_steps = data['data'];
                for(var i = 0; i < brew_steps.length; i++) {
                    select.append($("<option></option>")
                                        .attr("step_name", brew_steps[i].name)
                                        .text(brew_steps[i].name));
                };
                $('.step-list').prop('hidden', '');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('.submit-step').click(function() {
        var data = $('.step-form').serialize();
        alert(data);
        $.ajax({
            type: 'POST',
            url: '/set_step/',
            data: data,
            success: function(data) {
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('.pause').click(function() {
        $.ajax({
            type: 'POST',
            url: '/brew/set_status/',
            data: {'brew': brew, 'is_active': 0},
            success: function(data) {
                $('.pause').prop('hidden', 'true');
                $('.start').prop('hidden', '');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('.play').click(function() {
        $.ajax({
            type: 'POST',
            url: '/brew/set_status/',
            data: {'brew': brew, 'is_active': 1},
            success: function(data) {
                $('.start').prop('hidden', 'true');
                $('.pause').prop('hidden', '');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});