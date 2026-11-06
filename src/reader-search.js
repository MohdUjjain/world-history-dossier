/* World History Dossier — full-book, offline passage search.
 * The immutable #chapterData supplies the complete corpus (even when screen
 * revision sections are hidden). Stable data keys survive engine screen clones;
 * this module never edits the print compositor or authored chapter files.
 */
(function (root, factory) {
  'use strict';
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) {
    root.WHDReaderSearch = api;
    if (root.document) api.mount(root.document);
  }
})(typeof window === 'object' ? window : null, function () {
  'use strict';
  function squish(value) { return String(value || '').replace(/\s+/g, ' ').trim(); }
  function normalize(value) {
    return squish(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
  }
  function match(text, query) {
    var terms = normalize(query).split(' ').filter(Boolean);
    var target = normalize(text);
    return !!terms.length && terms.every(function (term) { return target.includes(term); });
  }
  // UTF-16 offsets into original display text, even for accents and ligatures.
  function mappedText(value) {
    var source = String(value || ''), folded = '', starts = [], ends = [];
    for (var i = 0; i < source.length;) {
      var glyph = String.fromCodePoint(source.codePointAt(i));
      var part = glyph.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
      var from = i; i += glyph.length;
      if (!part) {
        if (ends.length) ends[ends.length - 1] = i;
        continue;
      }
      for (var k = 0; k < part.length; k++) {
        if (/\s/.test(part[k])) {
          if (!folded || folded.endsWith(' ')) continue;
          folded += ' ';
        } else folded += part[k];
        starts.push(from); ends.push(i);
      }
    }
    if (folded.endsWith(' ')) { folded = folded.slice(0, -1); starts.pop(); ends.pop(); }
    return {source: source, folded: folded, starts: starts, ends: ends};
  }
  function locate(text, query) {
    var folded = normalize(text), phrase = normalize(query);
    var terms = phrase.split(' ').filter(Boolean);
    if (!terms.length || !terms.every(function (term) { return folded.includes(term); })) return null;
    var exact = folded.indexOf(phrase), first = exact >= 0 ? exact : folded.indexOf(terms[0]);
    return {exact: exact >= 0, start: first, terms: terms};
  }
  function snippetParts(text, query, limit) {
    var source = squish(text), map = mappedText(source), where = locate(source, query);
    var width = limit || 195;
    if (!where) return {parts: [{text: source.slice(0, width), hit: false}],
      prefix: false, suffix: source.length > width};
    var terms = where.exact ? [normalize(query)] : where.terms;
    var ranges = [];
    terms.forEach(function (term) {
      var pos = 0, found = 0, at;
      while (found < 80 && (at = map.folded.indexOf(term, pos)) !== -1) {
        ranges.push([map.starts[at], map.ends[at + term.length - 1]]);
        pos = at + Math.max(1, term.length); found++;
      }
    });
    ranges.sort(function (a, b) { return a[0] - b[0] || b[1] - a[1]; });
    var merged = [];
    ranges.forEach(function (range) {
      var previous = merged[merged.length - 1];
      if (previous && range[0] <= previous[1]) previous[1] = Math.max(previous[1], range[1]);
      else merged.push(range.slice());
    });
    var focal = map.starts[where.start] || 0;
    var start = Math.max(0, focal - Math.floor(width / 3));
    var end = Math.min(source.length, start + width);
    if (end - start < width) start = Math.max(0, end - width);
    var parts = [], cursor = start;
    merged.forEach(function (range) {
      var a = Math.max(start, range[0]), b = Math.min(end, range[1]);
      if (b <= a || a < cursor) return;
      if (a > cursor) parts.push({text: source.slice(cursor, a), hit: false});
      parts.push({text: source.slice(a, b), hit: true});
      cursor = b;
    });
    if (cursor < end) parts.push({text: source.slice(cursor, end), hit: false});
    return {parts: parts, prefix: start > 0, suffix: end < source.length};
  }
  function hashText(text) {
    var value = 2166136261;
    for (var i = 0; i < text.length; i++) {
      value ^= text.charCodeAt(i);
      value = Math.imul(value, 16777619) >>> 0;
    }
    return value.toString(36);
  }
  function buildIndex(doc) {
    var corpus = [], fragments = new Set();
    var semantic = 'h1,h2,h3,h4,h5,h6,p,li,td,th,caption,dt,dd,blockquote,pre,figcaption';
    var skipped = 'script,style,noscript,template,[hidden],[aria-hidden="true"]';
    var serial = 0;
    function register(node, chapter, section, isRevision, kind, targetSelector, displayOverride) {
      var text = squish(displayOverride == null ? (node && node.textContent) : displayOverride);
      if (text.length < 2) return;
      var index = corpus.length;
      var key = node && !targetSelector ? 'whd-search-' + chapter.num + '-' + (++serial) : null;
      if (key) node.setAttribute('data-whd-search-key', key);
      var base = 'whd-hit-' + chapter.num + '-' + hashText(section + '\n' + text.slice(0, 320));
      var fragment = base, suffix = 1;
      while (fragments.has(fragment)) fragment = base + '-' + (++suffix);
      fragments.add(fragment);
      corpus.push({index: index, chapter: chapter.num, title: chapter.title,
        section: section, revision: isRevision, kind: kind, text: text,
        normalized: normalize(text), key: key, selector: targetSelector || null,
        fragment: fragment, node: node});
    }
    Array.from(doc.querySelectorAll('#chapterData > .chapter-source')).forEach(function (source) {
      var chapter = {num: source.getAttribute('data-chapter'),
        title: source.getAttribute('data-title') || 'Untitled chapter'};
      var hero = source.querySelector('.src-hero');
      register(null, chapter, 'Chapter overview', false, 'chapter', '.banner h1',
        'Chapter ' + chapter.num + ' · ' + chapter.title);
      if (hero) [
        ['.hk', '.banner .kicker', 'Chapter overview'],
        ['.hs', '.banner .subtitle', 'Chapter overview'],
        ['.hb', '.banner .byline', 'Chapter overview'],
        ['.hthesis', '.banner .thesis', 'Central thesis'],
        ['.hyears', '.banner .yrs', 'Timeline']
      ].forEach(function (parts) {
        var unit = hero.querySelector(parts[0]);
        if (unit) register(null, chapter, parts[2], false, 'hero', parts[1], unit.textContent);
      });
      var sectionNames = new Map([['intro', 'Opening overview']]);
      Array.from(source.querySelectorAll('.src-main > .block[data-kind="section-head"]'))
        .forEach(function (block) {
          sectionNames.set(block.getAttribute('data-section-key') || '',
            block.getAttribute('data-title') || squish(block.textContent));
        });
      ['.src-main', '.src-side'].forEach(function (selector) {
        var inMain = selector === '.src-main';
        var stream = source.querySelector(selector);
        if (!stream) return;
        var sectionKey = 'intro', revision = false;
        Array.from(stream.children).forEach(function (block) {
          // The hidden boundary is the first revision marker OR its section
          // identity. Follow it through the rest of each authored stream,
          // including cards without an explicit data-revision-start flag.
          if (block.getAttribute('data-revision-start') === 'true' ||
              block.getAttribute('data-section-key') === 'revision' ||
              block.getAttribute('data-for-section') === 'revision') revision = true;
          if (inMain && block.getAttribute('data-kind') === 'section-head')
            sectionKey = block.getAttribute('data-section-key') || sectionKey;
          var key = inMain ? sectionKey : (block.getAttribute('data-for-section') || 'intro');
          var section = sectionNames.get(key) || (revision ? 'Revision and recall' : 'Study aids');
          var insideRevision = revision || key === 'revision';
          var grouped = new Map();
          var walker = doc.createTreeWalker(block, NodeFilter.SHOW_TEXT);
          var leaf;
          while ((leaf = walker.nextNode())) {
            if (!leaf.nodeValue || !leaf.nodeValue.trim() || !leaf.parentElement) continue;
            var parent = leaf.parentElement;
            if (parent.closest(skipped)) continue;
            var unit = parent.closest(semantic) || parent.closest('div,span,small,cite,strong,em,b') || block;
            if (!block.contains(unit)) unit = block;
            var value = grouped.get(unit) || '';
            grouped.set(unit, value + leaf.nodeValue);
          }
          grouped.forEach(function (text, unit) {
            var tag = unit.localName;
            var heading = /^h[1-6]$/.test(tag) || block.getAttribute('data-kind') === 'section-head' && tag === 'h2';
            register(unit, chapter, section, insideRevision,
              heading ? 'heading' : 'passage', null, text);
          });
          // A diagram with independent inline captions also deserves a joined
          // searchable phrase, without duplicating whole paragraphs or tables.
          var isVisual = !block.querySelector(semantic) &&
            /^(flow|quote|memory|concept|def|tip|hy|mistake)$/.test(block.getAttribute('data-kind') || '');
          if (isVisual && squish(block.textContent).length <= 520 && grouped.size > 1)
            register(block, chapter, section, insideRevision, 'visual');
        });
      });
    });
    return corpus;
  }
  function find(index, query, options) {
    var phrase = normalize(query), found = [];
    if (!phrase) return found;
    var includeRevision = !options || options.includeRevision !== false;
    index.forEach(function (entry) {
      // The source index is immutable, but visible search scope follows
      // Contents → Tools → Include chapter summaries on every query.
      if (!includeRevision && entry.revision) return;
      var where = locate(entry.normalized, phrase);
      if (!where) return;
      var score = (where.exact ? 140 : 0) +
        (entry.kind === 'chapter' ? 170 : entry.kind === 'heading' ? 85 : 0) +
        (where.start === 0 ? 14 : 0) +
        Math.max(0, 40 - Math.floor(entry.text.length / 16));
      found.push({entry: entry, score: score});
    });
    // A matching phrase in a child label should not reappear as a second hit
    // from its enclosing diagram wrapper; retain cross-label wrapper matches.
    found = found.filter(function (hit) {
      return hit.entry.kind !== 'visual' || !found.some(function (other) {
        return other.entry !== hit.entry && other.entry.chapter === hit.entry.chapter &&
          other.entry.node && hit.entry.node && hit.entry.node.contains(other.entry.node) &&
          other.entry.normalized.includes(phrase);
      });
    });
    found.sort(function (a, b) { return b.score - a.score || a.entry.index - b.entry.index; });
    return found;
  }
  function mount(doc) {
    var input = doc.getElementById('readerSearchInput');
    var popup = doc.getElementById('readerSearchResults');
    var hits = doc.getElementById('readerSearchHits');
    var status = doc.getElementById('readerSearchStatus');
    var clear = doc.getElementById('readerSearchClear');
    var close = doc.getElementById('readerSearchClose');
    var more = doc.getElementById('readerSearchMore');
    var box = doc.getElementById('readerSearchBox');
    var feedback = doc.getElementById('readerSearchFeedback');
    if (!input || !popup || !hits || !status || !clear || !close || !more || !box) return;
    var corpus = null, found = [], shown = 0, timer = null, generation = 0;
    var currentQuery = '', highlighted = null, highlightTimer = null;
    var suppressFocus = false, screenRenderedOnce = false, suppressFragment = false;
    var PAGE_SIZE = 30;
    function ensure() { if (!corpus) corpus = buildIndex(doc); return corpus; }
    function show() { popup.hidden = false; input.setAttribute('aria-expanded', 'true'); }
    function focusInput() {
      suppressFocus = true; input.focus({preventScroll: true}); suppressFocus = false;
    }
    function hide() { popup.hidden = true; input.setAttribute('aria-expanded', 'false'); }
    function invalidate() {
      generation++;
      if (timer !== null) clearTimeout(timer);
      timer = null;
    }
    function clearHighlight() {
      if (highlightTimer) clearTimeout(highlightTimer);
      highlightTimer = null;
      if (window.CSS && CSS.highlights) CSS.highlights.delete('whd-reader-search');
      if (highlighted && highlighted.isConnected) highlighted.classList.remove('reader-search-target');
      highlighted = null;
    }
    function targetFor(entry) {
      var chapter = doc.getElementById('chapter-' + entry.chapter);
      if (!chapter) return null;
      if (entry.selector) return chapter.querySelector(entry.selector);
      return chapter.querySelector('[data-whd-search-key="' + entry.key + '"]');
    }
    function revisionAllowed(entry) {
      var checkbox = doc.getElementById('includeRevisionChk');
      return !entry.revision || !checkbox || checkbox.checked;
    }
    function navigate(entry, fromHash) {
      if (!revisionAllowed(entry) && !fromHash) {
        render(); return; // stale search result cannot change Tools preference
      }
      hide();
      invalidate();
      // Old passage URLs remain safe: when revision is hidden, land on its
      // chapter instead of silently enabling summaries or changing settings.
      var target = revisionAllowed(entry) ? targetFor(entry) :
        doc.getElementById('chapter-' + entry.chapter);
      if (!target) return;
      clearHighlight();
      var anchor = target.id || entry.fragment;
      if (!target.id) target.id = anchor;
      if (!fromHash && window.history && window.history.pushState &&
          window.location.hash !== '#' + encodeURIComponent(anchor))
        window.history.pushState({historySearch: true}, '', '#' + encodeURIComponent(anchor));
      highlighted = target;
      target.classList.add('reader-search-target');
      if (window.CSS && CSS.highlights && typeof Highlight === 'function') {
        var ranges = [], walker = doc.createTreeWalker(target, NodeFilter.SHOW_TEXT), leaf;
        var words = normalize(input.value).split(' ').filter(Boolean);
        while ((leaf = walker.nextNode()) && ranges.length < 80) {
          var map = mappedText(leaf.nodeValue);
          words.forEach(function (word) {
            var pos = 0, at;
            while (ranges.length < 80 && (at = map.folded.indexOf(word, pos)) !== -1) {
              var range = doc.createRange();
              range.setStart(leaf, map.starts[at]);
              range.setEnd(leaf, map.ends[at + word.length - 1]);
              ranges.push(range);
              pos = at + Math.max(1, word.length);
            }
          });
        }
        if (ranges.length) CSS.highlights.set('whd-reader-search', new Highlight(...ranges));
      }
      var original = target.getAttribute('tabindex');
      if (original === null) target.setAttribute('tabindex', '-1');
      requestAnimationFrame(function () {
        // A search result should land deterministically, even if a previous
        // smooth animation or a chapter-visibility rebuild is in flight.
        target.scrollIntoView({block: 'center', behavior: 'instant'});
        target.focus({preventScroll: true});
        highlightTimer = setTimeout(function () {
          if (highlighted === target) clearHighlight();
          if (original === null && target.getAttribute('tabindex') === '-1') target.removeAttribute('tabindex');
        }, 4500);
      });
    }
    function maybeFollowHash() {
      if (suppressFragment) return;
      var id;
      try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (_) { return; }
      if (!id || !id.startsWith('whd-hit-')) return;
      var entry = ensure().find(function (candidate) { return candidate.fragment === id; });
      if (entry) navigate(entry, true);
    }
    function resultButton(hit) {
      var entry = hit.entry;
      var button = doc.createElement('button');
      button.type = 'button'; button.className = 'reader-search-hit';
      var context = doc.createElement('strong'); context.className = 'reader-search-context';
      context.textContent = 'Ch.' + String(entry.chapter).padStart(2, '0') + ' — ' + entry.title;
      var section = doc.createElement('span'); section.className = 'reader-search-section';
      section.textContent = entry.section + (entry.revision ? ' · Revision' : '');
      var snippet = doc.createElement('span'); snippet.className = 'reader-search-snippet';
      var excerpt = snippetParts(entry.text, input.value, 192);
      if (excerpt.prefix) snippet.append(doc.createTextNode('…'));
      excerpt.parts.forEach(function (part) {
        if (part.hit) {
          var mark = doc.createElement('mark'); mark.textContent = part.text; snippet.appendChild(mark);
        } else snippet.append(doc.createTextNode(part.text));
      });
      if (excerpt.suffix) snippet.append(doc.createTextNode('…'));
      button.append(context, section, snippet);
      button.addEventListener('click', function () {
        if (currentQuery !== input.value.trim()) { render(); return; }
        navigate(entry, false);
      });
      return button;
    }
    function appendPage() {
      var end = Math.min(found.length, shown + PAGE_SIZE);
      for (var i = shown; i < end; i++) hits.appendChild(resultButton(found[i]));
      shown = end;
      more.hidden = shown >= found.length;
      if (!more.hidden) more.textContent = 'Show more · ' + shown + ' of ' + found.length;
      status.textContent = found.length ?
        'Showing ' + shown + ' of ' + found.length + ' matching passages.' :
        'No matches found. Try a different word or phrase.';
    }
    function render() {
      invalidate();
      currentQuery = input.value.trim();
      hits.replaceChildren();
      shown = 0; found = []; more.hidden = true;
      clear.hidden = !currentQuery;
      if (!currentQuery || doc.body.classList.contains('drawer-open')) { hide(); return; }
      found = find(ensure(), currentQuery, {
        includeRevision: revisionAllowed({revision:true})
      });
      appendPage(); show();
    }
    input.addEventListener('input', function () {
      invalidate();
      hide();
      clear.hidden = !input.value.trim();
      var ticket = generation;
      timer = setTimeout(function () { if (ticket === generation) render(); }, 120);
    });
    input.addEventListener('focus', function () {
      if (!suppressFocus && input.value.trim() && popup.hidden) render();
    });
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        if (!popup.hidden) hide();
        else if (input.value) { input.value = ''; render(); }
        event.preventDefault(); return;
      }
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        if (popup.hidden) render();
        var options = hits.querySelectorAll('.reader-search-hit');
        if (options.length) {
          event.preventDefault();
          options[event.key === 'ArrowDown' ? 0 : options.length - 1].focus();
        }
      } else if (event.key === 'Enter') {
        if (popup.hidden) render();
        var first = hits.querySelector('.reader-search-hit');
        if (first) { event.preventDefault(); first.click(); }
      }
    });
    hits.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { event.preventDefault(); hide(); focusInput(); return; }
      if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return;
      var buttons = Array.from(hits.querySelectorAll('.reader-search-hit'));
      var index = buttons.indexOf(doc.activeElement);
      if (index < 0) return;
      event.preventDefault();
      var next = index + (event.key === 'ArrowDown' ? 1 : -1);
      if (next < 0) input.focus();
      else if (next < buttons.length) buttons[next].focus();
      else if (!more.hidden) more.focus();
    });
    more.addEventListener('click', function () {
      var start = shown; appendPage();
      var next = hits.querySelectorAll('.reader-search-hit')[start];
      if (next) next.focus();
    });
    close.addEventListener('click', function () { hide(); focusInput(); });
    clear.addEventListener('click', function () {
      input.value = ''; render(); input.focus();
    });
    doc.addEventListener('pointerdown', function (event) {
      if (!popup.hidden && !box.contains(event.target)) hide();
    });
    doc.addEventListener('keydown', function (event) {
      var active = doc.activeElement;
      if (event.key !== '/' || event.ctrlKey || event.altKey || event.metaKey ||
          doc.body.classList.contains('drawer-open') ||
          ['INPUT', 'TEXTAREA', 'SELECT'].includes(active && active.tagName) ||
          (active && active.isContentEditable)) return;
      event.preventDefault(); input.focus(); input.select();
    });
    doc.getElementById('navTab')?.addEventListener('click', hide, true);
    doc.addEventListener('whd:screen-will-render', function () {
      // Engine reads these attributes while cloning the immutable sources.
      ensure();
      clearHighlight();
    });
    doc.addEventListener('whd:screen-rendered', function () {
      if (!screenRenderedOnce) { screenRenderedOnce = true; maybeFollowHash(); }
      else if (!popup.hidden && input.value.trim()) render();
    });
    window.addEventListener('hashchange', maybeFollowHash);
    window.addEventListener('popstate', maybeFollowHash);
    // On initial load the engine fires will-render, then screen-rendered;
    // no MutationObserver or global service is required.
    return {getStats: function () { return {entries: ensure().length, matches: found.length}; }};
  }
  return Object.freeze({squish: squish, normalize: normalize, match: match,
    mappedText: mappedText, locate: locate, snippetParts: snippetParts,
    buildIndex: buildIndex, find: find, mount: mount});
});
