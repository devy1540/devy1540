<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->

<p align="center"><a href="./README.en.md" lang="en">English</a> · <a href="./README.ko.md" lang="ko">한국어</a> · <a href="./README.ja.md" lang="ja">日本語</a> · <a href="./README.zh-CN.md" lang="zh-CN">简体中文</a> · <a href="./README.es.md" lang="es">Español</a> · <a href="./README.fr.md" lang="fr">Français</a></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-hero-dark.svg#locale-zh-CN" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/profile-hero-light.svg#locale-zh-CN" />
    <img src="./assets/profile-hero-light.svg#locale-zh-CN" width="860" alt="Applied AI Engineer | Backend Engineer. 运用 AI， 打造产品。 从设计到开发与运维， 亲自构建并验证。" />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-mobile-dark.svg#locale-zh-CN" />
    <source media="(max-width: 600px)" srcset="./assets/profile-tech-stack-mobile-light.svg#locale-zh-CN" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-dark.svg#locale-zh-CN" />
    <img src="./assets/profile-tech-stack-light.svg#locale-zh-CN" width="860" alt="Backend: Java, Spring Boot, PostgreSQL, MySQL, Redis. AI: Spring AI; OpenAI, Gemini, Amazon Bedrock; Codex, Claude Code. Infrastructure: Kubernetes, AWS, Google Cloud, Terraform, Grafana." />
  </picture>
</p>

## 关于我

我在首尔的Day1Company担任后端工程师。

基于支付、认证和服务基础设施的设计与运维经验，我将AI融入产品功能以及团队的开发和运维流程。

此前，我在EXEM开发监控服务和基于Kafka、Druid的数据采集流水线。

## 主要工作

- **AI产品** — 使用Spring AI构建诊断与反馈流水线及客服回答辅助功能。诊断生成时间从6–7分钟缩短至1–2分钟，LLM成本降低约50%。 [诊断流水线](https://dev.devy.dev/about/projects/ai-diagnostic-pipeline/) · [客服辅助](https://dev.devy.dev/about/projects/cs-automation/)

- **后端系统** — 重新设计支付模块和认证体系，并构建多渠道通知服务。涉及PortOne，以及基于GCP KMS的RS256/JWKS签名。 [支付](https://dev.devy.dev/about/projects/payment-system/) · [认证](https://dev.devy.dev/about/projects/auth-refactoring/) · [通知](https://dev.devy.dev/about/projects/notification-server/)

- **基础设施与可观测性** — 完成ECS→EKS、AWS→GCP/GKE迁移，搭建ArgoCD GitOps交付流程和OpenTelemetry、LGTM可观测性环境。 [基础设施项目](https://dev.devy.dev/about/projects/infra-modernization/)

## 开源项目

- **[FCP](https://github.com/devy1540/fcp)** — 用于本地开发和集成测试的Go云服务模拟器，可连接官方AWS、GCP SDK。明确各API的支持范围，并提供结构化CLI和快照。

- **[toard](https://github.com/devy1540/toard)** — 自托管仪表盘，汇总Claude Code、Codex、Cursor等AI编程工具的使用量、预估成本和活动记录。

- **[Codex Collaboration Conductor](https://github.com/devy1540/codex-collab-conductor)** — Codex插件，根据任务范围分配原生子智能体，并定义以证据为基础的PR审查流程。

- **[LLM Wiki](https://github.com/devy1540/ltm-wiki)** — Codex插件，将选定资料整理为带来源和链接的Markdown知识，在Obsidian中管理各项目的Wiki。目前处于MVP阶段。

- **[JVM Concurrency Benchmark](https://github.com/devy1540/jvm-concurrency-benchmark)** — 可复现的JVM并发基准测试，在I/O、CPU和高并发场景下比较Platform Thread、Virtual Thread与Kotlin Coroutine，并使用Prometheus、Grafana查看运行指标。

## 当前开发

我正在改进智能体协作流程，将Slack请求连接到开发、审查、验证和部署。面向各PR的E2E验证智能体及检查执行记录的审计智能体仍在开发中。 [智能体工作流程详情](https://dev.devy.dev/about/projects/ai-agent-workflow/)

## 开发与运维方式

- 从后端设计与实现延伸到所需的界面、测试、交付和可观测性。
- 明确智能体的职责与需要人工判断的条件，并关联请求、Issue、PR和部署记录。
- 依据代码、测试和运行证据判断是否完成，并在部署后再次确认实际行为。

## 技术文章

我用韩语记录实现选择、运维约束及验证结果。

- [通过AI智能体减少团队工作流程中的瓶颈](https://dev.devy.dev/posts/odin-ax-transformation/)
- [使用Spring AI构建七阶段诊断流水线](https://dev.devy.dev/posts/spring-ai-pipeline-real-world/)
- [JWT签名迁移 — 从HS256到RS256/JWKS/KMS](https://dev.devy.dev/posts/jwt-hs256-to-rs256-jwks-kms/)
- [从Datadog迁移到LGTM技术栈](https://dev.devy.dev/posts/lgtm-stack-observability/)

## 联系我

[作品集](https://dev.devy.dev/about/) · [博客](https://dev.devy.dev/) · [邮箱: gurwns1540@gmail.com](mailto:gurwns1540@gmail.com) · [LinkedIn](https://www.linkedin.com/in/%ED%98%81%EC%A4%80-%EC%9C%A4-21a3bb22a/)
