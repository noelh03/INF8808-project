/* Story sections: narrative text stays hidden until the entrance animation runs. */
(function () {
    var MAX_SETUP_ATTEMPTS = 200;
    var setupAttempts = 0;
    var activeSection = null;
    var wasAboveThreshold = new WeakMap();

    var reduceMotion =
        typeof window.matchMedia === "function" &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var ENTRANCE_DURATION_MS = 1300;
    var ENTRANCE_DELAY_MS = 100;
    var ENTRANCE_SLIDE_PX = 20;

    if (!reduceMotion) {
        document.documentElement.classList.add("story-fade");
    }

    function hideStoryText(section) {
        [".section-intro", ".section-inline-info"].forEach(function (sel) {
            var node = section.querySelector(sel);
            if (!node) return;
            if (typeof node.getAnimations === "function") {
                node.getAnimations().forEach(function (a) {
                    a.cancel();
                });
            }
            node.style.opacity = "0";
            node.style.transform = "translateY(" + ENTRANCE_SLIDE_PX + "px)";
            node.style.filter = "blur(6px)";
            node.style.pointerEvents = "none";
        });
    }

    function pulseElement(el) {
        if (!el) return;
        if (reduceMotion) {
            el.style.opacity = "1";
            el.style.transform = "none";
            el.style.filter = "none";
            el.style.pointerEvents = "auto";
            return;
        }
        if (typeof el.animate !== "function") {
            el.classList.remove("section-fade-pulse");
            void el.offsetWidth;
            el.classList.add("section-fade-pulse");
            el.style.pointerEvents = "auto";
            return;
        }
        if (typeof el.getAnimations === "function") {
            el.getAnimations().forEach(function (anim) {
                anim.cancel();
            });
        }
        el.style.removeProperty("opacity");
        el.style.removeProperty("transform");
        el.style.removeProperty("filter");
        el.style.removeProperty("pointer-events");
        var anim = el.animate(
            [
                {
                    opacity: 0,
                    transform: "translateY(" + ENTRANCE_SLIDE_PX + "px)",
                    filter: "blur(8px)",
                    offset: 0,
                },
                {
                    opacity: 0.45,
                    transform: "translateY(10px)",
                    filter: "blur(3px)",
                    offset: 0.4,
                },
                {
                    opacity: 1,
                    transform: "translateY(0)",
                    filter: "blur(0)",
                    offset: 1,
                },
            ],
            {
                duration: ENTRANCE_DURATION_MS,
                delay: ENTRANCE_DELAY_MS,
                easing: "cubic-bezier(0.16, 1, 0.32, 1)",
                fill: "both",
            }
        );
        anim.onfinish = function () {
            el.style.pointerEvents = "auto";
        };
    }

    function pulseText(section) {
        if (!section) return;
        pulseElement(section.querySelector(".section-intro"));
        pulseElement(section.querySelector(".section-inline-info"));
    }

    function activateSection(section) {
        if (!section || activeSection === section) return;
        activeSection = section;
        pulseText(section);
    }

    function init(sections) {
        if (!("IntersectionObserver" in window)) return;

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    var el = entry.target;
                    var above =
                        entry.isIntersecting && entry.intersectionRatio >= 0.5;

                    if (above) {
                        el.classList.add("section-visible");
                        var already = wasAboveThreshold.get(el);
                        if (!already) {
                            wasAboveThreshold.set(el, true);
                            activateSection(el);
                        }
                    } else {
                        el.classList.remove("section-visible");
                        wasAboveThreshold.set(el, false);
                        hideStoryText(el);
                        if (activeSection === el) {
                            activeSection = null;
                        }
                    }
                });
            },
            { threshold: [0.5, 0.75] }
        );

        sections.forEach(function (s) {
            observer.observe(s);
        });
    }

    function trySetup() {
        setupAttempts += 1;
        var sections = document.querySelectorAll(".story-section");
        if (!sections.length) {
            if (setupAttempts < MAX_SETUP_ATTEMPTS) {
                requestAnimationFrame(trySetup);
            }
            return;
        }
        init(sections);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", trySetup);
    } else {
        trySetup();
    }
})();
