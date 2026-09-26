/**
 * Couche de relecture des incrustations (mots-clés / petits schémas).
 * Chargée depuis modules/_shared — absente des ZIP SCORM.
 * Désactivée par défaut, un bouton par vidéo.
 */
(function (global) {
    var DATA_URL = new URL("incrustations.json", document.currentScript.src).href;
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

    function currentItem(items, t) {
        var i, it, start, end;
        for (i = 0; i < items.length; i++) {
            it = items[i];
            start = toSec(it.debut);
            end = toSec(it.fin);
            if (end < start) end = start;
            if (t >= start && t <= end + 0.35) return it;
        }
        return null;
    }

    function schemaHtml(text) {
        var raw = String(text || "").trim();
        if (!raw) return "";
        var parts = raw.split(/\s*(?:→|->|\|)\s*/).filter(Boolean);
        if (parts.length < 2) {
            return '<div class="incrust-label">' + escapeHtml(raw) + "</div>";
        }
        var sep = /→|->/.test(raw) ? "→" : "|";
        return '<div class="incrust-schema">' + parts.map(function (p, idx) {
            return (idx ? '<span class="incrust-arrow">' + escapeHtml(sep) + "</span>" : "") +
                '<span class="incrust-node">' + escapeHtml(p) + "</span>";
        }).join("") + "</div>";
    }

    function escapeHtml(str) {
        return String(str).replace(/[&<>"']/g, function (ch) {
            return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch];
        });
    }

    function render(card, item, time) {
        var layer = card.querySelector(".incrust-layer");
        var now = card.querySelector(".incrust-now");
        if (!layer) return;
        var panel = layer.querySelector(".incrust-panel");
        if (!item) {
            layer.classList.add("is-empty");
            panel.innerHTML = '<div class="incrust-kicker">Proposition d’incrustation</div>' +
                '<div class="incrust-label">En attente du prochain calage</div>' +
                '<div class="incrust-pourquoi">Lancez la lecture. Les mots-clés et schémas apparaissent au timecode du dérushage.</div>';
            if (now) now.textContent = "Incrustations actives — lancez la lecture pour voir le calage.";
            return;
        }
        layer.classList.remove("is-empty");
        var kind = item.type === "schema" ? "Petit schéma" : "Mot-clé";
        var body = item.type === "schema" && item.schema
            ? schemaHtml(item.schema)
            : '<div class="incrust-label">' + escapeHtml(item.ecran || item.schema || "—") + "</div>";
        var extra = item.developpe ? '<div class="incrust-developpe">' + escapeHtml(item.developpe) + "</div>" : "";
        var why = item.pourquoi ? '<div class="incrust-pourquoi">' + escapeHtml(item.pourquoi) + "</div>" : "";
        panel.innerHTML = '<div class="incrust-kicker">' + escapeHtml(kind) + " · " +
            escapeHtml(item.debut) + "–" + escapeHtml(item.fin) + "</div>" + body + extra + why;
        if (now) {
            now.innerHTML = "<strong>" + escapeHtml(kind) + "</strong> · " +
                escapeHtml(item.debut) + "–" + escapeHtml(item.fin) + " · " +
                escapeHtml(item.ecran || item.schema || "") +
                (item.pourquoi ? " — " + escapeHtml(item.pourquoi) : "");
        }
    }

    function decorate(card, video) {
        if (card.querySelector(".incrust-toggle")) return;
        var header = card.querySelector(".video-header") || card;
        var wrapper = card.querySelector(".video-wrapper");
        if (!wrapper) return;
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "incrust-toggle";
        btn.setAttribute("aria-pressed", "false");
        btn.innerHTML = '<i class="fa-solid fa-layer-group"></i> Incrustations <span>(' + video.nb + ")</span>";
        btn.addEventListener("click", function () {
            var on = card.classList.toggle("is-incrust-on");
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            if (on) render(card, currentItem(video.items, card._incrustTime || 0), card._incrustTime || 0);
        });
        header.appendChild(btn);
        var stage = document.createElement("div");
        stage.className = "incrust-stage";
        wrapper.parentNode.insertBefore(stage, wrapper);
        stage.appendChild(wrapper);
        var layer = document.createElement("div");
        layer.className = "incrust-layer is-empty";
        layer.innerHTML = '<div class="incrust-panel"></div>';
        stage.appendChild(layer);
        var now = document.createElement("div");
        now.className = "incrust-now";
        stage.insertAdjacentElement("afterend", now);
        card._incrustItems = video.items;
        card._incrustTime = 0;
        render(card, null, 0);
        cards.push(card);
    }

    function applyTime(card, seconds) {
        if (seconds == null || !isFinite(seconds)) return;
        card._incrustTime = seconds;
        if (!card.classList.contains("is-incrust-on")) return;
        render(card, currentItem(card._incrustItems || [], seconds), seconds);
    }

    function toNumber(value) {
        var n = Number(value);
        return isFinite(n) ? n : null;
    }

    function deepFind(obj, keys, depth) {
        if (!obj || typeof obj !== "object" || depth > 4) return null;
        var key, found, i;
        for (i = 0; i < keys.length; i++) {
            key = keys[i];
            if (obj[key] != null && obj[key] !== "") {
                found = toNumber(obj[key]);
                if (found != null) return found;
            }
        }
        for (key in obj) {
            if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;
            if (obj[key] && typeof obj[key] === "object") {
                found = deepFind(obj[key], keys, depth + 1);
                if (found != null) return found;
            }
        }
        return null;
    }

    function parseTime(raw) {
        var data = raw;
        if (typeof data === "string") {
            try { data = JSON.parse(data); } catch (e) { return null; }
        }
        if (Array.isArray(data)) return toNumber(data[1]);
        if (!data || typeof data !== "object") return null;
        return deepFind(data, ["currentTime", "current_time", "time", "position", "current"], 0);
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
                    if (iframe && iframe.contentWindow === event.source) applyTime(card, t);
                } catch (e) {}
            });
        });
        setInterval(function () {
            cards.forEach(function (card) {
                if (!card.classList.contains("is-incrust-on")) return;
                var iframe = card.querySelector("iframe");
                if (!iframe || !iframe.contentWindow) return;
                try {
                    iframe.contentWindow.postMessage({ event: "command", func: "getCurrentTime", args: [] }, "*");
                    iframe.contentWindow.postMessage({ method: "getCurrentTime" }, "*");
                    iframe.contentWindow.postMessage({ action: "getCurrentTime" }, "*");
                } catch (e) {}
            });
        }, 400);
    }

    function boot(videos) {
        document.querySelectorAll(".video-card").forEach(function (card) {
            var code = videoCode(card);
            var video = code && videos[code];
            if (!video || !video.items || !video.items.length) return;
            card.setAttribute("data-incrust-code", code);
            decorate(card, video);
        });
        bindPlayer();
    }

    function start() {
        fetch(DATA_URL).then(function (res) {
            if (!res.ok) throw new Error("incrustations.json introuvable");
            return res.json();
        }).then(function (data) {
            boot((data && data.videos) || {});
        }).catch(function () {});
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})(window);
