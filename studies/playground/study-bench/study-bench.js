/* @ds-bundle: {"format":4,"namespace":"StudyBench","components":[{"name":"Algorithm"},{"name":"AppBar"},{"name":"BackupDiagram"},{"name":"Bench"},{"name":"Button"},{"name":"Callout"},{"name":"Chips"},{"name":"ConceptCards"},{"name":"Controls"},{"name":"CourseMap"},{"name":"Cover"},{"name":"DecisionGuide"},{"name":"DemoMode"},{"name":"DiffLedger"},{"name":"Drawer"},{"name":"Equation"},{"name":"EquationLineage"},{"name":"Flashcards"},{"name":"FlowDiagram"},{"name":"FormulaSheet"},{"name":"GlossaryMap"},{"name":"GridWorld"},{"name":"GuidedTour"},{"name":"Hero"},{"name":"KeyTermNotes"},{"name":"Legend"},{"name":"LineChart"},{"name":"LineageMap"},{"name":"LinkedHighlight"},{"name":"MasterTable"},{"name":"MethodRack"},{"name":"MethodsTable"},{"name":"NotationSheet"},{"name":"Orientation"},{"name":"Overview"},{"name":"PageGuide"},{"name":"PageShell"},{"name":"Panel"},{"name":"PayoffMatrix"},{"name":"Quiz"},{"name":"Readout"},{"name":"ReturnNav"},{"name":"Search"},{"name":"Segmented"},{"name":"SideBySide"},{"name":"States"},{"name":"StoryMode"},{"name":"Takeaways"},{"name":"TermHover"},{"name":"TopicNav"},{"name":"TopicPage"},{"name":"TopicPager"},{"name":"Trajectory"},{"name":"UpdateEngine"},{"name":"VisualGlossary"},{"name":"WorkedExample"}]} */
/* Study Bench helpers v2.7 (equation keys, glossary walk-through, faceted filters; return navigation, card links, guide waits for Next; page shell, theme toggle, demo hint; key-term notes, autolink, demo mode, visual glossary). Vanilla, no dependencies. Every engine styles its marks through tokens
   (style="stroke:var(--…)"), so light/dark switches need no redraw except where a color is computed (grid). */
