'use strict';

const csvFile = __dirname + '/../../COVID19_Cases_Cantons_CH_total.csv';
const csv = require('csvtojson');
const request = require('request');
var allData;

csv({
    checkType: true
})
    //.fromFile(csvFile)
    .fromStream(request.get('https://raw.githubusercontent.com/openZH/covid_19/master/COVID19_Cases_Cantons_CH_total.csv'))
    .then(dataAsJson => allData = dataAsJson);

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

