// ------------------------------------------------------------- HELPERS
function añadirOpcion(numero) {
    var html = '<div class="control-group">\n'+
                    '<label class="control-label" for="inputOpcion'+numero+'">Opción '+numero+'</label>\n'+
                    '<div class="controls">\n'+
                        '<input name="choice" type="text" id="inputOpcion'+numero+'" placeholder="¿Opción?">\n'+
                    '</div>'+
                '</div>\n';
    $("#opciones").append(html)
    $("#inputOpcion"+numero).focus();
}

function serializarVotacion() {
    var json_object = {};
    json_object.title = "";
    json_object.choices = [];
    var serial = $("form").serializeArray();
    json_object.title = serial[0].value;
    for (var i = 1; i<serial.length; i++){
        json_object.choices[i-1] = {"choice": serial[i].value};
    }
    //console.log(json_object);
    //return {"title":"Hola!","choices": [{"choice":"uno"},{"choice":"dos"},{"choice":"tres"}]};
    return json_object;
}

function insertarVotacion(id, titulo) {
    var html = '<li><a href="/polls/'+id+'/">'+titulo+'</a></li>';
    $("#votaciones").append(html);
}


// ------------------------ DJANGO Cross Site Request Forgery protection
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});


