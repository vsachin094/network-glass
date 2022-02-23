from flask import Flask, request, Response, render_template
import ssh_client
import helpers
import json
import routers

app = Flask(__name__, static_url_path='/static')

# main route where we render the html
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# GET route in order to fetch the available routers for a given ASN
@app.route('/routers/<asn>', methods=['GET'])
def get_routers(asn):
  results = []
  for r in routers.routers_list:
    if r['asn'] == asn:
      # only return the address/hostname, the location and the OS type of the matching routers
    #   results.append(dict(name=r['address'][0],
    #                       location=r['address'],
    #                       type=r['type'])
    #   )
        router=r['address'][0]
        # print(router)
        results.append(dict(name=r['address'][0],router=router,type=r['type'],cmds="test cmd"))
  return json.dumps(results) 


# POST route in order to invoke the looking glass service
@app.route('/lg', methods=['POST'])
def lg():
    # get parameters from the request body
    req_data = request.get_json()
    print(req_data)
    # obtain the router object and the ready-to-enter command
    router, command = helpers.get_vars(req_data['router'], req_data['cmd'], req_data['ipprefix'])
    print(router,command)
    # instantiate our SSH_Client class
    client = ssh_client.SSH_Client(router)
    print(client)
    # run the command
    output_stream = client.run(command)
    # print(output_stream)
    # generator function
    def generate():
        for chunk in output_stream:
            yield chunk
        # close the underlaying transport session of the ssh client
        client.close()
    
    # each yield iteration  in generate() is sent directly to the browser
    return Response(generate())

@app.route('/cmds', methods=['POST'])
def cmds():
    
    return {'id':"Test Data from backend" }
    # return("testing for the cmd return!")
    # # get 

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000,threaded=True)

