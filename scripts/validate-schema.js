const csval = require("csval");
const fs = require("fs").promises;

const rules = require("../schema.json");

const validateSequentially = async csvFiles => {
  let failedChecks = 0;

  for (let csvFile of csvFiles) {
    const csv = await csval.readCsv(csvFile);
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
  const csvFiles = (await fs.readdir(process.cwd())).filter(f =>
    f.match(/^COVID19_.+\.csv$/)
  );

  const failedChecks = await validateSequentially(csvFiles);

  if (failedChecks > 0) {
    process.exit(1);
  }
};

run().catch(e => console.error(e));
