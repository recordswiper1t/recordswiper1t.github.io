import { statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { chromium } from 'playwright';

const origin = process.env.THREE_GAME_ORIGIN || 'http://127.0.0.1:8000';
const browser = await chromium.launch({ headless: true, args: ['--lang=en-US', '--enable-unsafe-swiftshader'] });
const context = await browser.newContext({ locale: 'en-US', viewport: { width: 1280, height: 800 } });

const requested = new Set((process.env.THREE_GAME_FILTER || '').split(',').map(value => value.trim()).filter(Boolean));
const epicWarClicks = process.env.THREE_GAME_EW_CLICKS
  ? JSON.parse(process.env.THREE_GAME_EW_CLICKS)
  : [
      { x: 0.5, y: 0.75, after: 10000 },
      { x: 0.35, y: 0.45, after: 3000 },
      { x: 0.66, y: 0.735, after: 8000 },
      { x: 0.33, y: 0.40, after: 20000 },
      { x: 0.79, y: 0.245, after: 10000 },
    ];
const cases = [
  {
    name: 'kingdom-rush',
    url: `${origin}/ultimate/play.html?campaign=ultimate`,
    click: null,
    wait: 90000,
    settle: 75000,
    checkpointBeforeClicks: 'map',
    insideClicks: [
      { x: 0.495, y: 0.038, after: 20000 },
      { x: 0.613, y: 0.038, after: 15000 },
    ],
  },
  { name: 'stick-war', url: `${origin}/stickwar-complete/`, click: '#playLab', wait: 30000, settle: 45000, insideClicks: [] },
  { name: 'epic-war-5', url: `${origin}/epicwar5-expansion/`, click: '#play', wait: 30000, settle: 15000, insideClicks: epicWarClicks },
].filter(test => requested.size === 0 || requested.has(test.name));

for (const test of cases) {
  const page = await context.newPage();
  const fatal = [];
  page.on('pageerror', error => fatal.push(error.stack || error.message || String(error)));
  page.on('console', message => {
    const line = message.text();
    if (message.type() === 'error' || message.type() === 'warning') console.log(`${test.name} ${message.type()}: ${line}`);
    if (/panicked at|RuntimeError|Error #\d+|AVM2.*error|unhandled/i.test(line)) fatal.push(line);
  });
  await page.goto(test.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  if (test.click) await page.click(test.click);
  await page.waitForSelector('ruffle-player', { timeout: 30000 });
  await page.waitForFunction(() => {
    const player = document.querySelector('ruffle-player');
    const canvas = player?.shadowRoot?.querySelector('canvas');
    player?.shadowRoot?.querySelector('#hardware-acceleration-modal .close-modal')?.click();
    return Boolean(canvas && canvas.width > 0 && canvas.height > 0 && player.readyState >= 2);
  }, null, { timeout: test.wait });
  await page.waitForTimeout(test.settle);
  if (test.checkpointBeforeClicks) {
    const checkpoint = join(tmpdir(), `three-game-${test.name}-${test.checkpointBeforeClicks}.png`);
    await page.screenshot({ path: checkpoint });
    if (statSync(checkpoint).size < 20000) throw new Error(`${test.name}: suspiciously empty ${test.checkpointBeforeClicks} checkpoint`);
  }
  for (const insideClick of test.insideClicks) {
    await page.evaluate(() => {
      const root = document.querySelector('ruffle-player')?.shadowRoot;
      root?.querySelector('#hardware-acceleration-modal .close-modal')?.click();
      root?.querySelector('#continue-btn')?.click();
    });
    const box = await page.locator('ruffle-player').boundingBox();
    if (!box) throw new Error(`${test.name}: player has no clickable area`);
    const clicks = insideClick.clicks || 1;
    for (let index = 0; index < clicks; index++) {
      await page.mouse.click(box.x + box.width * insideClick.x, box.y + box.height * insideClick.y, { delay: 140 });
      if (index + 1 < clicks) await page.waitForTimeout(500);
    }
    await page.waitForTimeout(insideClick.after);
  }
  await page.evaluate(() => {
    const root = document.querySelector('ruffle-player')?.shadowRoot;
    root?.querySelector('#hardware-acceleration-modal .close-modal')?.click();
    root?.querySelector('#continue-btn')?.click();
  });
  if (process.env.THREE_GAME_DEBUG_SHADOW === '1') {
    const shadow = await page.evaluate(() => {
      const root = document.querySelector('ruffle-player')?.shadowRoot;
      return {
        text: root?.innerText || '',
        buttons: [...(root?.querySelectorAll('button') || [])].map(button => ({ id: button.id, text: button.textContent, hidden: button.offsetParent === null })),
      };
    });
    console.log(`${test.name} shadow: ${JSON.stringify(shadow)}`);
  }
  const shot = join(tmpdir(), `three-game-${test.name}.png`);
  await page.screenshot({ path: shot });
  if (fatal.length) throw new Error(`${test.name}: fatal runtime diagnostics\n${fatal.join('\n')}`);
  if (statSync(shot).size < 20000) throw new Error(`${test.name}: suspiciously empty screenshot`);
  console.log(`${test.name}: ready (${shot})`);
  await page.close();
}

await context.close();
await browser.close();
