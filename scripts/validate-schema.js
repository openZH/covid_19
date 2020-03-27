const csval = require("csval");
const fs = require("fs").promises;
const path = require("path");

const DIR = path.resolve(process.argv[2] || process.cwd());

const validateSequentially = async csvFiles => {
  const rules = await csval.readRules(path.join(DIR, "schema.json"));

  let failedChecks = 0;

  for (let csvFile of csvFiles) {
    const csv = await csval.readCsv(path.join(DIR, csvFile));
    const parsed = await csval.parseCsv(csv);
    let valid = false;
    try {
      valid = await csval.validate(parsed, rules);
    } catch (e) {
      failedChecks++;
      console.log(`× ${csvFile} failed the following checks:${e.message}\n`);
    }
    if (valid) {
      console.log(`✓ ${csvFile} is valid.`);
    }
  }

  return failedChecks;
};

const run = async () => {
  const csvFiles = (await fs.readdir(DIR)).filter(f => f.match(/\.csv$/));
  const failedChecks = await validateSequentially(csvFiles);

  if (failedChecks > 0) {
    process.exit(1);
  }
};

run().catch(e => console.error(e));
