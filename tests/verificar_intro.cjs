// Prueba de navegador opcional. Usa audio local, sin perfiles personales ni IA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('../.herramientas/browser-check/node_modules/playwright-core');

const url = process.argv[2];
if (!url || !['127.0.0.1', 'localhost'].includes(new URL(url).hostname)) {
  throw new Error('Indicar la URL del servidor local de prueba.');
}
const output = path.resolve('.herramientas/browser-check');
fs.mkdirSync(output, { recursive: true });

async function main() {
  const browser = await chromium.launch({
    executablePath: process.env.OMNITRIX_BROWSER || 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',
    headless: true,
    args: ['--autoplay-policy=document-user-activation-required'],
  });
  const resultados = [];
  try {
    for (const caso of [
      { nombre: 'clic', viewport: { width: 1440, height: 900 } },
      { nombre: 'enter', viewport: { width: 1440, height: 900 } },
      { nombre: 'movil', viewport: { width: 390, height: 844 } },
      { nombre: 'movimiento-reducido', viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' },
      { nombre: 'audio-bloqueado', viewport: { width: 1440, height: 900 } },
    ]) {
      console.log(`Comprobando ${caso.nombre}`);
      const context = await browser.newContext({ viewport: caso.viewport, reducedMotion: caso.reducedMotion || 'no-preference' });
      const externos = [];
      await context.route('**/*', route => {
        const destino = new URL(route.request().url());
        if (['127.0.0.1', 'localhost'].includes(destino.hostname)) return route.continue();
        externos.push(destino.hostname);
        return route.abort();
      });
      const page = await context.newPage();
      await page.addInitScript(({ blocked }) => {
        window.omniAudio = [];
        const play = HTMLMediaElement.prototype.play;
        HTMLMediaElement.prototype.play = function () {
          window.omniAudio.push(this);
          if (blocked && window.omniAudio.length === 1) return Promise.reject(new DOMException('Autoplay blocked', 'NotAllowedError'));
          return play.call(this);
        };
      }, { blocked: caso.nombre === 'audio-bloqueado' });
      const errores = [];
      page.on('pageerror', e => errores.push(e.message));
      await page.goto(url);
      await page.locator('.omni-start-button').waitFor({ state: 'visible', timeout: 20000 });
      await page.locator('.omni-start-symbol').evaluate(img => img.decode());
      await page.evaluate(() => {
        window.omniContinuidad = { vioCapa: false, corte: false };
        const observer = new MutationObserver(() => {
          const veil = document.querySelector('[data-omnitrix-reveal]');
          if (veil) window.omniContinuidad.vioCapa = true;
          if (window.omniContinuidad.vioCapa && !document.querySelector('.omni-start') && !veil && !document.querySelector('[data-testid="stChatInput"]')) window.omniContinuidad.corte = true;
        });
        observer.observe(document.body, { childList: true, subtree: true });
      });
      assert.equal(await page.getByRole('button', { name: 'Activar sonido', exact: true }).count(), 0);
      assert.equal(await page.evaluate(() => window.omniAudio.length), 0);
      assert.equal(await page.locator('[data-testid="stChatInput"]').count(), 0);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
      if (caso.nombre === 'clic' || caso.nombre === 'movil') {
        await page.screenshot({ path: path.join(output, `intro-${caso.nombre}.png`) });
      }
      if (caso.nombre === 'enter') {
        await page.keyboard.press('Enter');
      } else {
        await page.getByRole('button', { name: 'Levantar selector del Omnitrix', exact: true }).click();
      }
      await page.getByRole('button', { name: 'Activar Archivo Omnitrix', exact: true }).waitFor();
      assert.equal(await page.locator('[data-testid="stChatInput"]').count(), 0);
      assert.equal(await page.evaluate(() => window.omniAudio.length), 1);
      assert.equal(await page.locator('.omni-start.is-transitioning').count(), 0);
      if (caso.nombre !== 'audio-bloqueado') {
        await page.waitForFunction(() => window.omniAudio[0]?.currentTime > 0);
      }
      if (caso.nombre === 'clic') {
        await page.screenshot({ path: path.join(output, 'intro-selector-levantado.png') });
      }
      if (caso.nombre === 'enter') {
        await page.keyboard.press('Enter');
      } else {
        await page.getByRole('button', { name: 'Activar Archivo Omnitrix', exact: true }).click();
      }
      if (caso.nombre === 'clic') {
        await page.locator('.omni-start.is-pressing').waitFor({ state: 'visible' });
        await page.waitForTimeout(120);
        await page.screenshot({ path: path.join(output, 'intro-pulsacion.png') });
        await page.locator('.omni-start.is-transitioning').waitFor({ state: 'visible' });
        await page.waitForTimeout(330);
        await page.screenshot({ path: path.join(output, 'intro-verde.png') });
        await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'attached' });
        assert.equal(await page.locator('[data-omnitrix-reveal]').evaluate(el => getComputedStyle(el).opacity), '1');
      }
      await page.getByRole('heading', { name: 'Archivo Omnitrix', exact: true }).waitFor({ state: 'visible', timeout: 20000 });
      assert.ok(await page.evaluate(() => window.omniAudio.length >= 2));
      if (caso.nombre === 'clic') {
        // Debe cubrir tanto el panel izquierdo como el área central.
        assert.ok(await page.evaluate(() => {
          const veil = document.querySelector('[data-omnitrix-reveal]');
          return veil && document.elementFromPoint(80, 300) === veil &&
            document.elementFromPoint(innerWidth / 2, 300) === veil;
        }));
        await page.screenshot({ path: path.join(output, 'intro-sidebar-verde.png') });
      }
      await page.locator('.omni-start').waitFor({ state: 'detached' });
      await page.locator('[data-omnitrix-reveal]').waitFor({ state: 'detached' });
      await page.waitForTimeout(800);
      assert.ok(await page.getByRole('main').evaluate(el => el.scrollTop <= 1), 'El dashboard debe iniciar arriba');
      const tituloInicial = await page.getByRole('heading', { name: 'Archivo Omnitrix', exact: true }).boundingBox();
      assert.ok(tituloInicial && tituloInicial.y >= 0 && tituloInicial.y < caso.viewport.height);
      assert.deepEqual(await page.evaluate(() => ({ vioCapa: window.omniContinuidad.vioCapa, corte: window.omniContinuidad.corte })), { vioCapa: true, corte: false });
      const audios = await page.evaluate(() => window.omniAudio.map(a => ({ tiempo: a.currentTime, duracion: a.duration, pausado: a.paused, error: a.error?.message, src: a.src.slice(0, 28) })));
      assert.ok(audios.at(-1).tiempo > 0 && !audios.at(-1).error, JSON.stringify(audios));
      if (caso.nombre === 'clic') {
        await page.screenshot({ path: path.join(output, 'intro-dashboard.png') });
      }
      const desplazado = await page.getByRole('main').evaluate(el => { el.scrollTop = el.scrollHeight; return el.scrollTop; });
      await page.waitForTimeout(250);
      assert.ok(await page.getByRole('main').evaluate((el, esperado) => Math.abs(el.scrollTop - esperado) <= 1, desplazado), 'El desplazamiento manual debe seguir disponible');
      if (await page.getByTestId('stExpandSidebarButton').isVisible()) {
        await page.getByTestId('stExpandSidebarButton').click();
      }
      await page.getByTestId('stRadioOption').filter({ hasText: 'Consultar archivo' }).click();
      await page.getByRole('heading', { name: 'Consultar archivo', exact: true }).waitFor({ state: 'visible' });
      assert.equal(await page.locator('.omni-start').count(), 0);
      await page.getByTestId('stRadioOption').filter({ hasText: 'Analizar opinión' }).click();
      if (caso.nombre === 'movil') {
        await page.getByTestId('stSidebarCollapseButton').click();
      }
      await page.getByRole('button', { name: 'Nueva conversación', exact: true }).click();
      assert.equal(await page.locator('.omni-start').count(), 0);
      assert.deepEqual(errores, []);
      assert.deepEqual(externos, []);
      resultados.push({ caso: caso.nombre, resultado: 'correcto', errores_js: errores.length, peticiones_externas: externos.length });
      await context.close();
    }
    fs.writeFileSync(path.join(output, 'resultado-intro.json'), JSON.stringify(resultados, null, 2));
    console.log(JSON.stringify(resultados, null, 2));
  } finally {
    await browser.close();
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
