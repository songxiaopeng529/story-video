#!/usr/bin/env python3
"""Generate five Seedream keyframes for the friends-dinner episode."""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional


PROJECT_DIR = Path(__file__).resolve().parent
ANCHOR_DIR = PROJECT_DIR / "anchors"


def load_env_file(env_file: Path) -> None:
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if name.startswith("export "):
            name = name.removeprefix("export ").strip()
        os.environ[name] = value.strip().strip("'\"")


load_env_file(Path.home() / ".config/story-video/seedream.env")
load_env_file(PROJECT_DIR / ".env.local")

MODEL = (
    os.getenv("SEEDREAM_ENDPOINT_ID")
    or os.getenv("SEEDREAM_MODEL")
    or "doubao-seedream-5-0-260128"
)
API_BASE = os.getenv(
    "ARK_BASE_URL",
    os.getenv("MODEL_IMAGE_API_BASE", "https://ark.cn-beijing.volces.com/api/v3"),
).rstrip("/")
API_BASE = API_BASE.replace("/api/coding/v3", "/api/v3")

COMMON_PROMPT = """
生成一张写实、温馨、精致的微缩住宅生活摄影，原生 9:16 竖图。
输入图是建筑布局蓝本。严格保留完整椭圆形白色住宅、外围花园、画面底部唯一木门、
中央白色曲线结构和圆形天井、左侧木质书桌、右侧弧形厨房、左下弧形沙发、
右下圆形餐桌的原始位置、比例、数量、透视和材质。
右侧厨房必须保持输入图原有的贴墙弧形布局。厨房只有沿右侧外墙连续延伸的
现有石材操作台，水槽嵌在这段贴墙操作台中；菜盘只能放在水槽左右两侧的
现有台面上。厨房与圆餐桌之间必须保持完整、开阔、无障碍的地面通道。
严禁从厨房向餐厅方向新增或伸出任何板状结构，严禁新增半岛、岛台、吧台、
餐台、悬空木板、搁板、推车或第二层台面。

只允许对画面顶部睡眠区做一次明确的建筑升级，并在后续全部图片中永久保持：
顶部卧室向左右和下方适度扩大，约占室内面积的四分之一，形成更宽敞的主卧，
但仍只保留一张双人床；
在主卧右侧设置一间明显可见、面积更大的独立卫生间。卫生间不能紧贴床，
床右边缘与卫生间玻璃墙之间必须留出约一米宽、清楚可见的空白步行过道，
让卫生间视觉上离睡床更远。卫生间采用完整透明玻璃隔墙和玻璃门，面积约为
原参考卫生间的一点五倍，内部清楚分为洗手台、马桶和独立玻璃淋浴区三个区域。
卫生间朝向卧室和室内过道的全部边界必须由通高、无框、清透玻璃构成，
从床边到卫生间入口之间不能有任何白色灰泥实体墙、半墙、厚墙、挡板、立柱或壁龛；
只允许房屋最外圈的弧形外墙保持白色实体材质。玻璃隔断必须连续通透，
透过玻璃能完整看见洗手台、马桶和淋浴区，结构与后续关键帧完全一致。
卫生间必须位于卧室右上区域，不能消失，不能缩成壁龛，不能被改成衣柜或空墙。
从正上方必须能同时清楚识别玻璃隔墙、玻璃门、洗手台、马桶和独立淋浴区。
这间卫生间是五张关键帧共同的永久建筑结构，每一张图都必须完整保留且清楚可见。
扩大卧室和卫生间时只微调顶部区域，不能挤压或移动中央天井、厨房、餐厅和客厅。

摄影机始终固定在房屋正上方，完整房屋与外围花园全部入画，焦距和构图不变。
故事发生在明亮温暖的周末午后，自然阳光柔和，米白灰泥、浅木和鼠尾草绿配色。

全屋恰好只有四位 23 至 26 岁的年轻东亚成年人，两男两女。四人面容年轻清爽，
身形自然利落，有都市年轻情侣的生活感，不成熟老气，不幼态。移除输入图中床上的
人物和虎斑猫，卧室保持无人且整洁。四位人物必须是房屋中的微小生活尺度：
男主人约 26 岁，短黑发，白色亚麻衬衫挽袖、黑色直筒长裤、现代剪裁鼠尾草绿围裙；
女主人约 24 岁，深色锁骨发，象牙白方领修身针织上衣、陶土红高腰 A 字中长裙、
小巧金色耳饰和棕色乐福鞋，轻法式、时尚但适合居家；
男客人约 25 岁，短黑发，天蓝色宽松衬衫外套、白色 T 恤、米色直筒裤和白色运动鞋；
女客人约 23 岁，低马尾，灰粉色短款针织开衫、白色内搭、炭灰百褶中长裙、
小巧耳饰和黑色玛丽珍鞋，年轻精致但不过度正式。
保持四人的脸、发型、体型和整套服装稳定，动作自然克制，不面对摄影机摆拍，
不穿职业套装，不穿显老宽松针织衫，不使用夸张性感或礼服造型。

除上述顶部卧室与卫生间升级外，禁止改变其他户型；禁止裁掉外墙或花园，
禁止放大其他局部房间，禁止移动或复制家具，禁止新增屋顶、第二张床、
第二套餐桌、第二个厨房或第二个卫生间。
禁止改变右侧贴墙弧形厨房的轮廓，禁止在厨房和餐桌之间生成伸出板、半岛或岛台。
禁止儿童、第五个人、重复人物、额外宠物、床上人物、穿墙、悬浮、人物重叠、
肢体畸形、文字、字幕、品牌标志、水印、黑边和白边。
如果人物动作与建筑一致性冲突，优先保持完整户型、扩大后的卧室、
独立大卫生间、固定机位和人物数量。
""".strip()

