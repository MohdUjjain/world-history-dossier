(function(){
"use strict";

/* ================= CONFIG ================= */
var PAGE_W=1280, PAGE_H=720, HEAD_H=46, FOOT_H=30, PAD_X=26, PAD_Y=20, GUTTER=24, SIDE_W=330;
var MAIN_W = PAGE_W - 2*PAD_X - GUTTER - SIDE_W;   // 874
var FULL_W = PAGE_W - 2*PAD_X;                      // 1228
var CONTENT_H = PAGE_H - HEAD_H - FOOT_H - 2*PAD_Y; // 604
var SAFETY_BUFFER = 44; // cushion against any residual sub-pixel drift between the
                        // measuring rig and the live page, so packing decisions
                        // never rely on the exact last pixel of budget. Scaled up
                        // alongside the larger print font sizes, since drift grows
                        // roughly with line count and text height.
var PAGE_BUDGET = CONTENT_H - SAFETY_BUFFER;

/* Chapter identity palette. Each chapter is assigned one {id, contrast} pair,
   cycling by chapter index so the book stays visually varied as chapters are
   added, while every pair stays dark/muted enough for white text (banner) and
   readable against parchment (body accents). 'id' brands that chapter's own
   sections; 'contrast' brands ONLY its end-of-chapter revision material, so
   revision always reads as a distinctly different zone. */
var CHAPTER_PALETTE = [
  {id:'#A9793B', contrast:'#1E5F5A'}, // brass gold      <-> deep teal
  {id:'#3E7C7C', contrast:'#7E2A31'}, // verdigris teal  <-> oxblood
  {id:'#8B3A3F', contrast:'#3E6B8A'}, // oxblood crimson <-> steel blue
  {id:'#4A5C8A', contrast:'#C08A2E'}, // slate blue      <-> amber
  {id:'#5C6E3E', contrast:'#6B3F78'}, // olive forest    <-> plum
  {id:'#6B3F78', contrast:'#5C6E3E'}, // plum            <-> olive
  {id:'#A85C32', contrast:'#2E4A6B'}, // rust            <-> ink-blue
  {id:'#2E4A6B', contrast:'#A85C32'}  // ink-blue        <-> rust
];
function paletteFor(chapterNum){
  var i = Math.abs(parseInt(chapterNum,10)) % CHAPTER_PALETTE.length;
  return CHAPTER_PALETTE[i];
}
var INCLUDE_REVISION = true; // toggled by the sidebar "Include chapter summaries" checkbox
var MIN_HEAD_SPACE = 170;

/* ================= MEASURING RIGS ================= */
function makeRig(width, cls){
  var d=document.createElement('div');
  d.className='measure-rig '+cls;
  d.style.cssText='position:fixed; left:-9999px; top:0; width:'+width+'px; visibility:hidden;';
  document.body.appendChild(d);
  return d;
}
var rigMain=makeRig(MAIN_W,'col-main');
var rigSide=makeRig(SIDE_W,'col-side');
var rigFull=makeRig(FULL_W,'col-full');

function heightOf(node,rig){
  // Measure a CLONE, never the original — 'node' must stay permanently attached
  // to its parent in #chapterData so renderScreenView() can be called again at
  // any point (e.g. every time the "include summaries" checkbox toggles) and
  // still find pristine, un-consumed content to clone from.
  var clone = node.cloneNode(true);
  rig.appendChild(clone);
  var h = clone.getBoundingClientRect().height;
  rig.removeChild(clone);
  return h;
}

/* ================= BLOCK EXTRACTION ================= */
function extractBlocks(container, rig){
  var out=[];
  var kids=Array.from(container.children);
  kids.forEach(function(el){
    var keep=el.getAttribute('data-keep')||'together';
    var kind=el.getAttribute('data-kind')||'generic';
    if(keep==='split-table'){
      // Measure a CLONE so 'el' itself never leaves #chapterData. rowsOriginal
      // is sourced from the ORIGINAL element (still attached), so it stays the
      // pristine source-of-truth for every future resetWorkingCopies() call —
      // across any number of screen re-renders and print builds.
      var measureClone = el.cloneNode(true);
      var mTable=measureClone.querySelector('table');
      var mThead=mTable.querySelector('thead');
      var mRows=Array.from(mTable.querySelectorAll('tbody > tr'));
      var mCap=mTable.querySelector('caption');
      var mWrapEl=measureClone.querySelector('.table-wrap');
      rig.appendChild(measureClone);
      var theadH=mThead.getBoundingClientRect().height;
      var capH = mCap ? mCap.getBoundingClientRect().height : 0;
      var rowHs=mRows.map(function(r){return r.getBoundingClientRect().height;});
      var rowsSum = rowHs.reduce(function(a,b){return a+b;},0);
      // wrapOverhead captures ANY extra spacing on .table-wrap itself (border,
      // padding) that isn't part of caption/thead/rows individually — measured
      // dynamically so future CSS tweaks to .table-wrap can't silently
      // reintroduce a height-accounting gap the way a hardcoded constant would.
      var wrapOverhead = mWrapEl.getBoundingClientRect().height - (capH+theadH+rowsSum);
      if(wrapOverhead < 0) wrapOverhead = 0;
      rig.removeChild(measureClone);
      var origTable = el.querySelector('table');
      var origRows = Array.from(origTable.querySelectorAll('tbody > tr'));
      var origCap = origTable.querySelector('caption');
      out.push({kind:kind, keep:keep, node:el, height:wrapOverhead+capH+theadH+rowsSum,
                theadH:theadH, capH:capH, wrapOverhead:wrapOverhead, rowsOriginal:origRows, rowHsOriginal:rowHs,
                rows:null, rowHs:null, table:origTable, capText: origCap?origCap.textContent:null,
                started:false});
    } else if(keep==='split-list'){
      var measureClone2 = el.cloneNode(true);
      var mList=measureClone2.querySelector('ul,ol');
      var mItems=Array.from(mList.children);
      rig.appendChild(measureClone2);
      var fullH=measureClone2.getBoundingClientRect().height;
      var itemHs=mItems.map(function(li){return li.getBoundingClientRect().height;});
      rig.removeChild(measureClone2);
      var sumItems=itemHs.reduce(function(a,b){return a+b;},0);
      var origList = el.querySelector('ul,ol');
      var origItems = Array.from(origList.children);
      out.push({kind:kind, keep:keep, node:el, height:fullH, itemsOriginal:origItems, itemHsOriginal:itemHs,
                items:null, itemHs:null, list:origList,
                nonListH: fullH-sumItems, started:false});
    } else {
      var h=heightOf(el,rig);
      var title = el.getAttribute('data-title')||null;
      out.push({kind:kind, keep:keep, node:el, height:h, title:title});
    }
  });
  return out;
}

/* Regenerate fresh, disposable working copies of every split-table/split-list
   block's row/item data from its pristine original, and reset the 'started'
   flag. Must run at the top of every runPipeline() call — packChapter()
   consumes (shifts) the working arrays, so without this reset a second
   pagination pass over the same chapter would see already-drained queues. */
function resetWorkingCopies(chapters){
  chapters.forEach(function(ch){
    ch.main.concat(ch.side).forEach(function(blk){
      if(blk.keep==='split-table'){
        blk.rows = blk.rowsOriginal.map(function(tr){ return tr.cloneNode(true); });
        blk.rowHs = blk.rowHsOriginal.slice();
        blk.started = false;
      } else if(blk.keep==='split-list'){
        blk.items = blk.itemsOriginal.map(function(li){ return li.cloneNode(true); });
        blk.itemHs = blk.itemHsOriginal.slice();
        blk.started = false;
      }
    });
  });
}

/* ================= SLICE HELPERS ================= */
function sliceTableBlock(blk, rowsToTake, isFirst){
  var wrap = blk.node.cloneNode(false);
  wrap.setAttribute('data-kind', blk.kind);
  var innerWrap = blk.node.querySelector('.table-wrap');
  var innerClone = innerWrap ? innerWrap.cloneNode(false) : document.createElement('div');
  if(innerWrap) wrap.appendChild(innerClone); else wrap.appendChild(innerClone);
  var tableClone = blk.table.cloneNode(false);
  innerClone.appendChild(tableClone);
  if(blk.capText){
    var capEl=document.createElement('caption');
    capEl.textContent = isFirst? blk.capText : (blk.capText+' (continued)');
    tableClone.appendChild(capEl);
  }
  var theadClone = blk.table.querySelector('thead').cloneNode(true);
  tableClone.appendChild(theadClone);
  var tbody=document.createElement('tbody');
  tableClone.appendChild(tbody);
  for(var i=0;i<rowsToTake;i++){
    tbody.appendChild(blk.rows.shift());
    blk.rowHs.shift();
  }
  return wrap;
}
function sliceListBlock(blk, itemsToTake, isFirst){
  var wrap = blk.node.cloneNode(true); // deep clone keeps label/box chrome
  var list = wrap.querySelector('ul,ol');
  // remove the placeholder deep-cloned items; we'll move the REAL nodes in
  while(list.firstChild) list.removeChild(list.firstChild);
  if(!isFirst){
    var lbl=wrap.querySelector('.box-label');
    if(lbl) lbl.insertAdjacentHTML('beforeend',' <span class="contd-label">(continued)</span>');
  }
  for(var i=0;i<itemsToTake;i++){
    list.appendChild(blk.items.shift());
    blk.itemHs.shift();
  }
  return wrap;
}

/* ================= PACK ONE CHAPTER ================= */
function fillPages(mainQ, sideQ, pages, ch, isRevision, startSectionTitle){
  var lastSection = startSectionTitle;
  var guard=0;
  while(mainQ.length || sideQ.length){
    if(++guard>3000){ console.error('pagination guard tripped for chapter', ch.num); break; }
    var page={type:'content', chapterNum:ch.num, chapterTitle:ch.title, sectionTitle:lastSection,
              isRevision:isRevision, main:[], side:[]};
    var mainUsed=0, sideUsed=0;

    while(mainQ.length){
      var blk=mainQ[0];
      var remaining = PAGE_BUDGET - mainUsed;

      if(blk.keep==='split-table'){
        if(blk.rowHs.length===0){ mainQ.shift(); continue; }
        var isFirst = !blk.started;
        var headOverhead = blk.wrapOverhead + blk.theadH + (isFirst ? blk.capH : 0);
        var need = headOverhead + blk.rowHs[0];
        if(remaining < need){
          if(mainUsed===0){ /* force one row even if tight, to guarantee progress */ }
          else break;
        }
        var rowsFit=0, used=headOverhead;
        while(rowsFit<blk.rowHs.length && (used+blk.rowHs[rowsFit] <= remaining || rowsFit===0)){
          used+=blk.rowHs[rowsFit]; rowsFit++;
          if(used>remaining && rowsFit>0) break;
        }
        if(rowsFit===0) rowsFit=1;
        blk.started=true;
        var slice = sliceTableBlock(blk, rowsFit, isFirst);
        page.main.push(slice); mainUsed+=used;
        continue;
      }

      if(blk.keep==='split-list'){
        if(blk.itemHs.length===0){ mainQ.shift(); continue; }
        var need2 = blk.nonListH + blk.itemHs[0];
        if(remaining < need2 && mainUsed>0){ break; }
        var itemsFit=0, used2=blk.nonListH;
        while(itemsFit<blk.itemHs.length && (used2+blk.itemHs[itemsFit] <= remaining || itemsFit===0)){
          used2+=blk.itemHs[itemsFit]; itemsFit++;
          if(used2>remaining && itemsFit>0) break;
        }
        if(itemsFit===0) itemsFit=1;
        var isFirst2 = !blk.started; blk.started=true;
        var slice2 = sliceListBlock(blk, itemsFit, isFirst2);
        page.main.push(slice2); mainUsed+=used2;
        continue;
      }

      // atomic block
      var needSpace = (blk.kind==='section-head') ? Math.max(blk.height, MIN_HEAD_SPACE) : blk.height;
      if(mainUsed===0 || needSpace<=remaining){
        page.main.push(blk.node); mainUsed+=blk.height;
        if(blk.kind==='section-head'){ lastSection=blk.title; page.sectionTitle=blk.title; }
        mainQ.shift();
      } else break;
    }

    while(sideQ.length){
      var sblk=sideQ[0];
      var sremaining=PAGE_BUDGET - sideUsed;

      if(sblk.keep==='split-table'){
        if(sblk.rowHs.length===0){ sideQ.shift(); continue; }
        var sIsFirst = !sblk.started;
        var sHeadOverhead = sblk.wrapOverhead + sblk.theadH + (sIsFirst ? sblk.capH : 0);
        var sNeed = sHeadOverhead + sblk.rowHs[0];
        if(sremaining < sNeed){
          if(sideUsed===0){ /* force one row even if tight, to guarantee progress */ }
          else break;
        }
        var sRowsFit=0, sUsed=sHeadOverhead;
        while(sRowsFit<sblk.rowHs.length && (sUsed+sblk.rowHs[sRowsFit] <= sremaining || sRowsFit===0)){
          sUsed+=sblk.rowHs[sRowsFit]; sRowsFit++;
          if(sUsed>sremaining && sRowsFit>0) break;
        }
        if(sRowsFit===0) sRowsFit=1;
        sblk.started=true;
        page.side.push(sliceTableBlock(sblk, sRowsFit, sIsFirst)); sideUsed+=sUsed;
        continue;
      }

      if(sblk.keep==='split-list'){
        if(sblk.itemHs.length===0){ sideQ.shift(); continue; }
        var sNeed2 = sblk.nonListH + sblk.itemHs[0];
        if(sremaining < sNeed2 && sideUsed>0){ break; }
        var sItemsFit=0, sUsed2=sblk.nonListH;
        while(sItemsFit<sblk.itemHs.length && (sUsed2+sblk.itemHs[sItemsFit] <= sremaining || sItemsFit===0)){
          sUsed2+=sblk.itemHs[sItemsFit]; sItemsFit++;
          if(sUsed2>sremaining && sItemsFit>0) break;
        }
        if(sItemsFit===0) sItemsFit=1;
        var sIsFirst2 = !sblk.started; sblk.started=true;
        page.side.push(sliceListBlock(sblk, sItemsFit, sIsFirst2)); sideUsed+=sUsed2;
        continue;
      }

      // atomic
      if(sideUsed===0 || sblk.height<=sremaining){
        page.side.push(sblk.node); sideUsed+=sblk.height; sideQ.shift();
      } else break;
    }

    pages.push(page);
  }
}

function packChapter(ch, pages){
  pages.push({type:'hero', chapterNum:ch.num, chapterTitle:ch.title, heroNode:ch.heroNode});

  // Split each chapter's queues at the revision boundary (marked via
  // data-revision-start on the "Chapter Summary" section-head and the first
  // collected-definitions side block). Packing them as a SEPARATE fillPages()
  // call — rather than just continuing the same loop — is what guarantees the
  // revision material always starts on a fresh page: a new call always opens
  // with an empty page, regardless of how much space was left on the last
  // body page.
  var isRevMain = function(b){ return b.node.getAttribute && b.node.getAttribute('data-revision-start')==='true'; };
  var mainSplit = ch.main.findIndex(isRevMain);
  var sideSplit = ch.side.findIndex(isRevMain);
  var bodyMain = mainSplit===-1 ? ch.main.slice() : ch.main.slice(0, mainSplit);
  var revMain  = mainSplit===-1 ? [] : ch.main.slice(mainSplit);
  var bodySide = sideSplit===-1 ? ch.side.slice() : ch.side.slice(0, sideSplit);
  var revSide  = sideSplit===-1 ? [] : ch.side.slice(sideSplit);

  // Pack narrative first. Placing side notes independently by their total height
  // made chapter concepts drift to unrelated pages. The second pass anchors
  // each note to a page containing the corresponding main-text section.
  var bodyPages=[];
  fillPages(bodyMain, [], bodyPages, ch, false, ch.title);
  attachSectionSideNotes(bodyPages, bodySide, ch, false);
  bodyPages.forEach(function(pg){pages.push(pg);});
  if(INCLUDE_REVISION && (revMain.length || revSide.length)){
    var revisionPages=[];
    fillPages(revMain, [], revisionPages, ch, true, 'Chapter Summary');
    attachSectionSideNotes(revisionPages, revSide, ch, true);
    revisionPages.forEach(function(pg){pages.push(pg);});
  }
}

/**
 * Section-aware sidebar placement for the paginated PDF.
 * A card prefers the FIRST page with the associated section in the main column;
 * if that page is full, later pages of that section are tried before spillover.
 * When all normal candidates are full, append a safe side-only continuation
 * page immediately following the section, instead of losing/overlapping cards.
 * This packs from disposable measurement data and never moves source nodes.
 */
function fitSidebarFragment(blk, available){
  if(blk.keep==='split-list'){
    if(!blk.itemHs.length) return null;
    var used=blk.nonListH, n=0;
    while(n<blk.itemHs.length && used+blk.itemHs[n]<=available){
      used+=blk.itemHs[n];n++;
    }
    if(!n) return null;
    var first=!blk.started;blk.started=true;
    return {node:sliceListBlock(blk,n,first),height:used,done:!blk.itemHs.length};
  }
  if(blk.keep==='split-table'){
    if(!blk.rowHs.length) return null;
    var first=!blk.started;
    var used=blk.wrapOverhead+blk.theadH+(first?blk.capH:0),n=0;
    while(n<blk.rowHs.length && used+blk.rowHs[n]<=available){
      used+=blk.rowHs[n];n++;
    }
    if(!n) return null;
    blk.started=true;
    return {node:sliceTableBlock(blk,n,first),height:used,done:!blk.rowHs.length};
  }
  if(blk.height>available) return null;
  return {node:blk.node,height:blk.height,done:true};
}
function attachSectionSideNotes(pages, blocks, ch, isRevision){
  if(!blocks.length) return;
  if(!pages.length){
    pages.push({type:'content',chapterNum:ch.num,chapterTitle:ch.title,
      sectionTitle:isRevision?'Chapter Summary':ch.title,isRevision:isRevision,main:[],side:[]});
  }
  var heights=new Map();
  pages.forEach(function(pg){heights.set(pg,0);});
  var lastPlaced=0;
  blocks.forEach(function(blk){
    var section=blk.node.getAttribute('data-for-section')||'intro';
    var incomplete=true, forceAfterLast=false, guard=0;
    while(incomplete){
      if(++guard>500){console.error('Sidebar split guard',ch.num,section);break;}
      var matches=[];
      pages.forEach(function(pg,i){
        if(pg.main.some(function(node){return node.getAttribute && node.getAttribute('data-content-section')===section;})) matches.push(i);
      });
      var first=matches.length?matches[0]:lastPlaced;
      var eligible=matches.filter(function(i){return i>=lastPlaced && (!forceAfterLast || i>lastPlaced);});
      var later=[];
      for(var i=Math.max(first,lastPlaced+(forceAfterLast?1:0));i<pages.length;i++){
        if(eligible.indexOf(i)===-1) later.push(i);
      }
      var options=eligible.concat(later),placed=false;
      options.some(function(i){
        var pg=pages[i], available=PAGE_BUDGET-(heights.get(pg)||0);
        var fragment=fitSidebarFragment(blk,available);
        if(!fragment) return false;
        pg.side.push(fragment.node);heights.set(pg,(heights.get(pg)||0)+fragment.height);
        lastPlaced=i;incomplete=!fragment.done;forceAfterLast=incomplete;placed=true;return true;
      });
      if(!placed){
        // Insert a continuation immediately after the matching section's last
        // page, and split long lists/tables there. This also supports old
        // archival chapter fixtures which had very large sidebar glossaries.
        var anchor=Math.max(lastPlaced,matches.length?matches[matches.length-1]:lastPlaced);
        var prev=pages[Math.min(anchor,pages.length-1)];
        var fragment=fitSidebarFragment(blk,PAGE_BUDGET);
        if(!fragment){console.error('Unbreakable sidebar block exceeds page',ch.num,section);break;}
        var continuation={type:'content',chapterNum:ch.num,chapterTitle:ch.title,
          sectionTitle:prev.sectionTitle||ch.title,isRevision:isRevision,main:[],side:[fragment.node]};
        pages.splice(anchor+1,0,continuation);
        heights.set(continuation,fragment.height);lastPlaced=anchor+1;
        incomplete=!fragment.done;forceAfterLast=incomplete;
      }
    }
  });
}

/* ================= TOC PACK (full width, no sidebar) ================= */
function packRows(rows){
  var pages=[]; var q=rows.slice(); var guard=0;
  while(q.length){
    if(++guard>500) break;
    var page={type:'toc', main:[]}; var used=0;
    while(q.length){
      var r=q[0]; var rem=PAGE_BUDGET-used;
      if(used===0 || r.height<=rem){ page.main.push(r.node); used+=r.height; q.shift(); }
      else break;
    }
    pages.push(page);
  }
  return pages;
}
function FULL_W_H(){ return CONTENT_H; }

/* ================= BUILD CHAPTER MODEL FROM DOM ================= */
/*
 * Concepts belong to the EDUCATIONAL SIDEBAR, not the narrative column.
 * Build normalized throwaway streams rather than mutating #chapterData.
 * This is a defensive fallback for incorrectly authored main-column concept
 * blocks; new chapter files should put concepts in .src-side directly.
 * data-kind="list" revision question banks are NOT moved merely because they
 * use the green .box.concept style.
 */
function normalizedStreams(chEl){
  var main = chEl.querySelector('.src-main').cloneNode(true);
  var side = chEl.querySelector('.src-side').cloneNode(true);
  var sideRevision = Array.from(side.children).find(function(b){
    return b.getAttribute('data-revision-start')==='true';
  }) || null;
  var inRevision = false;
  Array.from(main.children).forEach(function(block){
    if(block.getAttribute('data-revision-start')==='true') inRevision=true;
    if(block.getAttribute('data-kind')!=='concept') return;
    main.removeChild(block);
    if(inRevision && !sideRevision){
      // A chapter may have revision content in the main stream without any
      // sidebar revision block. Preserve its zone when a concept moves across.
      sideRevision=document.createElement('div');
      sideRevision.className='block';
      sideRevision.setAttribute('data-kind','revision-divider');
      sideRevision.setAttribute('data-revision-start','true');
      sideRevision.setAttribute('data-keep','together');
      sideRevision.style.display='none';
      side.appendChild(sideRevision);
    }
    if(!inRevision && sideRevision) side.insertBefore(block, sideRevision);
    else side.appendChild(block);
  });
  // Keep narrative source immutable. Attach section identity only to these
  // disposable clones, used by BOTH screen pairing and print side-note packing.
  var currentSection='intro', serial=0;
  Array.from(main.children).forEach(function(block){
    if(block.getAttribute('data-kind')==='section-head'){
      serial++;
      currentSection=block.getAttribute('data-section-key') || 'section-'+serial;
    }
    block.setAttribute('data-content-section', currentSection);
  });
  Array.from(side.children).forEach(function(block){
    if(!block.hasAttribute('data-for-section')) block.setAttribute('data-for-section','intro');
  });
  return {main:main, side:side};
}
function buildChapters(){
  var srcEls = Array.from(document.querySelectorAll('#chapterData .chapter-source'));
  return srcEls.map(function(el){
    var num = el.getAttribute('data-chapter');
    var title = el.getAttribute('data-title');
    var author = el.getAttribute('data-author');
    var subtitle = el.getAttribute('data-subtitle');
    var heroSrc = el.querySelector('.src-hero');
    var heroNode = buildHeroNode(heroSrc, num, title, author, subtitle);
    var streams = normalizedStreams(el);
    var main = extractBlocks(streams.main, rigMain);
    var side = extractBlocks(streams.side, rigSide);
    return {num:num, title:title, author:author, subtitle:subtitle, heroNode:heroNode, main:main, side:side};
  });
}

function buildHeroNode(src, num, title, author, subtitle){
  var kicker = src.querySelector('.hk').textContent;
  var thesis = src.querySelector('.hthesis').innerHTML;
  var years = src.querySelector('.hyears').textContent.split(',').map(function(s){return s.trim();});
  var wrap=document.createElement('div'); wrap.className='hero-content';
  var left=document.createElement('div'); left.className='hero-left';
  left.innerHTML =
    '<span class="hero-kicker">'+kicker+'</span>'+
    '<h1 class="hero-title">'+title+'</h1>'+
    '<p class="hero-subtitle">'+subtitle+'</p>'+
    '<p class="hero-byline">'+author+'</p>'+
    '<div class="hero-thesis"><span class="lbl">Central Thesis</span>'+thesis+'</div>';
  var right=document.createElement('div'); right.className='hero-right';
  var rows = years.map(function(y){return '<div class="yr-pt"><b>'+y+'</b></div>';}).join('');
  right.innerHTML = '<div class="hero-ribbon-lbl">Timeline</div><div class="hero-ribbon">'+rows+'</div>';
  wrap.appendChild(left); wrap.appendChild(right);
  return wrap;
}

/* ================= TOC ENTRIES ================= */
function collectTocEntries(contentPages){
  var chapters=[]; var cur=null;
  contentPages.forEach(function(p, idx){
    if(p.type==='hero'){
      cur={num:p.chapterNum, title:p.chapterTitle, relPage:idx+1, sections:[]};
      chapters.push(cur);
    } else if(p.type==='content'){
      p.main.forEach(function(n){
        if(n.getAttribute && n.getAttribute('data-kind')==='section-head'){
          cur.sections.push({title:n.getAttribute('data-title'), relPage:idx+1});
        }
      });
    }
  });
  return chapters;
}
function buildTocRowNodes(chapters){
  var rows=[];
  chapters.forEach(function(ch){
    var pal = paletteFor(ch.num);
    var d=document.createElement('div'); d.className='toc-row chapter';
    d.style.setProperty('--chapter-color', pal.id);
    d.innerHTML='<span class="n">'+String(ch.num).padStart(2,'0')+'</span><a href="#" data-rel="'+ch.relPage+'">'+ch.title+'</a><span class="leader"></span><span class="pg" data-rel-target="'+ch.relPage+'"></span>';
    // Printed contents deliberately lists CHAPTERS ONLY. Section-level
    // navigation belongs in the native PDF bookmark outline generated by
    // tools/export_full_pdf.py (and remains in the on-screen TOC).
    // This keeps the printed index short without dropping detailed navigation.
    rows.push({node:d, height:0, relPage:ch.relPage});
  });
  rows.forEach(function(r){ r.height = heightOf(r.node, rigFull); });
  return rows;
}

/* ================= PRINT RENDER (page boxes) ================= */
function renderPage(p, absNum, isLast){
  var slot=document.createElement('div'); slot.className='page-slot';
  var page=document.createElement('div'); page.className='page type-'+p.type; page.id='pg-'+absNum;

  if(p.type==='hero' || p.type==='content'){
    var pal = paletteFor(p.chapterNum);
    page.style.setProperty('--chapter-color', pal.id);
    page.style.setProperty('--chapter-contrast', pal.contrast);
  }

  if(p.type==='title'){
    var tp=document.createElement('div'); tp.className='pt-inner';
    tp.innerHTML =
      '<div class="pt-mark">&#10022;</div>'+
      '<div class="pt-series">An Independent Study Companion</div>'+
      '<h1 class="pt-title">World History Dossier</h1>'+
      '<p class="pt-subtitle">Study Notes on Twentieth-Century International History</p>'+
      '<div class="pt-rule"></div>'+
      '<p class="pt-desc">Focused, clearly structured study notes, rebuilt chapter by chapter for comfortable reading and revision.</p>'+
      '<div class="pt-imprint"><p>Prepared by <strong>Mohammed Husain Ujjainwala</strong></p><p>TR 25368 &middot; Hadi Ashar 1448H</p></div>';
    page.appendChild(tp);
  } else if(p.type==='hero'){
    page.appendChild(p.heroNode.cloneNode(true));
    var f=document.createElement('div'); f.className='page-footer-bar';
    f.innerHTML='<span></span><span>'+absNum+'</span>';
    page.appendChild(f);
  } else if(p.type==='toc'){
    var h=document.createElement('div'); h.className='page-header-bar';
    h.innerHTML='<span class="h-chap">Contents</span><span class="h-sec">20th-Century International History</span>';
    page.appendChild(h);
    var inner=document.createElement('div'); inner.className='page-inner full';
    var col=document.createElement('div'); col.className='col-full';
    // clone: TOC rows are freshly built (not from #chapterData) so cloning is
    // just extra safety; costs nothing meaningful
    p.main.forEach(function(n){ col.appendChild(n.cloneNode(true)); });
    inner.appendChild(col); page.appendChild(inner);
    var f2=document.createElement('div'); f2.className='page-footer-bar';
    f2.innerHTML='<span>Running Notes</span><span>'+absNum+'</span>';
    page.appendChild(f2);
  } else { // content
    if(p.isRevision) page.classList.add('is-revision');
    var h2=document.createElement('div'); h2.className='page-header-bar';
    var chapLabel = String(p.chapterNum).padStart(2,'0')+' — '+p.chapterTitle + (p.isRevision ? ' · Revision' : '');
    h2.innerHTML='<span class="h-chap">Chapter '+chapLabel+'</span><span class="h-sec">'+(p.sectionTitle||'')+'</span>';
    page.appendChild(h2);
    var inner2=document.createElement('div'); inner2.className='page-inner';
    var colMain=document.createElement('div'); colMain.className='col-main';
    // CRITICAL: clone before append. blk.node for atomic blocks is the ORIGINAL
    // DOM node still living in #chapterData. Without cloning, appendChild() MOVES
    // it out of #chapterData, leaving nothing for the next renderScreenView() call.
    // Split-table/split-list slices are already freshly-built elements (not originals),
    // so cloning them is harmless duplication.
    p.main.forEach(function(n){ colMain.appendChild(n.cloneNode(true)); });
    var colSide=document.createElement('div'); colSide.className='col-side';
    p.side.forEach(function(n){ colSide.appendChild(n.cloneNode(true)); });
    inner2.appendChild(colMain); inner2.appendChild(colSide);
    page.appendChild(inner2);
    var f3=document.createElement('div'); f3.className='page-footer-bar';
    f3.innerHTML='<span>20th-Century International History</span><span>'+absNum+'</span>';
    page.appendChild(f3);
  }
  slot.appendChild(page);
  return slot;
}

/* ================= PRINT PIPELINE (builds #printView only — never shown on screen) ================= */
var ALL_CHAPTERS = null;
var lastRange = null;

function buildPrintView(chapterNumList){
  if(!ALL_CHAPTERS) ALL_CHAPTERS = buildChapters();
  var chapters = chapterNumList.map(function(n){
    return ALL_CHAPTERS.find(function(c){ return parseInt(c.num,10)===n; });
  }).filter(Boolean);
  lastRange = chapterNumList.slice();

  var contentPages=[];
  chapters.forEach(function(ch){
    // Reset THIS chapter's split-table/list working copies immediately before
    // packing it (not once for the whole batch) — so if the same chapter number
    // is listed twice in one export, both occurrences get fresh, complete content
    // instead of the second seeing rows/items already drained by the first.
    resetWorkingCopies([ch]);
    packChapter(ch, contentPages);
  });

  var tocChapters = collectTocEntries(contentPages);
  var tocPages=[];
  if(chapters.length>1){
    var rows = buildTocRowNodes(tocChapters);
    tocPages = packRows(rows);
  }
  var T = tocPages.length;

  var wrap = document.getElementById('printView');
  wrap.innerHTML='';
  var n=0;
  n++; wrap.appendChild(renderPage({type:'title'}, n)); // page 1 — number consumed but not displayed, matching book convention
  tocPages.forEach(function(tp){ n++; wrap.appendChild(renderPage(tp, n)); });
  contentPages.forEach(function(p, idx){ p.__abs = 1 + T + idx + 1; });
  wrap.querySelectorAll('[data-rel-target]').forEach(function(el){
    var rel=parseInt(el.getAttribute('data-rel-target'),10);
    el.textContent = 1 + T + rel;
  });
  wrap.querySelectorAll('a[data-rel]').forEach(function(a){
    var rel=parseInt(a.getAttribute('data-rel'),10);
    a.setAttribute('href','#pg-'+(1+T+rel));
  });
  contentPages.forEach(function(p){ n++; wrap.appendChild(renderPage(p, n)); });
}

/* ================= FLOWING SCREEN VIEW (comfortable, continuous — never paginated) ================= */
function buildFlowingHero(src, num, title, author, subtitle){
  var kicker = src.querySelector('.hk').textContent;
  var thesis = src.querySelector('.hthesis').innerHTML;
  var years = src.querySelector('.hyears').textContent.split(',').map(function(s){return s.trim();});
  var wrap=document.createElement('div'); wrap.className='banner';
  var yrHtml = years.map(function(y){return '<span>'+y+'</span>';}).join('');
  wrap.innerHTML =
    '<span class="kicker">'+kicker+'</span>'+
    '<h1>'+title+'</h1>'+
    '<p class="subtitle">'+subtitle+'</p>'+
    '<p class="byline">'+author+'</p>'+
    '<div class="thesis"><span class="lbl">Central Thesis</span>'+thesis+'</div>'+
    '<div class="yrs">'+yrHtml+'</div>';
  return wrap;
}

/**
 * Continuous HTML remains flowing, but each narrative section and its
 * educational sidebar get their OWN grid row. This prevents notes from
 * collecting at the top of a long chapter and gives a close visual pairing.
 */
function appendPairedSections(host, mainNodes, sideNodes){
  var groups=[], byKey=new Map(), active='intro';
  mainNodes.forEach(function(node){
    var key=node.getAttribute('data-content-section')||active;
    active=key;
    if(!byKey.has(key)){
      var group={key:key,main:[],side:[]};
      byKey.set(key,group);groups.push(group);
    }
    byKey.get(key).main.push(node);
  });
  sideNodes.forEach(function(node){
    var key=node.getAttribute('data-for-section')||'intro';
    if(!byKey.has(key)){
      var extra={key:key,main:[],side:[]};
      byKey.set(key,extra);groups.push(extra);
    }
    byKey.get(key).side.push(node);
  });
  groups.forEach(function(group){
    var grid=document.createElement('div');
    grid.className='chapter-grid section-pair';
    grid.setAttribute('data-section-pair',group.key);
    var mainCol=document.createElement('div'); mainCol.className='main-flow';
    group.main.forEach(function(n){mainCol.appendChild(n);});
    var sideCol=document.createElement('aside');sideCol.className='side-flow';
    sideCol.setAttribute('aria-label','Study aids for '+group.key);
    group.side.forEach(function(n){sideCol.appendChild(n);});
    grid.appendChild(mainCol);grid.appendChild(sideCol);host.appendChild(grid);
  });
}

function renderScreenView(){
  var root = document.getElementById('screenView');
  root.innerHTML = '';
  var jumpEntries = [];
  var secCounter = 0;

  var activeChapters = Array.from(document.querySelectorAll('#chapterData .chapter-source'));
  if(!activeChapters.length){
    root.innerHTML = '<section class="empty-state"><div class="empty-state-eyebrow">Ready for new notes</div>'+ 
      '<h2>Your refreshed World History Dossier begins here.</h2>'+ 
      '<p>The previous long notes have been archived outside the active book. '+
      'Send the new Chapter 00 notes to populate this reading view.</p></section>';
    buildNavPanel([]);
    return;
  }
  activeChapters.forEach(function(chEl){
    var num = chEl.getAttribute('data-chapter'), title = chEl.getAttribute('data-title'),
        author = chEl.getAttribute('data-author'), subtitle = chEl.getAttribute('data-subtitle');
    var pal = paletteFor(num);

    var section = document.createElement('section');
    section.className = 'chapter-flow';
    section.id = 'chapter-'+num;
    section.style.setProperty('--chapter-color', pal.id);
    section.style.setProperty('--chapter-contrast', pal.contrast);

    section.appendChild(buildFlowingHero(chEl.querySelector('.src-hero'), num, title, author, subtitle));

    var streams = normalizedStreams(chEl);
    var mainAll = Array.from(streams.main.children);
    var sideAll = Array.from(streams.side.children);
    var isRevMarker = function(b){ return b.getAttribute('data-revision-start')==='true'; };
    var mSplit = mainAll.findIndex(isRevMarker);
    var sSplit = sideAll.findIndex(isRevMarker);
    var bodyMain = mSplit===-1 ? mainAll : mainAll.slice(0,mSplit);
    var revMain  = mSplit===-1 ? [] : mainAll.slice(mSplit);
    var bodySide = sSplit===-1 ? sideAll : sideAll.slice(0,sSplit);
    var revSide  = sSplit===-1 ? [] : sideAll.slice(sSplit);

    appendPairedSections(section, bodyMain, bodySide);

    if(INCLUDE_REVISION && (revMain.length || revSide.length)){
      var revWrap = document.createElement('div'); revWrap.className='revision-flow';
      var revBadge = document.createElement('div'); revBadge.className='revision-badge';
      revBadge.textContent = 'Chapter '+num+' Revision';
      revWrap.appendChild(revBadge);
      appendPairedSections(revWrap, revMain, revSide);
      section.appendChild(revWrap);
    }

    root.appendChild(section);

    jumpEntries.push({kind:'chapter', num:num, title:title, id:section.id});
    section.querySelectorAll('[data-kind="section-head"]').forEach(function(sh){
      secCounter++;
      var id = 'sec-'+secCounter;
      sh.id = id;
      jumpEntries.push({kind:'section', chapterNum:num, title:sh.getAttribute('data-title'), id:id});
    });
  });

  buildNavPanel(jumpEntries);
  setupChapterSpy();
}

function buildNavPanel(entries){
  var toc = document.getElementById('navToc');
  toc.innerHTML = '';
  if(!entries.length){ toc.innerHTML='<p class="nav-empty">No chapters yet. New chapters will appear here automatically.</p>'; return; }
  var currentChapterEl = null, currentSections = null;
  entries.forEach(function(e){
    if(e.kind==='chapter'){
      var pal = paletteFor(e.num);
      var wrap = document.createElement('div'); wrap.className='nav-chapter';
      var row = document.createElement('div'); row.className='nav-chapter-row';
      row.innerHTML = '<span class="car">▸</span><span class="dot" style="background:'+pal.id+'"></span><span class="lbl">Ch.'+String(e.num).padStart(2,'0')+' — '+e.title+'</span>';
      var sections = document.createElement('div'); sections.className='nav-sections';
      row.addEventListener('click', function(){ wrap.classList.toggle('expanded'); });
      wrap.appendChild(row); wrap.appendChild(sections);
      toc.appendChild(wrap);
      currentChapterEl = wrap; currentSections = sections;
    } else if(currentSections){
      var a = document.createElement('a');
      a.href = '#'+e.id;
      a.textContent = e.title;
      a.addEventListener('click', function(ev){
        ev.preventDefault();
        closeNav();
        var target = document.getElementById(e.id);
        if(target) target.scrollIntoView({behavior:'smooth', block:'start'});
      });
      currentSections.appendChild(a);
    }
  });
}

function openNav(){ document.getElementById('navPanel').classList.add('open'); document.getElementById('navOverlay').classList.add('open'); }
function closeNav(){ document.getElementById('navPanel').classList.remove('open'); document.getElementById('navOverlay').classList.remove('open'); }
document.getElementById('navTab').addEventListener('click', openNav);
document.getElementById('navClose').addEventListener('click', closeNav);
document.getElementById('navOverlay').addEventListener('click', closeNav);

/* ---- reading progress bar (kept visible throughout, including revision zones) ---- */
function updateProgress(){
  var doc=document.documentElement;
  var scrollable = doc.scrollHeight - window.innerHeight;
  var pct = scrollable>0 ? Math.min(100, Math.max(0, (window.scrollY/scrollable)*100)) : 0;
  document.getElementById('progressFill').style.width = pct+'%';
}
window.addEventListener('scroll', updateProgress, {passive:true});
window.addEventListener('resize', updateProgress);

/* ---- current-chapter label in header, via scroll-spy ---- */
function setupChapterSpy(){
  var label = document.getElementById('currentChapterLabel');
  var sections = document.querySelectorAll('.chapter-flow');
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        var chEl = document.querySelector('#chapterData .chapter-source[data-chapter="'+entry.target.id.replace('chapter-','')+'"]');
        if(chEl) label.textContent = 'Ch.'+String(chEl.getAttribute('data-chapter')).padStart(2,'0')+' — '+chEl.getAttribute('data-title');
      }
    });
  }, {rootMargin:'-10% 0px -80% 0px'});
  sections.forEach(function(s){ io.observe(s); });
}

