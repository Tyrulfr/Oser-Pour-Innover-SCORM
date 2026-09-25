window.EVAL_BANK = (function () {
    var SITE = "https://tyrulfr.github.io/Oser-Pour-Innover-SCORM/modules/module-r-avancement/pages/";

    function mr(file, title, why) {
        return {
            title: title,
            why: why,
            href: "../../module-r-avancement/pages/" + file,
            siteHref: SITE + file
        };
    }

    return {
        grain_t1_pourquoi_oser: {
            micro: {
                objectif: "Repérer que l’innovation peut naître de plusieurs chemins",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "D’après la chorale, une innovation issue de la recherche naît surtout…",
                options: [
                    { text: "De chemins différents : un pas de côté, un besoin, une rencontre, des années de recherche.", correct: true },
                    { text: "D’un unique moment Eurêka, toujours le même.", correct: false },
                    { text: "Uniquement de la création immédiate d’une start-up.", correct: false }
                ],
                feedbackOk: "Sylvia parle d’un pas de côté, Muriel d’un besoin, d’autres d’une rencontre : il n’y a pas un seul schéma.",
                feedbackKo: "La chorale ne raconte pas un unique Eurêka, ni l’obligation de créer une entreprise."
            },
            quiz: [
                {
                    objectif: "Distinguer technologie et innovation",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour Bernard, une technologie remarquable devient une innovation quand…",
                    options: [
                        { text: "Elle rencontre un besoin important auquel elle répond mieux que les solutions existantes.", correct: true },
                        { text: "Elle a donné lieu à suffisamment de publications.", correct: false },
                        { text: "Elle est protégée par un brevet, quelle que soit l’utilité.", correct: false }
                    ],
                    feedbackOk: "Bernard le dit clairement : une techno n’est pas encore une innovation ; elle le devient au contact d’un besoin.",
                    feedbackKo: "Le brevet ou les publications peuvent exister sans qu’il y ait encore innovation."
                },
                {
                    objectif: "Reconnaître le socle commun des cinq récits",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Selon Bernard, le point commun des cinq témoignages est…",
                    options: [
                        { text: "Un potentiel scientifique ou technologique développé longtemps, puis rapproché d’un besoin.", correct: true },
                        { text: "La décision de quitter définitivement la recherche.", correct: false },
                        { text: "Un financement obtenu avant même le premier résultat.", correct: false }
                    ],
                    feedbackOk: "Le socle, ce sont des années de recherche ensuite mises en regard d’un besoin.",
                    feedbackKo: "Personne ne dit qu’il faut quitter la recherche, ni que l’argent précède le résultat."
                },
                {
                    objectif: "Savoir quoi faire d’une intuition de domaine",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Le domaine d’application est pressenti, mais le problème précis reste flou. Que faire selon Bernard ?",
                    options: [
                        { text: "Confronter l’intuition au terrain : qui est concerné, quelles difficultés, dans quelles situations.", correct: true },
                        { text: "Déposer un brevet avant d’avoir formulé le problème.", correct: false },
                        { text: "Attendre qu’un industriel vienne de lui-même proposer le cahier des charges.", correct: false }
                    ],
                    feedbackOk: "L’intuition donne une direction ; elle doit être confrontée au terrain.",
                    feedbackKo: "Bernard insiste sur les personnes, les difficultés et les situations — pas sur l’attente."
                }
            ],
            memory: [
                { front: "Une innovation naît-elle d’un seul Eurêka ?", back: "Non. Plusieurs chemins : pas de côté, besoin, rencontre, années de recherche." },
                { front: "Techno remarquable = innovation ?", back: "Non. Elle le devient en rencontrant un besoin, mieux que les solutions existantes." },
                { front: "Que faire d’une intuition de domaine ?", back: "La confronter au terrain : qui, quelles difficultés, quelles situations." }
            ],
            plusLoin: [
                mr("grain1.html", "1.1 — Définition & fondamentaux", "Clarifier ce qu’est une innovation : processus et résultat, nouveauté et valeur."),
                mr("grain4.html", "1.4 — Le nuage de vocabulaire", "Invention vs innovation : le lexique qui évite de prendre une techno pour une innovation."),
                mr("grain18.html", "3.1 — Les 3 stratégies", "Need Seeker, Market Reader, Technology Driver : d’où part une innovation.")
            ]
        },

        grain_t2_recherche_innovation: {
            micro: {
                objectif: "Distinguer idée intéressante et besoin validé",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Yann a consulté des rapports et des outils d’IA. Pourquoi cela ne suffit-il pas, d’après la chorale ?",
                options: [
                    { text: "Il faut ensuite aller chercher de vrais industriels, les futurs clients.", correct: true },
                    { text: "Parce que les rapports d’industriels n’ont aucune valeur.", correct: false },
                    { text: "Parce que seule une publication scientifique valide un besoin.", correct: false }
                ],
                feedbackOk: "Yann le dit : la vision globale aide, mais à la fin il faut des vrais industriels.",
                feedbackKo: "Les rapports existent et aident ; ce qui manque, c’est la confrontation aux acteurs."
            },
            media: {
                when: "after-t",
                type: "steps",
                title: "De la techno au problème",
                lead: "E2 n’est pas encore disponible. Ce schéma porte le raccord : ce n’est pas la techno qui est le problème.",
                steps: [
                    { title: "1. Techno", text: "Ce que le laboratoire sait faire." },
                    { title: "2. Qui / où", text: "Utilisateur, client, situation d’usage." },
                    { title: "3. Problème", text: "La difficulté concrète, pas la solution." },
                    { title: "4. Preuve", text: "Ce qui montre que le besoin existe vraiment." }
                ]
            },
            mr: [mr("grain10.html", "2.4 — Cadrage du problème", "Pour passer d’une techno à un problème, on cadre d’abord (Double diamant), on ne commence pas par prototyper la solution.")],
            quiz: [
                {
                    objectif: "Valider un besoin sur le terrain",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour vérifier qu’un besoin existe, la chorale insiste surtout sur…",
                    options: [
                        { text: "Rencontrer les acteurs et futurs clients, pas seulement lire des rapports.", correct: true },
                        { text: "Multiplier les dépôts de brevets avant toute discussion.", correct: false },
                        { text: "Attendre la fin de la thèse pour sortir du laboratoire.", correct: false }
                    ],
                    feedbackOk: "Sylvia se pose l’usage dès le début ; Yann va chercher les industriels.",
                    feedbackKo: "Le besoin ne se valide pas uniquement sur papier."
                },
                {
                    objectif: "Cadrer le problème avant de le résoudre",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration (capsule MR)",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Dans le Double diamant du module Ressources, on commence par…",
                    options: [
                        { text: "Cadrer le problème (setting), puis seulement le résoudre (solving).", correct: true },
                        { text: "Prototype immédiat, puis on verra quel problème il résout.", correct: false },
                        { text: "Choisir un modèle économique avant d’avoir un utilisateur.", correct: false }
                    ],
                    feedbackOk: "Le premier diamant cadre le problème ; le second cherche la solution.",
                    feedbackKo: "Si cette question résiste, rouvrez la capsule 2.4 — Cadrage du problème."
                }
            ],
            memory: [
                { front: "Une étude bibliographique suffit-elle ?", back: "Non. Il faut aller voir de vrais industriels / utilisateurs." },
                { front: "Par quoi commencer : un problème ou une solution ?", back: "Cadrer le problème d’abord (Double diamant), puis le résoudre." },
                { front: "La techno est-elle déjà le problème ?", back: "Non. Le problème se formule côté usage, situation et preuve." }
            ],
            plusLoin: [
                mr("grain18.html", "3.1 — Les 3 stratégies", "Technology Driver vs Need Seeker : d’où vous partez change la façon de cadrer le problème."),
                mr("grain1.html", "1.1 — Définition & fondamentaux", "Revenir à la différence entre nouveauté technique et valeur créée.")
            ]
        },

        grain_t3_besoin_poc: {
            micro: {
                objectif: "Accepter qu’un besoin se précise (et parfois pivote)",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Jean-Jacques raconte une étude de marché et des rencontres utilisateurs. Qu’est-ce que cela a produit ?",
                options: [
                    { text: "Un pivot : adapter la technologie à un autre besoin, clairement défini.", correct: true },
                    { text: "L’abandon définitif du projet.", correct: false },
                    { text: "La preuve que l’étude de marché est inutile si on a déjà une techno.", correct: false }
                ],
                feedbackOk: "Ils ont modifié la cible : un pivot, pas un arrêt.",
                feedbackKo: "Le récit montre un ajustement de cible, pas un échec ni un refus du terrain."
            },
            media: {
                when: "after-t",
                type: "steps",
                title: "Niveaux de preuve",
                lead: "E4 n’est pas encore disponible. L’escalier pose le vocabulaire ; le détail TRL est dans le module Ressources.",
                steps: [
                    { title: "Résultat", text: "Ce que le labo a montré." },
                    { title: "POC", text: "Preuve que ça peut marcher." },
                    { title: "Prototype", text: "Objet testable, encore imparfait." },
                    { title: "MVP", text: "Produit minimal utilisable par un client." }
                ]
            },
            mr: [mr("grain19.html", "2.9 — Les échelles de maturité", "E4 devait porter POC / prototype / MVP / TRL. Cette capsule le fait déjà : situez votre niveau de preuve, puis revenez.")],
            quiz: [
                {
                    objectif: "Interpréter un pivot",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour Virginia, un pivot c’est…",
                    options: [
                        { text: "Une décision, pas un échec.", correct: true },
                        { text: "La preuve que le projet n’avait aucun potentiel.", correct: false },
                        { text: "Un simple changement de logo ou de nom.", correct: false }
                    ],
                    feedbackOk: "Virginia : « un pivot, pas un échec, une décision ». L’équipe a ajusté la techno vers un autre besoin.",
                    feedbackKo: "Le pivot dont elle parle change la cible, ce n’est pas un échec ni un habillage."
                },
                {
                    objectif: "Savoir où se trouve le vrai problème de marché",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Selon Virginia, le « vrai problème de marché »…",
                    options: [
                        { text: "Ne se trouve jamais au banc d’essai.", correct: true },
                        { text: "Se lit uniquement dans les publications du laboratoire.", correct: false },
                        { text: "Est toujours identique d’une filière à l’autre.", correct: false }
                    ],
                    feedbackOk: "La solution la plus élégante ne vaut rien si personne, sur le terrain, n’en a besoin sous cette forme.",
                    feedbackKo: "Loïc et Virginia insistent : les exigences changent selon les acteurs, pas au banc d’essai."
                },
                {
                    objectif: "Situer un niveau de maturité (TRL)",
                    bloom: "Appliquer",
                    mecanisme: "Récupération (capsule MR)",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Dans la grille TRL du module Ressources, la zone la plus risquée (« vallée de la mort ») se situe généralement…",
                    options: [
                        { text: "TRL 4 à 6", correct: true },
                        { text: "TRL 1 à 3", correct: false },
                        { text: "TRL 7 à 9", correct: false }
                    ],
                    feedbackOk: "C’est le message de la capsule 2.9 : le risque se concentre souvent entre TRL 4 et 6.",
                    feedbackKo: "Rouvrez « Les échelles de maturité » : la vallée de la mort n’est ni le tout début, ni la fin."
                }
            ],
            memory: [
                { front: "Un pivot, c’est un échec ?", back: "Non. C’est une décision : on ajuste la cible et parfois la techno." },
                { front: "Où trouve-t-on le vrai problème de marché ?", back: "Jamais au seul banc d’essai : sur le terrain, auprès des acteurs." },
                { front: "À quoi sert le TRL ici ?", back: "À nommer son niveau de preuve et la prochaine incertitude à lever." }
            ],
            plusLoin: [
                mr("grain3.html", "1.3 — L’innovation est un processus", "Le dérisquage n’est pas un saut : c’est une suite d’étapes que l’on pilote."),
                mr("grain5.html", "1.5 — La chaîne de valeur", "Associer un niveau de preuve aux flux de financement et de valeur.")
            ]
        },

        grain_t4_idee_freins_leviers: {
            micro: {
                objectif: "Protéger avant de communiquer",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Dans la chorale, dès qu’il y a une idée, le premier geste évoqué par Jean-Jacques est…",
                options: [
                    { text: "S’en servir pour rédiger un brevet et protéger l’innovation.", correct: true },
                    { text: "La présenter tout de suite en congrès pour avoir des retours.", correct: false },
                    { text: "Créer la start-up avant toute protection.", correct: false }
                ],
                feedbackOk: "Idée, puis brevet pour protéger, en parallèle de l’expérience technique.",
                feedbackKo: "Le récit commence par protéger, pas par divulguer ni par créer trop tôt."
            },
            quiz: [
                {
                    objectif: "Anticiper la divulgation",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Avant de diffuser largement un résultat (article, congrès), Stéphanie recommande…",
                    options: [
                        { text: "De se poser la question de la valorisation, via une déclaration d’invention.", correct: true },
                        { text: "De publier d’abord, la protection viendra après si besoin.", correct: false },
                        { text: "De ne plus jamais communiquer, même après dépôt.", correct: false }
                    ],
                    feedbackOk: "Une communication publique peut fermer des portes. La déclaration d’invention existe pour ça.",
                    feedbackKo: "Il ne s’agit pas de se taire pour toujours, mais de ne pas divulguer à l’aveugle."
                },
                {
                    objectif: "Savoir quoi faire avant un colloque",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Vous avez un résultat intéressant et un abstract à envoyer demain. Premier réflexe ?",
                    options: [
                        { text: "En parler au chargé de valorisation (déclaration d’invention).", correct: true },
                        { text: "Envoyer l’abstract tel quel : un abstract n’est jamais une divulgation.", correct: false },
                        { text: "Attendre d’avoir un business plan complet.", correct: false }
                    ],
                    feedbackOk: "Stéphanie : avant de publier, de présenter, de divulguer, prenez le temps d’en parler.",
                    feedbackKo: "Pas besoin d’un dossier fini ; il faut surtout ne pas brûler la nouveauté."
                },
                {
                    objectif: "Oser aller voir la valorisation tôt",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour aller voir son chargé de valorisation, il faut…",
                    options: [
                        { text: "Pouvoir expliquer le résultat, ce qu’il apporte de nouveau, le problème visé, où l’on en est.", correct: true },
                        { text: "Avoir déjà créé l’entreprise et levé des fonds.", correct: false },
                        { text: "Avoir réponse à toutes les questions juridiques.", correct: false }
                    ],
                    feedbackOk: "Stéphanie : inutile d’avoir tout construit ; ces informations suffisent pour évaluer le potentiel.",
                    feedbackKo: "On ne vient pas avec un projet fini : on vient avec un résultat et des questions."
                }
            ],
            memory: [
                { front: "Que faire avant de parler publiquement ?", back: "Se poser la valorisation. Outil : déclaration d’invention." },
                { front: "Protéger, est-ce mettre la recherche en pause ?", back: "Non. Brevet et expériences peuvent avancer en parallèle." },
                { front: "Faut-il tout savoir avant d’aller en valorisation ?", back: "Non. Expliquer le résultat, le nouveau, le problème, l’avancement." }
            ],
            plusLoin: [
                mr("grain3.html", "1.3 — L’innovation est un processus", "Protéger avant de divulguer fait partie du processus, ça ne le met pas en pause."),
                mr("grain5.html", "1.5 — La chaîne de valeur", "Voir où se situent protection et premier financement, du labo vers l’usage.")
            ]
        },

        grain_t5_protection_valorisation: {
            micro: {
                objectif: "Relier PI et valeur",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Pour Yann, protéger la propriété intellectuelle est décisif parce que…",
                options: [
                    { text: "C’est sur elle que repose une grande part de la valeur de la recherche ou de la future start-up.", correct: true },
                    { text: "Sans brevet, il est interdit de publier.", correct: false },
                    { text: "L’INPI finance automatiquement tous les projets brevetés.", correct: false }
                ],
                feedbackOk: "Yann : la PI fonde la valeur au début de la boîte, et protège aussi face à des industriels.",
                feedbackKo: "La chorale parle de valeur et de protection, pas d’une interdiction de publier."
            },
            quiz: [
                {
                    objectif: "Choisir brevet et/ou secret",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Une partie de la techno serait indétectable chez un concurrent. Selon Loïc et Stanislas…",
                    options: [
                        { text: "La garder en secret ; l’autre partie peut être brevetée.", correct: true },
                        { text: "Tout breveter, même ce qu’on ne pourra jamais prouver.", correct: false },
                        { text: "Tout publier pour créer une antériorité mondiale.", correct: false }
                    ],
                    feedbackOk: "Si on ne peut pas démontrer la copie, le secret est plus sûr. Les deux outils sont complémentaires.",
                    feedbackKo: "Loïc : tout n’était pas à divulguer, même si tout était potentiellement brevetable."
                },
                {
                    objectif: "Comprendre l’effet d’une publication",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Vous publiez l’invention avant tout dépôt. Conséquence selon Stanislas ?",
                    options: [
                        { text: "La nouveauté est détruite : plus aucun dépôt de brevet n’est possible.", correct: true },
                        { text: "Le brevet est automatiquement accordé, la publication sert de preuve.", correct: false },
                        { text: "Rien : on a 10 ans pour déposer après publication.", correct: false }
                    ],
                    feedbackOk: "Protéger avant d’en parler publiquement : la publication tue la nouveauté.",
                    feedbackKo: "Ce n’est pas une preuve pour obtenir un brevet : c’est souvent ce qui l’empêche."
                },
                {
                    objectif: "Comprendre la liberté d’exploitation",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "L’étude Freedom to Operate (FTO) sert à…",
                    options: [
                        { text: "Vérifier que l’invention ne dépend pas d’un brevet tiers.", correct: true },
                        { text: "Remplacer le dépôt de brevet.", correct: false },
                        { text: "Mesurer uniquement la taille du marché.", correct: false }
                    ],
                    feedbackOk: "Si la techno repose sur un brevet tiers, il faudra peut-être une licence ou revoir le modèle.",
                    feedbackKo: "La FTO n’est ni un titre de PI, ni une étude de marché."
                }
            ],
            memory: [
                { front: "Brevet ou secret ?", back: "Souvent les deux. Secret si la copie est indétectable." },
                { front: "Publier avant de déposer ?", back: "La publication détruit la nouveauté. Plus de brevet possible." },
                { front: "À quoi sert la FTO ?", back: "Savoir si l’on peut exploiter sans dépendre d’un brevet tiers." }
            ],
            plusLoin: [
                mr("grain5.html", "1.5 — La chaîne de valeur", "La PI est un actif : elle circule avec la valeur, du laboratoire au marché."),
                mr("grain4.html", "1.4 — Le nuage de vocabulaire", "Nommer clairement invention, innovation, secret, brevet.")
            ]
        },

        grain_t6_transfert_licensing: {
            micro: {
                objectif: "Se poser tôt la voie de transfert",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Muriel insiste pour se poser dès le début licensing vs création d’entreprise. Pourquoi ?",
                options: [
                    { text: "Ce choix conditionne les étapes de recherche et de maturation.", correct: true },
                    { text: "La loi impose de créer une entreprise avant toute licence.", correct: false },
                    { text: "Le licensing n’existe que pour les logiciels.", correct: false }
                ],
                feedbackOk: "Ce n’est pas une question de statut juridique en fin de course : ça oriente le travail tout de suite.",
                feedbackKo: "Muriel et Virginia : se poser tôt, pas au moment de choisir les statuts."
            },
            mediaExtra: {
                type: "list",
                title: "Ne pas confondre : PACTE / concours de l’agent",
                lead: "Hors quiz. Si vous êtes agent public, le cadre n’est pas celui d’i-Lab.",
                items: [
                    "Le concours scientifique de l’agent et la loi PACTE concernent le cumul / l’essaimage des personnels.",
                    "Ce n’est pas le concours i-Lab, ni le « pacte d’associés » entre fondateurs (autre grain).",
                    "Pour le détail, parlez-en à votre service de valorisation."
                ]
            },
            quiz: [
                {
                    objectif: "Distinguer licence et création",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Dans la licence, selon Virginia…",
                    options: [
                        { text: "L’établissement reste propriétaire du brevet ou du savoir-faire ; l’industriel paie une redevance.", correct: true },
                        { text: "L’industriel devient automatiquement propriétaire du brevet.", correct: false },
                        { text: "Il n’y a jamais de contrepartie financière.", correct: false }
                    ],
                    feedbackOk: "Licence = droit d’exploiter, établissement propriétaire. Création d’entreprise : on porte soi-même la mise sur le marché.",
                    feedbackKo: "La licence n’est pas un transfert automatique de propriété."
                },
                {
                    objectif: "Choisir une voie selon le projet",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Une innovation qui s’insère dans un procédé industriel déjà existant se prête plutôt…",
                    options: [
                        { text: "À la licence.", correct: true },
                        { text: "Toujours à la création d’entreprise, sans alternative.", correct: false },
                        { text: "À l’absence de tout contrat.", correct: false }
                    ],
                    feedbackOk: "Virginia : insertion dans un existant → licence ; rupture sans marché constitué → plus souvent création.",
                    feedbackKo: "Le troisième critère reste ce que vous avez envie de porter — mais la typologie oriente."
                },
                {
                    objectif: "Comprendre ce qu’est une licence",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour Soizic, une licence…",
                    options: [
                        { text: "Concède l’exploitation (contrat de louage) sans transférer la propriété du titre.", correct: true },
                        { text: "Est toujours mondiale, tous domaines, sans clause.", correct: false },
                        { text: "Remplace le contrat de confidentialité.", correct: false }
                    ],
                    feedbackOk: "Exclusive ou non, sur un territoire et un domaine. La propriété du titre reste au concédant.",
                    feedbackKo: "Avant de discuter, Soizic rappelle d’abord le contrat de confidentialité — ce n’est pas la licence."
                }
            ],
            memory: [
                { front: "Licence ou start-up : quand se le demander ?", back: "Dès le début : ça conditionne recherche et maturation." },
                { front: "Qui reste propriétaire en licence ?", back: "L’établissement. L’industriel exploite contre redevance." },
                { front: "Une licence transfère-t-elle le brevet ?", back: "Non. C’est un louage du droit d’exploiter, souvent borné." }
            ],
            plusLoin: [
                mr("grain5.html", "1.5 — La chaîne de valeur", "Licence ou création d’entreprise : deux façons de faire circuler la valeur."),
                mr("grain2.html", "1.2 — Sur quoi innover ?", "Le champ n’est pas que le produit : service, organisation, procédé.")
            ]
        },

        grain_t7_accompagnement: {
            micro: {
                objectif: "Accepter de ne pas avancer seul",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "D’après Muriel et Loïc, plus le projet est ambitieux…",
                options: [
                    { text: "Plus on a besoin d’acteurs (labos, incubateurs, financeurs) : on n’avance pas seul.", correct: true },
                    { text: "Plus il faut tout faire soi-même pour rester crédible.", correct: false },
                    { text: "Moins les investisseurs regardent l’équipe.", correct: false }
                ],
                feedbackOk: "Muriel liste l’écosystème ; Jean-Jacques : les investisseurs parient sur une équipe humaine.",
                feedbackKo: "La chorale dit l’inverse : besoin d’aide, et les investisseurs regardent l’équipe, pas seulement la techno."
            },
            quiz: [],
            memory: [
                { front: "Peut-on avancer seul ?", back: "Rarement. Plus le projet est ambitieux, plus il faut des acteurs." },
                { front: "Sur quoi parient les investisseurs, selon Jean-Jacques ?", back: "Sur une équipe humaine complémentaire, pas sur la seule techno." },
                { front: "À quoi servent Design Spot / fablabs (E13bis) ?", back: "Passer de l’idée à une preuve concrète et travailler l’usage tôt." }
            ],
            plusLoin: [
                mr("grain5.html", "1.5 — La chaîne de valeur", "Situer incubateurs, SATT et financeurs dans le parcours du labo à l’usage."),
                mr("grain9.html", "2.3 — Le front-end innovation", "L’accompagnement sert surtout au flou du début, pas à tout faire seul.")
            ]
        },

        grain_t8_financements: {
            micro: {
                objectif: "Ne pas créer trop tôt",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Jean-Jacques met en garde : il ne faut pas créer trop tôt, parce que…",
                options: [
                    { text: "Beaucoup de financements sont anti-création : une fois créé, on n’y est plus éligible.", correct: true },
                    { text: "Il est interdit de créer une entreprise tant qu’on est chercheur.", correct: false },
                    { text: "Les aides n’existent qu’après le premier chiffre d’affaires.", correct: false }
                ],
                feedbackOk: "Étapes anti-création puis post-création. Créer trop tôt ferme des portes d’aides.",
                feedbackKo: "La chorale parle d’éligibilité des aides, pas d’une interdiction d’entreprendre."
            },
            media: {
                when: "after-t",
                type: "steps",
                title: "Frise entendue dans la chorale",
                lead: "Les mots viennent de T8, pas d’un expert encore manquant.",
                steps: [
                    { title: "Anti-création", text: "Valorisation univ. / CNRS, Pockin Lab, prématuration." },
                    { title: "Marches", text: "i-Lab, recrutement, preuves plus solides." },
                    { title: "Création", text: "On bascule : certaines aides se ferment." },
                    { title: "Après", text: "Investisseurs ou clients." }
                ]
            },
            mr: [mr("grain5.html", "1.5 — La chaîne de valeur", "E14 n’est pas là. Cette capsule montre déjà les flux parallèles de financement et de création de valeur, du labo vers l’usage.")],
            quiz: [
                {
                    objectif: "Choisir le moment de création",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Créer trop tôt, concrètement, c’est…",
                    options: [
                        { text: "Perdre l’éligibilité à des financements anti-création.", correct: true },
                        { text: "Gagner automatiquement plus d’aides publiques.", correct: false },
                        { text: "Obligatoire pour déposer un brevet.", correct: false }
                    ],
                    feedbackOk: "Jean-Jacques : beaucoup d’aides disparaissent dès que la société existe.",
                    feedbackKo: "Le brevet n’exige pas une société ; trop tôt peut coûter des aides."
                },
                {
                    objectif: "Relier financement et création de valeur",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration (capsule MR)",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "D’après la chaîne de valeur du module Ressources, innover ce n’est pas seulement inventer : c’est…",
                    options: [
                        { text: "Faire circuler valeur et financements, du laboratoire jusqu’à l’usage.", correct: true },
                        { text: "S’arrêter au dépôt de brevet.", correct: false },
                        { text: "Attendre que le marché vienne tout seul au laboratoire.", correct: false }
                    ],
                    feedbackOk: "La capsule 1.5 superpose flux de valeur et flux de financement.",
                    feedbackKo: "Si c’est flou, rouvrez « La chaîne de valeur » puis revenez."
                }
            ],
            memory: [
                { front: "Pourquoi ne pas créer trop tôt ?", back: "Des aides anti-création deviennent inaccessibles." },
                { front: "Pockin Lab, dans la chorale, sert à quoi ?", back: "Une année pour une preuve de concept, encore lié au labo." },
                { front: "Innover, ce n’est que inventer ?", back: "Non. Il faut aussi faire circuler valeur et financements." }
            ],
            plusLoin: [
                mr("grain19.html", "2.9 — Les échelles de maturité", "Associer un financement au bon niveau de preuve (et à la « vallée de la mort »)."),
                mr("grain3.html", "1.3 — L’innovation est un processus", "Les aides anti-création puis post-création sont des étapes, pas un unique chèque.")
            ]
        },

        grain_t9_partenariats_equipe: {
            micro: {
                objectif: "Aller chercher les compétences qui manquent",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Loïc dit que les scientifiques ne savent pas tout faire (marché, brevetabilité, vente). Que faire ?",
                options: [
                    { text: "Aller chercher des expertises — et pas un profil « business » générique, sans le secteur.", correct: true },
                    { text: "Rester entre scientifiques jusqu’au premier client.", correct: false },
                    { text: "Recruter n’importe quel profil d’école de commerce, le secteur n’importe pas.", correct: false }
                ],
                feedbackOk: "Ils sont allés à la SATT. Un profil business sans vision du secteur agricole n’a pas suffi.",
                feedbackKo: "La chorale valorise l’expertise, mais ancrée dans le métier."
            },
            quiz: [],
            memory: [
                { front: "Faut-il tout savoir faire ?", back: "Non. Aller chercher des experts (marché, PI, finance, vente)." },
                { front: "Un profil business suffit-il ?", back: "Pas s’il ne comprend pas les enjeux du secteur." },
                { front: "Qui compose l’entourage utile ?", back: "Noyau fondateur, conseils, comité scientifique, réseau." }
            ],
            plusLoin: [
                mr("grain10.html", "2.4 — Cadrage du problème", "Une équipe se construit autour d’un problème partagé, pas seulement de profils."),
                mr("grain12.html", "2.6 — La méthode des personas", "Clarifier qui est concerné aide à choisir les compétences à aller chercher.")
            ]
        },

        grain_t10_enrichir_langage: {
            micro: {
                objectif: "Adapter son langage à l’interlocuteur",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Pour parler à des partenaires non académiques, Yann a dû…",
                options: [
                    { text: "Parler bénéfices et gains pour l’interlocuteur, plutôt que de seuls termes techniques.", correct: true },
                    { text: "Ajouter encore plus de jargon scientifique pour paraître crédible.", correct: false },
                    { text: "Renoncer à tout article ou pitch hors laboratoire.", correct: false }
                ],
                feedbackOk: "IA / jumeau numérique parlaient aux scientifiques ; les décideurs entendent ROI et bénéfice.",
                feedbackKo: "Adapter, ce n’est pas se taire : c’est changer de posture et de vocabulaire."
            },
            mr: [mr("grain4.html", "1.4 — Le nuage de vocabulaire", "E18 n’est pas encore là. Cette capsule travaille déjà le lexique projet : invention ≠ innovation, s’adapter à qui vous écoute.")],
            quiz: [
                {
                    objectif: "Choisir les mots qui donnent envie de recontacter",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour un décideur industriel, Yann remplace « intelligence artificielle / jumeau numérique » par…",
                    options: [
                        { text: "Retour sur investissement et bénéfice concret.", correct: true },
                        { text: "Une liste plus longue d’algorithmes.", correct: false },
                        { text: "Un silence complet sur ce que fait la solution.", correct: false }
                    ],
                    feedbackOk: "La personne se focalise sur ce que ça lui apporte, pas sur la solution technique.",
                    feedbackKo: "Il ne s’agit pas d’effacer le projet, mais de parler valeur."
                },
                {
                    objectif: "Comprendre comment s’apprend ce langage",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration (T + MR)",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Adapter son vocabulaire, d’après Muriel et le module Ressources…",
                    options: [
                        { text: "Ça s’apprend en discutant et en se formant ; et invention n’est pas encore innovation.", correct: true },
                        { text: "Ça se décide seul, une fois pour toutes, devant une feuille.", correct: false },
                        { text: "C’est inutile : le bon mot scientifique suffit toujours.", correct: false }
                    ],
                    feedbackOk: "Muriel : ça s’inculque en discutant. La capsule 1.4 rappelle qu’invention ≠ innovation.",
                    feedbackKo: "Ni solitaire, ni optionnel : le lexique se travaille avec les autres."
                }
            ],
            memory: [
                { front: "Que changer dans son discours ?", back: "Bénéfices et gains pour l’autre, pas seulement la techno." },
                { front: "Comment s’apprend ce langage ?", back: "En discutant, en se formant (incubateur, SATT, HEC…)." },
                { front: "Invention = innovation ?", back: "Non. L’innovation implique valeur et usage, pas seulement du nouveau." }
            ],
            plusLoin: [
                mr("grain1.html", "1.1 — Définition & fondamentaux", "Le bon mot change selon que l’on parle de nouveauté ou de valeur."),
                mr("grain11.html", "2.5 — Design Thinking : principes", "Empathie et test : le langage se cale sur l’interlocuteur, pas sur le labo.")
            ]
        },

        grain_t11_evolution_metier: {
            media: {
                when: "after-t",
                type: "callout",
                html: "Concilier, pas choisir. On peut enrichir le métier de chercheur sans le renier."
            },
            micro: {
                objectif: "Oser un engagement compatible avec la recherche",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Quel conseil traverse la chorale de T11 ?",
                options: [
                    { text: "Y aller : l’expérience rend visible l’utilité de la recherche, pour soi et pour les autres.", correct: true },
                    { text: "Il faut quitter le laboratoire pour que le projet compte.", correct: false },
                    { text: "L’entrepreneuriat n’apporte rien au métier de chercheur.", correct: false }
                ],
                feedbackOk: "Muriel : ne pas hésiter. Jean-Jacques : voir une application concrète après 35 ans. Loïc cumule les casquettes.",
                feedbackKo: "Les récits parlent d’enrichir le métier, pas de le quitter."
            },
            quiz: [
                {
                    objectif: "Casser le mythe du « né entrepreneur »",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "« N’est-on entrepreneur ? » Pascal répond…",
                    options: [
                        { text: "Non. Il n’y a pas un profil type ; les compétences s’apprennent.", correct: true },
                        { text: "Oui : sans talent inné, inutile d’essayer.", correct: false },
                        { text: "Oui, mais seulement après une école de commerce.", correct: false }
                    ],
                    feedbackOk: "Jean-Jacques apprenait « la langue de l’entrepreneuriat » comme l’anglais : ça s’apprend.",
                    feedbackKo: "Pascal écarte le profil inné et les histoires trop lisses."
                },
                {
                    objectif: "Voir des formes compatibles avec le métier",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "S’engager dans un projet, d’après Bernard, c’est…",
                    options: [
                        { text: "Pas forcément une reconversion : des formes compatibles existent (ex. comité scientifique).", correct: true },
                        { text: "Toujours abandonner l’enseignement et la recherche.", correct: false },
                        { text: "Incompatible avec toute impartialité académique.", correct: false }
                    ],
                    feedbackOk: "Loïc reste enseignant-chercheur et siège au comité scientifique. Ce n’est pas une rupture obligatoire.",
                    feedbackKo: "Bernard : enrichir le métier sans le renier, en conciliant les casquettes."
                },
                {
                    objectif: "Nommer ce qu’il faut concilier",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Parmi les tensions à concilier, Bernard cite notamment…",
                    options: [
                        { text: "Liberté académique et protection de la propriété intellectuelle.", correct: true },
                        { text: "L’obligation de choisir entre publier et enseigner.", correct: false },
                        { text: "L’interdiction de tout accompagnement institutionnel.", correct: false }
                    ],
                    feedbackOk: "Il parle de cadre clair, d’accompagnement, et de PI qui doit s’articuler avec la liberté académique.",
                    feedbackKo: "Ce n’est pas « tout abandonner » : c’est tenir ensemble plusieurs exigences."
                }
            ],
            memory: [
                { front: "Faut-il naître entrepreneur ?", back: "Non. Les compétences s’apprennent, par tâtonnements." },
                { front: "Doit-on quitter la recherche ?", back: "Non. On peut concilier : comité scientifique, double casquette." },
                { front: "Que rend visible l’innovation ?", back: "L’utilité de la recherche — Muriel parle d’intégrateur social." }
            ],
            plusLoin: [
                mr("grain1.html", "1.1 — Définition & fondamentaux", "Innover n’oblige pas à quitter la recherche : c’est un processus et un résultat."),
                mr("grain3.html", "1.3 — L’innovation est un processus", "Voir l’engagement comme une suite d’apprentissages, pas une reconversion.")
            ]
        },

        grain_t12_dispositifs_collaborations: {
            micro: {
                objectif: "Voir l’accompagnement comme un moyen, pas une collection de sigles",
                bloom: "Comprendre",
                mecanisme: "Récupération + feedback",
                dispositif: "QCM",
                fonction: "Formative",
                question: "Dans la chorale, l’accompagnement sert surtout à…",
                options: [
                    { text: "Résoudre des problèmes concrets et ajuster le projet, pas à collectionner les dispositifs.", correct: true },
                    { text: "Remplacer toute discussion avec un partenaire.", correct: false },
                    { text: "Éviter d’avoir à se former ou à pitcher.", correct: false }
                ],
                feedbackOk: "Trouver un électronicien, travailler son pitch, ajuster selon les collaborations : du concret.",
                feedbackKo: "Les noms de programmes illustrent ; l’objectif du grain est la collaboration sécurisée."
            },
            media: {
                when: "after-e",
                type: "list",
                title: "Checklist : préparer une collaboration",
                lead: "Pour recaler le grain sur son objectif : collaborer de façon équilibrée et sécurisée.",
                items: [
                    "Qui apporte quoi ? Qui attend quoi ?",
                    "Accord de confidentialité avant de parler du projet.",
                    "État des lieux des connaissances propres de chaque partie.",
                    "PI, publication, conditions de sortie : les écrire."
                ]
            },
            quiz: [
                {
                    objectif: "Distinguer collaboration et prestation",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour Rémi, une collaboration ce n’est pas…",
                    options: [
                        { text: "Une prestation où le client achète simplement des résultats.", correct: true },
                        { text: "Un cadre où chacun apporte et chacun attend quelque chose.", correct: false },
                        { text: "Une mise en relation suivie d’un équilibre des bénéfices.", correct: false }
                    ],
                    feedbackOk: "La mise en relation n’est pas encore la collaboration. Il faut un équilibre : chacun apporte, chacun gagne.",
                    feedbackKo: "Les deux autres phrases décrivent justement la collaboration selon Rémi."
                },
                {
                    objectif: "Sécuriser avant de parler",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Avant de discuter d’un projet avec un tiers, Nelly recommande…",
                    options: [
                        { text: "Un accord de confidentialité et un état des lieux des connaissances propres.", correct: true },
                        { text: "D’envoyer d’abord le manuscrit complet de l’article.", correct: false },
                        { text: "D’attendre la création de la start-up pour tout contractualiser.", correct: false }
                    ],
                    feedbackOk: "NDA pour limiter le vol de savoir-faire ; connaissances propres formalisées pour qu’elles ne soient pas absorbées par le projet.",
                    feedbackKo: "Ce n’est pas après coup : c’est avant toute nouvelle collaboration."
                },
                {
                    objectif: "Reconnaître une collaboration équilibrée",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Une collaboration équilibrée, c’est…",
                    options: [
                        { text: "Chacun apporte, chacun attend, tout le monde y trouve un bénéfice.", correct: true },
                        { text: "Une partie prend toute la PI, l’autre fournit uniquement le travail.", correct: false },
                        { text: "Un échange oral, sans jamais écrire les droits et devoirs.", correct: false }
                    ],
                    feedbackOk: "Rémi : conditions d’entente mutuelle. Nelly : un contrat pour une compréhension commune.",
                    feedbackKo: "L’équilibre se négocie et s’écrit ; ce n’est pas un don unilatéral."
                }
            ],
            memory: [
                { front: "Collaboration = prestation ?", back: "Non. On ne se contente pas d’acheter des résultats." },
                { front: "Premier réflexe avant de parler ?", back: "NDA + connaissances propres formalisées." },
                { front: "À quoi ressemble l’équilibre ?", back: "Chacun apporte, chacun attend, chacun y gagne. Et c’est écrit." }
            ],
            plusLoin: [
                mr("grain10.html", "2.4 — Cadrage du problème", "Une collaboration tient si le besoin de chaque partie est cadré, pas seulement mis en relation."),
                mr("grain11.html", "2.5 — Design Thinking : principes", "Écouter l’autre (empathie) avant de contractualiser.")
            ]
        },

        grain_t13_conclusion: {
            quiz: [
                {
                    objectif: "Partir d’un problème, pas d’une idée",
                    bloom: "Comprendre",
                    mecanisme: "Récupération + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour entreprendre, Yann dit qu’on n’a pas besoin d’une idée : on a besoin…",
                    options: [
                        { text: "D’un problème, d’une problématique terrain.", correct: true },
                        { text: "D’une idée révolutionnaire dès le premier jour.", correct: false },
                        { text: "D’avoir déjà levé des fonds.", correct: false }
                    ],
                    feedbackOk: "L’idée vient ensuite, une fois qu’on s’intéresse à la problématique.",
                    feedbackKo: "Yann : vous pouvez vous intéresser à l’entrepreneuriat sans idée révolutionnaire."
                },
                {
                    objectif: "Oser avant d’être sûr",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Jean-Jacques : si vous attendez d’être sûr que ça va marcher…",
                    options: [
                        { text: "Vous ne sauterez jamais.", correct: true },
                        { text: "Vous maximisez vos chances de succès.", correct: false },
                        { text: "Les structures d’accompagnement refuseront de vous voir.", correct: false }
                    ],
                    feedbackOk: "« Il ne faut pas hésiter, il faut y aller. » La certitude n’arrive pas avant le saut.",
                    feedbackKo: "Le message de clôture est d’oser un premier pas, pas d’attendre la preuve totale."
                },
                {
                    objectif: "Choisir un premier pas réversible",
                    bloom: "Appliquer",
                    mecanisme: "Transfert + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Quel premier pas est aligné avec ce que dit la chorale ?",
                    options: [
                        { text: "Aller discuter avec des entrepreneurs et l’écosystème.", correct: true },
                        { text: "Rédiger seul un business plan parfait avant toute conversation.", correct: false },
                        { text: "Attendre d’avoir quitté son poste de chercheur.", correct: false }
                    ],
                    feedbackOk: "Loïc : aller discuter. Jean-Jacques : vous ne serez pas tout seul ; ceux qui sont passés avant aident.",
                    feedbackKo: "Le premier pas est social et réversible, pas un plan isolé ni une démission."
                }
            ],
            memory: [
                { front: "Par quoi commencer ?", back: "Un problème terrain. L’idée vient ensuite." },
                { front: "Attendre d’être sûr ?", back: "Si vous attendez, vous ne sauterez jamais." },
                { front: "Quel premier pas ?", back: "Discuter avec des entrepreneurs. Vous ne serez pas seul." }
            ],
            plusLoin: [
                mr("grain10.html", "2.4 — Cadrage du problème", "Revenir au problème terrain avant de « sauter »."),
                mr("grain19.html", "2.9 — Les échelles de maturité", "Nommer son niveau de preuve pour choisir le prochain pas."),
                mr("sommaire_sequence1.html", "Séquence 1 — De quoi parle-t-on ?", "Revoir définitions et vocabulaire si un terme bloque encore.")
            ]
        }
    };
})();
