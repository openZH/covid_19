const csv = require('csv-validator');
const fs = require("fs").promises;
const path = require("path");

const csvFiles = process.argv.slice(2);

const validateSequentially = async csvFiles => {
    //field names starting with `_` are optional
    const headers = {
        date: /^\d{4}-\d{2}-\d{2}$/,
        _time: /^(([0-1]?[0-9]|2[0-3]):[0-5][0-9])?$/,
        abbreviation_canton_and_fl: /^[A-Z]{2}$/,
        _ncumul_tested: /^(\d+)?$/,
        _ncumul_conf: /^(\d+)?$/,
        _new_hosp: /^(\d+)?$/,
        _current_hosp: /^(\d+)?$/,
        _current_icu: /^(\d+)?$/,
        _current_vent: /^(\d+)?$/,
        _ncumul_released: /^(\d+)?$/,
        _ncumul_deceased: /^(\d+)?$/,
        _source: ''
    };
    const requiredKeys = [
      "date",
      "time",
      "abbreviation_canton_and_fl",
      "ncumul_tested",
      "ncumul_conf",
      "new_hosp",
      "current_hosp",
      "current_icu",
      "current_vent",
      "ncumul_released",
      "ncumul_deceased",
      "source"
    ];
    
    const cumulativeFields = [
      "ncumul_tested",
      "ncumul_conf",
      "ncumul_released",
      "ncumul_deceased"
    ];



  let failedChecks = 0;

  for (let csvFile of csvFiles) {
    const csvFilePath = path.resolve(csvFile);

    try {
        // check if file can be parsed
    	const parsed = await csv(csvFilePath, headers);

        //make sure all keys are present
        const hasAllKeys = requiredKeys.every(key => parsed[0].hasOwnProperty(key));
        if (!hasAllKeys) {
            throw new Error(`Required field missing`);
        }

        //check the cumulative fields
        var last = {};
        var errors = [];
        parsed.forEach(function (item, index) {
            cumulativeFields.forEach(function(col, col_idx) {
                if (col in last && last[col] && item[col] && parseInt(item[col]) < parseInt(last[col])) {
                    errors.push(`Row ${index+1}: cumulative field ${col}: ${item[col]} < ${last[col]}`);
                }
                if (item[col]) {
                    last[col] = item[col];
                }
            });
        });
        if (errors.length > 0) {
            throw new Error(errors);
        }
    } catch (e) {
      failedChecks++;
      if (Array.isArray(e)) {
          e = e.join('\n');
      }
      console.log(`× ${csvFile} failed the following checks:\n${e}`);
      continue;
	}
    console.log(`✓ ${csvFile} is valid.`);
  }

  return failedChecks;
};

const run = async () => {
  const failedChecks = await validateSequentially(csvFiles);

  if (failedChecks > 0) {
    process.exit(1);
  }
};

run().catch(e => console.error(e));
