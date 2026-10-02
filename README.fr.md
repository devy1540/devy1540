<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->

<p align="center"><a href="./README.en.md" lang="en">English</a> · <a href="./README.ko.md" lang="ko">한국어</a> · <a href="./README.ja.md" lang="ja">日本語</a> · <a href="./README.zh-CN.md" lang="zh-CN">简体中文</a> · <a href="./README.es.md" lang="es">Español</a> · <a href="./README.fr.md" lang="fr">Français</a></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-hero-dark.svg#locale-fr" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/profile-hero-light.svg#locale-fr" />
    <img src="./assets/profile-hero-light.svg#locale-fr" width="860" alt="Applied AI Engineer | Backend Engineer. Je crée avec l’IA, et livre des produits. De la conception au code et à l’exploitation, je construis et vérifie moi-même." />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-mobile-dark.svg#locale-fr" />
    <source media="(max-width: 600px)" srcset="./assets/profile-tech-stack-mobile-light.svg#locale-fr" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-dark.svg#locale-fr" />
    <img src="./assets/profile-tech-stack-light.svg#locale-fr" width="860" alt="Backend: Java, Spring Boot, PostgreSQL, MySQL, Redis. AI: Spring AI; OpenAI, Gemini, Amazon Bedrock; Codex, Claude Code. Infrastructure: Kubernetes, AWS, Google Cloud, Terraform, Grafana." />
  </picture>
</p>

## À propos

Je suis ingénieur backend chez Day1Company, à Séoul.

J’applique mon expérience en paiement, authentification et infrastructure de services aux fonctionnalités d’IA et aux processus de développement et d’exploitation des équipes.

Auparavant, chez EXEM, je développais des services de supervision et des pipelines de collecte de données avec Kafka et Druid.

## Expérience

- **Produits d’IA** — J’ai construit des pipelines de diagnostic et de feedback ainsi qu’une aide aux réponses du support client avec Spring AI. La génération des diagnostics est passée de 6–7 à 1–2 minutes, avec une baisse d’environ 50 % des coûts des LLM. [Pipeline de diagnostic](https://dev.devy.dev/about/projects/ai-diagnostic-pipeline/) · [Assistance au support](https://dev.devy.dev/about/projects/cs-automation/)

- **Systèmes backend** — J’ai repensé les modules de paiement et l’authentification, et développé des notifications multicanales. Mon travail inclut PortOne et la signature RS256/JWKS avec GCP KMS. [Paiement](https://dev.devy.dev/about/projects/payment-system/) · [Authentification](https://dev.devy.dev/about/projects/auth-refactoring/) · [Notifications](https://dev.devy.dev/about/projects/notification-server/)

- **Infrastructure et observabilité** — J’ai réalisé les migrations ECS→EKS et AWS→GCP/GKE, mis en place les déploiements GitOps avec ArgoCD et l’observabilité avec OpenTelemetry et la stack LGTM. [Projet d’infrastructure](https://dev.devy.dev/about/projects/infra-modernization/)

## Projets open source

- **[FCP](https://github.com/devy1540/fcp)** — Émulateur cloud en Go pour le développement local et les tests d’intégration avec les SDK officiels AWS et GCP. Il précise le périmètre de chaque API et fournit une CLI structurée et des snapshots.

- **[toard](https://github.com/devy1540/toard)** — Tableau de bord auto-hébergé pour consulter l’usage, les coûts estimés et l’activité des outils de développement avec IA, dont Claude Code, Codex et Cursor.

- **[Codex Collaboration Conductor](https://github.com/devy1540/codex-collab-conductor)** — Plugin Codex pour déléguer des tâches délimitées aux sous-agents natifs et effectuer des revues de PR fondées sur des éléments vérifiables.

- **[LLM Wiki](https://github.com/devy1540/ltm-wiki)** — Plugin Codex qui transforme des sources choisies en connaissances Markdown liées et référencées. Les Wikis propres à chaque projet sont gérés dans Obsidian. Le projet est actuellement au stade MVP.

- **[JVM Concurrency Benchmark](https://github.com/devy1540/jvm-concurrency-benchmark)** — Benchmark reproductible comparant Platform Threads, Virtual Threads et Kotlin Coroutines dans des scénarios I/O, CPU et de forte concurrence, avec des métriques Prometheus et Grafana.

## En développement

J’améliore la collaboration entre agents pour relier les demandes Slack au développement, à la revue, à la vérification et au déploiement. Les agents E2E pour vérifier chaque PR et les agents d’audit des traces d’exécution sont en cours de développement. [Projet de processus avec agents](https://dev.devy.dev/about/projects/ai-agent-workflow/)

## Ma façon de travailler

- Je relie la conception et l’implémentation du backend aux interfaces, aux tests, à la livraison et à l’observabilité nécessaires.
- Je définis les responsabilités des agents et les décisions humaines, et relie les demandes, issues, PR et traces de déploiement.
- Je vérifie l’achèvement avec le code, les tests et des preuves d’exécution, puis le comportement après le déploiement.

## Articles

J’écris en coréen sur les choix d’implémentation, les contraintes d’exploitation et les résultats vérifiés.

- [Utiliser des agents pour réduire les blocages dans les processus de l’équipe](https://dev.devy.dev/posts/odin-ax-transformation/)
- [Un pipeline de diagnostic en sept étapes avec Spring AI](https://dev.devy.dev/posts/spring-ai-pipeline-real-world/)
- [Migration de la signature JWT : HS256 → RS256/JWKS/KMS](https://dev.devy.dev/posts/jwt-hs256-to-rs256-jwks-kms/)
- [Migration de Datadog vers la stack LGTM](https://dev.devy.dev/posts/lgtm-stack-observability/)

## Contact

[Portfolio](https://dev.devy.dev/about/) · [Blog](https://dev.devy.dev/) · [E-mail: gurwns1540@gmail.com](mailto:gurwns1540@gmail.com) · [LinkedIn](https://www.linkedin.com/in/%ED%98%81%EC%A4%80-%EC%9C%A4-21a3bb22a/)
