// Revisión visual local: no pulsa Evaluar ni consume la API.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('../.herramientas/browser-check/node_modules/playwright-core');
const url = process.argv[2];
if (!url || !['127.0.0.1', 'localhost'].includes(new URL(url).hostname)) throw new Error('Indicar servidor local.');
const output = path.resolve('.herramientas/browser-check');
async function main() {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true,
    executablePath: process.env.OMNITRIX_BROWSER || 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe' });
  const resultados = [];
  try {
    for (const [nombre, viewport] of [['escritorio', { width: 1440, height: 1000 }], ['movil', { width: 390, height: 844 }]]) {
      const context = await browser.newContext({ viewport });
      const externos = [], errores = [];
      await context.route('**/*', route => {
        if (['127.0.0.1', 'localhost'].includes(new URL(route.request().url()).hostname)) return route.continue();
        externos.push(route.request().url()); return route.abort();
      });
      const page = await context.newPage();
      page.on('pageerror', e => errores.push(e.message));
      async function navegar(seccion) {
        if (await page.getByTestId('stExpandSidebarButton').isVisible()) await page.getByTestId('stExpandSidebarButton').click();
        await page.getByTestId('stRadioOption').filter({ hasText: seccion }).click();
        if (nombre === 'movil') await page.getByTestId('stSidebarCollapseButton').click();
      }
      await page.goto(url);
      await page.getByRole('button', { name: 'Levantar selector del Omnitrix', exact: true }).click();
      await page.getByRole('button', { name: 'Activar Archivo Omnitrix', exact: true }).click();
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'attached' });
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'detached' });
      await navegar('Desafíos del Omnitrix');
      await page.getByRole('heading', { name: 'Desafíos del Omnitrix', exact: true }).waitFor();
      assert.ok(await page.getByRole('button', { name: 'Evaluar mi elección', exact: true }).isDisabled());
      const titulo = await page.getByRole('heading', { level: 3 }).first().innerText();
      await page.getByRole('combobox', { name: 'Tu transformación', exact: true }).click();
      await page.getByRole('combobox', { name: 'Tu transformación', exact: true }).fill('Whampire');
      await page.getByRole('option', { name: 'Whampire', exact: true }).click();
      await page.getByRole('heading', { name: 'Whampire', exact: true }).waitFor();
      const plan = page.getByRole('textbox', { name: '¿Cómo lo resolverías? (opcional)', exact: true });
      await plan.fill('Aprovecharía sus habilidades para alcanzar el objetivo.');
      await plan.press('Tab');
      await page.waitForTimeout(500);
      assert.ok(await page.getByRole('button', { name: 'Evaluar mi elección', exact: true }).isEnabled());
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      await page.getByRole('heading', { name: 'Desafíos del Omnitrix', exact: true }).scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(output, `desafios-${nombre}.png`), fullPage: true });
      await navegar('Analizar opinión');
      await page.getByRole('heading', { name: 'Analizar opinión', exact: true }).waitFor();
      await navegar('Desafíos del Omnitrix');
      await page.getByRole('heading', { name: 'Whampire', exact: true }).waitFor();
      assert.equal(await plan.inputValue(), 'Aprovecharía sus habilidades para alcanzar el objetivo.');
      assert.equal(await page.getByRole('heading', { level: 3 }).first().innerText(), titulo);
      await page.getByRole('button', { name: 'Otra situación', exact: true }).click();
      await page.waitForFunction(old => [...document.querySelectorAll('h3')][0]?.textContent !== old, titulo);
      await page.waitForFunction(() => document.querySelector('textarea')?.value === '');
      assert.equal(await plan.inputValue(), '');
      assert.deepEqual(errores, []); assert.deepEqual(externos, []);
      resultados.push({ caso: nombre, resultado: 'correcto', errores_js: 0, peticiones_externas: 0 });
      await context.close();
    }
    fs.writeFileSync(path.join(output, 'resultado-desafios.json'), JSON.stringify(resultados, null, 2));
    console.log(JSON.stringify(resultados, null, 2));
  } finally { await browser.close(); }
}
main().catch(e => { console.error(e); process.exitCode = 1; });
