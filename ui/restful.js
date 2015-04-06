function request(method) {
    var url = $('#tf-url').val();

    try {
        var parameters = JSON.parse($('#ta-params').val());
    } catch (err) {
    }

    $.ajax({
        url: url,
        method: method,
        data: parameters,
        dataType: 'json',
        success: function(data) {
            $('#result').text(JSON.stringify(data, null, 2));
        },
        error: function(xhr) {
            $('#result').text(xhr.responseText);
        }
    });
}
