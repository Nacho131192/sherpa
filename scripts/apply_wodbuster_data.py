"""Aplica en index.html los datos públicos de la web provisional de WodBuster:
coaches (nombre y foto), horario de invierno y tarifas.
"""
import sys

PATH = "C:/Users/nache/Documents/Sherpa/index.html"
s = open(PATH, encoding="utf-8").read()


def must_once(text):
    n = s.count(text)
    if n != 1:
        sys.exit(f"ABORT: expected 1 match, found {n}: {text[:80]!r}")


# ---------------------------------------------------------------- Horario
DAYS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
F, K, A, W = "Funcional", "Kids", "Entrena con tu Amig@", "Wom_Ray (embarazadas)"
WEEK = {0, 1, 2, 3, 4}
SCHEDULE = [
    ("07:00", {0: F, 2: F, 4: F}),
    ("07:30", {1: F, 3: F}),
    ("08:30", {d: F for d in WEEK}),
    ("09:00", {5: A}),
    ("09:30", {0: F, 2: F, 4: F}),
    ("10:30", {1: W}),
    ("13:00", {1: F, 4: F}),
    ("16:00", {4: W}),
    ("17:00", {0: F, 1: K, 2: F, 3: K, 4: F}),
    ("18:00", {d: F for d in WEEK}),
    ("19:00", {d: F for d in WEEK}),
    ("20:00", {d: F for d in WEEK}),
]
CLASSES = [F, A, K, W]


def cell(name):
    if not name:
        return "<td></td>"
    return (f'<td><span class="hz-cls" data-class="{name}">{name}</span></td>')


rows = []
for t, byday in SCHEDULE:
    tds = "".join(cell(byday.get(d)) for d in range(7))
    rows.append(f'<tr><th scope="row" class="hz-time">{t}</th>{tds}</tr>')

head = "".join(f'<th scope="col">{d}</th>' for d in DAYS)
table = (
    '<div class="hz-scroll"><table class="hz-table">'
    '<caption class="sr-only">Horario de invierno semanal</caption>'
    f'<thead><tr><th scope="col"><span class="sr-only">Hora</span></th>{head}</tr></thead>'
    f'<tbody>{"".join(rows)}</tbody></table></div>'
)
buttons = "".join(
    f'<button type="button" class="hz-btn" data-filter="{c}" aria-pressed="false">{c}</button>'
    for c in CLASSES
)

