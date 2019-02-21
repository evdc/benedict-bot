from benedict.app.sms import send_message

def ping(number):
    m = "Hello from Benedict! It is {}".format(datetime.now())
    print("Pinging {} from PID {}".format(number, os.getpid()))
    send_message(m, number)
