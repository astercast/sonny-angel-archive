(function(){
  var river=document.getElementById('river');
  var q=document.getElementById('q');
  var data=null, family='all', term='';
  function ebay(d){return 'https://www.ebay.com/sch/i.html?_nkw='+encodeURIComponent(d.ebay_query);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function plate(d){
    if(d.image){return '<div class="plate"><img src="'+esc(d.image)+'" alt="Official product photo, '+esc(d.name)+'" loading="lazy" onerror="this.parentNode.innerHTML=\'<span class=&quot;initial&quot; aria-hidden=&quot;true&quot;>'+esc(d.name.charAt(0))+'</span>\'"></div>';}
    return '<div class="plate"><span class="initial" aria-hidden="true">'+esc(d.name.charAt(0))+'</span></div><p class="nophoto">No photo yet.</p>';
  }
  function row(d){
    return '<article class="drop"><div>'+plate(d)+'</div><div class="dropbody">'
      +'<p class="dropdate">'+esc(d.display_date)+'</p>'
      +'<h3 class="dropname">'+esc(d.name)+'<span class="fam">'+esc(d.family)+'</span></h3>'
      +'<p>'+esc(d.theme)+'</p>'
      +'<p class="lineup"><b>Lineup.</b> '+esc(d.lineup)+'</p>'
      +'<p class="secretline"><b>Secret.</b> '+esc(d.secret)+'</p>'
      +'<a class="ebay" href="'+ebay(d)+'" rel="noopener">Search eBay for this series</a>'
      +'</div></article>';
  }
  function render(){
    if(!data)return;
    var list=data.drops.filter(function(d){
      if(family!=='all'&&d.family!==family)return false;
      if(!term)return true;
      var hay=(d.name+' '+d.theme+' '+d.lineup+' '+d.display_date+' '+d.family).toLowerCase();
      return hay.indexOf(term)>-1;
    });
    if(!list.length){river.innerHTML='<p class="empty">Nothing matches that. Try a shorter word.</p>';return;}
    var html='',year=null;
    list.forEach(function(d){
      var y=String(d.sort).slice(0,4);
      if(y!==year){if(year!==null)html+='</div></div>';year=y;
        html+='<div class="yearblock"><div class="year" aria-label="Year '+y+'">'+y+'</div><div class="rows">';}
      html+=row(d);
    });
    html+='</div></div>';
    river.innerHTML=html;
    document.getElementById('count-line').textContent=
      'Showing '+list.length+' of '+data.meta.catalogued+' releases.';
  }
  fetch('data/v1/drops.json').then(function(r){return r.json();}).then(function(j){
    data=j;data.drops.sort(function(a,b){return a.sort-b.sort;});
    render();
  }).catch(function(){river.innerHTML='<p class="empty">The archive data failed to load. Refresh to try again.</p>';});
  q.addEventListener('input',function(){term=q.value.trim().toLowerCase();render();});
  document.querySelectorAll('.filters button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.filters button').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on');family=b.getAttribute('data-f');render();
    });
  });
})();
