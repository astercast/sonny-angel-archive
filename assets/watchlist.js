(function(){
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  fetch('data/v1/watchlist.json').then(function(r){return r.json();}).then(function(j){
    document.getElementById('shops').innerHTML=j.retailers.map(function(s){
      return '<article class="shop"><p class="kind">'+esc(s.kind)+'</p>'
        +'<h2>'+esc(s.name)+'</h2>'
        +'<p><b>Watch for:</b> '+esc(s.watch_for)+'</p>'
        +'<a class="visit" href="'+esc(s.url)+'" rel="noopener">Visit the store</a></article>';
    }).join('');
    document.getElementById('not-listed').innerHTML=j.checked_not_listed.map(function(s){
      return '<p><b>'+esc(s.name)+'.</b> Checked '+esc(s.checked)+'.</p>';
    }).join('');
  }).catch(function(){
    document.getElementById('shops').innerHTML='<p class="empty">The watchlist failed to load. Refresh to try again.</p>';
  });
})();
