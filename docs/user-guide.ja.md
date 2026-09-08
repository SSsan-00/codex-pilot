# Codex Pilot 利用ガイド — 0.4

Codex Pilotは開発タスクに必要な実行能力・調査・委譲・検証を判断する薄いPolicy Skillです。実行中Parentの自動切替や外部ツール管理は行いません。

## 導入・更新

[READMEの導入手順](../README.md#installation)でSkillをリンクまたはコピーします。Ponytailや外部MCPの導入は必須ではありません。更新時はソースの変更を確認した上で実行します。

```sh
git pull --ff-only
```

リンク方式は再コピー不要です。コピー方式は更新した `skills/codex-pilot` を再コピーします。Marketplace方式はインストール元の同じカタログとHost標準の更新手順を使用します。いずれも更新後に新しいタスクを開始してください。

アンインストールは、このソースを指すリンクであることを確認してリンクのみ削除するか、Host標準のPlugin削除を使用します。

## 使い方

```text
$codex-pilot このBugを修正し、影響範囲を検証してください。
$codex-pilot route-only: 現行ASP.NET Core APIを使う複数モジュールの変更を評価して。
```

route-onlyは提案内容だけを分類し、対象ファイル調査・実装・依存診断・Worker起動を行いません。

```text
Classification: COMPLEX
Recommended: strong capability
Capabilities: semantic_navigation, current_documentation
Agents: 1 bounded investigator
Reasons: multi-module impact; version-dependent behavior
```

通常の最終Routingは推奨実行能力を表し、現在のモデルを変更した証拠ではありません。使用した能力だけを追記します。必要な能力が利用できず検証に制約があれば、本文で説明します。

```text
Routing: COMPLEX -> strong capability | Capabilities: semantic_navigation
```

Workerを実際に使った場合は同じ行へ `Workers: review=<実モデルID> / <reasoning>` を追記します。観測できない値は `unknown` とします。

## 完了の防御策

Codex Pilotは、次のすべてを満たす場合だけ完了として報告します。

- 依頼された受入条件を満たした
- 関連する検証が成功した、またはUserが明示的に省略した
- 必要な分析に十分な代替手段があり、その結果を確認した
- 重要なRiskや未解決事項が残っていない

1つでも満たさなければ、`Status: partial`または`Status: blocked`として、不足している条件と次の安全な確認を報告します。弱いParent、利用不能なWorker、UserのResource制限、検証失敗、必要なCapabilityの不足を、完了扱いに変換しません。

## 能力と検証

- semantic_navigation：呼び出し関係や複数ファイルの流れを調べる場合。
- current_documentation：現行・バージョン依存のframework、SDK、APIを扱う場合。
- context_compression：大量の反復ログを扱う場合。元ログを保持し、重要なエラーを原文で確認。
- security_analysis：認証・認可、入力境界、秘密情報などの安全性を扱う場合。

Serena、Context7、Headroom、SemgrepはProviderの例です。特定製品の有無ではなく、代替手段で必要な分析と検証を満たせるかを判断します。README誤字の修正ではどれも不要です。

小変更は対象確認、通常変更は関連テスト、複雑な変更は必要な範囲の追加検証、重大変更は重要な前提の独立確認を行います。Workerは独立作業がある場合だけ使用し、既定上限は再試行を含め2体です。

## 設定と0.3からの移行

```toml
policy = "quality"
max_agents = 2
show_routing = true
```

設定は任意です。Repositoryの `.codex-pilot.toml`、Userの `$CODEX_HOME/codex-pilot.toml` の順で参照し、現在の依頼文を最優先します。Codex本体の `config.toml` にPilot設定を追加しないでください。

0.4では上記3キーだけが有効です。[廃止キー一覧](../skills/codex-pilot/references/configuration.md#migration-from-03)の旧設定は無視されるため、継続したいモデル・reasoning・実行モード制限は依頼文やHost設定へ移してください。既存ファイルは自動変更しません。

Parent昇降格提案、独自強度番号、多段階昇格、Ponytail必須化は廃止しました。未解決の意味ある失敗に対して、根拠のある強い実行での再試行は1回までです。Ponytailは任意の補助として利用できます。

品質・token削減の効果はまだ実測比較していません。[評価手順](../evals/README.md)と[検証範囲](verification.md)を参照してください。
