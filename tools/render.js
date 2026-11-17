const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const B = path.join(__dirname, '..', 'build');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.goto('file://' + B + '/cover.html', { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: B + '/cover.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await page.goto('file://' + B + '/body.html', { waitUntil: 'load', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: B + '/body.pdf', format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>', footerTemplate: fs.readFileSync(B + '/footer.html', 'utf8'),
    margin: { top: '16mm', bottom: '20mm', left: '17mm', right: '17mm' }, timeout: 300000 });
  await browser.close();
})();