horarios_html = f'''<!-- HORARIOS -->
<style>
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
.hz-btn{{min-height:44px;padding:0 18px;border-radius:2px;cursor:pointer;font-family:'Archivo',sans-serif;font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;background:transparent;color:#EEEAE2;border:1px solid rgba(238,234,226,.25)}}
.hz-btn[aria-pressed="true"]{{background:#FEBD59;color:#0C0D0C;border-color:#FEBD59}}
.hz-scroll{{overflow-x:auto}}
.hz-table{{width:100%;min-width:760px;border-collapse:collapse;font-size:14px}}
.hz-table th,.hz-table td{{padding:8px 6px;border-top:1px solid rgba(238,234,226,.1);vertical-align:top;text-align:left}}
.hz-table thead th{{font-family:'Archivo',sans-serif;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#A8A8A0;border-top:0;padding-bottom:14px}}
.hz-time{{font-family:'Archivo',sans-serif;font-weight:700;font-size:16px;font-variant-numeric:tabular-nums;white-space:nowrap}}
.hz-cls{{display:block;padding:8px 10px;line-height:1.3;border-left:3px solid #6F6F68;background:rgba(238,234,226,.04);transition:opacity .2s ease,background-color .2s ease}}
.hz-cls.is-active{{background:#FEBD59;color:#0C0D0C;border-left-color:#0C0D0C}}
.hz-cls.is-dim{{opacity:.25}}
</style>
<section id="horarios" class="a-sec" style="padding-top: 128px; padding-bottom: 128px; background: #121412; border-top: 1px solid rgba(238,234,226,.08); border-bottom: 1px solid rgba(238,234,226,.08)">
<div class="a-wrap">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 24px; margin-bottom: 40px">
<div>
<div class="a-label" style="color: #A8A8A0; margin-bottom: 20px">07 — Horarios</div>
<h2 class="a-disp" style="font-size: clamp(40px, 5vw, 72px)">Tu hora, tu clase</h2>
</div>
<p style="margin: 0; max-width: 380px; color: #A8A8A0">Horario de invierno. Pulsa una clase para ver dónde encaja en la semana.</p>
</div>
<div role="group" aria-label="Filtrar por clase" style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px">
{buttons}
</div>
<div class="a-g2" style="display: grid; grid-template-columns: minmax(0, 8fr) minmax(0, 4fr); gap: 40px; align-items: start">
<div>
{table}
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
  var btns = document.querySelectorAll('.hz-btn');
  var cells = document.querySelectorAll('.hz-cls');
  function apply() {{
    var sel = [];
    btns.forEach(function (b) {{ if (b.getAttribute('aria-pressed') === 'true') sel.push(b.getAttribute('data-filter')); }});
    cells.forEach(function (c) {{
      var hit = sel.indexOf(c.getAttribute('data-class')) > -1;
      c.classList.toggle('is-active', hit);
      c.classList.toggle('is-dim', sel.length > 0 && !hit);
    }});
  }}
  btns.forEach(function (b) {{
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

# ---------------------------------------------------------------- Tarifas
tarifas_cards = '''<div class="a-g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; align-items: stretch">
<div style="border: 1px solid rgba(238,234,226,.14); padding: 40px 32px; display: flex; flex-direction: column; gap: 24px">
<div class="a-label" style="color: #A8A8A0">Entrenamiento funcional</div>
<h3 class="a-disp" style="font-size: 32px">8 sesiones</h3>
<div style="display: flex; align-items: baseline; gap: 6px"><span style="font-family: 'Archivo', sans-serif; font-weight: 800; font-size: 56px; line-height: 1">45,00 €</span><span style="color: #A8A8A0">/mes</span></div>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 15px; color: #C9C6BE; flex-grow: 1">
<li>✓ 8 clases al mes</li><li>✓ Funcional, Entrena con tu Amig@ y Wom_Ray</li><li>✓ Reserva en app</li>
</ul>
<a href="#contacto" class="a-btn a-btn-g" style="justify-content: center">Empezar</a>
</div>
<div style="border: 1px solid #FEBD59; background: #161310; padding: 40px 32px; display: flex; flex-direction: column; gap: 24px; position: relative">
<div style="position: absolute; top: -1px; right: -1px; background: #FEBD59; color: #0C0D0C; font-family: 'Archivo', sans-serif; font-weight: 800; font-size: 11px; letter-spacing: .14em; padding: 8px 12px">RECOMENDADA</div>
<div class="a-label" style="color: #FEBD59">Entrenamiento funcional</div>
<h3 class="a-disp" style="font-size: 32px">12 sesiones</h3>
<div style="display: flex; align-items: baseline; gap: 6px"><span style="font-family: 'Archivo', sans-serif; font-weight: 800; font-size: 56px; line-height: 1">50,00 €</span><span style="color: #A8A8A0">/mes</span></div>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 15px; color: #C9C6BE; flex-grow: 1">
<li>✓ 12 clases al mes</li><li>✓ Funcional, Entrena con tu Amig@ y Wom_Ray</li><li>✓ Reserva en app</li>
</ul>
<a href="#contacto" class="a-btn a-btn-p" style="justify-content: center">Empezar</a>
</div>
<div style="border: 1px solid rgba(238,234,226,.14); padding: 40px 32px; display: flex; flex-direction: column; gap: 24px">
<div class="a-label" style="color: #A8A8A0">Entrenamiento funcional</div>
<h3 class="a-disp" style="font-size: 32px">Ilimitado</h3>
<div style="display: flex; align-items: baseline; gap: 6px"><span style="font-family: 'Archivo', sans-serif; font-weight: 800; font-size: 56px; line-height: 1">60,00 €</span><span style="color: #A8A8A0">/mes</span></div>
<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 15px; color: #C9C6BE; flex-grow: 1">
<li>✓ Clases ilimitadas</li><li>✓ Funcional, Entrena con tu Amig@ y Wom_Ray</li><li>✓ Reserva en app</li>
</ul>
<a href="#contacto" class="a-btn a-btn-g" style="justify-content: center">Empezar</a>
</div>
</div>
<div class="a-g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: rgba(238,234,226,.12); border: 1px solid rgba(238,234,226,.12); margin-top: 20px">
<div style="background: #0C0D0C; padding: 28px 32px">
<div style="font-weight: 600; margin-bottom: 12px">Entrenamiento personal</div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Sesión suelta</span><span>[XX] €</span></div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Bono 5 sesiones</span><span>[XX] €</span></div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Bono 10 sesiones</span><span>[XX] €</span></div>
</div>
<div style="background: #0C0D0C; padding: 28px 32px">
<div style="font-weight: 600; margin-bottom: 12px">Mamá Sherpa</div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Wom_Ray (embarazadas)</span><span>30,00 €/mes</span></div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Postparto</span><span>[XX] €/mes</span></div>
</div>
<div style="background: #0C0D0C; padding: 28px 32px">
<div style="font-weight: 600; margin-bottom: 12px">Otros</div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Kids · 8 sesiones</span><span>30,00 €/mes</span></div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Drop-in</span><span>1,00 €</span></div>
<div style="display: flex; justify-content: space-between; font-size: 15px; color: #C9C6BE; padding: 6px 0"><span>Matrícula</span><span>[XX] €</span></div>
</div>
</div>
'''
ts = s.index('<div class="a-g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; align-items: stretch">')
te = s.index("</div>\n</section>\n\n<!-- EQUIPO", ts)
s = s[:ts] + tarifas_cards + s[te:]

# ---------------------------------------------------------------- Coaches
coaches = [
    ("assets/coaches/antonio-salguero.jpg", "Antonio Salguero"),
    ("assets/coaches/marievap3085.jpg", "marievap3085"),
    ("assets/coaches/dunia.jpg", "Dunia"),
]
figs = "".join(
    f'<figure style="margin: 0; display: flex; flex-direction: column; gap: 14px"><img src="{src}" alt="Foto de {name}" style="width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block"><figcaption style="font-weight: 600; font-size: 18px">{name}</figcaption></figure>'
    for src, name in coaches
)
grid_new = '<div class="a-g3" style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px">' + figs + "</div>\n\n"
cs = s.index('<div class="a-g4" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px">')
ce = s.index('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 24px; margin-top: 112px', cs)
s = s[:cs] + grid_new + s[ce:]

# ---------------------------------------------------------------- DC script: keep only FAQ logic
s = s.replace("    var day = st.day == null ? 0 : st.day;\n", "")
c0 = s.index("    var C = {")
c1 = s.index("    var qs = [")
s = s[:c0] + s[c1:]
must_once("    return { days: days, sessions: sessions, faqs: faqs };")
s = s.replace("    return { days: days, sessions: sessions, faqs: faqs };", "    return { faqs: faqs };")

open(PATH, "w", encoding="utf-8", newline="\n").write(s)
print("OK")
