import re


class Product:
    def __init__(self, name, saving, lifetime, link, store):
        self.name = re.sub("^Ben .* Jerry('s)?", "", name)
        self.saving = saving
        self.lifetime = lifetime
        self.link = link
        self.store = store

    def __str__(self):
        return f"*\t{self.name}\n" \
               f"\t{self.saving}\n" \
               f"\t{self.lifetime}\n" \
               f"\t{self.link}\n"

    def get_card(self):
        return f'<a href={self.link} class="text-decoration-none">' \
               f'   <div class="card text-white bg-success">' \
               f'       <div class="row g-0">' \
               f'           <div class="col-md-8">' \
               f'               <div class="card-body">' \
               f'                   <h1 class="card-title display-4">{self.name}</h1>' \
               f'               </div>' \
               f'           </div>' \
               f'           <div class="col-md-4">' \
               f'               <div class="card-body text-end">' \
               f'                   <h4>{self.saving}</h4></br>' \
               f'                   <h4>{self.lifetime}</h4>' \
               f'               </div>' \
               f'           </div>' \
               f'       </div>' \
               f'   </div>' \
               f'</a>' \
