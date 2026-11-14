/* Accessible lightbox for the job gallery. No dependencies. */
(function () {
  var buttons = Array.prototype.slice.call(document.querySelectorAll(".shot"));
  var dialog = document.getElementById("lightbox");
  if (!buttons.length || !dialog) return;

  var img = dialog.querySelector("img");
  var caption = document.getElementById("lightbox-caption");
  var closeBtn = dialog.querySelector(".lightbox-close");
  var prevBtn = dialog.querySelector(".lightbox-prev");
  var nextBtn = dialog.querySelector(".lightbox-next");
  var index = 0;
  var lastFocus = null;

  function dataFor(button) {
    var thumb = button.querySelector("img");
    return {
      webp: button.getAttribute("data-full-webp") || "",
      jpg: button.getAttribute("data-full") || "",
      alt: thumb ? thumb.alt : "",
      width: button.getAttribute("data-width") || "",
      height: button.getAttribute("data-height") || ""
    };
  }

  function show(nextIndex) {
    index = (nextIndex + buttons.length) % buttons.length;
    var data = dataFor(buttons[index]);
    var failed = false;
    img.alt = data.alt;
    if (data.width) img.width = Number(data.width);
    if (data.height) img.height = Number(data.height);
    img.onerror = function () {
      if (!failed && data.jpg && img.getAttribute("src") !== data.jpg) {
        failed = true;
        img.src = data.jpg;
      }
    };
    img.src = data.webp || data.jpg;
    caption.textContent = data.alt;
    var single = buttons.length < 2;
    prevBtn.hidden = single;
    nextBtn.hidden = single;
  }

  function focusables() {
    return [closeBtn, prevBtn, nextBtn].filter(function (el) {
      return el && !el.hidden;
    });
  }

  function openAt(start) {
    lastFocus = document.activeElement;
    show(start);
    dialog.hidden = false;
    document.body.classList.add("lightbox-open");
    closeBtn.focus();
  }

  function close() {
    dialog.hidden = true;
    img.removeAttribute("src");
    img.alt = "";
    document.body.classList.remove("lightbox-open");
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  buttons.forEach(function (button, i) {
    button.addEventListener("click", function () {
      openAt(i);
    });
  });

  closeBtn.addEventListener("click", close);
  prevBtn.addEventListener("click", function () {
    show(index - 1);
  });
  nextBtn.addEventListener("click", function () {
    show(index + 1);
  });

  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) close();
  });

  document.addEventListener("keydown", function (event) {
    if (dialog.hidden) return;
    if (event.key === "Escape") {
      event.preventDefault();
      close();
      return;
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      show(index - 1);
      return;
    }
    if (event.key === "ArrowRight") {
      event.preventDefault();
      show(index + 1);
      return;
    }
    if (event.key !== "Tab") return;
    var items = focusables();
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
})();
