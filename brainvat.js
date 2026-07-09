/* =========================================================================
   Brain-in-a-vat scroll buddy: a little doodle that hops as you scroll.
   ========================================================================= */
(function () {
  var el = document.getElementById("brainvat");
  if (!el) return;
  var body = el.querySelector(".biv-body");

  function hop() {
    // restart the animation even if it's mid-jump
    body.classList.remove("jump");
    el.classList.remove("jumping");
    void body.offsetWidth;                 // force reflow
    body.classList.add("jump");
    el.classList.add("jumping");
  }
  body.addEventListener("animationend", function () {
    body.classList.remove("jump");
    el.classList.remove("jumping");
  });

  var last = 0;
  var THROTTLE = 460;                       // ms — hop at most this often while scrolling
  window.addEventListener("scroll", function () {
    var now = (window.performance && performance.now) ? performance.now() : +new Date();
    if (now - last < THROTTLE) return;
    last = now;
    hop();
  }, { passive: true });
})();
