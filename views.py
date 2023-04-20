from simple_fw.renderer import render


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html", date=request.get("date"))
    

class Elements:
    def __call__(self, request):
        return "200 OK", render("elements.html", folder="templates", data=request.get("date"))