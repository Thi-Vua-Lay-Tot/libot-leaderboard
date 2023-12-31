import re
import os
import os.path
import logging
import logging.handlers
import datetime
import subprocess
import sys


css_styles = """
<head>
  <title> Lichess - Bảng xếp hạng </title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script async src="https://stats.chessnibble.com/script.js" data-website-id="8205b599-208b-4d50-be05-5a4bb2f3775d"></script>
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
  <link rel="icon" href="https://raw.githubusercontent.com/Thi-Vua-Lay-Tot/thi-vua-lay-tot.github.io/main/images/favicon.ico" type="image/x-icon" />
  <header>
        <nav>
              <a href="https://thi-vua-lay-tot.github.io/libot-leaderboard/">< Quay lại</a>
        </nav>
  </header>
  <style>
    .styled-table {
      font-family: "Raleway", sans-serif;
      border-collapse: collapse;
      width: 100%;
      border: 1px solid #ddd;
      font-size: 16px;
    }
    .styled-table th, .styled-table td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    .styled-table th {
      background-color: #f0A51;
    }
    body {
      margin-bottom: 70px;
    }
    .github-logo {
      width: 1.5em;
      height: auto;
      vertical-align: middle;
    }
    footer {
      font-family: "Raleway", sans-serif;
      background-color: #04FFf0;
      padding: 5px;
      margin-left: auto;
      margin-top: auto;
      position: fixed;
      bottom: 0;
      right: 0;
      width: 100%;
    }
  </style>
</head>
"""

footer_styles = """
<footer align="center">
  <p>
      <a href="https://www.youtube.com/@TungJohnPlayingChess"><img src="https://img.shields.io/badge/-Youtube-EA4335?style=flat-square&logo=Youtube&logoColor=white" target="_blank"></a>
      <a href="https://clubs.chess.com/GkQy"> <img src="https://img.shields.io/badge/-Chess.com-11111?logo=chess.com&logoColor=11111" target="_blank"> </a>
      <a href="https://lichess.org/team/thi-vua-lay-tot-tungjohn-playing-chess"><img src="https://img.shields.io/badge/-Lichess-050505?style=flat-square&logo=Lichess&logoColor=white" target="_blank"></a>
      <a href="https://lishogi.org/team/thi-vua-lay-tot-tungjohn-playing-shogi"><img src="https://img.shields.io/badge/-Lishogi-050505?style=flat-square&logo=Lishogi&logoColor=white" target="_blank"></a>
      <a href="https://lidraughts.org/team/thi-vua-lay-quan-tungjohn-playing-draughts"><img src="https://img.shields.io/badge/-Lidraughts-050505?style=flat-square&logo=Lidraughts&logoColor=white" target="_blank"></a>
      <a href="https://playstrategy.org/team/thi-vua-lay-tot-tungjohn-playing-chess"><img src="https://img.shields.io/badge/-PlayStrategy-050505?style=flat-square&logo=PlayStrategy&logoColor=white" target="_blank"></a>
      <a href="https://www.facebook.com/TungJohn2005"><img src="https://img.shields.io/badge/-Facebook-00B2FF?style=flat-square&logo=Facebook&logoColor=white" target="_blank"> </a>
      <a href="https://discord.gg/7vYq2gRCrv"><img src="https://dcbadge.vercel.app/api/server/7vYq2gRCrv?style=flat" target="_blank"> </a>
  </p>
  <p>
    <a href="https://github.com/Thi-Vua-Lay-Tot/libot-leaderboard">
      <img class="github-logo" src="https://github.com/fluidicon.png" alt="GitHub Icon">
    </a>
    Tạo bởi <a href="https://github.com/M-DinhHoangViet">Đinh Hoàng Việt</a>
  </p>
</footer>
"""

def generate_h1_tag(filename):
    title = os.path.splitext(filename)[0].capitalize()
    utc_datetime = datetime.datetime.utcnow()
    h1_tag = f"""<h1 align="center">Bảng xếp hạng {title}</h1>
    <p><i>Lần cuối cập nhật: {utc_datetime.hour}:{utc_datetime.minute}:{utc_datetime.second} UTC, ngày {utc_datetime.day} tháng {utc_datetime.month} năm {utc_datetime.year}</i></p>"""
    return h1_tag

def markdown_table_to_html(markdown_table):
    rows = markdown_table.strip().split('\n')
    html_table = '<table class="styled-table">\n'
    for i, row in enumerate(rows):
        if '---|---|---' in row:
            continue

        tag = 'th' if i == 0 else 'td'
        cells = re.split(r'\s*\|\s*', row)

        if len(cells) == 1 and cells[0] == '':
            continue
        
        html_table += '  <tr>\n'
        for cell in cells:
            if cell.startswith('@'):
                username = cell[1:]
                cell_content = f'<{tag}><a href="https://lichess.org/@/{username}">{cell}</a></{tag}>'
            else:
                cell_content = f'<{tag}>{cell}</{tag}>'
            html_table += f'    {cell_content}\n'
        html_table += '  </tr>\n'
    html_table += '</table>'
    return html_table

directories = ['html']

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            with open(os.path.join(directory, filename), 'r') as md_file:
                if filename not in ['chess960.md', 'threeCheck.md', 'kingOfTheHill.md', 'racingKings.md']:
                    f = filename
                elif filename in ["chess960.md"]:
                    f = "chess 960.md"
                elif filename in ["threeCheck.md"]:
                    f = "three-check.md"
                elif filename in ["kingOfTheHill.md"]:
                    f = "king of the hill.md"
                else:
                    f = "racing kings.md"
                h1_tag = generate_h1_tag(f)

                markdown_table = md_file.read()
                html_table = markdown_table_to_html(markdown_table)

                styled_html_table = css_styles + h1_tag + html_table + footer_styles

                html_filename = os.path.splitext(filename)[0] + '.html'
                with open(os.path.join(directory, html_filename), 'w') as html_file:
                    html_file.write(styled_html_table)
