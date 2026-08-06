"""图鉴与徽章：把法则变成看得见的收藏。"""
from datetime import datetime


def badge_svg(law_name: str, solved_date: str | None = None, accent: str = "#a4763f") -> str:
    """用 Python 生成一枚法则徽章（SVG，暖纸×古铜）。"""
    date = solved_date or datetime.now().strftime("%Y-%m-%d")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="360" viewBox="0 0 300 360">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbf4e3"/>
      <stop offset="100%" stop-color="#efe2c6"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d9a441"/>
      <stop offset="100%" stop-color="#a4763f"/>
    </linearGradient>
  </defs>
  <rect width="300" height="360" rx="18" fill="url(#bg)"/>
  <path d="M150 40 L250 90 L250 190 Q250 250 150 310 Q50 250 50 190 L50 90 Z"
        fill="none" stroke="url(#gold)" stroke-width="3"/>
  <text x="150" y="175" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#8a6a34">已化解</text>
  <text x="150" y="225" text-anchor="middle" font-family="Georgia,serif" font-size="19" fill="#3a3126">{law_name}</text>
  <text x="150" y="338" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#9c8f76">{date}</text>
</svg>'''


def certificate_svg(law_names: list[str], date: str | None = None) -> str:
    """维修师之证：把化解过的法则写进一张毕业证（暖纸×古铜）。"""
    date = date or datetime.now().strftime("%Y-%m-%d")
    laws = " · ".join(law_names) if law_names else "（法则待填）"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="620" height="440" viewBox="0 0 620 440">
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbf4e3"/>
      <stop offset="100%" stop-color="#efe2c6"/>
    </linearGradient>
    <linearGradient id="cgold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#d9a441"/>
      <stop offset="100%" stop-color="#a4763f"/>
    </linearGradient>
  </defs>
  <rect width="620" height="440" rx="20" fill="url(#cbg)"/>
  <rect x="14" y="14" width="592" height="412" rx="14" fill="none" stroke="url(#cgold)" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="310" y="86" text-anchor="middle" font-family="Georgia,serif" font-size="34" fill="#8a6a34" letter-spacing="6">魔法维修师之证</text>
  <text x="310" y="130" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#9c8f76">—— 授予一名学会了倾听机器真话的人 ——</text>
  <text x="310" y="200" text-anchor="middle" font-family="sans-serif" font-size="17" fill="#6b5f4c">已化解法则：</text>
  <text x="310" y="252" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#3a3126">{laws}</text>
  <text x="310" y="330" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#9c8f76">{date}</text>
</svg>'''
