from flask import Flask, render_template, request, Response, abort, jsonify, make_response

from proxy import findAddress_with_failover

app = Flask(__name__)

@app.route('/')

def home():
	return render_template('index.html')

@app.route('/find/')
def find_address_args():
	if 'address' in request.args:
		address = request.args.get('address')
		if address: 
			return find_address(address)
		else: 
			abort (400)
	else:
		abort(400)

@app.route('/find/<string:address>')
def find_address(address):

	result=findAddress_with_failover(address)

	if result is not None:
		return Response(result.toJson(), status=200, mimetype='application/json')
	else:
		abort(404)


@app.errorhandler(400)
def required_error(error):
    return make_response(jsonify({'errors':[
	    	{'status':'400',
	    	'title':'Parameter required',
	    	'details':'The address parameter is required (and really important) to perform the geocoding search.'}
    	]}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'errors':[
	    	{'status':'404',
	    	'title':'Address not found',
	    	'details':'The address provided by the user was not found or no geocoding service provider were available.'}
    	]}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0')