/* jshint esversion: 6 */
/* jshint node: true */
/* jshint browser: true */
/* jshint jquery: true */
'use strict';

const URL_RANDOM = "https://music-shack-demo.herokuapp.com/api/instruments/random"

async function requestData() {
    return fetch(`${URL_RANDOM}`)
    .then(response => response.json())
    .then(json => printData(json.random))
    .catch(error => console.log(error))
}

function printData(instrument) {
    let responseDiv = document.querySelector("#response");
    responseDiv.setAttribute("class", "alert-success m-3 p-2 align-self-center");
    responseDiv.innerHTML = instrument.name + " is a " + instrument.category + " instrument. At Music Shack, we currently have " + instrument.quantity + " of these in stock. Full Price: " + instrument.price + " USD & Rental Fee: " + instrument["rental fee"] + " USD per month.";
}