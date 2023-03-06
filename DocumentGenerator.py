import os
import pandas as pd
from weasyprint import HTML

class DocumentGenerator:
    def __init__(self, **kwargs):
        self.path2logs = kwargs['path2logs']
        self.fig_count = 0
        self.html = f"<h1>{kwargs['title']}</h1><p><strong>{kwargs['author']}</strong></p>"
        
    def add_section(self, section_title, section_content=""):
        self.html += f"<h2>{section_title}</h2><p>{section_content}</p>"

    def add_sub_section(self, ss_title, ss_content):
        self.html += f"<h3>{ss_title}</h3><p>{ss_content}</p>"

    def add_image(self, filename, caption="", width='400px'):
        filename = os.path.abspath(filename)
        self.html += f'<img src="{filename}" width="{width}"/><p>{caption}</p>'
        self.fig_count += 1

    def add_new_page(self):
        self.html += '<div style="page-break-after: always;"></div>'

    def add_pandas_table(self, df):
        nr, nc = df.shape
        self.html += '<table><tr>'
        self.html += '<th></th>' + ''.join([f'<th>{col}</th>' for col in df.columns]) + '</tr>'
        for row in df.itertuples():
            self.html += '<tr>'
            self.html += f'<td>{row[0]}</td>' + ''.join([f'<td>{val}</td>' for val in row[1:]]) + '</tr>'
        self.html += '</table>'

    def add_new_lines(self, n=1):
        self.html += '<br/>' * n

    def save_pdf(self, output_file):
        HTML(string=self.html).write_pdf(output_file)
