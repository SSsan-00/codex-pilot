# Codex Pilot 利用ガイド

Codex Pilotは、開発タスクの複雑さ・リスク・不確実性・検証難度に合わせて、Codexのモデル、reasoning、Worker、Multi-Agent利用を必要十分な範囲に調整するSkillです。

通常はモデルを毎回選ぶ必要はありません。インストール後は、Codexへ普段どおり開発作業を依頼してください。

既定ではPonytailも必須です。先に導入するか、導入できない環境では`ponytail = "auto"`を明示してください。導入手順は「7. Ponytailを導入する」にあります。

## 1. インストール

### macOS / Linux / WSL

```sh
git clone https://github.com/SSsan-00/codex-pilot.git
mkdir -p "$HOME/.agents/skills"
ln -s "$(pwd)/codex-pilot/skills/codex-pilot" "$HOME/.agents/skills/codex-pilot"
```

すでに`$HOME/.agents/skills/codex-pilot`が存在する場合は上書きしないでください。既存のインストール元を確認してから、更新または削除してください。

### Windows PowerShell

```powershell
git clone https://github.com/SSsan-00/codex-pilot.git
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
New-Item -ItemType SymbolicLink `
  -Path "$HOME\.agents\skills\codex-pilot" `
  -Target "$(Resolve-Path .\codex-pilot\skills\codex-pilot)"
```

Symbolic Linkを作成できない環境では、`codex-pilot\skills\codex-pilot`を`$HOME\.agents\skills\codex-pilot`へコピーできます。コピー方式では、更新時に再コピーが必要です。

## 2. 認識確認

インストール後に新しいCodexタスクを開始します。`/skills`でCodex Pilotを確認するか、次を送信してください。

```text
$codex-pilot route-only: READMEの誤字を1箇所直す作業を分類して
```

ファイルを変更せず、次のような短い判断が返れば利用できます。

```text
Classification: SIMPLE
Recommended: Luna / medium [Luna-2]
Agents: 0
Ultra: unnecessary
Routing confidence: high
```

## 3. 通常利用

Codex Pilotは暗黙選択に対応しています。通常はSkill名を付けずに依頼できます。

```text
このBugを直して、回帰Testも追加してください。
```

確実に利用したい場合は、明示的に指定します。

```text
$codex-pilot このBugを直して、回帰Testも追加してください。
```

Codex Pilotは内部でタスクを分類し、必要な場合だけWorker、強いreasoning、Multi-Agentを使用します。既定では、最終回答に`Routing: NORMAL -> Terra / high [Terra-3] (...)`のような短いRouting判断を1行だけ表示します。`[Terra-3]`はTerra系列内でhighが3段階目という意味で、異なるモデル系列を横断した性能順位ではありません。対応は`low=1`、`medium=2`、`high=3`、`xhigh=4`、`max=5`です。途中経過だけに表示して最終回答から省略することはありません。非表示にする場合は`show_routing = false`を指定します。

## 4. Resource Policyを指定する

一時的な指定は依頼文に含めます。

```text
$codex-pilot balanced policyでこのRefactorを実施して。Ultraは禁止、reasoningはhighまで。
```

利用できるPolicyは次の3つです。

| Policy | 用途 |
| --- | --- |
| `quality` | 既定。正確性と検証を優先 |
| `balanced` | 日常開発で品質と計算量を両立 |
| `throughput` | 正確性を維持できる最低限のResourceを優先 |

継続的な設定が必要な場合は、Repository Rootの`.codex-pilot.toml`または`$CODEX_HOME/codex-pilot.toml`を使用します。[設定例](../examples/codex-pilot.toml)をコピーして必要な値だけ変更してください。Codex本体の`config.toml`へこれらのキーを追加しないでください。

設定の優先順位は次のとおりです。

```text
現在のUser指示
> Repositoryの.codex-pilot.toml
> Userのcodex-pilot.toml
> Codex Pilotの既定値
```

## 5. Routingだけ確認する

実装前に推奨Resourceだけ確認する場合は`route-only`を使用します。

```text
$codex-pilot route-only: 大規模Systemの認証基盤を移行する作業を評価して
```

