/* Before/after slider. The section stays hidden until a real pair exists. */
(function () {
  var root = document.querySelector("[data-compare]");
  if (!root) return;

  var before = root.querySelector(".compare-before");
  var range = root.querySelector(".compare-range");
  var handle = root.querySelector(".compare-handle");

  function set(value) {
    var next = Math.max(0, Math.min(100, Number(value)));
    if (!isFinite(next)) next = 50;
    before.style.width = next + "%";
    handle.style.left = next + "%";
    range.setAttribute("aria-valuenow", String(Math.round(next)));
  }

  range.addEventListener("input", function () {
    set(range.value);
  });

  root.addEventListener("pointerdown", function (event) {
    if (event.target === range) return;
    function move(ev) {
      var rect = root.getBoundingClientRect();
      if (!rect.width) return;
      var percent = ((ev.clientX - rect.left) / rect.width) * 100;
      range.value = String(Math.round(percent));
      set(percent);
    }
    move(event);
    function stop() {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", stop);
    }
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", stop);
  });

  set(range.value);
})();
