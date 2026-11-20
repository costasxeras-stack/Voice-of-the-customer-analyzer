import { initModel } from "@energetic-ai/embeddings";
import { modelSource } from "@energetic-ai/model-embeddings-en";
import fs from "fs";
const sents = JSON.parse(fs.readFileSync("work/sents.json", "utf8"));
const n = Number(process.argv[2] || sents.length);
const model = await initModel(modelSource);
const t0 = Date.now(); const out = [];
for (let i = 0; i < n; i += 256) { const e = await model.embed(sents.slice(i, Math.min(n, i + 256)).map(s => s[1])); out.push(...e.map(v => Array.from(v))); }
const buf = Buffer.alloc(out.length * out[0].length * 4); let k = 0;
out.forEach(v => v.forEach(x => { buf.writeFloatLE(x, k); k += 4; }));
fs.writeFileSync("work/emb.f32", buf);
console.log(n, out[0].length, ((Date.now() - t0) / 1000).toFixed(1) + "s");
