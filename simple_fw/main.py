from quopri import decodestring
from simple_fw.renderer import render
from simple_fw.requests import *


class PageNotFound404:

    def __call__(self, request):
        return "404 Not found", render("error404.html")
    

class Framework:
    """
    _summary_
    Main loop of framework
    """

    def __init__(self, routes_obj, fronts_obj):
        self.routes_obj = routes_obj
        self.fronts_obj = fronts_obj

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]

        if not path.endswith("/"):
            path = f"{path}/"

        if path in self.routes_obj:
            view = self.routes_obj[path]
        else:
            view = PageNotFound404()

        request = {}
        
        # Get request method
        method = environ["REQUEST_METHOD"]
        request["method"] = method

        if method == "POST":
            data = PostRequest().get_request_params(environ)
            request["data"] = Framework.decode_value(data)
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
        elif method == "GET":
            request_params = GetRequests().get_request_params(environ)
            request["request_params"] = request_params
            print(f'Нам пришли GET-параметры:'
                    f' {Framework.decode_value(request_params)}')

        for front in self.fronts_obj:
            front(request)

        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])

        return [body.encode("utf-8")]
    
    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
    

# Логирующий WSGI-Application
class DebugApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']