(function (global) {
    var MAX_ATTEMPTS = 3;

    function el(tag, attrs, children) {
        var node = document.createElement(tag);
        attrs = attrs || {};
        Object.keys(attrs).forEach(function (key) {
            if (key === "className") node.className = attrs[key];
            else if (key === "text") node.textContent = attrs[key];
            else if (key === "html") node.innerHTML = attrs[key];
            else if (key.indexOf("on") === 0 && typeof attrs[key] === "function") node.addEventListener(key.slice(2).toLowerCase(), attrs[key]);
            else if (attrs[key] !== undefined && attrs[key] !== null) node.setAttribute(key, attrs[key]);
        });
        (children || []).forEach(function (child) {
            if (child) node.appendChild(child);
        });
        return node;
    }

    function shuffle(list) {
        var copy = list.slice();
        for (var i = copy.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var tmp = copy[i];
            copy[i] = copy[j];
            copy[j] = tmp;
        }
        return copy;
    }

    function renderMeta(item) {
        return el("div", { className: "eval-meta" }, [
            el("span", { className: "eval-chip", text: "Objectif · " + item.objectif }),
            el("span", { className: "eval-chip", text: "Bloom · " + item.bloom }),
            el("span", { className: "eval-chip", text: "Mécanisme · " + item.mecanisme }),
            el("span", { className: "eval-chip", text: "Dispositif · " + item.dispositif }),
            el("span", { className: "eval-chip", text: "Fonction · " + item.fonction })
        ]);
    }

    function renderItem(host, item, kind, onDone) {
        var attempts = 0;
        var selected = -1;
        var locked = false;
        var options = shuffle(item.options);
        var attemptLabel = el("div", { className: "eval-attempts", text: "3 tentatives" });
        var feedback = el("div", { className: "eval-feedback" });
        feedback.hidden = true;
        var buttons = [];

        function mark(correct) {
            buttons.forEach(function (btn, idx) {
                btn.disabled = true;
                if (options[idx].correct) btn.classList.add("is-correct");
                else if (idx === selected && !correct) btn.classList.add("is-wrong");
            });
        }

        function submit() {
            if (locked || selected < 0) return;
            attempts += 1;
            var correct = !!options[selected].correct;
            feedback.hidden = false;
            if (correct) {
                locked = true;
                mark(true);
                feedback.className = "eval-feedback is-ok";
                feedback.textContent = item.feedbackOk;
                attemptLabel.textContent = "Bien vu";
                check.disabled = true;
                if (onDone) onDone(true);
                return;
            }
            feedback.className = "eval-feedback is-ko";
            if (attempts >= MAX_ATTEMPTS) {
                locked = true;
                mark(false);
                feedback.textContent = item.feedbackKo + " " + item.feedbackOk;
                attemptLabel.textContent = "Correction affichée";
                check.disabled = true;
                if (onDone) onDone(false);
            } else {
                feedback.textContent = item.feedbackKo + " Il vous reste " + (MAX_ATTEMPTS - attempts) + " tentative(s).";
                attemptLabel.textContent = (MAX_ATTEMPTS - attempts) + " tentative(s) restante(s)";
            }
        }

        var optionWrap = el("div");
        options.forEach(function (opt, idx) {
            var btn = el("button", {
                className: "eval-option",
                type: "button",
                text: opt.text,
                onclick: function () {
                    if (locked) return;
                    selected = idx;
                    buttons.forEach(function (b) { b.classList.remove("is-selected"); });
                    btn.classList.add("is-selected");
                    check.disabled = false;
                }
            });
            buttons.push(btn);
            optionWrap.appendChild(btn);
        });

        var check = el("button", { className: "eval-btn", type: "button", text: "Valider", onclick: submit });
        check.disabled = true;

        host.appendChild(el("section", { className: "eval-block", "data-kind": kind }, [
            el("div", { className: "eval-head" }, [
                el("div", {}, [
                    el("p", { className: "eval-kicker", text: kind === "micro" ? "Après le témoin" : "Après les apports" }),
                    el("h2", { text: kind === "micro" ? "Micro-question" : "Quiz formatif" })
                ]),
                attemptLabel
            ]),
            renderMeta(item),
            el("div", { className: "eval-body" }, [
                el("p", { className: "eval-question", text: item.question }),
                optionWrap,
                el("div", { className: "eval-actions" }, [check]),
                feedback
            ])
        ]));
    }

    function renderQuiz(host, items) {
        if (!items || !items.length) return;
        var index = 0;
        var wrap = el("div");
        host.appendChild(wrap);

        function show() {
            wrap.innerHTML = "";
            renderItem(wrap, items[index], "formative", function () {
                if (index < items.length - 1) {
                    var next = el("button", {
                        className: "eval-btn secondary",
                        type: "button",
                        text: "Question suivante",
                        onclick: function () {
                            index += 1;
                            show();
                            wrap.scrollIntoView({ behavior: "smooth", block: "start" });
                        }
                    });
                    wrap.querySelector(".eval-actions").appendChild(next);
                }
            });
            var nav = el("div", { className: "eval-nav", text: "Question " + (index + 1) + " / " + items.length });
            wrap.querySelector(".eval-body").appendChild(nav);
        }
        show();
    }

    function renderMr(host, cards) {
        (cards || []).forEach(function (card) {
            host.appendChild(el("aside", { className: "mr-card" }, [
                el("p", { className: "mr-kicker", text: "Module Ressources" }),
                el("h2", { text: card.title }),
                el("p", { text: card.why }),
                el("div", { className: "mr-actions" }, [
                    el("a", { className: "mr-btn", href: card.href, target: "_blank", rel: "noopener", html: '<i class="fa-solid fa-arrow-up-right-from-square"></i> Ouvrir la capsule' }),
                    card.siteHref ? el("a", { className: "mr-btn ghost", href: card.siteHref, target: "_blank", rel: "noopener", text: "Ouvrir sur le site" }) : null
                ]),
                el("p", { className: "mr-note", text: "Revenez ensuite ici : une question s’appuie sur cette capsule. Si le lien ne s’ouvre pas dans le LMS, passez par Accueil → Modules Ressources." })
            ]));
        });
    }

    function renderMedia(host, media) {
        if (!media) return;
        if (media.type === "callout") {
            host.appendChild(el("div", { className: "callout-box", html: media.html || media.text }));
            return;
        }
        var body;
        if (media.type === "steps") {
            body = el("div", { className: "media-steps" }, (media.steps || []).map(function (step) {
                return el("div", { className: "media-step" }, [
                    el("strong", { text: step.title }),
                    el("span", { text: step.text })
                ]);
            }));
        } else {
            body = el("ul", { className: "media-list" }, (media.items || []).map(function (line) {
                return el("li", { text: line });
            }));
        }
        host.appendChild(el("section", { className: "media-block" }, [
            el("h2", { text: media.title }),
            media.lead ? el("p", { className: "media-lead", text: media.lead }) : null,
            body
        ]));
    }

    function renderMemory(host, cards) {
        if (!cards || !cards.length) return;
        var grid = el("div", { className: "memory-grid" });
        cards.forEach(function (card, idx) {
            var btn = el("button", {
                className: "memory-card",
                type: "button",
                "aria-pressed": "false",
                onclick: function () {
                    btn.classList.toggle("is-flipped");
                    btn.setAttribute("aria-pressed", btn.classList.contains("is-flipped") ? "true" : "false");
                }
            });
            btn.appendChild(el("div", { className: "memory-inner" }, [
                el("div", { className: "memory-face memory-front" }, [
                    el("small", { text: "Carte " + (idx + 1) }),
                    el("p", { text: card.front })
                ]),
                el("div", { className: "memory-face memory-back" }, [
                    el("small", { text: "À retenir" }),
                    el("p", { text: card.back })
                ])
            ]));
            grid.appendChild(btn);
        });
        host.appendChild(el("section", { className: "eval-block", "data-kind": "memory" }, [
            el("div", { className: "eval-head" }, [
                el("div", {}, [
                    el("p", { className: "eval-kicker", text: "Fin de grain" }),
                    el("h2", { text: "Memory cards" })
                ])
            ]),
            el("div", { className: "eval-body" }, [
                el("p", { className: "memory-hint", text: "Cliquez une carte pour la retourner. Ce sont les messages à emporter, pas une évaluation." }),
                grid
            ])
        ]));
    }

    function renderPlusLoin(host, cards) {
        if (!cards || !cards.length) return;
        var items = cards.map(function (card) {
            return el("li", { className: "plus-loin-item" }, [
                el("div", {}, [
                    el("strong", { text: card.title }),
                    el("span", { text: card.why })
                ]),
                el("a", {
                    href: card.href,
                    target: "_blank",
                    rel: "noopener",
                    html: '<i class="fa-solid fa-arrow-up-right-from-square"></i> Ouvrir'
                })
            ]);
        });
        host.appendChild(el("aside", { className: "plus-loin" }, [
            el("p", { className: "plus-loin-kicker", text: "Module Ressources" }),
            el("h2", { text: "Pour aller plus loin !" }),
            el("p", { className: "plus-loin-lead", text: "Ces capsules approfondissent le grain. Elles ne sont pas exigées pour valider." }),
            el("ul", { className: "plus-loin-list" }, items)
        ]));
    }

    function mediaWhen(media, when) {
        if (!media) return null;
        if ((media.when || "after-t") === when) return media;
        return null;
    }

    function mount(grainId) {
        var bank = (global.EVAL_BANK || {})[grainId];
        if (!bank) return;
        var afterT = document.getElementById("eval-after-t");
        var afterE = document.getElementById("eval-after-e");
        var memory = document.getElementById("eval-memory");
        if (afterT) {
            renderMedia(afterT, mediaWhen(bank.media, "after-t"));
            if (bank.micro) renderItem(afterT, bank.micro, "micro");
            if (bank.mrEarly) renderMr(afterT, bank.mrEarly);
        }
        if (afterE) {
            renderMedia(afterE, mediaWhen(bank.media, "after-e"));
            if (bank.mediaExtra) renderMedia(afterE, bank.mediaExtra);
            renderMr(afterE, bank.mr);
            renderQuiz(afterE, bank.quiz);
        }
        if (memory) {
            renderMemory(memory, bank.memory);
            renderPlusLoin(memory, bank.plusLoin);
        }
    }

    global.EvalApp = { mount: mount };
})(window);
