// import * as http from "http"
const http = require('http')
const express = require('express')
const dotenv = require('dotenv')
const bodyparser = require('body-parser')



function latLngToTileCoords(lat, lng, zoom) {
    let n = Math.pow(2, zoom);
    let xTile = Math.floor(n * ((lng + 180) / 360));
    let latRad = (lat * Math.PI) / 180;  // Convert latitude to radians
    let yTile = Math.floor(n * (1 - (Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI)) / 2);
    return {xTile: xTile, yTile: yTile};
}

// let tileCoords = latLngToTileCoords(40.7128, -74.0060, 8);
// console.log(tileCoords);

// console.log("start");

let app = express()
let app_port = 8083

app.get("/toxy", (req, res) =>{


    // exaple http://localhost:8083/toxy?zoom=8&lng=-74.0060&lat=40.7128


    if(req.query.zoom === undefined || req.query.zoom === null || req.query.zoom === '') {
        res.status(404).send('bad zoom')
        res.end()        
    }
    if(req.query.lng === undefined || req.query.lng === null || req.query.lng === ''){
        res.status(404).send('bad lng longitude')
        res.end()        
    }
    if(req.query.lat === undefined || req.query.lat === null || req.query.lat === ''){
        res.status(404).send('bad lat latitude')
        res.end()        
    }

    let tile = latLngToTileCoords(parseInt(req.query.lat), parseInt(req.query.lng), parseInt(req.query.zoom))
    // return {xTile: xTile, yTile: yTile};
    tile.zoom = parseInt(req.query.zoom)
    res.setHeader('Content-Type', 'application/json');
    res.status(200).send(JSON.stringify(tile))
    res.end()

    return;

})

app.use("*", (req, res) => {
    console.log("app procesing /")
    res.status(400).send("debug stop")
    res.end()
})  


let tileCoords = latLngToTileCoords(40.7128, -74.0060, 8);

// Accessing values using dot notation
console.log("xTile:", tileCoords.xTile);
console.log("yTile:", tileCoords.yTile);

// Accessing values using bracket notation
console.log("xTile:", tileCoords['xTile']);
console.log("yTile:", tileCoords['yTile']);

http_server = http.createServer(app)
http_server.listen(app_port)
