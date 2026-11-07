// Ejecutar solo contra tests/app_interpretacion_visual.py, con --simulado.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('../.herramientas/browser-check/node_modules/playwright-core');
const url=process.argv[2];
if(process.argv[3]!=='--simulado'||!url||!['127.0.0.1','localhost'].includes(new URL(url).hostname))throw new Error('Indica URL local del servidor visual y --simulado.');
const out=path.resolve('.herramientas/browser-check');
async function main(){
 const browser=await chromium.launch({headless:true,executablePath:process.env.OMNITRIX_BROWSER||'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'});
 const resultados=[];let activa;
 try{
  for(const ancho of [1440,390]){
   const context=await browser.newContext({viewport:{width:ancho,height:1000},reducedMotion:'reduce'});
   const errores=[],externos=[];
   await context.route('**/*',r=>{if(['127.0.0.1','localhost'].includes(new URL(r.request().url()).hostname))return r.continue();externos.push(r.request().url());return r.abort()});
   const page=await context.newPage();activa=page;page.on('pageerror',e=>errores.push(e.message));
   await page.goto(url);
   await page.getByRole('button',{name:'Levantar selector del Omnitrix',exact:true}).click();
   await page.getByRole('button',{name:'Activar Archivo Omnitrix',exact:true}).click();
   await page.locator('[data-omnitrix-reveal]').waitFor({state:'attached'});
   await page.locator('[data-omnitrix-reveal]').waitFor({state:'detached'});
   await page.getByText('Servidor visual de interpretación: IA simulada, sin API.',{exact:true}).waitFor();
   if(await page.getByTestId('stExpandSidebarButton').isVisible())await page.getByTestId('stExpandSidebarButton').click();
   await page.getByTestId('stRadioOption').filter({hasText:'Interpretación alienígena'}).click();
   if(ancho<600)await page.getByTestId('stSidebarCollapseButton').click();
   assert.ok(await page.getByRole('button',{name:'Iniciar',exact:true}).isDisabled());
   for(const modo of ['Mi alien favorito','Tu afinidad alienígena']){
    await page.getByTestId('stRadioOption').filter({hasText:modo}).click();
    assert.equal(await page.getByRole('textbox').count(),0);
    await page.getByRole('button',{name:'Iniciar',exact:true}).click();
    if(modo==='Mi alien favorito'){
     const selector=page.getByRole('combobox',{name:'Tu alien favorito',exact:true});
     await selector.click();await selector.fill('Fuego');
     await page.getByRole('option',{name:'Fuego',exact:true}).click();
     await page.getByRole('heading',{name:'Fuego',exact:true}).waitFor();
     await page.getByRole('textbox').fill('Me gusta su diseño y cómo protege a otras personas.');
     await page.getByRole('button',{name:'Interpretar mi elección',exact:true}).click();
    }else{
     for(let n=1;n<=6;n++){
      await page.getByText(`Pregunta ${n} de 6 ·`,{exact:false}).waitFor();
      const respuesta=`Respuesta ${n}: escucharía las ideas del equipo y buscaría una solución creativa.`;
      await page.getByRole('textbox',{name:'Tu respuesta',exact:true}).fill(respuesta);
      if(n===2){
       await page.getByRole('button',{name:'Anterior',exact:true}).click();
       await page.getByText('Pregunta 1 de 6 ·',{exact:false}).waitFor();
       assert.ok((await page.getByRole('textbox').inputValue()).startsWith('Respuesta 1'));
       await page.getByRole('button',{name:'Siguiente',exact:true}).click();
       await page.getByText('Pregunta 2 de 6 ·',{exact:false}).waitFor();
       assert.equal(await page.getByRole('textbox').inputValue(),respuesta);
      }
      await page.getByRole('button',{name:n===6?'Revisar mis respuestas':'Siguiente',exact:true}).click();
     }
     await page.getByRole('heading',{name:'Revisa tus respuestas',exact:true}).waitFor();
     assert.equal(await page.getByTestId('stExpander').count(),6);
     await page.screenshot({path:path.join(out,`interpretacion-revision-${ancho}.png`)});
     await page.getByRole('button',{name:'Descubrir mi afinidad',exact:true}).click();
    }
    await page.getByText('Interpretación simulada para revisar la interfaz. No se consultó Gemini.',{exact:true}).waitFor();
    const titulo=page.getByRole('heading',{name:modo==='Mi alien favorito'?'Tu conexión con el alien elegido':'Tu afinidad principal',exact:true});
    await titulo.scrollIntoViewIfNeeded();
    await page.locator('.st-key-ficha_interpretacion_principal img').evaluate(img=>img.decode());
    await page.screenshot({path:path.join(out,`interpretacion-resultado-${ancho}-${modo==='Mi alien favorito'?'favorito':'afinidad'}.png`)});
    if(modo==='Tu afinidad alienígena')assert.equal(await page.getByText('Otra afinidad posible: Diamante',{exact:true}).count(),1);
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.getByRole('button',{name:'Volver al menú de modos',exact:true}).click();
    await page.getByRole('button',{name:'Iniciar',exact:true}).waitFor();
    resultados.push({ancho,modo,resultado:'correcto',evaluacion:'simulada',errores_js:0,peticiones_externas:0});
    console.log(`Correcto: ${ancho} / ${modo}`);
   }
   assert.deepEqual(errores,[]);assert.deepEqual(externos,[]);
   await context.close();
  }
  fs.writeFileSync('evidencias/navegador-interpretacion.json',JSON.stringify(resultados,null,2)+'\n');
 }catch(error){
  if(activa&&!activa.isClosed()){
   await activa.screenshot({path:path.join(out,'interpretacion-fallo.png')});
   fs.writeFileSync(path.join(out,'interpretacion-fallo.txt'),await activa.locator('body').innerText());
  }throw error;
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
