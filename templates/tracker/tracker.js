var visit = visit || {};
visit.id = '{{ domain }}';
visit.params = [];
visit.add = function(key, value) { this.params.push(key + '=' + value); }
visit.visit = function() {
    params = params.join('&');
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '{{ url }}/visit.html/{{ domain }}/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(params); 
    this.params = [];
}