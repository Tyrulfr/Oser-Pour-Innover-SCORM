/**
 * Couche de relecture des commentaires vidéaste (cadrage, lecture).
 * Chargée depuis modules/_shared — absente des ZIP SCORM.
 * Désactivée par défaut, un bouton par vidéo concernée.
 */
(function () {
    var DATA_URL = new URL("videaste.json?v=7", document.currentScript.src).href;
    var cards = [];
    var bound = false;

    function toSec(tc) {
        var parts = String(tc || "").trim().split(":");
        if (parts.length === 3) return (+parts[0] * 3600) + (+parts[1] * 60) + parseFloat(parts[2]);
        if (parts.length === 2) return (+parts[0] * 60) + parseFloat(parts[1]);
        var n = parseFloat(tc);
        return isFinite(n) ? n : 0;
    }

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

    function typeLabel(type) {
        if (type === "cadrage") return "Cadrage";
        if (type === "lecture") return "Lecture";
        if (type === "coupe") return "Coupe";
        if (type === "flou") return "Flou";
        if (type === "camera") return "Caméra";
        if (type === "montage") return "Montage";
        if (type === "conclusion") return "Conclusion";
        if (type === "son") return "Son";
        if (type === "habillage") return "Habillage";
        return "Commentaire";
    }

    function seekTo(iframe, seconds) {
        if (!iframe || !iframe.contentWindow) return;
        var win = iframe.contentWindow;
        var t = Math.max(0, seconds);
        var payloads = [
            { event: "command", func: "seekTo", args: [t, true] },
            JSON.stringify({ event: "command", func: "seekTo", args: [t, true] }),
            { method: "seekTo", value: t },
            { method: "setCurrentTime", value: t },
            { action: "seek", time: t }
        ];
        payloads.forEach(function (msg) {
            try { win.postMessage(msg, "*"); } catch (e) {}
        });
    }

    function currentItem(items, t) {
        var i, it, start, end;
        for (i = 0; i < items.length; i++) {
            it = items[i];
            start = toSec(it.debut);
            end = Math.max(toSec(it.fin), start + 4);
            if (t >= start && t <= end) return it;
        }
        return null;
    }

    function highlight(card, item) {
        var rows = card.querySelectorAll(".videaste-item");
        var items = card._videasteItems || [];
        rows.forEach(function (row, i) {
            var on = items[i] === item;
            row.classList.toggle("is-current", on);
        });
    }

    function headerActions(header) {
        var actions = header.querySelector(".video-header-actions");
        if (!actions) {
            actions = document.createElement("div");
            actions.className = "video-header-actions";
            header.appendChild(actions);
        }
        return actions;
    }

    function decorate(card, video) {
        if (card.querySelector(".videaste-toggle")) return;
        var header = card.querySelector(".video-header") || card;
        var wrapper = card.querySelector(".video-wrapper");
        if (!wrapper) return;
        var actions = headerActions(header);
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "videaste-toggle";
        btn.setAttribute("aria-pressed", "false");
        btn.innerHTML = '<i class="fa-solid fa-clapperboard"></i> Vidéaste <span>(' + video.nb + ")</span>";
        btn.addEventListener("click", function () {
            var on = card.classList.toggle("is-videaste-on");
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            if (on) highlight(card, currentItem(video.items, card._videasteTime || 0));
        });
        actions.appendChild(btn);
        var panel = document.createElement("div");
        panel.className = "videaste-panel";
        panel.setAttribute("aria-label", "Commentaires pour le vidéaste");
        video.items.forEach(function (item) {
            var row = document.createElement("button");
            row.type = "button";
            row.className = "videaste-item is-" + (item.type || "note");
            row.innerHTML = '<div class="videaste-kicker">' +
                escapeHtml(typeLabel(item.type)) +
                (item.debut ? " · " + escapeHtml(item.debut) + "–" + escapeHtml(item.fin) : "") +
                "</div>" +
                '<p class="videaste-passage">' + escapeHtml(item.passage || "") + "</p>" +
                '<p class="videaste-action">' + escapeHtml(item.action || "") + "</p>" +
                (item.note ? '<p class="videaste-note">' + escapeHtml(item.note) + "</p>" : "");
            row.addEventListener("click", function () {
                if (!card.classList.contains("is-videaste-on")) {
                    card.classList.add("is-videaste-on");
                    btn.setAttribute("aria-pressed", "true");
                }
                highlight(card, item);
                seekTo(card.querySelector("iframe"), toSec(item.debut) + 0.1);
            });
            panel.appendChild(row);
        });
        var footer = card.querySelector(".video-footer");
        if (footer) footer.insertAdjacentElement("beforebegin", panel);
        else card.appendChild(panel);
        card._videasteItems = video.items;
        card._videasteTime = 0;
        cards.push(card);
    }

    function toNumber(value) {
        var n = Number(value);
        return isFinite(n) ? n : null;
    }

    function parseTime(raw) {
        var data = raw;
        if (typeof data === "string") {
            try { data = JSON.parse(data); } catch (e) { return null; }
        }
        if (Array.isArray(data)) return toNumber(data[1]);
        if (!data || typeof data !== "object") return null;
        var keys = ["currentTime", "current_time", "time", "position", "current"];
        var i, key;
        for (i = 0; i < keys.length; i++) {
            key = keys[i];
            if (data[key] != null && data[key] !== "") {
                var n = toNumber(data[key]);
                if (n != null) return n;
            }
        }
        return null;
    }

    function bindPlayer() {
        if (bound) return;
        bound = true;
        window.addEventListener("message", function (event) {
            var t = parseTime(event.data);
            if (t == null) return;
            cards.forEach(function (card) {
                var iframe = card.querySelector("iframe");
                try {
                    if (iframe && iframe.contentWindow === event.source) {
                        card._videasteTime = t;
                        if (card.classList.contains("is-videaste-on")) {
                            highlight(card, currentItem(card._videasteItems || [], t));
                        }
                    }
                } catch (e) {}
            });
        });
    }

    function boot(videos) {
        document.querySelectorAll(".video-card").forEach(function (card) {
            var code = videoCode(card);
            var video = code && videos[code];
            if (!video || !video.items || !video.items.length) return;
            card.setAttribute("data-videaste-code", code);
            decorate(card, video);
        });
        bindPlayer();
    }

    function start() {
        fetch(DATA_URL).then(function (res) {
            if (!res.ok) throw new Error("videaste.json introuvable");
            return res.json();
        }).then(function (data) {
            boot((data && data.videos) || {});
        }).catch(function () {});
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})();
