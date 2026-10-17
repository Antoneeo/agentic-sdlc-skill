/* Docs site — the page. A classic script: a page opened from disk cannot fetch,
   so the generator writes its data as scripts this page loads. Every word comes
   from strings.js; text from the project is inserted as text, and document
   bodies arrive already formatted and sanitized by the generator. The only
   action anywhere is opening a document: filters, search and view switches
   change nothing. */
(function () {
  "use strict";

  var S = window.DOCS_SITE_STRINGS || {};
  var C = window.DOCS_SITE_CORE;
  var D = null;   // documents, loaded on first use
  var K = null;   // knowledge base, loaded on first use
  var app = document.getElementById("app");
  var ORIGINS = ["given", "elicited", "derived", "ruling", "imported"];

  // ------------------------------------------------------------- helpers

  function t(key, params) {
    var s = Object.prototype.hasOwnProperty.call(S, key) ? S[key] : key;
    if (params) {
      Object.keys(params).forEach(function (k) {
        s = s.split("{" + k + "}").join(String(params[k]));
      });
    }
    return s;
  }

  function el(tag, attrs) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k === "class") node.className = v;
        else if (k === "text") node.textContent = v;
        else if (k.slice(0, 2) === "on") node.addEventListener(k.slice(2), v);
        else node.setAttribute(k, v === true ? "" : v);
      });
    }
    for (var i = 2; i < arguments.length; i++) add(node, arguments[i]);
    return node;
  }

  function add(node, child) {
    if (child === null || child === undefined || child === false) return;
    if (Array.isArray(child)) { child.forEach(function (c) { add(node, c); }); return; }
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }

  function docHref(path) { return "#/doc/" + encodeURI(path); }
  function link(href, text, cls) { return el("a", { href: href, "class": cls }, text); }
  function docLink(path, text) { return link(docHref(path), text || path); }

  function normalize(s) {
    s = String(s || "").normalize("NFKD").replace(/\p{Mn}/gu, "");
    s = s.toLowerCase();
    s = s.replace(/[‐-―−﹘﹣－]/g, "-");
    s = s.replace(/[­​-‏⁠-⁤﻿]/g, "");
    return s.replace(/\s+/g, " ").trim();
  }

  function written(v) { return v !== undefined && v !== null && String(v).trim() !== "" && String(v).trim() !== "-"; }

  var pending = {};

  function loadScript(src, ready) {
    if (pending[src]) { pending[src].push(ready); return; }
    pending[src] = [ready];
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () { var q = pending[src]; pending[src] = null; q.forEach(function (f) { f(); }); };
    s.onerror = function () { fail(); };
    document.body.appendChild(s);
  }

  function needDocs(then) {
    if (D) return then();
    main(el("p", { "class": "muted", text: t("loading_documents") }));
    loadScript("data/docs.js", function () {
      D = window.DOCS_SITE_DOCS;
      if (!D) return fail();
      then();
    });
  }

  function needKb(then) {
    if (K) return then();
    if (!C.meta.has_kb) return notFound();
    main(el("p", { "class": "muted", text: t("loading_knowledge") }));
    loadScript("data/kb.js", function () {
      K = window.DOCS_SITE_KB;
      if (!K) return fail();
      then();
    });
  }

  function html(target, markup) {
    target.innerHTML = markup;   // produced by the generator's sanitizer only
    Array.prototype.forEach.call(target.querySelectorAll("code.notfact"), function (c) {
      c.title = t("not_fact_id");
    });
    Array.prototype.forEach.call(target.querySelectorAll('a[href^="#"]:not([href^="#/"])'), function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        var id = decodeURIComponent(a.getAttribute("href").slice(1));
        var dest = document.getElementById(id);
        if (dest) dest.scrollIntoView({ behavior: "smooth" });
      });
    });
    return target;
  }

  function levelLabel(v) {
    return Object.prototype.hasOwnProperty.call(S, "level_" + v) ? t("level_" + v) : v;
  }

  function statusPill(status, group) {
    return el("span", { "class": "pill g" + group, title: t("group_" + group) }, status || t("group_" + group));
  }

  function originClass(o) { return ORIGINS.indexOf(o) >= 0 ? o : "other"; }

  function originLabel(o) {
    return ORIGINS.indexOf(o) >= 0 ? t("origin_" + o) : t("origin_other", { v: o });
  }

  function originWhy(o) { return ORIGINS.indexOf(o) >= 0 ? t("origin_" + o + "_why") : t("origin_other_why"); }

  // ------------------------------------------------------------ the frame

  var mainEl, panelEl = null, navLinks = {};

  function frame() {
    var nav = el("nav");
    var items = [["home", "#/", "nav_home"], ["chronology", "#/chronology", "nav_chronology"],
                 ["work", "#/work", "nav_work"]];
    if (C.meta.units_page) items.push(["units", "#/units", "nav_" + C.meta.units_page]);
    items.push(["rules", "#/rules", "nav_rules"], ["guides", "#/guides", "nav_guides"], ["documents", "#/documents", "nav_documents"]);
    if (C.meta.has_kb) items.push(["map", "#/map", "nav_map"]);
    if (C.meta.has_sources) items.push(["sources", "#/sources", "nav_sources"]);
    items.forEach(function (it) {
      navLinks[it[0]] = link(it[1], t(it[2]));
      if (it[0] === "map") {
        // the side bar's Map always opens the topics view
        navLinks.map.addEventListener("click", function () {
          mapView = "topics";
          if (location.hash === "#/map") pageMap();
        });
      }
      nav.appendChild(navLinks[it[0]]);
    });
    var stamp = C.meta.git
      ? t("stamp_git", { date: C.meta.generated, commit: C.meta.commit }) +
        (C.meta.changed === 1 ? t("stamp_changed_one")
          : C.meta.changed > 1 ? t("stamp_changed_many", { n: C.meta.changed }) : "")
      : t("stamp_no_git", { date: C.meta.generated });
    var rail = el("aside", { "class": "rail" },
      el("div", { "class": "brand" }, el("div", { "class": "kicker", text: t("site_name") }),
         el("div", { "class": "name", text: C.home.title || t("site_name") })),
      nav,
      el("button", { "class": "searchbtn", type: "button", onclick: openSearch },
         el("span", { text: t("nav_search") }), el("kbd", { text: t("search_hint") })),
      el("div", { "class": "stamp", text: stamp }));
    mainEl = el("main");
    app.textContent = "";
    add(app, [rail, mainEl]);
    document.title = (C.home.title ? C.home.title + " — " : "") + t("site_name");
  }

  function main() {
    mainEl.className = "";
    mainEl.textContent = "";
    for (var i = 0; i < arguments.length; i++) add(mainEl, arguments[i]);
    window.scrollTo(0, 0);
  }

  function setNav(key) {
    Object.keys(navLinks).forEach(function (k) { navLinks[k].className = k === key ? "on" : ""; });
  }

  function fail() {
    app.textContent = "";
    add(app, el("main", null, el("p", { "class": "empty", text: t("incomplete") })));
  }

  function notFound() {
    main(el("p", { "class": "empty" }, t("not_found"), " ", link("#/", t("back_home"))));
  }

  function heading(title, why) {
    return [el("h1", { text: title }), why ? el("p", { "class": "why", text: why }) : null];
  }

  // ------------------------------------------------------------- the pages

  function eventList(events) {
    return el("ul", { "class": "events" }, events.map(function (e) {
      return el("li", { "class": "event" },
        el("span", { "class": "date", text: e.date }),
        el("span", null, el("div", { "class": "kind", text: t("event_" + e.kind) }),
           e.path ? docLink(e.path, e.label) : e.label));
    }));
  }

  function pageHome() {
    var h = C.home;
    setNav("home");
    var northStar = h.vision && h.vision.north_star
      ? el("section", { "class": "north-star" },
          el("h2", { text: h.vision.section_title }),
          el("p", { "class": "why", text: t("home_north_star_why") }),
          html(el("div", { "class": "prose" }), h.vision.section_html),
          el("div", { "class": "links" },
            el("span", { "class": "status", text: t("home_vision_status", { status: h.vision.status || "—" }) }),
            docLink(h.vision.path, t("home_vision"))))
      : null;
    var project = el("section", { "class": "block" },
      el("h2", { text: t("home_project") }),
      el("p", { "class": "why", text: t("home_project_why") }),
      h.vision
        ? el("div", { "class": "vision-box" },
            el("div", { "class": "status", text: t("home_vision_status", { status: h.vision.status || "—" }) }),
            !h.vision.north_star && h.vision.section_title ? el("h3", { text: h.vision.section_title }) : null,
            !h.vision.north_star ? html(el("div", { "class": "prose" }), h.vision.section_html) : null,
            docLink(h.vision.path, t("home_vision")))
        : el("p", { "class": "muted", text: t("home_vision_none") }),
      el("div", { "class": "links" },
        h.links.readme ? docLink(h.links.readme, t("home_readme")) : null,
        link("#/rules", t("home_rules")),
        h.links.manifest ? docLink(h.links.manifest, t("home_manifest")) : null,
        h.links.router ? docLink(h.links.router, t("home_router")) : null));
    var lately = el("section", { "class": "block" },
      el("h2", null, link("#/chronology", t("home_lately"))),
      el("p", { "class": "why", text: t("home_lately_why") }),
      h.lately.length ? eventList(h.lately) : el("p", { "class": "muted", text: t("chronology_empty") }),
      link("#/chronology", t("home_all_chronology"), "more"));
    var open = el("section", { "class": "block" },
      el("h2", null, link("#/work", t("home_open"))),
      el("p", { "class": "why", text: t("home_open_why") }),
      h.open.length
        ? el("ul", null, h.open.map(function (c) {
            return el("li", null, docLink(c.path, c.name), " ", c.status ? el("span", { "class": "pill", text: c.status }) : null,
              c.next ? el("div", { "class": "muted", text: c.next }) : null);
          }))
        : el("p", { "class": "muted", text: t("work_empty") }),
      el("div", { "class": "links" },
        link("#/work", t("home_all_work")),
        h.links.notes ? docLink(h.links.notes, t("home_notes")) : null,
        h.links.register ? docLink(h.links.register, t("home_register")) : null));
    var known = el("section", { "class": "block" },
      el("h2", null, C.meta.has_kb ? link("#/map", t("home_known")) : t("home_known")),
      el("p", { "class": "why", text: t("home_known_why") }),
      h.known.length
        ? h.known.map(function (a) {
            return el("div", { "class": "area-row" }, link("#/topic/" + encodeURIComponent(a.slug), a.name, "area"),
              el("div", { "class": "chips" }, a.topics.map(function (s) {
                return link("#/topic/" + encodeURIComponent(s), s, "chip");
              })));
          })
        : el("p", { "class": "muted", text: t("home_known_none") }),
      C.meta.has_kb ? link("#/map", t("home_map"), "more") : null);
    var head = el("div", { "class": "home-head" },
      el("h1", { text: h.title || t("home_no_title") }),
      html(el("div", { "class": "intro" }), h.intro_html));
    main(head, northStar, el("div", { "class": "quad" }, project, lately, open, known));
  }

  function pageChronology() {
    setNav("chronology");
    main(heading(t("chronology_title"), t("chronology_why")),
      C.chronology.length ? eventList(C.chronology) : el("p", { "class": "empty", text: t("chronology_empty") }));
  }

  function pageWork() {
    setNav("work");
    var w = C.work;
    var cards = w.cards.length
      ? el("div", { "class": "cards" }, w.cards.map(function (c) {
          var rows = [];
          function row(label, value) { if (written(value)) rows.push(el("dt", { text: t(label) }), el("dd", null, value)); }
          row("work_status", c.status ? statusPill(c.status, c.group) : null);
          row("work_level", c.level ? levelLabel(c.level) : null);
          row("work_since", c.since);
          row("work_updated", c.updated);
          row("work_branch", c.branch ? el("code", { text: c.branch }) : null);
          return el("article", { "class": "card" },
            el("h3", { text: c.name }),
            el("dl", null, rows),
            c.next ? el("div", { "class": "next" }, el("b", { text: t("work_next") }), c.next) : null,
            el("div", { "class": "links" }, docLink(c.path, t("work_resume"))));
        }))
      : el("p", { "class": "empty", text: t("work_empty") });
    main(heading(t("work_title"), t("work_why")), cards,
      w.notes ? [el("h2", { text: t("work_notes") }), el("p", { "class": "why", text: t("work_notes_why") }),
                 html(el("div", { "class": "prose prose-box" }), w.notes.html)] : null,
      w.register ? el("p", null, docLink(w.register, t("work_register"))) : null);
  }

  var unitsView = "columns", unitsLens = "";

  function pageUnits() {
    if (!C.meta.units_page) return notFound();
    setNav("units");
    var units = C.units || [];
    var title = t("units_" + C.meta.units_page);
    if (!units.length) return main(heading(title, t("units_why")), el("p", { "class": "empty", text: t("units_empty") }));
    var lenses = units.map(function (u) { return u.lens; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort();
    var shown = units.filter(function (u) { return !unitsLens || u.lens === unitsLens; });
    function lensName(l) { return Object.prototype.hasOwnProperty.call(S, "lens_" + l) ? t("lens_" + l) : l; }
    function dates(u) { return [u.start, u.end].filter(written).join(" → "); }
    var bar = el("div", { "class": "toolbar" },
      el("span", { "class": "seg" },
        el("button", { type: "button", "class": unitsView === "columns" ? "on" : "", onclick: function () { unitsView = "columns"; pageUnits(); } }, t("units_columns")),
        el("button", { type: "button", "class": unitsView === "list" ? "on" : "", onclick: function () { unitsView = "list"; pageUnits(); } }, t("units_list"))),
      lenses.length > 1
        ? el("label", null, t("units_lens"), " ",
            el("select", { onchange: function (e) { unitsLens = e.target.value; pageUnits(); } },
              el("option", { value: "", text: t("units_lens_all") }),
              lenses.map(function (l) { return el("option", { value: l, text: lensName(l), selected: l === unitsLens }); })))
        : null);
    var body;
    if (unitsView === "columns") {
      var groups = [];
      shown.forEach(function (u) { if (groups.indexOf(u.group) < 0) groups.push(u.group); });
      groups.sort(function (a, b) { return a - b; });
      body = el("div", { "class": "columns" }, groups.map(function (g) {
        return el("section", { "class": "column" }, el("h3", { text: t("group_" + g) }),
          shown.filter(function (u) { return u.group === g; }).map(function (u) {
            return el("div", { "class": "unit" },
              el("span", { "class": "id", text: u.id || "" }),
              docLink(u.path, u.name),
              el("div", { "class": "muted" }, [u.status, u.level ? levelLabel(u.level) : null, lensName(u.lens), dates(u)].filter(written).join(" · ")));
          }));
      }));
    } else {
      body = el("table", { "class": "list" },
        el("thead", null, el("tr", null, [t("units_id"), t("units_name"), t("work_status"), t("work_level"), t("units_lens"), t("units_dates")].map(function (h) { return el("th", { text: h }); }))),
        el("tbody", null, shown.map(function (u) {
          return el("tr", null, el("td", null, el("code", { text: u.id || "" })), el("td", null, docLink(u.path, u.name)),
            el("td", null, u.status ? statusPill(u.status, u.group) : ""), el("td", { text: u.level ? levelLabel(u.level) : "" }),
            el("td", { text: lensName(u.lens) }), el("td", { text: dates(u) }));
        })));
    }
    main(heading(title, t("units_why")), bar, body);
  }

  function ruleList(items, withStatus) {
    return el("ul", null, items.map(function (r) {
      return el("li", null, docLink(r.path, r.title),
        withStatus && r.status ? [" ", el("span", { "class": "pill", text: r.status })] : null,
        r.when ? el("div", { "class": "muted", text: withStatus ? r.when : t("rules_when", { when: r.when }) }) : null);
    }));
  }

  function pageRules() {
    setNav("rules");
    var r = C.rules;
    var any = r.vision.length || r.decisions.length;
    main(heading(t("rules_title"), t("rules_why")),
      any ? null : el("p", { "class": "empty", text: t("rules_empty") }),
      r.vision.length ? [el("h2", { text: t("rules_vision") }), ruleList(r.vision, true)] : null,
      r.decisions.length ? [el("h2", { text: t("rules_decisions") }), el("p", { "class": "why", text: t("rules_decisions_why") }), ruleList(r.decisions)] : null,
      el("div", { "class": "links" }, r.manifest ? docLink(r.manifest, t("rules_manifest")) : null,
        link("#/guides", t("rules_see_guides"))));
  }

  // The guides (R26): which guide to read before which task, the operative guides with
  // when to read each and their status as declared, then the maps of complex parts.
  function guideList(items) {
    return el("ul", { "class": "guides" }, items.map(function (g) {
      return el("li", null, docLink(g.path, g.title),
        g.status ? [" ", el("span", { "class": "pill", text: g.status })] : null,
        g.when ? el("div", { "class": "muted", text: t("rules_when", { when: g.when }) }) : null);
    }));
  }

  function pageGuides() {
    setNav("guides");
    var g = C.guides;
    var any = g.operative.length || g.comprehension.length;
    main(heading(t("guides_title"), t("guides_why")),
      g.router ? el("p", { "class": "router" }, docLink(g.router, t("guides_router")),
        el("span", { "class": "why-line", text: t("guides_router_why") })) : null,
      any ? null : el("p", { "class": "empty", text: t("guides_empty") }),
      g.operative.length ? [el("h2", { text: t("guides_operative") }), el("p", { "class": "why", text: t("guides_operative_why") }), guideList(g.operative)] : null,
      g.comprehension.length ? [el("h2", { text: t("guides_comprehension") }), el("p", { "class": "why", text: t("guides_comprehension_why") }), guideList(g.comprehension)] : null);
  }

  function folderName(f) {
    var key = "folder_" + f.replace(/[\/\\]/g, "_");
    return Object.prototype.hasOwnProperty.call(S, key) ? t(key) : f;
  }

  function pageDocuments() {
    setNav("documents");
    main(heading(t("documents_title"), t("documents_why")),
      C.tree.length
        ? el("div", { "class": "tree" }, C.tree.map(function (f) {
            return el("details", { open: C.tree.length < 8 },
              el("summary", null, folderName(f.folder), f.folder ? el("span", { "class": "muted", text: f.folder + "/" }) : null),
              el("ul", null, f.docs.map(function (d) { return el("li", null, docLink(d.path, d.title)); })));
          }))
        : el("p", { "class": "empty", text: t("documents_empty") }));
  }

  function docAt(path, id) { return docHref(path) + "?at=" + encodeURIComponent(id); }

  function pageDoc(address) {
    setNav("documents");
    var at = address.split("?at=");
    var path = at[0];
    needDocs(function () {
      var d = D[path];
      if (!d) return notFound();
      // the document's own first heading is its title; the body follows the chain
      var body = d.html.replace(/^<h1[^>]*>[\s\S]*?<\/h1>/, "");
      main(el("h1", { text: d.title }),
        el("p", { "class": "muted" }, el("code", { text: path })),
        d.meta.length ? el("div", { "class": "doc-meta", title: t("doc_about") }, d.meta.map(function (kv) {
          return el("span", { "class": "label" }, el("b", { text: kv[0] }), kv[1]);
        })) : null,
        d.chain ? chainStrip(d.chain) : null,
        html(el("article", { "class": "prose" }), body));
      if (at[1]) {
        var dest = document.getElementById(at[1]);
        if (dest) dest.scrollIntoView();
      }
    });
  }

  // An analysis read as the chain the agent works through (R24): one row per step,
  // each linking to its sections as written; a step with none says so. Nothing here
  // counts, scores or marks completeness.
  function chainStrip(chain) {
    function jump(id, label) {
      return el("a", { href: "#" + id, onclick: function (e) {
        e.preventDefault();
        var dest = document.getElementById(id);
        if (dest) dest.scrollIntoView({ behavior: "smooth" });
      } }, label);
    }
    var c = chain.companions || {};
    return el("nav", { "class": "chain", "aria-label": t("chain_title") },
      el("h2", { text: t("chain_title") }),
      el("ol", null, chain.steps.map(function (s) {
        // what this analysis has for the step: its sections (for "merge and tests", the
        // unit's own merge brief and E2E script). Only that decides "Not in this analysis";
        // the project's North Star and the request record sit beside it, never in place of it.
        var own = s.sections.map(function (sec) { return jump(sec.id, sec.title); });
        if (s.step === "merge_tests") {
          if (c.merge) own.push(docLink(c.merge, t("chain_merge")));
          if (c.e2e) own.push(docLink(c.e2e, t("chain_e2e")));
        }
        var beside = [];
        if (s.step === "vision" && chain.north_star) beside.push(link(docAt(chain.north_star.path, chain.north_star.id), t("chain_north_star")));
        if (s.step === "vision" && c.request) beside.push(docLink(c.request, t("chain_request")));
        return el("li", { "class": own.length ? "" : "absent" },
          el("span", { "class": "step" }, el("b", { text: t("chain_step_" + s.step) }),
            el("span", { "class": "why-line", text: t("chain_step_" + s.step + "_why") })),
          el("span", { "class": "links" }, own.length ? own : el("span", { "class": "muted", text: t("chain_absent") }), beside));
      })));
  }

  // ----------------------------------------------------- what is known

  // The one way a fact's text becomes a label or a tooltip: a fact resting on a
  // person's statement says so wherever its text appears (criterion 6).
  function factTitle(f) { return f.statement ? t("statement_prefix", { text: f.text }) : f.text; }

  function factLine(id, opts) {
    var f = K.facts[id];
    if (!f) return el("li", { "class": "fact" }, el("span"), el("span", { "class": "muted", text: id + " — " + t("fact_unknown") }));
    var oc = originClass(f.origin);
    var marks = [el("span", { "class": "tag o-" + oc, title: originWhy(f.origin), text: originLabel(f.origin) })];
    if (f.statement) marks.push(el("span", { "class": "tag statement", title: t("statement_notice"), text: t("statement_mark") }));
    if (f.state === "superseded") marks.push(el("span", { "class": "tag replaced", title: t("state_superseded_why"), text: t("state_superseded") }));
    if (f.state === "contested") marks.push(el("span", { "class": "tag conflict", title: t("state_contested_why"), text: t("state_contested") }));
    if (opts && opts.topic) marks.push(link("#/topic/" + encodeURIComponent(f.topic), f.topic, "chip"));
    return el("li", { "class": "fact" + (f.state === "superseded" ? " replaced" : ""), onclick: function () { location.hash = "#/fact/" + encodeURIComponent(id); } },
      el("span", { "class": "dot bg-" + oc }),
      el("span", null, el("span", { "class": "text", text: f.text }), el("div", { "class": "marks" }, marks)));
  }

  function topicPage(slug) {
    needKb(function () {
      var tp = K.topics[slug];
      if (!tp) return notFound();
      if (tp.merged_into) { location.replace("#/topic/" + encodeURIComponent(tp.merged_into)); return; }
      setNav("map");
      var filterText = "", filterOrigin = "";
      var list = el("ul", { "class": "facts" });
      function refill() {
        list.textContent = "";
        var q = normalize(filterText).split(" ").filter(Boolean);
        var ids = tp.facts.filter(function (id) {
          var f = K.facts[id];
          if (!f) return true;
          if (filterOrigin && f.origin !== filterOrigin) return false;
          var n = normalize(f.text);
          return q.every(function (w) { return n.indexOf(w) >= 0; });
        });
        add(list, ids.length ? ids.map(function (id) { return factLine(id); }) : el("li", { "class": "muted", text: t("topic_no_facts") }));
      }
      function chipsOf(slugs) {
        return el("div", { "class": "chips" }, slugs.map(function (s) { return link("#/topic/" + encodeURIComponent(s), K.topics[s] ? K.topics[s].name : s, "chip"); }));
      }
      var dl = [];
      function row(label, v) { if (v) dl.push(el("dt", { text: t(label) }), el("dd", null, v)); }
      row("topic_area", tp.area ? link("#/topic/" + encodeURIComponent(tp.area), K.topics[tp.area].name) : el("span", { "class": "muted", text: t("topic_no_area") }));
      row("topic_parents", tp.parents.length ? chipsOf(tp.parents) : null);
      row("topic_aka", tp.aka.length ? tp.aka.join(" · ") : null);
      row("topic_gaps", tp.gaps.length ? tp.gaps.join(" · ") : null);
      row("topic_related", tp.related.length ? chipsOf(tp.related) : null);
      row("topic_children", tp.children.length ? chipsOf(tp.children) : null);
      var used = tp.facts.map(function (id) { return K.facts[id] && K.facts[id].origin; })
        .filter(function (v, i, a) { return v && a.indexOf(v) === i; });
      main(el("h1", { text: tp.name }),
        el("p", { "class": "muted" }, el("code", { text: slug }), " · ",
          tp.count === 1 ? t("topic_facts_one") : t("topic_facts_count", { n: tp.count }), " · ",
          link("#/map/" + encodeURIComponent(slug), t("topic_on_map"))),
        tp.description ? el("p", { "class": "intro", text: tp.description }) : null,
        el("div", { "class": "panel-inline" }, el("dl", { "class": "card", style: null }, dl)),
        el("h2", { text: t("topic_facts") }),
        el("div", { "class": "toolbar" },
          el("input", { type: "search", placeholder: t("topic_filter"), oninput: function (e) { filterText = e.target.value; refill(); } }),
          used.length > 1 ? el("select", { onchange: function (e) { filterOrigin = e.target.value; refill(); } },
            el("option", { value: "", text: t("topic_origin_all") }),
            used.map(function (o) { return el("option", { value: o, text: originLabel(o) }); })) : null),
        list);
      refill();
    });
  }

  function whereText(w) {
    if (!w) return "";
    if (w.page) return t("fact_page", { n: w.page });
    if (w.lines) return w.lines[0] === w.lines[1] ? t("fact_line", { a: w.lines[0] }) : t("fact_lines", { a: w.lines[0], b: w.lines[1] });
    return "";
  }

  function sourceBlock(s) {
    var target = s.source
      ? link("#/source/" + encodeURIComponent(s.source), s.source)
      : s.path.indexOf("corpus/notes/") === 0 ? docLink(s.path, s.path.split("/").pop()) : docLink(s.path);
    var body = [];
    if (s.passage !== undefined) {
      body.push(el("div", { "class": "passage" }, s.before || "", el("mark", { text: s.passage }), s.after || ""));
    } else if (s.reason) {
      body.push(el("div", { "class": "reason", text: t("reason_" + s.reason, s.where || {}) }));
    }
    return el("div", { "class": "src" },
      el("div", { "class": "head" }, target, el("span", { "class": "muted", text: whereText(s.where) })),
      body);
  }

  function factPanel(id) {
    needKb(function () {
      closePanel();
      var f0 = K.facts[id];
      if (!lastPage) {
        lastPage = f0 && K.topics[f0.topic] ? "#/topic/" + encodeURIComponent(f0.topic) : "#/";
        if (f0 && K.topics[f0.topic]) topicPage(f0.topic); else pageHome();
      }
      var f = K.facts[id];
      var box = el("aside", { "class": "panel" });
      var close = el("button", { "class": "close", type: "button", onclick: leavePanel }, t("fact_close"));
      if (!f) { add(box, [close, el("h2", { text: t("fact_title") }), el("p", { "class": "empty", text: t("fact_unknown") })]); return openPanel(box); }
      var dl = [];
      function row(label, v) { if (v) dl.push(el("dt", { text: t(label) }), el("dd", null, v)); }
      row("fact_origin", el("span", null, el("span", { "class": "o-" + originClass(f.origin), text: originLabel(f.origin) }),
        el("span", { "class": "why-line", text: originWhy(f.origin) })));
      if (written(f.valid)) row("fact_valid", f.valid);
      if (written(f.qty)) row("fact_qty", f.qty);
      if (written(f.about)) row("fact_about", f.about);
      row("fact_topic", link("#/topic/" + encodeURIComponent(f.topic), K.topics[f.topic] ? K.topics[f.topic].name : f.topic));
      var parts = [];
      if (f.state === "superseded") {
        parts.push(el("h3", null, el("span", { "class": "tag replaced", text: t("state_superseded") }), " ", t("fact_replaced_by")),
          el("p", { "class": "why-line", text: t("state_superseded_why") }),
          el("ul", { "class": "facts" }, (f.successors || []).map(function (s) { return factLine(s, { topic: true }); })),
          el("h3", { text: t("fact_current_at_end") }),
          el("ul", { "class": "facts" }, (f.chain_ends || []).map(function (e) {
            if (e.stop) return el("li", { "class": "reason", text: t("chain_" + e.stop, { id: e.id }) });
            return factLine(e.id, { topic: true });
          })));
      }
      if (f.state === "contested") {
        parts.push(el("h3", null, el("span", { "class": "tag conflict", text: t("state_contested") }), " ", t("fact_in_conflict_with")),
          el("p", { "class": "why-line", text: t("state_contested_why") }),
          el("ul", { "class": "facts" }, (f.with || []).map(function (s) { return factLine(s, { topic: true }); })));
      }
      if (f.grounds) {
        parts.push(el("h3", { text: t("fact_rests_on") }),
          el("p", { "class": "why-line", text: t("ground_class_" + f.ground_class) }),
          el("ul", null, f.grounds.map(function (g) {
            var what = t("ground_" + g.kind);
            var where = g.path ? (g.path.indexOf("corpus/given/") === 0
              ? link("#/source/" + encodeURIComponent(g.path.slice(13)), g.path.slice(13))
              : docLink(g.path, g.path.split("/").pop())) : null;
            return el("li", null, el("b", { text: what }), where ? [" — ", where] : null,
              g.kind === "untraceable" ? el("div", { "class": "reason" }, t("fact_untraced"), g.entry ? [" ", el("code", { text: g.entry })] : null) : null);
          })));
      }
      parts.push(el("h3", { text: t("fact_sources") }), f.sources.map(sourceBlock));
      add(box, [close, el("div", { "class": "muted" }, el("code", { text: id })),
        el("div", { "class": "ftext", text: f.text }),
        f.statement ? el("div", { "class": "statement-notice" }, el("b", { text: t("statement_mark") + ": " }), t("statement_notice")) : null,
        el("dl", null, dl), parts]);
      openPanel(box);
    });
  }

  function leavePanel() { location.hash = lastPage || "#/"; }

  function openPanel(box) { panelEl = box; document.body.appendChild(box); }
  function closePanel() {
    Array.prototype.forEach.call(document.querySelectorAll(".panel"), function (p) { p.remove(); });
    panelEl = null;
  }

  function readText(r) {
    if (!r) return "";
    if (r.kind === "complete") return t("read_complete");
    if (r.kind === "page") return r.of ? t("read_page_of", { n: r.n, m: r.of }) : t("read_page", { n: r.n });
    if (r.kind === "line") return r.of ? t("read_line_of", { n: r.n, m: r.of }) : t("read_line", { n: r.n });
    if (r.kind === "unreadable") return t("read_unreadable");
    return t("read_unrecorded");
  }

  function pageSources() {
    needKb(function () {
      setNav("sources");
      var names = Object.keys(K.sources).sort();
      if (!names.length) return main(heading(t("sources_title"), t("sources_why")), el("p", { "class": "empty", text: t("sources_empty") }));
      main(heading(t("sources_title"), t("sources_why")),
        el("table", { "class": "list" },
          el("thead", null, el("tr", null, ["source_name", "source_kind", "source_date", "source_facts", "source_topics"].map(function (k) { return el("th", { text: t(k) }); }))),
          el("tbody", null, names.map(function (n) {
            var s = K.sources[n];
            return el("tr", null, el("td", null, link("#/source/" + encodeURIComponent(n), n)), el("td", { text: s.kind }),
              el("td", { text: s.date }), el("td", { text: String(s.facts) }),
              el("td", null, el("div", { "class": "chips" }, s.topics.map(function (tp) { return link("#/topic/" + encodeURIComponent(tp), tp, "chip"); }))));
          }))));
    });
  }

  function pageSource(name) {
    needKb(function () {
      var s = K.sources[name];
      if (!s) return notFound();
      setNav("sources");
      var dl = [];
      function row(label, v) { if (written(v) || (v && v.nodeType)) dl.push(el("dt", { text: t(label) }), el("dd", null, v)); }
      row("source_kind", s.kind);
      row("source_date", s.date);
      row("source_facts", String(s.facts));
      row("source_read", readText(s.read));
      row("source_newer", s.older_of ? link("#/source/" + encodeURIComponent(s.older_of), s.older_of) : null);
      row("source_older", s.newer_of ? (K.sources[s.newer_of] ? link("#/source/" + encodeURIComponent(s.newer_of), s.newer_of) : s.newer_of) : null);
      row("source_topics", s.topics.length ? el("div", { "class": "chips" }, s.topics.map(function (tp) { return link("#/topic/" + encodeURIComponent(tp), tp, "chip"); })) : null);
      row("source_record", docLink(s.sidecar, s.sidecar.split("/").pop()));
      var ids = Object.keys(K.facts).filter(function (id) {
        return K.facts[id].sources.some(function (x) { return x.source === name; });
      }).sort();
      main(el("h1", { text: name }), el("dl", { "class": "card" }, dl),
        el("h2", { text: t("source_facts_list") }),
        el("ul", { "class": "facts" }, ids.map(function (id) { return factLine(id, { topic: true }); })));
    });
  }

  // ----------------------------------------------------------- the map

  var mapView = "topics";
  var hidden = {};

  function areaColors() {
    var areas = K.order.filter(function (s) { return K.topics[s].area === s; });
    var colors = {};
    areas.forEach(function (a, i) {
      var hue = Math.round((i * 137.508 + 28) % 360);
      colors[a] = "hsl(" + hue + ", 46%, 62%)";
    });
    return colors;
  }

  function originColor(o) {
    return getComputedStyle(document.documentElement).getPropertyValue("--o-" + originClass(o)).trim() || "#888";
  }

  function pageMap(slug) {
    needKb(function () {
      setNav("map");
      if (slug !== undefined && !K.topics[slug]) return notFound();
      if (slug && K.topics[slug].merged_into) { location.replace("#/map/" + encodeURIComponent(K.topics[slug].merged_into)); return; }
      // the address decides the view: #/map/<slug> is one topic up close; #/map is
      // the topics view, or everything when its button was pressed (the side bar's
      // Map resets to topics)
      if (slug) { mapView = "close"; lastFocus = slug; }
      else if (mapView === "close") mapView = "topics";
      var focus = slug || lastFocus || K.order.filter(function (s) { return K.topics[s].area === s; })[0] || K.order[0];
      var ctl = null;
      var views = el("span", { "class": "seg" },
        ["topics", "close", "every"].map(function (v) {
          return el("button", { type: "button", "class": mapView === v ? "on" : "", disabled: v === "close" && !focus, onclick: function () {
            if (v === "close") { location.hash = "#/map/" + encodeURIComponent(focus); return; }
            mapView = v;
            if (slug) location.hash = "#/map"; else pageMap();
          } }, t("map_view_" + v));
        }));
      var zoom = el("span", { "class": "seg" },
        el("button", { type: "button", title: t("map_zoom_out_why"), onclick: function () { if (ctl) ctl.zoom(1 / 1.4); } }, t("map_zoom_out")),
        el("button", { type: "button", title: t("map_zoom_in_why"), onclick: function () { if (ctl) ctl.zoom(1.4); } }, t("map_zoom_in")),
        el("button", { type: "button", onclick: function () { if (ctl) ctl.fit(); } }, t("map_fit")));
      var wrap = el("div", { "class": "mapwrap" });
      var canvas = el("canvas");
      var tip = el("div", { "class": "tip" });
      wrap.appendChild(canvas);
      wrap.appendChild(tip);
      wrap.appendChild(el("div", { "class": "maphint", text: t(mapView === "close" ? "map_hint_close" : "map_hint") }));
      main(heading(t("map_title"), t(mapView === "close" ? "map_why_close" : mapView === "every" ? "map_why_every" : "map_why")),
        el("div", { "class": "toolbar" }, views, zoom,
          mapView === "close" ? link("#/topic/" + encodeURIComponent(focus), t("map_open_topic", { name: K.topics[focus].name })) : null), wrap);
      mainEl.className = "wide";
      if (!K.order.length) { wrap.textContent = ""; add(wrap, el("p", { "class": "empty", text: t("map_empty") })); return; }
      var g = mapView === "close" ? closeGraph(focus) : mapView === "every" ? everyGraph() : topicGraph();
      wrap.appendChild(legend(g, function () { if (ctl) ctl.draw(); }));
      ctl = canvasGraph(canvas, tip, g);
    });
  }

  var lastFocus = null;

  function topicGraph() {
    var colors = areaColors();
    var nodes = K.map.nodes.map(function (n) {
      return { id: n.id, x: n.x, y: n.y, r: 5 + 2.2 * Math.sqrt(n.count), kind: "topic",
               color: n.area ? colors[n.area] : "#6c747d", label: K.topics[n.id].name,
               href: "#/map/" + encodeURIComponent(n.id), tip: K.topics[n.id].name + (n.area ? "" : " · " + t("map_no_area")) };
    });
    var edges = K.map.edges.map(function (e) {
      return { a: e.a, b: e.b, style: e.kind === "related" ? "dash" : e.kind === "shared" ? "thin" : "solid",
               w: e.kind === "shared" ? Math.min(4, 0.6 + Math.log(1 + e.n)) : 1.4 };
    });
    var keys = [["solid", "map_edge_part"], ["dash", "map_edge_related"], ["thin", "map_edge_shared"]];
    return { nodes: nodes, edges: edges, labels: true, edgeKeys: keys, kinds: ["topic"], origins: false };
  }

  function closeGraph(slug) {
    var tp = K.topics[slug];
    var nodes = [], edges = [], byId = {};
    function node(n) { if (!byId[n.id]) { byId[n.id] = n; nodes.push(n); } return byId[n.id]; }
    node({ id: "t:" + slug, x: 0, y: 0, r: 14, kind: "topic", color: "#d9a441", label: tp.name, href: "#/topic/" + encodeURIComponent(slug), tip: tp.name });
    var ids = tp.facts.slice();
    tp.facts.forEach(function (id) {
      var f = K.facts[id];
      if (!f) return;
      (f.successors || []).concat(f.with || []).forEach(function (o) { if (ids.indexOf(o) < 0 && K.facts[o]) ids.push(o); });
    });
    var ring = Math.max(170, ids.length * 9);
    ids.forEach(function (id, i) {
      var f = K.facts[id];
      if (!f) return;
      var a = 2 * Math.PI * i / Math.max(1, ids.length);
      node({ id: "f:" + id, x: ring * Math.cos(a), y: ring * Math.sin(a), r: 6, kind: "fact", origin: f.origin,
             color: originColor(f.origin), dim: f.state === "superseded", conflict: f.state === "contested",
             statement: f.statement, label: factTitle(f), href: "#/fact/" + encodeURIComponent(id), tip: factTitle(f) });
      if (f.topic === slug) edges.push({ a: "f:" + id, b: "t:" + slug, style: "thin", w: 1 });
    });
    var outer = [], outerSet = {};
    ids.forEach(function (id) {
      var f = K.facts[id];
      if (!f) return;
      f.sources.forEach(function (s) { var k = s.source ? "s:" + s.source : "n:" + s.path; if (!outerSet[k]) { outerSet[k] = 1; outer.push([k, s]); } });
      (f.grounds || []).forEach(function (gr) { if (gr.path) { var k = gr.path.indexOf("corpus/given/") === 0 ? "s:" + gr.path.slice(13) : "n:" + gr.path; if (!outerSet[k]) { outerSet[k] = 1; outer.push([k, { path: gr.path, source: k.slice(0, 2) === "s:" ? gr.path.slice(13) : null }]); } } });
    });
    var ring2 = ring + 170;
    outer.forEach(function (o, i) {
      var a = 2 * Math.PI * (i + 0.5) / Math.max(1, outer.length);
      var s = o[1], isSrc = o[0].slice(0, 2) === "s:";
      node({ id: o[0], x: ring2 * Math.cos(a), y: ring2 * Math.sin(a), r: 7, kind: isSrc ? "source" : "note",
             color: isSrc ? "#c9c2b2" : "#8b93a0", square: true, label: (isSrc ? s.source : s.path.split("/").pop()),
             href: isSrc ? "#/source/" + encodeURIComponent(s.source) : docHref(s.path), tip: isSrc ? s.source : s.path });
    });
    ids.forEach(function (id) {
      var f = K.facts[id];
      if (!f) return;
      f.sources.forEach(function (s) { var k = s.source ? "s:" + s.source : "n:" + s.path; if (byId[k]) edges.push({ a: "f:" + id, b: k, style: "solid", w: 1 }); });
      (f.grounds || []).forEach(function (gr) { if (!gr.path) return; var k = gr.path.indexOf("corpus/given/") === 0 ? "s:" + gr.path.slice(13) : "n:" + gr.path; if (byId[k]) edges.push({ a: "f:" + id, b: k, style: "based", w: 1.2 }); });
      (f.successors || []).forEach(function (o) { if (byId["f:" + o]) edges.push({ a: "f:" + id, b: "f:" + o, style: "dash", w: 1.2 }); });
      (f.with || []).forEach(function (o) { if (byId["f:" + o]) edges.push({ a: "f:" + id, b: "f:" + o, style: "conflict", w: 1.4 }); });
    });
    Object.keys(K.sources).forEach(function (n) {
      var s = K.sources[n];
      if (s.newer_of && byId["s:" + n] && byId["s:" + s.newer_of]) edges.push({ a: "s:" + n, b: "s:" + s.newer_of, style: "newer", w: 1.2 });
    });
    var keys = [["thin", "topic_facts"], ["solid", "fact_sources"], ["based", "map_edge_based"], ["newer", "map_edge_newer"], ["dash", "map_edge_replaced"], ["conflict", "map_edge_conflict"]];
    return { nodes: nodes, edges: edges, labels: true, edgeKeys: keys, kinds: ["topic", "fact", "source", "note"], origins: true };
  }

  function everyGraph() {
    var g = topicGraph();
    g.edges = g.edges.filter(function (e) { return e.style !== "thin"; });
    var topics = g.nodes;
    g.nodes = [];
    K.map.every.forEach(function (n) {
      if (n.kind === "fact") {
        var f = K.facts[n.id];
        if (!f) return;
        g.nodes.push({ id: "f:" + n.id, x: n.x, y: n.y, r: 2.2, kind: "fact", origin: f.origin, color: originColor(f.origin),
                       dim: f.state === "superseded", conflict: f.state === "contested", statement: f.statement, label: factTitle(f), href: "#/fact/" + encodeURIComponent(n.id), tip: factTitle(f) });
      } else {
        g.nodes.push({ id: "s:" + n.id, x: n.x, y: n.y, r: 3.5, kind: "source", color: "#c9c2b2", square: true,
                       label: n.id, href: "#/source/" + encodeURIComponent(n.id), tip: n.id });
      }
    });
    g.nodes = g.nodes.concat(topics);   // topics drawn last, on top of their facts
    g.labels = true;
    g.kinds = ["topic", "fact", "source"];
    g.origins = true;
    return g;
  }

  var KIND_SWATCH = { topic: "#d9a441", fact: "#9aa3ad", source: "#c9c2b2", note: "#8b93a0" };

  function legend(g, redraw) {
    var box = el("details", { "class": "legend", open: window.innerWidth > 1000 });
    add(box, el("summary", { text: t("map_legend") }));
    function toggle(key, label, swatch) {
      var cb = el("input", { type: "checkbox", checked: !hidden[key], onchange: function (e) { hidden[key] = !e.target.checked; redraw(); } });
      return el("label", null, cb, swatch, label);
    }
    if (g.origins) {
      add(box, el("h4", { text: t("fact_origin") }));
      ORIGINS.forEach(function (o) {
        add(box, toggle("o:" + o, originLabel(o), el("span", { "class": "sw bg-" + o })));
      });
    }
    if (g.kinds.length > 1) {
      add(box, el("h4", { text: t("map_kinds") }));
      g.kinds.forEach(function (k) {
        var sw = el("span", { "class": "sw" + (k === "source" || k === "note" ? " sq" : "") });
        sw.style.background = KIND_SWATCH[k];
        add(box, toggle("k:" + k, t("map_kind_" + k), sw));
      });
    }
    add(box, el("h4", { text: t("map_lines") }));
    g.edgeKeys.forEach(function (k) { add(box, el("label", null, el("span", { "class": "ln " + k[0] }), t(k[1]))); });
    if (g.origins) add(box, el("label", { title: t("statement_notice") }, el("span", { "class": "sw ring" }), t("statement_mark")));
    add(box, el("label", null, el("span", { "class": "tag replaced", text: t("state_superseded") })),
      el("label", null, el("span", { "class": "tag conflict", text: t("state_contested") })));
    return box;
  }

  function canvasGraph(canvas, tip, g) {
    var ctx = canvas.getContext("2d");
    var byId = {};
    g.nodes.forEach(function (n) { byId[n.id] = n; });
    var view = { s: 1, x: 0, y: 0 };
    var W = 0, H = 0, dpr = window.devicePixelRatio || 1;

    function visible(n) {
      if (hidden["k:" + n.kind]) return false;
      if (n.origin && hidden["o:" + originClass(n.origin)]) return false;
      return true;
    }
    function fit() {
      var r = canvas.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      var xs = g.nodes.map(function (n) { return n.x; }), ys = g.nodes.map(function (n) { return n.y; });
      var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
      var pad = 60;
      view.s = Math.min((W - 2 * pad) / Math.max(1, x1 - x0), (H - 2 * pad) / Math.max(1, y1 - y0), 2.2);
      view.x = W / 2 - view.s * (x0 + x1) / 2;
      view.y = H / 2 - view.s * (y0 + y1) / 2;
    }
    function sx(x) { return view.x + view.s * x; }
    function sy(y) { return view.y + view.s * y; }
    function draw() {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      g.edges.forEach(function (e) {
        var a = byId[e.a], b = byId[e.b];
        if (!a || !b || !visible(a) || !visible(b)) return;
        ctx.beginPath();
        ctx.setLineDash(e.style === "dash" ? [6, 5] : e.style === "newer" ? [2, 4] : []);
        ctx.strokeStyle = e.style === "thin" ? "rgba(120,132,145,0.35)" : e.style === "based" ? "rgba(169,155,224,0.7)"
          : e.style === "newer" ? "rgba(111,183,168,0.8)" : e.style === "conflict" ? "rgba(224,96,90,0.85)" : "rgba(160,168,178,0.55)";
        ctx.lineWidth = e.w;
        ctx.moveTo(sx(a.x), sy(a.y));
        ctx.lineTo(sx(b.x), sy(b.y));
        ctx.stroke();
      });
      ctx.setLineDash([]);
      var rs = Math.max(0.6, Math.min(1.6, Math.sqrt(view.s)));
      g.nodes.forEach(function (n) {
        if (!visible(n)) return;
        var r = n.r * rs;
        ctx.globalAlpha = n.dim ? 0.35 : 1;
        ctx.fillStyle = n.color;
        ctx.beginPath();
        if (n.square) ctx.rect(sx(n.x) - r, sy(n.y) - r, 2 * r, 2 * r);
        else ctx.arc(sx(n.x), sy(n.y), r, 0, 2 * Math.PI);
        ctx.fill();
        if (n.conflict) { ctx.strokeStyle = "#e0605a"; ctx.lineWidth = 2; ctx.stroke(); }
        if (n.statement) {
          ctx.beginPath();
          ctx.arc(sx(n.x), sy(n.y), r + 2.5, 0, 2 * Math.PI);
          ctx.strokeStyle = "#e0a24a"; ctx.lineWidth = 1.5; ctx.setLineDash([2, 2]); ctx.stroke(); ctx.setLineDash([]);
        }
        ctx.globalAlpha = 1;
      });
      if (g.labels) labels(rs);
    }

    // Every node carries its label; a label is drawn only where it can be read
    // whole without touching another one. Topics first, then documents and notes,
    // then facts -- whose text is wrapped, never cut. Zooming in makes room, so
    // more labels appear.
    var PRIORITY = { topic: 0, source: 1, note: 1, fact: 2 };
    var labelled = g.nodes.filter(function (n) { return n.label; }).sort(function (a, b) {
      return (PRIORITY[a.kind] - PRIORITY[b.kind]) || (b.r - a.r) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
    });
    var family = null;
    function fontOf(n) { return (n.kind === "topic" ? "600 12.5px " : n.kind === "fact" ? "11.5px " : "11px ") + family; }
    function linesOf(n) {
      if (n._lines) return n._lines;
      ctx.font = fontOf(n);
      var maxW = n.kind === "fact" ? 220 : Infinity, lines = [], cur = "";
      String(n.label).split(/\s+/).forEach(function (w) {
        var next = cur ? cur + " " + w : w;
        if (cur && ctx.measureText(next).width > maxW) { lines.push(cur); cur = w; } else cur = next;
      });
      if (cur) lines.push(cur);
      n._lines = lines;
      n._w = Math.max.apply(null, lines.map(function (l) { return ctx.measureText(l).width; }));
      n._lh = n.kind === "topic" ? 15 : 14;
      return lines;
    }
    function labels(rs) {
      family = family || getComputedStyle(document.body).fontFamily;
      var CELL = 96, grid = {};
      function keys(b) {
        var out = [];
        for (var gx = Math.floor(b.x0 / CELL); gx <= Math.floor(b.x1 / CELL); gx++)
          for (var gy = Math.floor(b.y0 / CELL); gy <= Math.floor(b.y1 / CELL); gy++) out.push(gx + ":" + gy);
        return out;
      }
      function free(b, ks) {
        return ks.every(function (k) {
          return !(grid[k] || []).some(function (o) { return b.x0 < o.x1 && o.x0 < b.x1 && b.y0 < o.y1 && o.y0 < b.y1; });
        });
      }
      ctx.textAlign = "center";
      ctx.textBaseline = "bottom";
      ctx.lineJoin = "round";
      labelled.forEach(function (n) {
        if (!visible(n)) return;
        var x = sx(n.x), y = sy(n.y);
        if (x < -40 || x > W + 40 || y < -40 || y > H + 40) return;
        var lines = linesOf(n), h = lines.length * n._lh, top = y - n.r * rs - 4 - h;
        var b = { x0: x - n._w / 2 - 3, x1: x + n._w / 2 + 3, y0: top - 2, y1: top + h + 2 };
        if (b.x0 < 0 || b.x1 > W || b.y0 < 0 || b.y1 > H) return;
        var ks = keys(b);
        if (!free(b, ks)) return;
        ks.forEach(function (k) { (grid[k] = grid[k] || []).push(b); });
        ctx.font = fontOf(n);
        lines.forEach(function (ln, i) {
          var yy = top + (i + 1) * n._lh;
          ctx.strokeStyle = "rgba(12,15,19,0.92)";
          ctx.lineWidth = 4;
          ctx.strokeText(ln, x, yy);
          ctx.fillStyle = n.kind === "topic" ? "#e8e2d4" : n.kind === "fact" ? "#d2ccbe" : "#b9b2a3";
          ctx.fillText(ln, x, yy);
        });
      });
    }
    function at(px, py) {
      var best = null, bd = 1e9;
      g.nodes.forEach(function (n) {
        if (!visible(n)) return;
        var d = Math.hypot(sx(n.x) - px, sy(n.y) - py);
        if (d < Math.max(8, n.r * 1.6) && d < bd) { bd = d; best = n; }
      });
      return best;
    }
    var drag = null, moved = false;
    canvas.addEventListener("mousedown", function (e) { drag = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y }; moved = false; canvas.style.cursor = ""; canvas.className = "drag"; });
    window.addEventListener("mouseup", function () { drag = null; canvas.className = ""; });
    canvas.addEventListener("mousemove", function (e) {
      var r = canvas.getBoundingClientRect();
      if (drag) {
        var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
        if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
        view.x = drag.vx + dx; view.y = drag.vy + dy; draw(); return;
      }
      var n = at(e.clientX - r.left, e.clientY - r.top);
      if (n && n.tip) { tip.textContent = n.tip; tip.style.display = "block"; tip.style.left = (e.clientX - r.left + 14) + "px"; tip.style.top = (e.clientY - r.top + 10) + "px"; canvas.style.cursor = "pointer"; }
      else { tip.style.display = "none"; canvas.style.cursor = ""; }
    });
    canvas.addEventListener("click", function (e) {
      if (moved) return;
      var r = canvas.getBoundingClientRect();
      var n = at(e.clientX - r.left, e.clientY - r.top);
      if (n && n.href) location.hash = n.href;
    });
    canvas.addEventListener("wheel", function (e) {
      e.preventDefault();
      var r = canvas.getBoundingClientRect();
      var px = e.clientX - r.left, py = e.clientY - r.top;
      var k = Math.exp(-e.deltaY * 0.0015);
      k = Math.max(0.02, Math.min(60, view.s * k)) / view.s;
      view.x = px - (px - view.x) * k; view.y = py - (py - view.y) * k; view.s *= k;
      draw();
    }, { passive: false });
    window.addEventListener("resize", function () { if (canvas.isConnected) { fit(); draw(); } });
    fit();
    draw();
    return {
      draw: draw,
      fit: function () { fit(); draw(); },
      zoom: function (k) {
        var px = W / 2, py = H / 2;
        view.x = px - (px - view.x) * k; view.y = py - (py - view.y) * k; view.s *= k;
        draw();
      }
    };
  }

  // ---------------------------------------------------------- search

  var overlay = null;

  function openSearch() {
    if (overlay) return;
    var input = el("input", { type: "search", placeholder: t(C.meta.has_kb ? "search_placeholder" : "search_placeholder_docs") });
    var results = el("div", { "class": "results" });
    overlay = el("div", { "class": "overlay", onclick: function (e) { if (e.target === overlay) closeSearch(); } },
      el("div", { "class": "searchbox" }, input, results, el("div", { "class": "keys", text: t("search_keys") })));
    document.body.appendChild(overlay);
    input.focus();
    var hits = [], sel = 0;
    function render() {
      results.textContent = "";
      var q = normalize(input.value).split(" ").filter(Boolean);
      if (!q.length) return;
      function match(e) { return q.every(function (w) { return e.n.indexOf(w) >= 0; }); }
      var groups = [];
      if (K) {
        groups.push(["search_group_facts", K.search.filter(function (e) { return e.k === "fact"; }).filter(match), function (e) { return "#/fact/" + encodeURIComponent(e.id); }]);
        groups.push(["search_group_topics", K.search.filter(function (e) { return e.k === "topic"; }).filter(match), function (e) { return "#/topic/" + encodeURIComponent(e.id); }]);
      }
      groups.push(["search_group_documents", C.search.filter(match), function (e) { return docHref(e.path); }]);
      hits = [];
      groups.forEach(function (gr) {
        if (!gr[1].length) return;
        add(results, el("div", { "class": "grp", text: t(gr[0]) }));
        gr[1].slice(0, 40).forEach(function (e) {
          var a = el("a", { "class": "res", href: gr[2](e), onclick: closeSearch }, e.title || e.path,
            e.statement ? [" ", el("span", { "class": "tag statement", title: t("statement_notice"), text: t("statement_mark") })] : null,
            el("small", { text: e.path || e.id }));
          hits.push(a);
          results.appendChild(a);
        });
        if (gr[1].length > 40) add(results, el("div", { "class": "none", text: t("search_more", { n: gr[1].length - 40 }) }));
      });
      if (!hits.length) add(results, el("div", { "class": "none", text: t(C.meta.has_kb ? "search_none_kb" : "search_none_docs") }));
      sel = 0;
      mark();
    }
    function mark() { hits.forEach(function (a, i) { a.className = "res" + (i === sel ? " sel" : ""); }); if (hits[sel]) hits[sel].scrollIntoView({ block: "nearest" }); }
    input.addEventListener("input", render);
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { sel = Math.min(hits.length - 1, sel + 1); mark(); e.preventDefault(); }
      else if (e.key === "ArrowUp") { sel = Math.max(0, sel - 1); mark(); e.preventDefault(); }
      else if (e.key === "Enter" && hits[sel]) { location.hash = hits[sel].getAttribute("href"); closeSearch(); }
      else if (e.key === "Escape") closeSearch();
    });
    if (C.meta.has_kb && !K) {
      loadScript("data/kb.js", function () { K = window.DOCS_SITE_KB; render(); });
    }
  }

  function closeSearch() { if (overlay) { overlay.remove(); overlay = null; } }

  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); openSearch(); }
    else if (e.key === "Escape" && panelEl && !overlay) leavePanel();
  });

  // ---------------------------------------------------------- routing

  var lastPage = "";

  function route() {
    var h = location.hash || "#/";
    var parts = h.replace(/^#\/?/, "").split("/");
    var head = parts[0];
    var rest;
    try { rest = decodeURIComponent(parts.slice(1).join("/")); }
    catch (e) { closePanel(); notFound(); return; }
    closeSearch();
    if (head === "fact") { factPanel(rest); return; }
    closePanel();
    lastPage = h;
    if (head === "") pageHome();
    else if (head === "chronology") pageChronology();
    else if (head === "work") pageWork();
    else if (head === "units") pageUnits();
    else if (head === "rules") pageRules();
    else if (head === "guides") pageGuides();
    else if (head === "documents") pageDocuments();
    else if (head === "doc") pageDoc(rest);
    else if (head === "map") pageMap(parts.length > 1 && rest ? rest : undefined);
    else if (head === "topic") topicPage(rest);
    else if (head === "sources") pageSources();
    else if (head === "source") pageSource(rest);
    else notFound();
  }

  if (!C || !C.meta || !C.home) { fail(); return; }
  frame();
  window.addEventListener("hashchange", route);
  route();
})();
