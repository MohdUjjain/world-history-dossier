/* World History Dossier — screen-only contents, accessibility and reading position.
 * Pagination and chapter content remain owned by src/engine.js.
 * This file is inlined by src/build.py; it is safe inside the offline PWA.
 */
(function () {
  'use strict';
  var toc = document.getElementById('navToc');
  var panel = document.getElementById('navPanel');
  var trigger = document.getElementById('navTab');
  var overlay = document.getElementById('navOverlay');
  var closeButton = document.getElementById('navClose');
  var indexTab = document.getElementById('navIndexTab');
  var toolsTab = document.getElementById('navToolsTab');
  var indexPanel = document.getElementById('navIndexPanel');
  var toolsPanel = document.getElementById('navToolsPanel');
  var toolsResumeSection = document.getElementById('navToolsResumeSection');
  var toolsResumeContext = document.getElementById('navToolsResumeContext');
  var toolsResumeButton = document.getElementById('navToolsResume');
  var expandButton = document.getElementById('tocExpandAll');
  var collapseButton = document.getElementById('tocCollapseAll');
  var ring = document.getElementById('chapterProgressRing');
  var ringText = document.getElementById('chapterProgressNumber');
  var currentLabel = document.getElementById('currentChapterLabel');
  var prompt = document.getElementById('resumeReaderPrompt');
  var description = document.getElementById('resumeReaderDescription');
  var resumeButton = document.getElementById('resumeReaderContinue');
  var startButton = document.getElementById('resumeReaderStart');
  var forgetButton = document.getElementById('resumeReaderForget');
  var dismissButton = document.getElementById('resumeReaderDismiss');
  var KEY = 'whd-reading-place-v1';
  var chapterRows = [], lastFocused = null, manualExpanded = new Set();
  var backgroundInertSnapshot = [];
  var editionNoticeVisible = false, resumeDismissed = false;
  var lastActiveChapter = null, lastActiveSection = null;
  var rebuilding = false, framePending = false, printing = false;
  var pendingView = null;
  var savedPosition = null, permitSaving = true, lastSaveAt = 0, lastReading = null;
  var userMoved = false, saveAfter = 0, deferredSaveTimer = null;

  function safeStorage(action, value) {
    try {
      if (action === 'get') return JSON.parse(localStorage.getItem(KEY) || 'null');
      if (action === 'remove') localStorage.removeItem(KEY);
      if (action === 'put') localStorage.setItem(KEY, JSON.stringify(value));
    } catch (_) { return null; }
  }
  function chapterNum(chapter) {
    return chapter.id.replace(/^chapter-/, '');
  }
  function titleOf(chapter) {
    return chapter.querySelector('.banner h1')?.textContent.trim() || 'Chapter ' + chapterNum(chapter);
  }
  function targetFor(id) {
    return document.getElementById(id);
  }
  function updateHash(id) {
    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, '', '#' + encodeURIComponent(id));
    }
  }
  function goTo(id, keepHash) {
    var el = targetFor(id);
    if (!el) return;
    hideResume();
    permitSaving = true;
    saveAfter = Date.now() + 1400;
    closeDrawer(false);
    if (keepHash !== false) updateHash(id);
    el.setAttribute('tabindex', '-1');
    try { el.focus({preventScroll:true}); } catch (_) { el.focus(); }
    el.scrollIntoView({
      behavior: window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
      block: 'start'
    });
    requestReadingUpdate();
  }

  // One keyboard tab stop, with inert inactive panes.
  // Opening the Contents launcher always starts in Index.
  function switchNavView(which, focus) {
    var index = which !== 'tools';
    indexTab.setAttribute('aria-selected', String(index));
    toolsTab.setAttribute('aria-selected', String(!index));
    indexTab.tabIndex = index ? 0 : -1;
    toolsTab.tabIndex = index ? -1 : 0;
    indexPanel.hidden = !index; indexPanel.inert = !index;
    toolsPanel.hidden = index; toolsPanel.inert = index;
    if (focus) (index ? indexTab : toolsTab).focus();
  }
  function handleNavTabKeys(event) {
    if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();
    var next = event.key === 'Home' ? 'index' :
      event.key === 'End' ? 'tools' :
      event.currentTarget === indexTab ? 'tools' : 'index';
    switchNavView(next, true);
  }
  function syncToolsResume() {
    if (!toolsResumeSection) return;
    var chapter = savedPosition &&
      document.getElementById('chapter-' + savedPosition.chapter);
    toolsResumeSection.hidden = !chapter;
    if (chapter) toolsResumeContext.textContent = 'Chapter ' +
      String(savedPosition.chapter).padStart(2, '0') + ' — ' + titleOf(chapter);
  }
  function focusables() {
    return Array.from(panel.querySelectorAll('a[href],button:not([disabled]):not([tabindex="-1"]),input:not([disabled]),summary,[tabindex]:not([tabindex="-1"])'))
      .filter(function(el){return !el.hidden && !el.closest('[hidden],[inert]') && el.getClientRects().length > 0;});
  }
  // A focus trap alone is insufficient for screen-reader modal isolation.
  // Preserve every sibling's prior inert state, including the update notice.
  function isolateBackground(isOpen) {
    if (isOpen) {
      backgroundInertSnapshot = Array.from(document.body.children)
        .filter(function(el){ return el !== panel && el !== overlay; })
        .map(function(el){return {element:el,wasInert:el.inert};});
      backgroundInertSnapshot.forEach(function(state){state.element.inert=true;});
    } else {
      backgroundInertSnapshot.forEach(function(state){
        if (state.element.isConnected) state.element.inert=state.wasInert;
      });
      backgroundInertSnapshot=[];
    }
  }
  function openDrawer() {
    if (panel.classList.contains('open')) return;
    lastFocused = document.activeElement;
    switchNavView('index', false);
    panel.inert = false;
    panel.setAttribute('aria-hidden', 'false');
    panel.classList.add('open');
    overlay.classList.add('open');
    trigger.setAttribute('aria-expanded', 'true');
    document.body.classList.add('drawer-open');
    isolateBackground(true);
    closeButton.focus();
  }
  function closeDrawer(restore) {
    if (!panel.classList.contains('open')) return;
    panel.classList.remove('open');
    overlay.classList.remove('open');
    document.body.classList.remove('drawer-open');
    panel.inert = true;
    panel.setAttribute('aria-hidden', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    isolateBackground(false);
    if (restore !== false && lastFocused && lastFocused.isConnected &&
        typeof lastFocused.focus === 'function') lastFocused.focus();
    lastFocused = null;
  }
  function handleKeys(event) {
    if (!panel.classList.contains('open')) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      closeDrawer(true);
      return;
    }
    if (event.key !== 'Tab') return;
    var nodes = focusables();
    if (!nodes.length) { event.preventDefault(); panel.focus(); return; }
    var first = nodes[0], last = nodes[nodes.length-1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement === panel)) {
      event.preventDefault(); last.focus();
    } else if (!event.shiftKey && (document.activeElement === last || document.activeElement === panel)) {
      event.preventDefault(); first.focus();
    } else if (!panel.contains(document.activeElement)) {
      event.preventDefault(); first.focus();
    }
  }
  function updateExpanded(entry) {
    var expanded = manualExpanded.has(entry.num);
    entry.wrap.classList.toggle('expanded', expanded);
    entry.toggle.setAttribute('aria-expanded', String(expanded));
    entry.toggle.setAttribute('aria-label',
      (expanded ? 'Hide' : 'Show') + ' sections and study shortcuts for chapter ' + entry.num);
    entry.sections.hidden = !expanded;
    entry.shortcuts.hidden = !expanded || !entry.shortcuts.childElementCount;
  }
  function syncExpandedState() {
    chapterRows.forEach(updateExpanded);
  }
  function addLink(host, label, id, cls) {
    var a = document.createElement('a');
    a.href = '#' + id;
    a.dataset.target = id;
    a.className = cls;
    a.textContent = label;
    host.appendChild(a);
    return a;
  }
  function firstAid(chapter, selector, type, num) {
    var target = chapter.querySelector(selector);
    if (!target) return null;
    var id = 'aid-' + num + '-' + type;
    target.id = id;
    return id;
  }
  function buildChapterRows() {
    if (rebuilding) return;
    rebuilding = true;
    var chapters = Array.from(document.querySelectorAll('#screenView > .chapter-flow'));
    toc.replaceChildren();
    chapterRows = [];
    chapters.forEach(function(chapter) {
      var num = chapterNum(chapter), title = titleOf(chapter);
      var wrap = document.createElement('section');
      wrap.className = 'nav-chapter';
      wrap.dataset.chapter = num;
      var top = document.createElement('div');
      top.className = 'nav-chapter-row';
      var dot = document.createElement('span');
      dot.className = 'dot';
      dot.style.background = getComputedStyle(chapter).getPropertyValue('--chapter-color');
      dot.setAttribute('aria-hidden', 'true');
      var link = addLink(top, 'Ch.' + String(num).padStart(2,'0') + ' — ' + title, chapter.id, 'nav-chapter-link');
      var toggle = document.createElement('button');
      toggle.className = 'nav-chapter-toggle';
      toggle.type = 'button';
      toggle.textContent = '▸';
      toggle.setAttribute('aria-controls', 'nav-sections-' + num);
      toggle.addEventListener('click', function(){
        if (manualExpanded.has(num)) manualExpanded.delete(num);
        else manualExpanded.add(num);
        syncExpandedState();
      });
      top.prepend(dot);
      top.appendChild(toggle);
      wrap.appendChild(top);
      var list = document.createElement('div');
      list.className = 'nav-sections';
      list.id = 'nav-sections-' + num;
      chapter.querySelectorAll('[data-kind="section-head"]').forEach(function(heading, i) {
        var key = heading.getAttribute('data-section-key') || 's' + (i+1);
        var id = 'whd-sec-' + num + '-' + key.replace(/[^a-z0-9_-]/gi,'-');
        if (chapter.querySelectorAll('[id="' + id + '"]').length) id += '-' + (i+1);
        heading.id = id;
        addLink(list, heading.getAttribute('data-title') || heading.textContent.trim(), id, 'nav-section-link');
      });
      wrap.appendChild(list);
      var shortcuts = document.createElement('div');
      shortcuts.className = 'nav-shortcuts';
      shortcuts.setAttribute('aria-label', 'Chapter ' + num + ' study shortcuts');
      var revision = chapter.querySelector('.revision-flow [data-kind="section-head"]');
      if (revision) addLink(shortcuts, 'Revision', revision.id, 'nav-shortcut');
      var definitions = firstAid(chapter, '[data-kind="def"]', 'definitions', num);
      if (definitions) addLink(shortcuts, 'Definitions', definitions, 'nav-shortcut');
      var memory = firstAid(chapter, '[data-kind="memory"]', 'memory', num);
      if (memory) addLink(shortcuts, 'Memory aids', memory, 'nav-shortcut');
      // Question lists vary by chapter; never invent a shortcut when none exists.
      var question = Array.from(chapter.querySelectorAll('.revision-flow .block'))
        .find(function(node){ return /revision prompts|review questions|self.test|test yourself|exam question/i.test(node.textContent); });
      if (question) {
        question.id = 'aid-' + num + '-questions';
        addLink(shortcuts, 'Questions', question.id, 'nav-shortcut');
      }
      wrap.appendChild(shortcuts);
      toc.appendChild(wrap);
      chapterRows.push({num:num,title:title,wrap:wrap,link:link,toggle:toggle,sections:list,shortcuts:shortcuts});
    });
    syncExpandedState();
    applyActiveReading();
    rebuilding = false;
    requestReadingUpdate();
  }
  function activeChapterAndSection() {
    var chapters = Array.from(document.querySelectorAll('#screenView > .chapter-flow'));
    var y = window.scrollY + Math.max(70, Math.min(window.innerHeight * .30, 260));
    var chosen = null;
    for (var i=0; i<chapters.length; i++) {
      if (chapters[i].getBoundingClientRect().top + window.scrollY <= y) chosen = chapters[i];
      else break;
    }
    if (!chosen) return null;
    var headings = Array.from(chosen.querySelectorAll('[data-kind="section-head"]'));
    var section = null;
    headings.forEach(function(heading){
      if (heading.getBoundingClientRect().top + window.scrollY <= y) section = heading;
    });
    var rect = chosen.getBoundingClientRect();
    var ratio = Math.min(1, Math.max(0, (y - (rect.top + window.scrollY)) / Math.max(1,rect.height)));
    return {chapter:chosen, section:section, ratio:ratio, num:chapterNum(chosen)};
  }
  function applyActiveReading() {
    chapterRows.forEach(function(e){
      var active = e.num === lastActiveChapter;
      e.wrap.classList.toggle('current-chapter', active);
      e.link.removeAttribute('aria-current');
      if (active && !lastActiveSection) e.link.setAttribute('aria-current', 'location');
      e.sections.querySelectorAll('a').forEach(function(a) {
        var on = a.dataset.target === lastActiveSection;
        a.classList.toggle('current-section', on);
        if (on) a.setAttribute('aria-current','location');
        else a.removeAttribute('aria-current');
      });
    });
  }
  function updateReading() {
    framePending = false;
    if (printing) return;
    var current = activeChapterAndSection();
    lastReading = current;
    lastActiveChapter = current ? current.num : null;
    lastActiveSection = current && current.section ? current.section.id : null;
    applyActiveReading();
    if (current) {
      currentLabel.textContent = 'Ch.'+String(current.num).padStart(2,'0')+' — '+titleOf(current.chapter);
      currentLabel.title = currentLabel.textContent;
      var pct = Math.round(current.ratio * 100);
      ring.hidden = false;
      ring.style.setProperty('--chapter-progress',pct+'%');
      ring.style.setProperty('--chapter-accent',getComputedStyle(current.chapter).getPropertyValue('--chapter-color'));
      ringText.textContent = pct + '%';
      ring.setAttribute('aria-valuenow',String(pct));
      ring.setAttribute('aria-valuetext','Chapter '+current.num+': '+pct+' percent');
    } else {
      currentLabel.textContent = '';
      currentLabel.removeAttribute('title');
      ring.hidden = true;
    }
    if (userMoved && permitSaving && current) {
      // A single wheel/touch scroll may arrive during the short navigation
      // guard period. Schedule the save once that guard expires instead of
      // relying on a second scroll event that may never happen.
      var now = Date.now();
      var nextAllowed = Math.max(saveAfter, lastSaveAt + 1100);
      if (now >= nextAllowed) {
        lastSaveAt = now;
        saveCurrent(current);
      } else if (!deferredSaveTimer) {
        deferredSaveTimer = setTimeout(function(){
          deferredSaveTimer = null;
          requestReadingUpdate();
        }, Math.max(60, nextAllowed - now + 20));
      }
    }
  }
  function requestReadingUpdate() {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(updateReading);
  }
  function saveCurrent(current) {
    var section = current.section;
    var sectionRatio = 0;
    if (section) {
      var y = window.scrollY + Math.max(70,Math.min(window.innerHeight*.30,260));
      var next = Array.from(current.chapter.querySelectorAll('[data-kind="section-head"]'));
      var idx = next.indexOf(section);
      var bottom = idx >= 0 && idx+1 < next.length ?
        next[idx+1].getBoundingClientRect().top + window.scrollY :
        current.chapter.getBoundingClientRect().bottom + window.scrollY;
      var start = section.getBoundingClientRect().top + window.scrollY;
      sectionRatio = Math.max(0,Math.min(1,(y-start)/Math.max(1,bottom-start)));
    }
    var checkpoint = {
      chapter:current.num, section:section?.id || null,
      chapterRatio:Math.max(0,Math.min(1,current.ratio)),
      sectionRatio:sectionRatio, savedAt:Date.now()
    };
    safeStorage('put',checkpoint);
    savedPosition = checkpoint;
    syncToolsResume();
  }
  // Preserve a viewport-relative *reading block*, not an absolute scroll
  // pixel, across whole-reader reconstruction when revision is toggled.
  // The chapter's main block order is stable when revision cards are removed.
  function contentTargets(chapter) {
    var banner = chapter.querySelector('.banner');
    var blocks = Array.from(chapter.querySelectorAll('.main-flow > .block'));
    return banner ? [banner].concat(blocks) : blocks;
  }
  function captureView() {
    // Initial load has no prior reading tree. Do not force a scrollTo(0,0)
    // that could override the browser's native history scroll restoration.
    if (!document.querySelector('#screenView > .chapter-flow')) return null;
    var current = activeChapterAndSection();
    if (!current) return {chapter:null,scrollY:window.scrollY};
    var header = document.querySelector('.site-header').getBoundingClientRect().height;
    var anchorY = Math.max(header + 28, Math.min(window.innerHeight * .30, 260));
    var targets = contentTargets(current.chapter), index = 0;
    targets.forEach(function(node,i){
      if (node.getBoundingClientRect().top <= anchorY) index = i;
    });
    var rect = targets[index] && targets[index].getBoundingClientRect();
    return {
      chapter:current.num, scrollY:window.scrollY, anchorY:anchorY,
      blockIndex:index,
      fraction:rect ? Math.min(1,Math.max(0,
        (anchorY-rect.top)/Math.max(1,rect.height))) : 0
    };
  }
  function restoreView(view) {
    if (!view) return;
    var top=view.scrollY;
    var chapter=view.chapter && document.getElementById('chapter-'+view.chapter);
    if (chapter) {
      var targets=contentTargets(chapter);
      if (targets.length) {
        var idx=Math.min(view.blockIndex,targets.length-1);
        var node=targets[idx],rect=node.getBoundingClientRect();
        top=rect.top+window.scrollY+
          rect.height * (idx===view.blockIndex ? view.fraction : 1)-view.anchorY;
      }
    }
    window.scrollTo({top:Math.max(0,top),behavior:'instant'});
    // Guard the local reading bookmark from the restoration's synthetic scroll.
    saveAfter=Date.now()+1100;
    requestReadingUpdate();
  }
  function hideResume() {
    if (prompt) prompt.hidden = true;
  }
  function forgetSaved() {
    resumeDismissed=true;
    safeStorage('remove');
    savedPosition = null;
    permitSaving = true;
    hideResume();
    syncToolsResume();
  }
  function resumeReading() {
    if (!savedPosition) return;
    resumeDismissed=true;
    var chapter = document.getElementById('chapter-' + savedPosition.chapter);
    if (!chapter) return forgetSaved();
    var section = savedPosition.section && document.getElementById(savedPosition.section);
    var top;
    if (section && chapter.contains(section)) {
      var heads = Array.from(chapter.querySelectorAll('[data-kind="section-head"]'));
      var idx = heads.indexOf(section);
      var next = idx >= 0 && idx+1 < heads.length ? heads[idx+1] : null;
      var begin = section.getBoundingClientRect().top + window.scrollY;
      var end = next ? next.getBoundingClientRect().top + window.scrollY :
        chapter.getBoundingClientRect().bottom + window.scrollY;
      top = begin + (end-begin)*Math.max(0,Math.min(1,savedPosition.sectionRatio||0));
    } else {
      var r = chapter.getBoundingClientRect();
      top = r.top + window.scrollY + r.height * Math.max(0,Math.min(1,savedPosition.chapterRatio||0));
    }
    hideResume();
    permitSaving = true;
    userMoved = true;
    saveAfter = Date.now() + 1600;
    window.scrollTo({top:Math.max(0,top-window.innerHeight*.25),behavior:'auto'});
    requestReadingUpdate();
  }
  function offerResumeIfEligible() {
    if (!savedPosition || resumeDismissed || editionNoticeVisible ||
        location.hash || window.scrollY > 120 || userMoved) return;
    var chapter=document.getElementById('chapter-' + savedPosition.chapter);
    if (!chapter) { forgetSaved(); return; }
    description.textContent='Your saved place: Chapter '+
      String(savedPosition.chapter).padStart(2,'0')+' — '+titleOf(chapter)+'.';
    prompt.hidden=false;
  }
  document.addEventListener('whd:edition-notice',function(event){
    editionNoticeVisible=Boolean(event.detail && event.detail.visible);
    if (editionNoticeVisible) {
      hideResume();
    } else {
      offerResumeIfEligible();
    }
  });
  function initializeResume() {
    savedPosition = safeStorage('get');
    syncToolsResume();
    if (!savedPosition || typeof savedPosition.chapter !== 'string') {
      permitSaving = true; return;
    }
    permitSaving = false;
    // Direct chapter links and browser-restored scroll positions have priority.
    setTimeout(function() {
      if (location.hash || window.scrollY > 120 || userMoved) {
        permitSaving=true; return;
      }
      offerResumeIfEligible();
    }, 250);
  }

  if (resumeButton) resumeButton.addEventListener('click',resumeReading);
  if (toolsResumeButton) toolsResumeButton.addEventListener('click',function(){
    closeDrawer(false);
    resumeReading();
  });
  [indexTab,toolsTab].forEach(function(tab){
    tab.addEventListener('click',function(){
      switchNavView(tab === indexTab ? 'index' : 'tools',false);
    });
    tab.addEventListener('keydown',handleNavTabKeys);
  });
  switchNavView('index',false);
  if (startButton) startButton.addEventListener('click',function(){
    forgetSaved(); userMoved = false; window.scrollTo({top:0,behavior:'auto'});
  });
  if (forgetButton) forgetButton.addEventListener('click',forgetSaved);
  if (dismissButton) dismissButton.addEventListener('click',function(){
    resumeDismissed=true;
    hideResume(); permitSaving = true;
  });
  trigger.addEventListener('click', function(event){
    event.stopImmediatePropagation();
    openDrawer();
  }, true);
  closeButton.addEventListener('click', function(event){
    event.stopImmediatePropagation();
    closeDrawer(true);
  }, true);
  overlay.addEventListener('click', function(event){
    event.stopImmediatePropagation();
    closeDrawer(true);
  }, true);
  document.addEventListener('keydown',handleKeys);
  toc.addEventListener('click',function(event){
    var link = event.target.closest('a[data-target]');
    if (!link) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    goTo(link.dataset.target,true);
  }, true);
  expandButton.addEventListener('click',function(){
    chapterRows.forEach(function(row){manualExpanded.add(row.num);});
    syncExpandedState();
  });
  collapseButton.addEventListener('click',function(){
    manualExpanded.clear();
    syncExpandedState();
  });
  document.addEventListener('whd:drawer-close',function(event) {
    closeDrawer(!event.detail || event.detail.restoreFocus !== false);
  });
  document.addEventListener('whd:screen-will-render',function() {
    pendingView = captureView();
  });
  document.addEventListener('whd:screen-rendered',function() {
    var view = pendingView;
    pendingView = null;
    buildChapterRows();
    restoreView(view);
  });
  window.addEventListener('scroll',requestReadingUpdate,{passive:true});
  window.addEventListener('resize',requestReadingUpdate);
  ['wheel','touchmove','keydown'].forEach(function(type) {
    window.addEventListener(type,function(e){
      if (type==='keydown' && !['ArrowDown','ArrowUp','PageDown','PageUp',' ','Home','End'].includes(e.key)) return;
      userMoved = true;
    },{passive:true});
  });
  window.addEventListener('beforeprint',function(){printing=true;});
  window.addEventListener('afterprint',function(){printing=false;requestReadingUpdate();});
  window.addEventListener('pagehide',function(){
    if (permitSaving && userMoved && lastReading && !printing) saveCurrent(lastReading);
  });
  panel.inert = true; panel.setAttribute('aria-hidden','true');

  window.addEventListener('load',function(){
    // Normally engine.js dispatches screen-rendered first. This is only a
    // resilience fallback if another host omitted the lifecycle event.
    if (!chapterRows.length) buildChapterRows();
    initializeResume();
    if (location.hash) {
      var id;
      try { id=decodeURIComponent(location.hash.slice(1)); } catch (_) { id=location.hash.slice(1); }
      if (targetFor(id)) setTimeout(function(){targetFor(id).scrollIntoView();},40);
    }
  });
})();