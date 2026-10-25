(function(){
  var river=document.getElementById('river');
  var q=document.getElementById('q');
  var data=null, family='all', term='';
  function ebay(d){return 'https://www.ebay.com/sch/i.html?_nkw='+encodeURIComponent(d.ebay_query);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function plate(d){
    if(d.image){return '<div class="plate"><img src="'+esc(d.image)+'" alt="Official product photo, '+esc(d.name)+'" loading="lazy" decoding="async" onerror="this.parentNode.innerHTML=\'<span class=&quot;initial&quot; aria-hidden=&quot;true&quot;>'+esc(d.name.charAt(0))+'</span>\'"></div>';}
    return '<div class="plate"><span class="initial" aria-hidden="true">'+esc(d.name.charAt(0))+'</span></div><p class="nophoto">No photo yet.</p>';
  }
  /* TS3 (rotation 140): "upcoming" is computed from the release
     date on the visitor's clock, never stored in display text. */
  function todayStr(){var t=new Date();return t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');}
  function stateOf(d){return d.date>todayStr()?' · Upcoming':' · Out now';}
  function row(d){
    return '<article class="drop"><div>'+plate(d)+'</div><div class="dropbody">'
      +'<p class="dropdate">'+esc(d.display_date)+'</p>'
      +'<h3 class="dropname">'+esc(d.name)+'<span class="fam">'+esc(d.family)+'</span></h3>'
      +'<p>'+esc(d.theme)+'</p>'
      +'<p class="lineup"><b>Lineup.</b> '+esc(d.lineup)+'</p>'
      +'<p class="secretline"><b>Secret.</b> '+esc(d.secret)+'</p>'
      +'<a class="ebay" aria-label="Search eBay for '+esc(d.name)+'" href="'+ebay(d)+'" rel="noopener nofollow">Search eBay for this series</a>'
      +'</div></article>';
  }
  /* SO2 (rotation 140): the featured card is generated from the
     data, never a hard-coded sample: the newest drop whose release
     date has arrived, rendered in the catalog card's shape. No
     price is read or rendered here, as everywhere on this site
     (SO4). */
  function featured(){
    var mount=document.getElementById('featured-mount');
    if(!mount||!data)return;
    var released=data.drops.filter(function(d){return d.date<=todayStr();});
    if(!released.length)return;
    var d=released[released.length-1];
    var parts=d.name.split(', Sonny Angel x ');
    var title=parts[0], collab=parts.length>1?('Sonny Angel x '+parts[1]):'';
    var secret=/^To be confirmed/.test(d.secret)?'Not confirmed yet.':d.secret;
    mount.innerHTML='<article class="index-card featured" aria-labelledby="new-h">'
      +'<p class="card-tab">Newest</p>'
      +(d.image?'<figure class="card-photo"><img src="'+esc(d.image)+'" alt="Official product photo, '+esc(d.name)+'" width="828" height="828" fetchpriority="high" decoding="async"><span class="tape" aria-hidden="true"></span></figure>':'')
      +'<div class="card-lines">'
      +'<p class="card-date">'+esc(d.display_date)+stateOf(d)+'</p>'
      +'<h2 class="card-name" id="new-h">'+esc(title)+'</h2>'
      +(collab?'<p class="card-collab">'+esc(collab)+' · '+esc(d.family)+'</p>':'<p class="card-collab">'+esc(d.family)+'</p>')
      +'<p>'+esc(d.theme)+'</p>'
      +'<p><b>Lineup.</b> '+esc(d.lineup)+'</p>'
      +'<p><b class="secret">Secret.</b> '+esc(secret)+'</p>'
      +'<p><a class="card-link" aria-label="Search eBay for '+esc(d.name)+'" href="'+ebay(d)+'" rel="noopener nofollow">Search eBay for this series</a></p>'
      +'</div><span class="card-hole" aria-hidden="true"></span></article>';
  }
  /* TS4 (rotation 143): index.html ships with the river, the
     featured card and the count line already rendered by
     scripts/build.py, in exactly this markup, so the page is
     complete without JavaScript. render() below re-creates the
     identical markup from the public data when the visitor
     searches or filters. */
  function emptyMsg(on,termNow){
    return '<p class="empty" role="status">Nothing matches that.'+(on||termNow?' <button type="button" class="clearall">Show everything</button>':'')+'</p>';
  }
  function clearAll(){
    q.value='';term='';family='all';
    document.querySelectorAll('.filters button').forEach(function(x){var on=x.getAttribute('data-f')==='all';x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false');});
    render();q.focus();
  }
  river.addEventListener('click',function(e){if(e.target.classList&&e.target.classList.contains('clearall'))clearAll();});
  /* A row of year links keeps a 51 card list short to move through. */
  function yearJump(){
    var nav=document.getElementById('yearjump');if(!nav)return;
    var blocks=river.querySelectorAll('.yearblock');
    nav.hidden=!blocks.length;
    var h='';
    blocks.forEach(function(b){var y=b.querySelector('.year').textContent;b.id='y'+y;h+='<a href="#y'+y+'">'+y+'</a>';});
    nav.innerHTML=h;
  }
  function render(){
    if(!data)return;
    var list=data.drops.filter(function(d){
      if(family!=='all'&&d.family!==family)return false;
      if(!term)return true;
      var hay=(d.name+' '+d.theme+' '+d.lineup+' '+d.display_date+' '+d.family).toLowerCase();
      return hay.indexOf(term)>-1;
    });
    var cl=document.getElementById('count-line');
    if(!list.length){
      river.innerHTML=emptyMsg(family!=='all',term);
      cl.textContent='Showing 0 of '+data.meta.catalogued+' releases.';
      river.scrollIntoView({block:'nearest'});
      return;
    }
    var html='',year=null;
    list.forEach(function(d){
      var y=String(d.sort).slice(0,4);
      if(y!==year){if(year!==null)html+='</div></div>';year=y;
        html+='<div class="yearblock"><div class="year" aria-label="Year '+y+'">'+y+'</div><div class="rows">';}
      html+=row(d);
    });
    html+='</div></div>';
    river.innerHTML=html;
    cl.textContent=
      'Showing '+list.length+' of '+data.meta.catalogued+' releases.';
    yearJump();
  }
  yearJump();
  fetch('data/v1/drops.json').then(function(r){return r.json();}).then(function(j){
    data=j;data.drops.sort(function(a,b){return a.sort-b.sort;});
    featured();
    render();
  }).catch(function(){river.innerHTML='<p class="empty">The archive data failed to load. Refresh to try again.</p>';});
  q.addEventListener('input',function(){term=q.value.trim().toLowerCase();render();});
  document.querySelectorAll('.filters button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.filters button').forEach(function(x){x.classList.remove('on');x.setAttribute('aria-pressed','false');});
      b.classList.add('on');b.setAttribute('aria-pressed','true');family=b.getAttribute('data-f');render();
    });
  });
})();
