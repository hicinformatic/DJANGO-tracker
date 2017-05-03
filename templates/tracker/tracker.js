function visit(url) {
    this.params = [];
    this.url;
    this.add = function(key, value) { this.params.push(key + '=' + value); };
    this.start = function() { this.url = typeof url !== 'undefined' ? '//' + url : ''; }
    this.start();
    this.visit = function() {
        this.add('url', window.location.href);
        this.add('title', document.title);
        params = this.params.join('&');
        var xhr = new XMLHttpRequest();
        xhr.open("POST", this.url + '{{ domain }}/visit.html', true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params); 
        this.params = [];
    };
}