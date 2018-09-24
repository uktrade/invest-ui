(function() {
  var element = document.getElementById('contact-section');
  var paragraph = element.getElementsByTagName('p')[0];
  var hero = document.getElementById('hero');
  window.addEventListener('scroll', function(e) {
    if (window.innerWidth <= 375) {
      // deactivate for mobile.
      paragraph.style.display = 'block';
      return
    }
    var rect = hero.getBoundingClientRect();
    if (paragraph.style.display != 'none' && rect.bottom <= -50) {
      paragraph.style.display = 'none';
      window.scrollTo(0, document.documentElement.scrollTop + 50 )
    } else if (paragraph.style.display != 'block' && rect.bottom > 30) {
      paragraph.style.display = 'block';
    }
  });
})()
