'use strict';

const csvFile = __dirname + '/../../COVID19_Cases_Cantons_CH_total.csv';
const csv = require('csvtojson');
const request = require('request');
const cron = require('node-cron');

var allData;

// initial load
loadData();

// reaload each minute
cron.schedule('* * * * *', function () {
   loadData();
});

exports.allData = function (req, res) {
    res.json(allData);

};

exports.findByDate = function (req, res) {
    var data = allData.filter(row => row.date === req.params.date);
    res.json(data)
};

exports.findByArea = function (req, res) {
    var data = allData.filter(row => row.canton.toUpperCase() === req.params.area.toUpperCase()
    );
    res.json(data)
};

exports.findByDateAndArea = function (req, res) {
    var data = allData.filter(row => row.date === req.params.date
        && row.canton.toUpperCase() === req.params.area.toUpperCase()
    );
    res.json(data)
};

function loadData() {
    var dataLocation = 'https://raw.githubusercontent.com/openZH/covid_19/master/COVID19_Cases_Cantons_CH_total.csv';
    csv({
        checkType: true
    })
    //.fromFile(csvFile)
        .fromStream(request.get(dataLocation))
        .then(dataAsJson => {
            allData = dataAsJson;
            console.log(new Date().toISOString() + ': Data refreshed from: ' + dataLocation)
        });
}