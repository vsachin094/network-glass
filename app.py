from flask import Flask, request, Response, render_template
import ssh_client
import helpers
import json
import routers

app = Flask(__name__, static_url_path="/static")


# main route where we render the html
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# GET route in order to fetch the available routers for a given ASN
@app.route("/routers/<asn>", methods=["GET"])
def get_routers(asn):
    results = []
    for r in routers.routers_list:
        if r["asn"] == asn:
            # only return the address/hostname, the location and the OS type of the matching routers
            #   results.append(dict(name=r['address'][0],
            #                       location=r['address'],
            #                       type=r['type'])
            #   )
            router = r["address"][0]
            # print(router)
            results.append(
                dict(
                    name=r["address"][0], router=router, type=r["type"], cmds="test cmd"
                )
            )
    return json.dumps(results)


# POST route in order to invoke the looking glass service

@app.route("/lg", methods=["POST"])
def lg():
    req_data = request.get_json()
    print(req_data)

    # Find the full router dict by name/address
    def find_router(router_name):
        for r in routers.routers_list:
            if r["address"][0] == router_name or r.get("name") == router_name:
                return r
        return None

    if req_data.get("cmd") == "custom" and req_data.get("customCmd"):
        router = find_router(req_data["router"])
        command = req_data["customCmd"]
    else:
        router, command = helpers.get_vars(
            req_data["router"], req_data["cmd"], req_data["ipprefix"]
        )

    if not router:
        return Response("Router not found", status=404)

    print(router, command)
    client = ssh_client.SSH_Client(router)
    print(client)
    output_stream = client.run(command)

    def generate():
        for chunk in output_stream:
            yield chunk
        client.close()

    return Response(generate())


@app.route("/cmds", methods=["POST"])
def cmds():

    return {"id": "Test Data from backend"}
    # return("testing for the cmd return!")
    # # get


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
