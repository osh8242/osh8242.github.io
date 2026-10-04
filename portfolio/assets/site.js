(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  let preferredTheme;
  try { preferredTheme = localStorage.getItem('portfolio-theme'); } catch (_) { /* Storage is optional. */ }
  if (preferredTheme === 'dark' || preferredTheme === 'light') root.dataset.theme = preferredTheme;
  const updateThemeButton = () => {
    const dark = root.dataset.theme === 'dark';
    themeButton?.setAttribute('aria-label', dark ? '밝은 테마로 전환' : '어두운 테마로 전환');
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#131c18' : '#f7f6f1');
  };
  updateThemeButton();
  themeButton?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('portfolio-theme', root.dataset.theme); } catch (_) { /* Continue without persistence. */ }
    updateThemeButton();
  });

  const filterButtons = document.querySelectorAll('[data-filter]');
  const rows = document.querySelectorAll('.project-row');
  filterButtons.forEach(button => button.addEventListener('click', () => {
    filterButtons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    let visibleCount = 0;
    rows.forEach(row => {
      const visible = button.dataset.filter === 'all' || row.dataset.category === button.dataset.filter;
      row.hidden = !visible;
      if (visible) visibleCount++;
    });
    document.querySelector('.project-count').textContent = `${visibleCount}개 프로젝트`;
  }));
})();
