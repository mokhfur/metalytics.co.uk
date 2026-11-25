/* Metalytics — mobile nav + progressive form submission */
(function () {
  'use strict';

  /* ---- mobile navigation ---- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- forms: submit in place, fall back to a normal POST ---- */
  Array.prototype.forEach.call(document.querySelectorAll('form[data-ajax]'), function (form) {
    var msg = form.querySelector('.form-msg');
    var btn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
      if (!window.fetch || !form.checkValidity()) { return; }
      e.preventDefault();

      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      if (msg) { msg.className = 'form-msg'; msg.textContent = ''; }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (data) {
          if (data && data.ok) {
            form.reset();
            if (msg) { msg.className = 'form-msg is-ok'; msg.textContent = 'Thanks for submitting! We will be in touch shortly.'; }
          } else {
            throw new Error((data && data.error) || 'Something went wrong.');
          }
        })
        .catch(function (err) {
          if (msg) {
            msg.className = 'form-msg is-err';
            msg.textContent = err.message + ' You can also email us directly.';
          }
        })
        .then(function () {
          if (btn) { btn.disabled = false; btn.textContent = label; }
        });
    });
  });


  /* ---- feature carousel: one panel at a time ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-carousel]'), function (root) {
    var slides = [].slice.call(root.querySelectorAll('.carousel__slide'));
    var dots   = [].slice.call(root.querySelectorAll('.carousel__dot'));
    var prev   = root.querySelector('.carousel__arrow--prev');
    var next   = root.querySelector('.carousel__arrow--next');
    var count  = root.querySelector('.carousel__count');
    var title  = root.querySelector('.carousel__title');
    if (slides.length < 2) { return; }

    var titles = dots.map(function (d) { return d.getAttribute('aria-label') || ''; });
    var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var i = 0, timer = null, stopped = false;
    var DELAY = 6000;

    root.classList.add('is-ready');

    function show(n) {
      n = (n + slides.length) % slides.length;
      if (n === i) { return; }
      var from = slides[i];
      from.classList.remove('is-active');
      from.classList.add('is-leaving');
      window.setTimeout(function () { from.classList.remove('is-leaving'); }, 450);
      i = n;
      slides[i].classList.add('is-active');
      dots.forEach(function (d, k) { d.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
      if (count) { count.textContent = (i + 1) + ' / ' + slides.length; }
      if (title) { title.textContent = titles[i]; }
    }

    function start() {
      if (stopped || calm || timer) { return; }
      timer = window.setInterval(function () { show(i + 1); }, DELAY);
    }
    function pause() { window.clearInterval(timer); timer = null; }
    function stop() { stopped = true; pause(); }

    slides[0].classList.add('is-active');
    slides.forEach(function (s) { s.querySelector('img').loading = 'eager'; });

    if (prev) { prev.addEventListener('click', function () { stop(); show(i - 1); }); }
    if (next) { next.addEventListener('click', function () { stop(); show(i + 1); }); }
    dots.forEach(function (d, k) { d.addEventListener('click', function () { stop(); show(k); }); });

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft')  { stop(); show(i - 1); e.preventDefault(); }
      if (e.key === 'ArrowRight') { stop(); show(i + 1); e.preventDefault(); }
    });

    root.addEventListener('mouseenter', pause);
    root.addEventListener('mouseleave', start);
    root.addEventListener('focusin', pause);
    root.addEventListener('focusout', start);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { pause(); } else { start(); }
    });

    /* touch swipe */
    var x0 = null;
    root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) { stop(); show(dx < 0 ? i + 1 : i - 1); }
      x0 = null;
    }, { passive: true });

    /* only run while it is on screen */
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        entries[0].isIntersecting ? start() : pause();
      }, { threshold: 0.35 }).observe(root);
    } else {
      start();
    }
  });

  /* ---- current year in the footer ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
