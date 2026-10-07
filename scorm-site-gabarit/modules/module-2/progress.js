/**
 * Avancement + scores LMS pour les modules T/E.
 * Remonte vidéos, quiz, memory, capsules MR, completion du grain et du SCO.
 */
(function (global) {
    var cfg = { grainId: '', pages: [], suspendKey: '' };
    var saveTimer = null;
    var VIDEO_END_WINDOW = 15;
    var videoWatchers = [];
    var videoMsgBound = false;

    function parse(str) {
        try { return str ? JSON.parse(str) : {}; } catch (e) { return {}; }
    }

    function emptyGrain() {
        return { vd: [], vn: 0, q: {}, qn: 0, m: 0, mn: 0, mr: [], d: 0 };
    }

    function migrate(raw) {
        var state = {
            v: 1,
            th: raw.th || (raw.theme === 'dark' ? 'd' : 'l'),
            t: raw.t || 0,
            g: raw.g || {}
        };
        var completed = raw.completed || [];
        var scores = raw.scores || {};
        cfg.pages.forEach(function (id) {
            if (!state.g[id]) state.g[id] = emptyGrain();
            if (completed.indexOf(id) !== -1) state.g[id].d = 1;
        });
        return state;
    }

    function merge(a, b) {
        var out = migrate(a);
        var other = migrate(b);
        if (other.th) out.th = other.th;
        out.t = Math.max(out.t || 0, other.t || 0);
        cfg.pages.concat(Object.keys(other.g), Object.keys(out.g)).forEach(function (id) {
            if (!id) return;
            var x = out.g[id] || emptyGrain();
            var y = other.g[id] || emptyGrain();
            var vd = {};
            (x.vd || []).concat(y.vd || []).forEach(function (v) { vd[v] = 1; });
            var q = {};
            [x.q, y.q].forEach(function (bag) {
                if (bag) Object.keys(bag).forEach(function (k) { q[k] = bag[k]; });
            });
            var mr = {};
            (x.mr || []).concat(y.mr || []).forEach(function (v) { mr[v] = 1; });
            out.g[id] = {
                vd: Object.keys(vd),
                vn: Math.max(x.vn || 0, y.vn || 0),
                q: q,
                qn: Math.max(x.qn || 0, y.qn || 0),
                m: Math.max(x.m || 0, y.m || 0),
                mn: Math.max(x.mn || 0, y.mn || 0),
                mr: Object.keys(mr),
                d: (x.d || y.d) ? 1 : 0
            };
        });
        return out;
    }

    function getState() {
        var fromAPI = (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) ? (ScormAPI.getSuspendData() || '') : '';
        var fromLS = '';
        try { fromLS = localStorage.getItem(cfg.suspendKey) || ''; } catch (e) {}
        return merge(parse(fromAPI), parse(fromLS));
    }

    function grain(state, id) {
        id = id || cfg.grainId;
        if (!id) return emptyGrain();
        if (!state.g[id]) state.g[id] = emptyGrain();
        return state.g[id];
    }

    function persist(state) {
        var json = JSON.stringify(state);
        try { localStorage.setItem(cfg.suspendKey, json); } catch (e) {}
        if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) {
            ScormAPI.setSuspendData(json);
        }
    }

    function quizKeys(g) {
        return Object.keys(g.q || {}).filter(function (k) { return k !== "legacy"; });
    }

    function quizStats(g) {
        var keys = quizKeys(g);
        var ok = 0;
        keys.forEach(function (k) { if (g.q[k]) ok += 1; });
        var total = g.qn || keys.length;
        if (g.d && g.qn) total = g.qn;
        return { total: total, ok: ok, pct: total ? Math.round((ok / total) * 100) : 0 };
    }

    function videoIds() {
        var ids = [];
        document.querySelectorAll('.video-card').forEach(function (card, idx) {
            var iframe = card.querySelector('iframe');
            if (!iframe) return;
            var src = iframe.getAttribute('src') || '';
            if (!src || /VIDEO_ID/i.test(src)) return;
            var title = (iframe.getAttribute('title') || card.querySelector('h3') && card.querySelector('h3').textContent || ('video-' + idx)).replace(/\s+/g, ' ').trim();
            ids.push({ card: card, iframe: iframe, id: title });
        });
        return ids;
    }

    function expectedQuizCount() {
        var bank = (global.EVAL_BANK || {})[cfg.grainId] || {};
        var n = 0;
        if (bank.micro) n += 1;
        if (bank.quiz && bank.quiz.length) n += bank.quiz.length;
        return n;
    }

    function grainProgress(g, id) {
        var videos = (cfg.grainId && id === cfg.grainId) ? videoIds() : [];
        var needV = g.vn || videos.length;
        var gotV = (g.vd || []).length;
        if (videos.length) {
            gotV = videos.filter(function (v) { return g.vd.indexOf(v.id) !== -1; }).length;
        }
        var needQ = g.qn || (id === cfg.grainId ? expectedQuizCount() : Object.keys(g.q || {}).length);
        var gotQ = Object.keys(g.q || {}).length;
        var needM = g.mn || 0;
        var gotM = Math.min(g.m || 0, needM || g.m || 0);
        var needMr = ((global.EVAL_BANK || {})[id] || {}).mr ? 1 : 0;
        var gotMr = (g.mr || []).length ? 1 : 0;
        var parts = [];
        parts.push({ w: 0.2, r: g.d ? 1 : 0 });
        if (needV) parts.push({ w: 0.3, r: gotV / needV });
        if (needQ) parts.push({ w: 0.4, r: Math.min(gotQ, needQ) / needQ });
        if (needM || needMr) {
            var act = 0;
            var den = 0;
            if (needM) { act += gotM / needM; den += 1; }
            if (needMr) { act += gotMr; den += 1; }
            parts.push({ w: 0.1, r: den ? act / den : 0 });
        }
        var tw = parts.reduce(function (s, p) { return s + p.w; }, 0) || 1;
        var r = parts.reduce(function (s, p) { return s + p.w * p.r; }, 0) / tw;
        return { ratio: r, videos: { got: gotV, need: needV }, quiz: quizStats(g), memory: { got: gotM, need: needM }, mr: { got: gotMr, need: needMr } };
    }

    function moduleTotals(state) {
        var ratio = 0;
        var quizOk = 0;
        var quizTot = 0;
        var done = 0;
        cfg.pages.forEach(function (id) {
            var g = grain(state, id);
            var p = grainProgress(g, id);
            ratio += p.ratio;
            quizOk += p.quiz.ok;
            quizTot += p.quiz.total;
            if (g.d) done += 1;
        });
        var n = cfg.pages.length || 1;
        var score = quizTot ? Math.round((quizOk / quizTot) * 100) : (done ? Math.round((done / n) * 100) : 0);
        return {
            progress: ratio / n,
            score: score,
            done: done,
            total: n,
            complete: done >= n && n > 0
        };
    }

    function reportLMS(state) {
        if (typeof ScormAPI === 'undefined' || !ScormAPI.isAvailable()) return;
        var tot = moduleTotals(state);
        ScormAPI.setScore(tot.score, 0, 100);
        ScormAPI.setProgress(tot.progress);
        if (cfg.grainId) ScormAPI.setLocation(cfg.grainId);
        cfg.pages.forEach(function (id, idx) {
            var g = grain(state, id);
            var p = grainProgress(g, id);
            ScormAPI.setObjective(idx, {
                id: id,
                completion: g.d ? 'completed' : 'incomplete',
                success: p.quiz.total ? (p.quiz.pct >= 50 ? 'passed' : 'failed') : (g.d ? 'passed' : 'unknown'),
                progress: p.ratio.toFixed(4),
                score: p.quiz.total ? p.quiz.pct : (g.d ? 100 : 0)
            });
        });
        if (tot.complete) {
            ScormAPI.setLessonStatus(tot.score >= 50 ? 'passed' : 'completed');
            ScormAPI.setSuccess(tot.score >= 50 ? 'passed' : 'failed');
        } else {
            ScormAPI.setLessonStatus('incomplete');
            ScormAPI.setSuccess('unknown');
        }
        ScormAPI.commit();
    }

    function save(state) {
        persist(state);
        reportLMS(state);
        refreshUI(state);
    }

    function scheduleSave(state) {
        persist(state);
        clearTimeout(saveTimer);
        saveTimer = setTimeout(function () { reportLMS(state); }, 250);
    }

    function refreshUI(state) {
        state = state || getState();
        var tot = moduleTotals(state);
        var bar = document.getElementById('hero-progress-bar');
        var text = document.getElementById('progress-text');
        if (bar) bar.style.width = Math.round(tot.progress * 100) + '%';
        if (text) text.textContent = tot.done;
        document.querySelectorAll('.video-card[data-video-id]').forEach(function (card) {
            var id = card.getAttribute('data-video-id');
            var g = grain(state, cfg.grainId);
            var watched = !!(g.vd && g.vd.indexOf(id) !== -1);
            card.classList.toggle('is-watched', watched);
            if (watched) {
                card.classList.add('is-near-end');
                var btn = card.querySelector('.video-seen-btn');
                if (btn) btn.hidden = false;
                setVideoHint(card, "Vidéo vue jusqu’au bout.");
            }
        });
    }

    function markVideo(id) {
        if (!cfg.grainId || !id) return;
        var state = getState();
        var g = grain(state);
        if (g.vd.indexOf(id) === -1) g.vd.push(id);
        if (typeof ScormAPI !== 'undefined' && ScormAPI.recordInteraction) {
            ScormAPI.recordInteraction({
                id: cfg.grainId + '_vid_' + id.replace(/\s+/g, '_').slice(0, 80),
                type: 'true-false',
                question: 'Vidéo vue : ' + id,
                response: 'true',
                correct: 'true',
                result: 'correct',
                objective: cfg.grainId
            });
        }
        save(state);
    }

    function markQuiz(itemId, correct, attempts, question) {
        if (!cfg.grainId || !itemId) return;
        var state = getState();
        var g = grain(state);
        g.q[itemId] = correct ? 1 : 0;
        if (typeof ScormAPI !== 'undefined' && ScormAPI.recordInteraction) {
            ScormAPI.recordInteraction({
                id: cfg.grainId + '_' + itemId,
                type: 'choice',
                question: (question || itemId).slice(0, 240),
                response: correct ? 'correct' : 'incorrect',
                result: correct ? 'correct' : 'incorrect',
                weighting: 1,
                objective: cfg.grainId
            });
        }
        save(state);
    }

    function markMemory(flipped, total) {
        if (!cfg.grainId) return;
        var state = getState();
        var g = grain(state);
        g.m = Math.max(g.m || 0, flipped || 0);
        g.mn = total || g.mn || 0;
        scheduleSave(state);
    }

    function markMr(href) {
        var id = String(href || '').split('/').pop() || href;
        if (!id) return;
        var target = cfg.grainId;
        if (!target && cfg.pages) {
            // consultation depuis une copie MR : rattacher au grain porteur
            var map = {
                'mr-grain10.html': 'grain_t2_recherche_innovation',
                'mr-grain19.html': 'grain_t3_besoin_poc',
                'mr-grain5.html': 'grain_t8_financements',
                'mr-grain4.html': 'grain_t10_enrichir_langage'
            };
            target = map[id] || '';
        }
        if (!target) return;
        var state = getState();
        if (!state.g[target]) state.g[target] = emptyGrain();
        if (state.g[target].mr.indexOf(id) === -1) state.g[target].mr.push(id);
        if (typeof ScormAPI !== 'undefined' && ScormAPI.recordInteraction) {
            ScormAPI.recordInteraction({
                id: target + '_mr_' + id.replace(/\s+/g, '_').slice(0, 60),
                type: 'other',
                question: 'Capsule Module Ressources consultée',
                response: id,
                result: 'neutral',
                objective: target
            });
        }
        save(state);
    }

    function markCompleted() {
        if (!cfg.grainId) {
            save(getState());
            return;
        }
        var state = getState();
        grain(state).d = 1;
        save(state);
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        var state = getState();
        state.th = document.body.classList.contains('dark-mode') ? 'd' : 'l';
        persist(state);
        if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) ScormAPI.commit();
    }

    function toNumber(value) {
        var n = Number(value);
        return isFinite(n) ? n : null;
    }

    function deepFind(obj, keys, depth) {
        if (!obj || typeof obj !== "object" || depth > 4) return null;
        var i, key, found;
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

    function parsePlayerMessage(raw) {
        var data = raw;
        if (typeof data === "string") {
            try { data = JSON.parse(data); } catch (e) { data = { event: raw }; }
        }
        if (Array.isArray(data)) {
            return {
                event: String(data[0] || ""),
                current: toNumber(data[1]),
                duration: toNumber(data[2]),
                ended: /ended|finished|complete/i.test(String(data[0] || ""))
            };
        }
        if (data && typeof data === "object" && data.data && typeof data.data === "object" && data.event == null && data.type == null) {
            data = data.data;
        }
        if (!data || typeof data !== "object") return null;
        var event = String(data.event || data.type || data.name || data.action || data.func || data.method || "");
        var info = data.info && typeof data.info === "object" ? data.info : data.arg;
        var current = deepFind(data, ["currentTime", "current_time", "time", "position", "current"], 0);
        var duration = deepFind(data, ["duration", "durationTime", "length", "total"], 0);
        if (info && typeof info === "object") {
            if (current == null) current = toNumber(info.currentTime || info.time);
            if (duration == null) duration = toNumber(info.duration || info.length);
        }
        var text = event + " " + (typeof raw === "string" ? raw : "");
        var ended = data.ended === true || /ended|finished|complete|stopvideo/i.test(text);
        if (data.event === "onStateChange" && (data.info === 0 || (info && info === 0))) ended = true;
        return { event: event, current: current, duration: duration, ended: ended };
    }

    function setVideoHint(card, text) {
        var hint = card.querySelector(".video-watch-hint");
        if (!hint) {
            hint = document.createElement("p");
            hint.className = "video-watch-hint";
            var host = card.querySelector(".video-footer") || card;
            host.appendChild(hint);
        }
        hint.textContent = text;
    }

    function unlockSeenButton(card, watched) {
        card.classList.add("is-near-end");
        if (watched) card.classList.add("is-watched");
        var btn = card.querySelector(".video-seen-btn");
        if (btn) btn.hidden = false;
    }

    function applyVideoProgress(item, msg) {
        if (!item || !msg) return;
        if (msg.duration != null && msg.duration > 0) item.duration = msg.duration;
        if (msg.current != null && msg.current >= 0) item.current = msg.current;
        var duration = item.duration || 0;
        var current = item.current || 0;
        var remaining = duration > 0 ? duration - current : null;
        if (msg.ended || (duration > 0 && remaining != null && remaining <= 0.75)) {
            unlockSeenButton(item.card, true);
            markVideo(item.id);
            setVideoHint(item.card, "Vidéo vue jusqu’au bout.");
            return;
        }
        if (duration > 0 && remaining != null && remaining <= VIDEO_END_WINDOW) {
            unlockSeenButton(item.card, false);
            setVideoHint(item.card, "Plus que " + Math.ceil(remaining) + " s — vous pouvez valider la lecture.");
            return;
        }
        if (duration > 0) {
            setVideoHint(item.card, "Regardez la vidéo jusqu’à la fin pour la valider.");
        }
    }

    function decorateVideos() {
        videoWatchers = [];
        videoIds().forEach(function (item) {
            item.card.setAttribute("data-video-id", item.id);
            item.current = 0;
            item.duration = 0;
            var footer = item.card.querySelector(".video-footer") || item.card;
            if (!item.card.querySelector(".video-watch-hint")) {
                setVideoHint(item.card, "Regardez la vidéo jusqu’à la fin pour la valider.");
            }
            var btn = item.card.querySelector(".video-seen-btn");
            if (!btn) {
                btn = document.createElement("button");
                btn.type = "button";
                btn.className = "video-seen-btn";
                btn.hidden = true;
                btn.innerHTML = '<i class="fa-solid fa-eye"></i> Marquer comme vue';
                btn.addEventListener("click", function () {
                    if (!item.card.classList.contains("is-near-end") && !item.card.classList.contains("is-watched")) return;
                    markVideo(item.id);
                });
                footer.appendChild(btn);
            } else {
                btn.hidden = !item.card.classList.contains("is-watched");
            }
            var src = item.iframe.getAttribute("src") || "";
            if (/youtube\.com|youtu\.be/i.test(src) && src.indexOf("enablejsapi=1") === -1) {
                item.iframe.src = src + (src.indexOf("?") >= 0 ? "&" : "?") + "enablejsapi=1";
            }
            try {
                item.iframe.contentWindow && item.iframe.contentWindow.postMessage(JSON.stringify({ event: "listening" }), "*");
                item.iframe.contentWindow && item.iframe.contentWindow.postMessage({ method: "addEventListener", value: "timeupdate" }, "*");
            } catch (e) {}
            videoWatchers.push(item);
        });
        if (!decorateVideos._ping) {
            decorateVideos._ping = setInterval(function () {
                videoWatchers.forEach(function (watcher) {
                    if (!watcher.iframe || watcher.card.classList.contains("is-watched")) return;
                    try {
                        var win = watcher.iframe.contentWindow;
                        if (!win) return;
                        win.postMessage({ event: "command", func: "getCurrentTime", args: [] }, "*");
                        win.postMessage({ method: "getCurrentTime" }, "*");
                        win.postMessage({ action: "getCurrentTime" }, "*");
                    } catch (e) {}
                });
            }, 1000);
        }
        if (videoMsgBound) return;
        videoMsgBound = true;
        window.addEventListener("message", function (event) {
            var msg = parsePlayerMessage(event.data);
            if (!msg) return;
            var item = null;
            videoWatchers.forEach(function (watcher) {
                try {
                    if (watcher.iframe.contentWindow === event.source) item = watcher;
                } catch (e) {}
            });
            if (!item && videoWatchers.length === 1) item = videoWatchers[0];
            if (!item && msg.ended) {
                item = document.querySelector(".video-card[data-video-id]:not(.is-watched)");
                if (item) {
                    item = videoWatchers.filter(function (w) { return w.card === item || w.id === item.getAttribute("data-video-id"); })[0] || videoWatchers[0];
                }
            }
            if (item) applyVideoProgress(item, msg);
        });
    }

    function boot(options) {
        cfg = options || cfg;
        cfg.pages = cfg.pages || [];
        cfg.suspendKey = cfg.suspendKey || 'module_suspend';
        if (typeof ScormAPI !== 'undefined') ScormAPI.LMSInitialize();
        var state = getState();
        if (state.th === 'd') document.body.classList.add('dark-mode');
        if (cfg.consultMr) markMr(cfg.consultMr);
        if (cfg.grainId) {
            if (typeof ScormAPI !== "undefined" && ScormAPI.setLocation) ScormAPI.setLocation(cfg.grainId);
            var g = grain(state);
            g.vn = videoIds().length;
            g.qn = expectedQuizCount();
            persist(state);
            decorateVideos();
            if (global.EvalApp) EvalApp.mount(cfg.grainId);
        }
        reportLMS(state);
        refreshUI(state);
        var stayInSco = false;
        document.addEventListener('click', function (ev) {
            var a = ev.target && ev.target.closest ? ev.target.closest('a') : null;
            if (!a || !a.href) return;
            try {
                var next = new URL(a.href, window.location.href);
                stayInSco = next.origin === window.location.origin;
            } catch (e) { stayInSco = true; }
        }, true);
        setInterval(function () {
            if (typeof ScormAPI !== 'undefined' && ScormAPI.isAvailable()) ScormAPI.commit();
        }, 30000);
        function flush(leave) {
            if (typeof ScormAPI === 'undefined') return;
            ScormAPI.LMSCommit();
            if (leave && !stayInSco) ScormAPI.LMSFinish();
        }
        window.addEventListener('pagehide', function () { flush(true); });
        window.addEventListener('beforeunload', function () { flush(true); });
    }

    global.ProgressApp = {
        boot: boot,
        getState: getState,
        markVideo: markVideo,
        markQuiz: markQuiz,
        markMemory: markMemory,
        markMr: markMr,
        markCompleted: markCompleted,
        toggleTheme: toggleTheme,
        refreshUI: refreshUI,
        debug: function () {
            var state = getState();
            return { state: state, totals: moduleTotals(state) };
        }
    };
    global.toggleTheme = toggleTheme;
    global.markCompleted = markCompleted;
    global.getState = getState;
})(window);