ANCHORS = [
    {
        "filename": "00s-opening.png",
        "prompt": """
这是 30 秒故事的 00:00 开场状态。关键菜肴动线规则：所有菜必须先在右侧弧形厨房
操作台面上做好、码好，再由四人分批端到右下圆餐桌，严禁凭空出现。
本帧卧室右侧卫生间必须与 08s、14s、21s、27s 的透明玻璃卫生间完全相同：
面向双人床和室内过道的一整面边界全部改为通高无框透明玻璃与玻璃门，
删除床与卫生间之间现有的白色实体隔墙，严禁保留任何灰泥墙、半墙或厚挡板。
这里的厨房操作台专指沿右侧外墙、带嵌入式水槽的原有弧形石材台面，
不是向餐厅伸出的新板子。四盘菜全部放在水槽左右两侧的现有贴墙台面上，
厨房与餐桌之间保持空旷地面，绝对不能新增伸出板、半岛、岛台或吧台。
当前画面：这段现有贴墙台面上清楚码放着四盘已经做好的家常菜——
一大盘清蒸鱼（正中）、一盘红烧排骨（红亮浓郁）、一盘翠绿蒜蓉西兰花、
一碗番茄蛋汤（冒热气），四个盘碗都装满真实食物，沿水槽两侧整齐摆放，
绝对不能让厨房台面是空的。男主人身穿白T和绿色围裙，站在厨房操作台内侧，
正伸出双手准备端起其中一盘（清蒸鱼）往餐桌方向移动——他在"端菜"，
不是在炒菜装盘。女主人坐在左下弧形沙发靠近入口的一端，刚听见声音，
微微转头看向底部入口。男客人和女客人并肩站在房屋底部唯一木门外，
面向入口；男客人抬起一只手准备敲门。右下圆餐桌只有四套餐具、四只水杯和
简单桌布，菜品尚未摆上，绝对不能有任何菜盘。其他区域无人。
""",
    },
    {
        "filename": "08s-welcome.png",
        "prompt": """
这是同一房屋、同一午后、同四个人的 00:08 状态，只改变人物位置和入口门状态。
关键菜肴动线规则延续 00s：右侧弧形厨房操作台面上，刚才那四盘已经做好的菜
（清蒸鱼、红烧排骨、蒜蓉西兰花、番茄蛋汤）仍然原封不动摆在原处，每盘都满，
必须清楚可见，不能减少、不能消失。菜仍只放在水槽两侧的原有贴墙石材台面，
厨房与餐桌之间没有伸出板、半岛、岛台或吧台。底部唯一木门已经打开。女主人站在门内侧
并侧身欢迎；男客人刚跨过门槛进入室内；女客人紧跟在男客人身后，仍靠近门口。
男主人仍在右侧厨房内，身体转向门口看他们，但没有离开厨房，双手可以空着
或仍扶在台面上的菜盘边。右下圆餐桌仍只有餐具水杯，没有任何菜盘，
严禁菜盘凭空出现。四人互不重叠，沿现有通道站立。
""",
    },
    {
        "filename": "14s-serving.png",
        "prompt": """
这是同一房屋、同一午后、同四个人的 00:14 状态，只改变人物动作和位置。
关键菜肴动线规则：四人手中端的菜必须是 00s/08s 厨房台面那四盘已做好的菜，
加上一个水果拼盘，来源必须明确，数量必须对上（厨房原有 4 菜 + 1 果盘 = 共 5 份）。
底部入口门已经关闭。水槽两侧的原有贴墙厨房台面上还剩 1-2 盘没端完
（暗示正从厨房端向餐桌）；厨房与餐桌之间仍是空旷通道，没有伸出板或岛台。
男主人从右侧厨房向右下圆餐桌移动，双手端着那一大盘清蒸鱼；
女主人位于厨房与餐桌之间，双手端着红烧排骨；男客人靠近圆餐桌，
一只手端蒜蓉西兰花、另一只手端番茄蛋汤；
女客人位于餐桌另一侧，双手端着水果拼盘（葡萄、西瓜、橙子）
另加四只小碗米饭。四人共同端菜，动作自然，沿现有通道分散站立，
不重叠、不穿墙，尚未坐下。右下圆餐桌上已经摆好了 1-2 盘
（正是前面几人刚端过来的，来源可追溯）。人物数量是本图最高优先级：
必须同时清楚看见四具完整身体，逐一可辨认出绿色围裙男主人、象牙白方领上衣和
陶土红长裙女主人、天蓝衬衫外套男客人、灰粉短开衫和炭灰百褶裙女客人，
一个都不能缺少。
""",
    },
    {
        "filename": "21s-dining.png",
        "prompt": """
这是同一房屋、同一午后、同四个人的 00:21 状态，只改变人物姿势和餐桌上的菜品。
关键菜肴动线规则：桌上的菜全部是 00s 厨房台面原有的那四菜加一果盘端过来的，
合计五份，必须如数端上桌且每盘都满。
四个人分别坐在右下圆餐桌的四个不同座位。男主人坐在靠厨房的一侧，仍穿绿色围裙，
微微抬手与朋友说话（约打球台词阶段）；女主人坐在他相邻的位置；
男客人和女客人坐在桌子另一侧。桌面必须丰盛且每盘菜都满：俯视角度清楚看到
四个独立菜盘 + 一个果盘 = 共五份食物——正中一大盘清蒸鱼、一盘红烧排骨
（红亮浓郁）、一盘翠绿蒜蓉西兰花、一大碗番茄蛋汤（冒热气），外围还有
一个水果拼盘（葡萄西瓜橙子）、四只装着米饭的小碗、四只玻璃水杯
（半满柠檬水插柠檬片）。合计：4 菜 + 1 果盘，不多不少，来源与 14s 端菜一致。
四人正在自然夹菜和聊天，没有任何人站立，入口门关闭，其他房间无人。
圆桌虽然有六把椅子，但只能有四把椅子坐人，另外两把椅子必须清楚保持空置。
画面必须恰好四人：绿色围裙男主人一人、象牙白上衣和陶土红裙女主人一人、
天蓝外套男客人一人、灰粉短开衫女客人一人。严禁第五个人，
严禁复制任何一位女性，严禁灰色衣服的额外角色，严禁只有1-2个菜。
""",
    },
    {
        "filename": "27s-group-photo.png",
        "prompt": """
这是同一房屋、同一午后、同四个人的 00:27 状态，只改变餐桌旁人物姿势。
关键菜肴动线规则：桌上的菜必须与 21s 完全一致，不能减少、不能变空——
四个菜盘（清蒸鱼、红烧排骨、蒜蓉西兰花、番茄蛋汤）+ 一个水果拼盘 +
四碗米饭 + 四只玻璃水杯，每份都满，必须清楚可见。严禁只剩 1-2 个菜、
严禁盘子变空、严禁凭空多出新菜。男主人在靠厨房的座位旁站起半步，
仍穿绿色围裙，一只手将手机举向圆桌中央准备自拍。女主人、男客人、
女客人仍在各自座位附近，身体自然向桌心靠拢，抬头看向手机并轻松微笑。
这是吃饭中途临时拍照，不是整齐摆拍。只有男主人手里有一部手机。画面必须恰好
四个人，四个人都必须清楚可见且身体不能互相遮挡：绿色围裙男主人在餐桌上方站立
举手机，象牙白上衣和陶土红裙女主人在餐桌左上方，天蓝外套男客人必须保留在
餐桌左下方，灰粉短开衫和炭灰百褶裙女客人在餐桌右侧。只有这两男两女；
圆桌其余两把椅子保持空置，
严禁省略蓝衣男客人，严禁第五个人或重复女性，严禁餐桌菜品减少。
""",
    },
]


