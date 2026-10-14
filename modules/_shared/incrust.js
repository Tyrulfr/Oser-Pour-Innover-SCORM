/**
 * Couche de relecture des incrustations (mots-clés / petits schémas).
 * Chargée depuis modules/_shared — absente des ZIP SCORM.
 * Désactivée par défaut, un bouton par vidéo.
 */
(function (global) {
    var DATA_URL = new URL("incrustations.json?v=25", document.currentScript.src).href;
    var SCRIPT_SRC = document.currentScript.src;
    var cards = [];
    var bound = false;
    var MIN_HOLD = 4.5;
    var HOLD_PAD = 2;

    function toSec(tc) {
        var parts = String(tc || "").trim().split(":");
        if (parts.length === 3) return (+parts[0] * 3600) + (+parts[1] * 60) + parseFloat(parts[2]);
        if (parts.length === 2) return (+parts[0] * 60) + parseFloat(parts[1]);
        var n = parseFloat(tc);
        return isFinite(n) ? n : 0;
    }

    function windowOf(items, index) {
        var it = items[index];
        var start = toSec(it.debut);
        var end = toSec(it.fin);
        if (end < start) end = start;
        var hold = Math.max(end + HOLD_PAD, start + MIN_HOLD);
        if (index + 1 < items.length) {
            var nextStart = toSec(items[index + 1].debut);
            if (nextStart > start) hold = Math.min(hold, nextStart - 0.15);
        }
        if (hold < end) hold = end;
        return { start: start, end: hold };
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
        var i, win;
        for (i = 0; i < items.length; i++) {
            win = windowOf(items, i);
            if (t >= win.start && t <= win.end) return items[i];
        }
        return null;
    }

    function itemIndex(items, item) {
        var i;
        for (i = 0; i < items.length; i++) {
            if (items[i] === item) return i;
        }
        return -1;
    }

    function labelOf(item) {
        return item.ecran || item.schema || "Incrustation";
    }

    function idNum(item) {
        var m = String(item.id || "").match(/(\d+)$/);
        return m ? m[1] : "";
    }

    /* Ensemble 1 = cycle (schéma 5). Ensemble 2 = incrustations, seulement si le concept n’existe pas. */
    var PICTO = {
        "fa-lightbulb": "cycle/idee.png",
        "fa-play": "cycle/idee.png",
        "fa-pen": "cycle/creativite.png",
        "fa-circle-check": "cycle/solutions.png",
        "fa-flag-checkered": "cycle/solutions.png",
        "fa-puzzle-piece": "cycle/solutions.png",
        "fa-file-magnifying-glass": "cycle/selection.png",
        "fa-link": "cycle/prototypage.png",
        "fa-stairs": "cycle/prototypage.png",
        "fa-flask": "cycle/experimentation.png",
        "fa-magnifying-glass": "cycle/decouverte.png",
        "fa-binoculars": "cycle/decouverte.png",
        "fa-location-dot": "cycle/decouverte.png",
        "fa-file-lines": "cycle/valorisation.png",
        "fa-file-signature": "cycle/valorisation.png",
        "fa-file-contract": "cycle/valorisation.png",
        "fa-book": "cycle/valorisation.png",
        "fa-diagram-project": "cycle/valorisation.png",
        "fa-person-walking": "cycle/transfert.png",
        "fa-share-nodes": "cycle/transfert.png",
        "fa-rocket": "cycle/transfert.png",
        "fa-graduation-cap": "cycle/transfert.png",
        "fa-road": "cycle/transfert.png",
        "fa-palette": "cycle/design.png",
        "fa-gear": "cycle/design.png",
        "fa-industry": "cycle/production.png",
        "fa-store": "cycle/production.png",
        "fa-bullhorn": "cycle/diffusion.png",
        "fa-newspaper": "cycle/diffusion.png",
        "fa-users": "cycle/adoption-impact.png",
        "fa-seedling": "cycle/adoption-impact.png",
        "fa-leaf": "cycle/adoption-impact.png",
        "fa-heart-pulse": "cycle/adoption-impact.png",
        "fa-circle-question": "incrustations/question.png",
        "fa-lock": "incrustations/secret.png",
        "fa-shield-halved": "incrustations/protection.png",
        "fa-coins": "incrustations/financement.png",
        "fa-comments-dollar": "incrustations/financement.png",
        "fa-comments": "incrustations/dialogue.png",
        "fa-comment": "incrustations/dialogue.png",
        "fa-building": "incrustations/etablissement.png",
        "fa-envelope": "incrustations/enveloppe.png",
        "fa-code": "incrustations/logiciel.png",
        "fa-trademark": "incrustations/marque.png",
        "fa-copyright": "incrustations/droit-auteur.png",
        "fa-gem": "incrustations/actif.png",
        "fa-chart-line": "incrustations/strategie.png",
        "fa-chess": "incrustations/strategie.png",
        "fa-triangle-exclamation": "incrustations/alerte.png",
        "fa-handshake": "incrustations/partenaire.png",
        "fa-scale-balanced": "incrustations/equilibre.png",
        "fa-clock": "incrustations/temps.png",
        "fa-stopwatch": "incrustations/temps.png",
        "fa-list": "cycle/valorisation.png",
        "fa-cubes": "cycle/production.png",
        "fa-bullseye": "incrustations/cible.png",
        "fa-code-branch": "incrustations/pivot.png",
        "fa-arrows-rotate": "incrustations/pivot.png",
        "fa-shuffle": "incrustations/pivot.png",
        "fa-address-book": "incrustations/contact.png",
        "fa-user": "incrustations/contact.png",
        "fa-circle": "incrustations/sans.png"
    };

    function picto(name) {
        var file = PICTO[name] || "incrustations/question.png";
        var url = new URL("icones/" + file, SCRIPT_SRC).href;
        return '<img class="incrust-picto" alt="" src="' + url + '">';
    }

    function splitParts(text) {
        return String(text || "").split(/\s*(?:→|->|\|)\s*/).filter(Boolean);
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
            { action: "seek", time: t },
            { action: "setCurrentTime", currentTime: t },
            { type: "player:seek", currentTime: t }
        ];
        payloads.forEach(function (msg) {
            try { win.postMessage(msg, "*"); } catch (e) {}
        });
    }

    function highlightJump(card, item) {
        var jumps = card.querySelectorAll(".incrust-jump");
        var items = card._incrustItems || [];
        var idx = itemIndex(items, item);
        jumps.forEach(function (btn, i) {
            var on = i === idx;
            btn.classList.toggle("is-current", on);
            btn.setAttribute("aria-current", on ? "true" : "false");
        });
    }

    function schemaHtml(text) {
        var raw = String(text || "").trim();
        if (!raw) return "";
        var parts = splitParts(raw);
        if (parts.length < 2) {
            return '<div class="incrust-label">' + escapeHtml(raw) + "</div>";
        }
        var sep = /→|->/.test(raw) ? "→" : "|";
        return '<div class="incrust-schema">' + parts.map(function (p, idx) {
            return (idx ? '<span class="incrust-arrow">' + escapeHtml(sep) + "</span>" : "") +
                '<span class="incrust-node">' + escapeHtml(p) + "</span>";
        }).join("") + "</div>";
    }

    function etapesHtml(text, icons, opts) {
        var parts = splitParts(text);
        var emp = (opts && opts.emphasis) || "";
        var fork = opts && opts.fork;
        return '<div class="incrust-etapes' + (fork ? " is-fork" : "") + ((opts && opts.vertical) ? " is-vertical" : "") + '">' + parts.map(function (p, i) {
            var ico = icons && icons[i] ? '<span class="incrust-step-ico">' + picto(icons[i]) + "</span>" : "";
            var on = emp && p === emp;
            return (i ? '<span class="incrust-arrow' + (fork && i === parts.length - 1 ? " is-fork" : "") + '">→</span>' : "") +
                '<span class="incrust-step' + (on ? " is-emphasis" : "") + '">' + ico +
                '<span>' + escapeHtml(p) + "</span></span>";
        }).join("") + "</div>";
    }

    function motionHtml(item) {
        var vue = item.vue;
        var label = '<div class="incrust-label">' + escapeHtml(item.ecran || "") + "</div>";
        if (vue === "horloge") {
            return '<div class="incrust-motion is-horloge">' +
                '<div class="incrust-ico">' + picto("fa-clock") + "</div>" +
                '<div class="incrust-compteurs">' +
                '<div class="incrust-compte is-a"><strong>55</strong><span>minutes</span></div>' +
                '<div class="incrust-compte is-b"><strong>5</strong><span>min</span></div>' +
                "</div>" +
                '<div class="incrust-caption">pour définir le problème · pour le résoudre</div></div>';
        }
        if (vue === "cible") {
            return '<div class="incrust-motion is-cible">' +
                '<div class="incrust-ico">' + picto("fa-bullseye") + "</div>" +
                '<div class="incrust-etapes">' +
                '<span class="incrust-step is-emphasis"><span>Le bon problème</span></span>' +
                '<span class="incrust-arrow">→</span>' +
                '<span class="incrust-step"><span>La bonne solution</span></span></div></div>';
        }
        if (vue === "etapes") return '<div class="incrust-motion">' + etapesHtml(item.schema || item.ecran, item.icones) + "</div>";
        if (vue === "pivot") {
            return '<div class="incrust-motion is-pivot">' +
                '<div class="incrust-path" aria-hidden="true"><span></span></div>' +
                etapesHtml(item.schema || item.ecran, item.icones, { fork: true, emphasis: "Pivoter" }) +
                "</div>";
        }
        if (vue === "dialogue") {
            return '<div class="incrust-motion is-dialogue">' +
                '<div class="incrust-ico">' + picto("fa-comments") + "</div>" +
                label + "</div>";
        }
        if (vue === "morph") {
            return '<div class="incrust-motion is-morph">' +
                '<div class="incrust-ico">' + picto("fa-arrows-rotate") + "</div>" +
                '<div class="incrust-morph">' +
                '<span class="is-from">Culture de recherche</span>' +
                '<span class="incrust-arrow">→</span>' +
                '<span class="is-to">Culture de valorisation</span></div>' +
                label + "</div>";
        }
        if (vue === "frise") {
            return '<div class="incrust-motion is-frise' + (item.vertical ? " is-vertical" : "") + '">' +
                (item.titre ? '<div class="incrust-col-title">' + escapeHtml(item.titre) + "</div>" : "") +
                (item.vertical ? "" : '<div class="incrust-frise-line" aria-hidden="true"></div>') +
                etapesHtml(item.schema || item.ecran, item.icones, { vertical: !!item.vertical }) +
                (item.caption ? '<div class="incrust-caption">' + escapeHtml(item.caption) + "</div>" : "") +
                "</div>";
        }
        if (vue === "traverse") {
            return '<div class="incrust-motion is-traverse">' +
                '<div class="incrust-walk" aria-hidden="true">' +
                picto("fa-flask") + '<span class="incrust-arrow">→</span>' + picto("fa-person-walking") +
                '<span class="incrust-arrow">→</span>' + picto("fa-users") + "</div>" +
                label + "</div>";
        }
        if (vue === "colonnes") {
            return '<div class="incrust-motion is-colonnes">' +
                '<div class="incrust-col"><div class="incrust-col-title">Techno Push</div>' +
                etapesHtml("Technologie → Produit → Marché") + "</div>" +
                '<div class="incrust-col-vs">vs</div>' +
                '<div class="incrust-col"><div class="incrust-col-title">Market Pull</div>' +
                etapesHtml("Besoin → Solution → Technologie") + "</div></div>";
        }
        if (vue === "puzzle") {
            return '<div class="incrust-motion is-puzzle">' +
                '<div class="incrust-pieces">' +
                '<span class="incrust-piece is-left">' + picto("fa-puzzle-piece") + " Problème</span>" +
                '<span class="incrust-piece is-right">' + picto("fa-puzzle-piece") + " Solution</span></div>" +
                '<div class="incrust-label is-final">Problem–Solution Fit</div></div>';
        }
        if (vue === "conclusion") {
            return '<div class="incrust-motion is-conclusion">' +
                '<div class="incrust-ico">' + picto("fa-handshake") + "</div>" + label + "</div>";
        }
        if (vue === "texte") {
            return '<div class="incrust-motion is-texte">' +
                (item.icone ? '<div class="incrust-ico">' + picto(item.icone) + "</div>" : "") +
                label +
                (item.caption ? '<div class="incrust-caption">' + escapeHtml(item.caption) + "</div>" : "") +
                "</div>";
        }
        if (vue === "deux-parties") {
            var parties = item.parties || splitParts(item.schema || item.ecran);
            return '<div class="incrust-motion is-deux-parties">' +
                (item.titre ? '<div class="incrust-col-title">' + escapeHtml(item.titre) + "</div>" : "") +
                '<div class="incrust-duo">' +
                parties.map(function (p, i) {
                    return '<span class="incrust-part">' +
                        '<span class="incrust-part-n">' + (i + 1) + "</span>" +
                        escapeHtml(p) + "</span>";
                }).join('<span class="incrust-arrow">ou</span>') +
                "</div>" +
                (item.caption ? '<div class="incrust-caption">' + escapeHtml(item.caption) + "</div>" : "") +
                "</div>";
        }
        if (vue === "deux-messages") {
            var msgs = item.messages || [item.ecran];
            return '<div class="incrust-motion is-deux-messages">' +
                (item.icone ? '<div class="incrust-ico">' + picto(item.icone) + "</div>" : "") +
                msgs.map(function (m) {
                    return '<div class="incrust-msg">' + escapeHtml(m) + "</div>";
                }).join("") + "</div>";
        }
        if (vue === "boucle") {
            var loop = splitParts((item.schema || item.ecran).replace(/\s*⇄\s*/g, " → "));
            return '<div class="incrust-motion is-boucle">' +
                '<div class="incrust-loop">' +
                '<span class="incrust-step">' + escapeHtml(loop[0] || "Solutions commerciales") + "</span>" +
                '<span class="incrust-loop-arrows" aria-hidden="true">⇄</span>' +
                '<span class="incrust-step">' + escapeHtml(loop[1] || "Solutions techniques") + "</span></div>" +
                '<div class="incrust-caption">' + escapeHtml(item.caption || "Interactions permanentes") + "</div></div>";
        }
        if (vue === "tableaux") {
            var blocs = item.blocs || [];
            return '<div class="incrust-motion is-tableaux">' +
                (item.titre ? '<div class="incrust-col-title">' + escapeHtml(item.titre) + "</div>" : "") +
                '<div class="incrust-tables">' + blocs.map(function (bloc) {
                    return '<div class="incrust-table">' +
                        '<div class="incrust-col-title">' +
                        (bloc.icone ? picto(bloc.icone) + " " : "") +
                        escapeHtml(bloc.titre || "") + "</div><ul>" +
                        (bloc.lignes || []).map(function (ligne) {
                            return "<li>" + escapeHtml(ligne) + "</li>";
                        }).join("") + "</ul></div>";
                }).join("") + "</div></div>";
        }
        if (vue === "questions") {
            var qs = item.questions || [];
            var qIco = ["fa-flag-checkered", "fa-shuffle"];
            return '<div class="incrust-motion is-questions">' + qs.map(function (q, i) {
                return '<div class="incrust-q">' + picto(qIco[i] || "fa-circle-question") +
                    "<span>" + escapeHtml(q) + "</span></div>";
            }).join("") + "</div>";
        }
        if (vue === "grille") {
            var cells = item.cellules || [];
            return '<div class="incrust-motion is-grille' + (item.titre ? " has-title" : "") + '"' +
                (item.colonnes ? ' style="grid-template-columns:repeat(' + item.colonnes + ',minmax(0,1fr))"' : "") + '>' +
                (item.titre ? '<div class="incrust-col-title">' + escapeHtml(item.titre) + "</div>" : "") +
                (item.centre ? '<div class="incrust-hub-core">' + escapeHtml(item.centre) + "</div>" : "") +
                cells.map(function (c) {
                    return '<span class="incrust-cell">' +
                        (c.icone ? '<span class="incrust-step-ico">' + picto(c.icone) + "</span>" : "") +
                        "<span>" + escapeHtml(c.texte || "") + "</span>" +
                        (c.detail ? '<span class="incrust-cell-detail">' + escapeHtml(c.detail) + "</span>" : "") +
                        "</span>";
                }).join("") +
                (item.caption ? '<div class="incrust-caption">' + escapeHtml(item.caption) + "</div>" : "") +
                "</div>";
        }
        if (vue === "successifs") {
            var seq = item.cellules || [];
            return '<div class="incrust-motion is-successifs">' + seq.map(function (c) {
                return '<span class="incrust-cell">' +
                    (c.icone ? '<span class="incrust-step-ico">' + picto(c.icone) + "</span>" : "") +
                    "<span>" + escapeHtml(c.texte || "") + "</span></span>";
            }).join("") + "</div>";
        }
        if (vue === "liste") {
            var lignes = item.lignes || [];
            return '<div class="incrust-motion is-liste">' +
                (item.titre ? '<div class="incrust-col-title">' + escapeHtml(item.titre) + "</div>" : "") +
                "<ul>" + lignes.map(function (ligne) {
                    return "<li>" + picto("fa-circle-check") + "<span>" + escapeHtml(ligne) + "</span></li>";
                }).join("") + "</ul></div>";
        }
        if (vue === "hub") {
            var sats = item.satellites || [];
            function sat(i, cls, fallback) {
                var s = sats[i] || {};
                return '<span class="incrust-hub-sat ' + cls + '">' +
                    (s.icone ? '<span class="incrust-step-ico">' + picto(s.icone) + "</span>" : "") +
                    "<span>" + escapeHtml(s.texte || fallback) + "</span></span>";
            }
            return '<div class="incrust-motion is-hub">' +
                (item.titre ? '<div class="incrust-col-title">' + escapeHtml(item.titre) + "</div>" : "") +
                '<div class="incrust-hub">' +
                sat(0, "is-a", "Conseils") +
                sat(1, "is-b", "Contacts") +
                '<span class="incrust-hub-core">' + escapeHtml(item.centre || "Chargé de valorisation") + "</span>" +
                sat(2, "is-c", "Financements") +
                sat(3, "is-d", "Cadrage contractuel") +
                "</div></div>";
        }
        return label;
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
            layer.className = "incrust-layer is-empty";
            panel.innerHTML = '<div class="incrust-waiting">Proposition d’incrustation</div>';
            if (now) now.textContent = "Proposition d’incrustation";
            highlightJump(card, null);
            return;
        }
        var motion = item.type === "motion" || !!item.vue;
        var hasFigure = !!item.image && !motion;
        layer.className = "incrust-layer" + (hasFigure ? " has-figure" : "") + (motion ? " is-motion" : "");
        var kind = hasFigure ? "Schéma du fascicule" : (motion ? (item.id || "Incrustation") : (item.type === "schema" ? "Petit schéma" : "Mot-clé"));
        var body;
        if (motion) {
            body = motionHtml(item);
        } else if (hasFigure) {
            var imgUrl = new URL(item.image, SCRIPT_SRC).href;
            body = '<img class="incrust-figure" alt="' + escapeHtml(item.ecran || item.schema || "Schéma") + '" src="' + imgUrl + '">';
        } else if (item.type === "schema" && item.schema) {
            body = schemaHtml(item.schema);
        } else {
            body = '<div class="incrust-label">' + escapeHtml(item.ecran || item.schema || "—") + "</div>";
        }
        var extra = (!motion && item.developpe) ? '<div class="incrust-developpe">' + escapeHtml(item.developpe) + "</div>" : "";
        var why = (!motion && !hasFigure && item.pourquoi) ? '<div class="incrust-pourquoi">' + escapeHtml(item.pourquoi) + "</div>" : "";
        panel.innerHTML = (motion ? "" : '<div class="incrust-kicker">' + escapeHtml(kind) + " · " +
            escapeHtml(item.debut) + "–" + escapeHtml(item.fin) + "</div>") + body + extra + why;
        if (now) {
            now.innerHTML = "<strong>" + escapeHtml(item.id || kind) + "</strong> · " +
                escapeHtml(item.debut) + "–" + escapeHtml(item.fin) + " · " +
                escapeHtml(item.ecran || item.schema || "");
        }
        highlightJump(card, item);
    }

    function goToItem(card, item) {
        if (!item) return;
        if (card._incrustPinned === item) {
            card._incrustPinned = null;
            highlightJump(card, currentItem(card._incrustItems || [], card._incrustTime || 0));
            render(card, currentItem(card._incrustItems || [], card._incrustTime || 0), card._incrustTime || 0);
            return;
        }
        card._incrustPinned = item;
        if (!card.classList.contains("is-incrust-on")) {
            card.classList.add("is-incrust-on");
            var toggle = card.querySelector(".incrust-toggle");
            if (toggle) toggle.setAttribute("aria-pressed", "true");
        }
        render(card, item, toSec(item.debut));
        seekTo(card.querySelector("iframe"), toSec(item.debut) + 0.15);
    }

    function buildJumps(card, video) {
        var nav = document.createElement("div");
        nav.className = "incrust-jumps";
        nav.setAttribute("role", "tablist");
        nav.setAttribute("aria-label", "Aller à une proposition d’incrustation");
        video.items.forEach(function (item, i) {
            var b = document.createElement("button");
            b.type = "button";
            b.className = "incrust-jump";
            b.title = (item.id ? item.id + " · " : "") + (item.debut || "") + " — " + labelOf(item);
            b.innerHTML = "<span>" + (idNum(item) || (i + 1)) + "</span> " + escapeHtml(labelOf(item));
            b.addEventListener("click", function () { goToItem(card, item); });
            nav.appendChild(b);
        });
        return nav;
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
            if (!on) {
                card._incrustPinned = null;
                highlightJump(card, null);
                return;
            }
            render(card, card._incrustPinned || currentItem(video.items, card._incrustTime || 0), card._incrustTime || 0);
        });
        var actions = header.querySelector(".video-header-actions");
        if (!actions) {
            actions = document.createElement("div");
            actions.className = "video-header-actions";
            header.appendChild(actions);
        }
        actions.appendChild(btn);
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
        now.insertAdjacentElement("afterend", buildJumps(card, video));
        card._incrustItems = video.items;
        card._incrustTime = 0;
        card._incrustPinned = null;
        render(card, null, 0);
        cards.push(card);
    }

    function applyTime(card, seconds) {
        if (seconds == null || !isFinite(seconds)) return;
        card._incrustTime = seconds;
        var items = card._incrustItems || [];
        var live = currentItem(items, seconds);
        if (card._incrustPinned) {
            var idx = itemIndex(items, card._incrustPinned);
            var win = idx >= 0 ? windowOf(items, idx) : null;
            if (win && seconds >= win.start && seconds <= win.end) {
                card._incrustPinned = null;
            } else if (card.classList.contains("is-incrust-on")) {
                render(card, card._incrustPinned, seconds);
                return;
            }
        }
        if (!card.classList.contains("is-incrust-on")) return;
        render(card, live, seconds);
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
