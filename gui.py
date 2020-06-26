from flask import Flask
app = Flask(__name__)
from flask import render_template
from flask import url_for, request, redirect
from connections.manager import Manager


ctal = Manager()
ctal.connect_to_database()

@app.route('/', methods=["GET", "POST"])
def dashboard(message='Status Group : "All"'):

    #Add if not connected then connect to database

    update_list = ctal.get_update()
    ctal.update_database('all', update_list)
    status = ctal.get_status_data('WLR')



    """if request.method == "POST":
        command = request.form["command"]
        command = command.lower()

        if "show" in command:
            if command == "show":
                return display_tickets(ticket_number="all")
            else:
                command = command.split()
                return display_tickets(ticket_number=command[1])
        elif command == "add" or command == "new":
            return redirect('/add')"""
    #status = [["12:00", "wlringest14", "CONNECTED", "ops.wlr"],["15:00", "wlringest12", "CONNECTED", "ops.wlr"], ["8:00", "wlringest8", "CONNECTED", "ops.wlr"]]


    return render_template('dashboard.html', message=message, status=status)


@app.route('/add', methods=["GET", "POST"])
def add():
    message = ""
    loggers = ctal.get_logger_and_group()

    if request.method == "POST":
        pc_name = request.form["pc_name"]
        type = request.form["type"]
        group = request.form["group"]
        logger = ctal.add_logger(pc_name, type, group=group)

        if "does not exist" in logger:
            return render_template('add.html', message=f"Failed: {logger}", loggers=loggers)
        else:
            # Gets the most recent logger and runs it through intial_status()
            update = ctal.initial_status(ctal.all_loggers[len(ctal.all_loggers)-1])
            ctal.update_database(group, update)

            loggers = ctal.get_logger_and_group()
            return render_template('add.html', message=f"Complete: {logger}", loggers=loggers)


    return render_template('add.html', message=message, loggers=loggers)



@app.route("/groups", methods=["GET", "POST"])
def groups():

    message = "All Groups"
    groups = ctal.get_groups()

    if request.method == "POST":
        group_name = request.form["group_name"]
        ctal.create_logger_group(group_name)
        groups = ctal.get_groups()

    return render_template('groups.html', message=message, groups=groups)



"""
#@app.route('/show/<ticket_number>')
def display_tickets(ticket_number):
    if ticket_number == "all":
        print_file = ticket_input.show_tickets()
    else:
        print_file = ticket_input.show_tickets(ticket_number)
    ticket_header = print_file[0]
    print_file = print_file[1:]
    return render_template('show.html', print_file=print_file, ticket_header=ticket_header )

@app.route('/add', methods=["GET", "POST"])
def get_ticket_number(ticket_number=None, client=None, report=None, message='Enter Ticket Number'):
    if request.method == "POST":
        command = request.form["command"]
        command = command.lower()

        if command == 'q':
            return redirect('/')

        if ticket_number is None:
            if command == "same":
                return redirect(f'/add/{command}/{command}')
            elif command == 'n':
                ticket_number = ticket_input.get_ticket_number()
                return redirect(f'/add/{ticket_number}')
            else:
                return redirect(f'/add/{command}')
        elif client is None:
            return redirect(f'/add/{ticket_number}/{command}')
        elif report is None:
            message = ticket_input.add_ticket(ticket_number, client, command)
            return redirect('/')

    return render_template('add.html', message=message)


@app.route('/add/<ticket>', methods=["GET", "POST"])
def add_client(ticket):
    return get_ticket_number(ticket_number=ticket, message="Enter Client Name")

@app.route('/add/<ticket>/<client>', methods=["GET", "POST"])
def add_report(ticket, client):
    return get_ticket_number(ticket_number=ticket, client=client, message="Enter report:")"""
