from datetime import date
from simple_fw.renderer import render
from patterns.creational_patterns import Engine, Logger


site = Engine()
logger = Logger("main")



class Index:
    def __call__(self, request):
        return "200 OK", render("index.html", object_list=site.category)
    

class Elements:
    def __call__(self, request):
        return "200 OK", render("elements.html", folder="templates", data=request.get("date"))
    

class Courses:
    def __call__(self, request):
        logger.log('Список курсов')
        return '200 OK', render('courses.html')
        