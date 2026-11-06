/* Pure full-book search contracts — no Chromium/npm dependencies. */
'use strict';
import assert from 'node:assert/strict';
import search from '../reader-search.js';

assert.equal(search.normalize('  Émpire   ECONOMY '), 'empire economy');
assert.equal(search.match('The conference ended in Bandung, 1955.', '1955 bandung'), true);
assert.equal(search.match('Bandung was in Indonesia', 'bandung kenya'), false);
assert.equal(search.match('', ''), false);
assert.equal(search.mappedText('Crème').folded, 'creme');
const snippet = search.snippetParts('Europe debated the term Pan-Turanianism.', 'pan-turanianism', 80);
assert.equal(snippet.parts.filter(p=>p.hit).map(p=>p.text).join(''), 'Pan-Turanianism');
const fixtures = [
  {index:0,chapter:'0',normalized:search.normalize('The Imperial Mindset'),text:'The Imperial Mindset',kind:'heading'},
  {index:1,chapter:'0',normalized:search.normalize('Imperial landmasses matter'),text:'Imperial landmasses matter',kind:'passage'},
  {index:2,chapter:'2',normalized:search.normalize('Empire explained'),text:'Empire explained',kind:'chapter'}
];
const found = search.find(fixtures,'imperial');
assert.deepEqual(found.map(x=>x.entry.index),[0,1]);
assert.equal(search.find(fixtures,'nonexistent').length,0);
const hiddenFixtures = fixtures.concat([
  {index:3,chapter:'3',normalized:search.normalize('Revision summary of empire'),
   text:'Revision summary of empire',kind:'passage',revision:true}
]);
assert.equal(search.find(hiddenFixtures,'revision',{includeRevision:false}).length,0);
assert.equal(search.find(hiddenFixtures,'revision',{includeRevision:true}).length,1);
console.log('PASS: full-book case/accent matching, excerpts and relevance');
