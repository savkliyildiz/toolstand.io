/**
 * toolstand.io — Bot Detection Module (zero-dependency)
 * Adds `_bot` field to analytics beacons:
 *   0 = likely human
 *   1 = suspicious (no mouse, WebDriver, headless)
 *   2 = confirmed bot
 */
(function() {
  'use strict';

  var botScore = 0;
  var reasons = [];

  // 1. navigator.webdriver — most reliable bot signal
  if (navigator.webdriver) {
    botScore += 2;
    reasons.push('webdriver');
  }

  // 2. Headless Chrome detection
  var ua = navigator.userAgent || '';
  if (/HeadlessChrome/i.test(ua)) {
    botScore += 2;
    reasons.push('headless');
  }

  // 3. Generic bot UA patterns
  if (/bot|crawler|spider|scraper|curl|wget|python|java|go-http/i.test(ua)) {
    botScore += 1;
    reasons.push('ua_pattern');
  }

  // 4. Missing common browser properties
  if (!navigator.languages || navigator.languages.length === 0) {
    botScore += 1;
    reasons.push('no_languages');
  }
  if (navigator.plugins && navigator.plugins.length === 0) {
    botScore += 0.5;
  }
  if (!navigator.hardwareConcurrency || navigator.hardwareConcurrency < 2) {
    botScore += 1;
    reasons.push('no_hw');
  }

  // 5. Missing screen dimensions (headless browsers often have 0x0)
  if (screen.width === 0 || screen.height === 0) {
    botScore += 2;
    reasons.push('zero_screen');
  }

  // 6. Mouse/touch detection (runs after 3 seconds)
  var hasInteraction = false;
  function markHuman() {
    hasInteraction = true;
    botScore = Math.max(0, botScore - 1);
  }
  document.addEventListener('mousemove', markHuman, { once: true });
  document.addEventListener('touchstart', markHuman, { once: true });
  document.addEventListener('keydown', markHuman, { once: true });
  document.addEventListener('scroll', markHuman, { once: true });

  // After 5 seconds, if no human interaction + other signs → classify
  setTimeout(function() {
    if (!hasInteraction && botScore >= 1) {
      botScore += 1;
      reasons.push('no_interaction');
    }
  }, 5000);

  // Export: add bot info to analytics payload
  window._tsBotInfo = {
    score: botScore,
    reasons: reasons.join(','),
    getLevel: function() {
      if (botScore >= 3) return 2; // confirmed bot
      if (botScore >= 1) return 1; // suspicious
      return 0; // likely human
    }
  };

  // Patch analytics beacon to include bot level
  var origBeacon = window._tsBeacon;
  window._tsBeacon = function(data) {
    data = data || {};
    data._bt = window._tsBotInfo.getLevel();
    data._br = window._tsBotInfo.reasons;
    if (origBeacon) origBeacon(data);
  };
})();
