function visit(visitor, url) {
    this.visitor;
    this.url;
    this.domain;
    this.visitd;
    this.visitv;
    this.params = [];
    this.start = function() {
        this.url = typeof url !== 'undefined' ? '//' + url : '';
        this.domain = '{{ domain }}';
        this.visitd = this.url + this.domain + '/visitd.svg';
        this.visitv = this.url + this.domain + '/visitv.svg';
        if(typeof visitor !== 'undefined') {
            this.visitor = visitor;
            this.visitd += this.visitor;
            this.visitv += this.visitor;
        }
    };
    this.add = function(key, value) { this.params.push(key + '=' + value); };
    this.visit = function() {
        this.add('url', window.location.href);
        this.add('title', document.title);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", this.visitd, true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(this.params.join('&'));
        this.params = [];
    };
    this.event = function(key, value) { 
        params = [ key+'='+value, 'url='+window.location.href, 'title='+document.title ]
        var xhr = new XMLHttpRequest();
        xhr.open("POST", this.visitd, true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params.join('&')); 
    };
    this.start();
}