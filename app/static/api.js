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
        contentType: 'application/json',
        success: function (r) {
            log('success,', method, url);
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

chart.get = function (url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response, response);
};

chart.post = function(url, form, success, error) {
    var method = 'post';
    this.ajax(url, method, form, success, error);
};

chart.serverStatus = function (form, success, error) {
    var url = 'api/status';
    this.post(url, form, success, error);
};
