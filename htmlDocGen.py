class HTML_Doc:

    def __init__(self, title):
        self.title = title
        self.body_content = ""

    def add_title(self, title):
        self.title = title
        self.body_content += f"<h1>{title}</h1>"

    def add_section(self, section_title, content):
        self.body_content += f"<h1>{section_title}</h1>\n<p>{content}</p>\n"
        
    def add_subsection(self, subsection_title, content):
        self.body_content += f"<h2>{subsection_title}</h2>\n<p>{content}</p>\n"

    def add_hn_header(self, header_title, header="h3", content=""):
        self.body_content += f"<{header}>{header_title}</{header}>\n<p>{content}</p>\n"

    def add_figure(self, fig_name):
        self.body_content += f"<figure>\n  <img src='{fig_name}' alt='{fig_name}'>\n  <figcaption>{fig_name}</figcaption>\n</figure>\n"

    def add_image(self, img_name):
        self.body_content += f"<img src='{img_name}' alt='{img_name}'>"

    def create_html_file(self):
        html_code = f"""
        <!DOCTYPE html>
        
        <html>
        
        <head>
        <title>{self.title}
        </title>
        </head>
        
        <body>
        {self.body_content}
        </body>\n
        
        </html>
        """
        self.html_code = html_code

    def write_html(self, filename=None):
        if not filename:
            filename = self.title
        with open(f"{filename}.html", "w") as file:
            file.write(self.html_code)
        return

def main():
    doc = HTML_Doc("Podalize")
    doc.add_title("This is a sample podalie title")
    doc.add_section("First section", "This is the content of the first section.")
    doc.add_subsection("First subsection", "This is the content of the first subsection.")
    #doc.add_figure("./data/usage.png")
    doc.add_image("./data/usage.png")
    html_code = doc.create_html_file()
    doc.write_html(html_code, filename="sample_podalize_doc")
    print("html doc was created!")

if __name__ == '__main__':
    main()
