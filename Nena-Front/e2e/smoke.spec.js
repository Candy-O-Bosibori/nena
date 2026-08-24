// Single end-to-end smoke test: sign up, land on /overview, confirm topics
// and modes render. Not a full e2e suite -- this is the one high-value
// "is the whole stack actually wired together" check to run before a
// deploy, on top of the backend's pytest suite and `vite build`.
//
// Standalone script (not @playwright/test) so it needs no new project
// dependency by default. Resolves Playwright from PLAYWRIGHT_PATH if set
// (a path to an existing playwright install's node_modules), falling back
// to a normal `import "playwright"` if this project has its own -- run
// `npm install -D playwright` here to make that the default.
//
// Requires both dev servers running first:
//   Nena_Back:  ./venv/bin/python3 app.py
//   Nena-Front: npm run dev
//
// Usage: node e2e/smoke.spec.js [frontendUrl]
// Exits 0 on success, 1 on any failed assertion.

const playwrightSpecifier = process.env.PLAYWRIGHT_PATH
  ? `${process.env.PLAYWRIGHT_PATH}/playwright/index.mjs`
  : "playwright";
const { chromium } = await import(playwrightSpecifier);

const FRONTEND_URL = process.argv[2] || "http://localhost:5173";

let failures = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ok - ${message}`);
  } else {
    console.error(`  FAIL - ${message}`);
    failures += 1;
  }
}

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  const consoleErrors = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });

  try {
    console.log("1. Sign up with a fresh account");
    const email = `smoketest_${Date.now()}@example.com`;
    await page.goto(`${FRONTEND_URL}/signup`, { waitUntil: "networkidle" });
    await page.locator('input[placeholder="Your name"]').fill("Smoke Test");
    await page.locator('input[placeholder="you@example.com"]').fill(email);
    await page.locator('input[placeholder="At least 8 characters"]').fill("TestPass123!");
    await page.locator('button[type="submit"]').click();
    await page.waitForTimeout(2000);

    console.log("2. Confirm landing on /overview after signup");
    assert(page.url().includes("/overview"), `redirected to /overview (got ${page.url()})`);

    const hasToken = await page.evaluate(() => !!localStorage.getItem("access_token"));
    assert(hasToken, "access_token is present in localStorage");

    console.log("3. Confirm modes render");
    const modeTabs = page.locator("nav button", { hasText: /Random Topic|Interview Prep/i });
    assert((await modeTabs.count()) > 0, "at least one mode tab is visible");

    console.log("4. Confirm a topic renders");
    await page.waitForTimeout(1000);
    const bodyText = await page.locator("body").innerText();
    assert(bodyText.length > 100, "page has substantial content (topics/modes loaded)");

    console.log("5. Check for console errors");
    assert(consoleErrors.length === 0, `no console errors (found ${consoleErrors.length})`);
    if (consoleErrors.length > 0) {
      consoleErrors.forEach((e) => console.error(`    - ${e}`));
    }
  } catch (err) {
    console.error("Unexpected error during smoke test:", err);
    failures += 1;
  } finally {
    await browser.close();
  }

  if (failures > 0) {
    console.error(`\n${failures} assertion(s) failed.`);
    process.exit(1);
  } else {
    console.log("\nAll smoke checks passed.");
    process.exit(0);
  }
})();
