"""Generate a dependency-free portfolio from the public-safe content source."""
import json
import struct
from html import escape as e
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent
ROOT = REPO / "portfolio"
DATA = json.loads((REPO / "content.json").read_text(encoding="utf-8"))


def redirect(path, destination, canonical_path):
    """Preserve old bookmarks, including their query string and section anchor."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>포트폴리오 주소 안내 | 오승환</title>
  <link rel="canonical" href="https://osh8242.github.io/{canonical_path}">
  <script>location.replace({json.dumps(destination)} + location.search + location.hash);</script>
  <meta http-equiv="refresh" content="0; url={e(destination, quote=True)}">
</head>
<body>
  <h1>포트폴리오 주소가 변경되었습니다.</h1>
  <p><a href="{e(destination, quote=True)}">새 포트폴리오로 이동</a></p>
</body>
</html>''', encoding="utf-8")

ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'


def shell(title, description, body, prefix="", project=False):
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(description, quote=True)}">
  <meta name="theme-color" content="#f5f4ef">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title, quote=True)}">
  <meta property="og:description" content="{e(description, quote=True)}">
  <title>{e(title)}</title>
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">본문으로 바로 가기</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{prefix}index.html" aria-label="오승환 포트폴리오 홈"><span class="brand-mark">OS<span>.</span></span><span class="brand-name">오승환</span></a>
      <nav aria-label="주요 메뉴">
        <a href="{prefix}index.html#about">소개</a>
        <a href="{prefix}index.html#projects"{' aria-current="page"' if project else ''}>프로젝트</a>
        <a href="{prefix}index.html#stack">기술</a>
        <a href="{prefix}index.html#contact">연락</a>
      </nav>
      <button class="theme-toggle" type="button" aria-label="어두운 테마로 전환" title="테마 전환">{SUN}</button>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer wrap"><a class="brand-mark" href="{prefix}index.html" aria-label="홈">OS<span>.</span></a><p>오승환 · 데이터 플랫폼 백엔드 개발자</p><a href="{DATA['github']}" target="_blank" rel="noopener noreferrer">GitHub {ICON}</a></footer>
</body>
</html>'''


def chips(tech):
    return '<ul class="chips" aria-label="사용 기술">' + ''.join(f'<li>{e(t)}</li>' for t in tech) + '</ul>'


def skill_grid():
    parts = []
    for skill in DATA["skills"]:
        src = f"https://img.shields.io/badge/{quote(skill['name'], safe='')}-{skill['color']}?style=flat-square&logo={skill['logo']}&logoColor=white"
        parts.append(f'''<li class="skill-item"><span class="skill-number">0{len(parts)+1}</span><div><img src="{src}" alt="{e(skill['name'])}" loading="lazy" height="24"><p>{e(skill['description'])}</p></div></li>''')
    return '<ul class="skill-grid">' + ''.join(parts) + '</ul>'


def home():
    projects = ''
    for p in DATA["projects"]:
        projects += f'''<article class="project-row" data-category="{p['category']}">
          <span class="project-number">{p['number']}</span>
          <div class="project-overview">
            <div class="project-meta"><span>{e(p['categoryLabel'])}</span><span>{e(p['period'])}</span></div>
            <h3><a href="projects/{p['slug']}.html">{e(p['title'])}</a></h3>
            <p>{e(p['summary'])}</p>
            {chips(p['tech'])}
          </div>
          <a class="project-open" href="projects/{p['slug']}.html" aria-label="{e(p['title'])} 상세 보기">{ICON}</a>
        </article>'''
    responsibilities = ''.join(f'<div class="responsibility"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>' for t,d in DATA["responsibilities"])
    filters = ''.join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{label}</button>' for k,label in [('all','전체'),('platform','데이터 플랫폼'),('async','비동기 처리'),('performance','성능·정확성'),('ai','AI·외부 연동')])
    body = f'''
    <section class="hero wrap" aria-labelledby="hero-title">
      <div class="hero-copy">
        <p class="eyebrow"><span class="status-dot"></span> DATA PLATFORM / BACKEND ENGINEER</p>
        <h1 id="hero-title">데이터의 흐름을 읽고,<br>서비스의 구조를<br><span>만듭니다.</span></h1>
        <p class="hero-description">복잡한 업무 규칙과 데이터 흐름을<br class="desktop-break"> Java/Spring 서비스로 구현하는 개발자, <strong>오승환</strong>입니다.</p>
        <div class="hero-actions"><a class="button primary" href="#projects">프로젝트 살펴보기 {ARROW}</a><a class="text-link" href="{DATA['github']}" target="_blank" rel="noopener noreferrer">GitHub {ICON}</a></div>
      </div>
      <aside class="hero-note" aria-label="주요 개발 분야">
        <div class="note-top"><span>ENGINEERING FOCUS</span><span class="note-dot"></span></div>
        <p class="note-title">데이터를 다루는<br>서비스의 안쪽.</p>
        <ul class="focus-list"><li><span>01</span>고객사별 데이터 경계</li><li><span>02</span>오래 걸리는 작업의 상태</li><li><span>03</span>조회 성능과 결과 정확성</li><li><span>04</span>외부 시스템과의 연결</li></ul>
        <div class="note-bottom"><span>JAVA · SPRING BOOT</span><span>OS / PORTFOLIO</span></div>
      </aside>
    </section>
    <section id="about" class="about-section wrap" aria-labelledby="about-title">
      <div class="section-label"><span class="eyebrow">01 / ABOUT</span><h2 id="about-title">경력 요약</h2></div>
      <div class="about-content"><p class="about-lead">{e(DATA['career'])}</p><p class="about-voice">{e(DATA['intro'])}</p><dl class="responsibilities">{responsibilities}</dl></div>
    </section>
    <section id="projects" class="projects-section wrap" aria-labelledby="projects-title">
      <div class="section-top"><div><p class="eyebrow">02 / SELECTED WORK</p><h2 id="projects-title">문제를 풀어낸 과정</h2></div><p class="section-aside">설계, 구현, 그리고 결과 검증.<br>직접 맡은 범위와 판단을 담았습니다.</p></div>
      <div class="filter-bar"><div class="project-filters" role="group" aria-label="프로젝트 분야 선택">{filters}</div><span class="project-count" aria-live="polite">6개 프로젝트</span></div>
      <div class="project-list">{projects}</div>
    </section>
    <section id="stack" class="stack-section wrap" aria-labelledby="stack-title"><div class="section-top"><div><p class="eyebrow">03 / TECH STACK</p><h2 id="stack-title">기술을 사용한 맥락</h2></div><p class="section-aside">어떤 일을 위해 사용했는지 함께 적었습니다.</p></div>{skill_grid()}</section>
    <section id="contact" class="contact-section wrap" aria-labelledby="contact-title"><p class="eyebrow">04 / CONTACT</p><div class="contact-inner"><div><h2 id="contact-title">더 자세한 이야기는<br><span>여기에서.</span></h2><p>프로젝트와 개발 경험에 대해 이야기 나눌 수 있습니다.</p></div><div class="contact-links"><a href="mailto:{DATA['email']}"><span><small>EMAIL</small>{DATA['email']}</span>{ARROW}</a><a href="{DATA['github']}" target="_blank" rel="noopener noreferrer"><span><small>GITHUB</small>github.com/osh8242</span>{ICON}</a><a href="{DATA['notion']}" target="_blank" rel="noopener noreferrer"><span><small>NOTION</small>포트폴리오 원문</span>{ICON}</a></div></div></section>'''
    (ROOT / "index.html").write_text(shell("오승환 | 데이터 플랫폼 백엔드 개발자", DATA["career"], body), encoding="utf-8")


def section_html(section):
    result = f'<section class="case-section" id="{section["id"]}"><h2>{e(section["title"])}</h2>'
    result += ''.join(f'<p>{e(p)}</p>' for p in section.get('paragraphs', []))
    if section.get('items'):
        result += '<ul>' + ''.join(f'<li>{e(item)}</li>' for item in section['items']) + '</ul>'
    if section.get('table'):
        rows=section['table']
        result += '<div class="table-scroll"><table><thead><tr>' + ''.join(f'<th scope="col">{e(cell)}</th>' for cell in rows[0]) + '</tr></thead><tbody>'
        result += ''.join('<tr>'+''.join(f'<td>{e(cell)}</td>' for cell in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>'
    if section.get('note'):
        result += f'<p class="case-note">{e(section["note"])}</p>'
    return result + '</section>'


def project_page(p, next_project):
    preview = p['diagram'].replace('.html', '.png')
    image_width, image_height = struct.unpack('>II', (ROOT/'assets'/'diagrams'/preview).read_bytes()[16:24])
    sections=''.join(section_html(section) for section in p['sections'])
    toc=''.join(f'<li><a href="#{s["id"]}">{e(s["title"])}</a></li>' for s in p['sections'])
    body=f'''
    <section class="case-hero wrap">
      <a href="../index.html#projects" class="back-link">← 모든 프로젝트</a>
      <p class="eyebrow">PROJECT {p['number']} / {e(p['categoryLabel'])}</p>
      <h1>{e(p['title'])}</h1>
      <p class="case-intro">{e(p['intro'])}</p>
      <dl class="case-facts"><div><dt>기간</dt><dd>{e(p['period'])}</dd></div><div><dt>담당 역할</dt><dd>{e(p['role'])}</dd></div></dl>
      {chips(p['tech'])}
    </section>
    <div class="case-layout wrap">
      <aside class="case-toc"><p class="eyebrow">IN THIS PROJECT</p><nav aria-label="프로젝트 목차"><ol>{toc}<li><a href="#diagram">처리 흐름</a></li></ol></nav><a class="text-link" href="{p['notion']}" target="_blank" rel="noopener noreferrer">노션 원문 {ICON}</a></aside>
      <div class="case-body">{sections}
        <section class="case-section diagram-section" id="diagram"><h2>{e(p['diagramTitle'])}</h2><p>{e(p['diagramCaption'])}</p><figure class="diagram-frame"><a class="diagram-preview" href="../assets/diagrams/{p['diagram']}" target="_blank" rel="noopener noreferrer" aria-label="{e(p['diagramTitle'])} 확대·탐색"><img src="../assets/diagrams/{preview}" alt="{e(p['diagramTitle'])} 전체 흐름" width="{image_width}" height="{image_height}" loading="lazy"></a><figcaption>전체 흐름을 먼저 보고, 세부 내용은 확대해서 확인할 수 있습니다.<a href="../assets/diagrams/{p['diagram']}" target="_blank" rel="noopener noreferrer">다이어그램 확대·탐색 {ICON}</a></figcaption></figure></section>
        <div class="next-project"><span class="eyebrow">NEXT PROJECT</span><a href="{next_project['slug']}.html">{e(next_project['title'])} {ARROW}</a></div>
      </div>
    </div>'''
    out=ROOT/'projects'/f'{p["slug"]}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(shell(f'{p["title"]} | 오승환', p['summary'], body, '../', True), encoding='utf-8')


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=True)
    home()
    for index, project in enumerate(DATA['projects']):
        project_page(project, DATA['projects'][(index+1)%len(DATA['projects'])])
        redirect(REPO/'projects'/f'{project["slug"]}.html', f'../portfolio/projects/{project["slug"]}.html', f'portfolio/projects/{project["slug"]}.html')
        redirect(REPO/'assets'/'diagrams'/project['diagram'], f'../../portfolio/assets/diagrams/{project["diagram"]}', f'portfolio/assets/diagrams/{project["diagram"]}')
    redirect(REPO/'index.html', 'portfolio/', 'portfolio/')
    redirect(REPO/'portpolio'/'index.html', '../portfolio/', 'portfolio/')
    print('Built /portfolio/ with 6 project pages and redirects for old URLs.')
