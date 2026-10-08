/**
 * Couche de relecture intro / outro (texte animateur).
 * Chargée depuis modules/_shared — absente des ZIP SCORM.
 * Désactivée par défaut, un bouton par vidéo.
 * Pour retirer : supprimer animateur.js, animateur.css, animateur.json et les balises dans les grains.
 */
(function () {
    var DATA_URL = new URL("animateur.json?v=1", document.currentScript.src).href;

    function videoCode(card) {
        var title = "";
        var iframe = card.querySelector("iframe");
        var h3 = card.querySelector("h3");
        if (iframe) title += " " + (iframe.getAttribute("title") || "");
        if (h3) title += " " + (h3.textContent || "");
        var match = title.match(/\b(E\d+bis|T\d+|E\d+)\b/i);
        if (!match) return "";
        return match[1].replace(/^t/i, "T").replace(/^e/i, "E").replace(/BIS$/i, "bis");
    }

    function escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, function (ch) {
            return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch];
        });
    }

    function headerActions(header) {
        var actions = header.querySelector(".video-header-actions");
        if (!actions) {
            actions = document.createElement("div");
            actions.className = "video-header-actions";
            header.appendChild(actions);
        }
        var incrust = header.querySelector(":scope > .incrust-toggle");
        if (incrust) actions.appendChild(incrust);
        return actions;
    }

    function block(kind, text, isTemoin) {
        var el = document.createElement("div");
        el.className = "anim-block is-" + kind + (isTemoin ? " is-temoin" : "");
        el.innerHTML = '<div class="anim-kicker">' +
            (kind === "intro" ? "Avant la vidéo · texte animateur" : "Après la vidéo · texte animateur") +
            "</div><p>" + escapeHtml(text) + "</p>";
        return el;
    }

    function decorate(card, entry) {
        if (card.querySelector(".anim-toggle")) return;
        var header = card.querySelector(".video-header") || card;
        var wrapper = card.querySelector(".video-wrapper");
        if (!wrapper) return;
        var isTemoin = !header.classList.contains("expert");
        var actions = headerActions(header);
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "anim-toggle";
        btn.setAttribute("aria-pressed", "false");
        btn.innerHTML = '<i class="fa-solid fa-microphone"></i> Intro / Outro';
        btn.addEventListener("click", function () {
            var on = card.classList.toggle("is-anim-on");
            btn.setAttribute("aria-pressed", on ? "true" : "false");
        });
        actions.insertBefore(btn, actions.firstChild);
        var intro = block("intro", entry.intro, isTemoin);
        var outro = block("outro", entry.outro, isTemoin);
        header.insertAdjacentElement("afterend", intro);
        var footer = card.querySelector(".video-footer");
        if (footer) footer.insertAdjacentElement("beforebegin", outro);
        else card.appendChild(outro);
    }

    function boot(videos) {
        document.querySelectorAll(".video-card").forEach(function (card) {
            var code = videoCode(card);
            var entry = code && videos[code];
            if (!entry || !entry.intro || !entry.outro) return;
            card.setAttribute("data-anim-code", code);
            decorate(card, entry);
        });
    }

    function start() {
        fetch(DATA_URL).then(function (res) {
            if (!res.ok) throw new Error("animateur.json introuvable");
            return res.json();
        }).then(function (data) {
            boot((data && data.videos) || {});
        }).catch(function () {});
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})();
