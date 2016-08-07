/**
 * Created by Gabriel on 2016/8/7.
 */

var log = function () {
    console.log(arguments);
};

var chart = {
    data: {}
};

chart.ajax = function (url, method, form, success, error) {
    var request = {
        url: url,
        type: method,
        data: data,
        contentType: 'application/json',
        success: function (r) {
            log('success, ', method, url);
            success(r)
        },
        error: function (err) {
            r = {
                success: false,
                data: err
            };
            log('chart err', url, err);
            error(r);
        }
    };
    if (method === 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};

bs.get = function (url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response, response);
};
