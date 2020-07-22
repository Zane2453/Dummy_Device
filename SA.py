from flask import Flask
from flask import render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_cors import cross_origin # Fix the CROS issue

from iottalkpy.dan import Client
import uuid

app = Flask(__name__, template_folder='templates')

class DAI():
    def __init__(self, p_id, do_id, d_id):
        self.p_id = p_id
        self.do_id = do_id
        self.d_id = d_id
        self.dan = Client()

    def on_data(self, odf_name, data):
        print(f"[da] {odf_name}: {data}")

    def on_signal(self, signal, df_list):
        print('[cmd] %s, %s', signal, df_list)

    def on_register(self):
        print('[da] register successfully')

    def on_deregister(self):
        print('[da] register fail')

    def register(self):
        print(self.d_id)
        self.dan.register(
            "https://iottalk2.tw/csm",
            on_signal=self.on_signal,
            on_data=self.on_data,
            idf_list=[
                ['Dummy_Sensor', ['int']]
            ],
            odf_list=[
                ['Dummy_Control', ['int']]
            ],
            accept_protos=['mqtt'],
            name=self.d_id,
            id_=self.d_id,
            profile={
                'model': "Dummy_Device"
            },
            on_register=self.on_register,
            on_deregister=self.on_deregister
        )

@app.route("/", methods=['GET'], strict_slashes=False)
@cross_origin()
def index():
    # Create FrameTalk Project
    #p_id, ido_id, odo_id, dev_name = utlis.create_frame(gen_uuid())
    p_id, ido_id = 13, 69
    DAI(p_id, ido_id, gen_uuid()).register()

    return jsonify({"result": "Success Register"})

# Generate UUID
def gen_uuid():
    mac = str(uuid.uuid4())
    return mac

if __name__ == "__main__":
    app.run(host="localhost", port=5000)