route-onlyでは、対象の実装、Bug再現、ファイル変更、変更コマンド、Agent起動を行いません。

## 6. Parent Upgradeの提案

Codex Pilotは実行中のParentモデルを勝手に変更しません。限定調査後もRouting Confidenceが低く、現在のParentによる分類または結果統合がbottleneckだと判断できる場合だけ、次のタスクやSession向けに最小限のUpgradeを提案します。

```text
Sol / high -> Sol / xhigh -> Sol / max -> Astra / high -> Astra / xhigh -> Astra / max -> Codex Ultra
```

難しい実装を担当するWorkerのEscalationと、Parent Upgradeは別々に判断されます。

既定では、明らかに簡単な作業に対して既知のParentが過剰に強い場合、完了後に次回向けのDowngrade候補を1行だけ提案します。現在の作業は中断せず、Parentが不明な場合は提案しません。無効にする場合は`suggest_parent_downgrade = false`を指定します。

## 7. Ponytailを導入する

Ponytailは外部依存で、既定の`ponytail = "required"`では必須です。未導入の場合、実装を開始せず不足を通知します。

Ponytailを導入済みなら、実装依頼では`$codex-pilot`だけを指定すれば十分です。`$ponytail`を同じPromptへ重ねて指定する必要はなく、Codex Pilotが対象Codeを理解した後にPonytailを一度だけ読み込みます。`route-only`や説明だけの依頼では読み込みません。

```text
$codex-pilot このBugを最小限の変更で修正し、Testしてください。
```

導入する場合：

```sh
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

新しいCodexタスクを開始し、`/hooks`でPonytailのLifecycle Hookを確認してから、必要なHookだけを信頼してください。Codex PilotはPonytailを最小実装・再利用・YAGNI Reviewに使用します。Ponytailの`ultra`はPonytail自身の強度であり、Codex Ultraやモデル設定ではありません。

Ponytailを任意利用または無効にする例：

```toml
ponytail = "auto"
# または
ponytail = "disabled"
```

## 8. 更新

Symbolic Link方式ではSourceを更新するとSkillにも反映されます。

```sh
cd codex-pilot
git pull --ff-only
```

更新後は新しいCodexタスクを開始してください。Symbolic Link方式では再コピーは不要です。コピー方式では、更新した`skills/codex-pilot`をインストール先へ再コピーしてから新しいタスクを開始します。

Marketplace方式では、現在のCLIにPlugin単体の`update`コマンドがないため、Catalogを更新して同じMarketplace identityを再インストールします。

```sh
codex plugin marketplace upgrade <marketplace-name>
codex plugin remove codex-pilot@<marketplace-name>
codex plugin add codex-pilot@<marketplace-name>
```

その後、新しいCodexタスクを開始してください。

## 9. Uninstall

Symbolic Link方式では、リンク先がこのRepositoryであることを確認してから、そのリンクだけを削除します。Source Repositoryやskills Directory全体を再帰削除しないでください。

macOS / Linux / WSL：

```sh
test -L "$HOME/.agents/skills/codex-pilot" && rm "$HOME/.agents/skills/codex-pilot"
```

Windows PowerShell：

```powershell
$skillLink = "$HOME\.agents\skills\codex-pilot"
if ((Test-Path $skillLink) -and (Get-Item $skillLink).LinkType) {
  Remove-Item $skillLink
}
```

Ponytailを別途導入した場合、その削除はCodex Pilotとは独立しています。

```sh
codex plugin remove ponytail@ponytail
codex plugin marketplace remove ponytail
```

## 10. 制約

- 実行中Parentのモデル・reasoningをすべてのCodex環境で検出または変更できるわけではありません。
- FastやCodex UltraをSkillから直接有効化することはできません。
- 利用可能なモデル名・reasoning・Agent数はHostとAccountによって異なります。
- 暗黙選択はモデル判断のため、確実性が必要な場合は`$codex-pilot`を明示してください。
- Windows Native、WSL、Linuxは実機検証が完了していません。

詳しい設計、Privacy、Troubleshooting、検証範囲は[README](../README.md)と[Compatibility snapshot](compatibility.md)を参照してください。
