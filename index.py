'''
                                                                                                                                                                                                                                                                                                                                     
 _|_|_|      _|_|_|    _|_|_|        _|_|_|  _|      _|    _|_|    _|_|_|    _|_|_|_|_|      _|      _|    _|_|    _|_|_|  _|      _|  _|_|_|_|_|  _|_|_|_|  _|      _|    _|_|    _|      _|    _|_|_|  _|_|_|_|        _|_|    _|_|_|    _|_|_|    _|        _|_|_|    _|_|_|    _|_|    _|_|_|_|_|  _|_|_|    _|_|    _|      _|  
 _|    _|  _|        _|            _|        _|_|  _|_|  _|    _|  _|    _|      _|          _|_|  _|_|  _|    _|    _|    _|_|    _|      _|      _|        _|_|    _|  _|    _|  _|_|    _|  _|        _|            _|    _|  _|    _|  _|    _|  _|          _|    _|        _|    _|      _|        _|    _|    _|  _|_|    _|  
 _|_|_|      _|_|    _|  _|_|        _|_|    _|  _|  _|  _|_|_|_|  _|_|_|        _|          _|  _|  _|  _|_|_|_|    _|    _|  _|  _|      _|      _|_|_|    _|  _|  _|  _|_|_|_|  _|  _|  _|  _|        _|_|_|        _|_|_|_|  _|_|_|    _|_|_|    _|          _|    _|        _|_|_|_|      _|        _|    _|    _|  _|  _|  _|  
 _|              _|  _|    _|            _|  _|      _|  _|    _|  _|    _|      _|          _|      _|  _|    _|    _|    _|    _|_|      _|      _|        _|    _|_|  _|    _|  _|    _|_|  _|        _|            _|    _|  _|        _|        _|          _|    _|        _|    _|      _|        _|    _|    _|  _|    _|_|  
 _|        _|_|_|      _|_|_|      _|_|_|    _|      _|  _|    _|  _|    _|      _|          _|      _|  _|    _|  _|_|_|  _|      _|      _|      _|_|_|_|  _|      _|  _|    _|  _|      _|    _|_|_|  _|_|_|_|      _|    _|  _|        _|        _|_|_|_|  _|_|_|    _|_|_|  _|    _|      _|      _|_|_|    _|_|    _|      _|  
                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                     
WebApplication to report College Facility Maintenance
BY AADITYA RENGARAJAN
CREATION TIMESTAMP : 22:53 12/22/21 22 12 2021
[TO-DO]
- Change Flask Port
- Remove Debuggers on Production Deployment
'''
#==============IMPORTING MODULES======================================================
#/- see 'requirements.txt' to install extra modules via pip
from flask import redirect, render_template, Flask, request, make_response, send_file
from modules import qrgen

#==============DEFINING BASIC FUNCTIONS======================================================
app = Flask(__name__)
#==============ROUTES======================================================
#/- routes are defined by @app.route decorator



@app.route('/')
def index():
    if request.args.get("options")==None:
        return render_template("index.html")
    else:
        qrgen.makeresult(request.args.get("options"),
            {"block": request.args.get("block"),
                "floor": request.args.get("floor"),
                "room" : request.args.get("room"),
                "department" : request.args.get("department"),
                "dispenser_no" : request.args.get("dispenser")})
        with open('qrcode_result.pdf', 'rb') as f:
            file_content = f.read()
        response = make_response(file_content, 200)
        response.headers['Content-Disposition'] = f'attachment; filename="QR_{request.args.get("options").upper()}_{request.args.get("block")}{request.args.get("floor")}.pdf"'
        response.headers['Content-type'] = 'application/pdf'
        return response   
        return send_file("qrcode_result.pdf", mimetype='application/pdf', as_attachment=False)


#==============ERROR HANDLING======================================================
#/- custom error handling using custom template to get fancy ;)

@app.errorhandler(404)
def page_not_found(e):
    return str((render_template('error.html',
                code="404",
                type="Not Found",
                content="Sorry, this page was not found!"))), 404

@app.errorhandler(500)
def internal_server_error(e):
    return str((render_template('error.html',
                code="500",
                type="Internal Server Error",
                content=f"Oh No! Something Went Wrong!<br/>{e}"))), 500

@app.errorhandler(410)
def gone(e):
    return str((render_template('error.html',
                code="410",type="Gone",
                content="Sorry, this page is has mysteriously vanished!"))), 410

@app.errorhandler(403)
def forbidden(e):
    return str((render_template('error.html',
                code="403",
                type="Forbidden",
                content="Sorry, you are not allowed to access this page!"))), 403

@app.errorhandler(401)
def unauthorized(e):
    return str((render_template('error.html',
                code="401",
                type="Unauthorized",
                content="Sorry, you are not authorized to access this page!"))), 401
#==============PROGRAM RUN======================================================
if __name__=="__main__":
    #/- note : remove debuggers and change port respectively
    #/- on production deployment.
    app.run(
        debug=True,
        use_reloader=True,
        use_debugger=True,
        port=7500,
	host='0.0.0.0',
        use_evalex=True,
        threaded=True,
        passthrough_errors=False
        )
#==============END OF WEBAPP======================================================
