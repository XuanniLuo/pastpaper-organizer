// export_to_json.js
// Usage: node export_to_json.js
// Put this file in the SAME folder as your data.js (the file containing
// `const topicMeta = {...}` and `const paper2Data = [...]`), and make sure
// data.js ends with:
//   module.exports = { topicMeta, paper2Data };
// (just add that one line to the bottom of your existing file)

const fs = require('fs');
const { topicMeta, paper2Data } = require('./data.js');

fs.writeFileSync(
  'paper2_data.json',
  JSON.stringify({ topicMeta, paper2Data }, null, 2)
);

console.log('Wrote paper2_data.json —', paper2Data.length, 'questions,', Object.keys(topicMeta).length, 'topics');
