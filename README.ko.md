<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->

<p align="center"><a href="./README.en.md" lang="en">English</a> · <a href="./README.ko.md" lang="ko">한국어</a> · <a href="./README.ja.md" lang="ja">日本語</a> · <a href="./README.zh-CN.md" lang="zh-CN">简体中文</a> · <a href="./README.es.md" lang="es">Español</a> · <a href="./README.fr.md" lang="fr">Français</a></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-hero-dark.svg#locale-ko" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/profile-hero-light.svg#locale-ko" />
    <img src="./assets/profile-hero-light.svg#locale-ko" width="860" alt="Applied AI Engineer | Backend Engineer. AI를 활용하고, 제품으로 완성합니다. 설계부터 구현·운영까지, 직접 만들고 검증합니다." />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-mobile-dark.svg#locale-ko" />
    <source media="(max-width: 600px)" srcset="./assets/profile-tech-stack-mobile-light.svg#locale-ko" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-dark.svg#locale-ko" />
    <img src="./assets/profile-tech-stack-light.svg#locale-ko" width="860" alt="Backend: Java, Spring Boot, PostgreSQL, MySQL, Redis. AI: Spring AI; OpenAI, Gemini, Amazon Bedrock; Codex, Claude Code. Infrastructure: Kubernetes, AWS, Google Cloud, Terraform, Grafana." />
  </picture>
</p>

## 소개

안녕하세요, 윤혁준입니다. 서울에서 데이원컴퍼니의 백엔드 엔지니어로 일하고 있습니다.

결제·인증과 서비스 인프라를 설계·운영해 온 경험을 바탕으로, AI를 제품 기능과 팀의 개발·운영 흐름에 연결합니다.

이전에는 엑셈에서 모니터링 서비스와 Kafka·Druid 기반 데이터 수집 파이프라인을 개발했습니다.

## 주요 경험

- **AI 제품** — Spring AI 기반 진단·피드백 파이프라인과 CS 상담 보조 기능을 구축했습니다. 진단 생성 시간은 6–7분에서 1–2분으로 줄였고, LLM 비용은 약 50% 절감했습니다. [진단 파이프라인](https://dev.devy.dev/about/projects/ai-diagnostic-pipeline/) · [CS 상담 보조](https://dev.devy.dev/about/projects/cs-automation/)

- **백엔드** — 결제 모듈과 인증 구조를 재설계하고, 멀티채널 알림 서버를 구축했습니다. PortOne, RS256/JWKS·GCP KMS, 메시징과 데이터 저장소를 서비스 운영에 연결합니다. [결제](https://dev.devy.dev/about/projects/payment-system/) · [인증](https://dev.devy.dev/about/projects/auth-refactoring/) · [알림](https://dev.devy.dev/about/projects/notification-server/)

- **인프라·관측** — ECS→EKS와 AWS→GCP/GKE 이관, ArgoCD 기반 GitOps, OpenTelemetry·LGTM 관측 환경을 구축했습니다. [인프라 프로젝트](https://dev.devy.dev/about/projects/infra-modernization/)

## 오픈소스 프로젝트

- **[FCP](https://github.com/devy1540/fcp)** — 공식 AWS·GCP SDK를 연결해 로컬 개발과 통합 테스트에 사용하는 Go 클라우드 에뮬레이터. API별 지원 범위, 구조화된 CLI와 스냅샷을 제공합니다.

- **[toard](https://github.com/devy1540/toard)** — AI 코딩 도구의 사용량·예상 비용·활동을 모아 보는 셀프호스팅 대시보드. Claude Code, Codex, Cursor 등 여러 도구의 기록을 연결합니다.

- **[Codex Collaboration Conductor](https://github.com/devy1540/codex-collab-conductor)** — 작업 범위에 맞춘 네이티브 하위 에이전트 분담과 근거 중심 PR 리뷰를 정의하는 Codex 플러그인.

- **[LLM Wiki](https://github.com/devy1540/ltm-wiki)** — 선택한 자료를 출처가 있는 Markdown 지식으로 정리하는 Codex 플러그인. 프로젝트별 Wiki를 Obsidian에서 관리합니다. 현재 MVP 단계입니다.

- **[JVM Concurrency Benchmark](https://github.com/devy1540/jvm-concurrency-benchmark)** — Platform Thread·Virtual Thread·Kotlin Coroutine을 I/O, CPU, 동시성 시나리오로 비교하는 재현 가능한 벤치마크. Prometheus와 Grafana로 실행 지표를 확인합니다.

## 현재 만드는 것

Slack 요청을 개발·리뷰·검증·배포로 연결하는 에이전트 협업 흐름을 개선하고 있습니다. PR별 검증을 위한 E2E 에이전트와 실행 기록을 점검하는 감사 에이전트는 개발 중입니다. [에이전트 업무 흐름 상세](https://dev.devy.dev/about/projects/ai-agent-workflow/)

## 개발·운영 방식

- 백엔드 설계·구현에서 필요한 화면, 테스트, 배포·관측까지 연결합니다.
- 에이전트의 담당 범위와 사람이 판단할 조건을 정하고 요청·이슈·PR·배포 기록을 연결합니다.
- 완료 여부는 코드·테스트·실행 근거로 확인하고, 운영 반영 뒤 동작을 다시 확인합니다.

## 개발 기록

구현 과정에서 선택한 방법, 운영 제약과 검증한 결과를 한국어로 기록합니다.

- [팀의 업무 병목을 줄이기 위한 AX 전환](https://dev.devy.dev/posts/odin-ax-transformation/)
- [Spring AI 실전 적용기 — 7단계 AI 진단 파이프라인](https://dev.devy.dev/posts/spring-ai-pipeline-real-world/)
- [JWT 서명 전환 — HS256에서 RS256/JWKS/KMS로](https://dev.devy.dev/posts/jwt-hs256-to-rs256-jwks-kms/)
- [Datadog 걷어내고 LGTM 스택 구축하기](https://dev.devy.dev/posts/lgtm-stack-observability/)

## 연락처

[포트폴리오](https://dev.devy.dev/about/) · [블로그](https://dev.devy.dev/) · [이메일: gurwns1540@gmail.com](mailto:gurwns1540@gmail.com) · [LinkedIn](https://www.linkedin.com/in/%ED%98%81%EC%A4%80-%EC%9C%A4-21a3bb22a/)
