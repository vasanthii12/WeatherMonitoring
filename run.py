import threading
from app import app
from main import main

def run_flask():
    app.run(debug=False)

def run_main():
    main()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    main_thread = threading.Thread(target=run_main)

    flask_thread.start()
    main_thread.start()

    flask_thread.join()
    main_thread.join()