from controller import *
from model import *

my_model = Model()
my_model.create_database()
# Starting the python applicaiton
if __name__ == '__main__':
    # Step 1: Change this port number if needed
    PORT_NUMBER = 5000
    host = '127.0.0.1'

    print("-"*70)
    print("""Welcome to Server Backend.\n
             Please open your browser to:
             http://127.0.0.1:{}""".format(PORT_NUMBER))
    print("-"*70)


    # Note, you're going to have to change the PORT number
    app.run(debug=True, host=host, port=PORT_NUMBER)
