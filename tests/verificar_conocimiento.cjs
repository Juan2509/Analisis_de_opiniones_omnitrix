// Solo contra tests/app_conocimiento_visual.py; nunca consume cuota de Gemini.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('../.herramientas/browser-check/node_modules/playwright-core');
const url = process.argv[2];
if (process.argv[3] !== '--simulado' || !url || !['127.0.0.1','localhost'].includes(new URL(url).hostname)) {
  throw new Error('Indicar URL local del servidor visual y --simulado.');
}
const out = path.resolve('.herramientas/browser-check');
async function main() {
 const browser = await chromium.launch({headless:true, executablePath:process.env.OMNITRIX_BROWSER || 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'});
 const resultados=[];
 let paginaActual;
 try {
  for(const viewport of [{width:1440,height:1000},{width:390,height:844}]) {
   const context=await browser.newContext({viewport,reducedMotion:'reduce'});
   const externos=[],errores=[];
   await context.route('**/*',r=>{if(['127.0.0.1','localhost'].includes(new URL(r.request().url()).hostname))return r.continue();externos.push(r.request().url());return r.abort()});
   const page=await context.newPage();page.on('pageerror',e=>errores.push(e.message));
   paginaActual=page;
   await page.goto(url);
   await page.getByRole('button',{name:'Levantar selector del Omnitrix',exact:true}).click();
   await page.getByRole('button',{name:'Activar Archivo Omnitrix',exact:true}).click();
   await page.locator('[data-omnitrix-reveal]').waitFor({state:'attached'});
   await page.locator('[data-omnitrix-reveal]').waitFor({state:'detached'});
   await page.getByText('Servidor de prueba visual: conocimiento simulado, sin API.',{exact:true}).waitFor();
   if(await page.getByTestId('stExpandSidebarButton').isVisible())await page.getByTestId('stExpandSidebarButton').click();
   await page.getByTestId('stRadioOption').filter({hasText:'Conocimiento alienígena'}).click();
   if(viewport.width<600)await page.getByTestId('stSidebarCollapseButton').click();
   assert.ok(await page.getByRole('button',{name:'Iniciar',exact:true}).isDisabled());
   for(const modo of ['Nombres','Habilidades','Especie','General']) {
    await page.getByTestId('stRadioOption').filter({hasText:modo}).click();
    assert.equal(await page.getByRole('textbox',{name:'Tu respuesta',exact:true}).count(),0);
    await page.getByRole('button',{name:'Iniciar',exact:true}).click();
    const card=page.locator('.st-key-pregunta_conocimiento');
    const imagen=card.locator('img');await imagen.waitFor();await imagen.evaluate(img=>img.decode());
    assert.ok(await imagen.evaluate(img=>img.naturalWidth>0 && img.getBoundingClientRect().height<=221));
    const input=page.getByRole('textbox',{name:'Tu respuesta',exact:true});await input.fill('Respuesta escrita de prueba');
    // Las reejecuciones del reloj no deben borrar el borrador ni cambiar imagen.
    const src=await imagen.getAttribute('src');
    const tiempo=await page.getByTestId('stMetricValue').first().innerText();
    await page.waitForTimeout(2200);
    assert.equal(await input.inputValue(),'Respuesta escrita de prueba');
    assert.equal(await imagen.getAttribute('src'),src);
    assert.notEqual(await page.getByTestId('stMetricValue').first().innerText(),tiempo);
    await card.screenshot({path:path.join(out,`conocimiento-${viewport.width}-${modo}.png`)});
    assert.equal(await page.getByRole('link',{name:'Fuente de especie',exact:true}).count(),0);
    await page.getByRole('button',{name:'Enviar y siguiente',exact:true}).click();
    await page.getByText('1 respuestas guardadas · Pregunta 2',{exact:false}).waitFor();
    if(modo==='General') {
     await page.getByRole('button',{name:'Agotar tiempo (prueba visual)',exact:true}).click();
     await page.getByRole('heading',{name:'Tiempo agotado',exact:true}).waitFor();
    } else {
     await page.getByRole('button',{name:'Terminar ronda',exact:true}).click();
    }
    await page.getByRole('button',{name:'Evaluar respuestas con IA',exact:true}).click();
    await page.getByText('Corrección simulada para revisar la interfaz. No se consultó Gemini.',{exact:true}).waitFor();
    await page.getByText('Correctas',{exact:true}).waitFor();
    await page.screenshot({path:path.join(out,`conocimiento-resultado-${viewport.width}-${modo}.png`)});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.getByRole('button',{name:'Volver a jugar',exact:true}).click();
    await page.getByText('0 respuestas guardadas · Pregunta 1',{exact:false}).waitFor();
    await page.getByRole('button',{name:'Terminar ronda',exact:true}).click();
    await page.getByRole('textbox',{name:'Tu respuesta',exact:true}).waitFor({state:'detached'});
    await page.getByRole('button',{name:'Volver al menú de modos',exact:true}).click();
    await page.getByRole('button',{name:'Iniciar',exact:true}).waitFor();
    resultados.push({ancho:viewport.width,modo,resultado:'correcto',reloj_y_borrador:'conservados',evaluacion:'simulada sin API'});
    console.log(`Correcto: ${viewport.width} / ${modo}`);
   }
   assert.deepEqual(errores,[]);assert.deepEqual(externos,[]);
   await context.close();
  }
  fs.writeFileSync('evidencias/navegador-conocimiento.json',JSON.stringify({casos:resultados,errores_js:0,peticiones_externas:0},null,2)+'\n');
  console.log(JSON.stringify(resultados));
 } catch(error) {
   if(paginaActual && !paginaActual.isClosed()) {
     await paginaActual.screenshot({path:path.join(out,'conocimiento-fallo.png')});
     fs.writeFileSync(path.join(out,'conocimiento-fallo.txt'),await paginaActual.locator('body').innerText());
   }
   throw error;
 } finally {await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
