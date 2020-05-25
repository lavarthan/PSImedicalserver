from Database_connector import get_details, db


def get_database_details(tag, details):
    if tag == "check doctor details":
        name = details[0][0]

        doctor_details = list(get_details("select * from doctor_details where name='%s'" % name))
        print(doctor_details)
        if len(doctor_details) != 0:
            print("Here is the information about Dr.%s" % name)
            answer = "Name : " + doctor_details[0][1] + " " + "Working hospitals: " + doctor_details[0][2] + " " + \
                     doctor_details[0][3]
        else:
            print("sorry there is no information about Dr." + name)

    elif tag == "hospital details check":
        if len(details) != 0:
            location = details[0][0]
            hospital_details = list(get_details("select * from hospital_details where district='%s'" % location))
            answer = ""
            if len(hospital_details) != 0:
                print("Here is the hospitals details in %s" % location)
                for i in hospital_details:
                    answer += "Name : " + i[1] + "\n" + "Address: " + i[2] + "\n" + "Services : " + i[3] + "\n"
            else:
                answer = "Sorry we only provide hospital details by district name."

        else:
            answer = "Sorry we only provide hospital details by district name."

    elif tag == "appointment check":
        for i in details:
            if i[1] == 'PERSON':
                name = i[0]
            elif i[1] == 'DATE':
                date = i[0]
        appointment_details = get_details(
            "select * from appointment_details where name='%s' and date = '%s'" % (name, date))
        check_doctor = get_details("select * from doctor_details where name ='%s'" % name)

        answer = ""
        if len(check_doctor) != 0:
            if len(appointment_details) != 0:
                print("Here is the appointment details of Dr.%s" % name)
                for i in appointment_details:
                    answer += "\nDate : " + i[2] + "\n" + "Time : " + i[3] + "\n" + "Hospital : " + i[4] + "\n"
            else:
                answer = "There is no appointment for Dr." + name + " on " + date
        else:
            answer = "Sorry there is no name Dr.%s found" % name
    return answer


def insert_details(complain):
    cur = db.cursor()
    cur.execute("insert into complain_details (name,complain) values ('user_name','%s')" % complain)
    db.commit()
    print("Your complain filed successfully.")