def api_key() -> str:
    key = (
        os.getenv("ARK_API_KEY")
        or os.getenv("MODEL_IMAGE_API_KEY")
        or os.getenv("MODEL_AGENT_API_KEY")
    )
    if not key:
        raise RuntimeError(
            "Missing API key. Set ARK_API_KEY, MODEL_IMAGE_API_KEY, "
            "or MODEL_AGENT_API_KEY."
        )
    return key


def image_data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def request_image(prompt: str, reference: Path, timeout: int) -> bytes:
    body = {
        "model": MODEL,
        "prompt": f"{COMMON_PROMPT}\n\n当前关键帧要求：\n{prompt.strip()}",
        "image": image_data_uri(reference),
        "size": "2K",
        "response_format": "b64_json",
        "watermark": False,
        "optimize_prompt_options": {"mode": "standard"},
    }
    if "seedream-4-0" not in MODEL and "seedream-4-5" not in MODEL:
        body["output_format"] = "png"
    request = urllib.request.Request(
        f"{API_BASE}/images/generations",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Seedream HTTP {error.code}: {details}") from error

    if payload.get("error"):
        raise RuntimeError(json.dumps(payload["error"], ensure_ascii=False))

    data = payload.get("data") or []
    if not data:
        raise RuntimeError("Seedream returned no image data.")

    first = data[0]
    if first.get("b64_json"):
        return base64.b64decode(first["b64_json"])
    if first.get("url"):
        with urllib.request.urlopen(first["url"], timeout=timeout) as response:
            return response.read()
    raise RuntimeError("Seedream response contains neither b64_json nor URL.")


def generate(force: bool, timeout: int, stop_after: Optional[int]) -> None:
    ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
    reference = PROJECT_DIR / "00-layout-reference.png"

    for index, anchor in enumerate(ANCHORS, start=1):
        output = ANCHOR_DIR / anchor["filename"]
        if output.exists() and not force:
            print(f"[{index}/{len(ANCHORS)}] keep {output.name}")
            reference = output
            if stop_after is not None and index >= stop_after:
                return
            continue

        print(f"[{index}/{len(ANCHORS)}] generating {output.name}")
        for attempt in range(1, 4):
            try:
                image = request_image(anchor["prompt"], reference, timeout)
                output.write_bytes(image)
                print(f"[{index}/{len(ANCHORS)}] saved {output}")
                reference = output
                break
            except (
                OSError,
                urllib.error.URLError,
                urllib.error.HTTPError,
                RuntimeError,
            ) as error:
                if "ModelIDAccessDisabled" in str(error):
                    raise RuntimeError(
                        "This Ark account requires a custom endpoint ID. "
                        "Set SEEDREAM_ENDPOINT_ID=ep-... and run again."
                    ) from error
                if "AccessDenied" in str(error):
                    raise RuntimeError(
                        "ARK_API_KEY cannot access this endpoint. Use an API key "
                        "from the same Ark account and project."
                    ) from error
                if attempt == 3:
                    raise RuntimeError(
                        f"Failed to generate {output.name}: {error}"
                    ) from error
                wait_seconds = attempt * 5
                print(
                    f"[{index}/{len(ANCHORS)}] attempt {attempt} failed; "
                    f"retrying in {wait_seconds}s"
                )
                time.sleep(wait_seconds)
        if stop_after is not None and index >= stop_after:
            return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate and overwrite existing anchor images.",
    )
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument(
        "--stop-after",
        type=int,
        choices=range(1, len(ANCHORS) + 1),
        help="Stop after generating or keeping the given anchor number.",
    )
    args = parser.parse_args()
    generate(force=args.force, timeout=args.timeout, stop_after=args.stop_after)


if __name__ == "__main__":
    main()
