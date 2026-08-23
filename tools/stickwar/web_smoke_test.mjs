import { chromium } from 'playwright';

const url = process.env.STICKWAR_URL || 'http://127.0.0.1:8000/stickwar-complete/';
const browser = await chromium.launch({ headless: true, args: ['--lang=en-US', '--enable-unsafe-swiftshader'] });
const context = await browser.newContext({ locale: 'en-US', viewport: { width: 1280, height: 800 } });
const page = await context.newPage();
const events = [];

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
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60_000 });
  console.log('[locale]', JSON.stringify(await page.evaluate(() => ({
    language: navigator.language,
    languages: navigator.languages,
    intl: Intl.DateTimeFormat().resolvedOptions().locale,
  }))));
  await page.waitForFunction(() => document.querySelector('#status')?.textContent?.includes('Verified'), null, { timeout: 30_000 });
  await page.click('#playCampaign');
  await page.waitForSelector('ruffle-player', { timeout: 30_000 });
  await page.waitForTimeout(12_000);

  const state = await page.evaluate(() => {
    const player = document.querySelector('ruffle-player');
    const shadow = player?.shadowRoot;
    const canvas = shadow?.querySelector('canvas');
    shadow?.querySelector('#hardware-acceleration-modal .close-modal')?.click();
    return {
      status: document.querySelector('#status')?.textContent || '',
      shellDisplay: getComputedStyle(document.querySelector('#playerShell')).display,
      playerPresent: Boolean(player),
      canvasPresent: Boolean(canvas),
      canvasWidth: canvas?.width || 0,
      canvasHeight: canvas?.height || 0,
      readyState: player?.readyState ?? null,
    };
  });
  console.log('[state]', JSON.stringify(state));
  await page.waitForTimeout(500);
  await page.screenshot({ path: '/tmp/super-stick-war-main-menu.png' });

  if (!state.playerPresent || !state.canvasPresent || state.canvasWidth === 0 || state.canvasHeight === 0 || state.readyState < 2) {
    throw new Error(`Ruffle did not load the SWF: ${JSON.stringify(state)}`);
  }

  // Exercise the real Flash menu: PLAY CAMPAIGN is the lower-left button in the 850x700 SWF.
  const eventMark = events.length;
  await page.mouse.click(180, 760);
  await page.waitForTimeout(5000);
  await page.screenshot({ path: '/tmp/super-stick-war-after-campaign.png' });
  console.log('[campaign-transition-events]', JSON.stringify(events.slice(eventMark)));

  const fatal = events.filter(line => /\[pageerror\]|panicked at|RuntimeError|wasm.*error|unhandled/i.test(line));
  if (fatal.length) {
    throw new Error(`Fatal browser/Ruffle diagnostics detected:\n${fatal.join('\n')}`);
  }
} finally {
  await context.close();
  await browser.close();
}
