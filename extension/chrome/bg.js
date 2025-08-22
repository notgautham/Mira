// Minimal service worker: send tab-activation events to FastAPI on localhost
async function post(ev) {
  try {
    await fetch("http://127.0.0.1:8765/event", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ev)
    });
  } catch (e) {
    // Bridge might be offline; ignore in Phase 0
  }
}

chrome.tabs.onActivated.addListener(async info => {
  try {
    const tab = await chrome.tabs.get(info.tabId);
    const url = new URL(tab.url || "http://unknown/");
    await post({
      ts: Date.now(),
      event: "activated",
      domain: url.hostname,
      title: tab.title || "",
      tabId: info.tabId
    });
  } catch (e) {
    // Some pages (chrome://, store, pdf viewer) don't expose URL/title; safe to ignore
  }
});
