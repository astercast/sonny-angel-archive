(function(){
  var river=document.getElementById('river');
  var q=document.getElementById('q');
  var data=null, line='before', term='';
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  /* Dates in source notes read as words: 2026-10-15 becomes Oct 15, 2026. */
  var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function plain(s){return String(s).replace(/(\d{4})-(\d{2})-(\d{2})/g,function(m,y,mo,d){return MON[+mo-1]+' '+(+d)+', '+y;}).replace(/ ; /g,'; ');}
  function plate(d){
    if(d.image){return '<div class="plate"><img src="'+esc(d.image)+'" alt="Official product photo, '+esc(d.name)+'" loading="lazy" onerror="this.parentNode.innerHTML=\'<span class=&quot;initial&quot; aria-hidden=&quot;true&quot;>'+esc(d.name.charAt(0))+'</span>\'"></div>';}
    return '<div class="plate"><span class="initial" aria-hidden="true">'+esc(d.name.charAt(0))+'</span></div>';
  }
  function row(d){
    return '<article class="drop tl"><div>'+plate(d)+'</div><div class="dropbody">'
      +'<p class="dropdate">'+esc(d.display)+'</p>'
      +'<h3 class="dropname">'+esc(d.name)+'<span class="fam">'+esc(d.line)+'</span></h3>'
      +'<p>'+esc(d.scope)+'</p>'
      +'<p class="lineup"><b>Source.</b> '+esc(plain(d.source))+'.</p>'
      +'</div></article>';
  }
  function render(){
    if(!data)return;
    var list=data.entries.filter(function(d){
      if(line==='before'){if(!(d.year&&d.year<2019))return false;}
      else if(line!=='all'&&d.line!==line)return false;
      if(!term)return true;
      var hay=(d.name+' '+d.scope+' '+d.display+' '+d.line).toLowerCase();
      return hay.indexOf(term)>-1;
    });
    var cl=document.getElementById('count-line');
    if(!list.length){
      river.innerHTML='<p class="empty" role="status">Nothing matches that. <button type="button" class="clearall">Show everything</button></p>';
      cl.textContent='Showing 0 of '+data.meta.entries+' series lines, 2004 to today.';
      river.scrollIntoView({block:'nearest'});
      return;
    }
    var html='',year=null;
    list.forEach(function(d){
      var y=d.year?String(d.year):'Year not stated';
      if(y!==year){if(year!==null)html+='</div></div>';year=y;
        html+='<div class="yearblock"><div class="year'+(d.year?'':' tl-year')+'" aria-label="Year '+esc(y)+'">'+esc(y)+'</div><div class="rows">';}
      html+=row(d);
    });
    html+='</div></div>';
    river.innerHTML=html;
    cl.textContent=
      'Showing '+list.length+' of '+data.meta.entries+' series lines, 2004 to today.';
  }
  river.addEventListener('click',function(e){
    if(e.target.classList&&e.target.classList.contains('clearall')){
      q.value='';term='';line='all';
      document.querySelectorAll('.filters button').forEach(function(x){var on=x.getAttribute('data-f')==='all';x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false');});
      render();q.focus();
    }
  });
  fetch('data/v1/history.json').then(function(r){return r.json();}).then(function(j){
    data=j;render();
  }).catch(function(){river.innerHTML='<p class="empty">The timeline data failed to load. Refresh to try again.</p>';});
  q.addEventListener('input',function(){term=q.value.trim().toLowerCase();render();});
  document.querySelectorAll('.filters button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.filters button').forEach(function(x){x.classList.remove('on');x.setAttribute('aria-pressed','false');});
      b.classList.add('on');b.setAttribute('aria-pressed','true');line=b.getAttribute('data-f');render();
    });
  });
})();
