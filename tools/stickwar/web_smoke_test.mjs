import { statSync } from 'node:fs';
import { chromium } from 'playwright';

const url = process.env.STICKWAR_URL || 'http://127.0.0.1:8000/stickwar-complete/';
const browser = await chromium.launch({ headless: true, args: ['--lang=en-US', '--enable-unsafe-swiftshader'] });
const context = await browser.newContext({ locale: 'en-US', viewport: { width: 1280, height: 800 } });
const page = await context.newPage();
const events = [];

async function flashPress(x, y, holdMs = 140) {
  await page.mouse.move(x, y);
  await page.waitForTimeout(120);
  await page.mouse.down();
  await page.waitForTimeout(holdMs);
  await page.mouse.up();
}

async function playerState() {
  return page.evaluate(() => {
    const player = document.querySelector('ruffle-player');
    const shadow = player?.shadowRoot;
    const canvas = shadow?.querySelector('canvas');
    const api = player?.ruffle?.();
    shadow?.querySelector('#hardware-acceleration-modal .close-modal')?.click();
    return {
      status: document.querySelector('#status')?.textContent || '',
      playerPresent: Boolean(player),
      canvasPresent: Boolean(canvas),
      canvasWidth: canvas?.width || 0,
      canvasHeight: canvas?.height || 0,
      readyState: player?.readyState ?? null,
      parameters: api?.loadedConfig?.parameters ?? null,
    };
  });
}

function assertPlayerLoaded(state, label) {
  if (!state.playerPresent || !state.canvasPresent || state.canvasWidth === 0 || state.canvasHeight === 0 || state.readyState < 2) {
    throw new Error(`${label}: Ruffle did not load the SWF: ${JSON.stringify(state)}`);
  }
}

page.on('console', msg => {
  const line = `[console:${msg.type()}] ${msg.text()}`;
  events.push(line);
  console.log(line);
});
page.on('pageerror', err => {
  const line = `[pageerror] ${err.stack || err.message || String(err)}`;
  events.push(line);
  console.error(line);
});
page.on('requestfailed', req => {
  if (req.method() === 'HEAD') return;
  const line = `[requestfailed] ${req.method()} ${req.url()} ${req.failure()?.errorText || ''}`;
  events.push(line);
  console.error(line);
});
page.on('response', res => {
  if (res.status() >= 400) {
    const line = `[http:${res.status()}] ${res.request().method()} ${res.url()}`;
    events.push(line);
    console.error(line);
  }
});

try {
  // Normal campaign path: prove the released SWF reaches the interactive SW2 title menu.
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60_000 });
  console.log('[locale]', JSON.stringify(await page.evaluate(() => ({
    language: navigator.language,
    languages: navigator.languages,
    intl: Intl.DateTimeFormat().resolvedOptions().locale,
  }))));
  await page.waitForFunction(() => document.querySelector('#status')?.textContent?.includes('Verified'), null, { timeout: 30_000 });
  await page.click('#playCampaign');
  await page.waitForSelector('ruffle-player', { timeout: 30_000 });
  await page.waitForTimeout(20_000);
  const campaignState = await playerState();
  console.log('[campaign-state]', JSON.stringify(campaignState));
  assertPlayerLoaded(campaignState, 'campaign');
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/tmp/super-stick-war-main-menu.png' });

  // SW2 polls mouse-down state once per Flash frame, so use a frame-visible press.
  await flashPress(180, 760);
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/tmp/super-stick-war-campaign-menu.png' });
  // NEW GAME is centered in the next panel. Reaching it proves the normal campaign button works.
  await flashPress(500, 760);
  await page.waitForTimeout(2500);
  await page.screenshot({ path: '/tmp/super-stick-war-difficulty-menu.png' });

  // Battle Lab is the strongest web-runtime regression test: swcLab=1 must now bypass
  // the dead Flash-era intro loaders and route a fresh campaign directly into level 0,
  // which CampaignScreen immediately opens as CampaignGameScreen.
  const labEventMark = events.length;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60_000 });
  await page.waitForFunction(() => document.querySelector('#status')?.textContent?.includes('Verified'), null, { timeout: 30_000 });
  await page.click('#playLab');
  await page.waitForSelector('ruffle-player', { timeout: 30_000 });
  await page.waitForTimeout(12_000);
  const labState = await playerState();
  console.log('[lab-state]', JSON.stringify(labState));
  assertPlayerLoaded(labState, 'lab');
  await page.waitForTimeout(500);
  const labScreenshot = '/tmp/super-stick-war-battle-lab.png';
  await page.screenshot({ path: labScreenshot });
  const labScreenshotBytes = statSync(labScreenshot).size;
  console.log('[lab-screenshot-bytes]', labScreenshotBytes);
  // The static title/menu screenshots are ~10 KB in this deterministic runner. A live
  // battlefield is far more visually complex. This catches silent AS3 transition failures
  // that leave Ruffle alive but strand the user on the title screen.
  if (labScreenshotBytes < 25_000) {
    throw new Error(`Battle Lab did not leave the title/menu screen (screenshot ${labScreenshotBytes} bytes)`);
  }
  console.log('[lab-events]', JSON.stringify(events.slice(labEventMark)));

  const fatal = events.filter(line => /\[pageerror\]|panicked at|RuntimeError|Error #\d+|AVM2.*error|wasm.*error|unhandled/i.test(line));
  if (fatal.length) {
    throw new Error(`Fatal browser/Ruffle diagnostics detected:\n${fatal.join('\n')}`);
  }
} finally {
  await context.close();
  await browser.close();
}
