/**
 * Ferme les panneaux d'info (details.section-info-details) lors d'un clic
 * en dehors de la bulle (ex. sur le graphique).
 */
(function () {
    document.addEventListener(
        "click",
        function (e) {
            document.querySelectorAll("details.section-info-details[open]").forEach(function (details) {
                if (!details.contains(e.target)) {
                    details.removeAttribute("open");
                }
            });
        },
        false
    );
})();
