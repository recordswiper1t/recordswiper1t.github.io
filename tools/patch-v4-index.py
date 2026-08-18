#!/usr/bin/env python3
from pathlib import Path
import re

p = Path('mod/index.html')
text = p.read_text(encoding='utf-8')
sha_text = Path('assets/V4-SHA256SUMS.txt').read_text(encoding='utf-8')
m = re.search(r'^([0-9a-f]{64})\s+assets/kingdom-rush-frontiers-v4\.swf$', sha_text, re.M)
if not m:
    raise SystemExit('V4 hash not found')
v4_sha = m.group(1)


def one(old, new, label):
    global text
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected one match, found {n}')
    text = text.replace(old, new, 1)

one('<title>Kingdom Rush Frontiers — V3 Mobile + Sandbox</title>', '<title>Kingdom Rush Frontiers — V4 Sandbox + Stability</title>', 'title')
one('<span class="pill">V3 • Mobile input + sandbox • Unlock-All included</span>', '<span class="pill">V4 • Sandbox + stability • Unlock-All included</span>', 'pill')
one('<p><strong>V3</strong> is the recommended iPhone build. It keeps the previous unlock and fast-boot mods, moves gameplay cheats into the in-level pause/settings screen, and adds the requested sandbox tools.</p>', '<p><strong>V4</strong> is the recommended build. It keeps the V3 sandbox tools, adds per-hero selection and max/reset trees, expands special towers, improves wave dispatch stability, and tightens touch handling.</p>', 'intro')
one('<button id="installV3Btn" class="primary">Install V3 Mobile + Sandbox</button>', '<button id="installV4Btn" class="primary">Install V4 Sandbox + Stability</button>\n<button id="installV3Btn" class="secondary">Install V3 Mobile + Sandbox</button>', 'setup buttons')
one('<div id="status" class="status">Checking the stored build and verified V3 asset…</div>', '<div id="status" class="status">Checking the stored build and verified V4 asset…</div>', 'status copy')

start = text.index('<h2>V3 changes</h2>')
end = text.index('</section>', start)
new_changes = f'''<h2>V4 changes</h2>
<ul class="changes">
<li><strong>Heroes:</strong> the pause tools now have individual ON/OFF toggles for all <strong>9 hero implementations present in this Flash build</strong>: Alric, Mirage, Captain Blackthorne, Cronan, Sha'tra, Grawl, Nivus, Dierdre and Ashbite.</li>
<li><strong>Maxed by default:</strong> a session starts with all six star-upgrade trees and every hero skill tree maxed. Use <strong>Trees: MAXED (reset)</strong> to reset everything and receive the exact spendable stars/hero points again; press it again to max them.</li>
<li><strong>Gold:</strong> the old +100 button is now a numeric field. Enter 0, 50, 9000 or another non-negative amount and press <strong>ADD</strong>.</li>
<li><strong>Waves:</strong> the next-wave flag appears immediately after the previous wave is sent, so you can chain manual early waves. <strong>Send all waves</strong> remains available, but releases waves across frames instead of activating every remaining wave in one frame.</li>
<li><strong>Special towers:</strong> the radial page expands from 2 to <strong>8 buildable choices</strong>: Dwarf Riflemen, Pirate Barracks, Crossbow Fort, Tribal Axethrowers, Archmage, Necromancer, DWAARP and Battle-Mecha T200. Dwarf/Pirate placements now have explicit costs; the six advanced towers use their built-in game costs.</li>
<li><strong>Tower placement:</strong> special towers now use the same +36px holder adjustment as normal towers, fixing the half-tile-high placement.</li>
<li><strong>Touch + performance:</strong> V4 pause buttons respond on press, the player is re-focused on pointer-down, touch devices use medium render quality, and a leaked TowerHolder mouse listener is cleaned up correctly.</li>
<li><strong>Previous mods retained:</strong> unlock-all, fast boot, Heroic/Iron availability, custom enemy rounds and 1×/3× speed remain included.</li>
</ul>
<p class="muted">Verified V4 SHA-256: <code>{v4_sha}</code></p>
'''
text = text[:start] + new_changes + text[end:]

