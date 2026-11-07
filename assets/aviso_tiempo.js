export default function ({ data }) {
  // Las actualizaciones del reloj y los cambios de pregunta pueden volver a
  // montar el componente. El registro del documento evita reiniciar el sonido.
  const key = '__omnitrixAvisoTiempo';
  let estado = window[key];
  if (!estado || estado.ronda !== data.ronda) {
    estado?.audio.pause();
    estado = { ronda: data.ronda, audio: new Audio(data.audio),
      intentado: false, bloqueado: false, reproduciendo: false };
    estado.audio.preload = 'auto';
    window[key] = estado;
  }
  estado.restantes = data.restantes;
  function reproducir() {
    if (estado.reproduciendo || estado.restantes <= 0 || estado.restantes > 4) return;
    estado.intentado = true;
    estado.reproduciendo = true;
    estado.bloqueado = false;
    estado.audio.play().catch(() => {
      estado.reproduciendo = false;
      estado.bloqueado = true;
    });
  }
  function desbloquear() {
    if (estado.bloqueado) reproducir();
  }
  if (data.restantes > 0 && data.restantes <= 4 && !estado.intentado) reproducir();
  // Si el navegador bloquea el aviso, reintentar solo con el siguiente gesto;
  // sin botones adicionales ni intentos repetidos por cada tick del reloj.
  document.addEventListener('pointerdown', desbloquear);
  document.addEventListener('keydown', desbloquear);
  return () => {
    document.removeEventListener('pointerdown', desbloquear);
    document.removeEventListener('keydown', desbloquear);
    // Dejar que el aviso termine aunque cambie la pregunta o finalice el reloj.
  };
}
