from pylatex import Command
from pylatex.utils import NoEscape
from pylatex import Document, Section, Subsection, Figure, NewPage, NewLine, Tabular
from myutils import *

class DocumentGenerator:
    def __init__(self, **kwargs):
        self.path2logs = kwargs['path2logs']
        self.fig_count = 0
        self.doc = Document()
        self.doc.preamble.append(Command('title', kwargs['title']))
        self.doc.preamble.append(Command('author', kwargs['author']))
        self.doc.preamble.append(Command('date', NoEscape(r'\today')))
        self.doc.append(NoEscape(r'\maketitle'))

    def add_section(self, section_title, section_content=""):
        with self.doc.create(Section(section_title)):
            self.doc.append(section_content)

    def add_sub_section(self,ss_title, ss_content):
        with self.doc.create(Subsection(ss_title)):
            self.doc.append(ss_content)

    def add_image(self, filename, caption="", width='400px'):
        filename = os.path.abspath(filename)
        with self.doc.create(Figure(position='h!')) as pic:
            self.doc.append(Command('centering'))
            pic.add_image(filename, width=width)
            pic.add_caption(caption)
        self.fig_count += 1
    def add_new_page(self):
        self.doc.append(NewPage())

    def add_pandas_table(self, df):
        nr, nc = df.shape
        with self.doc.create(Tabular('c'*(nc+1), pos='centering', row_height=2)) as table:
            table.add_hline()
            table.add_row([""] +list(df.columns))
            table.add_hline()
            for row in df.index:
                table.add_row([row] + list(df.loc[row,:]))
            table.add_hline()

    def add_new_lines(self, n=1):
        for _ in range(n):
            self.doc.append(NewLine())
