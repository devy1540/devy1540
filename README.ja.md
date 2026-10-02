<!-- Edit profile/content.json or profile/header.html, then run python3 scripts/render_readmes.py. -->

<p align="center"><a href="./README.en.md" lang="en">English</a> · <a href="./README.ko.md" lang="ko">한국어</a> · <a href="./README.ja.md" lang="ja">日本語</a> · <a href="./README.zh-CN.md" lang="zh-CN">简体中文</a> · <a href="./README.es.md" lang="es">Español</a> · <a href="./README.fr.md" lang="fr">Français</a></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-hero-dark.svg#locale-ja" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/profile-hero-light.svg#locale-ja" />
    <img src="./assets/profile-hero-light.svg#locale-ja" width="860" alt="Applied AI Engineer | Backend Engineer. AIを活用し、 プロダクトを形に。 設計から実装・運用まで、 自らつくり、検証します。" />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-mobile-dark.svg#locale-ja" />
    <source media="(max-width: 600px)" srcset="./assets/profile-tech-stack-mobile-light.svg#locale-ja" />
    <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-tech-stack-dark.svg#locale-ja" />
    <img src="./assets/profile-tech-stack-light.svg#locale-ja" width="860" alt="Backend: Java, Spring Boot, PostgreSQL, MySQL, Redis. AI: Spring AI; OpenAI, Gemini, Amazon Bedrock; Codex, Claude Code. Infrastructure: Kubernetes, AWS, Google Cloud, Terraform, Grafana." />
  </picture>
</p>

## 自己紹介

ソウルを拠点に、Day1Companyでバックエンドエンジニアとして働いています。

決済・認証・サービス基盤の設計と運用の経験を生かし、AIをプロダクトの機能とチームの開発・運用フローに組み込んでいます。

以前はEXEMで、監視サービスとKafka・Druidによるデータ収集パイプラインを開発していました。

## 主な取り組み

- **AIプロダクト** — Spring AIで診断・フィードバックパイプラインとカスタマーサポートの回答支援を構築しました。診断生成を6〜7分から1〜2分に短縮し、LLMコストを約50%削減しました。 [診断パイプライン](https://dev.devy.dev/about/projects/ai-diagnostic-pipeline/) · [CS回答支援](https://dev.devy.dev/about/projects/cs-automation/)

- **バックエンド** — 決済モジュールと認証を再設計し、マルチチャネル通知を構築しました。PortOneや、GCP KMSによるRS256/JWKS署名を扱っています。 [決済](https://dev.devy.dev/about/projects/payment-system/) · [認証](https://dev.devy.dev/about/projects/auth-refactoring/) · [通知](https://dev.devy.dev/about/projects/notification-server/)

- **インフラ・監視** — ECS→EKSとAWS→GCP/GKEの移行、ArgoCDによるGitOps、OpenTelemetryとLGTMスタックによる監視基盤を構築しました。 [インフラプロジェクト](https://dev.devy.dev/about/projects/infra-modernization/)

## オープンソースプロジェクト

- **[FCP](https://github.com/devy1540/fcp)** — 公式AWS・GCP SDKを接続して、ローカル開発と結合テストに使うGo製クラウドエミュレーター。APIごとの対応範囲、構造化CLI、スナップショットを提供します。

- **[toard](https://github.com/devy1540/toard)** — Claude Code、Codex、CursorなどのAIコーディングツールの使用量・推定コスト・アクティビティをまとめて確認するセルフホスト型ダッシュボード。

- **[Codex Collaboration Conductor](https://github.com/devy1540/codex-collab-conductor)** — タスクの範囲に応じたネイティブサブエージェントへの分担と、根拠に基づくPRレビューを定義するCodexプラグイン。

- **[LLM Wiki](https://github.com/devy1540/ltm-wiki)** — 選択した資料を、出典とリンクのあるMarkdown知識にまとめるCodexプラグイン。プロジェクトごとのWikiをObsidianで管理します。現在はMVP段階です。

- **[JVM Concurrency Benchmark](https://github.com/devy1540/jvm-concurrency-benchmark)** — Platform Thread、Virtual Thread、Kotlin CoroutineをI/O・CPU・高並行性のシナリオで比較する再現可能なベンチマーク。PrometheusとGrafanaで実行メトリクスを確認できます。

## 現在の開発

Slackの依頼を開発・レビュー・検証・デプロイにつなぐエージェント協業フローを改善しています。PRごとの検証を行うE2Eエージェントと、実行記録を点検する監査エージェントは開発中です。 [エージェント業務フローの詳細](https://dev.devy.dev/about/projects/ai-agent-workflow/)

## 開発・運用の進め方

- バックエンドの設計・実装を、必要な画面、テスト、デプロイ、監視までつなぎます。
- エージェントの担当範囲と人が判断する条件を定め、依頼・Issue・PR・デプロイの記録をつなぎます。
- コード、テスト、実行の根拠で完了を確認し、運用反映後の動作も確かめます。

## 技術記事

実装時の選択、運用上の制約、検証結果を韓国語で記録しています。

- [チームの業務ボトルネックを減らすためのAIエージェント活用](https://dev.devy.dev/posts/odin-ax-transformation/)
- [Spring AIによる7段階の診断パイプライン](https://dev.devy.dev/posts/spring-ai-pipeline-real-world/)
- [JWT署名の移行 — HS256からRS256/JWKS/KMSへ](https://dev.devy.dev/posts/jwt-hs256-to-rs256-jwks-kms/)
- [DatadogからLGTMスタックへの移行](https://dev.devy.dev/posts/lgtm-stack-observability/)

## 連絡先

[ポートフォリオ](https://dev.devy.dev/about/) · [ブログ](https://dev.devy.dev/) · [メール: gurwns1540@gmail.com](mailto:gurwns1540@gmail.com) · [LinkedIn](https://www.linkedin.com/in/%ED%98%81%EC%A4%80-%EC%9C%A4-21a3bb22a/)
