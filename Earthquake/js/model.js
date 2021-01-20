/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';

class Article {
    constructor(input, title, description, url, publishedAt){
        this._input = input;
        this._title = title;
        this._description = description;
        this._url = url;
        this._publishedAt = publishedAt;
    }

    get input() {return this._input;}
    get title() {return this._title;}
    get description() {return this._description;}
    get url() {return this._url;}
    get publishedAt() {return this._publishedAt;}

}

class Subject {
    constructor() {
        this.handlers = [];
    }

    subscribe(func) {
        this.handlers.push(func);
    }

    unsubscribe(func) {
        this.handlers = this.handlers.filter(item => item != func);
    }

    publish(msg, obj) {
        let scope = obj || window;
        for (let f of this.handlers) {
            f(scope, msg);
        }
    }
}

class ArticleList extends Subject {
    constructor() {
        super();
        this._list = [];
    }

    get articles() {return this._list;} // ??

    addArticle(newArticle){
        this._list.push(newArticle);
        this.publish("New article added", this);
    }

    clear() {
        this._list = [];
        this.publish("Clear all articles", this);
    }

    [Symbol.iterator]() {
        let idx = -1;
        return {
            next: () => ({value: this._list[++idx], done: !(idx in this._list)})
        };
    }

}

