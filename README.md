# Mario Bros Arcade

Juego arcade estilo Mario Bros hecho con [Pyxel](https://github.com/kitao/pyxel).

Autores: Héctor Molina Garde & Nicolás Maire Bravo

## Ejecutar

```bash
uv run src/main.py
```

`uv` lee las dependencias del bloque `# /// script` al principio de `src/main.py`
(solo `pyxel`) y las instala automáticamente.

## Estructura

- `src/` — juego principal (`main.py`, `mario_module.py`, `Constants.py`, `Highscore.py`)
- `src/enemy/` — enemigos y monedas
- `src/scene/` — escenario y attrezo (plataformas, bloques, tuberías, POW)

## Controles

- Flechas: mover
- Espacio: saltar / empezar
- Q: salir
