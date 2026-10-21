window.EVAL_BANK = (function () {
    function mr(file, title, why) {
        return {
            title: title,
            why: why,
            href: file
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
                    objectif: "Nommer les deux origines d’une innovation",
                    bloom: "Comprendre",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Tech-push et market-pull désignent…",
                    options: [
                        { text: "Deux origines possibles : partir d’une technologie, ou partir d’un besoin de marché.", correct: true },
                        { text: "Deux façons de déposer un brevet.", correct: false },
                        { text: "Deux types de financements dilutifs.", correct: false }
                    ],
                    feedbackOk: "Bernard pose les deux entrées. Un même projet peut combiner les deux.",
                    feedbackKo: "Ce n’est ni un outil de PI, ni un type d’investissement : ce sont les origines de l’innovation."
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
                { front: "Invention = innovation ?", back: "Non. Elle le devient en rencontrant un besoin, mieux que les solutions existantes." },
                { front: "Tech-push / market-pull ?", back: "Deux origines : partir d’une techno, ou partir d’un besoin." },
                { front: "Que faire d’une intuition de domaine ?", back: "La confronter au terrain : qui, quelles difficultés, quelles situations." }
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
                lead: "E2 (passer d’une techno à un problème) est à venir. E3 pose déjà l’ordre : le bon problème avant la bonne solution.",
                steps: [
                    { title: "1. Techno", text: "Ce que le laboratoire sait faire." },
                    { title: "2. Qui / où", text: "Utilisateur, client, situation d’usage." },
                    { title: "3. Problème", text: "La difficulté concrète, pas la solution." },
                    { title: "4. Preuve", text: "Ce qui montre que le besoin existe vraiment." }
                ]
            },
            mr: [mr("mr-grain10.html", "2.4 — Cadrage du problème", "Capsule du Module Ressources, incluse ici en consultation (sans quiz). Pour passer d’une techno à un problème, on cadre d’abord (Double diamant).")],
            quiz: [
                {
                    objectif: "Prioriser le problème avant la solution",
                    bloom: "Comprendre",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour poser le bon problème, l’expert insiste d’abord sur…",
                    options: [
                        { text: "Le bon problème avant la bonne solution.", correct: true },
                        { text: "Le prototype avant d’avoir formulé le besoin.", correct: false },
                        { text: "Le dépôt de brevet avant toute rencontre terrain.", correct: false }
                    ],
                    feedbackOk: "L’incrustation le dit : le bon problème avant la bonne solution. Problem–Solution Fit.",
                    feedbackKo: "Ce n’est pas « faire d’abord l’objet » : c’est formuler et valider le problème."
                },
                {
                    objectif: "Retenir la séquence de cadrage",
                    bloom: "Appliquer",
                    mecanisme: "Récupération + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "L’ordre enseigné pour le problème est…",
                    options: [
                        { text: "Identifier → Formuler → Valider.", correct: true },
                        { text: "Protéger → Publier → Financer.", correct: false },
                        { text: "Prototype → Logo → Levée de fonds.", correct: false }
                    ],
                    feedbackOk: "Identifier, formuler, valider : ensuite seulement on résout.",
                    feedbackKo: "Ce n’est pas la frise PI ni la start-up : c’est la séquence du problème."
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
                { front: "Quoi d’abord : problème ou solution ?", back: "Le bon problème avant la bonne solution." },
                { front: "Quel ordre pour le problème ?", back: "Identifier → Formuler → Valider." },
                { front: "Une étude bibliographique suffit-elle ?", back: "Non. Il faut échanger avec les acteurs du terrain." }
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
                lead: "E4 (POC, prototype, MVP, TRL) est à venir. E5 enseigne déjà à dérisquer par étapes. Le détail TRL est dans le module Ressources.",
                steps: [
                    { title: "Résultat", text: "Ce que le labo a montré." },
                    { title: "POC", text: "Preuve que ça peut marcher." },
                    { title: "Prototype", text: "Objet testable, encore imparfait." },
                    { title: "MVP", text: "Produit minimal utilisable par un client." }
                ]
            },
            mr: [mr("mr-grain19.html", "2.9 — Les échelles de maturité", "Capsule du Module Ressources, incluse ici en consultation (sans quiz). E4 n’est pas encore là : situez votre niveau de preuve (TRL), puis revenez.")],
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
                    objectif: "Relier terrain et dérisquage",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Aller sur le terrain pour comprendre les besoins, selon l’expert, c’est surtout…",
                    options: [
                        { text: "Un moyen de dérisquer le projet.", correct: true },
                        { text: "Une perte de temps tant que la techno n’est pas parfaite.", correct: false },
                        { text: "Réservé à la phase après création d’entreprise.", correct: false }
                    ],
                    feedbackOk: "Dérisquer par étapes : la solution technique doit rejoindre les besoins du marché.",
                    feedbackKo: "Le terrain n’attend pas la techno parfaite ni la société créée."
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
                { front: "Un pivot, c’est un échec ?", back: "Non. C’est une décision : pivoter rapidement n’est pas échouer." },
                { front: "À quoi sert le terrain ?", back: "À dérisquer : la solution doit rejoindre un besoin de marché." },
                { front: "Quelle frise de dérisquage ?", back: "Invention → Prématuration → Maturation." }
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
                    objectif: "Nommer les voies de valorisation",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Parmi les voies de valorisation enseignées, on trouve…",
                    options: [
                        { text: "Licence, création d’entreprise, co-développement et partenariat.", correct: true },
                        { text: "Uniquement la création d’entreprise.", correct: false },
                        { text: "Uniquement le dépôt de brevet, sans contrat.", correct: false }
                    ],
                    feedbackOk: "Quatre voies : licence, start-up, co-développement, partenariat. Le choix est structurant.",
                    feedbackKo: "Le brevet protège ; il ne dit pas encore par quelle voie on valorise."
                },
                {
                    objectif: "Distinguer licence et cession",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Licence et cession, ce n’est pas la même chose :",
                    options: [
                        { text: "Licence = louage du droit d’exploiter ; cession = vente du titre.", correct: true },
                        { text: "Licence = vente du brevet ; cession = simple prêt.", correct: false },
                        { text: "Les deux transfèrent toujours toute la propriété, partout.", correct: false }
                    ],
                    feedbackOk: "La licence concède l’exploitation sans transférer la propriété. Exclusive ou non.",
                    feedbackKo: "Avant d’en parler : contrat de confidentialité. Puis on choisit le mécanisme."
                }
            ],
            memory: [
                { front: "Quelles voies de valorisation ?", back: "Licence, création d’entreprise, co-développement, partenariat." },
                { front: "Licence ou cession ?", back: "Licence = louage. Cession = vente du titre." },
                { front: "Premier contrat avant de parler ?", back: "Un accord de confidentialité (NDA)." }
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
            quiz: [
                {
                    objectif: "Découpler maturation et incubation",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Maturation technologique et incubation business, d’après l’incubateur…",
                    options: [
                        { text: "Ce sont deux aspects à découpler : une excellente techno ne fait pas une start-up.", correct: true },
                        { text: "C’est la même étape, menée uniquement au laboratoire.", correct: false },
                        { text: "L’incubation remplace toujours la maturation SATT.", correct: false }
                    ],
                    feedbackOk: "La SATT mature une technologie. L’incubateur prépare le côté entrepreneurial.",
                    feedbackKo: "Techno robuste ≠ entreprise. Les deux peuvent avancer, mais ce n’est pas le même métier."
                },
                {
                    objectif: "Situer le rôle de l’incubateur",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "L’incubateur aide surtout à…",
                    options: [
                        { text: "Préparer les rencontres, tester les hypothèses et intéresser les financeurs.", correct: true },
                        { text: "Déposer le brevet à la place du chercheur.", correct: false },
                        { text: "Remplacer toute étude de marché par un concours.", correct: false }
                    ],
                    feedbackOk: "Confrontation au terrain, feuille de route, réseau : pas un substitut à la PI.",
                    feedbackKo: "L’incubateur n’est pas l’office des brevets."
                },
                {
                    objectif: "Relier fablab et usage",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Design Spot / fablabs servent surtout à…",
                    options: [
                        { text: "Passer de l’idée à une preuve concrète et travailler tôt le besoin et l’usage.", correct: true },
                        { text: "Rédiger le pacte d’associés.", correct: false },
                        { text: "Lever des fonds dilutifs auprès d’industriels.", correct: false }
                    ],
                    feedbackOk: "Compétences, équipements, accompagnements : prototyper pour un usage, pas pour le style.",
                    feedbackKo: "Ce n’est ni le contrat entre fondateurs, ni la levée de fonds."
                }
            ],
            memory: [
                { front: "Maturation = incubation ?", back: "Non. Techno d’un côté, entreprise de l’autre." },
                { front: "Une excellente techno = une start-up ?", back: "Non. Il manque le besoin réel, les associés, le terrain." },
                { front: "À quoi sert un fablab ?", back: "Prototyper tôt pour un besoin et un usage." }
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
                    { text: "Beaucoup de financements sont anté-création : une fois créé, on n’y est plus éligible.", correct: true },
                    { text: "Il est interdit de créer une entreprise tant qu’on est chercheur.", correct: false },
                    { text: "Les aides n’existent qu’après le premier chiffre d’affaires.", correct: false }
                ],
                feedbackOk: "Étapes anté-création puis post-création. Créer trop tôt ferme des portes d’aides.",
                feedbackKo: "La chorale parle d’éligibilité des aides, pas d’une interdiction d’entreprendre."
            },
            media: {
                when: "after-t",
                type: "steps",
                title: "Frise entendue dans la chorale",
                lead: "E15 (chaîne des financements) est à venir. E19 enseigne déjà dilutif / non-dilutif et le dérisquage par l’argent.",
                steps: [
                    { title: "Anté-création", text: "Valorisation univ. / CNRS, POC'in Lab, prématuration." },
                    { title: "Marches", text: "i-Lab, recrutement, preuves plus solides." },
                    { title: "Création", text: "On bascule : certaines aides se ferment." },
                    { title: "Après", text: "Investisseurs ou clients." }
                ]
            },
            mr: [mr("mr-grain5.html", "1.5 — La chaîne de valeur", "Capsule du Module Ressources, incluse ici en consultation (sans quiz). Elle montre les flux de financement et de valeur, du labo vers l’usage.")],
            quiz: [
                {
                    objectif: "Choisir le moment de création",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Créer trop tôt, concrètement, c’est…",
                    options: [
                        { text: "Perdre l’éligibilité à des financements anté-création.", correct: true },
                        { text: "Gagner automatiquement plus d’aides publiques.", correct: false },
                        { text: "Obligatoire pour déposer un brevet.", correct: false }
                    ],
                    feedbackOk: "Jean-Jacques : beaucoup d’aides disparaissent dès que la société existe.",
                    feedbackKo: "Le brevet n’exige pas une société ; trop tôt peut coûter des aides."
                },
                {
                    objectif: "Distinguer dilutif et non-dilutif",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Un financement non dilutif, c’est…",
                    options: [
                        { text: "Les fondateurs détiennent toujours autant de parts.", correct: true },
                        { text: "Les investisseurs prennent des parts au capital.", correct: false },
                        { text: "La seule façon de financer l’industrialisation.", correct: false }
                    ],
                    feedbackOk: "Subvention, avance remboursable, prêts d’honneur : pas de prise de parts. Le dilutif, si : les fondateurs sont dilués.",
                    feedbackKo: "Non-dilutif ≠ levée de fonds au capital."
                },
                {
                    objectif: "Relier argent et dérisquage",
                    bloom: "Comprendre",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Financer progressivement, selon l’expert, sert à…",
                    options: [
                        { text: "Réduire les risques : minimiser son risque, maximiser la valeur de son engagement.", correct: true },
                        { text: "Remplacer toute confrontation au terrain.", correct: false },
                        { text: "Publier plus vite, avant toute protection.", correct: false }
                    ],
                    feedbackOk: "On finance des jalons de dérisquage, pas une publication.",
                    feedbackKo: "L’argent ne dispense ni du terrain ni de la PI."
                }
            ],
            memory: [
                { front: "Pourquoi ne pas créer trop tôt ?", back: "Des aides anté-création deviennent inaccessibles." },
                { front: "Non-dilutif, ça veut dire ?", back: "Les fondateurs gardent autant de parts (subvention, prêt…)." },
                { front: "Dilutif, ça veut dire ?", back: "Prise de parts : les fondateurs sont dilués." }
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
            quiz: [
                {
                    objectif: "Voir ce que regardent les investisseurs",
                    bloom: "Comprendre",
                    mecanisme: "Récupération + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Les investisseurs regardent attentivement…",
                    options: [
                        { text: "L’équipe du projet — elle survit aux différents pivots.", correct: true },
                        { text: "Uniquement le nombre de publications.", correct: false },
                        { text: "Uniquement le nom de l’établissement.", correct: false }
                    ],
                    feedbackOk: "Compétences collectives, alignement des finalités : chacun a un rôle.",
                    feedbackKo: "Ce n’est pas le CV académique seul."
                },
                {
                    objectif: "Choisir une posture dans l’équipe",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "S’engager dans le projet, ce n’est pas forcément être CEO : on peut aussi…",
                    options: [
                        { text: "Siéger au comité scientifique, selon la posture choisie.", correct: true },
                        { text: "Rester hors de tout rôle tant qu’on est chercheur.", correct: false },
                        { text: "Cumul obligatoire de tous les rôles (CEO, juridique, finance).", correct: false }
                    ],
                    feedbackOk: "CEO ou comité scientifique : choisir la posture. Les compétences s’augmentent.",
                    feedbackKo: "Il y a plusieurs places dans le collectif."
                },
                {
                    objectif: "Séparer PI et parts sociales",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Droits de PI et parts sociales…",
                    options: [
                        { text: "Ce sont deux distributions distinctes, à définir et quantifier dans le contrat.", correct: true },
                        { text: "C’est la même chose : qui invente possède automatiquement la majorité.", correct: false },
                        { text: "Le contrat est inutile si l’équipe s’entend bien au début.", correct: false }
                    ],
                    feedbackOk: "Le contrat fait la loi des parties : gouvernance, pouvoir, conditions financières.",
                    feedbackKo: "Inventer ≠ détenir les parts. Il faut écrire les apports."
                }
            ],
            memory: [
                { front: "Que regardent les investisseurs ?", back: "L’équipe. Elle survit aux pivots." },
                { front: "Doit-on être CEO ?", back: "Non. Comité scientifique, autre rôle : chacun a une place." },
                { front: "PI = parts sociales ?", back: "Non. Deux distributions distinctes, à écrire." }
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
            mr: [mr("mr-grain4.html", "1.4 — Le nuage de vocabulaire", "Capsule du Module Ressources, incluse ici en consultation (sans quiz). Invention ≠ innovation : adapter le lexique à qui vous écoute.")],
            quiz: [
                {
                    objectif: "Relier changement de contexte et vocabulaire",
                    bloom: "Comprendre",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Un changement de contexte, selon l’experte, amène surtout…",
                    options: [
                        { text: "Un changement de vocabulaire — et parfois de posture.", correct: true },
                        { text: "L’obligation de cesser toute publication.", correct: false },
                        { text: "La disparition de toute PI.", correct: false }
                    ],
                    feedbackOk: "On navigue chercheur ⇄ entrepreneurial. Le lexique change (business model, pitch, B2B…).",
                    feedbackKo: "Adapter les mots n’efface ni la science ni la PI."
                },
                {
                    objectif: "Distinguer les trois sens de « valorisation »",
                    bloom: "Analyser",
                    mecanisme: "Élaboration",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "« Valorisation » peut vouloir dire, dans l’ordre enseigné…",
                    options: [
                        { text: "Publication → propriété intellectuelle → valeur monétaire.", correct: true },
                        { text: "Uniquement une levée de fonds.", correct: false },
                        { text: "Uniquement une note dans une revue.", correct: false }
                    ],
                    feedbackOk: "Trois sens, trois destinataires. D’où l’écoute de l’interlocuteur.",
                    feedbackKo: "Le mot n’a pas qu’un usage académique, ni qu’un usage financier."
                },
                {
                    objectif: "Adapter le discours à qui écoute",
                    bloom: "Appliquer",
                    mecanisme: "Application + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Le même résultat se raconte différemment selon que l’on parle à…",
                    options: [
                        { text: "Financeurs, partenaires, industriels, institutions, décideurs ou clients.", correct: true },
                        { text: "Uniquement à d’autres chercheurs, toujours avec le même lexique.", correct: false },
                        { text: "Personne : le discours unique suffit.", correct: false }
                    ],
                    feedbackOk: "Écouter l’interlocuteur fait gagner du temps et de l’énergie.",
                    feedbackKo: "Un seul jargon scientifique ne passe pas tous les contextes."
                }
            ],
            memory: [
                { front: "Changement de contexte ?", back: "Changement de vocabulaire — et de posture." },
                { front: "Trois sens de « valorisation » ?", back: "Publication → PI → valeur monétaire." },
                { front: "À qui adapter le discours ?", back: "Financeurs, partenaires, industriels, institutions, décideurs, clients." }
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
                question: "Quel conseil traverse la chorale de T12 ?",
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
                { front: "Faut-il naître entrepreneur ?", back: "Non. La posture s’apprend (feedback, mentorat)." },
                { front: "Doit-on quitter la recherche ?", back: "Non. Enrichir le métier : double casquette, comité scientifique." },
                { front: "Quoi concilier ?", back: "Liberté académique et protection de la PI ; deux temporalités." }
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
            ]
        },

        grain_t13_conclusion: {
            media: {
                when: "after-e",
                type: "list",
                title: "Synthèse du parcours",
                lead: "Le quiz et les cartes ci-dessous reprennent les points principaux des six modules — pas seulement la chorale.",
                items: [
                    "M1 — Invention ≠ innovation : un besoin réel, le bon problème d’abord.",
                    "M2 — Protéger avant de communiquer ; choisir une voie de valorisation.",
                    "M3 — On n’avance pas seul ; ne pas créer trop tôt.",
                    "M4 — L’équipe et le langage comptent autant que la techno.",
                    "M5 — Collaborer de façon équilibrée ; enrichir le métier, pas le quitter.",
                    "M6 — Oser un premier pas."
                ]
            },
            quiz: [
                {
                    objectif: "Relier résultat, besoin et problème (M1)",
                    bloom: "Analyser",
                    mecanisme: "Élaboration + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Tout au long du parcours, un résultat de recherche devient une innovation surtout quand…",
                    options: [
                        { text: "Il rencontre un besoin réel, mieux que l’existant — après avoir formulé le bon problème.", correct: true },
                        { text: "Il a été publié dans une revue de rang A.", correct: false },
                        { text: "Il a été breveté, même sans usage ni terrain.", correct: false }
                    ],
                    feedbackOk: "Invention ≠ innovation. Tech-push ou market-pull : le bon problème avant la bonne solution, confronté au terrain.",
                    feedbackKo: "Ni la publication ni le brevet ne suffisent : il faut un besoin, mieux servi que les solutions existantes."
                },
                {
                    objectif: "Protéger, choisir une voie, ne pas créer trop tôt (M2–M3)",
                    bloom: "Analyser",
                    mecanisme: "Discrimination + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour valoriser un résultat, la formation retient surtout…",
                    options: [
                        { text: "Protéger avant de communiquer, choisir une voie (licence, création, partenariat) et ne pas créer trop tôt.", correct: true },
                        { text: "Publier d’abord pour créer une antériorité, puis éventuellement protéger.", correct: false },
                        { text: "Créer une société dès la première intuition, pour ouvrir toutes les aides.", correct: false }
                    ],
                    feedbackOk: "Déclaration d’invention, puis une voie. Créer trop tôt ferme des aides anté-création. On n’avance pas seul.",
                    feedbackKo: "Publier trop tôt tue la nouveauté. Créer trop tôt ferme des financements. Le brevet ne dit pas encore la voie."
                },
                {
                    objectif: "Équipe, langage, collaboration, métier, action (M4–M6)",
                    bloom: "Appliquer",
                    mecanisme: "Transfert + feedback",
                    dispositif: "QCM",
                    fonction: "Formative",
                    question: "Pour passer à l’action, le fil des derniers modules insiste sur…",
                    options: [
                        { text: "S’appuyer sur une équipe et l’écosystème, adapter son langage, collaborer de façon équilibrée — et oser un premier pas, sans quitter forcément la recherche.", correct: true },
                        { text: "Tout faire seul, avec le même jargon scientifique, jusqu’à être absolument sûr.", correct: false },
                        { text: "Quitter le laboratoire et tout raconter sans accord de confidentialité.", correct: false }
                    ],
                    feedbackOk: "PI ≠ parts. Chacun apporte, chacun gagne — et c’est écrit. On n’est pas « né entrepreneur ». Le premier pas est réversible.",
                    feedbackKo: "Attendre d’être sûr, rester seul ou tout divulguer : ce n’est pas le fil du parcours."
                }
            ],
            memory: [
                { front: "M1 · Invention = innovation ?", back: "Non. Un besoin réel, mieux servi que l’existant. Bon problème d’abord." },
                { front: "M2 · Avant de communiquer ?", back: "Protéger (déclaration d’invention). Puis une voie : licence, création, partenariat." },
                { front: "M3 · Avancer seul ?", back: "Non. Maturation ≠ incubation. Ne pas créer trop tôt : des aides se ferment." },
                { front: "M4 · Quoi au-delà de la techno ?", back: "Une équipe (PI ≠ parts). Un langage adapté à qui écoute." },
                { front: "M5 · Collaborer / métier ?", back: "Chacun apporte, chacun gagne — et c’est écrit. Enrichir le métier, pas le quitter." },
                { front: "M6 · Premier pas ?", back: "Oser avant d’être sûr. Discuter, se faire accompagner. Vous n’êtes pas seul." }
            ]
        }
    };
})();
