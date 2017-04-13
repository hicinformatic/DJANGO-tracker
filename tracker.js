var visit = visit || {};
visit.domains;
visit.params = [];
visit.add = function(key, value) {
    this.params.push(key + '=' + value);
}
visit.visit = function(url, params) {
    params = params.join('&');
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url + 'visit.html', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(params); 
    this.params = [];
}