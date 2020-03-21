'use strict';
module.exports = function(app) {
    var controller = require('./controller');

    app.route('/covid19')
        .get(controller.allData);

    app.route('/covid19/date/:date')
        .get(controller.findByDate);

    app.route('/covid19/area/:area')
        .get(controller.findByArea);

    app.route('/covid19/date/:date/area/:area')
        .get(controller.findByDateAndArea);

};