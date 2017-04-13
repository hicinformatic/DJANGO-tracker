function visit(url=null) {
    this.params = [];
    this.url = url;
    this.add = function(key, value) {
        this.params.push(key + '=' + value);
    };
    this.visit = function() {
        this.add('url', window.location.href);
        this.add('title', document.title);
        params = this.params.join('&');
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url + '/visit.html/{{ domain }}/', true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send(params); 
        this.params = [];
    };
    this.start function() {
        if( this.url == null ) {
            alert('null');
            this.url = ''
        }else{
            alert('pas null');
            this.url = '//' + this.url
        }
    }
    this.start();
}
visit = new visit();
visit.add('height', window.screen.height);
visit.add('width', window.screen.width);
visit.visit();