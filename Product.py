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
        return f"<li><a class ='btn btn-primary m-2 p-2' href='{self.link}' role='button'>" \
               f"{self.name}" \
               f"<p>{self.saving}</p>" \
               f"<p>{self.lifetime}</p>" \
               "</a></li>"