/* ================= EXPORT CONTROLS (now inside the sidebar panel) ================= */
function lightweightChapterList(){
  return Array.from(document.querySelectorAll('#chapterData .chapter-source')).map(function(el){
    return {num:el.getAttribute('data-chapter'), title:el.getAttribute('data-title')};
  });
}
var rangeChapters = null;

/* Parses strings like "5-6,1,3,20-24" into an ORDERED array of chapter
   numbers, preserving exactly the sequence and direction the person typed
   (so "6-5" walks backward, "5-6" walks forward). Empty input means "the
   whole book, in its natural order." Numbers that don't match a real
   chapter are reported back but simply skipped, rather than blocking the
   rest of a valid export. */
function parseChapterRangeInput(str, allChapters){
  var validNums = allChapters.map(function(c){ return parseInt(c.num,10); });
  var trimmed = (str||'').trim();
  if(!trimmed){
    return {list: validNums.slice(), unknown: [], isDefault:true};
  }
  var list = [], unknown = [];
  trimmed.split(',').forEach(function(tokRaw){
    var tok = tokRaw.trim();
    if(!tok) return;
    var dash = tok.indexOf('-');
    if(dash > 0){ // '-' at position 0 would be a bare negative number, not a range
      var a = parseInt(tok.slice(0,dash),10), b = parseInt(tok.slice(dash+1),10);
      if(isNaN(a) || isNaN(b)){ unknown.push(tok); return; }
      if(a<=b){ for(var i=a;i<=b;i++) list.push(i); } else { for(var j=a;j>=b;j--) list.push(j); }
    } else {
      var n = parseInt(tok,10);
      if(isNaN(n)){ unknown.push(tok); return; }
      list.push(n);
    }
  });
  var finalList = [];
  list.forEach(function(n){
    if(validNums.indexOf(n)!==-1) finalList.push(n);
    else if(unknown.indexOf(String(n))===-1) unknown.push(String(n));
  });
  return {list: finalList, unknown: unknown, isDefault:false};
}

