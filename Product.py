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
        return f"<li><a href={self.link} class='button'>{self.name}</a>" \
               f"<p>{self.saving}</p>" \
               f"<p>{self.lifetime}</p>" \
               f"</li>"
