export default function ({ parentElement, data, setTriggerValue }) {
  // Streamlit puede volver a ejecutar el renderer al enviar el evento.
  // La transición ya está en curso: no reiniciar ni la entrada ni su audio.
  if (document.querySelector('[data-omnitrix-reveal]')) return () => {};
  const screen = parentElement.querySelector('.omni-start');
  const button = screen.querySelector('.omni-start-button');
  const status = screen.querySelector('.omni-start-status');
  const hint = screen.querySelector('.omni-start-hint');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const timers = new Set();
  let busy = false;
  let completed = false;
  let armed = false;
  screen.querySelector('.omni-start-symbol').src = data.simbolo;
  const ready = new Audio(data.inicio_audio);
  const transform = new Audio(data.transformacion_audio);
  ready.preload = transform.preload = 'auto';
  function later(callback, delay) {
    const id = window.setTimeout(() => { timers.delete(id); callback(); }, delay);
    timers.add(id);
  }
  function handoff() {
    completed = true;
    // Una sola capa, creada antes del rerun, sobrevive al desmontaje.
    const veil = document.createElement('div');
    veil.setAttribute('aria-hidden', 'true');
    veil.setAttribute('data-omnitrix-reveal', '');
    veil.setAttribute('popover', 'manual');
    Object.assign(veil.style, {
      position: 'fixed', inset: '0', zIndex: '2147483647', background: '#8cff38',
      width: '100vw', height: '100dvh', maxWidth: 'none', maxHeight: 'none',
      margin: '0', padding: '0', border: '0',
      opacity: reducedMotion ? '0' : '1', pointerEvents: 'auto',
      transition: reducedMotion ? 'none' : 'opacity 1400ms ease-in-out',
    });
    document.body.appendChild(veil);
    // La capa superior del navegador cubre también el sidebar de Streamlit,
    // independientemente de sus contextos de apilamiento.
    if (veil.showPopover) veil.showPopover();
    else veil.removeAttribute('popover');
    const started = performance.now();
    let revealing = false;
    let settle;
    const observer = new MutationObserver(check);
    observer.observe(document.body, { childList: true, subtree: true });
    const safety = window.setTimeout(reveal, 15000);
    function reveal() {
      if (revealing) return;
      revealing = true;
      observer.disconnect();
      window.clearTimeout(settle);
      window.clearTimeout(safety);
      veil.style.pointerEvents = 'none';
      window.requestAnimationFrame(() => window.requestAnimationFrame(() => {
        veil.style.opacity = '0';
        window.setTimeout(() => veil.remove(), reducedMotion ? 0 : 1500);
      }));
    }
    function check() {
      window.clearTimeout(settle);
      if (document.querySelector('.omni-start') ||
          !document.querySelector('[data-testid="stSidebar"] .omnitrix-marca') ||
          !document.querySelector('[data-testid="stChatInput"], [data-testid="stAlert"]')) return;
      settle = window.setTimeout(async () => {
        await Promise.all(Array.from(document.querySelectorAll('[data-testid="stMain"] img'))
          .map(img => img.decode().catch(() => {})));
        const remaining = reducedMotion ? 0 : Math.max(0, 600 - (performance.now() - started));
        window.setTimeout(reveal, remaining);
      }, 300);
    }
    setTriggerValue('activar', true);
    check();
  }
  function activate() {
    if (busy) return;
    busy = true;
    button.disabled = true;
    if (!armed) {
      // Primer gesto: levantar el selector y reproducir su sonido.
      ready.play().catch(() => {});
      screen.classList.add('is-armed');
      status.textContent = 'Selector listo';
      hint.textContent = 'Vuelve a pulsar Enter o el símbolo para entrar';
      later(() => {
        armed = true;
        busy = false;
        button.disabled = false;
        button.setAttribute('aria-label', 'Activar Archivo Omnitrix');
      }, 400);
      return;
    }
    ready.pause();
    ready.currentTime = 0;
    // Reproducir dentro del gesto para respetar la política del navegador.
    transform.play().catch(() => {});
    screen.classList.add('is-pressing');
    status.textContent = 'Activando el Omnitrix…';
    later(() => {
      screen.classList.add('is-transitioning');
      later(handoff, reducedMotion ? 0 : 950);
    }, reducedMotion ? 0 : 350);
  }
  function onKey(event) {
    if (event.key !== 'Enter' || event.repeat || event.isComposing || event.ctrlKey || event.altKey || event.metaKey) return;
    if (event.target.closest?.('input, textarea, [contenteditable="true"]')) return;
    event.preventDefault();
    activate();
  }
  button.addEventListener('click', activate);
  document.addEventListener('keydown', onKey);
  const focusFrame = window.requestAnimationFrame(() => button.focus({ preventScroll: true }));
  return () => {
    button.removeEventListener('click', activate);
    document.removeEventListener('keydown', onKey);
    window.cancelAnimationFrame(focusFrame);
    timers.forEach(id => window.clearTimeout(id));
    ready.pause();
    // No cortar la transformación cuando se desmonte el componente.
    if (!completed) transform.pause();
  };
}
