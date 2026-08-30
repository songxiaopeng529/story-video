# 锚点图生成提示

四张图片均使用内置图像生成能力完成。第一张是新图生成，后三张以前一张为编辑目标，只改变指定状态，保持摄影机、户型、人物和道具连续。

## 00s｜下班后睡着

用途：整条视频的母图、首帧和唯一摄影机参考。

生成提示：

Create a visually striking but emotionally recognizable opening image for “After She Fell Asleep, the Room Finished the Day for Her.” Show a beautiful compact double-height urban LOFT apartment at 1 a.m. as a clean architectural cutaway from a fixed high three-quarter overhead camera, vertical 9:16. A huge floor-to-ceiling window reveals a real rainy residential city at night, with cold blue-gray rain outside and warm honey light inside. One clearly adult East Asian woman in her late twenties has fallen asleep curled on the sofa, still wearing a cream blouse, charcoal trousers and socks, face turned naturally into the cushion.

By the door include a rain-soaked pale-yellow raincoat, white commuter e-bike helmet, wet dark shoes, a small puddle, tote bag and office badge without readable text. On the low table include a half-eaten cold bowl of convenience-store noodles and an unplugged phone beside its cable. Keep an open glowing laptop on the desk, a folded cream blanket on the sofa back, and one small orange tabby cat watching from the bottom stair. Premium cinematic photorealism, lived-in and attainable, not a luxury showroom. No magic yet, no text, no logo, no watermark. Avoid cyberpunk, steampunk, sci-fi, extra people, glamorous posing and excessive clutter.

成品：anchors/00s-after-work-asleep.png

## 06s｜玄关开始烘干

用途：第一段尾帧、第二段首帧。

编辑提示：

Preserve the exact camera, crop, apartment architecture, rainy city, furniture, sleeping woman’s identity, clothing and pose, cat position, color grade and photorealistic style. Change only the entry-area care action: turn on a subtle warm honey-colored floor-heating glow beneath the wet shoes, helmet and raincoat. Make the puddle slightly smaller at its edges. Add fine realistic water vapor rising gently from the wet items. Keep the laptop lit, cold noodles unchanged, woman asleep and cat still. No flames, sparks, sci-fi rings, magical beams, excessive steam, new objects, camera motion, text, logo or watermark.

成品：anchors/06s-entry-drying.png

## 13s｜未完成的事情被收好

用途：第二段尾帧、第三段首帧。

编辑提示：

Preserve the exact camera, crop, apartment geometry, stormy city view, furniture and object locations, entry drying glow, sleeping woman’s identity, clothing and pose, cat location and cinematic color grade. Advance only the quiet care actions: turn the laptop screen completely dark; connect the phone on the coffee table to its nearby charging cable with one tiny soft green status light and no readable symbol; add a gentle plume of warm steam to the same noodle bowl; make the entrance puddle visibly smaller and reduce the vapor to faint wisps. Keep the woman asleep and the cat still. Avoid floating objects, magical beams, visible robots, excessive steam, rearranged furniture, camera movement, text, logo or watermark.

成品：anchors/13s-day-being-finished.png

## 20s｜安全入睡

用途：第三段尾帧、最终 4 秒冻结底板。

编辑提示：

Preserve the exact camera, crop, apartment architecture, rainy city, furniture, all major object locations, sleeping woman’s identity, clothing and body pose, cat identity and stair location, materials and color grade. Advance only the final bedtime care: unfold the cream blanket from the sofa back over the sleeping woman’s shoulders, torso and legs while following her existing curled pose; keep the cat on the same stair but curl it asleep; make the entry floor fully dry and switch off the drying glow; keep the laptop dark, phone charging and only a small curl of warmth above the noodles. Dim the desk lamp and most kitchen lights, leaving a restrained amber bedside lamp, faint kitchen glow and warm pool around the sofa. No helper, no magical creature, no new furniture, no camera move, no text, no logo or watermark.

成品：anchors/20s-safe-asleep.png

## 全局连续性负面词

Extra people, woman waking up, walking, hand gestures, lip movement, face change, clothing change, cat walking or jumping, duplicated objects, floating props, rain entering the room, new puddles, furniture drift, duplicate stairs, warped railing, melting walls, window deformation, light flicker, exposure pumping, camera push, camera pull, zoom, pan, tilt, rotation, depth-of-field change, cyberpunk neon, steampunk machinery, text, logo, watermark, black border, white border.

