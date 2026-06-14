// ToolStand Analytics — privacy-first, no cookies, no fingerprint, no IP
(function() {
  'use strict';

  const ENDPOINT = '/api/analytics';
  const BATCH_INTERVAL = 5000; // 5s batch window
  let queue = [];
  let pageEnter = Date.now();
  let pagePath = location.pathname;
  let sent = false;

  // ── Send a single event ────────────────────────────
  function send(event) {
    // Attach bot detection data if available (set by bot-detect.js)
    if (window._tsBotInfo) {
      event._bt = window._tsBotInfo.getLevel ? window._tsBotInfo.getLevel() : 0;
      event._br = window._tsBotInfo.reasons || '';
    }
    const payload = JSON.stringify(event);
    if (navigator.sendBeacon) {
      navigator.sendBeacon(ENDPOINT, payload);
    } else {
      // Fallback: fire-and-forget XHR
      const x = new XMLHttpRequest();
      x.open('POST', ENDPOINT, true);
      x.setRequestHeader('Content-Type', 'application/json');
      x.send(payload);
    }
  }

  // ── Device type detection ───────────────────────────
  function deviceType() {
    var w = window.innerWidth;
    if (w < 768) return 'mobile';
    if (w < 1024) return 'tablet';
    return 'desktop';
  }

  // ── Embedded detection ──────────────────────────────
  function isEmbedded() {
    try { return window.self !== window.top ? 1 : 0; } catch(e) { return 1; }
  }

  // ── Build event ─────────────────────────────────────
  function event(type, extra) {
    return Object.assign({
      t: type,
      p: pagePath,
      ts: Date.now(),
      r: document.referrer || '',
      w: window.innerWidth,
      d: deviceType(),
      e: isEmbedded(),
    }, extra || {});
  }

  // ── Page view (fires immediately) ──────────────────
  function pageView() {
    const title = document.title || '';
    // Clean title: remove "| ToolStand" suffix
    const short = title.replace(/\s*[|–—\-]\s*ToolStand.*$/i, '').trim();
    send(event('page_view', { ti: short }));
  }

  // ── Time on page (fires on leave) ──────────────────
  function timeOnPage() {
    if (sent) return;
    sent = true;
    const ms = Date.now() - pageEnter;
    // Only report if > 1 second (filter bounces)
    if (ms > 1000) {
      send(event('time_on_page', { ms: ms }));
    }
  }

  // ── Tool event ──────────────────────────────────────
  window.tsTrack = function(action, detail) {
    send(event('tool_event', { a: action, d: detail || '' }));
  };

  // ── Error tracking ──────────────────────────────────
  window.addEventListener('error', function(e) {
    if (!e.target || e.target === window) {
      send(event('js_error', {
        msg: (e.message || '').slice(0, 200),
        file: (e.filename || '').replace(location.origin, ''),
        line: e.lineno || 0,
        col: e.colno || 0,
      }));
    }
  }, true);

  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', function(e) {
    send(event('js_error', {
      msg: (e.reason?.message || String(e.reason)).slice(0, 200),
      file: '',
      line: 0,
      col: 0,
    }));
  });

  // ── Leave events ────────────────────────────────────
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') timeOnPage();
  });
  window.addEventListener('beforeunload', timeOnPage);
  window.addEventListener('pagehide', timeOnPage);

  // ── Fire page view ──────────────────────────────────
  if (document.readyState === 'complete') {
    pageView();
  } else {
    window.addEventListener('load', pageView);
  }

  // ── Auto-detect tool usage ──────────────────────────
  // Copy events (user copies tool output)
  document.addEventListener('copy', function(e) {
    const tool = document.querySelector('h1');
    const toolName = tool ? tool.textContent.replace(/^[^\w]+/, '').trim() : pagePath;
    tsTrack('copy', toolName);
  });

  // Click on copy/download buttons
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('button');
    if (!btn) return;
    const text = (btn.textContent || '').toLowerCase();
    const toolEl = document.querySelector('h1');
    const toolName = toolEl ? toolEl.textContent.replace(/^[^\w]+/, '').trim() : pagePath;
    if (text.includes('copy')) tsTrack('copy_btn', toolName);
    if (text.includes('download')) tsTrack('download', toolName);
    if (text.includes('clear') || text.includes('reset')) tsTrack('reset', toolName);
    if (text.includes('calculate') || text.includes('convert') || text.includes('generate')) {
      tsTrack('action', toolName);
    }
  });

  // Input interaction (tool was used, not just viewed)
  let toolInteracted = false;
  document.addEventListener('input', function(e) {
    if (toolInteracted) return;
    const inp = e.target.closest('input, textarea, select');
    if (!inp) return;
    // Only count inputs inside tool areas (not search/nav)
    if (inp.closest('.tool-container, .tc-c, main')) {
      toolInteracted = true;
      const toolEl = document.querySelector('h1');
      const toolName = toolEl ? toolEl.textContent.replace(/^[^\w]+/, '').trim() : pagePath;
      tsTrack('tool_used', toolName);
    }
  }, { passive: true });

})();
