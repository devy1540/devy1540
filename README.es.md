<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->

<p align="center"><a href="./README.en.md" lang="en">English</a> · <a href="./README.ko.md" lang="ko">한국어</a> · <a href="./README.ja.md" lang="ja">日本語</a> · <a href="./README.zh-CN.md" lang="zh-CN">简体中文</a> · <a href="./README.es.md" lang="es">Español</a> · <a href="./README.fr.md" lang="fr">Français</a></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-hero-dark.svg#locale-es" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/profile-hero-light.svg#locale-es" />
    <img src="./assets/profile-hero-light.svg#locale-es" width="860" alt="Applied AI Engineer | Backend Engineer. Creo con IA, y entrego productos. Del diseño al desarrollo y la operación, lo construyo y verifico personalmente." />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-mobile-dark.svg#locale-es" />
    <source media="(max-width: 600px)" srcset="./assets/profile-tech-stack-mobile-light.svg#locale-es" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-dark.svg#locale-es" />
    <img src="./assets/profile-tech-stack-light.svg#locale-es" width="860" alt="Backend: Java, Spring Boot, PostgreSQL, MySQL, Redis. AI: Spring AI; OpenAI, Gemini, Amazon Bedrock; Codex, Claude Code. Infrastructure: Kubernetes, AWS, Google Cloud, Terraform, Grafana." />
  </picture>
</p>

## Sobre mí

Soy ingeniero de backend en Day1Company, en Seúl.

Aplico mi experiencia en pagos, autenticación e infraestructura de servicios a funciones de IA y a los flujos de desarrollo y operación de los equipos.

Antes, en EXEM, desarrollé servicios de monitorización y pipelines de recopilación de datos con Kafka y Druid.

## Experiencia destacada

- **Productos con IA** — Desarrollé pipelines de diagnóstico y feedback y asistencia para respuestas de atención al cliente con Spring AI. La generación de diagnósticos pasó de 6–7 a 1–2 minutos y el coste de los LLM se redujo aproximadamente un 50%. [Pipeline de diagnóstico](https://dev.devy.dev/about/projects/ai-diagnostic-pipeline/) · [Asistencia al cliente](https://dev.devy.dev/about/projects/cs-automation/)

- **Sistemas de backend** — Rediseñé módulos de pago y autenticación y desarrollé notificaciones multicanal. Mi trabajo incluye PortOne y firmas RS256/JWKS con GCP KMS. [Pagos](https://dev.devy.dev/about/projects/payment-system/) · [Autenticación](https://dev.devy.dev/about/projects/auth-refactoring/) · [Notificaciones](https://dev.devy.dev/about/projects/notification-server/)

- **Infraestructura y observabilidad** — Implementé migraciones ECS→EKS y AWS→GCP/GKE, despliegues GitOps con ArgoCD y observabilidad con OpenTelemetry y el stack LGTM. [Proyecto de infraestructura](https://dev.devy.dev/about/projects/infra-modernization/)

## Proyectos de código abierto

- **[FCP](https://github.com/devy1540/fcp)** — Emulador de nube en Go para desarrollo local y pruebas de integración con los SDK oficiales de AWS y GCP. Documenta el alcance de cada API y ofrece una CLI estructurada y snapshots.

- **[toard](https://github.com/devy1540/toard)** — Panel autoalojado para consultar el uso, los costes estimados y la actividad de herramientas de programación con IA como Claude Code, Codex y Cursor.

- **[Codex Collaboration Conductor](https://github.com/devy1540/codex-collab-conductor)** — Plugin de Codex para delegar tareas acotadas a subagentes nativos y realizar revisiones de PR basadas en evidencias.

- **[LLM Wiki](https://github.com/devy1540/ltm-wiki)** — Plugin de Codex que transforma fuentes seleccionadas en conocimiento Markdown enlazado y con referencias. Gestiona Wikis por proyecto en Obsidian. Actualmente está en fase MVP.

- **[JVM Concurrency Benchmark](https://github.com/devy1540/jvm-concurrency-benchmark)** — Benchmark reproducible que compara Platform Threads, Virtual Threads y Kotlin Coroutines en escenarios de I/O, CPU y alta concurrencia, con métricas de Prometheus y Grafana.

## En desarrollo

Estoy mejorando la colaboración entre agentes para conectar solicitudes de Slack con desarrollo, revisión, verificación y despliegue. Los agentes E2E para comprobar cada PR y los agentes de auditoría de registros de ejecución están en desarrollo. [Proyecto de flujos de trabajo con agentes](https://dev.devy.dev/about/projects/ai-agent-workflow/)

## Cómo trabajo

- Conecto el diseño y la implementación del backend con las interfaces, las pruebas, la entrega y la observabilidad que necesita cada función.
- Defino las responsabilidades de los agentes y las decisiones humanas, y enlazo solicitudes, issues, PR y registros de despliegue.
- Compruebo la finalización con código, pruebas y evidencias de ejecución, y verifico el comportamiento tras el despliegue.

## Artículos

Escribo en coreano sobre decisiones de implementación, restricciones operativas y resultados verificados.

- [Aplicar agentes para reducir los cuellos de botella del equipo](https://dev.devy.dev/posts/odin-ax-transformation/)
- [Un pipeline de diagnóstico de siete etapas con Spring AI](https://dev.devy.dev/posts/spring-ai-pipeline-real-world/)
- [Migrar la firma JWT: HS256 → RS256/JWKS/KMS](https://dev.devy.dev/posts/jwt-hs256-to-rs256-jwks-kms/)
- [Migrar de Datadog al stack LGTM](https://dev.devy.dev/posts/lgtm-stack-observability/)

## Contacto

[Portfolio](https://dev.devy.dev/about/) · [Blog](https://dev.devy.dev/) · [Correo: gurwns1540@gmail.com](mailto:gurwns1540@gmail.com) · [LinkedIn](https://www.linkedin.com/in/%ED%98%81%EC%A4%80-%EC%9C%A4-21a3bb22a/)
