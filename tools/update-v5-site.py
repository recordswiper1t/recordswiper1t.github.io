#!/usr/bin/env python3
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, found {count}")
    return text.replace(old, new, 1)


# Root menu: point iPhone users at the new fast V5 player.
p = Path("index.html")
s = p.read_text(encoding="utf-8")
s = s.replace("Fast V4 — best for iPhone", "Fast V5 — best for iPhone")
s = s.replace("Use ⋯ → Fast V4 for the lighter iPhone player", "Use ⋯ → Fast V5 for the lighter iPhone player")
p.write_text(s, encoding="utf-8", newline="\n")

# Fast player: direct same-origin V5 URL load, low visual quality by default on iOS.
p = Path("mod/fast.html")
s = p.read_text(encoding="utf-8")
s = s.replace("Fast V4", "Fast V5")
s = s.replace("optimized V4", "optimized V5")
s = s.replace("V4_URL='/assets/kingdom-rush-frontiers-v4.swf'", "V5_URL='/assets/kingdom-rush-frontiers-v5.swf'")
s = s.replace("fetch(V4_URL,{cache:'force-cache'})", "fetch(V5_URL,{cache:'force-cache'})")
s = s.replace("V4 asset unavailable", "V5 asset unavailable")
s = s.replace("Loading V4 • ", "Loading V5 • ")
s = s.replace("Fast V4 • ", "Fast V5 • ")
s = replace_once(
    s,
    "const resp=await fetch(V5_URL,{cache:'force-cache'});if(!resp.ok)throw new Error('V5 asset unavailable (HTTP '+resp.status+')');const data=await resp.arrayBuffer();const p=player||makePlayer();await p.ruffle().load({data,",
    "const p=player||makePlayer();await p.ruffle().load({url:V5_URL,",
    "Fast V5 direct URL loading",
)
p.write_text(s, encoding="utf-8", newline="\n")

