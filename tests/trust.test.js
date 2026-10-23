import assert from 'node:assert/strict';
import {makeReport} from '../web/trust.js';
const r=makeReport('<script>bad</script>','Incorrect scripture','check verse');
assert.equal(r.content,'<script>bad</script>');assert.match(r.status,/not submitted/);assert.ok(r.id);assert.ok(Date.parse(r.createdAt));
assert.equal(makeReport('x'.repeat(20000),'Other','x'.repeat(3000)).content.length,16000);
assert.equal(makeReport('x','Other','x'.repeat(3000)).comment.length,2000);
assert.throws(()=>makeReport('x','invalid'));
console.log('Report draft validation passed');
