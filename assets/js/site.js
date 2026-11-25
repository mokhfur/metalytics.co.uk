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

  /* ---- current year in the footer ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