(function () {
  "use strict";
  var root = document.documentElement;
  var SVGNS = "http://www.w3.org/2000/svg";

  /* ---------- tokens & theme ---------- */
  function token(name) { return getComputedStyle(root).getPropertyValue("--" + name).trim(); }
  var ROLE_NAMES = ["paper", "surface", "surface-sunk", "bench", "bench-grid", "line", "line-strong",
    "ink", "ink-2", "ink-3", "accent", "accent-soft", "on-accent", "hl", "good", "bad", "warn",
    "data-1", "data-2", "data-3", "data-4", "data-5", "data-6", "data-7", "data-8",
    "seq-lo", "seq-hi", "div-neg", "div-mid", "div-pos",
    "q-new", "q-changed", "q-reward", "q-value", "q-policy", "q-ratio", "q-trace", "q-model",
    "agent-1", "agent-2", "agent-3", "equilibrium", "pareto",
    "frame-x", "frame-y", "frame-z", "robot-body", "vec-twist", "vec-wrench"];
  function palette() {
    var cs = getComputedStyle(root), out = {};
    for (var i = 0; i < ROLE_NAMES.length; i++) out[ROLE_NAMES[i]] = cs.getPropertyValue("--" + ROLE_NAMES[i]).trim();
    return out;
  }
  function onThemeChange(cb) {
    var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
    var fire = function () { cb(palette()); };
    if (mq && mq.addEventListener) mq.addEventListener("change", fire);
    var mo = new MutationObserver(fire);
    mo.observe(root, { attributes: true, attributeFilter: ["data-theme"] });
    fire();
    return function () { if (mq && mq.removeEventListener) mq.removeEventListener("change", fire); mo.disconnect(); };
  }

  /* ---------- small utilities ---------- */
  function svg(tag, attrs, parent) {
    var e = document.createElementNS(SVGNS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function html(tag, attrs, text, parent) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function esc(s) { return (window.CSS && CSS.escape) ? CSS.escape(s) : String(s).replace(/"/g, '\\"'); }
  function store(key, val) {
    try {
      if (val === undefined) { var v = localStorage.getItem(key); return v ? JSON.parse(v) : null; }
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function ensureArrow(s, id) {
    var defs = svg("defs", null, s);
    var m = svg("marker", { id: id, viewBox: "0 0 10 10", refX: "9", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" }, defs);
    svg("path", { d: "M0 0 L10 5 L0 10 z", "class": "sb-arrowhead" }, m);
    return "url(#" + id + ")";
  }
  var uid = 0; function nextId(p) { uid += 1; return (p || "sb") + "-" + uid; }

  /* ---------- color scales ---------- */
  function hex(h) { h = h.replace("#", ""); if (h.length === 3) h = h.replace(/(.)/g, "$1$1"); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function mix(a, b, t) { var x = hex(a), y = hex(b); return "rgb(" + [0, 1, 2].map(function (i) { return Math.round(x[i] + (y[i] - x[i]) * t); }).join(",") + ")"; }
  function lum(rgb) { var m = rgb.match(/\d+/g).map(Number).map(function (c) { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }); return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]; }
  function seq(t) { return mix(token("seq-lo"), token("seq-hi"), Math.max(0, Math.min(1, t))); }
  function div(t) { t = Math.max(0, Math.min(1, t)); return t < 0.5 ? mix(token("div-neg"), token("div-mid"), t * 2) : mix(token("div-mid"), token("div-pos"), (t - 0.5) * 2); }

  /* ---------- segmented ---------- */
  function segmented(el, onChange) {
    function pick(b, focus) {
      var bs = el.querySelectorAll("button");
      for (var i = 0; i < bs.length; i++) { bs[i].setAttribute("aria-pressed", bs[i] === b ? "true" : "false"); bs[i].tabIndex = bs[i] === b ? 0 : -1; }
      if (focus) b.focus();
      if (onChange) onChange(b.value || b.textContent.trim(), b);
    }
    var bs0 = el.querySelectorAll("button"), cur = el.querySelector('button[aria-pressed="true"]') || bs0[0];
    for (var i = 0; i < bs0.length; i++) bs0[i].tabIndex = bs0[i] === cur ? 0 : -1;
    el.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b && el.contains(b)) pick(b, false); });
    el.addEventListener("keydown", function (e) {
      var bs = Array.prototype.slice.call(el.querySelectorAll("button")), k = bs.indexOf(document.activeElement); if (k < 0) return;
      var n = e.key === "ArrowRight" || e.key === "ArrowDown" ? k + 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? k - 1 : e.key === "Home" ? 0 : e.key === "End" ? bs.length - 1 : null;
      if (n === null) return; e.preventDefault(); pick(bs[(n + bs.length) % bs.length], true);
    });
  }

  /* ---------- linked highlighting: every [data-sym="x"] inside scope lights up together ---------- */
  function symOf(el) {
    if (!el || !el.closest) return null;
    var t = el.closest('[data-sym],[class*="sym-"]');
    if (!t) return null;
    if (t.hasAttribute("data-sym")) return { el: t, sym: t.getAttribute("data-sym") };
    var m = String(t.getAttribute("class") || "").match(/(?:^|\s)sym-([\w-]+)/);
    return m ? { el: t, sym: m[1] } : null;
  }
  function link(scope) {
    scope = scope || document;
    function set(sym, on) {
      var els = scope.querySelectorAll('[data-sym="' + esc(sym) + '"], .sym-' + esc(sym));
      for (var i = 0; i < els.length; i++) els[i].classList.toggle("is-lit", on);
      if (scope.classList) scope.classList.toggle("has-lit", on);
    }
    var pinned = null;
    function over(e) { if (e.pointerType === "touch") return; var t = symOf(e.target); if (t && scope.contains(t.el)) set(t.sym, true); }
    function out(e) { if (e.pointerType === "touch") return; var t = symOf(e.target); if (t && scope.contains(t.el) && t.sym !== pinned) set(t.sym, false); }
    function focusIn(e) { var t = symOf(e.target); if (t && scope.contains(t.el)) set(t.sym, true); }
    function focusOut(e) { var t = symOf(e.target); if (t && scope.contains(t.el) && t.sym !== pinned) set(t.sym, false); }
    scope.addEventListener("pointerover", over); scope.addEventListener("pointerout", out);
    scope.addEventListener("focusin", focusIn); scope.addEventListener("focusout", focusOut);
    /* tap or click pins a symbol (touch screens have no hover); tap again, tap elsewhere or Escape clears */
    scope.addEventListener("click", function (e) {
      var t = symOf(e.target);
      if (pinned) set(pinned, false);
      pinned = t && scope.contains(t.el) && t.sym !== pinned ? t.sym : null;
      if (pinned) set(pinned, true);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && pinned) { set(pinned, false); pinned = null; } });
    return { light: function (sym) { set(sym, true); }, clear: function (sym) { set(sym, false); } };
  }

  /* ---------- stepper: [data-on="2 4-6"] elements get .is-on at those steps; [data-step-text="n"] shows at step n ---------- */
  function inSpec(spec, i) {
    return String(spec).split(/[\s,]+/).some(function (p) {
      if (!p) return false;
      if (p.indexOf("-") > 0) { var ab = p.split("-"); return i >= +ab[0] && i <= +ab[1]; }
      if (p.slice(-1) === "+") return i >= +p.slice(0, -1);
      return +p === i;
    });
  }
  function stepper(rootEl, opts) {
    opts = opts || {};
    var n = +(rootEl.getAttribute("data-steps") || opts.steps || 1), i = 1, timer = null;
    var status = rootEl.querySelector("[data-status]"), scrub = rootEl.querySelector('[data-act="scrub"]');
    var playBtn = rootEl.querySelector('[data-act="play"]');
    if (scrub) { scrub.min = 1; scrub.max = n; scrub.step = 1; }
    function render() {
      var ons = rootEl.querySelectorAll("[data-on]");
      for (var k = 0; k < ons.length; k++) {
        var on = inSpec(ons[k].getAttribute("data-on"), i);
        ons[k].classList.toggle("is-on", on);
        ons[k].classList.toggle("is-past", !on && firstStep(ons[k]) < i);
      }
      var texts = rootEl.querySelectorAll("[data-step-text]");
      for (var t = 0; t < texts.length; t++) texts[t].hidden = +texts[t].getAttribute("data-step-text") !== i;
      if (status) status.textContent = "Step " + i + " of " + n;
      if (scrub) { scrub.value = i; scrub.setAttribute("aria-valuetext", "Step " + i + " of " + n); }
      var prev = rootEl.querySelector('[data-act="prev"]'), next = rootEl.querySelector('[data-act="next"]');
      if (prev) prev.disabled = i <= 1;
      if (next) next.disabled = i >= n;
      rootEl.setAttribute("data-step", i);
      if (playBtn && !timer) playBtn.textContent = i >= n ? "Replay ↺" : "Play ▶";
      if (opts.onStep) opts.onStep(i);
    }
    function firstStep(el) { for (var s = 1; s <= n; s++) if (inSpec(el.getAttribute("data-on"), s)) return s; return n + 1; }
    function go(k) { i = Math.max(1, Math.min(n, k)); render(); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } if (playBtn) { playBtn.textContent = i >= n ? "Replay ↺" : "Play ▶"; playBtn.setAttribute("aria-pressed", "false"); } }
    function play() {
      if (timer) return stop();
      if (i >= n) go(1);
      if (playBtn) { playBtn.textContent = "Pause ❚❚"; playBtn.setAttribute("aria-pressed", "true"); }
      timer = setInterval(function () { if (i >= n) stop(); else go(i + 1); }, opts.interval || 1800);
    }
    rootEl.addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]"); if (!b || !rootEl.contains(b)) return;
      var a = b.getAttribute("data-act");
      if (a === "prev") { stop(); go(i - 1); } else if (a === "next") { stop(); go(i + 1); }
      else if (a === "play") play(); else if (a === "reset") { stop(); go(1); }
      else if (a === "goto") { stop(); go(+b.getAttribute("data-goto")); }
    });
    if (scrub) scrub.addEventListener("input", function () { stop(); go(+scrub.value); });
    rootEl.addEventListener("keydown", function (e) {
      if (e.target.matches("input,select,textarea")) return;
      if (e.key === "ArrowRight") { stop(); go(i + 1); e.preventDefault(); }
      if (e.key === "ArrowLeft") { stop(); go(i - 1); e.preventDefault(); }
    });
    render();
    return { go: go, play: play, stop: stop, get step() { return i; } };
  }

  /* ---------- flow: workflow / process diagram with a walk-through ---------- */
  /* spec: {w,h, nodes:[{id,x,y,w,h,label,sub,kind}], edges:[{id,from,to,label,via:[[x,y]],side:"r|l|t|b"}], steps:[{on:[ids],text}]} */
  function flow(host, spec) {
    host.classList.add("sb-flow");
    var fig = html("figure", { "class": "sb-fig" }, null, host);
    var sc = html("div", { "class": "sb-scroll-x" }, null, fig);
    var s = svg("svg", { viewBox: "0 0 " + spec.w + " " + spec.h, role: "img", "aria-label": spec.title || "Workflow diagram" }, sc);
    var arrow = ensureArrow(s, nextId("arr"));
    var N = {}, E = {};
    spec.nodes.forEach(function (n) { N[n.id] = n; });
    function anchor(n, side) {
      var cx = n.x + n.w / 2, cy = n.y + n.h / 2;
      if (side === "r") return [n.x + n.w, cy]; if (side === "l") return [n.x, cy];
      if (side === "t") return [cx, n.y]; if (side === "b") return [cx, n.y + n.h];
      return [cx, cy];
    }
    function autoSide(a, b) {
      var dx = (b.x + b.w / 2) - (a.x + a.w / 2), dy = (b.y + b.h / 2) - (a.y + a.h / 2);
      return Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? ["r", "l"] : ["l", "r"]) : (dy > 0 ? ["b", "t"] : ["t", "b"]);
    }
    var gE = svg("g", { "class": "sb-flow-edges" }, s), gN = svg("g", { "class": "sb-flow-nodes" }, s);
    spec.edges.forEach(function (e, k) {
      var a = N[e.from], b = N[e.to], sides = e.sides || autoSide(a, b);
      var p0 = anchor(a, sides[0]), p1 = anchor(b, sides[1]);
      var pts = [p0].concat(e.via || []).concat([p1]);
      var d = "M" + pts.map(function (p) { return p[0] + " " + p[1]; }).join(" L");
      var id = e.id || (e.from + ">" + e.to);
      var g = svg("g", { "class": "sb-flow-edge", "data-id": id }, gE);
      var path = svg("path", { d: d, "marker-end": arrow }, g);
      if (e.dashed) path.setAttribute("stroke-dasharray", "5 4");
      if (e.label) {
        var mid = e.labelAt || [(pts[Math.floor((pts.length - 1) / 2)][0] + pts[Math.ceil((pts.length - 1) / 2)][0]) / 2 + (pts.length === 2 ? 0 : 0), (pts[Math.floor((pts.length - 1) / 2)][1] + pts[Math.ceil((pts.length - 1) / 2)][1]) / 2];
        var tl = svg("text", { x: mid[0] + (e.dx || 0), y: mid[1] + (e.dy || -6), "text-anchor": e.anchor || "middle", "class": "sb-flow-elabel" }, g);
        tl.textContent = e.label;
      }
      E[id] = { g: g, path: path };
    });
    spec.nodes.forEach(function (n) {
      var g = svg("g", { "class": "sb-flow-node" + (n.kind ? " is-" + n.kind : ""), "data-id": n.id, tabindex: "0", role: "img", "aria-label": n.label + (n.sub ? ", " + n.sub : "") }, gN);
      if (n.sym) g.setAttribute("data-sym", n.sym);
      svg("rect", { x: n.x, y: n.y, width: n.w, height: n.h, rx: n.kind === "store" ? 3 : 8 }, g);
      var t = svg("text", { x: n.x + n.w / 2, y: n.y + n.h / 2 + (n.sub ? -3 : 4), "text-anchor": "middle", "class": "sb-flow-label" }, g);
      t.textContent = n.label;
      if (n.sub) { var st = svg("text", { x: n.x + n.w / 2, y: n.y + n.h / 2 + 13, "text-anchor": "middle", "class": "sb-flow-sub" }, g); st.textContent = n.sub; }
      N[n.id].g = g;
    });
    var dot = svg("circle", { r: 5, "class": "sb-flow-token", cx: -20, cy: -20 }, s);
    if (spec.caption) html("figcaption", { "class": "sb-caption" }, spec.caption, fig);
    var api = { svg: s };
    if (spec.steps && spec.steps.length) {
      var ctl = html("div", { "class": "sb-flow-ctl", "data-steps": spec.steps.length }, null, host);
      ctl.innerHTML = '<div class="sb-btn-row"><button class="sb-btn sb-btn--primary" data-act="play" aria-pressed="false">Play ▶</button><button class="sb-btn" data-act="prev">← Back</button><button class="sb-btn" data-act="next">Next →</button><span class="sb-status" data-status></span></div><p class="sb-flow-text" aria-live="polite"></p>';
      var textEl = ctl.querySelector(".sb-flow-text"), raf = null;
      var st = stepper(ctl, {
        interval: spec.interval || 2200,
        onStep: function (i) {
          var step = spec.steps[i - 1];
          Object.keys(N).forEach(function (k) { N[k].g.classList.remove("is-on"); });
          Object.keys(E).forEach(function (k) { E[k].g.classList.remove("is-on"); });
          host.classList.add("is-walking");
          (step.on || []).forEach(function (id) { if (N[id]) N[id].g.classList.add("is-on"); if (E[id]) E[id].g.classList.add("is-on"); });
          textEl.textContent = step.text || "";
          var movingEdge = (step.on || []).filter(function (id) { return E[id]; })[0];
          if (raf) cancelAnimationFrame(raf);
          if (movingEdge && !reduced) {
            var p = E[movingEdge].path, L = p.getTotalLength(), t0 = null;
            var tick = function (ts) { if (!t0) t0 = ts; var f = Math.min(1, (ts - t0) / 900); var pt = p.getPointAtLength(f * L); dot.setAttribute("cx", pt.x); dot.setAttribute("cy", pt.y); if (f < 1) raf = requestAnimationFrame(tick); };
            raf = requestAnimationFrame(tick);
          } else if (movingEdge) { var q = E[movingEdge].path, pt = q.getPointAtLength(q.getTotalLength()); dot.setAttribute("cx", pt.x); dot.setAttribute("cy", pt.y); }
          else { dot.setAttribute("cx", -20); dot.setAttribute("cy", -20); }
        }
      });
      api.stepper = st;
      s.addEventListener("click", function (e) {
        var g = e.target.closest(".sb-flow-node"); if (!g) return;
        var id = g.getAttribute("data-id");
        for (var k = 0; k < spec.steps.length; k++) if ((spec.steps[k].on || []).indexOf(id) >= 0) { st.stop(); st.go(k + 1); return; }
      });
      s.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { var g = e.target.closest(".sb-flow-node"); if (g) { g.dispatchEvent(new MouseEvent("click", { bubbles: true })); e.preventDefault(); } } });
    }
    return api;
  }

  /* ---------- dag: layered graph for course maps, glossary maps and method lineage ---------- */
  /* spec: {nodes:[{id,label,sub,col,row,state:"done|current",tag}], edges:[[from,to,label?]], cols:[labels], nodeW, nodeH, onSelect(id), selected} */
  function dag(host, spec) {
    host.classList.add("sb-dag");
    var longest = 0; spec.nodes.forEach(function (n) { longest = Math.max(longest, String(n.label).length); });
    var W = spec.nodeW || Math.max(132, Math.min(230, Math.round(longest * 7.6 + 34))), Hh = spec.nodeH || 44, gx = spec.gapX || 44, gy = spec.gapY || 14, top = spec.cols ? 30 : 8, pad = 8;
    var ncol = 0, nrow = 0; spec.nodes.forEach(function (n) { ncol = Math.max(ncol, n.col + 1); nrow = Math.max(nrow, n.row + 1); });
    var w = pad * 2 + ncol * W + (ncol - 1) * gx, h = top + pad + nrow * Hh + (nrow - 1) * gy + pad;
    var wrap = html("div", { "class": "sb-scroll-x" }, null, host);
    var s = svg("svg", { viewBox: "0 0 " + w + " " + h, width: w, height: h, role: "group", "aria-label": spec.title || "Dependency graph" }, wrap);
    s.style.maxWidth = "none";
    var arrow = ensureArrow(s, nextId("dagarr"));
    var N = {}, out = {}, inn = {};
    spec.nodes.forEach(function (n) { n.x = pad + n.col * (W + gx); n.y = top + n.row * (Hh + gy); N[n.id] = n; out[n.id] = []; inn[n.id] = []; });
    if (spec.cols) spec.cols.forEach(function (c, k) { var t = svg("text", { x: pad + k * (W + gx), y: 16, "class": "sb-dag-col" }, s); t.textContent = c; });
    var gE = svg("g", null, s), gN = svg("g", null, s), EL = [];
    spec.edges.forEach(function (e) {
      var a = N[e[0]], b = N[e[1]]; if (!a || !b) return;
      out[a.id].push(b.id); inn[b.id].push(a.id);
      var d;
      if (a.col === b.col) { var x = a.x + W / 2; d = b.row > a.row ? "M" + x + " " + (a.y + Hh) + " L" + x + " " + (b.y - 1) : "M" + x + " " + a.y + " L" + x + " " + (b.y + Hh + 1); }
      else { var x0 = a.x + W, y0 = a.y + Hh / 2, x1 = b.x - 1, y1 = b.y + Hh / 2, mx = (x0 + x1) / 2; d = "M" + x0 + " " + y0 + " C" + mx + " " + y0 + " " + mx + " " + y1 + " " + x1 + " " + y1; }
      var p = svg("path", { d: d, "class": "sb-dag-edge", "marker-end": arrow }, gE);
      p._a = a.id; p._b = b.id; EL.push(p);
    });
    spec.nodes.forEach(function (n) {
      var g = svg("g", { "class": "sb-dag-node" + (n.state ? " is-" + n.state : ""), tabindex: "0", role: "button", "aria-label": n.label + (n.sub ? " (" + n.sub + ")" : "") + (n.state === "done" ? ", understood" : ""), "data-id": n.id }, gN);
      svg("rect", { x: n.x, y: n.y, width: W, height: Hh, rx: 6 }, g);
      var t = svg("text", { x: n.x + 10, y: n.y + (n.sub ? 18 : 27), "class": "sb-dag-label" }, g); t.textContent = n.label;
      if (n.sub) { var st = svg("text", { x: n.x + 10, y: n.y + 34, "class": "sb-dag-sub" }, g); st.textContent = n.sub; }
      if (n.state === "done") { svg("circle", { cx: n.x + W - 12, cy: n.y + Hh - 12, r: 5, "class": "sb-dag-done" }, g); }
      n.g = g;
    });
    function walk(id, map, acc) { map[id].forEach(function (k) { if (!acc[k]) { acc[k] = 1; walk(k, map, acc); } }); return acc; }
    var selected = null;
    function focusOn(id) {
      host.classList.toggle("has-focus", !!id);
      var anc = id ? walk(id, inn, {}) : {}, des = id ? walk(id, out, {}) : {};
      spec.nodes.forEach(function (n) {
        n.g.classList.toggle("is-sel", n.id === id);
        n.g.classList.toggle("is-anc", !!anc[n.id]);
        n.g.classList.toggle("is-desc", !!des[n.id]);
      });
      EL.forEach(function (p) {
        var onPath = id && ((p._b === id || anc[p._b]) && (anc[p._a] || p._a === id) || (p._a === id || des[p._a]) && (des[p._b]));
        p.classList.toggle("is-on", !!onPath);
      });
    }
    gN.addEventListener("pointerover", function (e) { if (e.pointerType === "touch") return; var g = e.target.closest(".sb-dag-node"); if (g) focusOn(g.getAttribute("data-id")); });
    gN.addEventListener("pointerout", function (e) { if (e.pointerType === "touch") return; focusOn(selected); });
    gN.addEventListener("focusout", function (e) { if (!gN.contains(e.relatedTarget)) focusOn(selected); });
    gN.addEventListener("focusin", function (e) { var g = e.target.closest(".sb-dag-node"); if (g) focusOn(g.getAttribute("data-id")); });
    function select(id) { selected = id || null; focusOn(selected); spec.nodes.forEach(function (m) { m.g.setAttribute("aria-pressed", m.id === selected ? "true" : "false"); }); if (spec.onSelect && selected) spec.onSelect(selected, N[selected]); }
    gN.addEventListener("click", function (e) { var g = e.target.closest(".sb-dag-node"); if (g) select(g.getAttribute("data-id")); });
    gN.addEventListener("keydown", function (e) {
      var g = e.target.closest(".sb-dag-node"); if (!g) return; var n = N[g.getAttribute("data-id")];
      if (e.key === "Enter" || e.key === " ") { select(n.id); e.preventDefault(); return; }
      if (e.key === "Escape") { select(null); e.preventDefault(); return; }
      var dc = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0, dr = e.key === "ArrowDown" ? 1 : e.key === "ArrowUp" ? -1 : 0;
      if (!dc && !dr) return; e.preventDefault();
      var best = null, bd = 1e9;
      spec.nodes.forEach(function (m) {
        if (m === n) return;
        if (dc && Math.sign(m.col - n.col) !== dc) return; if (dr && (m.col !== n.col || Math.sign(m.row - n.row) !== dr)) return;
        var d = Math.abs(m.col - n.col) * 10 + Math.abs(m.row - n.row); if (d < bd) { bd = d; best = m; }
      });
      if (best) best.g.focus();
    });
    s.addEventListener("click", function (e) { if (!e.target.closest(".sb-dag-node")) select(null); });
    if (spec.selected) select(spec.selected);
    return { select: select, ancestors: function (id) { return Object.keys(walk(id, inn, {})); }, nodes: N };
  }

  /* ---------- lineChart: learning curves, races, errors over episodes ---------- */
  /* spec: {x:{label,min,max,ticks}, y:{label,min,max,ticks,fmt}, series:[{name,color:"data-1",points:[[x,y]],dash}], height, directLabels} */
  function niceTicks(min, max, n) {
    var span = max - min, step = Math.pow(10, Math.floor(Math.log10(span / n))), err = span / n / step;
    if (err >= 7.5) step *= 10; else if (err >= 3.5) step *= 5; else if (err >= 1.5) step *= 2;
    var out = []; for (var v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(+v.toFixed(10));
    return out;
  }
  function lineChart(host, spec) {
    host.classList.add("sb-chart");
    var H = spec.height || 240, M = { t: 12, r: spec.directLabels === false ? 12 : 96, b: 38, l: 48 };
    var xs = spec.x, ys = spec.y, fmt = ys.fmt || function (v) { return (+v).toFixed(2); };
    var fig = html("figure", { "class": "sb-fig" }, null, host);
    var box = html("div", { "class": "sb-chart-box", tabindex: "0", "aria-label": (spec.title || "Line chart") + ". Use arrow keys to read values." }, null, fig);
    var tip = html("div", { "class": "sb-tip", role: "status" }, null, box); tip.hidden = true;
    var vis = spec.series.map(function () { return true; });
    if (spec.series.length > 1) {
      var lg = html("ul", { "class": "sb-legend", "aria-label": "Show or hide series" }, null, fig);
      spec.series.forEach(function (sr, j) {
        var li = html("li", null, null, lg), b = html("button", { "class": "sb-key sb-key-btn", type: "button", "aria-pressed": "true" }, null, li);
        var sw = html("span", { "class": "sb-sw " + (sr.dash ? "sb-sw--dash" : "sb-sw--line") }, null, b); sw.style.setProperty("--c", "var(--" + sr.color + ")");
        b.appendChild(document.createTextNode(sr.name));
        b.addEventListener("click", function () {
          if (vis[j] && vis.filter(Boolean).length === 1) return; /* keep at least one series */
          vis[j] = !vis[j]; b.setAttribute("aria-pressed", vis[j] ? "true" : "false"); draw();
        });
      });
    }
    if (spec.caption) html("figcaption", { "class": "sb-caption" }, spec.caption, fig);
    var det = html("details", { "class": "sb-datatable" }, null, fig);
    html("summary", null, "Show data table", det);
    var tb = html("table", { "class": "sb-table sb-table--compact" }, null, html("div", { "class": "sb-scroll-x" }, null, det));
    var head = "<thead><tr><th scope=\"col\">" + (xs.label || "x") + "</th>" + spec.series.map(function (s) { return "<th scope=\"col\">" + s.name + "</th>"; }).join("") + "</tr></thead><tbody>";
    var X = spec.series[0].points.map(function (p) { return p[0]; });
    tb.innerHTML = head + X.map(function (x, k) { return "<tr><td>" + x + "</td>" + spec.series.map(function (s) { return "<td>" + (s.points[k] ? fmt(s.points[k][1]) : "–") + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody>";
    var s = null, idx = -1, sx, sy, W;
    function draw() {
      W = Math.max(280, box.clientWidth || 600);
      if (s) s.remove();
      s = svg("svg", { viewBox: "0 0 " + W + " " + H, width: "100%", height: H, role: "img", "aria-label": spec.title || "Line chart" });
      box.insertBefore(s, tip);
      var iw = W - M.l - M.r, ih = H - M.t - M.b;
      sx = function (v) { return M.l + (v - xs.min) / (xs.max - xs.min) * iw; };
      sy = function (v) { return M.t + ih - (v - ys.min) / (ys.max - ys.min) * ih; };
      var g = svg("g", null, s);
      (ys.ticks || niceTicks(ys.min, ys.max, 4)).forEach(function (v) {
        svg("line", { x1: M.l, x2: M.l + iw, y1: sy(v), y2: sy(v), "class": "sb-grid-line" }, g);
        var t = svg("text", { x: M.l - 8, y: sy(v) + 4, "text-anchor": "end", "class": "sb-tick" }, g); t.textContent = fmt(v).replace(/\.0+$/, "");
      });
      (xs.ticks || niceTicks(xs.min, xs.max, Math.max(3, Math.floor(iw / 90)))).forEach(function (v) {
        var t = svg("text", { x: sx(v), y: M.t + ih + 18, "text-anchor": "middle", "class": "sb-tick" }, g); t.textContent = v >= 1000 ? (v / 1000) + "k" : v;
      });
      svg("line", { x1: M.l, x2: M.l + iw, y1: M.t + ih, y2: M.t + ih, "class": "sb-axis-line" }, g);
      var xl = svg("text", { x: M.l + iw / 2, y: H - 4, "text-anchor": "middle", "class": "sb-axis-label" }, g); xl.textContent = xs.label || "";
      var yl = svg("text", { x: 12, y: M.t + ih / 2, "text-anchor": "middle", transform: "rotate(-90 12 " + (M.t + ih / 2) + ")", "class": "sb-axis-label" }, g); yl.textContent = ys.label || "";
      var labels = [];
      spec.series.forEach(function (sr, j) {
        if (!vis[j]) return;
        var d = sr.points.map(function (p, k) { return (k ? "L" : "M") + sx(p[0]).toFixed(1) + " " + sy(p[1]).toFixed(1); }).join(" ");
        var pth = svg("path", { d: d, "class": "sb-series" }, g); pth.style.stroke = "var(--" + sr.color + ")";
        if (sr.dash) pth.setAttribute("stroke-dasharray", "6 5");
        var last = sr.points[sr.points.length - 1];
        var end = svg("circle", { cx: sx(last[0]), cy: sy(last[1]), r: 4, "class": "sb-endpoint" }, g); end.style.fill = "var(--" + sr.color + ")";
        labels.push({ y: sy(last[1]), name: sr.name, color: sr.color });
      });
      if (spec.directLabels !== false && spec.series.length <= 4) {
        labels.sort(function (a, b) { return a.y - b.y; });
        for (var k = 1; k < labels.length; k++) if (labels[k].y - labels[k - 1].y < 14) labels[k].y = labels[k - 1].y + 14;
        labels.forEach(function (l) { var t = svg("text", { x: M.l + iw + 10, y: l.y + 4, "class": "sb-direct" }, g); t.textContent = l.name; });
      }
      var cross = svg("line", { y1: M.t, y2: M.t + ih, "class": "sb-crosshair" }, g); cross.style.display = "none";
      var dots = spec.series.map(function (sr) { var c = svg("circle", { r: 5, "class": "sb-hover-dot" }, g); c.style.fill = "var(--" + sr.color + ")"; c.style.display = "none"; return c; });
      var hit = svg("rect", { x: M.l, y: M.t, width: iw, height: ih, fill: "transparent" }, g); hit.style.touchAction = "pan-y";
      function show(k) {
        if (k < 0) { cross.style.display = "none"; dots.forEach(function (d) { d.style.display = "none"; }); tip.hidden = true; return; }
        idx = k; var x = X[k];
        cross.setAttribute("x1", sx(x)); cross.setAttribute("x2", sx(x)); cross.style.display = "";
        var rows = spec.series.map(function (sr, j) { var p = sr.points[k]; if (!vis[j]) return null; if (p) { dots[j].setAttribute("cx", sx(p[0])); dots[j].setAttribute("cy", sy(p[1])); dots[j].style.display = ""; } return { n: sr.name, c: sr.color, v: p ? p[1] : null }; });
        rows = rows.filter(Boolean); rows.sort(function (a, b) { return (b.v || 0) - (a.v || 0); });
        tip.innerHTML = "<b>" + (xs.label || "x") + " " + x + "</b>" + rows.map(function (r) { return '<span class="sb-tip-row"><i style="background:var(--' + r.c + ')"></i>' + r.n + "<em>" + (r.v == null ? "–" : fmt(r.v)) + "</em></span>"; }).join("");
        tip.hidden = false;
        var px = sx(x) / W * box.clientWidth;
        tip.style.left = Math.min(box.clientWidth - tip.offsetWidth - 4, Math.max(4, px + 12)) + "px";
        tip.style.top = "8px";
      }
      hit.addEventListener("pointermove", function (e) {
        var r = s.getBoundingClientRect(), vx = (e.clientX - r.left) / r.width * W, best = 0;
        X.forEach(function (x, k) { if (Math.abs(sx(x) - vx) < Math.abs(sx(X[best]) - vx)) best = k; });
        show(best);
      });
      hit.addEventListener("pointerleave", function () { show(-1); });
      box.onkeydown = function (e) { if (e.key === "ArrowRight") { show(Math.min(X.length - 1, idx + 1)); e.preventDefault(); } if (e.key === "ArrowLeft") { show(Math.max(0, idx - 1)); e.preventDefault(); } if (e.key === "Escape") show(-1); };
      box.onblur = function () { show(-1); };
    }
    draw();
    if (window.ResizeObserver) new ResizeObserver(function () { if (Math.abs((box.clientWidth || 0) - W) > 8) draw(); }).observe(box);
    return { redraw: draw };
  }

  /* ---------- grid: gridworld values, policies and heatmaps ---------- */
  /* spec: {rows, cols, values:[[…]] (null = wall), scale:"seq"|"div", min, max, arrows:[[…]], marks:{"S":[r,c]}, cell, fmt, label} */
  function grid(host, spec) {
    host.classList.add("sb-grid");
    var C = spec.cell || 44, R = spec.rows, K = spec.cols, fmt = spec.fmt || function (v) { return v.toFixed(2); };
    var fig = html("figure", { "class": "sb-fig" }, null, host);
    var wrap = html("div", { "class": "sb-grid-box" }, null, fig);
    var s = svg("svg", { viewBox: "0 0 " + (K * C + 2) + " " + (R * C + 2), width: K * C + 2, height: R * C + 2, role: "img", "aria-label": spec.label || "Grid" }, wrap);
    var tip = html("div", { "class": "sb-tip" }, null, wrap); tip.hidden = true;
    var cells = [];
    for (var r = 0; r < R; r++) for (var c = 0; c < K; c++) {
      var v = spec.values[r][c], g = svg("g", { "class": "sb-cell", tabindex: v == null ? null : "0" }, s);
      var rect = svg("rect", { x: 1 + c * C, y: 1 + r * C, width: C - 2, height: C - 2, rx: 3 }, g);
      var t = svg("text", { x: 1 + c * C + C / 2, y: 1 + r * C + C / 2 + (spec.arrows ? 12 : 4), "text-anchor": "middle", "class": "sb-cell-v" }, g);
      var a = null;
      if (spec.arrows && spec.arrows[r][c]) { a = svg("text", { x: 1 + c * C + C / 2, y: 1 + r * C + C / 2 - 2, "text-anchor": "middle", "class": "sb-cell-arrow" }, g); a.textContent = spec.arrows[r][c]; }
      if (v == null) { g.classList.add("is-wall"); } else t.textContent = spec.showValues === false ? "" : fmt(v);
      Object.keys(spec.marks || {}).forEach(function (m) { var p = spec.marks[m]; if (p[0] === r && p[1] === c) { var mt = svg("text", { x: 1 + c * C + 5, y: 1 + r * C + 13, "class": "sb-cell-mark" }, g); mt.textContent = m; } });
      cells.push({ r: r, c: c, v: v, rect: rect, t: t, a: a, g: g });
      (function (cell) {
        function on() { if (cell.v == null) return; tip.hidden = false; tip.innerHTML = "<b>s = (" + cell.r + ", " + cell.c + ")</b><span class=\"sb-tip-row\">" + (spec.valueLabel || "V(s)") + "<em>" + fmt(cell.v) + "</em></span>" + (spec.arrows && spec.arrows[cell.r][cell.c] ? "<span class=\"sb-tip-row\">π(s)<em>" + spec.arrows[cell.r][cell.c] + "</em></span>" : ""); tip.style.left = Math.min(wrap.clientWidth - 150, (cell.c + 1) * C + 6) + "px"; tip.style.top = (cell.r * C) + "px"; cell.g.classList.add("is-hover"); }
        function off() { tip.hidden = true; cell.g.classList.remove("is-hover"); }
        cell.g.addEventListener("pointerenter", on); cell.g.addEventListener("pointerleave", off);
        cell.g.addEventListener("focus", on); cell.g.addEventListener("blur", off);
      })(cells[cells.length - 1]);
    }
    function paint() {
      var lo = spec.min, hi = spec.max;
      cells.forEach(function (cell) {
        if (cell.v == null) return;
        var t = (cell.v - lo) / (hi - lo), col = spec.scale === "div" ? div(t) : seq(t);
        cell.rect.style.fill = col;
        var ink = lum(col) > 0.28 ? "#11181b" : "#ffffff";
        cell.t.style.fill = ink; if (cell.a) cell.a.style.fill = ink;
      });
    }
    var off = onThemeChange(paint);
    if (spec.caption) html("figcaption", { "class": "sb-caption" }, spec.caption, fig);
    return { update: function (values, arrows) { cells.forEach(function (c) { c.v = values[c.r][c.c]; if (c.v != null) c.t.textContent = spec.showValues === false ? "" : fmt(c.v); if (arrows && c.a) c.a.textContent = arrows[c.r][c.c] || ""; }); if (arrows) spec.arrows = arrows; paint(); }, destroy: off };
  }

  /* ---------- table: sort, filter chips, search, count ---------- */
  function table(tbl) {
    var tbody = tbl.tBodies[0], rows = Array.prototype.slice.call(tbody.rows), id = tbl.id;
    var filters = {}, query = "";
    Array.prototype.forEach.call(tbl.querySelectorAll("th[data-sort]"), function (th, col) {
      var b = html("button", { "class": "sb-sort", type: "button" }); while (th.firstChild) b.appendChild(th.firstChild); th.appendChild(b);
      th.setAttribute("aria-sort", "none");
      b.addEventListener("click", function () {
        var idx = Array.prototype.indexOf.call(th.parentNode.children, th), dir = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        Array.prototype.forEach.call(tbl.querySelectorAll("th[data-sort]"), function (o) { o.setAttribute("aria-sort", "none"); });
        th.setAttribute("aria-sort", dir);
        var num = th.getAttribute("data-sort") === "num";
        rows.sort(function (a, b) {
          var x = a.cells[idx].getAttribute("data-v") || a.cells[idx].textContent, y = b.cells[idx].getAttribute("data-v") || b.cells[idx].textContent;
          var c = num ? (+x - +y) : x.localeCompare(y); return dir === "ascending" ? c : -c;
        });
        rows.forEach(function (r) { tbody.appendChild(r); }); if (empty) tbody.appendChild(empty);
      });
    });
    function apply() {
      var shown = 0;
      rows.forEach(function (r) {
        var ok = Object.keys(filters).every(function (k) { return !filters[k].length || filters[k].indexOf(r.getAttribute("data-" + k)) >= 0; });
        if (ok && query) ok = r.textContent.toLowerCase().indexOf(query) >= 0;
        r.hidden = !ok; if (ok) shown++;
      });
      var cnt = document.querySelector('[data-count-for="' + id + '"]'); if (cnt) cnt.textContent = shown + " of " + rows.length + " shown";
      var active = !!query || Object.keys(filters).some(function (k) { return filters[k].length; });
      var clr = document.querySelector('[data-clear-for="' + id + '"]'); if (clr) clr.hidden = !active;
      empty.hidden = shown > 0;
    }
    var empty = html("tr", { "class": "sb-table-empty" }, null, tbody);
    var ec = html("td", { colspan: String(tbl.tHead ? tbl.tHead.rows[0].cells.length : 1) }, null, empty);
    ec.innerHTML = 'Nothing matches these filters. <button type="button" class="sb-link-btn" data-clear-now>Clear filters</button>';
    function clearAll() {
      filters = {}; query = "";
      Array.prototype.forEach.call(document.querySelectorAll('[data-filter-for="' + id + '"] button[data-key]'), function (b) { b.setAttribute("aria-pressed", "false"); });
      var si2 = document.querySelector('[data-search-for="' + id + '"]'); if (si2) si2.value = "";
      apply();
    }
    empty.addEventListener("click", function (e) { if (e.target.closest("[data-clear-now]")) clearAll(); });
    var clrBtn = document.querySelector('[data-clear-for="' + id + '"]'); if (clrBtn) clrBtn.addEventListener("click", clearAll);
    var fb = document.querySelector('[data-filter-for="' + id + '"]');
    if (fb) fb.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-key]"); if (!b) return;
      var k = b.getAttribute("data-key"), v = b.getAttribute("data-val"), on = b.getAttribute("aria-pressed") !== "true";
      b.setAttribute("aria-pressed", on ? "true" : "false");
      filters[k] = filters[k] || []; if (on) filters[k].push(v); else filters[k] = filters[k].filter(function (x) { return x !== v; });
      apply();
    });
    var si = document.querySelector('[data-search-for="' + id + '"]');
    if (si) si.addEventListener("input", function () { query = si.value.trim().toLowerCase(); apply(); });
    apply();
    return { apply: apply, clear: clearAll };
  }

  /* ---------- terms: key-term notes. Hover previews; click or tap pins a card with the extra note ---------- */
  /* dict[key] = {name, sym, def, note, ref, href, viz} ; opts.onShow(key, entry) adds a "Show me" button */
  var termPop = null;
  function terms(scope, dict, opts) {
    scope = scope || document; opts = opts || {};
    var pop = html("div", { "class": "sb-pop", role: "tooltip", id: nextId("pop") }, null, document.body); pop.hidden = true;
    var cur = null, pinned = false, hideT = null, showT = null;
    function fill(key) {
      var d = dict[key]; if (!d) return false;
      pop.innerHTML = '<div class="sb-pop-head"><span class="sb-pop-name">' + d.name + "</span>" + (d.sym ? '<span class="sb-pop-sym">' + d.sym + "</span>" : "") + "</div>" +
        (d.viz ? '<div class="sb-pop-viz" aria-hidden="true">' + d.viz + "</div>" : "") +
        '<p class="sb-pop-def">' + d.def + "</p>" +
        (d.note ? '<p class="sb-pop-note"><b>Note.</b> ' + d.note + "</p>" : "") +
        '<div class="sb-pop-foot">' + (d.ref ? '<span class="sb-ref">' + d.ref + "</span>" : "") +
        '<span class="sb-pop-actions">' + (opts.onShow && d.showMe !== false ? '<button type="button" class="sb-btn sb-btn--ghost" data-pop="show">Show me ▶</button>' : "") +
        (d.href ? '<a class="sb-btn sb-btn--ghost" href="' + d.href + '" data-pop="open">Glossary ↗</a>' : "") + "</span></div>" +
        (pinned ? "" : '<span class="sb-pop-hint">Click the term to pin this note</span>');
      return true;
    }
    function place(el) {
      var r = el.getBoundingClientRect(), pw = pop.offsetWidth, ph = pop.offsetHeight;
      var x = Math.min(window.innerWidth - pw - 8, Math.max(8, r.left));
      var below = r.bottom + 8, y = below + ph > window.innerHeight && r.top - ph - 8 > 0 ? r.top - ph - 8 : below;
      pop.style.left = (x + window.scrollX) + "px"; pop.style.top = (y + window.scrollY) + "px";
    }
    function show(el, pin) {
      clearTimeout(hideT);
      var key = el.getAttribute("data-term"); pinned = !!pin;
      if (!fill(key)) return;
      if (cur && cur !== el) { cur.removeAttribute("aria-describedby"); cur.removeAttribute("aria-expanded"); }
      cur = el; el.setAttribute("aria-describedby", pop.id); if (pinned) el.setAttribute("aria-expanded", "true");
      pop.classList.toggle("is-pinned", pinned); pop.setAttribute("role", pinned ? "dialog" : "tooltip");
      if (pinned) pop.setAttribute("aria-label", dict[key].name); else pop.removeAttribute("aria-label");
      pop.hidden = false; place(el);
    }
    function hide(force) {
      if (pinned && !force) return;
      if (cur) { cur.removeAttribute("aria-describedby"); cur.removeAttribute("aria-expanded"); }
      cur = null; pinned = false; pop.hidden = true; pop.classList.remove("is-pinned");
    }
    function later() { clearTimeout(hideT); hideT = setTimeout(function () { hide(false); }, 220); }
    scope.addEventListener("pointerover", function (e) {
      if (e.pointerType === "touch" || pinned) return; var t = e.target.closest && e.target.closest(".sb-term-link");
      if (t) { clearTimeout(showT); showT = setTimeout(function () { if (!pinned) show(t, false); }, 120); }
    });
    scope.addEventListener("pointerout", function (e) { if (e.pointerType === "touch") return; var t = e.target.closest && e.target.closest(".sb-term-link"); if (t) { clearTimeout(showT); later(); } });
    pop.addEventListener("pointerenter", function () { clearTimeout(hideT); });
    pop.addEventListener("pointerleave", function () { later(); });
    document.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest(".sb-term-link");
      if (t && scope.contains(t)) { e.preventDefault(); clearTimeout(showT); if (cur === t && pinned) hide(true); else show(t, true); return; }
      var a = e.target.closest && e.target.closest("[data-pop]");
      if (a && pop.contains(a)) { var key = cur && cur.getAttribute("data-term"); if (a.getAttribute("data-pop") === "show" && opts.onShow && key) opts.onShow(key, dict[key]); hide(true); return; }
      if (!pop.contains(e.target)) hide(true);
    });
    scope.addEventListener("keydown", function (e) { var t = e.target.closest && e.target.closest(".sb-term-link"); if (t && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); if (cur === t && pinned) hide(true); else { show(t, true); var f = pop.querySelector("button, a"); if (f) f.focus(); } } });
    scope.addEventListener("focusin", function (e) { var t = e.target.closest && e.target.closest(".sb-term-link"); if (t && !pinned) show(t, false); });
    scope.addEventListener("focusout", function (e) { var t = e.target.closest && e.target.closest(".sb-term-link"); if (t && !pinned && !pop.contains(e.relatedTarget)) hide(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !pop.hidden) { var c = cur; hide(true); if (c) c.focus(); } });
    window.addEventListener("resize", function () { if (cur && !pop.hidden) place(cur); });
    termPop = { show: show, hide: hide };
    return termPop;
  }

  /* ---------- autolink: wrap the first use of every glossary term in each section, then attach notes ---------- */
  /* dict[key] = {name, alias:[...]} ; returns {linked, perTerm, missing} */
  var AUTOLINK_SKIP = "h1,h2,h3,h4,h5,h6,a,button,code,pre,kbd,samp,label,select,option,textarea,input,script,style,svg,math,mjx-container,.MathJax,.sb-term-link,.sb-eq-math,.sb-formula-math,.sb-anatomy,.sb-tok,.sb-ref,.sb-tag,.sb-prov,.sb-eyebrow,.sb-btn,.sb-seg,.sb-toc,.sb-appbar,.sb-pop,.sb-palette,.sb-vg-list,.sb-algo,[data-no-autolink],.sb-no-autolink";
  function autolink(scope, dict, opts) {
    scope = scope || document.body; opts = opts || {};
    var sectionSel = opts.section || "section, article, .sb-panel, .sb-orient-card, .sb-concept, .sb-callout, figure, li, td";
    var byName = {}, alts = [];
    Object.keys(dict).forEach(function (k) {
      var d = dict[k]; [d.name].concat(d.alias || []).forEach(function (n) {
        if (!n || n.length < 3) return; var low = n.toLowerCase(); if (byName[low]) return; byName[low] = k;
        alts.push(n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+"));
      });
    });
    alts.sort(function (a, b) { return b.length - a.length; });
    if (!alts.length) return { linked: 0, perTerm: {}, missing: [] };
    var re = new RegExp("(^|[^\\p{L}\\p{N}_-])(" + alts.join("|") + ")(?:s|es)?(?=$|[^\\p{L}\\p{N}_-])", "giu");
    var seen = new WeakMap(), per = {}, total = 0;
    var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, { acceptNode: function (n) { if (!n.nodeValue || n.nodeValue.trim().length < 3) return NodeFilter.FILTER_REJECT; var p = n.parentElement; return !p || p.closest(AUTOLINK_SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } });
    var nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var sec = node.parentElement.closest(sectionSel) || scope, used = seen.get(sec); if (!used) { used = {}; seen.set(sec, used); }
      if (opts.everywhere) used = {};
      var text = node.nodeValue, m, parts = [], last = 0; re.lastIndex = 0;
      while ((m = re.exec(text))) {
        var word = m[2], key = byName[word.toLowerCase().replace(/\s+/g, " ")]; var start = m.index + m[1].length, end = re.lastIndex;
        if (!key || used[key]) continue;
        used[key] = 1; parts.push([start, end, key]);
      }
      if (!parts.length) return;
      var frag = document.createDocumentFragment();
      parts.forEach(function (p) {
        frag.appendChild(document.createTextNode(text.slice(last, p[0])));
        var s = document.createElement("span"); s.className = "sb-term-link"; s.tabIndex = 0; s.setAttribute("role", "button"); s.setAttribute("data-term", p[2]); s.textContent = text.slice(p[0], p[1]);
        frag.appendChild(s); last = p[1]; per[p[2]] = (per[p[2]] || 0) + 1; total++;
      });
      frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
    if (!opts.noCards) terms(scope, dict, opts);
    var missing = Object.keys(dict).filter(function (k) { return !per[k]; });
    return { linked: total, perTerm: per, missing: missing };
  }

  /* ---------- demo: Watch (auto-run narration) and Guide me (your turn) for any interactive section ---------- */
  /* steps: [{target, title, text, do(api), wait, until(), timeout, task, expect(), done}] */
  function demo(steps, opts) {
    opts = opts || {};
    var i = -1, playing = false, mode = opts.mode || "watch", tok = 0, speed = 1, pollT = null;
    var ring = html("div", { "class": "sb-spot sb-spot--demo", "aria-hidden": "true" }, null, document.body); ring.hidden = true;
    var bar = html("div", { "class": "sb-demo", role: "region", "aria-label": (opts.title || "Demo") + " controls" }, null, document.body); bar.hidden = true;
    bar.innerHTML = '<div class="sb-demo-head"><span class="sb-eyebrow sb-eyebrow--live" data-d="kind"></span><span class="sb-demo-count" data-d="count"></span><button type="button" class="sb-btn sb-btn--ghost sb-btn--icon" data-d="exit" aria-label="Exit demo">✕</button></div>' +
      '<p class="sb-demo-title" data-d="title"></p><p class="sb-demo-text" data-d="text" aria-live="polite"></p>' +
      '<p class="sb-demo-task" data-d="task" hidden></p>' +
      '<div class="sb-demo-prog" aria-hidden="true"><i data-d="fill"></i></div>' +
      '<div class="sb-demo-ctl"><button type="button" class="sb-btn" data-d="prev" aria-label="Previous step">←</button><button type="button" class="sb-btn sb-btn--primary" data-d="play">Pause ❚❚</button><button type="button" class="sb-btn" data-d="next">Next →</button>' +
      '<div class="sb-seg sb-seg--sm" data-d="mode" role="group" aria-label="Demo mode"><button type="button" value="watch" aria-pressed="true">Watch</button><button type="button" value="guide" aria-pressed="false">Guide me</button></div>' +
      '<button type="button" class="sb-btn sb-btn--ghost" data-d="speed" aria-label="Speed">1×</button></div>';
    var q = function (k) { return bar.querySelector('[data-d="' + k + '"]'); };
    function resolve(t) { return typeof t === "function" ? t() : typeof t === "string" ? document.querySelector(t) : t; }
    function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
    var api = {
      click: function (sel) { var e = resolve(sel); if (e) e.click(); return sleep(120); },
      set: function (sel, v) { var e = resolve(sel); if (!e) return sleep(0); e.value = v; e.dispatchEvent(new Event("input", { bubbles: true })); e.dispatchEvent(new Event("change", { bubbles: true })); return sleep(120); },
      wait: function (ms) { return sleep(ms / speed); },
      until: function (fn, ms) { var t0 = Date.now(), my = tok; return new Promise(function (r) { (function poll() { if (my !== tok || fn() || Date.now() - t0 > (ms || 15000)) r(); else setTimeout(poll, 150); })(); }); },
      show: function (sel) { var e = resolve(sel); if (e) spot(e); },
      step: function () { return i; }
    };
    function spot(t) {
      if (!t) { ring.hidden = true; return; }
      var r = t.getBoundingClientRect();
      ring.style.left = (r.left + window.scrollX - 5) + "px"; ring.style.top = (r.top + window.scrollY - 5) + "px";
      ring.style.width = (r.width + 10) + "px"; ring.style.height = (r.height + 10) + "px"; ring.hidden = false;
    }
    function render() {
      var st = steps[i];
      q("kind").textContent = (opts.title || "Demo") + (mode === "guide" ? " · Guide me" : " · Watch");
      q("count").textContent = (i + 1) + " / " + steps.length;
      q("title").textContent = st.title || ""; q("text").textContent = st.text || "";
      var task = q("task"); task.hidden = !(mode === "guide" && st.expect); task.textContent = st.task ? "Your turn: " + st.task : "";
      task.classList.remove("is-done");
      q("fill").style.width = (100 * (i + 1) / steps.length) + "%";
      q("prev").disabled = i <= 0; q("next").textContent = i >= steps.length - 1 ? "Finish ✓" : "Next →"; q("next").classList.remove("is-ready"); q("next").classList.toggle("sb-btn--primary", mode === "guide" && !st.expect);
      q("play").hidden = mode === "guide"; q("play").textContent = playing ? "Pause ❚❚" : (i >= steps.length - 1 ? "Replay ↺" : "Play ▶");
      Array.prototype.forEach.call(q("mode").children, function (b) { b.setAttribute("aria-pressed", b.value === mode ? "true" : "false"); });
    }
    function autoDwell(st) { var w = String(st.text || "").split(/\s+/).length; return Math.max(1800, 900 + w * 280); }
    async function go(k) {
      if (k < 0 || k >= steps.length) return;
      var my = ++tok; clearTimeout(pollT); i = k; render();
      var st = steps[i], t = resolve(st.target);
      if (st.before) { try { await st.before(api); } catch (e) {} }
      if (t && t.scrollIntoView) { var r0 = t.getBoundingClientRect(); if (r0.top < 70 || r0.bottom > window.innerHeight - (bar.offsetHeight + 20)) { t.scrollIntoView({ block: "center", behavior: reduced ? "auto" : "smooth" }); await sleep(reduced ? 30 : 380); } }
      if (my !== tok) return; spot(t);
      if (mode === "watch") {
        if (st.do) { try { await st.do(api); } catch (e) {} }
        if (my !== tok) return; spot(resolve(st.target));
        if (st.until) await api.until(st.until, st.timeout);
        await sleep((st.wait != null ? st.wait : autoDwell(st)) / speed);
        if (my !== tok) return;
        if (playing) { if (i < steps.length - 1) go(i + 1); else { playing = false; render(); if (opts.onEnd) opts.onEnd(); } }
      } else if (st.expect) {
        (function poll() { if (my !== tok) return; var ok = false; try { ok = st.expect(api); } catch (e) {} if (ok) { var task = q("task"); task.classList.add("is-done"); task.textContent = "✓ " + (st.done || "Nice. That's it.") + (i < steps.length - 1 ? " Press Next → when you're ready." : " Press Finish ✓ when you're ready."); q("next").classList.add("sb-btn--primary", "is-ready"); } else pollT = setTimeout(poll, 250); })();
      }
    }
    function start(m) { if (m) mode = m; bar.hidden = false; document.body.classList.add("sb-demo-on"); playing = mode === "watch"; go(0); var p = mode === "watch" ? q("play") : q("next"); if (p) p.focus({ preventScroll: true }); }
    function stop() { tok++; clearTimeout(pollT); playing = false; bar.hidden = true; ring.hidden = true; document.body.classList.remove("sb-demo-on"); if (opts.onExit) opts.onExit(); }
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("[data-d]"), m = e.target.closest('[data-d="mode"] button'); if (!b && !m) return;
      if (m) { mode = m.value; playing = mode === "watch"; go(i < 0 ? 0 : i); return; }
      var d = b.getAttribute("data-d");
      if (d === "exit") stop();
      else if (d === "prev") { playing = false; go(i - 1); }
      else if (d === "next") { playing = false; if (i >= steps.length - 1) stop(); else go(i + 1); }
      else if (d === "play") { if (playing) { playing = false; tok++; render(); } else { playing = true; go(i >= steps.length - 1 ? 0 : i); } }
      else if (d === "speed") { speed = speed === 1 ? 2 : speed === 2 ? 0.5 : 1; b.textContent = (speed === 0.5 ? "½" : speed) + "×"; }
    });
    bar.addEventListener("keydown", function (e) { if (e.key === "Escape") stop(); if (e.key === "ArrowRight" && !e.target.closest("[data-d=mode]")) { playing = false; go(i + 1); } if (e.key === "ArrowLeft" && !e.target.closest("[data-d=mode]")) { playing = false; go(i - 1); } });
    /* taking over pauses Watch mode: any real pointer or key input outside the bar */
    function takeover(e) { if (bar.hidden || !playing || bar.contains(e.target) || !e.isTrusted) return; playing = false; tok++; render(); q("text").textContent = "Paused because you took over. Press Play ▶ to continue."; }
    document.addEventListener("pointerdown", takeover, true); document.addEventListener("keydown", function (e) { if (e.key !== "Tab") takeover(e); }, true);
    window.addEventListener("resize", function () { if (!bar.hidden && i >= 0) spot(resolve(steps[i].target)); });
    window.addEventListener("scroll", function () { if (!bar.hidden && i >= 0) spot(resolve(steps[i].target)); }, { passive: true });
    return { start: start, stop: stop, go: go, api: api, get step() { return i; }, get mode() { return mode; } };
  }

  /* ---------- visualGlossary: pick a term, see where it lives in a picture ---------- */
  /* spec: {terms:[{id,name,group,sym,def,note,ref,scene,focus:[part ids],label,related:[ids],topic:{href,label}}], scenes:{key:{title, svg}}, groups:[{id,name}], onShow(term), onSelect(term)} */
  function visualGlossary(host, spec) {
    host.classList.add("sb-vg");
    var T = {}; spec.terms.forEach(function (t) { T[t.id] = t; });
    var groups = spec.groups || [], gsel = "all", query = "", cur = null, playT = null;
    host.innerHTML = '<aside class="sb-vg-list" aria-label="Terms"><input class="sb-input" type="search" placeholder="Search ' + spec.terms.length + ' terms" aria-label="Search terms">' +
      '<div class="sb-chips sb-vg-groups" role="group" aria-label="Filter by group"><button type="button" class="sb-tag" aria-pressed="true" value="all">All</button>' + groups.map(function (g) { return '<button type="button" class="sb-tag" aria-pressed="false" value="' + g.id + '">' + g.name + "</button>"; }).join("") + "</div>" +
      '<span class="sb-status sb-vg-count" aria-live="polite"></span><ul class="sb-vg-items" role="listbox" aria-label="Glossary terms"></ul></aside>' +
      '<figure class="sb-vg-stage"><figcaption class="sb-vg-stage-head"><span class="sb-eyebrow" data-v="scene"></span><span class="sb-vg-look" data-v="look"></span></figcaption><div class="sb-vg-art" data-v="art"></div><span class="sb-vg-callout" data-v="callout" hidden></span></figure>' +
      '<article class="sb-vg-card" aria-live="polite"><p class="sb-eyebrow" data-v="group"></p><h3 class="sb-vg-name" data-v="name"></h3><p class="sb-vg-sym" data-v="sym"></p><p class="sb-vg-def" data-v="def"></p><p class="sb-vg-note" data-v="note"></p><div class="sb-chips" data-v="refs"></div><div data-v="rel" class="sb-vg-rel"></div><div class="sb-btn-row" data-v="acts"></div></article>';
    var list = host.querySelector(".sb-vg-items"), input = host.querySelector("input"), V = function (k) { return host.querySelector('[data-v="' + k + '"]'); };
    var sceneKey = null;
    function filtered() { return spec.terms.filter(function (t) { return (gsel === "all" || t.group === gsel) && (!query || (t.name + " " + (t.sym || "") + " " + (t.def || "")).toLowerCase().indexOf(query) >= 0); }); }
    function drawList() {
      var f = filtered();
      list.innerHTML = f.map(function (t) { var g = groups.filter(function (x) { return x.id === t.group; })[0]; return '<li role="none"><button type="button" role="option" class="sb-vg-item" data-id="' + t.id + '" aria-selected="' + (cur && cur.id === t.id) + '"><span class="sb-vg-item-n">' + t.name + '</span><span class="sb-vg-item-g">' + (g ? g.name : "") + "</span></button></li>"; }).join("") || '<li role="option" aria-disabled="true" class="sb-empty-inline">No terms match. Clear the search or pick All.</li>';
      host.querySelector(".sb-vg-count").textContent = f.length + " of " + spec.terms.length + " terms";
    }
    function select(id, fromUser) {
      var t = T[id]; if (!t) return; cur = t;
      var sc = spec.scenes[t.scene];
      if (sc && sceneKey !== t.scene) { V("art").innerHTML = sc.svg; sceneKey = t.scene; }
      V("scene").textContent = sc ? sc.title : "";
      var art = V("art"), parts = art.querySelectorAll("[data-part]"), focus = t.focus || [];
      art.classList.toggle("has-focus", focus.length > 0);
      Array.prototype.forEach.call(parts, function (p) { var on = focus.indexOf(p.getAttribute("data-part")) >= 0; p.classList.toggle("is-focus", on); });
      V("look").textContent = t.label ? "Look at: " + t.label : "";
      var first = art.querySelector('[data-part="' + focus[0] + '"]'), co = V("callout");
      if (first && t.label) {
        var fr = first.getBoundingClientRect(), hr = art.getBoundingClientRect(), ox = art.offsetLeft, oy = art.offsetTop;
        co.textContent = t.name; co.hidden = false;
        co.style.left = (ox + Math.max(4, Math.min(hr.width - co.offsetWidth - 4, fr.left - hr.left + fr.width / 2 - co.offsetWidth / 2))) + "px";
        co.style.top = (oy + Math.max(4, fr.top - hr.top - co.offsetHeight - 6)) + "px";
      } else co.hidden = true;
      var g = groups.filter(function (x) { return x.id === t.group; })[0];
      V("group").textContent = g ? g.name : ""; V("name").textContent = t.name; V("sym").innerHTML = t.sym || ""; V("sym").hidden = !t.sym;
      V("def").innerHTML = t.def || ""; V("note").innerHTML = t.note ? "<b>Note.</b> " + t.note : ""; V("note").hidden = !t.note;
      V("refs").innerHTML = (t.ref ? '<span class="sb-ref">' + t.ref + "</span>" : "") + (t.topic ? '<a class="sb-ref" href="' + t.topic.href + '">' + t.topic.label + " →</a>" : "");
      V("rel").innerHTML = t.related && t.related.length ? '<span class="sb-eyebrow">Related</span><div class="sb-chips">' + t.related.filter(function (r) { return T[r]; }).map(function (r) { return '<button type="button" class="sb-tag" data-rel="' + r + '">' + T[r].name + "</button>"; }).join("") + "</div>" : "";
      var fl = filtered(), pos = fl.indexOf(t);
      V("acts").innerHTML = (spec.onShow ? '<button type="button" class="sb-btn sb-btn--primary" data-act="show">Show in Lab ▶</button>' : "") +
        '<div class="sb-vg-walk" role="group" aria-label="Walk through the terms"><button type="button" class="sb-btn" data-act="back"' + (pos <= 0 ? " disabled" : "") + '>← Back</button><span class="sb-count" aria-live="polite">' + (pos >= 0 ? pos + 1 : "–") + " of " + fl.length + '</span><button type="button" class="sb-btn" data-act="next"' + (pos < 0 || pos >= fl.length - 1 ? " disabled" : "") + '>Next →</button></div>';
      Array.prototype.forEach.call(list.querySelectorAll(".sb-vg-item"), function (b) { var on = b.getAttribute("data-id") === id; b.setAttribute("aria-selected", on ? "true" : "false"); if (on && fromUser !== false) b.scrollIntoView({ block: "nearest" }); });
      if (spec.onSelect) spec.onSelect(t);
    }
    function stopPlay() { clearInterval(playT); playT = null; if (cur) select(cur.id, false); }
    list.addEventListener("click", function (e) { var b = e.target.closest(".sb-vg-item"); if (b) { stopPlay(); select(b.getAttribute("data-id")); } });
    list.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return; e.preventDefault();
      var bs = Array.prototype.slice.call(list.querySelectorAll(".sb-vg-item")), k = bs.indexOf(document.activeElement), n = bs[Math.max(0, Math.min(bs.length - 1, k + (e.key === "ArrowDown" ? 1 : -1)))];
      if (n) { n.focus(); select(n.getAttribute("data-id")); }
    });
    host.querySelector(".sb-vg-groups").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; gsel = b.value; Array.prototype.forEach.call(b.parentNode.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); drawList(); var f = filtered(); if (f.length) select(f[0].id, false); });
    input.addEventListener("input", function () { query = input.value.trim().toLowerCase(); drawList(); });
    host.addEventListener("click", function (e) {
      var r = e.target.closest("[data-rel]"); if (r) { select(r.getAttribute("data-rel")); return; }
      var a = e.target.closest("[data-act]"); if (!a) return;
      if (a.getAttribute("data-act") === "show" && spec.onShow && cur) spec.onShow(cur);
      if (a.getAttribute("data-act") === "back" || a.getAttribute("data-act") === "next" || a.getAttribute("data-act") === "tour") {
        var f = filtered(), k = f.indexOf(cur), d = a.getAttribute("data-act") === "back" ? -1 : 1;
        if (a.getAttribute("data-act") === "tour") k = -1, d = 1;
        var nk = Math.max(0, Math.min(f.length - 1, k + d)); if (f[nk]) { select(f[nk].id); var nb = host.querySelector('[data-act="' + (d < 0 ? "back" : "next") + '"]'); if (nb && !nb.disabled) nb.focus({ preventScroll: true }); }
      }
    });
    window.addEventListener("resize", function () { if (cur) select(cur.id, false); });
    drawList(); select(spec.start || spec.terms[0].id, false);
    return { select: select, stop: stopPlay };
  }

  /* ---------- flashcards ---------- */
  /* cards: [{front, back, ref}] ; key: storage key for "known" */
  function flashcards(host, cards, key) {
    host.classList.add("sb-flash");
    var order = cards.map(function (_, k) { return k; }), i = 0, known = store(key) || {};
    host.innerHTML = '<div class="sb-flash-card" tabindex="0" role="button" aria-live="polite"><div class="sb-flash-face"></div><span class="sb-flash-hint">Space or click to flip</span></div>' +
      '<div class="sb-btn-row"><button class="sb-btn" data-f="prev">← Previous</button><button class="sb-btn" data-f="flip">Flip</button><button class="sb-btn" data-f="next">Next →</button><button class="sb-btn sb-btn--ghost" data-f="shuffle">Shuffle</button><span class="sb-status"></span></div>' +
      '<div class="sb-btn-row sb-flash-grade" hidden><button class="sb-btn" data-f="again">Again</button><button class="sb-btn sb-btn--primary" data-f="knew">I knew it ✓</button></div>';
    var card = host.querySelector(".sb-flash-card"), face = host.querySelector(".sb-flash-face"), status = host.querySelector(".sb-status"), grade = host.querySelector(".sb-flash-grade"), back = false;
    function render() {
      var c = cards[order[i]];
      card.classList.toggle("is-back", back);
      face.innerHTML = back ? '<span class="sb-eyebrow">Answer</span><p>' + c.back + "</p>" + (c.ref ? '<span class="sb-ref">' + c.ref + "</span>" : "") : '<span class="sb-eyebrow">Card ' + (i + 1) + "</span><p class=\"sb-flash-q\">" + c.front + "</p>";
      grade.hidden = !back;
      var nk = Object.keys(known).filter(function (k) { return known[k]; }).length;
      status.textContent = (i + 1) + " / " + cards.length + " · " + nk + " known";
    }
    function flip() { back = !back; render(); }
    card.addEventListener("click", flip);
    card.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { flip(); e.preventDefault(); } if (e.key === "ArrowRight") { i = (i + 1) % cards.length; back = false; render(); } if (e.key === "ArrowLeft") { i = (i - 1 + cards.length) % cards.length; back = false; render(); } });
    host.addEventListener("click", function (e) {
      var b = e.target.closest("[data-f]"); if (!b) return; var f = b.getAttribute("data-f");
      if (f === "flip") flip();
      if (f === "next" || f === "knew" || f === "again") { if (f !== "next") { known[order[i]] = f === "knew"; store(key, known); } i = (i + 1) % cards.length; back = false; render(); }
      if (f === "prev") { i = (i - 1 + cards.length) % cards.length; back = false; render(); }
      if (f === "shuffle") { order.sort(function () { return Math.random() - 0.5; }); i = 0; back = false; render(); }
    });
    render();
  }

  /* ---------- decide: "which method should I use?" guide ---------- */
  /* tree: {q, why?, a:[{label, next}]} ; leaf: {result, ref, why, href} */
  function decide(host, tree) {
    host.classList.add("sb-decide");
    var path = [];
    function render() {
      var node = tree; path.forEach(function (k) { node = node.a[k].next; });
      var h = '<ol class="sb-decide-path">';
      var n2 = tree;
      path.forEach(function (k, j) { h += '<li><button class="sb-decide-step" data-back="' + j + '"><span class="sb-decide-q">' + n2.q + '</span><span class="sb-decide-a">' + n2.a[k].label + "</span></button></li>"; n2 = n2.a[k].next; });
      h += "</ol>";
      if (node.result) {
        h += '<div class="sb-decide-result"><span class="sb-eyebrow sb-eyebrow--live">Use</span><p class="sb-decide-title">' + node.result + "</p>" + (node.why ? '<p class="sb-caption">' + node.why + "</p>" : "") + '<div class="sb-btn-row">' + (node.ref ? '<span class="sb-ref">' + node.ref + "</span>" : "") + (node.href ? '<a class="sb-btn sb-btn--primary" href="' + node.href + '">Open topic →</a>' : "") + '<button class="sb-btn" data-restart>Start over</button></div></div>';
      } else {
        h += '<div class="sb-decide-now"><p class="sb-decide-title">' + node.q + "</p>" + (node.why ? '<p class="sb-caption">' + node.why + "</p>" : "") + '<div class="sb-btn-row">' + node.a.map(function (a, k) { return '<button class="sb-btn" data-pick="' + k + '">' + a.label + "</button>"; }).join("") + "</div></div>";
      }
      host.innerHTML = h;
      var f = host.querySelector("[data-pick],[data-restart]"); if (f && path.length) f.focus();
    }
    host.addEventListener("click", function (e) {
      var p = e.target.closest("[data-pick]"), b = e.target.closest("[data-back]"), r = e.target.closest("[data-restart]");
      if (p) { path.push(+p.getAttribute("data-pick")); render(); }
      if (b) { path = path.slice(0, +b.getAttribute("data-back")); render(); }
      if (r) { path = []; render(); }
    });
    render();
  }

  /* ---------- search: Ctrl/⌘-K palette over topics, methods, terms, symbols ---------- */
  /* index: [{kind, label, sub, href}] */
  function search(index, opts) {
    opts = opts || {};
    var dlg = html("div", { "class": "sb-palette", role: "dialog", "aria-modal": "true", "aria-label": "Search" }, null, opts.container || document.body); dlg.hidden = true;
    dlg.innerHTML = '<div class="sb-palette-box"><input class="sb-input sb-palette-input" type="search" placeholder="Search topics, methods, terms, symbols" aria-label="Search"><div class="sb-palette-results" role="listbox"></div><p class="sb-palette-foot"><kbd class="sb-kbd">↑</kbd><kbd class="sb-kbd">↓</kbd> to move · <kbd class="sb-kbd">Enter</kbd> to open · <kbd class="sb-kbd">Esc</kbd> to close</p></div>';
    var input = dlg.querySelector("input"), list = dlg.querySelector(".sb-palette-results"), sel = 0, hits = [], opener = null, lid = nextId("sr");
    list.id = lid; input.setAttribute("role", "combobox"); input.setAttribute("aria-controls", lid); input.setAttribute("aria-expanded", "true"); input.setAttribute("aria-autocomplete", "list");
    function score(it, q) { var s = (it.label + " " + (it.sub || "") + " " + (it.alias || "")).toLowerCase(); return q.split(/\s+/).every(function (w) { return s.indexOf(w) >= 0; }) ? (it.label.toLowerCase().indexOf(q) === 0 ? 2 : 1) : 0; }
    function render() {
      var q = input.value.trim().toLowerCase();
      hits = q ? index.map(function (it) { return { it: it, s: score(it, q) }; }).filter(function (x) { return x.s; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 12).map(function (x) { return x.it; }) : index.slice(0, 8);
      sel = Math.min(sel, Math.max(0, hits.length - 1));
      var kinds = {}; hits.forEach(function (h) { (kinds[h.kind] = kinds[h.kind] || []).push(h); });
      var k = 0, out = "";
      Object.keys(kinds).forEach(function (kind) {
        out += '<p class="sb-palette-kind">' + kind + "</p>";
        kinds[kind].forEach(function (h) { out += '<a class="sb-palette-item' + (k === sel ? " is-sel" : "") + '" id="' + lid + '-' + k + '" role="option" aria-selected="' + (k === sel) + '" href="' + (h.href || "#") + '" data-k="' + k + '"><span>' + h.label + "</span>" + (h.sub ? '<span class="sb-ref">' + h.sub + "</span>" : "") + "</a>"; k++; });
      });
      list.innerHTML = out || '<p class="sb-empty-inline">No matches. Try a symbol like α or a chapter like “Ch 6”.</p>';
      hits = [].concat.apply([], Object.keys(kinds).map(function (kd) { return kinds[kd]; }));
      if (hits.length) { input.setAttribute("aria-activedescendant", lid + "-" + sel); var cur = list.querySelector(".is-sel"); if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "nearest" }); } else input.removeAttribute("aria-activedescendant");
    }
    function open() { opener = document.activeElement; dlg.hidden = false; input.value = ""; sel = 0; render(); input.focus(); }
    function close() { dlg.hidden = true; if (opener && opener.focus) opener.focus(); }
    input.addEventListener("input", function () { sel = 0; render(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(); e.preventDefault(); }
      if (e.key === "ArrowDown") { sel = Math.min(hits.length - 1, sel + 1); render(); e.preventDefault(); }
      if (e.key === "ArrowUp") { sel = Math.max(0, sel - 1); render(); e.preventDefault(); }
      if (e.key === "Enter" && hits[sel]) { var a = list.querySelector('[data-k="' + sel + '"]'); if (a) a.click(); close(); }
    });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) close(); if (e.target.closest(".sb-palette-item")) close(); });
    document.addEventListener("keydown", function (e) { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); if (dlg.hidden) open(); else close(); } });
    document.addEventListener("click", function (e) { if (e.target.closest && e.target.closest("[data-open-search]")) open(); });
    return { open: open, close: close };
  }

  /* ---------- tour: coach marks with a spotlight ring ---------- */
  /* steps: [{target: selector|element, title, text}] */
  function tour(steps, opts) {
    opts = opts || {};
    var scope = opts.scope || document, i = 0;
    var ring = html("div", { "class": "sb-spot", "aria-hidden": "true" }, null, opts.container || document.body);
    var coach = html("div", { "class": "sb-coach", role: "dialog", "aria-label": opts.title || "Guided tour" }, null, opts.container || document.body);
    ring.hidden = coach.hidden = true;
    function place(scroll) {
      var st = steps[i], t = typeof st.target === "string" ? scope.querySelector(st.target) : st.target; if (!t) return;
      if (scroll !== false && t.scrollIntoView) { var r0 = t.getBoundingClientRect(); if (r0.top < 0 || r0.bottom > window.innerHeight) t.scrollIntoView({ block: "center", behavior: reduced ? "auto" : "smooth" }); }
      var host = opts.container || document.body, hr = host === document.body ? { left: -window.scrollX, top: -window.scrollY } : host.getBoundingClientRect();
      var r = t.getBoundingClientRect();
      ring.style.left = (r.left - hr.left - 4) + "px"; ring.style.top = (r.top - hr.top - 4) + "px"; ring.style.width = (r.width + 8) + "px"; ring.style.height = (r.height + 8) + "px";
      coach.innerHTML = '<span class="sb-eyebrow sb-eyebrow--live">' + (opts.title || "Tour") + " · " + (i + 1) + " / " + steps.length + '</span><p class="sb-coach-title">' + st.title + '</p><p class="sb-caption">' + st.text + '</p><div class="sb-btn-row"><button class="sb-btn" data-t="prev"' + (i ? "" : " disabled") + '>← Back</button>' + (i < steps.length - 1 ? '<button class="sb-btn sb-btn--primary" data-t="next">Next →</button>' : '<button class="sb-btn sb-btn--primary" data-t="end">Finish</button>') + '<button class="sb-btn sb-btn--ghost" data-t="end" aria-label="End tour">✕</button></div>';
      ring.hidden = coach.hidden = false;
      var below = r.bottom - hr.top + 12, maxL = (host === document.body ? window.innerWidth : hr.width) - coach.offsetWidth - 8;
      var roomBelow = window.innerHeight - r.bottom, above = r.top - hr.top - coach.offsetHeight - 12;
      coach.style.left = Math.max(8, Math.min(maxL, r.left - hr.left)) + "px";
      coach.style.top = (roomBelow < coach.offsetHeight + 16 && above > 0 ? above : below) + "px";
      var nb = coach.querySelector('[data-t="next"],[data-t="end"]'); if (nb) nb.focus({ preventScroll: true });
    }
    coach.addEventListener("click", function (e) { var b = e.target.closest("[data-t]"); if (!b) return; var a = b.getAttribute("data-t"); if (a === "next") { i++; place(); } else if (a === "prev") { i--; place(); } else end(); });
    coach.addEventListener("keydown", function (e) { if (e.key === "Escape") end(); });
    function end() { ring.hidden = coach.hidden = true; if (opts.onEnd) opts.onEnd(); }
    window.addEventListener("resize", function () { if (!coach.hidden) place(false); });
    return { start: function (k) { i = k || 0; place(); }, end: end };
  }

  /* ---------- progress: "understood" state shared by TOC checks, course map and meters ---------- */
  function progress(siteKey, ids) {
    var key = "sb-progress-" + siteKey, state = store(key) || {}, subs = [];
    function count() { return ids.filter(function (id) { return state[id]; }).length; }
    function sync() {
      Array.prototype.forEach.call(document.querySelectorAll("[data-understood]"), function (b) { var on = !!state[b.getAttribute("data-understood")]; b.setAttribute("aria-pressed", on ? "true" : "false"); b.textContent = on ? "Understood ✓" : "Mark as understood"; });
      Array.prototype.forEach.call(document.querySelectorAll("[data-check]"), function (c) { c.classList.toggle("is-done", !!state[c.getAttribute("data-check")]); });
      Array.prototype.forEach.call(document.querySelectorAll("[data-progress]"), function (m) {
        var n = count(); var bar = m.querySelector(".sb-meter-fill"), txt = m.querySelector(".sb-meter-text");
        if (bar) bar.style.width = (100 * n / ids.length) + "%"; if (txt) txt.textContent = n + " of " + ids.length + " understood";
        m.setAttribute("aria-valuenow", n); m.setAttribute("aria-valuemax", ids.length);
      });
      subs.forEach(function (f) { f(state); });
    }
    document.addEventListener("click", function (e) { var b = e.target.closest && e.target.closest("[data-understood]"); if (!b) return; var id = b.getAttribute("data-understood"); state[id] = !state[id]; store(key, state); sync(); });
    sync();
    return { get: function (id) { return !!state[id]; }, set: function (id, v) { state[id] = !!v; store(key, state); sync(); }, count: count, onChange: function (f) { subs.push(f); f(state); } };
  }


  /* ---------- quiz: .sb-q with button.sb-opt[data-correct]; .sb-q-why shows after answering ---------- */
  function quiz(root, opts) {
    opts = opts || {};
    var qs = root.querySelectorAll(".sb-q"), score = 0, answered = 0;
    Array.prototype.forEach.call(qs, function (q) {
      var why = q.querySelector(".sb-q-why"); if (why) { why.hidden = true; why.setAttribute("tabindex", "-1"); }
      q.addEventListener("click", function (e) {
        var b = e.target.closest(".sb-opt"); if (!b || q.getAttribute("data-done")) return;
        q.setAttribute("data-done", "1"); answered++;
        var right = b.getAttribute("data-correct") === "true"; if (right) score++;
        Array.prototype.forEach.call(q.querySelectorAll(".sb-opt"), function (o) {
          var c = o.getAttribute("data-correct") === "true", mark = o.querySelector(".sb-opt-mark");
          o.setAttribute("data-state", o === b ? (right ? "correct" : "wrong") : (c ? "answer" : "dim"));
          o.setAttribute("aria-disabled", "true");
          if (mark) mark.textContent = o === b ? (right ? "✓" : "✗") : (c ? "✓" : "");
        });
        if (why) { var lead = why.querySelector(".sb-q-verdict"); if (!lead) { lead = html("b", { "class": "sb-q-verdict" }); why.insertBefore(lead, why.firstChild); } lead.textContent = right ? "Correct. " : "Not quite. "; why.hidden = false; why.focus({ preventScroll: true }); }
        var out = root.querySelector("[data-quiz-score]"); if (out) out.textContent = score + " of " + answered + " correct";
        if (opts.onAnswer) opts.onAnswer(right, q);
      });
    });
    root.addEventListener("click", function (e) {
      if (!e.target.closest("[data-quiz-reset]")) return; score = 0; answered = 0;
      Array.prototype.forEach.call(qs, function (q) { q.removeAttribute("data-done"); var w = q.querySelector(".sb-q-why"); if (w) w.hidden = true;
        Array.prototype.forEach.call(q.querySelectorAll(".sb-opt"), function (o) { o.removeAttribute("data-state"); o.removeAttribute("aria-disabled"); var m = o.querySelector(".sb-opt-mark"); if (m) m.textContent = ""; }); });
      var out = root.querySelector("[data-quiz-score]"); if (out) out.textContent = "";
    });
  }

  /* ---------- drawer: modal side sheet with focus trap, Escape, scrim and focus return ---------- */
  function drawer(el, opts) {
    opts = opts || {};
    var scrim = opts.scrim || html("div", { "class": "sb-scrim" }, null, el.parentNode); scrim.hidden = true; el.hidden = true;
    el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true"); if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1");
    var opener = null;
    function focusables() { return Array.prototype.filter.call(el.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])'), function (x) { return x.offsetParent !== null; }); }
    function open(from) { opener = from || document.activeElement; el.hidden = scrim.hidden = false; document.documentElement.style.overflow = "hidden"; var f = el.querySelector("[autofocus]") || focusables()[0] || el; f.focus(); if (opts.onOpen) opts.onOpen(); }
    function close() { el.hidden = scrim.hidden = true; document.documentElement.style.overflow = ""; if (opener && opener.focus) opener.focus(); if (opts.onClose) opts.onClose(); }
    el.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(); e.preventDefault(); return; }
      if (e.key !== "Tab") return; var f = focusables(); if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { f[f.length - 1].focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { f[0].focus(); e.preventDefault(); }
    });
    scrim.addEventListener("click", close);
    el.addEventListener("click", function (e) { if (e.target.closest("[data-drawer-close]")) close(); });
    (opts.openers || []).forEach(function (b) { b.addEventListener("click", function () { open(b); }); b.setAttribute("aria-haspopup", "dialog"); });
    return { open: open, close: close };
  }

  /* ---------- audit: word limits from "Writing, notation and terminology" ---------- */
  var WORD_LIMITS = { ".sb-lede": 40, ".sb-orient-card p": 60, ".sb-outcomes li": 15, ".sb-concept-def": 20, ".sb-prose p": 80,
    ".sb-caption": 35, ".sb-step-text": 30, ".sb-flow-text": 30, ".sb-callout": 42, ".sb-takeaways li": 25, ".sb-q-text": 25, ".sb-opt": 12,
    ".sb-q-why": 40, ".sb-term-def": 35, ".sb-pop-def": 25, ".sb-coach .sb-caption": 35, ".sb-sbs-col": 12, ".sb-lineage-step": 12,
    ".sb-empty p": 30, ".sb-error": 32, ".sb-btn": 3, ".sb-seg > *": 2, ".sb-eyebrow:not(.sb-hero .sb-eyebrow)": 6, ".sb-hero .sb-eyebrow": 12 };
  /* Returns every element over its word limit (hidden step texts included) and logs a table. */
  function audit(scope) {
    scope = scope || document; var out = [];
    Object.keys(WORD_LIMITS).forEach(function (sel) {
      Array.prototype.forEach.call(scope.querySelectorAll(sel), function (e) {
        var words = e.textContent.replace(/[▶→←⏭↗✓✗✕❚·|\/]/g, " ").trim().split(/\s+/).filter(Boolean).length;
        if (words > WORD_LIMITS[sel]) out.push({ selector: sel, words: words, limit: WORD_LIMITS[sel], text: e.textContent.trim().slice(0, 80) });
      });
    });
    if (window.console && console.table) console.table(out);
    return out;
  }


  /* ---------- v2.4 shell helpers: one theme toggle, one demo hint, the same on every site ---------- */
  var THEME_KEY = "sb-theme", THEME_ORDER = ["system", "light", "dark"], THEME_LABEL = { system: "Theme: system", light: "Theme: light", dark: "Theme: dark" };
  function applyTheme(mode) {
    var root = document.documentElement;
    if (mode === "light" || mode === "dark") root.setAttribute("data-theme", mode); else root.removeAttribute("data-theme");
  }
  function themeToggle(btn, opts) {
    opts = opts || {};
    var key = opts.key || THEME_KEY, mode = "system";
    try { mode = localStorage.getItem(key) || "system"; } catch (e) {}
    if (THEME_ORDER.indexOf(mode) < 0) mode = "system";
    function sync() { btn.textContent = "◐"; btn.setAttribute("aria-label", THEME_LABEL[mode] + ". Change theme"); btn.title = THEME_LABEL[mode]; btn.setAttribute("data-mode", mode); }
    if (mode !== "system") applyTheme(mode); sync();
    btn.addEventListener("click", function () {
      mode = THEME_ORDER[(THEME_ORDER.indexOf(mode) + 1) % THEME_ORDER.length];
      try { localStorage.setItem(key, mode); } catch (e) {}
      applyTheme(mode); sync(); if (opts.onChange) opts.onChange(mode);
    });
    return { get: function () { return mode; }, set: function (m) { mode = m; applyTheme(m); sync(); } };
  }
  /* A "New here? Press Watch demo." hint placed as the last item of a .sb-demo-launch row; dismissal remembered per site */
  function demoHint(launch, siteKey) {
    if (!launch) return null;
    var k = "sb-demo-hint:" + (siteKey || location.pathname), seen = false;
    try { seen = localStorage.getItem(k) === "1"; } catch (e) {}
    var old = launch.querySelector(".sb-demo-hint"); if (old) old.remove();
    if (seen) return null;
    var h = html("span", { "class": "sb-demo-hint" }, null, launch);
    h.innerHTML = 'New here? Press Watch demo. <button type="button" class="sb-btn sb-btn--ghost">Got it</button>';
    function done() { try { localStorage.setItem(k, "1"); } catch (e) {} document.querySelectorAll(".sb-demo-hint").forEach(function (x) { x.hidden = true; }); }
    h.querySelector("button").addEventListener("click", done);
    var w = launch.querySelector("[data-demo-watch]"); if (w) w.addEventListener("click", done);
    return h;
  }


  /* ---------- v2.6 navigation: jumps you can undo, cards that go where they point, symbol parts that find their row ---------- */
  function flash(el) {
    if (!el) return; el.classList.remove("sb-arrive"); void el.offsetWidth; el.classList.add("sb-arrive");
    setTimeout(function () { el.classList.remove("sb-arrive"); }, 1800);
  }
  var NAV_SKIP = ".sb-return, .sb-demo, .sb-appbar-end, [data-demo-watch], [data-demo-guide], input, select, textarea, label, [data-d]";
  var NAV_ACT = 'a[href], button, [role="button"], [role="link"], [role="tab"], [role="option"], .sb-dag-node, [data-node], [data-cardlink], .sb-part[data-sym], .sb-anatomy [data-sym]';
  function returnNav(opts) {
    opts = opts || {};
    if (document.querySelector(".sb-return")) return null;
    var stack = [], returning = false, lastUserScroll = 0;
    var btn = html("div", { "class": "sb-return", role: "region", "aria-label": "Return" }, null, document.body); btn.hidden = true;
    btn.innerHTML = '<button type="button" class="sb-btn sb-return-go" data-r="go"></button><button type="button" class="sb-btn sb-btn--ghost sb-btn--icon" data-r="x" aria-label="Dismiss return">✕</button>';
    function curPage() { return document.querySelector("[data-page]:not([hidden])"); }
    function label() {
      var a = document.querySelector('nav.sb-views [aria-current="page"]'), page = a ? a.textContent.trim() : "";
      var root = curPage(), bits = [page];
      var st = root && root.querySelector(':scope > nav.sb-subtabs [aria-current="page"]'); if (st) bits.push(st.textContent.trim());
      var mid = window.innerHeight * 0.35, best = null;
      if (root) Array.prototype.forEach.call(root.querySelectorAll(".sb-topic-title, .sb-sec-title"), function (h) { if (!h.offsetParent) return; var r = h.getBoundingClientRect(); if (r.top < mid && (!best || r.top > best.getBoundingClientRect().top)) best = h; });
      if (best) { var t = best.textContent.replace(/\s+/g, " ").trim(); if (t && bits.indexOf(t) < 0) bits.push(t.length > 42 ? t.slice(0, 40) + "…" : t); }
      return bits.filter(Boolean).join(" · ");
    }
    function snap(anchor) { var root = curPage(), st = root && root.querySelector(':scope > nav.sb-subtabs [aria-current="page"]'); var a = anchor && anchor.getBoundingClientRect ? anchor : null; return { hash: location.hash, y: window.scrollY, sub: st ? st.textContent.trim() : null, label: label(), anchor: a, anchorTop: a ? a.getBoundingClientRect().top : 0 }; }
    function show() {
      var top = stack[stack.length - 1];
      if (!top) { btn.hidden = true; return; }
      btn.querySelector('[data-r="go"]').textContent = "← Return to " + top.label;
      btn.hidden = false;
    }
    ["wheel", "touchmove"].forEach(function (ev) { window.addEventListener(ev, function () { lastUserScroll = Date.now(); }, { passive: true }); });
    window.addEventListener("keydown", function (e) { if (/^(PageUp|PageDown|Home|End|ArrowUp|ArrowDown| )$/.test(e.key)) lastUserScroll = Date.now(); });
    document.addEventListener("click", function (e) {
      if (!e.isTrusted || returning) return;
      var t = e.target.closest && e.target.closest(NAV_ACT); if (!t || t.closest(NAV_SKIP)) return;
      var s0 = snap(t), t0 = Date.now();
      [250, 700, 1300].forEach(function (ms) {
        setTimeout(function () {
          if (s0.done || returning) return;
          var moved = location.hash !== s0.hash || Math.abs(window.scrollY - s0.y) > window.innerHeight * 0.6;
          if (!moved || lastUserScroll > t0) return;
          s0.done = true;
          var top = stack[stack.length - 1];
          if (!top || top.hash !== s0.hash || Math.abs(top.y - s0.y) > 40) { stack.push(s0); if (stack.length > 20) stack.shift(); }
          show();
        }, ms);
      });
    }, true);
    btn.addEventListener("click", function (e) {
      var b = e.target.closest("[data-r]"); if (!b) return;
      if (b.getAttribute("data-r") === "x") { stack = []; show(); return; }
      var s = stack.pop(); if (!s) return;
      returning = true;
      if (location.hash !== s.hash) location.hash = s.hash;
      function restore() {
        var root = curPage();
        if (s.sub && root) { var cur = root.querySelector(':scope > nav.sb-subtabs [aria-current="page"]'); if (!cur || cur.textContent.trim() !== s.sub) { var want = Array.prototype.find.call(root.querySelectorAll(":scope > nav.sb-subtabs > *"), function (x) { return x.textContent.trim() === s.sub; }); if (want) want.click(); } }
        var a = s.anchor, r = a && a.isConnected && a.getBoundingClientRect();
        var top = r && (r.width || r.height) ? window.scrollY + r.top - s.anchorTop : s.y;
        window.scrollTo({ top: top, behavior: "instant" });
      }
      setTimeout(restore, 120); setTimeout(restore, 450); setTimeout(function () { restore(); returning = false; show(); if (opts.onReturn) opts.onReturn(s); }, 900);
      show();
    });
    var mo = new MutationObserver(function () { btn.classList.toggle("is-under-demo", document.body.classList.contains("sb-demo-on")); });
    mo.observe(document.body, { attributes: true, attributeFilter: ["class"] });
    return { stack: function () { return stack.slice(); }, back: function () { btn.querySelector('[data-r="go"]').click(); } };
  }
  /* A card with one link inside goes where the link goes, wherever you click on it. termHref(name) gives a glossary link for concept cards that have none. */
  function cardLinks(root, opts) {
    root = root || document; opts = opts || {};
    function wire() {
      Array.prototype.forEach.call(root.querySelectorAll(".sb-sumcard, .sb-concept, .sb-way-card, [data-cardlink]"), function (c) {
        if (c.getAttribute("data-cardlink-on")) return;
        var a = c.querySelector("a[href]");
        if (!a && opts.termHref && c.classList.contains("sb-concept")) {
          var n = c.querySelector(".sb-concept-name"), href = n && opts.termHref(n.textContent.trim());
          if (href) { a = html("a", { "class": "sb-link sb-concept-go", href: href }, "In the glossary →", c); }
        }
        if (!a) return;
        c.setAttribute("data-cardlink-on", "1"); c.setAttribute("data-cardlink", "");
        c.addEventListener("click", function (e) { if (e.target.closest("a, button, input, select, textarea, [role=button], .sb-term-link")) return; if (window.getSelection && String(window.getSelection()).length) return; a.click(); });
      });
    }
    wire(); var mo = new MutationObserver(function () { clearTimeout(mo.t); mo.t = setTimeout(wire, 200); }); mo.observe(root === document ? document.body : root, { childList: true, subtree: true });
  }
  /* Clicking a part of a symbol anatomy strip scrolls to that symbol's row in the notation table and flashes it */
  function anatomyJump(root) {
    root = root || document;
    root.addEventListener("click", function (e) {
      var p = e.target.closest && e.target.closest(".sb-part[data-sym], .sb-anatomy [data-sym]"); if (!p) return;
      var page = p.closest("[data-page]") || document, sym = p.getAttribute("data-sym");
      var row = Array.prototype.find.call(page.querySelectorAll('tr[data-sym="' + sym + '"]'), function (r) { return r.offsetParent; });
      if (!row) return;
      row.scrollIntoView({ block: "center", behavior: reduced ? "auto" : "smooth" }); flash(row);
    });
    Array.prototype.forEach.call(root.querySelectorAll(".sb-part[data-sym], .sb-anatomy [data-sym]"), function (p) { p.style.cursor = "pointer"; if (!p.title) p.title = "Find it in the symbol table"; });
  }


  /* ---------- v2.7 faceted filters: chips that would give no results disappear; each chip shows its count ----------
     groups: [{ chips: [button...] (each with value or data-val; "all" = no filter), match: function (item, val) -> bool, selected: function () -> val }]
     items: array of elements (or data). Call after every filter change and after first render. */
  function facetCounts(items, groups) {
    items = Array.prototype.slice.call(items || []);
    groups.forEach(function (g, gi) {
      var others = items.filter(function (it) { return groups.every(function (h, hi) { if (hi === gi) return true; var v = h.selected(); return v == null || v === "all" || v === "" || h.match(it, v); }); });
      Array.prototype.forEach.call(g.chips, function (c) {
        var v = c.getAttribute("data-val") || c.value || c.getAttribute("value");
        if (v == null || v === "all" || v === "") { c.setAttribute("data-facet-count", others.length); c.removeAttribute("data-facet-empty"); return; }
        var n = others.filter(function (it) { return g.match(it, v); }).length;
        c.setAttribute("data-facet-count", n);
        if (n === 0 && String(g.selected()) !== String(v)) c.setAttribute("data-facet-empty", ""); else c.removeAttribute("data-facet-empty");
      });
    });
  }

  window.StudyBench = {
    token: token, palette: palette, onThemeChange: onThemeChange, segmented: segmented, seq: seq, div: div,
    link: link, stepper: stepper, flow: flow, dag: dag, lineChart: lineChart, grid: grid, table: table,
    terms: terms, flashcards: flashcards, decide: decide, search: search, tour: tour, progress: progress, quiz: quiz, drawer: drawer, autolink: autolink, demo: demo, visualGlossary: visualGlossary, audit: audit, themeToggle: themeToggle, demoHint: demoHint, returnNav: returnNav, facetCounts: facetCounts, cardLinks: cardLinks, anatomyJump: anatomyJump, flash: flash, WORD_LIMITS: WORD_LIMITS
  };
})();
