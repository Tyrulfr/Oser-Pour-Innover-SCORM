/**
 * Couche de relecture des propositions d’effets (zoom, Ken Burns).
 * Chargée depuis modules/_shared — absente des ZIP SCORM.
 */
(function () {
    var DATA_URL = new URL("effets.json?v=5", document.currentScript.src).href;
    var SCRIPT_SRC = document.currentScript.src;
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
        if (type === "regle") return "Règle";
        if (type === "hold") return "Hold";
        if (type === "recadrage") return "Recadrage";
        if (type === "punch-in") return "Punch-in";
        if (type === "zoom-out") return "Zoom-out";
        if (type === "ken-burns") return "Ken Burns";
        if (type === "interdit") return "Pas d’effet";
        return "Effet";
    }

    function easeInOut(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function sampleKf(kfs, t) {
        if (!kfs || !kfs.length) return { z: 1, x: 50, y: 50 };
        if (t <= kfs[0].t) return kfs[0];
        var i;
        for (i = 0; i < kfs.length - 1; i++) {
            if (t <= kfs[i + 1].t) {
                var a = kfs[i];
                var b = kfs[i + 1];
                var span = b.t - a.t;
                var p = span <= 0 ? 1 : easeInOut((t - a.t) / span);
                return {
                    z: a.z + (b.z - a.z) * p,
                    x: a.x + (b.x - a.x) * p,
                    y: a.y + (b.y - a.y) * p
                };
            }
        }
        return kfs[kfs.length - 1];
    }

    function applyFrame(card, t) {
        var videoEl = card._effetVideo;
        var live = card._effetLive;
        if (!videoEl) return;
        var on = card.classList.contains("is-effet-live");
        var pose = on ? sampleKf(card._effetKf, t) : { z: 1, x: 50, y: 50 };
        videoEl.style.transformOrigin = pose.x + "% " + pose.y + "%";
        videoEl.style.transform = "scale(" + pose.z.toFixed(4) + ")";
        if (live) {
            var item = currentItem(card._effetItems || [], t);
            var zoom = " ×" + pose.z.toFixed(2).replace(".", ",");
            live.textContent = on
                ? ((item && typeLabel(item.type) + " · " + (item.passage || "") + zoom) || ("Plan large" + zoom))
                : "Original — sans effet ×1,00";
        }
        highlight(card, currentItem(card._effetItems || [], t));
    }

    function seekToIframe(iframe, seconds) {
        if (!iframe || !iframe.contentWindow) return;
        var t = Math.max(0, seconds);
        var payloads = [
            { event: "command", func: "seekTo", args: [t, true] },
            JSON.stringify({ event: "command", func: "seekTo", args: [t, true] }),
            { method: "seekTo", value: t },
            { method: "setCurrentTime", value: t },
            { action: "seek", time: t }
        ];
        payloads.forEach(function (msg) {
            try { iframe.contentWindow.postMessage(msg, "*"); } catch (e) {}
        });
    }

    function seekCard(card, seconds, playAfter) {
        var t = Math.max(0, seconds);
        card._effetTime = t;
        if (card.classList.contains("is-effet-preview") && card._effetVideo) {
            seekWhenReady(card._effetVideo, t, function () {
                applyFrame(card, card._effetVideo.currentTime || t);
                if (playAfter) card._effetVideo.play().catch(function () {});
            });
            return;
        }
        seekToIframe(card.querySelector("iframe"), t);
    }

    function seekWhenReady(videoEl, t, done) {
        function go() {
            try { videoEl.currentTime = t; } catch (e) {}
            if (done) done();
        }
        if (videoEl.seekable && videoEl.seekable.length && videoEl.seekable.end(0) > t) {
            go();
            return;
        }
        var tries = 0;
        var id = setInterval(function () {
            tries += 1;
            var end = videoEl.seekable && videoEl.seekable.length ? videoEl.seekable.end(0) : 0;
            if (end > t || videoEl.readyState >= 3 || tries > 40) {
                clearInterval(id);
                go();
            }
        }, 120);
    }

    function firstKenBurnsTime(items) {
        var i, it;
        for (i = 0; i < (items || []).length; i++) {
            it = items[i];
            if (it && it.type === "ken-burns") return toSec(it.debut);
        }
        return 0;
    }

    function currentItem(items, t) {
        var i, it, start, end, best = null, bestStart = -1;
        for (i = 0; i < items.length; i++) {
            it = items[i];
            start = toSec(it.debut);
            end = Math.max(toSec(it.fin), start + 3);
            if (t >= start && t <= end && start >= bestStart) {
                best = it;
                bestStart = start;
            }
        }
        return best;
    }

    function highlight(card, item) {
        var rows = card.querySelectorAll(".effet-item");
        var items = card._effetItems || [];
        rows.forEach(function (row, i) {
            row.classList.toggle("is-current", items[i] === item);
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

    function tickPreview(card) {
        if (!card.classList.contains("is-effet-preview") || !card._effetVideo) return;
        applyFrame(card, card._effetVideo.currentTime || 0);
        if (!card._effetVideo.paused) {
            card._effetRaf = requestAnimationFrame(function () { tickPreview(card); });
        }
    }

    function setPreview(card, on) {
        var iframe = card.querySelector("iframe");
        var stage = card._effetStage;
        var testBtn = card._effetTestBtn;
        card.classList.toggle("is-effet-preview", on);
        if (testBtn) {
            testBtn.setAttribute("aria-pressed", on ? "true" : "false");
            testBtn.innerHTML = on
                ? '<i class="fa-solid fa-xmark"></i> Fermer le test'
                : '<i class="fa-solid fa-play"></i> Tester les effets';
        }
        if (iframe) iframe.style.display = on ? "none" : "";
        if (stage) stage.hidden = !on;
        if (on && card._effetVideo) {
            card.classList.add("is-effet-on", "is-effet-live");
            var listBtn = card.querySelector(".effet-toggle");
            if (listBtn) listBtn.setAttribute("aria-pressed", "true");
            var startAt = firstKenBurnsTime(card._effetItems);
            seekWhenReady(card._effetVideo, startAt, function () {
                applyFrame(card, card._effetVideo.currentTime || startAt);
                card._effetVideo.play().catch(function () {});
                cancelAnimationFrame(card._effetRaf || 0);
                tickPreview(card);
            });
        } else if (card._effetVideo) {
            card._effetVideo.pause();
            cancelAnimationFrame(card._effetRaf || 0);
        }
    }

    function buildPreview(card, video) {
        if (!video.preview) return;
        var wrapper = card.querySelector(".video-wrapper");
        if (!wrapper || card._effetStage) return;
        var src = new URL(video.preview, SCRIPT_SRC).href + (video.preview.indexOf("?") >= 0 ? "&" : "?") + "v=4";
        var stage = document.createElement("div");
        stage.className = "effet-stage";
        stage.hidden = true;
        stage.innerHTML =
            '<video class="effet-video" playsinline preload="auto"></video>' +
            '<div class="effet-live">Chargement de la preview…</div>' +
            '<div class="effet-preview-bar">' +
            '<button type="button" class="effet-mode is-on" data-mode="on">Mes effets</button>' +
            '<button type="button" class="effet-mode" data-mode="off">Original</button>' +
            "</div>";
        var videoEl = stage.querySelector("video");
        videoEl.src = src;
        wrapper.appendChild(stage);
        card._effetStage = stage;
        card._effetVideo = videoEl;
        card._effetLive = stage.querySelector(".effet-live");
        card._effetKf = video.keyframes || [];
        stage.querySelectorAll(".effet-mode").forEach(function (btn) {
            btn.addEventListener("click", function () {
                var live = btn.getAttribute("data-mode") === "on";
                card.classList.toggle("is-effet-live", live);
                stage.querySelectorAll(".effet-mode").forEach(function (b) {
                    b.classList.toggle("is-on", b === btn);
                });
                cancelAnimationFrame(card._effetRaf || 0);
                applyFrame(card, videoEl.currentTime || 0);
                if (!videoEl.paused) tickPreview(card);
            });
        });
        var playBtn = document.createElement("button");
        playBtn.type = "button";
        playBtn.className = "effet-mode effet-play";
        playBtn.textContent = "Lecture";
        playBtn.addEventListener("click", function () {
            if (videoEl.paused) videoEl.play().catch(function () {});
            else videoEl.pause();
        });
        stage.querySelector(".effet-preview-bar").appendChild(playBtn);
        videoEl.addEventListener("play", function () { playBtn.textContent = "Pause"; });
        videoEl.addEventListener("pause", function () { playBtn.textContent = "Lecture"; });
        videoEl.addEventListener("play", function () {
            cancelAnimationFrame(card._effetRaf || 0);
            tickPreview(card);
        });
        videoEl.addEventListener("pause", function () {
            applyFrame(card, videoEl.currentTime || 0);
        });
        videoEl.addEventListener("seeked", function () {
            applyFrame(card, videoEl.currentTime || 0);
        });
    }

    function decorate(card, video) {
        if (card.querySelector(".effet-toggle")) return;
        var header = card.querySelector(".video-header") || card;
        var wrapper = card.querySelector(".video-wrapper");
        if (!wrapper) return;
        var actions = headerActions(header);
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "effet-toggle";
        btn.setAttribute("aria-pressed", "false");
        btn.innerHTML = '<i class="fa-solid fa-film"></i> Effets <span>(' + video.nb + ")</span>";
        btn.addEventListener("click", function () {
            var on = card.classList.toggle("is-effet-on");
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            if (on) highlight(card, currentItem(video.items, card._effetTime || 0));
        });
        actions.appendChild(btn);
        if (video.preview) {
            var testBtn = document.createElement("button");
            testBtn.type = "button";
            testBtn.className = "effet-test";
            testBtn.setAttribute("aria-pressed", "false");
            testBtn.innerHTML = '<i class="fa-solid fa-play"></i> Tester les effets';
            testBtn.addEventListener("click", function () {
                setPreview(card, !card.classList.contains("is-effet-preview"));
            });
            actions.appendChild(testBtn);
            card._effetTestBtn = testBtn;
            buildPreview(card, video);
        }
        var panel = document.createElement("div");
        panel.className = "effet-panel";
        panel.setAttribute("aria-label", "Propositions d’effets");
        video.items.forEach(function (item) {
            var row = document.createElement("button");
            row.type = "button";
            row.className = "effet-item is-" + (item.type || "note");
            row.innerHTML = '<div class="effet-kicker">' +
                escapeHtml(typeLabel(item.type)) +
                (item.debut ? " · " + escapeHtml(item.debut) + "–" + escapeHtml(item.fin) : "") +
                "</div>" +
                '<p class="effet-passage">' + escapeHtml(item.passage || "") + "</p>" +
                '<p class="effet-action">' + escapeHtml(item.action || "") + "</p>" +
                (item.note ? '<p class="effet-note">' + escapeHtml(item.note) + "</p>" : "");
            row.addEventListener("click", function () {
                if (!card.classList.contains("is-effet-on")) {
                    card.classList.add("is-effet-on");
                    btn.setAttribute("aria-pressed", "true");
                }
                highlight(card, item);
                seekCard(card, toSec(item.debut) + 0.15, true);
            });
            panel.appendChild(row);
        });
        var footer = card.querySelector(".video-footer");
        if (footer) footer.insertAdjacentElement("beforebegin", panel);
        else card.appendChild(panel);
        card._effetItems = video.items;
        card._effetTime = 0;
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
                if (card.classList.contains("is-effet-preview")) return;
                var iframe = card.querySelector("iframe");
                try {
                    if (iframe && iframe.contentWindow === event.source) {
                        card._effetTime = t;
                        if (card.classList.contains("is-effet-on")) {
                            highlight(card, currentItem(card._effetItems || [], t));
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
            card.setAttribute("data-effet-code", code);
            decorate(card, video);
        });
        bindPlayer();
    }

    function start() {
        fetch(DATA_URL).then(function (res) {
            if (!res.ok) throw new Error("effets.json introuvable");
            return res.json();
        }).then(function (data) {
            boot((data && data.videos) || {});
        }).catch(function () {});
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})();
