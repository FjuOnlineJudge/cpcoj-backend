$(document).ready(function() {
    $.ajax({
        type: 'GET',
        url: '/contest/getinfo/0',
        dataType: "Json"
    }).done(function(json))
})