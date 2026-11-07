// Usar exclusivamente con tests/app_desafios_visual.py: evaluación simulada, sin API.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('../.herramientas/browser-check/node_modules/playwright-core');
const url = process.argv[2];
if (!url || !['127.0.0.1', 'localhost'].includes(new URL(url).hostname) || process.argv[3] !== '--simulado') {
  throw new Error('Indicar la URL local de tests/app_desafios_visual.py y --simulado.');
}
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
      await page.goto(url);
      await page.getByText('Servidor de prueba visual: evaluaciones simuladas, sin API.', { exact: true }).waitFor({ state: 'attached' });
      await page.getByRole('button', { name: 'Levantar selector del Omnitrix', exact: true }).click();
      await page.getByRole('button', { name: 'Activar Archivo Omnitrix', exact: true }).click();
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'attached' });
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'detached' });
      if (await page.getByTestId('stExpandSidebarButton').isVisible()) await page.getByTestId('stExpandSidebarButton').click();
      await page.getByTestId('stRadioOption').filter({ hasText: 'Desafíos del Omnitrix' }).click();
      if (nombre === 'movil') await page.getByTestId('stSidebarCollapseButton').click();
      await page.getByRole('button', { name: 'Iniciar', exact: true }).waitFor();
      await page.screenshot({ path: path.join(output, `rondas-menu-${nombre}.png`), fullPage: true });

      async function completar(modo, captura) {
        await page.getByText('MISIÓN ACTUAL', { exact: true }).waitFor();
        const textarea = page.locator('textarea');
        await textarea.waitFor();
        await page.locator('[data-testid="stApp"][data-test-script-state="notRunning"]').waitFor();
        assert.equal(await page.getByRole('button', { name: 'Otra situación', exact: true }).count(), 0);
        assert.equal(await page.getByRole('button', { name: 'Volver a jugar', exact: true }).count(), 0);
        const titulo = await page.getByRole('heading', { level: 3 }).first().innerText();
        if (modo === 'Adaptabilidad') {
          assert.equal(await page.getByRole('combobox').count(), 0);
          await page.getByText('Un alien asignado para esta misión.', { exact: true }).waitFor();
          assert.ok(await page.getByRole('button', { name: 'Evaluar mi estrategia', exact: true }).isDisabled());
        } else {
          const selector = page.getByRole('combobox', { name: 'Tu transformación', exact: true });
          await selector.click();
          if (modo === 'Control maestro') {
            await selector.fill('Whampire');
            await page.getByRole('option', { name: 'Whampire', exact: true }).click();
          } else {
            await selector.press('ArrowDown');
            await page.getByRole('option').first().waitFor();
            const opciones = (await page.getByRole('option').allTextContents()).filter(n => !n.includes('Elige un alien'));
            assert.equal(opciones.length, 3);
            assert.equal(new Set(opciones).size, 3);
            await page.getByRole('option', { name: opciones[0], exact: true }).click();
          }
        }
        await textarea.fill('Aprovecharía sus capacidades para alcanzar el objetivo sin dañar los equipos.');
        await textarea.press('Tab');
        await page.getByRole('heading', { name: 'Desafíos del Omnitrix', exact: true }).scrollIntoViewIfNeeded();
        if (captura) await page.screenshot({ path: path.join(output, `ronda-${nombre}-${modo}.png`), fullPage: true });
        const evaluar = page.getByRole('button', { name: modo === 'Adaptabilidad' ? 'Evaluar mi estrategia' : 'Evaluar mi elección', exact: true });
        await evaluar.click();
        await page.getByText('Evaluación simulada para pruebas visuales. No se consultó Gemini.', { exact: true }).waitFor();
        await textarea.waitFor({ state: 'detached' });
        assert.equal(await page.getByRole('combobox').count(), 0);
        await page.getByRole('button', { name: 'Volver a jugar', exact: true }).waitFor();
        await page.getByRole('button', { name: 'Volver al menú de modos', exact: true }).waitFor();
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        return titulo;
      }
      for (const modo of ['Control maestro', 'Héroe bajo presión', 'Adaptabilidad']) {
        console.log(`Comprobando ${nombre}: ${modo}`);
        await page.getByTestId('stRadioOption').filter({ hasText: modo }).click();
        await page.getByRole('button', { name: 'Iniciar', exact: true }).click();
        const anterior = await completar(modo, true);
        await page.getByRole('button', { name: 'Volver a jugar', exact: true }).click();
        const siguiente = await completar(modo, false);
        assert.notEqual(siguiente, anterior);
        await page.getByRole('button', { name: 'Volver al menú de modos', exact: true }).click();
        await page.getByRole('button', { name: 'Iniciar', exact: true }).waitFor();
        resultados.push({ pantalla: nombre, modo, resultado: 'correcto', evaluacion: 'simulada-sin-api' });
      }
      assert.deepEqual(errores, []); assert.deepEqual(externos, []);
      await context.close();
    }
    fs.writeFileSync(path.join(output, 'resultado-rondas.json'), JSON.stringify(resultados, null, 2));
    console.log(JSON.stringify(resultados, null, 2));
  } finally { await browser.close(); }
}
main().catch(e => { console.error(e); process.exitCode = 1; });
