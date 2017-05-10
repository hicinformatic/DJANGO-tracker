function visit(url, visitor) {
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
        if(typeof visitor !== 'undefined') {
            xhr.open("POST", this.url + '{{ domain }}/visitd.svg/' + visitor, true);
        }else{
            xhr.open("POST", this.url + '{{ domain }}/visitd.svg', true);
        }
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params); 
        this.params = [];
    };
    this.event = function(key, value) { 
        params = [ 'url='+window.location.href, 'title='+document.title ]
        var xhr = new XMLHttpRequest();
        if(typeof visitor !== 'undefined') {
            xhr.open("POST", this.url + '{{ domain }}/visitv.svg/' + visitor, true);
        }else{
            xhr.open("POST", this.url + '{{ domain }}/visitv.svg', true);
        }
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params.join('&')); 
    }
}