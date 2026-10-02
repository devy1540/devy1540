<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->

<p align="center"><a href="./README.en.md" lang="en">English</a> · <a href="./README.ko.md" lang="ko">한국어</a> · <a href="./README.ja.md" lang="ja">日本語</a> · <a href="./README.zh-CN.md" lang="zh-CN">简体中文</a> · <a href="./README.es.md" lang="es">Español</a> · <a href="./README.fr.md" lang="fr">Français</a></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-hero-dark.svg#locale-en" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/profile-hero-light.svg#locale-en" />
    <img src="./assets/profile-hero-light.svg#locale-en" width="860" alt="Applied AI Engineer | Backend Engineer. I build with AI, and ship products. From design to implementation and operations, I build and verify it myself." />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-mobile-dark.svg#locale-en" />
    <source media="(max-width: 600px)" srcset="./assets/profile-tech-stack-mobile-light.svg#locale-en" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-dark.svg#locale-en" />
    <img src="./assets/profile-tech-stack-light.svg#locale-en" width="860" alt="Backend: Java, Spring Boot, PostgreSQL, MySQL, Redis. AI: Spring AI; OpenAI, Gemini, Amazon Bedrock; Codex, Claude Code. Infrastructure: Kubernetes, AWS, Google Cloud, Terraform, Grafana." />
  </picture>
</p>

## About

I’m a backend engineer at Day1Company, based in Seoul.

I build AI features and development workflows on a foundation of backend systems: payments, authentication, and service infrastructure.

Previously at EXEM, I worked on monitoring services and Kafka/Druid data collection pipelines.

## Selected work

- **AI products** — Built diagnostic and feedback pipelines and CS answer assistance with Spring AI. Diagnostic generation dropped from 6–7 minutes to 1–2 minutes, with roughly 50% lower LLM costs. [Diagnostic pipeline](https://dev.devy.dev/about/projects/ai-diagnostic-pipeline/) · [CS assistance](https://dev.devy.dev/about/projects/cs-automation/)

- **Backend systems** — Redesigned payment modules and authentication, and built multi-channel notifications. My work includes PortOne and RS256/JWKS signing with GCP KMS. [Payments](https://dev.devy.dev/about/projects/payment-system/) · [Authentication](https://dev.devy.dev/about/projects/auth-refactoring/) · [Notifications](https://dev.devy.dev/about/projects/notification-server/)

- **Infrastructure & observability** — Built ECS→EKS and AWS→GCP/GKE migrations, ArgoCD GitOps delivery, and observability with OpenTelemetry and the LGTM stack. [Infrastructure project](https://dev.devy.dev/about/projects/infra-modernization/)

## Open-source projects

- **[FCP](https://github.com/devy1540/fcp)** — A Go cloud emulator for local development and integration tests with official AWS/GCP SDKs. It documents API support boundaries and provides a structured CLI and snapshots.

- **[toard](https://github.com/devy1540/toard)** — A self-hosted dashboard for AI coding-tool usage, estimated costs, and activity across Claude Code, Codex, Cursor, and other tools.

- **[Codex Collaboration Conductor](https://github.com/devy1540/codex-collab-conductor)** — A Codex plugin for task-scoped native subagent delegation and evidence-based PR review.

- **[LLM Wiki](https://github.com/devy1540/ltm-wiki)** — A Codex plugin that turns selected sources into linked, source-backed Markdown knowledge, with project Wikis managed in Obsidian. Currently an MVP.

- **[JVM Concurrency Benchmark](https://github.com/devy1540/jvm-concurrency-benchmark)** — A reproducible comparison of Platform Threads, Virtual Threads, and Kotlin Coroutines across I/O, CPU, and concurrency scenarios, with Prometheus and Grafana metrics.

## Currently building

I’m improving agent collaboration that connects Slack requests to development, review, verification, and deployment. E2E agents for PR-specific checks and audit agents for execution records are in development. [Agent workflow project](https://dev.devy.dev/about/projects/ai-agent-workflow/)

## How I work

- Connect backend design and implementation to the screens, tests, delivery, and observability a feature needs.
- Define agent responsibilities and human decision points, and connect requests, issues, PRs, and deployment records.
- Verify completion with code, tests, and execution evidence, then check behavior after deployment.

## Writing

I write engineering notes in Korean, with implementation choices, operating constraints, and what I verified.

- [Applying agents to reduce team workflow bottlenecks](https://dev.devy.dev/posts/odin-ax-transformation/)
- [A seven-stage diagnostic pipeline with Spring AI](https://dev.devy.dev/posts/spring-ai-pipeline-real-world/)
- [JWT signing: HS256 → RS256/JWKS/KMS](https://dev.devy.dev/posts/jwt-hs256-to-rs256-jwks-kms/)
- [Moving from Datadog to the LGTM stack](https://dev.devy.dev/posts/lgtm-stack-observability/)

## Find me

[Portfolio](https://dev.devy.dev/about/) · [Blog](https://dev.devy.dev/) · [Email: gurwns1540@gmail.com](mailto:gurwns1540@gmail.com) · [LinkedIn](https://www.linkedin.com/in/%ED%98%81%EC%A4%80-%EC%9C%A4-21a3bb22a/)
