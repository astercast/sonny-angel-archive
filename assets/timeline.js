(function(){
  var river=document.getElementById('river');
  var q=document.getElementById('q');
  var data=null, line='all', term='';
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function row(d){
    return '<article class="drop tl"><div class="plate"><span class="initial" aria-hidden="true">'+esc(d.name.charAt(0))+'</span></div><div class="dropbody">'
      +'<p class="dropdate">'+esc(d.display)+'</p>'
      +'<h3 class="dropname">'+esc(d.name)+'<span class="fam">'+esc(d.line)+'</span></h3>'
      +'<p>'+esc(d.scope)+'</p>'
      +'<p class="lineup"><b>Evidence '+esc(d.evidence)+'.</b> '+esc(d.source)+'.</p>'
      +'</div></article>';
  }
  function render(){
    if(!data)return;
    var list=data.entries.filter(function(d){
      if(line!=='all'&&d.line!==line)return false;
      if(!term)return true;
      var hay=(d.name+' '+d.scope+' '+d.display+' '+d.line).toLowerCase();
      return hay.indexOf(term)>-1;
    });
    if(!list.length){river.innerHTML='<p class="empty">Nothing matches that. Try a shorter word.</p>';return;}
    var html='',year=null;
    list.forEach(function(d){
      var y=d.year?String(d.year):'Year not stated';
      if(y!==year){if(year!==null)html+='</div></div>';year=y;
        html+='<div class="yearblock"><div class="year'+(d.year?'':' tl-year')+'" aria-label="Year '+esc(y)+'">'+esc(y)+'</div><div class="rows">';}
      html+=row(d);
    });
    html+='</div></div>';
    river.innerHTML=html;
    document.getElementById('count-line').textContent=
      'Showing '+list.length+' of '+data.meta.entries+' series lines, 2004 to today.';
  }
  fetch('data/v1/history.json').then(function(r){return r.json();}).then(function(j){
    data=j;render();
  }).catch(function(){river.innerHTML='<p class="empty">The timeline data failed to load. Refresh to try again.</p>';});
  q.addEventListener('input',function(){term=q.value.trim().toLowerCase();render();});
  document.querySelectorAll('.filters button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.filters button').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on');line=b.getAttribute('data-f');render();
    });
  });
})();
