"""Nueva presentación del horario (pestañas por día + lista) y ajuste de la sección de contacto."""
import sys

PATH = "C:/Users/nache/Documents/Sherpa/index.html"
s = open(PATH, encoding="utf-8").read()

DAYS = [("Lunes", "Lun"), ("Martes", "Mar"), ("Miércoles", "Mié"), ("Jueves", "Jue"),
        ("Viernes", "Vie"), ("Sábado", "Sáb"), ("Domingo", "Dom")]
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


def panel(di):
    items = [(t, byday[di]) for t, byday in SCHEDULE if di in byday]
    if not items:
        body = '<p class="hz-empty">Hoy no hay clases programadas.</p>'
    else:
        rows = "".join(
            f'<div class="hz-row" data-class="{name}">'
            f'<span class="hz-time">{t}</span>'
            f'<span class="hz-name"><span class="hz-dot" aria-hidden="true"></span>{name}</span>'
            f'</div>'
            for t, name in items
        )
        body = f'<div class="hz-list">{rows}</div>'
    hidden = "" if di == 0 else " hidden"
    return f'<div class="hz-panel" role="tabpanel" data-day="{di}"{hidden}>{body}</div>'


tabs = "".join(
    f'<button type="button" role="tab" class="hz-tab" data-day="{i}" aria-selected="{"true" if i == 0 else "false"}">{short}</button>'
    for i, (_, short) in enumerate(DAYS)
)
filters = "".join(
    f'<button type="button" class="hz-btn" data-filter="{c}" aria-pressed="false">{c}</button>'
    for c in CLASSES
)
panels = "".join(panel(i) for i in range(7))

