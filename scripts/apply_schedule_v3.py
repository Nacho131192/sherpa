"""Horario semanal completo (días en columnas) y retirada del bloque de reserva."""
import sys

PATH = "C:/Users/nache/Documents/Sherpa/index.html"
s = open(PATH, encoding="utf-8").read()

DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
F, K, A, W = "Funcional", "Kids", "Entrena con tu Amig@", "Wom_Ray (embarazadas)"
ALL = {0, 1, 2, 3, 4}
SCHEDULE = [
    ("07:00", {0: F, 2: F, 4: F}),
    ("07:30", {1: F, 3: F}),
    ("08:30", {d: F for d in ALL}),
    ("09:00", {5: A}),
    ("09:30", {0: F, 2: F, 4: F}),
    ("10:30", {1: W}),
    ("13:00", {1: F, 4: F}),
    ("16:00", {4: W}),
    ("17:00", {0: F, 1: K, 2: F, 3: K, 4: F}),
    ("18:00", {d: F for d in ALL}),
    ("19:00", {d: F for d in ALL}),
    ("20:00", {d: F for d in ALL}),
]
CLASSES = [F, A, K, W]

cells = ['<div class="hz-corner" aria-hidden="true"></div>']
cells += [f'<div class="hz-dayhead" role="columnheader">{d}</div>' for d in DAYS]
for t, byday in SCHEDULE:
    cells.append(f'<div class="hz-time" role="rowheader">{t}</div>')
    for d in range(7):
        name = byday.get(d)
        if name:
            cells.append(
                f'<div class="hz-cell"><span class="hz-card" data-class="{name}">{name}</span></div>'
            )
        else:
            cells.append('<div class="hz-cell"></div>')
grid = '<div class="hz-week" role="table" aria-label="Horario de invierno semanal">' + "".join(cells) + "</div>"

filters = "".join(
    f'<button type="button" class="hz-btn" data-filter="{c}" aria-pressed="false">{c}</button>'
    for c in CLASSES
)

horarios_html = f'''<!-- HORARIOS -->
<style>
.hz-filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}}
.hz-btn{{min-height:44px;padding:0 16px;border-radius:2px;cursor:pointer;font-family:'Archivo',sans-serif;font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;background:transparent;color:#EEEAE2;border:1px solid rgba(238,234,226,.25)}}
.hz-btn[aria-pressed="true"]{{background:#FEBD59;color:#0C0D0C;border-color:#FEBD59}}
.hz-scroll{{overflow-x:auto;padding-bottom:8px}}
.hz-week{{display:grid;grid-template-columns:84px repeat(7,minmax(128px,1fr));gap:8px;min-width:1000px}}
.hz-dayhead{{font-family:'Archivo',sans-serif;font-weight:800;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#A8A8A0;padding:0 4px 14px;border-bottom:1px solid rgba(238,234,226,.14)}}
.hz-time{{font-family:'Archivo',sans-serif;font-weight:700;font-size:15px;font-variant-numeric:tabular-nums;color:#EEEAE2;padding-top:12px}}
.hz-cell{{min-height:58px;border-top:1px solid rgba(238,234,226,.06);padding-top:6px}}
.hz-card{{display:block;height:100%;box-sizing:border-box;padding:9px 10px;font-size:13px;font-weight:600;line-height:1.25;color:#EEEAE2;background:rgba(238,234,226,.05);border-left:3px solid #FEBD59;transition:opacity .2s ease,background-color .2s ease,color .2s ease}}
.hz-card[data-class="Kids"]{{border-left-color:#EEEAE2}}
.hz-card[data-class="Entrena con tu Amig@"]{{border-left-color:#8E8E86}}
.hz-card[data-class="Wom_Ray (embarazadas)"]{{border-left-color:#E6C9A8}}
.hz-card.is-active{{background:#FEBD59;color:#0C0D0C}}
.hz-card.is-dim{{opacity:.22}}
</style>
<section id="horarios" class="a-sec" style="padding-top: 128px; padding-bottom: 128px; background: #121412; border-top: 1px solid rgba(238,234,226,.08); border-bottom: 1px solid rgba(238,234,226,.08)">
<div class="a-wrap">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 24px; margin-bottom: 40px">
<div>
<div class="a-label" style="color: #A8A8A0; margin-bottom: 20px">07 — Horarios</div>
<h2 class="a-disp" style="font-size: clamp(40px, 5vw, 72px)">Tu hora, tu clase</h2>
</div>
<p style="margin: 0; max-width: 380px; color: #A8A8A0">Horario de invierno. Pulsa una clase para resaltar sus sesiones en la semana.</p>
</div>
<div class="hz-filters" role="group" aria-label="Filtrar por clase">
{filters}
</div>
<div class="hz-scroll">
{grid}
</div>
</div>
</section>
<script>
(function () {{
  var filters = document.querySelectorAll('.hz-btn');
  var cards = document.querySelectorAll('.hz-card');
  function apply() {{
    var sel = [];
    filters.forEach(function (b) {{ if (b.getAttribute('aria-pressed') === 'true') sel.push(b.getAttribute('data-filter')); }});
    cards.forEach(function (c) {{
      var hit = sel.indexOf(c.getAttribute('data-class')) > -1;
      c.classList.toggle('is-active', hit);
      c.classList.toggle('is-dim', sel.length > 0 && !hit);
    }});
  }}
  filters.forEach(function (b) {{
    b.addEventListener('click', function () {{
      b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      apply();
    }});
  }});
}})();
</script>

'''

hs = s.index("<!-- HORARIOS -->")
he = s.index("<!-- TARIFAS -->")
s = s[:hs] + horarios_html + s[he:]
open(PATH, "w", encoding="utf-8", newline="\n").write(s)
print("OK", s.count("Reserva desde la app"))
