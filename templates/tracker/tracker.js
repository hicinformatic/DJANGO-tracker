function visit() {
    this.params = [];
    this.add = function(key, value) {
        this.params.push(key + '=' + value);
    };
    this.visit = function() {
        alert('start');
        this.add('url', window.location.href);
        this.add('title', document.title);
        params = params.join('&');
        alert(params);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '{{ url }}/visit.html/{{ domain }}/', true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params); 
        this.params = [];
        alert('end');
    };
}
visit = new visit();
visit.add('height', window.screen.height);
visit.add('width', window.screen.width);
visit.visit();