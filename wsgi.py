from simple_fw.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server


application = Framework(routes, fronts)

with make_server("", 8080, application) as httpd:
    print("Server started at port 8000...")
    httpd.serve_forever()