function describeRange(parsed, allChapters){
  var hint = document.getElementById('rangeHint');
  if(!allChapters.length){
    hint.textContent = 'No chapters available yet — add Chapter 00 first.';
    hint.classList.add('error');
    return;
  }
  if(parsed.isDefault){
    hint.textContent = 'Will export: all chapters, in order';
    hint.classList.remove('error');
    return;
  }
  if(parsed.list.length===0){
    hint.textContent = 'No matching chapters — check the numbers';
    hint.classList.add('error');
    return;
  }
  var byNum = {};
  allChapters.forEach(function(c){ byNum[c.num] = c.title; });
  var names = parsed.list.map(function(n){ return 'Ch '+n; });
  var text = 'Will export: ' + names.join(', ');
  if(parsed.unknown.length){
    text += ' — unknown: ' + parsed.unknown.join(', ');
  }
  hint.textContent = text;
  hint.classList.toggle('error', parsed.unknown.length>0);
}

document.getElementById('rangeInput').addEventListener('input', function(e){
  describeRange(parseChapterRangeInput(e.target.value, rangeChapters), rangeChapters);
});

document.getElementById('includeRevisionChk').addEventListener('change', function(e){
  INCLUDE_REVISION = e.target.checked;
  renderScreenView(); // rebuild screen view live so the toggle takes effect immediately
});
document.getElementById('printBtn').addEventListener('click', function(){
  var parsed = parseChapterRangeInput(document.getElementById('rangeInput').value, rangeChapters);
  describeRange(parsed, rangeChapters);
  if(parsed.list.length===0) return; // nothing valid to export — hint already explains why
  buildPrintView(parsed.list);
  closeNav();
  window.print();
});
// Safety net: if printing is triggered natively (Ctrl+P / browser menu) rather
// than via our button, still (re)build the print view fresh for the last-used
// selection immediately beforehand, so print output is never stale or empty.
window.addEventListener('beforeprint', function(){
  var list = lastRange || lightweightChapterList().map(function(c){ return parseInt(c.num,10); });
  if(!list.length) return;
  buildPrintView(list);
});

/* ================= INIT ================= */
window.addEventListener('load', function(){
  renderScreenView();      // clones from pristine #chapterData — must run before any print build
  rangeChapters = lightweightChapterList();
  document.getElementById('printBtn').disabled = !rangeChapters.length;
  describeRange(parseChapterRangeInput('', rangeChapters), rangeChapters);
  updateProgress();
});

})();
