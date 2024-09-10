import os
import mysql.connector
from flask import Flask, render_template, request
from dotenv import load_dotenv
from helper import process_event_data, create_logger, create_extra_dict

load_dotenv()

# Flask application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Create the logger
logger = create_logger()

# Database config
config = {
      "host": "localhost",
      "user": os.getenv("DB_USER"),
      "password": os.getenv("DB_PASS"),
      "database": os.getenv("DB_DB")
    }

# Global variables
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
invalidChar = [';', '\'', '\"', '}', ')', ']', '`']


@app.before_request
def add_client_ip() -> None:
    """Middleware to get users IP"""
    request.clientip = request.headers.get('X-Forwarded-For',
                                           request.remote_addr)


@app.after_request
def after_request(response) -> None:
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index() -> str:
    logger.info('Request received for "/" route',
                extra=create_extra_dict(request))
    return render_template("index.html")


@app.route("/about")
def about() -> str:
    logger.info('Request received for "/about" route',
                extra=create_extra_dict(request))
    return render_template("about.html")


@app.route("/wip")
def wip() -> str:
    logger.info('Request received for "/wip" route',
                extra=create_extra_dict(request))
    return render_template("wip.html")


@app.route("/error")
def error() -> str:
    logger.info('Request received for "/error" route',
                extra=create_extra_dict(request))
    return render_template("error.html")


@app.route("/contact", methods=["GET", "POST"])
def calender() -> str:
    logger.info('Request received for "/contact" route',
                extra=create_extra_dict(request))
    
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    if request.method == "POST":
        try:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message = request.form.get('message')

            list_of_input = [first_name, last_name, email, phone, message]

            for inp in list_of_input:
                if not inp:
                    logger.info('User was sent to error from'
                                '"/contact" because they were missing an input',
                                extra=create_extra_dict(request, list_of_input))
                    return render_template(
                        "error.html",
                        error="Submit all required inputs."
                        )

            for user_input in list_of_input:
                for char in invalidChar:
                    if char in user_input:
                        logger.info('User was sent to error from'
                                    '"/contact" because there were'
                                    'invalid characters in the input',
                                    extra=create_extra_dict(request,
                                                            list_of_input))
                        return render_template(
                            "error.html",
                            error="Invalid Characters."
                            )

                for num in numbers:
                    if str(num) in first_name or str(num) in last_name:
                        logger.info('User was sent to error from "/contact"'
                                    ' because there were invalid chars in name',
                                    extra=create_extra_dict(request,
                                                            list_of_input))
                        return render_template(
                            "error.html",
                            error="Invalid Characters."
                            )
            # Insert values into DB
            cursor.execute(
                """insert into contact
                (first_name, last_name, email, phone, message)
                values (%s, %s, %s, %s, %s)""",
                list_of_input
                )

            # Commit the insertion
            connection.commit()
        except Exception as e:
            print(e)
            return render_template(
                "error.html",
                error="Internal Server Error."
                )
        finally:
            if cursor is not None:
                cursor.close()

            connection.close()

        return render_template("success.html", success="""
                               Your submission has gone through!
                                Thank you for your feedback!
                               """)

    return render_template("contact.html", error=error)


@app.route("/schedule")
def calendar() -> str:
    logger.info('Request received for "/schedule" route',
                extra=create_extra_dict(request))

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    try:
        sql = "SELECT * FROM events"
        cursor.execute(sql)
        result = cursor.fetchall()
        processed_events_data = [process_event_data(event) for event in result]
    except Exception as e:
        print(e)
        return render_template(
            "error.html",
            error="Internal Server Error."
            )
    finally:
        if cursor is not None:
                cursor.close()

        connection.close()

    return render_template("calendar.html", events=processed_events_data)


@app.route("/addtoschedule", methods=["GET", "POST"])
def event_form():
    """
    This is a secret route to be able to add events to the calendar
	"""
    logger.info('Request received for "/addtoschedule" route',
                extra=create_extra_dict(request))
    
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    if request.method == "POST":
        try:
            event_name = request.form.get('event_name')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            year = request.form.get('year')
            month = request.form.get('month')
            day = request.form.get('day')
            password = request.form.get('password')

            user_input_list = [event_name, start_time,
                            end_time, year,
                            month, day,
                            password]

            for inp in user_input_list:
                if not inp:
                    logger.info('User was sent to error from "/addtoschedule"'
                                ' because they were missing an input',
                                extra=create_extra_dict(request, user_input_list))
                    return render_template(
                            "error.html",
                            error="Missing input."
                            )

            if not password == os.getenv("PASSWORD"):
                logger.info('User was sent to error from'
                            '"contact" because they were missing an input',
                            extra=create_extra_dict(request, user_input_list))
                return render_template(
                            "error.html",
                            error="Invalid password."
                            )
            user_input_list.pop()

            # Insert values into DB
            cursor.execute(
                """insert into events
                (occasion, startTime, endTime, year, month, day)
                values (%s, %s, %s, %s, %s, %s)""",
                user_input_list
                )

            # Commit the insertion
            connection.commit()
        except Exception as e:
            print(e)
            return render_template(
                "error.html",
                error="Internal Server Error."
                )
        finally:
            if cursor is not None:
                cursor.close()

            connection.close()
            
            return render_template("success.html",
                                success="""
                                    Nice!
                                    The event was added!
                                    """)

    return render_template("addtoschedule.html")


if __name__ == '__main__':
    app.run(port=3001)