one('<h2>Using V3</h2>', '<h2>Using V4</h2>', 'using heading')
one("<p>Inside a level, open the game's pause/settings screen to see the V3 controls. The enemy-round page is reached from there. On an empty build spot, use <strong>More…</strong> to reach the special-tower page.</p>", "<p>Inside a level, open the game's pause/settings screen to see the V4 controls. Hero selection and enemy-round tools are separate pages. On an empty build spot, use <strong>More…</strong> to reach the two special-tower pages.</p>", 'using copy')
one('Switching among V3, v2, v1 and clean builds uses the same Ruffle site storage.', 'Switching among V4, V3, v2, v1 and clean builds uses the same Ruffle site storage.', 'save copy')
one('<button id="v3Btn" class="primary">Install V3 Mobile + Sandbox</button>', '<button id="v4Btn" class="primary">Install V4 Sandbox + Stability</button>\n<button id="v3Btn" class="secondary">Install V3 Mobile + Sandbox</button>', 'panel buttons')

one("const V3_SWF_URL='/assets/kingdom-rush-frontiers-v3.swf';", "const V3_SWF_URL='/assets/kingdom-rush-frontiers-v3.swf';\nconst V4_SWF_URL='/assets/kingdom-rush-frontiers-v4.swf';", 'V4 URL')
one("const V3_SHA='0ac03b3832bbc79bdeadb5fe980b63aad3d5690dd114e294180c720ec55909c2';", f"const V3_SHA='0ac03b3832bbc79bdeadb5fe980b63aad3d5690dd114e294180c720ec55909c2';\nconst V4_SHA='{v4_sha}';", 'V4 hash')
one("const installV3Btn=document.getElementById('installV3Btn'),installV2Btn=document.getElementById('installV2Btn'),installV1Btn=document.getElementById('installV1Btn'),installCleanBtn=document.getElementById('installCleanBtn'),resumeBtn=document.getElementById('resumeBtn');", "const installV4Btn=document.getElementById('installV4Btn'),installV3Btn=document.getElementById('installV3Btn'),installV2Btn=document.getElementById('installV2Btn'),installV1Btn=document.getElementById('installV1Btn'),installCleanBtn=document.getElementById('installCleanBtn'),resumeBtn=document.getElementById('resumeBtn');", 'installer refs')
one("let player=null,lastRecord=null,toastTimer=null;", "let player=null,lastRecord=null,toastTimer=null;\nconst TOUCH_DEVICE=('ontouchstart' in window)||(navigator.maxTouchPoints||0)>0||(window.matchMedia&&window.matchMedia('(pointer:coarse)').matches);", 'touch detection')
one("function setRemoteDisabled(v){installV3Btn.disabled=v;installV2Btn.disabled=v;installV1Btn.disabled=v;installCleanBtn.disabled=v;document.getElementById('v3Btn').disabled=v;document.getElementById('v2Btn').disabled=v;document.getElementById('v1Btn').disabled=v;document.getElementById('cleanBtn').disabled=v}", "function setRemoteDisabled(v){installV4Btn.disabled=v;installV3Btn.disabled=v;installV2Btn.disabled=v;installV1Btn.disabled=v;installCleanBtn.disabled=v;document.getElementById('v4Btn').disabled=v;document.getElementById('v3Btn').disabled=v;document.getElementById('v2Btn').disabled=v;document.getElementById('v1Btn').disabled=v;document.getElementById('cleanBtn').disabled=v}", 'disable buttons')
one("function makePlayer(){const r=window.RufflePlayer&&window.RufflePlayer.newest&&window.RufflePlayer.newest();if(!r)throw new Error('Ruffle failed to load.');player=r.createPlayer();player.id='krf-mod-player';player.style.touchAction='none';player.style.webkitUserSelect='none';player.style.userSelect='none';playerHost.replaceChildren(player);return player}", "function makePlayer(){const r=window.RufflePlayer&&window.RufflePlayer.newest&&window.RufflePlayer.newest();if(!r)throw new Error('Ruffle failed to load.');player=r.createPlayer();player.id='krf-mod-player';player.tabIndex=0;player.style.touchAction='none';player.style.webkitUserSelect='none';player.style.userSelect='none';playerHost.replaceChildren(player);return player}", 'player focusability')
one("quality:'high'", "quality:TOUCH_DEVICE?'medium':'high'", 'mobile quality')
one("function installV3(){return installRemote({url:V3_SWF_URL,name:'kingdom-rush-frontiers-v3.swf',expectedHash:V3_SHA,source:'verified V3 Mobile + Sandbox',label:'V3 Mobile + Sandbox'})}", "function installV4(){return installRemote({url:V4_SWF_URL,name:'kingdom-rush-frontiers-v4.swf',expectedHash:V4_SHA,source:'verified V4 Sandbox + Stability',label:'V4 Sandbox + Stability'})}\nfunction installV3(){return installRemote({url:V3_SWF_URL,name:'kingdom-rush-frontiers-v3.swf',expectedHash:V3_SHA,source:'verified V3 Mobile + Sandbox',label:'V3 Mobile + Sandbox'})}", 'install V4')
old_inspect = "const [v3Ready,v2Ready,cleanReady]=await Promise.all([remoteAvailable(V3_SWF_URL),remoteAvailable(V2_SWF_URL),remoteAvailable(CLEAN_SWF_URL)]);if(v3Ready)statusEl.textContent='V3 is verified and ready. Tap Install V3 Mobile + Sandbox.';else if(v2Ready)statusEl.textContent='QoL v2 is ready; V3 is still publishing.';else if(cleanReady)statusEl.textContent='Clean build is ready; mod assets are still publishing.';else statusEl.textContent='Game assets are still publishing. Reload and try again.'"
new_inspect = "const [v4Ready,v3Ready,v2Ready,cleanReady]=await Promise.all([remoteAvailable(V4_SWF_URL),remoteAvailable(V3_SWF_URL),remoteAvailable(V2_SWF_URL),remoteAvailable(CLEAN_SWF_URL)]);if(v4Ready)statusEl.textContent='V4 is verified and ready. Tap Install V4 Sandbox + Stability.';else if(v3Ready)statusEl.textContent='V3 is ready; V4 is still publishing.';else if(v2Ready)statusEl.textContent='QoL v2 is ready; newer builds are still publishing.';else if(cleanReady)statusEl.textContent='Clean build is ready; mod assets are still publishing.';else statusEl.textContent='Game assets are still publishing. Reload and try again.'"
one(old_inspect,new_inspect,'inspect V4')
one("installV3Btn.onclick=installHandler(installV3);installV2Btn.onclick=installHandler(installV2);", "installV4Btn.onclick=installHandler(installV4);installV3Btn.onclick=installHandler(installV3);installV2Btn.onclick=installHandler(installV2);", 'setup V4 handler')
one("document.getElementById('v3Btn').onclick=()=>{panel.classList.remove('open');installV3().catch", "document.getElementById('v4Btn').onclick=()=>{panel.classList.remove('open');installV4().catch(e=>{showSetup();statusEl.textContent=e.message||String(e);toast(e.message||String(e))})};\ndocument.getElementById('v3Btn').onclick=()=>{panel.classList.remove('open');installV3().catch", 'panel V4 handler')
one("playerHost.addEventListener('touchmove',e=>{if(document.body.classList.contains('playing'))e.preventDefault()},{passive:false});", "playerHost.addEventListener('pointerdown',()=>{if(player){try{player.focus({preventScroll:true})}catch(_){try{player.focus()}catch(__){}}}},{capture:true,passive:true});\nplayerHost.addEventListener('touchmove',e=>{if(document.body.classList.contains('playing'))e.preventDefault()},{passive:false});", 'pointer focus')

p.write_text(text, encoding='utf-8')
print('patched mod/index.html for V4', v4_sha)
