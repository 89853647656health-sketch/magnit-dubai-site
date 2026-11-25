import http.server, functools, os, sys
CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self'; font-src 'self'; connect-src 'self' https://script.google.com https://script.googleusercontent.com https://magnit-shop-dcoe.onrender.com wss://generativelanguage.googleapis.com" + os.environ.get('MAGNIT_CSP_CONNECT_EXTRA', '') + "; frame-ancestors 'none'; base-uri 'self'; form-action 'none'; object-src 'none'"
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Security-Policy', CSP); self.send_header('X-Content-Type-Options', 'nosniff'); super().end_headers()
    def log_message(self, *a): pass
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8811), functools.partial(H, directory=d)).serve_forever()
