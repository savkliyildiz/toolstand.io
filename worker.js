// ToolStand Analytics Worker — Cloudflare Pages + KV
// POST /api/analytics → ingest events
// GET  /api/analytics/report → read report (auth required)

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // ── POST: Ingest analytics events ──────────────────
    if (url.pathname === '/api/analytics' && request.method === 'POST') {
      try {
        const contentType = request.headers.get('Content-Type') || '';
        let payload;
        if (contentType.includes('application/json')) {
          payload = await request.json();
        } else {
          payload = JSON.parse(await request.text());
        }

        const today = new Date().toISOString().slice(0, 10);
        const id = `${today}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        await env.ANALYTICS_KV.put(id, JSON.stringify({
          ...payload,
          _ts: new Date().toISOString(),
          _country: request.cf?.country ?? 'XX',
        }), { expirationTtl: 7 * 86400 });

        return new Response(JSON.stringify({ ok: true }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: e.message }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    // ── GET: Read analytics report ─────────────────────
    if (url.pathname === '/api/analytics/report' && request.method === 'GET') {
      const secret = env.ANALYTICS_SECRET || 'ts-analytics-2026';
      if (request.headers.get('X-Analytics-Key') !== secret) {
        return new Response(JSON.stringify({ error: 'unauthorized' }), {
          status: 401,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      try {
        // Get today's events
        const today = new Date().toISOString().slice(0, 10);
        const list = await env.ANALYTICS_KV.list({ prefix: today });
        const events = [];
        for (const key of list.keys) {
          const val = await env.ANALYTICS_KV.get(key.name);
          if (val) events.push(JSON.parse(val));
        }

        // Sort by timestamp descending
        events.sort((a, b) => b.ts - a.ts);

        return new Response(JSON.stringify({
          total: list.keys.length,
          events: events
        }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    // ── All other requests → static assets ─────────────
    return env.ASSETS.fetch(request);
  }
};
