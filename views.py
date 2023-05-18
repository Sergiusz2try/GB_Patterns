from datetime import date
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier
from patterns.structural_patterns import AppRoute, Debug
from simple_fw.renderer import render
from patterns.creational_patterns import Engine, Logger


site = Engine()
logger = Logger("main")
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}


@AppRoute(routes=routes, url="/")
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return "200 OK", render("index.html", object_list=site.category)
    

@AppRoute(routes=routes, url="/elements/")
class Elements:
    @Debug(name='Elements')
    def __call__(self, request):
        return "200 OK", render("elements.html", folder="templates", data=request.get("date"))
    

@AppRoute(routes=routes, url="/courses/")
class Courses:
    @Debug(name='Courses')
    def __call__(self, request):
        logger.log('Список курсов')
        return '200 OK', render('courses.html')
        