// Fondo decorativo y controles reales; no se envían opiniones ni estrategias a IA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('../.herramientas/browser-check/node_modules/playwright-core');
const url = process.argv[2];
if (!url || !['127.0.0.1', 'localhost'].includes(new URL(url).hostname)) throw new Error('Indicar una URL local.');
const output = path.resolve('.herramientas/browser-check');
async function main() {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true,
    executablePath: process.env.OMNITRIX_BROWSER || 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe' });
  const resultados = [];
  try {
    for (const caso of [
      { nombre: 'escritorio', viewport: { width: 1440, height: 900 } },
      { nombre: 'movil', viewport: { width: 390, height: 844 } },
      { nombre: 'movimiento-reducido', viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' },
    ]) {
      const context = await browser.newContext({ viewport: caso.viewport, reducedMotion: caso.reducedMotion || 'no-preference' });
      const errores = [], externos = [];
      await context.route('**/*', route => {
        if (['127.0.0.1', 'localhost'].includes(new URL(route.request().url()).hostname)) return route.continue();
        externos.push(route.request().url()); return route.abort();
      });
      const page = await context.newPage();
      page.on('pageerror', error => errores.push(error.message));
      await page.goto(url);
      await page.getByRole('button', { name: 'Levantar selector del Omnitrix', exact: true }).click();
      await page.getByRole('button', { name: 'Activar Archivo Omnitrix', exact: true }).click();
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'attached' });
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'detached' });
      assert.ok(await page.getByRole('main').evaluate(el => el.scrollTop <= 1));
      const estilos = () => page.getByTestId('stAppViewContainer').evaluate(el => {
        const before = getComputedStyle(el, '::before'), after = getComputedStyle(el, '::after');
        return { movimiento: before.animationName, transform: before.transform, eventos: before.pointerEvents,
          fondo: before.backgroundImage, nivel: before.zIndex, segunda: after.display };
      });
      const inicial = await estilos();
      assert.equal(inicial.eventos, 'none'); assert.equal(inicial.nivel, '-1');
      assert.ok(inicial.fondo.includes('radial-gradient'));
      await page.waitForTimeout(180);
      const siguiente = await estilos();
      if (caso.reducedMotion) assert.equal(siguiente.movimiento, 'none');
      else assert.notEqual(inicial.transform, siguiente.transform, 'Las células deben desplazarse y cambiar de escala');
      if (caso.nombre === 'movil') assert.equal(siguiente.segunda, 'none');
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      const titulo = page.getByRole('heading', { name: 'Archivo Omnitrix', exact: true });
      assert.ok(await titulo.evaluate(el => {
        const r = el.getBoundingClientRect();
        return el.contains(document.elementFromPoint(r.left + 15, r.top + 15));
      }), 'El texto debe quedar por encima del fondo');
      await page.locator('.omnitrix-emblema').evaluate(img => img.decode());
      await page.screenshot({ path: path.join(output, `fondo-${caso.nombre}.png`) });
      const selector = page.getByRole('combobox', { name: 'Selecciona un alien', exact: true });
      await selector.click(); await selector.fill('Diamante');
      await page.getByRole('option', { name: 'Diamante', exact: true }).click();
      await page.getByRole('heading', { name: 'Diamante', exact: true }).waitFor();
      await page.locator('.st-key-imagen_alien img').evaluate(img => img.decode());
      assert.ok(await page.getByTestId('stChatInput').isVisible());
      if (await page.getByTestId('stExpandSidebarButton').isVisible()) await page.getByTestId('stExpandSidebarButton').click();
      await page.getByTestId('stRadioOption').filter({ hasText: 'Desafíos del Omnitrix' }).click();
      if (caso.nombre === 'movil') await page.getByTestId('stSidebarCollapseButton').click();
      await page.getByRole('button', { name: 'Iniciar', exact: true }).waitFor();
      assert.ok(await page.getByRole('button', { name: 'Iniciar', exact: true }).isDisabled());
      assert.equal(await page.getByTestId('stRadioOption').filter({ hasText: 'Adaptabilidad' }).count(), 1);
      assert.deepEqual(errores, []); assert.deepEqual(externos, []);
      resultados.push({ caso: caso.nombre, resultado: 'correcto', movimiento: siguiente.movimiento,
        controles_e_imagenes: 'correctos', errores_js: 0, peticiones_externas: 0 });
      await context.close();
    }
    fs.writeFileSync(path.join(output, 'resultado-fondo.json'), JSON.stringify(resultados, null, 2));
    console.log(JSON.stringify(resultados, null, 2));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
