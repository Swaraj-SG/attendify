// smooth scroll
document.querySelectorAll("a[href^='#']").forEach(a=>{
  a.addEventListener('click', function(e){
    const href = this.getAttribute('href');
    if(!href || href === '#' || href.startsWith('mailto:')) return;
    const target = document.querySelector(href);
    if(target){
      e.preventDefault();
      const navbarHeight = document.querySelector('.navbar').offsetHeight;
      const offsetTop = target.offsetTop - navbarHeight - 20; // extra 20px for spacing
      window.scrollTo({top: offsetTop, behavior: 'smooth'});
    }
  });
});


// tooltip on hover, 2sec
document.querySelectorAll('.btn, .socials a').forEach(el => {
  let timer;
  const tooltip = document.createElement('div');
  tooltip.className = 'tooltip';
  tooltip.textContent = el.textContent.trim() || el.querySelector('i')?.className || 'Button';
  document.body.appendChild(tooltip);

  el.addEventListener('mouseenter', (e) => {
    timer = setTimeout(() => {
      tooltip.style.left = e.pageX + 10 + 'px';
      tooltip.style.top = e.pageY - 10 + 'px';
      tooltip.style.opacity = '1';
    }, 2000);
  });

  el.addEventListener('mouseleave', () => {
    clearTimeout(timer);
    tooltip.style.opacity = '0';
  });

  el.addEventListener('mousemove', (e) => {
    tooltip.style.left = e.pageX + 10 + 'px';
    tooltip.style.top = e.pageY - 10 + 'px';
  });
});