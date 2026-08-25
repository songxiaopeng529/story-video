# Story Video

[English](README.md)

一个开源的 Agent Skill：把主题、文章、产品资料、创意简报或粗稿，转成可以直接拍摄或录制的视频脚本。

`write-video-scripts` 支持短视频、口播、科普、教程、产品演示、广告、采访、纪录片和剧情短片。它会把旁白/对白、画面动作、屏幕文字、声音、时长、事实核验和制作限制清晰分开。

## 特点

- 输出可执行的拍摄脚本，而不是给普通文章简单加镜头标签
- 根据目标、受众、平台、时长和形式调整叙事与节奏
- 跟随用户语言，支持中文、英文及其他语言
- 信息不全时采用克制的合理默认值，减少无意义追问
- 检查时长、口语自然度、画面可拍性、事实、版权和安全风险
- 遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)
- 提供可选的 OpenAI `agents/openai.yaml` 界面元数据
- 不依赖运行时包、API Key 或特定模型工具

## 安装

把 Skill 目录复制到兼容客户端的技能目录。Codex 用户可在仓库根目录执行：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/write-video-scripts "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后开启一个新任务，让客户端重新发现 Skill。其他兼容 Agent Skills 的客户端可能使用不同目录；复制同一个 `skills/write-video-scripts` 文件夹即可，不要修改目录名。

## 使用

可以显式调用：

```text
使用 $write-video-scripts 给一家社区咖啡店写一条 45 秒竖屏视频。
只能一位店员、一个店内场景，语气轻松，结尾引导收藏。
```

也可以直接自然描述需求：

```text
把这份产品资料改成 3 分钟 B 站科普脚本，需要旁白、分镜和屏幕文字，
不能增加资料里没有的性能数据。
```

```text
把这份 90 秒脚本压到 60 秒，保留结尾的情绪回报，加强前三秒，
并只解释关键改动。
```

默认交付带时间码的完整制作脚本；如果用户只需要口播、结构大纲或改稿，Skill 会切换到更合适的格式。

## 默认输出

完整制作脚本可以包含：

- 创作简报与关键假设
- 连续的预计时间段
- 镜头与画面动作
- 旁白或对白
- 屏幕文字
- 音乐、音效和转场
- 人物、场景、道具与素材提示
- 已核验事实、来源与待确认项
- 简洁的交付检查

可以查看[中文咖啡店示例](examples/coffee-shop-45s.zh-CN.md)。示例展示的是结构与质量目标，不要求模型逐字复现。

## 仓库结构

```text
story-video/
├── skills/write-video-scripts/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── evals/cases.json
├── examples/
├── scripts/validate_repo.py
└── .github/workflows/validate.yml
```

主 `SKILL.md` 保持精炼；格式打法、交付模板、事实安全规则和质量量表只在需要时加载，符合开放规范的渐进披露原则。

## 校验

运行仓库自带的离线校验：

```bash
python3 scripts/validate_repo.py
```

校验范围包括开源健康文件、frontmatter 与命名、OpenAI 元数据、相对链接、引用资源、未清理占位符和评测语料。

还可以按 Agent Skills 官方文档运行参考校验器：

```bash
skills-ref validate skills/write-video-scripts
```

官方 `skills-ref` 定位为演示性参考实现，不是生产依赖，因此本仓库 CI 使用自包含校验。

## 评测策略

`evals/cases.json` 覆盖以下场景：

- 制作条件受限的 45 秒短视频
- 必须忠于原始资料的长视频改编
- 双人竖屏微短剧
- 信息刻意不完整的泛需求
- 含虚假背书和医疗承诺的高风险广告需求

评测关注约束覆盖、不编造事实、默认值是否合理、制作是否可执行，以及能否安全转换需求；不采用脆弱的整篇逐字匹配。

## 安全与限制

本 Skill 不负责实际生成、剪辑或发布视频。脚本时长在真人试读或剪辑确认前都只是估算。平台最新限制和受监管声明仍应查询权威来源。Skill 会标记没有依据的主张，不会编造证据，也会避免虚假真人背书、危险保证、精准模仿在世创作者，以及默认使用未授权素材。

安全问题请查看 [SECURITY.md](SECURITY.md)。

## 参与贡献

欢迎贡献。提交 Pull Request 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)，并运行本地校验。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)。
