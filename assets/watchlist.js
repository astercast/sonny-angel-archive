(function(){
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  /* Dates in source notes read as words: 2026-10-15 becomes Oct 15, 2026. */
  var MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function plain(s){return String(s).replace(/(\d{4})-(\d{2})-(\d{2})/g,function(m,y,mo,d){return MON[+mo-1]+' '+(+d)+', '+y;}).replace(/ ; /g,'; ');}
  fetch('data/v1/watchlist.json').then(function(r){return r.json();}).then(function(j){
    document.getElementById('shops').innerHTML=j.retailers.map(function(s){
      return '<article class="shop"><p class="kind">'+esc(s.kind)+'</p>'
        +'<h2>'+esc(s.name)+'</h2>'
        +'<p><b>Watch for:</b> '+esc(s.watch_for)+'</p>'
        +'<a class="visit" aria-label="Visit '+esc(s.name)+'" href="'+esc(s.url)+'" rel="noopener">Visit the store</a></article>';
    }).join('');
    document.getElementById('not-listed').innerHTML=j.checked_not_listed.map(function(s){
      return '<p><b>'+esc(s.name)+'.</b> Checked '+esc(plain(s.checked))+'.</p>';
    }).join('');
  }).catch(function(){
    document.getElementById('shops').innerHTML='<p class="empty">The watchlist failed to load. Refresh to try again.</p>';
  });
})();
