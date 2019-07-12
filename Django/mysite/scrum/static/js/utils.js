function loginTeam() {
    // console.log('updateform');
    var updateform = $('#' + 'loginform');
    var csrftoken = getCookie('csrftoken');
    // var name = document.getElementById("company");
    // var selectedvalue = name.options[name.selectedIndex].value;
    // console.log(selectedvalue);
    console.log("in login")
    $.ajax({
        type: "POST",
        url: '/loginweb/',
        data:updateform.serialize() + '&csrfmiddlewaretoken=' + csrftoken,
        success: function(message) {
            if (message =='success') {
                alert('Updated Successfully');
                window.location.href = "/";

            }

            else
            {
                alert('Error occured');
            }
        },
        error: function(xhr, errmsg, err) {
            alert('Error');
        },
    });
}

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
};