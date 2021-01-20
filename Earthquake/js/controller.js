/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';

// ****************************** NEWS ******************************  -->

var myArticleModel = new ArticleList();
var myArticleView = new ArticleView(myArticleModel);

async function getData(url) {
    return fetch(url)
    .then(response => response.json())
    .catch(error => console.log(error));
}

async function getNews(input){
    let text = await Promise.all([getData("https://newsapi.org/v2/everything?qInTitle="+input+
                                          "+Earthquake&apiKey=PRIVATE")]);
    return text;
}

async function getInfo(){

    let input = document.querySelector("#inputArticle").value;

    myArticleModel.clear();

    let text = await getNews(input);
    let articleCounts = text[0]["totalResults"];

    // error message
    if (articleCounts == 0) {
        let warning = document.createElement("p");
        warning.setAttribute("class", "alert-danger");
        warning.setAttribute("id", "remove");
        warning.innerHTML = "Sorry, there's no news article for your search.";
        warning.onclick = function() {warning.remove()};
        let body = document.querySelector("#errorMessage");
        body.appendChild(warning);
        return;
    } else {

        // success: receive articles' info
        for (let i = 0; i < articleCounts - 1 && i < 10; i++) {
            let title = text[0]["articles"][i]["title"];
            let description = text[0]["articles"][i]["description"];
            let url = text[0]["articles"][i]["url"];
            let publishedAt = text[0]["articles"][i]["publishedAt"];
            
            let anArticle = new Article(input, title, description, url, publishedAt);
            myArticleModel.addArticle(anArticle);
        }
    }
}

// ****************************** MAP & Earthquake ******************************  -->

async function earthquake(){ // default: earthquake data between 03-25-2020 and 04-03-2020 (NOW)

    let earthquakeData = await Promise.all([getData("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=03-25-2020&endtime=04-03-2020&orderby=time")]);
    return earthquakeData;
}

var locationMap = {};

async function data() { 
    // aapend UGSG API data to location map dictionary
    // 3 parameters to obtain: latitude, longitude, magnitude

    for (let i = 0; i < 100; i++) { // only feed in up to 100 data points for now
        let text = await earthquake();
        let longitude = text[0]["features"][i]["geometry"]["coordinates"][0];
        let latitude = text[0]["features"][i]["geometry"]["coordinates"][1]; 
        // 3 values: 0-longitude 1-latitude 2-depth (we don't need 2-depth)
        
        let center = {lat: latitude, lng: longitude};
        let magnitude = text[0]["features"][i]["properties"]["mag"];
        locationMap[i] = {center, magnitude}
    }
}

var map;

function initializeMap() {
  
    // default map view
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 40, lng: -160},
        mapTypeId: 'roadmap'
    });

    if (localStorage.getItem("savedCoordinates") != null) {
        // load saved coordinates, if exist
        let savedZoom = JSON.parse(localStorage.getItem("savedCoordinates"))[1];
        let savedCenter = JSON.parse(localStorage.getItem("savedCoordinates"))[0];
        map.setZoom(savedZoom);
        map.setCenter(savedCenter);
    }
    
    // adding gray circles to represent recent earthquake event
    // the radius of the circles represents magnitude (relative to other circles)
    for (var location in locationMap) {
        var locationCircle = new google.maps.Circle({
            strokeColor: '#9F9D9D',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#9F9D9D',
            fillOpacity: 0.35,
            map: map,
            center: locationMap[location].center,
            radius: Math.sqrt(Math.abs(locationMap[location].magnitude)) * 100000
        });
    }
}

function updatePositionByCountry() {

    var countryName = document.querySelector("#inputArticle").value;
    
    // takes care of errors when input value is not valid
    if (countryName in dict) {
        let latitude = parseFloat(dict[countryName][0]);
        let longitude = parseFloat(dict[countryName][1]);
        map.setZoom(5);
        map.setCenter({lat: latitude, lng: longitude});
    }
}

// ****************************** Local Storage ******************************

function saveArticle() {
    // save search result, articles feed
    let articleList = localStorage.getItem("articleList");
    articleList = articleList ? JSON.parse(articleList) : [];
    articleList.push(myArticleModel._list);
    localStorage.setItem("articleList", JSON.stringify(myArticleModel._list));
}

function saveCoordinates() {
    // save current map coordinates: center({lat, lng}) & zoom
    let savedCoordinates = localStorage.getItem("savedCoordinates");
    savedCoordinates = savedCoordinates ? JSON.parse(savedCoordinates) : [];
    var lst = [map.getCenter(), map.getZoom()];
    localStorage.setItem("savedCoordinates", JSON.stringify(lst));
}

function loadArticle() {

    // load saved articles
    let articleList = JSON.parse(localStorage.getItem("articleList"));
    if (!articleList) {
        return;
    }
    for (let i of articleList) {
        let ip = i._input;
        let tt = i._title;
        let dc = i._description;
        let ur = i._url;
        let pa = i._publishedAt;

        let nouveauArticle = new Article(ip, tt, dc, ur, pa);
        myArticleModel.addArticle(nouveauArticle);
    }

}

function clearEverything() { // clear local storage

    // clear articles from feed & from local storage
    myArticleModel.clear();
    saveArticle();

    // clear saved coordinates from local storage
    localStorage.removeItem("savedCoordinates");

    // navigate back to default coordinate
    map.setZoom(3);
    map.setCenter({lat: 40, lng: -160});
}


// ****************************** Window Onload / Reload Session ****************************** 

window.onload = async function() {
    loadArticle();
    await data();
    initializeMap();
};