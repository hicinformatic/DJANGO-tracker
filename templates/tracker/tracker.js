var visit = visit || {};
visit.params = [];
visit.add = function(key, value) { this.params.push(key + '=' + value); }
visit.visit = function() {
    alert('start');
    this.add('url', this.url);
    this.add('title', this.document.title);
    params = params.join('&');
    alert(params);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '{{ url }}/visit.html/{{ domain }}/', true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(params); 
    this.params = [];
    alert('end');
}