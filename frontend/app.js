/* =========================================================================
   MEDINGO — APP.JS
   Vanilla JS. No dependencies. Handles:
   1. Scroll-reveal (fade-up, staggered) for every existing section block
   2. Self-drawing architecture connector line
   3. Capability card cursor-follow spotlight
   4. AI report card — animated metrics + count-up (hero)
   5. Prototype step sequential stagger
   ========================================================================= */

(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  /* -----------------------------------------------------------------------
     1. SCROLL REVEAL
     Attach data-reveal to existing content blocks (no HTML edits required)
     and stagger children of grid/flow containers automatically.
     ------------------------------------------------------------------- */
  function markRevealTargets() {
    var singles = [
      "#problem .section-heading",
      "#solution .section-heading",
      "#capabilities .section-heading",
      "#architecture .section-heading",
      "#prototype .section-heading",
      "#launch .section-heading",
      ".launch-card",
    ];

    singles.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        el.setAttribute("data-reveal", "");
      });
    });

    var staggerGroups = [
      ".problem-grid > .problem-card",
      ".solution-flow > .flow-box",
      ".solution-results > div",
      ".capability-grid > .capability-card",
      ".architecture-flow > .arch-box, .architecture-flow > .cloud-box, .architecture-flow .output-card",
      ".prototype-flow > .prototype-step, .prototype-flow > .prototype-result",
    ];

    staggerGroups.forEach(function (sel) {
      var items = document.querySelectorAll(sel);
      items.forEach(function (el, i) {
        el.setAttribute("data-reveal", "");
        el.style.setProperty("--reveal-delay", Math.min(i * 90, 420) + "ms");
      });
    });
  }

  function initRevealObserver() {
    if (prefersReducedMotion) {
      document.querySelectorAll("[data-reveal]").forEach(function (el) {
        el.classList.add("in-view");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -60px 0px" }
    );

    document.querySelectorAll("[data-reveal]").forEach(function (el) {
      observer.observe(el);
    });
  }

  /* -----------------------------------------------------------------------
     2. ARCHITECTURE SELF-DRAWING CONNECTOR
     Updates --arch-progress on .architecture-flow as the section scrolls
     through the viewport, so the vertical spine "builds itself".
     ------------------------------------------------------------------- */
  function initArchitectureLine() {
    var flow = document.querySelector(".architecture-flow");
    if (!flow) return;

    function update() {
      var rect = flow.getBoundingClientRect();
      var vh = window.innerHeight;
      var total = rect.height + vh * 0.6;
      var seen = vh * 0.85 - rect.top;
      var progress = Math.max(0, Math.min(1, seen / total));
      flow.style.setProperty("--arch-progress", progress.toFixed(3));
    }

    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* -----------------------------------------------------------------------
     3. CAPABILITY CARD SPOTLIGHT
     Cursor-follow glow — subtle, premium hover feedback.
     ------------------------------------------------------------------- */
  function initCardSpotlight() {
    if (prefersReducedMotion) return;
    document.querySelectorAll(".capability-card").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
      });
    });
  }

  /* -----------------------------------------------------------------------
     4. HERO AI REPORT CARD — animated metrics
     Counts numeric values up and fills progress bars once in view.
     Safe no-op if the report card markup has not been added yet.
     ------------------------------------------------------------------- */
  function animateCount(el, target, suffix) {
    var start = 0;
    var duration = 1200;
    var startTime = null;

    function step(ts) {
      if (!startTime) startTime = ts;
      var progress = Math.min((ts - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var value = Math.round(start + (target - start) * eased);
      el.textContent = value + (suffix || "");
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function initReportCard() {
    var card = document.querySelector(".ai-report-card");
    if (!card) return;

    var run = function () {
      card.querySelectorAll("[data-count]").forEach(function (el) {
        var target = parseInt(el.getAttribute("data-count"), 10) || 0;
        var suffix = el.getAttribute("data-suffix") || "";
        if (prefersReducedMotion) {
          el.textContent = target + suffix;
        } else {
          animateCount(el, target, suffix);
        }
      });
      card.querySelectorAll(".report-bar-fill").forEach(function (bar) {
        var w = bar.getAttribute("data-fill") || "0%";
        requestAnimationFrame(function () {
          bar.style.width = w;
        });
      });
    };

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            run();
            observer.disconnect();
          }
        });
      },
      { threshold: 0.4 }
    );
    observer.observe(card);
  }

  /* -----------------------------------------------------------------------
     5. LUCIDE ICON INIT (safe no-op if no data-lucide icons are present)
     ------------------------------------------------------------------- */
  function initLucide() {
    if (window.lucide && typeof window.lucide.createIcons === "function") {
      window.lucide.createIcons();
    }
  }

  /* -----------------------------------------------------------------------
     BOOT
     ------------------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    markRevealTargets();
    initRevealObserver();
    initArchitectureLine();
    initCardSpotlight();
    initReportCard();
    initLucide();
  });
})();