'use strict';
module.exports = function(app) {
    var controller = require('./controller');

    app.route('/api')
        .get(controller.allData);

    app.route('/api/date/:date')
        .get(controller.findByDate);

    app.route('/api/area/:area')
        .get(controller.findByArea);

    app.route('/api/date/:date/area/:area')
        .get(controller.findByDateAndArea);

};