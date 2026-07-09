/* =========================================================================
   Cute yellow star cursor trail.
   Small stars sparkle out behind the cursor and fade. Tweak the knobs below.
   Skips entirely for visitors who prefer reduced motion.
   ========================================================================= */
(function () {
  // ---- knobs ----
  var MIN_INTERVAL = 45;   // ms between stars (higher = sparser trail)
  var STAR = '★';          // the character used for the star
  var STORAGE_KEY = 'ellie-star-cursor-v2';

  var lastTime = 0;
  var prefersReducedMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function getStoredPreference() {
    try { return window.localStorage && window.localStorage.getItem(STORAGE_KEY); }
    catch (e) { return null; }
  }
  function setStoredPreference(value) {
    try {
      if (window.localStorage) window.localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {}
  }
  var enabled = getStoredPreference() !== 'off' && !prefersReducedMotion;
  var toggleButton;

  function updateToggleLabel() {
    if (!toggleButton) return;
    toggleButton.textContent = enabled ? 'Stars off' : 'Stars on';
    toggleButton.setAttribute('aria-pressed', String(!enabled));
    toggleButton.setAttribute('aria-label', enabled ? 'Turn off star cursor' : 'Turn on star cursor');
  }

  function addToggle() {
    if (document.querySelector('.cursor-toggle')) return;
    var homeHeroInner = document.querySelector('.home-hero .hero-inner');
    toggleButton = document.createElement('button');
    toggleButton.type = 'button';
    toggleButton.className = homeHeroInner ? 'cursor-toggle home-photo-toggle' : 'cursor-toggle';
    toggleButton.addEventListener('click', function () {
      enabled = !enabled;
      setStoredPreference(enabled ? 'on' : 'off');
      document.querySelectorAll('.cursor-star').forEach(function (star) { star.remove(); });
      updateToggleLabel();
    });
    updateToggleLabel();
    (homeHeroInner || document.body).appendChild(toggleButton);
  }

  function spark(x, y) {
    var s = document.createElement('span');
    s.className = 'cursor-star';
    s.textContent = STAR;
    s.style.left = x + 'px';
    s.style.top = y + 'px';
    s.style.fontSize = (10 + Math.random() * 10) + 'px';        // 10–20px
    s.style.setProperty('--dx', ((Math.random() - 0.5) * 24) + 'px');
    s.style.setProperty('--rot', ((Math.random() - 0.5) * 90) + 'deg');
    document.body.appendChild(s);
    s.addEventListener('animationend', function () { s.remove(); });
  }

  window.addEventListener('pointermove', function (e) {
    if (!enabled) return;
    if (e.pointerType === 'touch') return;                       // skip touch drags
    if (e.timeStamp - lastTime < MIN_INTERVAL) return;
    lastTime = e.timeStamp;
    spark(e.clientX, e.clientY);                                 // fixed-position = viewport coords
  }, { passive: true });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addToggle);
  } else {
    addToggle();
  }
})();
