// Comprueba el renderer real con un reproductor/eventos controlados, sin red.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const listeners = new Map();
const audios = [];
let bloquear = false;
class AudioPrueba {
  constructor(src) { this.src=src; this.intentos=0; this.pausas=0; audios.push(this); }
  play() { this.intentos++; return bloquear ? Promise.reject(new Error('Bloqueado')) : Promise.resolve(); }
  pause() { this.pausas++; }
}
const documento = {
  addEventListener(nombre, fn) { if(!listeners.has(nombre))listeners.set(nombre,new Set()); listeners.get(nombre).add(fn); },
  removeEventListener(nombre, fn) { listeners.get(nombre)?.delete(fn); },
};
const render = vm.runInNewContext('('+fs.readFileSync('assets/aviso_tiempo.js','utf8').replace('export default','')+')',
  {window:{},document:documento,Audio:AudioPrueba});
let cleanup=()=>{};
const tick=(ronda,restantes)=>{cleanup();cleanup=render({data:{ronda,restantes,audio:'data:audio/mpeg;base64,prueba'}})};
async function main() {
  tick('ronda1',60);tick('ronda1',5);assert.equal(audios[0].intentos,0);
  tick('ronda1',4);assert.equal(audios[0].intentos,1);
  tick('ronda1',4);tick('ronda1',3);tick('ronda1',1);cleanup();
  assert.equal(audios[0].intentos,1);assert.equal(audios[0].pausas,0);
  tick('ronda2',60);assert.equal(audios[0].pausas,1);
  tick('ronda2',3);assert.equal(audios[1].intentos,1);
  tick('ronda3',0);assert.equal(audios[2].intentos,0);
  bloquear=true;tick('ronda4',4);await Promise.resolve();
  tick('ronda4',3);assert.equal(audios[3].intentos,1);
  bloquear=false;for(const f of listeners.get('keydown'))f();await Promise.resolve();
  assert.equal(audios[3].intentos,2);
  tick('ronda4',1);for(const f of listeners.get('pointerdown'))f();
  assert.equal(audios[3].intentos,2);
  cleanup();assert.equal([...listeners.values()].reduce((s,x)=>s+x.size,0),0);
  console.log('Aviso: umbral de 4 s, silencio a 5 s, una vez por ronda, salto a 3 s, rejuego y desbloqueo por gesto correctos.');
}
main().catch(e=>{console.error(e);process.exitCode=1});
