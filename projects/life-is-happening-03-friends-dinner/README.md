# 《日子正在发生》03｜朋友来家吃饭

## 项目定位

- 平台：抖音
- 画幅：原生 `9:16`
- 时长：严格 `30.0s`
- 形式：完整住宅固定上帝视角，四个成年小人在房间中连续表演
- 核心情绪：朋友到家、一起端菜、围桌吃饭、临时合照的轻松与温暖

## 文件结构

- `00-layout-reference.png`：从上一项目复制的户型参考，只用于锁定房屋结构、家具、材质和构图。
- `01-anchor-image-prompts.md`：五张动作锚点图的用途、人物位置和验收要求。
- `30s-fixed-overhead.md`：完整 30 秒剧情、对白、视频提示词和验收清单。
- `generate_anchor_images.py`：调用 Seedream 5.0 生成五张锚点图。
- `anchors/00s-opening.png`：开场，男主在厨房、女主在沙发、朋友在门外。
- `anchors/08s-welcome.png`：女主开门迎接朋友。
- `anchors/14s-serving.png`：四人协作端菜。
- `anchors/21s-dining.png`：四人围桌吃饭。
- `anchors/27s-group-photo.png`：男主举手机拍合照。

## API Key 配置

生成脚本按顺序读取 `ARK_API_KEY`、`MODEL_IMAGE_API_KEY`、`MODEL_AGENT_API_KEY`。推荐只配置 `ARK_API_KEY`。

仅对当前终端生效：

```bash
export ARK_API_KEY='你的火山方舟 API Key'
```

推荐写入全局私有配置，供所有项目复用：

```bash
mkdir -p ~/.config/story-video
cat > ~/.config/story-video/seedream.env <<'EOF'
export ARK_API_KEY='你的火山方舟 API Key'
export SEEDREAM_ENDPOINT_ID='ep-xxxxxxxx'
EOF
chmod 600 ~/.config/story-video/seedream.env
```

在 `~/.zshrc` 中加载该配置：

```bash
[[ -r "$HOME/.config/story-video/seedream.env" ]] && \
  source "$HOME/.config/story-video/seedream.env"
```

当前账号还要求通过自定义在线推理接入点调用模型。打开
[火山方舟创建推理接入点](https://console.volcengine.com/ark/region:cn-beijing/endpoint/create)，
选择 Seedream 5.0、按 Token 付费，创建后等待状态变为“健康”。复制形如
`ep-xxxxxxxx` 的接入点 ID，并写入上述全局配置。

确认两项配置都存在：

```bash
source ~/.config/story-video/seedream.env
test -n "$ARK_API_KEY" && echo "ARK_API_KEY is set"
test -n "$SEEDREAM_ENDPOINT_ID" && echo "SEEDREAM_ENDPOINT_ID is set"
```

不要把真实密钥写入项目、Markdown、Git 配置或生成提示词。生成脚本会自动读取
`~/.config/story-video/seedream.env`。API Key 与 Endpoint 必须属于同一个火山方舟账号和
项目，否则接口会返回 `403 AccessDenied`。

## 生成方法

在仓库根目录运行：

```bash
python3 projects/life-is-happening-03-friends-dinner/generate_anchor_images.py
```

默认使用 Seedream 5.0、PNG、无水印和 `2K` 尺寸。脚本先生成开场锚点，再以开场锚点为人物与空间参考，依次生成后续四张图片。

如需覆盖已经存在的图片：

```bash
python3 projects/life-is-happening-03-friends-dinner/generate_anchor_images.py --force
```

## 推荐制作顺序

1. 检查 `00-layout-reference.png` 的完整户型和固定上帝视角。
2. 生成并验收五张 `anchors/*.png`。
3. 以相邻锚点作为每个视频片段的首尾状态，分别生成 `0–8s`、`8–14s`、`14–21s`、`21–27s`、`27–30s`。
4. 剪辑时按动作连续硬切，并统一添加对白、环境声与 BGM。
5. 最终检查四个人物数量、服装、位置、家具和光线是否连续。
