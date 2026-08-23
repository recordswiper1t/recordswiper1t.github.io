import { chromium } from 'playwright';

const url = process.env.STICKWAR_URL || 'http://127.0.0.1:8000/stickwar-complete/';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
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
  await page.waitForFunction(() => document.querySelector('#status')?.textContent?.includes('Verified'), null, { timeout: 30_000 });
  await page.click('#play');
  await page.waitForSelector('ruffle-player', { timeout: 30_000 });
  await page.waitForTimeout(15_000);

  const state = await page.evaluate(() => {
    const player = document.querySelector('ruffle-player');
    const shadow = player?.shadowRoot;
    const canvas = shadow?.querySelector('canvas');
    return {
      status: document.querySelector('#status')?.textContent || '',
      shellDisplay: getComputedStyle(document.querySelector('#shell')).display,
      playerPresent: Boolean(player),
      canvasPresent: Boolean(canvas),
      canvasWidth: canvas?.width || 0,
      canvasHeight: canvas?.height || 0,
      shadowText: (shadow?.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 500),
    };
  });
  console.log('[state]', JSON.stringify(state));

  if (!state.playerPresent || !state.canvasPresent || state.canvasWidth === 0 || state.canvasHeight === 0) {
    throw new Error(`Ruffle did not produce a live canvas: ${JSON.stringify(state)}`);
  }

  const fatal = events.filter(line => /pageerror|panicked at|RuntimeError|Failed to load|wasm.*error|unhandled/i.test(line));
  if (fatal.length) {
    throw new Error(`Fatal browser/Ruffle diagnostics detected:\n${fatal.join('\n')}`);
  }
} finally {
  await browser.close();
}