# Existing Mod Lab player: keep historical installers, but make the player itself
# cheaper on iPhone and surface V5 Fast as the recommended path.
p = Path("mod/index.html")
s = p.read_text(encoding="utf-8")
s = replace_once(s, "<title>Kingdom Rush Frontiers — V4 Sandbox + Stability</title>", "<title>Kingdom Rush Frontiers — V5 Fast + Mod Lab</title>", "mod title")
s = replace_once(
    s,
    "#menuToggle{position:fixed;z-index:80;top:max(8px,env(safe-area-inset-top));right:max(8px,env(safe-area-inset-right));width:48px;height:48px;min-height:48px;padding:0;border:1px solid rgba(255,255,255,.25);border-radius:14px;background:rgba(20,20,20,.78);color:#fff;font-size:25px;backdrop-filter:blur(10px);touch-action:manipulation}",
    "#menuToggle{position:fixed;z-index:80;top:max(8px,env(safe-area-inset-top));right:max(8px,env(safe-area-inset-right));width:48px;height:48px;min-height:48px;padding:0;border:1px solid rgba(255,255,255,.25);border-radius:14px;background:#151515;color:#fff;font-size:25px;touch-action:manipulation;contain:layout paint style}",
    "menu compositing",
)
s = replace_once(
    s,
    "#panel{position:fixed;z-index:79;top:calc(max(8px,env(safe-area-inset-top)) + 54px);right:max(8px,env(safe-area-inset-right));display:none;gap:9px;width:min(285px,calc(100vw - 16px));max-height:calc(100dvh - 80px);overflow:auto;padding:10px;border:1px solid rgba(255,255,255,.2);border-radius:15px;background:rgba(15,15,15,.95);backdrop-filter:blur(12px)}",
    "#panel{position:fixed;z-index:79;top:calc(max(8px,env(safe-area-inset-top)) + 54px);right:max(8px,env(safe-area-inset-right));display:none;gap:9px;width:min(285px,calc(100vw - 16px));max-height:calc(100dvh - 80px);overflow:auto;padding:10px;border:1px solid rgba(255,255,255,.2);border-radius:15px;background:#0f0f0f;contain:layout paint style}",
    "panel compositing",
)
s = replace_once(s, '<span class="pill">V4 • Sandbox + stability • Unlock-All included</span>', '<span class="pill">V5 Fast • iPhone performance + sandbox fixes</span>', "version pill")
s = replace_once(
    s,
    '<p><strong>V4</strong> is the recommended build. It keeps the V3 sandbox tools, starts heroes/stars maxed with a persistent reset-to-custom mode, adds per-hero level toggles, expands the special-tower catalog, improves swarm performance, and tightens touch handling.</p>',
    '<p><strong>V5 Fast</strong> is the recommended iPhone path. It loads the new V5 SWF directly with lower iOS render quality, stronger swarm cosmetic throttling, a complete wave-backed enemy selector, Pirate Camp, and Send All boss triggers. The stored-build buttons below remain available for older versions.</p>',
    "intro",
)
s = replace_once(s, '<div class="actions">\n<button id="installV4Btn" class="primary">Install V4 Sandbox + Stability</button>', '<div class="actions">\n<a class="button primary" href="/mod/fast.html">Play V5 Fast — recommended on iPhone</a>\n<button id="installV4Btn" class="secondary">Install V4 Sandbox + Stability</button>', "setup V5 fast button")
s = replace_once(s, '<h2>V4 changes</h2>', '<h2>V5 changes</h2>', "changes heading")
s = replace_once(
    s,
    '<li><strong>Heroes:</strong> the pause tools have individual ON/OFF toggles for all <strong>9 hero implementations present in this Flash build</strong>: Alric, Mirage, Captain Blackthorne, Cronan, Sha\'tra, Grawl, Nivus, Dierdre and Ashbite. All 9 start ON in a level; toggle any hero off or back on for that level.</li>',
    '<li><strong>Heroes:</strong> the selector exposes all <strong>9 hero implementations actually present in this SWF</strong>: Alric, Mirage, Captain Blackthorne, Cronan, Sha\'tra, Grawl, Nivus, Dierdre and Ashbite. The later bonus heroes Rurin, Black Corsair and Lucrezia do not have classes/assets in this source binary, so V5 does not add crash-prone fake buttons for them.</li>',
    "hero note",
)
s = replace_once(
    s,
    '<li><strong>Waves:</strong> the next-wave flag appears immediately after the previous wave is sent, so you can chain manual early waves. <strong>Send all waves</strong> remains available, but releases waves across frames instead of activating every remaining wave in one frame.</li>',
    '<li><strong>Waves + bosses:</strong> <strong>Send all waves</strong> still releases waves across frames, now runs each level\'s normal wave hook, and triggers the native Efreeti, Gorilla and Umbra/final-boss entrance controllers when the last wave is queued.</li>',
    "wave note",
)
s = replace_once(
    s,
    '<li><strong>Special towers:</strong> the catalog has <strong>9 buildable choices</strong>: Dwarf Bastion (250), Pirate Barracks (180), Dwarf Hall (225), Crossbow Fort, Tribal Axethrowers, Archmage, Necromancer, DWAARP and Battle-Mecha T200. The six advanced specializations use their native in-game costs.</li>',
    '<li><strong>Special buildings:</strong> the catalog now has <strong>10 buildable choices</strong>, adding the previously missing <strong>Pirate Camp</strong> to Dwarf Riflemen, Pirate Barracks, Dwarf Hall, Crossbow Fort, Tribal Axethrowers, Archmage, Necromancer, DWAARP and Battle-Mecha T200.</li>',
    "special note",
)
s = replace_once(
    s,
    '<li><strong>Touch + performance:</strong> pause buttons, radial items and all three map-special towers respond on press; the player is re-focused on pointer-down. High-entity play reuses child snapshots instead of allocating per-tick Dictionaries and throttles cosmetic layers only when entity/bullet counts are high, while gameplay updates stay full-rate.</li>',
    '<li><strong>Enemy selector:</strong> V5 adds every enemy class used by normal wave data that V4 omitted, including Alien Breeder/Reaper, Bouncer, underwater cannibals, Desert Wolf Small, Munra and Wasp Queen. Boss/helper pieces with incompatible constructors stay out of the generic wave selector.</li>\n<li><strong>Touch + performance:</strong> iPhones default to low Flash quality, expensive CSS backdrop blur is removed, background execution is paused, and cosmetic/decal/background layers update less often as swarms become heavy or extreme. Entity and bullet gameplay updates remain full-rate.</li>',
    "performance note",
)
s = replace_once(s, '<p class="muted">Verified V4 SHA-256: <code>9744706b367e5b2fb36947614cd92f4957a87db1832a10b058477cf313930bdb</code></p>', '<p class="muted">V5 is served directly by the Fast player; its verified SHA-256 is stored alongside the SWF in <code>assets/kingdom-rush-frontiers-v5.sha256</code>.</p>', "hash note")
s = replace_once(s, '<h2>Using V4</h2>', '<h2>Using V5</h2>', "using heading")
s = replace_once(s, '<p>Inside a level, open the game\'s pause/settings screen to see the V4 controls. Hero selection and enemy-round tools are separate pages. On an empty build spot, use <strong>More…</strong> to reach the three special-tower pages.</p>', '<p>For iPhone, use <strong>Play V5 Fast</strong>. Inside a level, open the game\'s pause/settings screen for hero and enemy-round tools. On an empty build spot, use <strong>More…</strong> to reach the special-building pages.</p>', "using copy")
s = replace_once(s, '<p class="good"><strong>Your campaign save and stored SWF remain separate.</strong> Switching among V4, V3, v2, v1 and clean builds uses the same Ruffle site storage.</p>', '<p class="good"><strong>Your campaign save and game build remain separate.</strong> V5 Fast uses the same Ruffle site storage as the older Mod Lab builds.</p>', "save copy")
s = replace_once(s, '<button id="v4Btn" class="primary">Install V4 Sandbox + Stability</button>', '<a class="button primary" href="/mod/fast.html">Play V5 Fast</a>\n<button id="v4Btn" class="secondary">Install V4 Sandbox + Stability</button>', "panel V5 fast button")
s = replace_once(
    s,
    "const TOUCH_DEVICE=('ontouchstart' in window)||(navigator.maxTouchPoints||0)>0||(window.matchMedia&&window.matchMedia('(pointer:coarse)').matches);",
    "const TOUCH_DEVICE=('ontouchstart' in window)||(navigator.maxTouchPoints||0)>0||(window.matchMedia&&window.matchMedia('(pointer:coarse)').matches);\nconst IOS_DEVICE=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&(navigator.maxTouchPoints||0)>1);",
    "iOS detection",
)
s = replace_once(
    s,
    "quality:TOUCH_DEVICE?'medium':'high',allowScriptAccess:false,openUrlMode:'confirm',allowNetworking:'all',upgradeToHttps:true,compatibilityRules:true,warnOnUnsupportedContent:false,swfFileName:CANONICAL_SWF_NAME,base:location.origin+'/mod/'",
    "quality:IOS_DEVICE?'low':TOUCH_DEVICE?'medium':'high',allowScriptAccess:false,openUrlMode:'confirm',allowNetworking:'all',upgradeToHttps:true,compatibilityRules:true,warnOnUnsupportedContent:false,backgroundExecutionMode:'none',preloader:false,splashScreen:false,polyfills:false,swfFileName:CANONICAL_SWF_NAME,base:location.origin+'/mod/'",
    "Ruffle iPhone options",
)
p.write_text(s, encoding="utf-8", newline="\n")

print("Updated root, Fast V5 player, and Mod Lab iPhone performance settings.")
