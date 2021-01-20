/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';

class ArticleView {

    constructor(model){
        model.subscribe(this.redrawList.bind(this));
    }

    redrawList(listOfArticles, msg) {

        let outputContainer = document.querySelector("#output-container");
        outputContainer.innerHTML = "";

        for (let article of listOfArticles){

            let articleCell = document.createElement("div");
            articleCell.className = "custom-border";

            // Title
            let articleTitle = document.createElement("h4");
            articleTitle.setAttribute("class", "text-primary");
            articleTitle.appendChild(document.createTextNode(article.title));

            // Date & Time published
            let articlePublishedAt = document.createElement("div");
            articlePublishedAt.setAttribute("class", "font-weight-bold");
            articlePublishedAt.appendChild(document.createTextNode(article.publishedAt));

            // Desciption
            let articleDescription = document.createElement("p");
            articleDescription.appendChild(document.createTextNode(article.description));

            // link: Read More
            let articleURL = document.createElement("a");
            articleURL.setAttribute("href", article.url);
            articleURL.setAttribute("target", "_blank");
            articleURL.appendChild(document.createTextNode("Read More"));

            articleCell.appendChild(articleTitle);
            articleCell.appendChild(articlePublishedAt);
            articleCell.appendChild(articleDescription);
            articleCell.appendChild(articleURL);

            outputContainer.appendChild(articleCell);
        }
    }

}