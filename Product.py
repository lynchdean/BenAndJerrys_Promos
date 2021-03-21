class Product:
    def __init__(self, name, saving, lifetime, link, store):
        self.name = name
        self.saving = saving
        self.lifetime = lifetime
        self.link = link
        self.store = store

    def __str__(self):
        return f"*\t{self.name}\n" \
               f"\t{self.saving}\n" \
               f"\t{self.lifetime}\n" \
               f"\t{self.link}\n"

    def get_html(self):
        return "<style> .a {width: 100%;}</style>" \
               f"<a href={self.link}><button type='button' class='block'>" \
               f"<li>{self.name}" \
               f"<p>{self.saving}</p>" \
               f"<p>{self.lifetime}</p>" \
               "</li></button></a>"