horarios_html = f'''<!-- HORARIOS -->
<style>
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
.hz-btn,.hz-tab{{min-height:44px;padding:0 16px;border-radius:2px;cursor:pointer;font-family:'Archivo',sans-serif;font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;background:transparent;color:#EEEAE2;border:1px solid rgba(238,234,226,.25)}}
.hz-btn[aria-pressed="true"],.hz-tab[aria-selected="true"]{{background:#FEBD59;color:#0C0D0C;border-color:#FEBD59}}
.hz-filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}}
.hz-tabs{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:0;padding-bottom:20px;border-bottom:1px solid rgba(238,234,226,.14)}}
.hz-list{{border-bottom:1px solid rgba(238,234,226,.1)}}
.hz-row{{display:flex;align-items:center;gap:28px;padding:20px 8px;border-top:1px solid rgba(238,234,226,.1);transition:opacity .2s ease,background-color .2s ease}}
.hz-time{{font-family:'Archivo',sans-serif;font-weight:800;font-size:26px;font-variant-numeric:tabular-nums;min-width:96px}}
.hz-name{{display:flex;align-items:center;gap:12px;font-size:17px;font-weight:600}}
.hz-dot{{width:10px;height:10px;background:#6F6F68;flex-shrink:0}}
.hz-row[data-class="Funcional"] .hz-dot{{background:#FEBD59}}
.hz-row[data-class="Kids"] .hz-dot{{background:#EEEAE2}}
.hz-row[data-class="Entrena con tu Amig@"] .hz-dot{{background:#8E8E86}}
.hz-row[data-class="Wom_Ray (embarazadas)"] .hz-dot{{background:#E6C9A8}}
.hz-row.is-active{{background:rgba(254,189,89,.12);box-shadow:inset 3px 0 0 #FEBD59}}
.hz-row.is-dim{{opacity:.28}}
.hz-empty{{margin:0;padding:32px 8px;color:#A8A8A0}}
.hz-panel[hidden]{{display:none}}
@media (max-width:640px){{.hz-time{{font-size:20px;min-width:72px}}.hz-name{{font-size:15px}}}}
</style>
<section id="horarios" class="a-sec" style="padding-top: 128px; padding-bottom: 128px; background: #121412; border-top: 1px solid rgba(238,234,226,.08); border-bottom: 1px solid rgba(238,234,226,.08)">
<div class="a-wrap">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 24px; margin-bottom: 40px">
<div>
<div class="a-label" style="color: #A8A8A0; margin-bottom: 20px">07 — Horarios</div>
<h2 class="a-disp" style="font-size: clamp(40px, 5vw, 72px)">Tu hora, tu clase</h2>
</div>
<p style="margin: 0; max-width: 380px; color: #A8A8A0">Horario de invierno. Pulsa una clase para ver sus sesiones resaltadas en la semana.</p>
</div>
<div class="hz-filters" role="group" aria-label="Filtrar por clase">
{filters}
</div>
<div class="a-g2" style="display: grid; grid-template-columns: minmax(0, 8fr) minmax(0, 4fr); gap: 40px; align-items: start">
<div>
<div class="hz-tabs" role="tablist" aria-label="Día de la semana">
{tabs}
</div>
{panels}
</div>
<aside style="background: #0C0D0C; border: 1px solid rgba(238,234,226,.12); padding: 32px; display: flex; flex-direction: column; gap: 20px">
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FEBD59" stroke-width="1.5" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="2"></rect><path d="M10 18h4"></path></svg>
<h3 style="margin: 0; font-size: 22px; font-weight: 600">Reserva desde la app</h3>
<p style="margin: 0; color: #A8A8A0; font-size: 15px">Apúntate a tu clase, consulta el WOD del día y registra tus marcas desde WodBuster.</p>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 14px; color: #C9C6BE">
<li>— Reserva hasta [7 días] antes</li>
<li>— Cancela sin coste hasta [2 h] antes</li>
<li>— Entrenamiento personal: con cita previa</li>
</ul>
<div style="display: flex; gap: 8px; flex-wrap: wrap">
<a href="#" class="a-btn a-btn-g" style="min-height: 44px; padding: 0 16px; font-size: 12px">App Store</a>
<a href="#" class="a-btn a-btn-g" style="min-height: 44px; padding: 0 16px; font-size: 12px">Google Play</a>
</div>
</aside>
</div>
</div>
</section>
<script>
(function () {{
  var tabs = document.querySelectorAll('.hz-tab');
  var panels = document.querySelectorAll('.hz-panel');
  var filters = document.querySelectorAll('.hz-btn');
  var rows = document.querySelectorAll('.hz-row');

  function showDay(i) {{
    tabs.forEach(function (t) {{ t.setAttribute('aria-selected', String(Number(t.getAttribute('data-day')) === i)); }});
    panels.forEach(function (p) {{ p.hidden = Number(p.getAttribute('data-day')) !== i; }});
  }}
  function applyFilter() {{
    var sel = [];
    filters.forEach(function (b) {{ if (b.getAttribute('aria-pressed') === 'true') sel.push(b.getAttribute('data-filter')); }});
    rows.forEach(function (r) {{
      var hit = sel.indexOf(r.getAttribute('data-class')) > -1;
      r.classList.toggle('is-active', hit);
      r.classList.toggle('is-dim', sel.length > 0 && !hit);
    }});
  }}

  tabs.forEach(function (t) {{
    t.addEventListener('click', function () {{ showDay(Number(t.getAttribute('data-day'))); }});
  }});
  filters.forEach(function (b) {{
    b.addEventListener('click', function () {{
      b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      applyFilter();
    }});
  }});

  // Abre el día de hoy (lunes = 0 … domingo = 6)
  var today = (new Date().getDay() + 6) % 7;
  showDay(today);
}})();
</script>

'''

hs = s.index("<!-- HORARIOS -->")
he = s.index("<!-- TARIFAS -->")
s = s[:hs] + horarios_html + s[he:]

# ---------------------------------------------------------------- Contacto: título que no invade el formulario
cta = s.index("<!-- CTA + CONTACTO -->")
seg_end = s.index("<!-- MAPA -->", cta)
seg = s[cta:seg_end]
old_grid = 'grid-template-columns: minmax(0, 6fr) minmax(0, 6fr); gap: 72px; align-items: start'
if seg.count(old_grid) != 1:
    sys.exit("ABORT: contact grid not found once")
seg = seg.replace(old_grid, 'grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: 72px; align-items: start')
old_h2 = '<h2 class="a-disp" style="font-size: clamp(48px, 6.4vw, 104px)">Tu primera clase va por nuestra cuenta.</h2>'
if seg.count(old_h2) != 1:
    sys.exit("ABORT: contact heading not found once")
seg = seg.replace(old_h2, '<h2 class="a-disp" style="font-size: clamp(40px, 4.6vw, 72px); overflow-wrap: break-word">Tu primera clase va por nuestra cuenta.</h2>')
s = s[:cta] + seg + s[seg_end:]

open(PATH, "w", encoding="utf-8", newline="\n").write(s)
print("OK")
