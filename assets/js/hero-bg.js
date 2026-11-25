/* Metalytics — animated hero background
   ------------------------------------------------------------------
   A transparent canvas layered over the hero's gradient. Nothing is
   painted opaque, so the artwork and gradient underneath still read.

   Four motifs, all drawn in the brand violet:
     1. automation  — nodes joined by edges, with data packets
                      travelling the edges and pulsing each node
     2. statistics  — a live scatter cloud whose least-squares fit
                      line is recomputed every frame as points drift
     3. SAS         — code fragments drifting slowly upward
     4. a faint bar-chart horizon along the bottom edge

   The right-hand side carries the detail; a mask fades the left so
   the headline always sits on clean background.

   No dependencies. Pauses when the hero scrolls out of view, honours
   prefers-reduced-motion, and does nothing at all if the browser has
   no canvas.
*/
(function () {
  'use strict';

  var SAS = [
    'proc means data=adsl;', 'data _null_;', '%macro tlf(ds=);',
    'by usubjid trtan;', 'ods output summary=s;', 'proc sql noprint;',
    'run;', 'quit;', 'libname meta "/data/meta";', 'if last.usubjid;',
    '%let n = &sqlobs;', 'proc freq data=adae;', 'merge adsl adae;',
    'keep usubjid trt01p aval;', 'output out=stats mean=;', '%mend tlf;',
    'proc transpose out=wide;', 'where saffl = "Y";', '%do i = 1 %to &n;',
    'proc report nowd;'
  ];

  function rand(a, b) { return a + Math.random() * (b - a); }

  function Hero(host) {
    this.host = host;
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'hero__bg';
    this.canvas.setAttribute('aria-hidden', 'true');
    host.insertBefore(this.canvas, host.firstChild);

    this.ctx = this.canvas.getContext('2d');
    this.t = 0;
    this.raf = 0;
    this.visible = true;
    this.w = 0;
    this.h = 0;

    this.resize();
    this.bind();
    this.start();
  }

  /* ---------- sizing ---------- */

  Hero.prototype.resize = function () {
    var r = this.host.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);

    this.w = Math.max(r.width, 1);
    this.h = Math.max(r.height, 1);
    this.canvas.width = Math.round(this.w * dpr);
    this.canvas.height = Math.round(this.h * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    this.cell = this.w < 700 ? 96 : 124;
    this.build();
  };

  /* ---------- scene ---------- */

  Hero.prototype.build = function () {
    var w = this.w, h = this.h, cell = this.cell, i, j;
    var small = w < 700;
    this.small = small;

    /* --- the chart panel is reserved first, so the mesh can avoid it --- */
    this.plot = {
      x: w * (small ? 0.46 : 0.585),
      y: h * (small ? 0.54 : 0.24),
      w: w * (small ? 0.46 : 0.265),
      h: h * (small ? 0.27 : 0.42)
    };
    var pad = 26;

    /* --- nodes on a jittered grid, thinner behind the headline --- */
    this.nodes = [];
    var cols = Math.ceil(w / cell) + 1;
    var rows = Math.ceil(h / cell) + 1;

    for (i = 0; i < cols; i++) {
      for (j = 0; j < rows; j++) {
        var nx = i * cell + rand(-cell * 0.26, cell * 0.26);
        var ny = j * cell + rand(-cell * 0.26, cell * 0.26);
        /* thin out the left third — the headline lives there */
        if (nx / w < 0.34 && Math.random() < 0.6) continue;
        /* keep the chart panel clear */
        if (nx > this.plot.x - pad && nx < this.plot.x + this.plot.w + pad &&
            ny > this.plot.y - pad && ny < this.plot.y + this.plot.h + pad) continue;
        this.nodes.push({
          x: nx, y: ny,
          r: rand(1.2, 2.4),
          pulse: 0,
          phase: rand(0, Math.PI * 2)
        });
      }
    }

    /* --- edges: each node reaches its two nearest neighbours --- */
    this.edges = [];
    var seen = {};
    var max = cell * 1.18;

    for (i = 0; i < this.nodes.length; i++) {
      var near = [];
      for (j = 0; j < this.nodes.length; j++) {
        if (i === j) continue;
        var dx = this.nodes[i].x - this.nodes[j].x;
        var dy = this.nodes[i].y - this.nodes[j].y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (d < max) near.push({ j: j, d: d });
      }
      near.sort(function (a, b) { return a.d - b.d; });
      for (var k = 0; k < Math.min(2, near.length); k++) {
        var a = Math.min(i, near[k].j), b = Math.max(i, near[k].j);
        var key = a + ':' + b;
        if (seen[key]) continue;
        seen[key] = 1;
        this.edges.push({ a: a, b: b, len: near[k].d });
      }
    }

    /* --- packets travelling the edges --- */
    this.packets = [];
    var count = this.edges.length ? Math.min(small ? 11 : 24, this.edges.length) : 0;
    for (i = 0; i < count; i++) this.packets.push(this.newPacket(true));

    /* --- scatter cloud inside the chart panel --- */
    this.points = [];
    var n = small ? 26 : 44;
    for (i = 0; i < n; i++) {
      var u = Math.random();
      this.points.push({
        u: u,
        v: Math.min(0.97, Math.max(0.03, u * 0.66 + rand(-0.19, 0.19) + 0.17)),
        du: rand(-0.018, 0.018),
        dv: rand(-0.018, 0.018),
        r: rand(1.3, 2.6),
        tw: rand(0, Math.PI * 2)
      });
    }

    /* --- drifting SAS fragments --- */
    this.tokens = [];
    var tn = small ? 5 : 9;
    for (i = 0; i < tn; i++) {
      this.tokens.push(this.newToken(rand(0, h)));
    }

    /* --- bar-chart horizon --- */
    this.bars = [];
    var bw = small ? 16 : 22;
    for (i = 0; i * bw < w + bw; i++) {
      this.bars.push({ seed: rand(0, Math.PI * 2), speed: rand(0.35, 0.85) });
    }
    this.barW = bw;
  };

  Hero.prototype.newPacket = function (seed) {
    var e = (Math.random() * this.edges.length) | 0;
    return {
      e: e,
      p: seed ? Math.random() : 0,
      speed: rand(0.10, 0.26),
      dir: Math.random() < 0.5 ? 1 : -1
    };
  };

  Hero.prototype.newToken = function (y) {
    var i = (Math.random() * SAS.length) | 0;
    if (i === this.lastToken) i = (i + 1) % SAS.length;
    this.lastToken = i;
    return {
      x: rand(this.w * 0.30, this.w * 0.98),
      y: y === undefined ? this.h + rand(10, 90) : y,
      text: SAS[i],
      speed: rand(7, 17),
      life: 0,
      span: rand(7, 13)
    };
  };

  /* ---------- drawing ---------- */

  Hero.prototype.draw = function (dt) {
    var ctx = this.ctx, w = this.w, h = this.h, i;
    var t = this.t;

    ctx.clearRect(0, 0, w, h);

    /* 1. drifting plot grid */
    var g = 46;
    var ox = (t * 5) % g, oy = (t * 3) % g;
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(255,255,255,0.028)';
    ctx.beginPath();
    for (i = -1; i * g < w + g; i++) {
      var gx = Math.round(i * g + ox) + 0.5;
      ctx.moveTo(gx, 0); ctx.lineTo(gx, h);
    }
    for (i = -1; i * g < h + g; i++) {
      var gy = Math.round(i * g + oy) + 0.5;
      ctx.moveTo(0, gy); ctx.lineTo(w, gy);
    }
    ctx.stroke();

    /* 2. bar-chart horizon */
    var bw = this.barW;
    for (i = 0; i < this.bars.length; i++) {
      var b = this.bars[i];
      var bh = (0.5 + 0.5 * Math.sin(t * b.speed + b.seed)) * h * 0.17 + 6;
      ctx.fillStyle = 'rgba(123,48,252,0.16)';
      ctx.fillRect(i * bw, h - bh, bw - 5, bh);
    }

    /* 3. edges */
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(146,105,255,0.17)';
    ctx.beginPath();
    for (i = 0; i < this.edges.length; i++) {
      var e = this.edges[i];
      var na = this.nodes[e.a], nb = this.nodes[e.b];
      ctx.moveTo(na.x, na.y); ctx.lineTo(nb.x, nb.y);
    }
    ctx.stroke();

    /* 4. the chart panel: axes, scatter cloud, least-squares fit */
    var pl = this.plot;

    /* axes */
    ctx.strokeStyle = 'rgba(255,255,255,0.075)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pl.x, pl.y - 10);
    ctx.lineTo(pl.x, pl.y + pl.h);
    ctx.lineTo(pl.x + pl.w + 10, pl.y + pl.h);
    ctx.stroke();

    /* tick marks */
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.beginPath();
    for (i = 1; i <= 4; i++) {
      var ty = pl.y + (pl.h / 5) * i;
      ctx.moveTo(pl.x - 4, ty); ctx.lineTo(pl.x, ty);
      var tx = pl.x + (pl.w / 5) * i;
      ctx.moveTo(tx, pl.y + pl.h); ctx.lineTo(tx, pl.y + pl.h + 4);
    }
    ctx.stroke();

    var su = 0, sv = 0, suv = 0, suu = 0, n = this.points.length;

    for (i = 0; i < n; i++) {
      var p = this.points[i];
      p.u += p.du * dt;
      p.v += p.dv * dt;
      if (p.u < 0.03 || p.u > 0.97) p.du *= -1;
      if (p.v < 0.03 || p.v > 0.97) p.dv *= -1;
      p.tw += dt * 1.6;

      su += p.u; sv += p.v; suv += p.u * p.v; suu += p.u * p.u;

      var px = pl.x + p.u * pl.w;
      var py = pl.y + (1 - p.v) * pl.h;
      var a = 0.40 + 0.20 * Math.sin(p.tw);

      ctx.fillStyle = 'rgba(176,139,255,0.14)';
      ctx.beginPath();
      ctx.arc(px, py, p.r + 3.2, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = 'rgba(233,225,255,' + a.toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(px, py, p.r, 0, Math.PI * 2);
      ctx.fill();
    }

    /* fit line, recomputed every frame and clipped to the panel */
    if (n > 1) {
      var den = n * suu - su * su;
      if (Math.abs(den) > 1e-6) {
        var m = (n * suv - su * sv) / den;
        var c = (sv - m * su) / n;
        ctx.save();
        ctx.beginPath();
        ctx.rect(pl.x, pl.y - 6, pl.w, pl.h + 6);
        ctx.clip();
        ctx.strokeStyle = 'rgba(159,113,255,0.62)';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(pl.x, pl.y + (1 - c) * pl.h);
        ctx.lineTo(pl.x + pl.w, pl.y + (1 - (m + c)) * pl.h);
        ctx.stroke();
        ctx.restore();
      }
    }

    /* 5. nodes */
    for (i = 0; i < this.nodes.length; i++) {
      var nd = this.nodes[i];
      if (nd.pulse > 0) nd.pulse = Math.max(0, nd.pulse - dt * 1.7);
      var base = 0.26 + 0.10 * Math.sin(t * 0.8 + nd.phase);
      var al = base + nd.pulse * 0.6;
      var rr = nd.r + nd.pulse * 2.4;
      ctx.fillStyle = 'rgba(199,175,255,' + al.toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(nd.x, nd.y, rr, 0, Math.PI * 2);
      ctx.fill();
    }

    /* 6. packets riding the edges */
    for (i = 0; i < this.packets.length; i++) {
      var k = this.packets[i];
      var ed = this.edges[k.e];
      if (!ed) { this.packets[i] = this.newPacket(); continue; }

      k.p += (k.speed * dt * 160) / Math.max(ed.len, 1);

      if (k.p >= 1) {
        var hit = k.dir > 0 ? this.nodes[ed.b] : this.nodes[ed.a];
        if (hit) hit.pulse = 1;
        this.packets[i] = this.newPacket();
        continue;
      }

      var A = k.dir > 0 ? this.nodes[ed.a] : this.nodes[ed.b];
      var B = k.dir > 0 ? this.nodes[ed.b] : this.nodes[ed.a];
      var x = A.x + (B.x - A.x) * k.p;
      var y = A.y + (B.y - A.y) * k.p;
      var fade = Math.sin(k.p * Math.PI);

      ctx.fillStyle = 'rgba(206,232,255,' + (0.85 * fade).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(x, y, 2.1, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = 'rgba(160,120,255,' + (0.18 * fade).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(x, y, 6.5, 0, Math.PI * 2);
      ctx.fill();
    }

    /* 7. SAS fragments drifting up */
    ctx.font = '12px ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace';
    ctx.textBaseline = 'middle';
    for (i = 0; i < this.tokens.length; i++) {
      var tk = this.tokens[i];
      tk.y -= tk.speed * dt;
      tk.life += dt;
      if (tk.y < -20 || tk.life > tk.span) {
        this.tokens[i] = this.newToken();
        continue;
      }
      var f = Math.sin((tk.life / tk.span) * Math.PI);
      ctx.fillStyle = 'rgba(190,168,255,' + (0.17 * f).toFixed(3) + ')';
      ctx.fillText(tk.text, tk.x, tk.y);
    }

    /* 8. erase whatever sits behind the copy.
          Wide: fade from the left, where the headline is.
          Narrow: the copy fills the width, so fade from the top and
          leave only a quiet band along the bottom edge. */
    var mask;
    if (this.small) {
      mask = ctx.createLinearGradient(0, 0, 0, h);
      mask.addColorStop(0, 'rgba(0,0,0,0.95)');
      mask.addColorStop(0.55, 'rgba(0,0,0,0.86)');
      mask.addColorStop(0.82, 'rgba(0,0,0,0.55)');
      mask.addColorStop(1, 'rgba(0,0,0,0.20)');
    } else {
      mask = ctx.createLinearGradient(0, 0, w, 0);
      mask.addColorStop(0, 'rgba(0,0,0,1)');
      mask.addColorStop(0.30, 'rgba(0,0,0,0.72)');
      mask.addColorStop(0.58, 'rgba(0,0,0,0)');
    }
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = mask;
    ctx.fillRect(0, 0, w, h);
    ctx.globalCompositeOperation = 'source-over';
  };

  /* ---------- loop ---------- */

  Hero.prototype.start = function () {
    var self = this;
    var last = 0;

    function frame(now) {
      self.raf = window.requestAnimationFrame(frame);
      if (!last) last = now;
      var dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      if (!self.visible) return;
      self.t += dt;
      self.draw(dt);
    }

    this.raf = window.requestAnimationFrame(frame);
  };

  Hero.prototype.still = function () {
    /* one static frame for reduced-motion users */
    this.t = 3.2;
    this.draw(0);
  };

  Hero.prototype.bind = function () {
    var self = this;
    var timer;

    window.addEventListener('resize', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        self.resize();
        if (!self.raf) self.still();
      }, 180);
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        self.visible = entries[0].isIntersecting;
      }, { threshold: 0 }).observe(this.host);
    }

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) self.visible = false;
      else self.visible = true;
    });
  };

  /* ---------- boot ---------- */

  function init() {
    var test = document.createElement('canvas');
    if (!test.getContext || !test.getContext('2d')) return;

    var mq = window.matchMedia
      ? window.matchMedia('(prefers-reduced-motion: reduce)')
      : null;

    var heroes = document.querySelectorAll('.hero');
    for (var i = 0; i < heroes.length; i++) {
      var h = new Hero(heroes[i]);
      if (mq && mq.matches) {
        window.cancelAnimationFrame(h.raf);
        h.raf = 0;
        h.still();
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
