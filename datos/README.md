# Catálogo de Archivo Omnitrix

## Situaciones de Desafíos del Omnitrix

`desafios.json` contiene 32 escenarios originales para el juego, compartidos por Control maestro, Héroe bajo presión y Adaptabilidad. Se conservaron d001–d012 y se añadieron d013–d032. No fijan un alien obligatorio: la evaluación considera el objetivo, las capacidades y la estrategia.

Los 20 nuevos abarcan batallas con Vilgax, Animo, Hex, Zombozo, los Caballeros Eternos, SixSix/Kraab y Albedo; seguridad de museos y bases, robo de credenciales, rescates sin gravedad, fauna protegida, primer contacto, espuma expansiva y anomalías temporales/dimensionales. Los conflictos y dispositivos descritos son invenciones del juego. Como referencia general de los personajes se consultaron la [lista de personajes de Ben 10](https://en.wikipedia.org/wiki/List_of_Ben_10_characters) y [Vilgax clásico](https://ben10.fandom.com/wiki/Vilgax_(Classic)); las misiones no reproducen guiones de episodios.

El sorteo es local y no consume cuota. Una ronda conserva la situación hasta la evaluación; Volver a jugar elige otra diferente de la anterior.

## Transformaciones

`aliens.json` contiene 63 fichas de transformaciones de la continuidad clásica: las cuatro series, sus películas y el especial con Generador Rex. Conserva los 20 IDs originales y añade a021–a063. No es un ranking ni representa el millón de muestras de ADN del Omnitrix.

Se excluyen reboot, formas supremas, fusiones, transformaciones exclusivas de videojuegos/directos teatrales y formas solo mencionadas sin transformación animada identificable. Spitter se incluye por Ben 10.000 y su ficha lo aclara. Las dos variantes de Upchuck, Perk y Murk, tienen fichas separadas. Nanomech debuta en la película de la etapa Fuerza Alienígena; Shocksquatch, en el especial de la etapa Supremacía Alienígena. `serie_origen` agrupa esos debuts por etapa.

| Serie de introducción | Fichas |
| --- | --- |
| Ben 10 (serie original) | 22 |
| Ben 10: Fuerza Alienígena | 14 |
| Ben 10: Supremacía Alienígena | 11 |
| Ben 10: Omniverse | 16 |

### Catálogo completo

| ID | Nombre latino | Nombre original |
| --- | --- | --- |
| a001 | Fuego | Heatblast |
| a002 | Diamante | Diamondhead |
| a003 | XLR8 | XLR8 |
| a004 | Cuatro Brazos | Four Arms |
| a005 | Materia Gris | Grey Matter |
| a006 | Fuego Pantanoso | Swampfire |
| a007 | Eco Eco | Echo Echo |
| a008 | Humungosaurio | Humungousaur |
| a009 | Frío | Big Chill |
| a010 | Mono Araña | Spidermonkey |
| a011 | Amenaza Acuática | Water Hazard |
| a012 | Ampfibio | Ampfibian |
| a013 | Armadillo | Armodrillo |
| a014 | Tortutornado | Terraspin |
| a015 | NRG | NRG |
| a016 | Feedback | Feedback |
| a017 | Bloxx | Bloxx |
| a018 | Gravattack | Gravattack |
| a019 | Crashhopper | Crashhopper |
| a020 | Escarabola | Ball Weevil |
| a021 | Bestia | Wildmutt |
| a022 | Insectoide | Stinkfly |
| a023 | Acuático | Ripjaws |
| a024 | Ultra-T | Upgrade |
| a025 | Fantasmático | Ghostfreak |
| a026 | Cannonbolt | Cannonbolt |
| a027 | Wildvine | Wildvine |
| a028 | Blitzwolfer | Blitzwolfer |
| a029 | Snare-oh | Snare-Oh |
| a030 | Frankentrueno | Frankenstrike |
| a031 | Upchuck Perk | Upchuck (Perk) |
| a032 | Ditto | Ditto |
| a033 | Multi Ojos | Eye Guy |
| a034 | Muy Grande | Way Big |
| a035 | Spitter | Spitter |
| a036 | Bátore | Buzzshock |
| a037 | Arctiguana | Arctiguana |
| a038 | Jetray | Jetray |
| a039 | Piedra | Chromastone |
| a040 | Cerebrón | Brainstorm |
| a041 | Goop | Goop |
| a042 | Alien X | Alien X |
| a043 | Lodestar | Lodestar |
| a044 | Rath | Rath |
| a045 | Nanomech | Nanomech |
| a046 | Upchuck Murk | Upchuck (Murk) |
| a047 | Fasttrack | Fasttrack |
| a048 | Camaleón | Chamalien |
| a049 | Eatle | Eatle |
| a050 | Clockwork | Clockwork |
| a051 | Jury Rigg | Juryrigg |
| a052 | Shocksquatch | Shocksquatch |
| a053 | Walkatrout | Walkatrout |
| a054 | Molestolvo | Pesky Dust |
| a055 | Mole-Stache | Mole-Stache |
| a056 | El Peor | The Worst |
| a057 | Halcón | Kickin' Hawk |
| a058 | Toepick | Toepick |
| a059 | Astrodactyl | Astrodactyl |
| a060 | Bullfrag | Bullfrag |
| a061 | Atomix | Atomix |
| a062 | Barrigobot | Gutrot |
| a063 | Whampire | Whampire |

## Contrato de datos, versión 1

La raíz contiene `version: 1` y una lista `aliens`.

| Campo por alien | Tipo | Significado |
| --- | --- | --- |
| id | string | Identidad estable; no reutilizar ni cambiar al editar el nombre |
| nombre | string | Nombre visible en español latino; algunos se conservan en inglés en el doblaje |
| nombre_original | string | Alias original para identificación; puede coincidir con nombre |
| serie_origen | string | Serie en que la transformación fue introducida al público |
| descripcion | string | Resumen breve de habilidades, redactado para la ficha |
| imagen | string o null | Ruta local relativa a la raíz del proyecto; null si no hay imagen |

La serie de origen no indica todas las series donde aparece el alien. Por ejemplo, los recuerdos de Feedback en Omniverse no lo convierten en una transformación introducida en la serie original. Un rediseño posterior del mismo alien no constituye un registro nuevo. Las formas supremas y el reboot no forman parte de esta selección.

No asignar rutas ficticias a imágenes inexistentes. Los 63 registros apuntan a PNG locales en `assets/aliens/`. La interfaz admite `null` y archivos ausentes, dañados o ilegibles mediante un recurso alternativo local. La mayoría de las imágenes muestran diseños de Omniverse; Jetray, Fasttrack, Camaleón y Spitter usan imágenes de otras etapas, indicadas en sus fichas; `serie_origen` sigue indicando el debut del alien. Ver [fuentes y créditos](../assets/aliens/README.md). El catálogo y las fichas no requieren llamadas al modelo.

## Referencias consultadas

Consulta: 6 de noviembre de 2026. Los nombres regionales y la pertenencia a cada serie se contrastaron en las listas de alienígenas de [Ben 10](https://es.wikipedia.org/wiki/Ben_10), [Fuerza Alienígena](https://es.wikipedia.org/wiki/Ben_10:_Alien_Force), [Supremacía Alienígena](https://es.wikipedia.org/wiki/Ben_10:_Ultimate_Alien) y [Omniverse](https://es.wikipedia.org/wiki/Ben_10:_Omniverse).

Las descripciones sintetizan habilidades generales, sin estadísticas de poder, planetas, episodios ni afirmaciones de superioridad. Referencias complementarias: [aliens originales](https://en.wikipedia.org/wiki/Ben_10_(comic_series)), [Fuego Pantanoso](https://ben10.fandom.com/wiki/Swampfire), [Eco Eco](https://ben10.fandom.com/wiki/Echo_Echo), [Frío](https://ben10.fandom.com/wiki/Big_Chill_(Classic)), [Mono Araña](https://ben10.fandom.com/wiki/Spidermonkey_(Classic)), [Amenaza Acuática](https://ben10.fandom.com/wiki/Waterhazard), [Ampfibio](https://en.wikipedia.org/wiki/Ben_10_(2016_TV_series)), [Armadillo](https://ben10.fandom.com/wiki/Armodrillo), [Tortutornado](https://cartoonnetwork.fandom.com/wiki/Terraspin), [NRG](https://ben10.fandom.com/wiki/NRG), [Feedback](https://ben10.fandom.com/wiki/Feedback), [Bloxx](https://ben10.fandom.com/wiki/Bloxx_(Classic)), [Gravattack](https://ben10.fandom.com/wiki/Gravattack), [Crashhopper](https://ben10.fandom.com/wiki/Crashhopper) y [Escarabola](https://ben10.fandom.com/wiki/Ball_Weevil).

Son referencias comunitarias, no un catálogo oficial. Algunas páginas de Fandom bloquearon la apertura directa; en esos casos se consultó el contenido indexado disponible en búsqueda. Las descripciones son síntesis propias y pueden ajustarse si se detecta una discrepancia de doblaje o contenido, conservando los IDs.

## Fuentes de la ampliación

Revisión: 7 de noviembre de 2026. Listas comunitarias de [transformaciones clásicas](https://ben10.fandom.com/es/wiki/Aliens_del_Omnitrix), [debuts por serie](https://ben10.fandom.com/wiki/Jetray_(Classic)/Gallery) y [Spitter](https://ben10.fandom.com/wiki/Spitter). Nombres regionales contrastados con las páginas de las cuatro series enlazadas arriba. No se interpretan personajes del Nemetrix, transformaciones supremas de Albedo ni variantes de diseño como aliens nuevos. No se incluyen Rocks y Squidstrictor, del espectáculo en vivo, ni Eon de otra continuidad cinematográfica.

Los campos opcionales `serie_diseno` y `fuente_imagen` indican el diseño y la página de imagen de las fichas añadidas. En los 20 registros originales la interfaz conserva Omniverse como valor predeterminado; esos registros no se modificaron. Los hashes y dimensiones de las 63 imágenes se verifican contra el manifiesto de recursos.

## Verificación histórica del paso 3

Se comprobó el parseo del JSON, versión 1, 20 registros, IDs y nombres únicos, campos presentes y tipos básicos, cinco registros por serie, imágenes null y ausencia de nombres de formas supremas.

## Cargador implementado en el paso 4

`almacenamiento.cargar_aliens()` devuelve la lista de registros del catálogo, sin cambiar sus datos. Valida versión entera 1, lista de al menos 20 aliens, campos obligatorios, textos no vacíos e IDs únicos sin espacios exteriores. Acepta campos adicionales para permitir ampliar las fichas; no comprueba la exactitud del contenido sobre la serie ni exige la distribución de cinco por serie, que corresponde a la selección editorial del paso 3.

`imagen` admite `null` o una ruta local relativa a la raíz del proyecto, usando `/` y sin segmentos `..`. No admite URLs ni rutas absolutas de Linux o Windows. La existencia del recurso se comprobará al mostrar la ficha, con alternativa si falta la imagen.

Las rutas relativas del archivo de catálogo también se resuelven desde la raíz del proyecto. Los errores de archivo ausente, lectura, codificación UTF-8, JSON o esquema se comunican mediante `ErrorCatalogo`, sin crear ni sobrescribir el archivo.

Verificación del catálogo: `python3 -m unittest discover -s tests -p 'test_catalogo.py' -v`, desde la raíz del proyecto. Resultado del paso 4: 19 pruebas correctas con Python 3.10.12; sin dependencias externas ni llamadas al modelo. El fallo de permisos utiliza una simulación; los casos de archivo ausente, JSON dañado y codificación inválida usan archivos temporales reales. Las pruebas completas, incluida la interfaz del paso 5, requieren el entorno con dependencias y se ejecutan con `.venv/bin/python -m unittest discover -s tests -v`.
