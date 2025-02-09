import os
from flask import Flask, render_template, request, jsonify, send_file, abort, redirect
import random
from datetime import datetime
import datetime as dt
import pytz

app_link = ""
app = Flask(__name__)

utc_now = datetime.utcnow()

# Convert UTC time to Indian Standard Time (IST)
utc_now = pytz.utc.localize(utc_now)
ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

uid_2 = {}
prac_code = {}
class_code = {}
uid = {}
prac_date = {}

backup_cnt = 0
backup_tm = ""

with open("./enc/c_dat", "r") as file:
    raw_dat = file.read()
    file.close()

exec(raw_dat)
print("Initial Values:\nuid_2:", uid_2, "\nprac_code:", prac_code, "\nclass_code:", class_code, "\nuid:", uid,
      "\nprac_date", prac_date, "----------")


def get_user_data_by_uid(f_uid):
    global uid

    if uid.get(str(f_uid)):
        return {
            'uid': int(f_uid),
            'username': uid[str(f_uid)][0],
            'user-roll': int(uid[str(f_uid)][1]),
            'permissions': int(uid[str(f_uid)][2]),
            'password': uid[str(f_uid)][3]
        }

    return None


def get_class_data_by_code(f_class_code):
    global class_code

    if class_code.get(str(f_class_code)):
        return {
            'cls_code': f_class_code,
            'year': class_code[str(f_class_code)][0],
            'subject': class_code[str(f_class_code)][1],
            'faculty': class_code[str(f_class_code)][2],
            'student': class_code[str(f_class_code)][3]
        }

    return None


def create_class(year, subject):
    global class_code, prac_code

    ch = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
          "W", "X", "Y", "Z"]
    new_class_code = ""

    while 1:
        for i in range(4):
            new_class_code = new_class_code + ch[random.randint(0, len(ch) - 1)]

        if class_code.get(str(new_class_code)) is None and prac_code.get(new_class_code) is None:
            class_code[new_class_code] = [year, subject, ["0"], [], []]

            return new_class_code


def create_practical(year, subject, batches: int = 1):
    global prac_code, class_code, prac_date

    ch = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
          "W", "X", "Y", "Z"]
    new_class_code = ""

    while 1:
        for i in range(4):
            new_class_code = new_class_code + ch[random.randint(0, len(ch) - 1)]

        if class_code.get(str(new_class_code)) is None and prac_code.get(new_class_code) is None:
            btc = {}

            for n in range(int(batches)):
                btc[ch[n]] = []
            prac_code[new_class_code] = [year, subject, ["0"], [], [], btc]
            btc_cp = {}

            for n in range(int(batches)):
                btc_cp[ch[n]] = []
            prac_date[new_class_code] = btc_cp

            return new_class_code


def create_subject(f_uid, f_class_code):
    global class_code, uid_2

    if class_code.get(f_class_code):
        if uid.get(str(f_uid)):
            if str(uid[str(f_uid)][2]) == "1" and f_uid not in class_code[f_class_code][2]:
                class_code[f_class_code][2].append(str(f_uid))

                return True

            elif str(uid[str(f_uid)][2]) == "2" and f_uid not in class_code[f_class_code][3]:
                class_code[f_class_code][3].append(str(f_uid))

                if uid_2.get(str(f_uid)):
                    uid_2[str(f_uid)][f_class_code] = []

                else:
                    uid_2[str(f_uid)] = {}
                    uid_2[str(f_uid)][f_class_code] = []

                return True

            else:
                return False

        else:
            return False

    return False


def create_batch(f_uid, f_class_code):
    global prac_code, uid_2

    f_class_code, batch = f_class_code[:-1], f_class_code[-1]

    if prac_code.get(f_class_code):
        if uid.get(str(f_uid)):
            if str(uid[str(f_uid)][2]) == "1" and f_uid not in prac_code[f_class_code][2]:
                prac_code[f_class_code][2].append(str(f_uid))

                return True

            elif str(uid[str(f_uid)][2]) == "2" and f_uid not in prac_code[f_class_code][3]:
                prac_code[f_class_code][3].append(str(f_uid))
                prac_code[f_class_code][5][batch].append(str(f_uid))

                if uid_2.get(str(f_uid)):
                    uid_2[str(f_uid)][f_class_code] = []

                else:
                    uid_2[str(f_uid)] = {}
                    uid_2[str(f_uid)][f_class_code] = []

                return True

            else:
                return False

        else:
            return False

    return False


def class_0():
    global class_code, prac_code

    cls_names = []
    cls_code = []

    for key in class_code.keys():
        cls_names.append(class_code[key][0] + " " + class_code[key][1])
        cls_code.append(str(key))
    # for key in prac_code.keys():
    #     cls_names.append("P " + prac_code[key][0] + " " + prac_code[key][1])
    #     cls_code.append(str(key))

    return cls_names, cls_code


def prac_0():
    global prac_code

    prc_name = []
    prc_code = []

    for key in prac_code.keys():
        prc_name.append(prac_code[key][0] + " " + prac_code[key][1])
        prc_code.append(str(key))

    return prc_name, prc_code


def class_1(t_uid):
    global class_code

    cls_code = []
    cls_names = []

    for c in class_code:
        if t_uid in class_code[c][2]:
            cls_names.append(class_code[c][0] + " " + class_code[c][1])
            cls_code.append(c)

    return cls_names, cls_code


def prac_1(t_uid):
    global prac_code

    cls_code = []
    cls_names = []

    for c in prac_code:
        if t_uid in prac_code[c][2]:
            cls_names.append(prac_code[c][0] + " " + prac_code[c][1])
            cls_code.append(c)

    return cls_names, cls_code


def class_2():
    return


def cls_std(cc):
    global class_code, uid

    std_id = class_code[cc][3]
    std_name = []
    std_roll = []

    for i in std_id:
        std_name.append(uid[i][0])
        std_roll.append(int(uid[i][1]))

    combined_list = list(zip(std_roll, std_name, std_id))
    sorted_list = sorted(combined_list, key=lambda x: x[0])

    if len(sorted_list) == 0:
        return [], [], []

    std_roll, std_name, std_id = zip(*sorted_list)

    return std_name, std_roll, std_id


def prac_std(cc):
    global prac_code, uid

    std_name = []
    std_roll = []

    if len(cc) == 5:
        std_id = prac_code[cc[:-1]][5][cc[-1]]

    elif len(cc) == 4:
        std_id = prac_code[cc][3]

    else:
        return [], [], []

    for i in std_id:
        std_name.append(uid[i][0])
        std_roll.append(int(uid[i][1]))

    combined_list = list(zip(std_roll, std_name, std_id))
    sorted_list = sorted(combined_list, key=lambda x: x[0])

    if len(sorted_list) == 0:
        return [], [], []

    std_roll, std_name, std_id = zip(*sorted_list)

    return std_name, std_roll, std_id


@app.route("/")
def index():
    global class_code
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" in user_agent or "android" in user_agent:
        cookie_value = request.cookies.get('user_id')

        if cookie_value:
            print("Cookies: ", cookie_value)
            per = get_user_data_by_uid(int(cookie_value))
            print(per)

            if per is not None:
                per = per['permissions']

                if per == 0:
                    cc, cn = class_0()
                    prn, prc = prac_0()
                    cls_year = ["All"]
                    prac_year = ["All"]

                    for key in class_code.keys():
                        if class_code[key][0] not in cls_year:
                            cls_year.append(class_code[key][0])

                    for key in prac_code.keys():
                        if prac_code[key][0] not in prac_year:
                            prac_year.append(prac_code[key][0])

                    return render_template("hod_dash.html", PRACYEAR=prac_year, CLSYEAR=cls_year,
                                           CLASSCODE=cc, NAME=cn, PRACODE=prc, PRANAME=prn)

                elif per == 1:
                    cc, cn = class_1(str(cookie_value))
                    prc, prn = prac_1(str(cookie_value))

                    return render_template("faculty_dash.html", CLASSCODE=cc, NAME=cn, PRACODE=prc, PRANAME=prn)

                elif per == 2:
                    return render_template("student_dash.html")

                else:
                    return render_template("login.html")

        else:
            return render_template("login.html")
    return redirect("/docs")

@app.route("/profile")
def profile():
    global uid
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cookie_value = request.cookies.get('user_id')

    if uid[str(cookie_value)][2] == "0":

        return render_template("profile.html", DASH="/", PROGRESS="/hd_cls", PRINT='/print',
                               NAME=uid[str(cookie_value)][0].split(" ")[0],
                               ID=str(cookie_value), DES="HOD",
                               SERVERCODE="navigator.clipboard.writeText(btoa(window.location.host, 'calisthenics'));")

    elif uid[str(cookie_value)][2] == "2":
        return render_template("profile.html", DASH="/", PROGRESS="/progress", PRINT='/profile',
                               NAME=uid[str(cookie_value)][0].split(" ")[0],
                               ID=str(cookie_value), DES="Student",
                               SERVERCODE="alert('Your do not have permission to access Server Code.');")

    elif uid[str(cookie_value)][2] == "1":
        return render_template("profile.html", DASH="/", PROGRESS="/faculty-class", PRINT='/print',
                               NAME=uid[str(cookie_value)][0].split(" ")[0],
                               ID=str(cookie_value), DES="HOD", SERVERCODE="")


@app.route("/hd_cls")
def hd_cls():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cc, cn = class_0()
    k, m = prac_0()

    for i, j in zip(k, m):
        cc.append(i + " (Lab)")
        cn.append(j)

    return render_template("hod_class.html", CLASSCODE=cc, NAME=cn)


@app.route("/faculty-class")
def faculty_class():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cookie_value = request.cookies.get('user_id')
    cc, cn = class_1(str(cookie_value))
    k, m = prac_1(str(cookie_value))

    for i, j in zip(k, m):
        cc.append(i + " (Lab)")
        cn.append(j)

    return render_template("faculty_class.html", CLASSCODE=cc, NAME=cn)


@app.route("/progress")
def progress():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    global uid_2, class_code, prac_code

    cookie_value = request.cookies.get('user_id')

    if uid_2.get(str(cookie_value)):
        cc = []
        cn = []
        pc = []
        pn = []

        for i in uid_2[str(cookie_value)]:
            if class_code.get(i):
                cc.append(i)
                print(i)
                cn.append(class_code[i][0] + " " + class_code[i][1])

            elif prac_code.get(i):
                pc.append(i)
                print(i)
                pn.append(prac_code[i][0] + " " + prac_code[i][1])

        return render_template("student_class.html", CLASSCODE=cc, NAME=cn, PRACODE=pc, PRANAME=pn)

    else:
        return render_template("student_class.html", CLASSCODE=[], NAME=[], PRACODE=[], PRANAME=[])


@app.route("/print")
def prnt():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cookie_value = request.cookies.get("user_id")

    if uid.get(cookie_value):
        if uid[cookie_value][2] == "0":
            cc, cn = [], []
            cls_year = ["All"]

            for key in class_code.keys():
                if class_code[key][0] not in cls_year:
                    cls_year.append(class_code[key][0])

                cc.append(key)
                cn.append(class_code[key][0] + " " + class_code[key][1])

            for key in prac_code.keys():
                if prac_code[key][0] not in cls_year:
                    cls_year.append(prac_code[key][0])

                cc.append(key)
                cn.append(prac_code[key][0] + " " + prac_code[key][1] + " (Lab)")

            return render_template("print.html", CLASSNAME=cn, CLASSCODE=cc, CLSYEAR=cls_year, PROGRESS='/hd_cls')

        elif uid[cookie_value][2] == "1":
            cc, cn = [], []
            cls_year = ["All"]
            a, b = class_1(str(cookie_value))
            cc = cc + a
            cn = cn + b
            a, b = prac_1(str(cookie_value))

            for _, __ in zip(a, b):
                cc.append(_ + " (Lab)")
                cn.append(__)
            # cc = cc + a
            # cn = cn + b
            for c in class_code:
                if cookie_value in class_code[c][2] and class_code[c][0] not in cls_year:
                    cls_year.append(class_code[c][0])

            for c in prac_code:
                if cookie_value in prac_code[c][2] and prac_code[c][0] not in cls_year:
                    cls_year.append(prac_code[c][0])

            return render_template("print.html", CLASSNAME=cc, CLASSCODE=cn, CLSYEAR=cls_year,
                                   PROGRESS='/faculty-class')

        elif uid[cookie_value][2] == "2":
            return render_template("print.html")


@app.route("/print-report", methods=["POST"])
def print_request():
    def get_att(cookie_value, ccc, f_d, t_d):
        def date_cnt(date_list, f, t):
            d_cnt = 0

            for date in date_list:
                eff_d = datetime.strptime(date.split("_")[0], '%d-%m-%Y')

                if f <= eff_d <= t:
                    d_cnt = d_cnt + 1

            return d_cnt

        if uid_2.get(str(cookie_value)):
            cnt = 0
            ttl_cnt = 0

            if class_code.get(ccc):
                # ttl_cnt = len(class_code[ccc][4])
                ttl_cnt = date_cnt(class_code[ccc][4], f_d, t_d)
                # cnt = len(uid_2[str(cookie_value)][ccc])
                cnt = date_cnt(uid_2[str(cookie_value)][ccc], f_d, t_d)

            elif prac_code.get(ccc) and cookie_value in prac_code[ccc][3]:
                for e in prac_code[ccc][5].keys():

                    if cookie_value in prac_code[ccc][5][e]:
                        # ttl_cnt = len(prac_date[ccc][e])
                        ttl_cnt = date_cnt(prac_date[ccc][e], f_d, t_d)
                        # print("e: {}, ttl_cnt: {}".format(e, ttl_cnt))
                        # cnt = len(uid_2[str(cookie_value)][ccc])
                        cnt = date_cnt(uid_2[str(cookie_value)][ccc], f_d, t_d)

            if ttl_cnt == 0:
                return "-"

            perk = int((cnt / ttl_cnt) * 100)
            return perk

        return 0

    print_data_request = request.get_json()
    print(print_data_request)
    type_batch = print_data_request["type"]
    batch = print_data_request["batch"]
    f_date = print_data_request["f_date"]
    t_date = print_data_request["t_date"]
    percent_a_b = print_data_request["percent_a_b"]
    percent = print_data_request["percent"]
    out_arr = [["Sr. No.", "Roll Number", "Name"], ]
    f_date = datetime.strptime(f_date, '%Y-%m-%d')
    t_date = datetime.strptime(t_date, '%Y-%m-%d')
    print(f_date)

    if f_date > t_date or f_date == t_date:
        print("date miss")

        return jsonify({'message': "Date mismatched."}), 401

    if type_batch == "Year wise":
        cc = []
        pc = []
        batch_loc = []

        for b in batch:
            for c in class_code:
                if class_code[c][0] == b:
                    cc.append(c)
                    batch_loc.append(c)
                    out_arr[0].append(class_code[c][1])

        for b in batch:
            for c in prac_code:
                if prac_code[c][0] == b:
                    pc.append(c)
                    batch_loc.append(c)
                    out_arr[0].append(prac_code[c][1] + "(Lab)")

        # print(cc, pc, out_arr, )
        uid_loc = []

        for cl in cc:
            for s in class_code[cl][3]:
                if s not in uid_loc:
                    uid_loc.append(s)
                    temp_arr = [str(len(out_arr)), uid[s][1], uid[s][0]]
                    # for _ in range(len(batch_loc)):
                    #     temp_arr.append("0")
                    out_arr.append(temp_arr)

        for pl in pc:
            for s in prac_code[pl][3]:
                if s not in uid_loc:
                    uid_loc.append(s)
                    temp_arr = [str(len(out_arr)), uid[s][1], uid[s][0]]
                    # for _ in range(len(batch_loc)):
                    #     temp_arr.append("0")
                    out_arr.append(temp_arr)

        print("no mention\n", out_arr)

        for cl in cc:
            for s in class_code[cl][3]:
                per = get_att(s, cl, f_date, t_date)
                ind = batch_loc.index(cl) + 3
                # print("ind: {}".format(ind))
                len_diff = ind - len(out_arr[uid_loc.index(s) + 1])
                # print("len: {}".format(len(out_arr[uid_loc.index(s) + 1])))
                print("len_diff: {} for Att_Id: {}".format(len_diff, s))

                for _ in range(len_diff):
                    out_arr[uid_loc.index(s) + 1].append("-")
                out_arr[uid_loc.index(s) + 1].append(str(per))
                # out_arr[uid_loc.index(s) + 1].insert(batch_loc.index(cl) + 3, str(per))

        for pl in pc:
            for s in prac_code[pl][3]:
                per = get_att(s, pl, f_date, t_date)
                ind = batch_loc.index(pl) + 3
                # print("ind: {}".format(ind))
                len_diff = ind - len(out_arr[uid_loc.index(s) + 1])
                # print("len: {}".format(len(out_arr[uid_loc.index(s) + 1])))
                print("len_diff: {} for Att_Id: {}".format(len_diff, s))

                for _ in range(len_diff):
                    out_arr[uid_loc.index(s) + 1].append("-")
                out_arr[uid_loc.index(s) + 1].append(str(per))
                # out_arr[uid_loc.index(s) + 1].insert(batch_loc.index(pl) + 3, str(per))

        out_arr[0].append("Overall Attendance")
        final_arr = [out_arr[0], ]

        for id_, rem in enumerate(out_arr[1:]):
            cnt = 0
            t_cnt = 0

            for rec in rem[3:]:
                if rec != "-":
                    cnt = cnt + int(rec)
                    t_cnt = t_cnt + 100

            if t_cnt == 0:
                ka = 0
                # out_arr[id_+1].append("0")

            else:
                ka = (cnt / t_cnt) * 100

            ind = len(out_arr[0]) - 1
            len_diff = ind - len(rem)

            for _ in range(len_diff):
                rem.append("-")

            rem.append(str(round(ka, 2)))

            if percent_a_b == "Below":
                if ka <= int(percent):
                    final_arr.append(rem)

            elif percent_a_b == "Above":
                if ka > int(percent):
                    final_arr.append(rem)

            else:
                final_arr.append(rem)

            # out_arr[id_+1].append(str(ka))
        utc_now = datetime.utcnow()

        # Convert UTC time to Indian Standard Time (IST)
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        f_name = f"./dat/{ist_now.strftime('%H:%M')}_Overall_Attendance_Report_{f_date.date().strftime('%d-%m')}_to_{t_date.date().strftime('%d-%m')}.csv"

        with open(f_name, "a") as exp:
            for row in final_arr:
                for cell in row:
                    exp.write(str(cell) + ",")
                exp.write("\n")

        return jsonify({'message': 'File ready', 'file_path': app_link + f_name[24:]})

    elif type_batch == "Batch wise":

        cc = []
        pc = []
        batch_loc = []

        for b in batch:
            if class_code.get(b):
                cc.append(b)
                batch_loc.append(b)
                out_arr[0].append(class_code[b][1])

            elif prac_code.get(b):
                pc.append(b)
                batch_loc.append(b)
                out_arr[0].append(prac_code[b][1] + "(Lab)")

        print(cc, pc, out_arr, )
        uid_loc = []

        for cl in cc:
            for s in class_code[cl][3]:
                if s not in uid_loc:
                    uid_loc.append(s)
                    temp_arr = [str(len(out_arr)), uid[s][1], uid[s][0]]
                    # for _ in range(len(batch_loc)):
                    #     temp_arr.append("0")
                    out_arr.append(temp_arr)

        for pl in pc:
            for s in prac_code[pl][3]:
                if s not in uid_loc:
                    uid_loc.append(s)
                    temp_arr = [str(len(out_arr)), uid[s][1], uid[s][0]]
                    # for _ in range(len(batch_loc)):
                    #     temp_arr.append("0")
                    out_arr.append(temp_arr)

        print("no mention\n", out_arr)

        for cl in cc:
            for s in class_code[cl][3]:
                per = get_att(s, cl, f_date, t_date)
                ind = batch_loc.index(cl) + 3
                # print("ind: {}".format(ind))
                len_diff = ind - len(out_arr[uid_loc.index(s) + 1])
                # print("len: {}".format(len(out_arr[uid_loc.index(s) + 1])))
                print("len_diff: {} for Att_Id: {}".format(len_diff, s))

                for _ in range(len_diff):
                    out_arr[uid_loc.index(s) + 1].append("0")
                out_arr[uid_loc.index(s) + 1].append(str(per))
                # out_arr[uid_loc.index(s) + 1].insert(batch_loc.index(cl) + 3, str(per))

        for pl in pc:
            for s in prac_code[pl][3]:
                per = get_att(s, pl, f_date, t_date)
                ind = batch_loc.index(pl) + 3
                # print("ind: {}".format(ind))
                len_diff = ind - len(out_arr[uid_loc.index(s) + 1])
                # print("len: {}".format(len(out_arr[uid_loc.index(s) + 1])))
                print("len_diff: {} for Att_Id: {}".format(len_diff, s))

                for _ in range(len_diff):
                    out_arr[uid_loc.index(s) + 1].append("-")
                out_arr[uid_loc.index(s) + 1].append(str(per))
                # out_arr[uid_loc.index(s) + 1].insert(batch_loc.index(pl) + 3, str(per))

        out_arr[0].append("Overall Attendance")
        print("outarray: {}".format(out_arr))
        final_arr = [out_arr[0], ]

        for id_, rem in enumerate(out_arr[1:]):
            cnt = 0
            t_cnt = 0
            for rec in rem[3:]:
                if rec != "-":
                    cnt = cnt + int(rec)
                    t_cnt = t_cnt + 100

            if t_cnt == 0:
                ka = 0
                # out_arr[id_+1].append("0")

            else:
                ka = (cnt / t_cnt) * 100

            ind = len(out_arr[0]) - 1
            len_diff = ind - len(rem)

            for _ in range(len_diff):
                rem.append("-")

            rem.append(str(round(ka, 2)))

            if percent_a_b == "Below":
                if ka <= int(percent):
                    final_arr.append(rem)

            elif percent_a_b == "Above":
                if ka > int(percent):
                    final_arr.append(rem)
            else:
                final_arr.append(rem)

            # out_arr[id_+1].append(str(ka))
        utc_now = datetime.utcnow()

        # Convert UTC time to Indian Standard Time (IST)
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        f_name = f"./dat/{ist_now.strftime('%H:%M')}_Overall_Attendance_Report_{f_date.date().strftime('%d-%m')}_to_{t_date.date().strftime('%d-%m')}.csv"
        with open(f_name, "a") as exp:
            for row in final_arr:
                for cell in row:
                    exp.write(str(cell) + ",")
                exp.write("\n")

        return jsonify({'message': 'File ready', 'file_path': app_link + f_name[24:]})

    return jsonify({'message': 'Invalid credentials'}), 401


@app.route("/docs")
def docs():
    files = os.listdir("./dat")
    print(files)
    files = [f for f in files if os.path.isfile(os.path.join("./dat", f)) and not f.startswith('.')]
    files_with_creation_time = [(file, os.path.getctime(os.path.join("./dat", file))) for file in files]

    # Sort the list of tuples by creation time
    files_with_creation_time.sort(key=lambda x: x[1])

    # Extract only the filenames from the sorted list
    sorted_files = [file[0] for file in files_with_creation_time]
    return render_template("uptd_docs.html", FILE=sorted_files)


@app.route("/docs/get/<file_name>")
def s_docs(file_name):
    print(f"file_name: {file_name}")

    if os.path.exists(f"./dat/{file_name}"):
        return send_file(f"./dat/{file_name}", as_attachment=True)

    else:
        abort(500)


@app.route("/att/<cc>")
def att(cc):

    global class_code
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    n, r, i = cls_std(cc)
    sb_name, yr = class_code[cc][0], class_code[cc][1]

    return render_template("faculty_att.html", SUBJECT=sb_name, BATCH=yr, ROLL=r, NAME=n, ID=i, CLASSCODE=cc)


@app.route("/att-p/<cc>")
def att_p(cc):
    global prac_code
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    n, r, i = prac_std(cc)

    sb_name, yr = prac_code[cc[:-1]][0], prac_code[cc[:-1]][1]

    return render_template("faculty_att.html", SUBJECT=sb_name, BATCH=yr, ROLL=r, NAME=n, ID=i, CLASSCODE=cc)
    # if len(cc) == 4:
    #     n, r, i = prac_std(cc)
    #     sb_name, yr = prac_code[cc][0], prac_code[cc][1]
    #     return render_template("faculty_att.html", SUBJECT=sb_name, BATCH=yr, ROLL=r, NAME=n, ID=i, CLASSCODE=cc)
    # elif len(cc) == 5:
    #     cc, batch = cc[:-1], cc[-1]
    #     n, r, i = prac_std(cc)
    #     sb_name, yr = prac_code[cc][0], prac_code[cc][1]
    #     return render_template("faculty_att.html", SUBJECT=sb_name, BATCH=yr, ROLL=r, NAME=n, ID=i, CLASSCODE=cc)


@app.route("/att-s/<cc>")
def att_s(cc):
    global prac_code
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cds, nms = [], []
    nm = prac_code[cc][0] + " " + prac_code[cc][1]

    for k in prac_code[cc][5]:
        cds.append(cc + k)
        nms.append(nm + " batch " + k)

    sb_name, yr = prac_code[cc][0], prac_code[cc][1]

    return render_template("prac_batch.html", POSTL="/att-p/", SUBJECT=sb_name, BATCH=yr, NAME=nms, CLASSCODE=cds)


@app.route("/info/<cc>")
def class_info_rend(cc):
    global class_code, prac_code, uid
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    std_name = []
    faculty_name = []
    if class_code.get(cc):
        year, name, faculty, student = class_code[cc][0], class_code[cc][1], class_code[cc][2], class_code[cc][3]
        n, r, i = cls_std(cc)
    else:
        year, name, faculty, student = prac_code[cc][0], prac_code[cc][1] + " (Lab)", prac_code[cc][2], prac_code[cc][3]
        n, r, i = prac_std(cc)

    for _, __ in zip(n, r):
        std_name.append(str(__) + " " + str(_))
    for f in faculty:
        faculty_name.append(uid[f][0])
    # for s in student:
    #     std_name.append(str(uid[s][1]) + "  " + uid[s][0])

    return render_template("class_info.html", BATCH=year, NAME=name,
                           FACULTY=faculty_name, STUDENT=std_name, CC=cc)


@app.route('/login', methods=['POST'])
def login():
    user_credentials = request.get_json()
    print("\n", user_credentials)
    user_id = user_credentials.get("user_id")
    password = user_credentials.get("password")
    print(user_id, password)
    ud = get_user_data_by_uid(str(user_id))
    print(ud)

    if ud:
        if password == ud['password']:
            print("login success\n")
            response_data = {'message': 'Login successful', 'auth_token': 'example_auth_token'}
            response = jsonify(response_data)
            response.set_cookie('user_id', user_id)

            return response

        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    else:
        # Return an error response if authentication fails
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route("/signup", methods=["POST"])
def signup():
    global uid

    user_credentials = request.get_json()
    print(user_credentials)
    name = user_credentials["name"]
    roll = user_credentials['roll']
    password = user_credentials['password']
    i = 5

    while 1:
        if uid.get(str(i)):
            i = i + 1

        else:
            uid[str(i)] = [name, roll, '2', password]

            return jsonify({"n_id": i})


@app.route('/send-array/<cc>', methods=['POST'])
def receive_array(cc):
    global uid_2, class_code, prac_code, prac_date

    temp_uid_2 = uid_2

    try:
        data = request.get_json()
        utc_now = datetime.utcnow()

        # Convert UTC time to Indian Standard Time (IST)
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        cur_time = ist_now.strftime("%d-%m-%Y_%H:%M")

        if len(cc) == 5:
            cc, batch = cc[:-1], cc[-1]

        if class_code.get(cc):
            if cur_time not in class_code[cc][4]:
                received_array = data.get('array')

                for i in received_array:
                    uid_2[i][cc].append(cur_time)
                class_code[cc][4].append(cur_time)
                print(f"received attendance for {cc}", received_array, type(received_array))

                return jsonify({'success': True, 'message': 'Array received successfully'})

            else:
                return jsonify({'success': True, 'message': 'Array received successfully'})

        elif prac_code.get(cc):
            if cur_time not in prac_code[cc][4]:
                received_array = data.get('array')

                for i in received_array:
                    uid_2[i][cc].append(cur_time)

                prac_code[cc][4].append(cur_time)
                prac_date[cc][batch].append(cur_time)
                print(f"received attendance for {cc}", received_array, type(received_array))

                return jsonify({'success': True, 'message': 'Array received successfully'})

            else:
                return jsonify({'success': True, 'message': 'Array received successfully'})

        else:
            return jsonify({'success': False, 'message': f'Class code mismatched'})

    except Exception as e:
        uid_2 = temp_uid_2

        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route("/test")
def d_est():

    return render_template("test.html")


@app.route("/add_class", methods=['POST'])
def add_class():
    cookie_value = request.cookies.get('user_id')
    data = request.get_json()
    year = data.get('year')
    subject = data.get('subject')
    print("hello")
    print("Cookies: ", cookie_value)

    if cookie_value:
        per = get_user_data_by_uid(int(cookie_value))
        print(per)

        if per is not None:
            per = per['permissions']
            print(per, type(per))

            if per == 0:
                cc = create_class(year, subject)
                response_data = {'message': 'Data received successfully', 'class_code': cc}

                return jsonify(response_data)

            else:
                return jsonify({'error': "class cannot be added"}), 401

        else:
            return jsonify({'error': "class cannot be added"}), 401

    else:
        return jsonify({'error': "class cannot be added"}), 401


@app.route("/add_practical", methods=['POST'])
def add_practical():
    cookie_value = request.cookies.get('user_id')
    data = request.get_json()
    year = data.get('year')
    subject = data.get('subject')
    batch = data.get('batch')
    print("Cookies: ", cookie_value)

    if cookie_value:
        per = get_user_data_by_uid(int(cookie_value))
        print(per)

        if per is not None:
            per = per['permissions']
            print(per, type(per))

            if per == 0:
                if len(batch) < 1 or batch is None:
                    batch = 1

                cc = create_practical(year, subject, int(batch))
                cds = prac_code[cc][5]
                msg = ""

                for c in cds:
                    msg = msg + "Batch " + c + " using the code " + cc + c + ","

                response_data = {'message': 'Data received successfully', 'class_code': cc, 'btc_cd': msg}

                return jsonify(response_data)

            else:
                return jsonify({'error': "class cannot be added"}), 401

        else:
            return jsonify({'error': "class cannot be added"}), 401

    else:
        return jsonify({'error': "class cannot be added"}), 401


@app.route("/add_subject", methods=["POST"])
def add_subject():
    cookie_value = request.cookies.get('user_id')
    data = request.get_json()
    subject = data.get('subject')
    print("Att_Id: {} trying to join class: {}".format(cookie_value, subject))

    if cookie_value:
        per = get_user_data_by_uid(int(cookie_value))

        if per is not None:
            per = per['permissions']

            if per in [1, 2]:
                if create_subject(str(cookie_value), subject):
                    print("Att_Id: ", cookie_value, "added to class", subject)
                    response_data = {'message': 'Data received successfully'}

                    return jsonify(response_data)

                else:
                    return jsonify({'error': "class cannot be added"}), 401

        return jsonify({'error': "class cannot be added"}), 401

    return jsonify({'error': "class cannot be added"}), 401


@app.route("/add_batch", methods=["POST"])
def add_batch():
    cookie_value = request.cookies.get('user_id')
    data = request.get_json()
    subject = data.get('subject')
    print("Att_Id: {} trying to join practical: {}".format(cookie_value, subject))

    if cookie_value:
        per = get_user_data_by_uid(int(cookie_value))

        if per is not None:
            per = per['permissions']

            if per in [1, 2]:
                if create_batch(str(cookie_value), subject):
                    print("Att_Id: ", cookie_value, "added to practical", subject)
                    response_data = {'message': 'Data received successfully'}

                    return jsonify(response_data)

                else:
                    return jsonify({'error': "class cannot be added"}), 401

        return jsonify({'error': "class cannot be added"}), 401

    return jsonify({'error': "class cannot be added"}), 401


@app.route("/get_percentage")
def get_perc():
    global uid_2, class_code, prac_code, prac_date
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cookie_value = request.cookies.get('user_id')

    if uid_2.get(str(cookie_value)):
        cnt = 0
        ttl_cnt = 0
        # leaves = 0
        pcnt, lcnt = 0, 0
        p_t_cnt, l_t_cnt = 0, 0

        for i in uid_2[str(cookie_value)]:
            if class_code.get(i):
                ttl_cnt = ttl_cnt + len(class_code[i][4])
                l_t_cnt = l_t_cnt + len(class_code[i][4])
                cnt = cnt + len(uid_2[str(cookie_value)][i])
                lcnt = lcnt + len(uid_2[str(cookie_value)][i])

            elif prac_code.get(i):
                for c in prac_code[i][5]:

                    if cookie_value in prac_code[i][5][c]:
                        ttl_cnt = ttl_cnt + len(prac_date[i][c])
                        p_t_cnt = p_t_cnt + len(prac_date[i][c])
                        cnt = cnt + len(uid_2[str(cookie_value)][i])
                        pcnt = pcnt + len(uid_2[str(cookie_value)][i])

        if ttl_cnt == 0:
            return jsonify({'per': 0, "att": 0, "t_l": 0, "t_cnt": 0, "tp_cnt": 0,
                            "tl_cnt": 0, "l_t_cnt": 0, "p_t_cnt": 0})

        perk = int((cnt / ttl_cnt) * 100)
        print("pcnt: {}, lcnt: {}, uid_2[str(cookie_value)]: {}".format(pcnt, lcnt, uid_2[str(cookie_value)]))

        if l_t_cnt == 0:
            l_t_cnt_p = 0

        else:
            l_t_cnt_p = int((lcnt / l_t_cnt) * 100)

        if p_t_cnt == 0:
            p_t_cnt_p = 0

        else:
            p_t_cnt_p = int((pcnt / p_t_cnt) * 100)

        return jsonify(
            {'per': perk, "att": cnt, "t_l": ttl_cnt - cnt, "t_cnt": ttl_cnt, "tp_cnt": pcnt,
             "tl_cnt": lcnt, "l_t_cnt": l_t_cnt_p, "p_t_cnt": p_t_cnt_p})

    return jsonify({'per': 0, "att": 0, "t_l": 0, "t_cnt": 0, "tp_cnt": 0, "tl_cnt": 0, "l_t_cnt": 0, "p_t_cnt": 0})


# this is the previous working /report page
# @app.route('/report/<cc>')
# def report(cc):
#     global class_code, uid, uid_2, prac_date
#
#     name, roll, sid, sb_name, yr = [], [], [], [], []
#     print("cc: {}".format(cc))
#
#     if class_code.get(cc):
#         sb_name, yr = class_code[cc][0], class_code[cc][1]
#         name, roll, sid = cls_std(cc)
#
#     elif prac_code.get(cc):
#         sb_name, yr = prac_code[cc][0], prac_code[cc][1]
#         name, roll, sid = prac_std(cc)
#
#     def get_att(cookie_value):
#
#         if uid_2.get(str(cookie_value)):
#             cnt = 0
#             ttl_cnt = 0
#
#             if class_code.get(cc):
#                 ttl_cnt = len(class_code[cc][4])
#                 cnt = len(uid_2[str(cookie_value)][cc])
#
#             elif prac_code.get(cc) and cookie_value in prac_code[cc][3]:
#                 for e in prac_code[cc][5].keys():
#
#                     if cookie_value in prac_code[cc][5][e]:
#                         ttl_cnt = len(prac_date[cc][e])
#                         print("e: {}, ttl_cnt: {}".format(e, ttl_cnt))
#                         cnt = len(uid_2[str(cookie_value)][cc])
#
#             if ttl_cnt == 0:
#                 return 0
#
#             perk = int((cnt / ttl_cnt) * 100)
#
#             return perk
#
#         return 0
#
#     header = ["Roll", "Name", "Attendance"]
#     out_arr = [header, ["", "", ""]]
#
#     for n, r, i in zip(name, roll, sid):
#         p = str(get_att(i))
#         out_arr.append([r, n, p])
#
#     print(out_arr)
#
#     return render_template("attendance.html", SUBJECT=sb_name, BATCH=yr, REP=out_arr, CC=cc, DETV="1")


@app.route('/report/<cc>')
def report(cc):
    global class_code, uid, uid_2
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    name, roll, sid, sb_name, yr = [], [], [], [], []

    header = ["Roll", "Name"]

    if class_code.get(cc):
        sb_name, yr = class_code[cc][0], class_code[cc][1]
        name, roll, sid = cls_std(cc)

        if len(class_code[cc][4]) > 0:
            header.append(class_code[cc][4][-1])
        # for date in class_code[cc][4]:
        #     header.append(date)

    elif prac_code.get(cc):
        sb_name, yr = prac_code[cc][0], prac_code[cc][1]
        name, roll, sid = prac_std(cc)

        for date in prac_code[cc][4]:
            header.append(date)

    # sb_name, yr = class_code[cc][0], class_code[cc][1]
    # header.append("Total")
    print(header)
    out_arr = [header, [""]]
    # name, roll, sid = cls_std(cc)

    for n, r, i in zip(name, roll, sid):
        # p = str(get_att(i))
        temp_arr = [r, n]

        d = header[-1]

        if d in uid_2[i][cc]:
            temp_arr.append("1")

        else:
            temp_arr.append("")

        # temp_arr.append(p)
        out_arr.append(temp_arr)
    print(out_arr)

    footer = ["", "Total Count:"]
    for _ in range(len(out_arr[0][2:-1])):
        footer.append(0)
    footer.append(0)

    for row in out_arr:
        col = row[-1]
        if col == "1":
            footer[2] = footer[2] + 1

    out_arr.append(footer)

    return render_template("attendance.html", CC=cc, SUBJECT=sb_name, BATCH=yr, REP=out_arr, DETV="1")


@app.route('/det/<cc>')
def deta(cc):
    global class_code, uid, uid_2
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    name, roll, sid, sb_name, yr = [], [], [], [], []

    def get_att(cookie_value):
        if uid_2.get(str(cookie_value)):
            cnt = 0
            ttl_cnt = 0

            if class_code.get(cc):
                ttl_cnt = len(class_code[cc][4])
                cnt = len(uid_2[str(cookie_value)][cc])

            elif prac_code.get(cc) and cookie_value in prac_code[cc][3]:
                for e in prac_code[cc][5].keys():

                    if cookie_value in prac_code[cc][5][e]:
                        ttl_cnt = len(prac_date[cc][e])
                        print("e: {}, ttl_cnt: {}".format(e, ttl_cnt))
                        cnt = len(uid_2[str(cookie_value)][cc])

            if ttl_cnt == 0:
                return 0

            perk = int((cnt / ttl_cnt) * 100)

            return perk

        return 0

    header = ["Roll", "Name"]

    if class_code.get(cc):
        sb_name, yr = class_code[cc][0], class_code[cc][1]
        name, roll, sid = cls_std(cc)

        for date in class_code[cc][4]:
            header.append(date)

    elif prac_code.get(cc):
        sb_name, yr = prac_code[cc][0], prac_code[cc][1]
        name, roll, sid = prac_std(cc)

        for date in prac_code[cc][4]:
            header.append(date)

    # sb_name, yr = class_code[cc][0], class_code[cc][1]
    header.append("Total")
    out_arr = [header, [""]]
    # name, roll, sid = cls_std(cc)

    for n, r, i in zip(name, roll, sid):
        p = str(get_att(i))
        temp_arr = [r, n]

        for d in header[2:-1]:

            if d in uid_2[i][cc]:
                temp_arr.append("1")

            else:
                temp_arr.append("")

        temp_arr.append(p)
        out_arr.append(temp_arr)
    print(out_arr)

    footer = ["", "Total Count:"]
    for _ in range(len(out_arr[0][2:-1])):
        footer.append(0)
    footer.append("")

    for row in out_arr:
        for f_ind, col in enumerate(row[2:-1]):
            if col == "1":
                footer[f_ind + 2] = footer[f_ind + 2] + 1

    out_arr.append(footer)

    return render_template("attendance.html", CC=cc, SUBJECT=sb_name, BATCH=yr, REP=out_arr, DETV="0")


# @app.route("/only-report/<cc>", methods=["POST"])
# def only_report(cc):
#     global class_code, uid, uid_2, prac_date
#
#     try:
#         name, roll, sid, sb_name, yr = [], [], [], [], []
#         print("Generating only report for cc: {}".format(cc))
#
#         if class_code.get(cc):
#             sb_name, yr = class_code[cc][0], class_code[cc][1]
#             name, roll, sid = cls_std(cc)
#
#         elif prac_code.get(cc):
#             sb_name, yr = prac_code[cc][0], prac_code[cc][1] + "(Lab)"
#             name, roll, sid = prac_std(cc)
#
#         def get_att(cookie_value):
#
#             if uid_2.get(str(cookie_value)):
#                 cnt = 0
#                 ttl_cnt = 0
#
#                 if class_code.get(cc):
#                     ttl_cnt = len(class_code[cc][4])
#                     cnt = len(uid_2[str(cookie_value)][cc])
#
#                 elif prac_code.get(cc) and cookie_value in prac_code[cc][3]:
#                     for e in prac_code[cc][5].keys():
#
#                         if cookie_value in prac_code[cc][5][e]:
#                             ttl_cnt = len(prac_date[cc][e])
#                             print("e: {}, ttl_cnt: {}".format(e, ttl_cnt))
#                             cnt = len(uid_2[str(cookie_value)][cc])
#
#                 if ttl_cnt == 0:
#                     return 0
#
#                 perk = int((cnt / ttl_cnt) * 100)
#
#                 return perk
#
#             return 0
#
#         header = ["Roll", "Name", "Attendance"]
#         out_arr = [header]
#
#         for n, r, i in zip(name, roll, sid):
#             p = str(get_att(i))
#             out_arr.append([r, n, p])
#         # for i in std_lst:
#         #     r, n, p = uid[i][1], uid[i][0], str(get_att(i))
#         #     out_arr.append([r, n, p])
#
#         f_name = f"dat/{datetime.now().strftime('%H:%M')}_{sb_name}_{yr}_Attendance_Report.csv"
#
#         with open(f_name, "a") as exp:
#             for row in out_arr:
#
#                 for cell in row:
#                     exp.write(str(cell) + ",")
#                 exp.write("\n")
#
#         f_name = f_name.replace(" ", "%20")
#
#         return jsonify({'message': 'File ready', 'file_path': app_link + f_name[4:]})
#
#     except Exception as es:
#         print("Only report generation error for cc: {}. Error: {}".format(cc, es))
#
#         return jsonify({'message': 'Invalid credentials'}), 401


@app.route("/only-report/<cc>", methods=["POST"])
def only_report(cc):
    global class_code, uid, uid_2, prac_date

    try:
        name, roll, sid, sb_name, yr = [], [], [], [], []

        header = ["Roll", "Name"]

        if class_code.get(cc):
            sb_name, yr = class_code[cc][0], class_code[cc][1]
            name, roll, sid = cls_std(cc)

            if len(class_code[cc][4]) > 0:
                header.append(class_code[cc][4][-1])
            # for date in class_code[cc][4]:
            #     header.append(date)

        elif prac_code.get(cc):
            sb_name, yr = prac_code[cc][0], prac_code[cc][1]
            name, roll, sid = prac_std(cc)

            for date in prac_code[cc][4]:
                header.append(date)

        # sb_name, yr = class_code[cc][0], class_code[cc][1]
        # header.append("Total")
        print(header)
        out_arr = [header]
        # name, roll, sid = cls_std(cc)

        for n, r, i in zip(name, roll, sid):
            # p = str(get_att(i))
            temp_arr = [r, n]

            d = header[-1]

            if d in uid_2[i][cc]:
                temp_arr.append("1")

            else:
                temp_arr.append("")

            # temp_arr.append(p)
            out_arr.append(temp_arr)
        print(out_arr)

        footer = ["", "Total Count:"]
        for _ in range(len(out_arr[0][2:-1])):
            footer.append(0)
        footer.append(0)

        for row in out_arr:
            col = row[-1]
            if col == "1":
                footer[2] = footer[2] + 1

        out_arr.append(footer)
        utc_now = datetime.utcnow()

        # Convert UTC time to Indian Standard Time (IST)
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        f_name = f"./dat/{ist_now.strftime('%H:%M')}_{sb_name}_{yr}_Attendance_Report.csv"

        with open(f_name, "a") as exp:
            for row in out_arr:

                for cell in row:
                    exp.write(str(cell) + ",")
                exp.write("\n")

        f_name = f_name.replace(" ", "%20")

        return jsonify({'message': 'File ready', 'file_path': app_link + f_name[24:]})

    except Exception as es:
        print("Only report generation error for cc: {}. Error: {}".format(cc, es))

        return jsonify({'message': 'Invalid credentials'}), 401


@app.route("/only-det-report/<cc>", methods=["POST"])
def only_det_report(cc):
    global class_code, uid, uid_2

    try:
        name, roll, sid, sb_name, yr = [], [], [], [], []
        print("Generating detailed report for cc: {}".format(cc))

        def get_att(cookie_value):
            if uid_2.get(str(cookie_value)):
                cnt = 0
                ttl_cnt = 0

                if class_code.get(cc):
                    ttl_cnt = len(class_code[cc][4])
                    cnt = len(uid_2[str(cookie_value)][cc])

                elif prac_code.get(cc) and cookie_value in prac_code[cc][3]:
                    for e in prac_code[cc][5].keys():

                        if cookie_value in prac_code[cc][5][e]:
                            ttl_cnt = len(prac_date[cc][e])
                            print("e: {}, ttl_cnt: {}".format(e, ttl_cnt))
                            cnt = len(uid_2[str(cookie_value)][cc])

                if ttl_cnt == 0:
                    return 0

                perk = int((cnt / ttl_cnt) * 100)

                return perk

            return 0

        header = ["Roll", "Name"]

        if class_code.get(cc):
            sb_name, yr = class_code[cc][0], class_code[cc][1]
            name, roll, sid = cls_std(cc)

            for date in class_code[cc][4]:
                header.append(date)

        elif prac_code.get(cc):
            sb_name, yr = prac_code[cc][0], prac_code[cc][1]
            name, roll, sid = prac_std(cc)

            for date in prac_code[cc][4]:
                header.append(date)

        # sb_name, yr = class_code[cc][0], class_code[cc][1]
        header.append("Total")
        out_arr = [header]
        # name, roll, sid = cls_std(cc)

        for n, r, i in zip(name, roll, sid):
            p = str(get_att(i))
            temp_arr = [r, n]

            for d in header[2:-1]:
                if d in uid_2[i][cc]:
                    temp_arr.append("1")

                else:
                    temp_arr.append("0")

            temp_arr.append(p)
            out_arr.append(temp_arr)
        print(out_arr)

        footer = ["", "Total Count:"]
        for _ in range(len(out_arr[0][2:-1])):
            footer.append(0)
        footer.append("")

        for row in out_arr:
            for f_ind, col in enumerate(row[2:-1]):
                if col == "1":
                    footer[f_ind + 2] = footer[f_ind + 2] + 1

        out_arr.append(footer)
        utc_now = datetime.utcnow()

        # Convert UTC time to Indian Standard Time (IST)
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        f_name = f"./dat/{ist_now.strftime('%H:%M')}_{sb_name}_{yr}_Detailed_Attendance_Report.csv"

        with open(f_name, "a") as exp:
            for row in out_arr:
                for cell in row:
                    exp.write(str(cell) + ",")

                exp.write("\n")

        f_name = f_name.replace(" ", "%20")

        return jsonify({'message': 'File ready', 'file_path': app_link + f_name[24:]})

    except Exception as es:
        print("Detailed report generation error for cc: {}. Error".format(cc, es))

        return jsonify({'message': 'Invalid credentials'}), 401


@app.route("/wp-yr", methods=['POST'])
def wp_year():
    global class_code, prac_code

    cls_year = ["All"]

    for key in class_code.keys():
        if class_code[key][0] not in cls_year:
            cls_year.append(class_code[key][0])

    for key in prac_code.keys():
        if prac_code[key][0] not in cls_year:
            cls_year.append(prac_code[key][0])

    return jsonify({"year": cls_year})


@app.route("/get-att", methods=["POST"])
def get_att_year():
    global class_code, prac_code, uid

    def get_att(cookie_value, ccc, f_d, t_d):
        f_d = datetime.strptime(f_d, '%Y-%m-%d')
        t_d = datetime.strptime(t_d, '%Y-%m-%d')

        def date_cnt(date_list, f, t):
            d_cnt = 0
            for date in date_list:
                eff_d = datetime.strptime(date.split("_")[0], '%d-%m-%Y')

                if f <= eff_d <= t:
                    d_cnt = d_cnt + 1

            return d_cnt

        def note_date(tt_date, pt_date, f, t):
            tem_ar = []

            for date in tt_date:
                eff_d = datetime.strptime(date.split("_")[0], '%d-%m-%Y')

                if f <= eff_d <= t:
                    if date not in pt_date:
                        tem_ar.append(date)

            return tem_ar

        if uid_2.get(str(cookie_value)):
            cnt = 0
            ttl_cnt = 0
            absent_ = []

            if class_code.get(ccc):
                # ttl_cnt = len(class_code[ccc][4])
                ttl_cnt = date_cnt(class_code[ccc][4], f_d, t_d)
                # cnt = len(uid_2[str(cookie_value)][ccc])
                cnt = date_cnt(uid_2[str(cookie_value)][ccc], f_d, t_d)
                absent_ = note_date(class_code[ccc][4], uid_2[str(cookie_value)][ccc], f_d, t_d)

            elif prac_code.get(ccc) and cookie_value in prac_code[ccc][3]:
                for e in prac_code[ccc][5].keys():
                    if cookie_value in prac_code[ccc][5][e]:
                        # ttl_cnt = len(prac_date[ccc][e])
                        ttl_cnt = date_cnt(prac_date[ccc][e], f_d, t_d)
                        # print("e: {}, ttl_cnt: {}".format(e, ttl_cnt))
                        # cnt = len(uid_2[str(cookie_value)][ccc])
                        cnt = date_cnt(uid_2[str(cookie_value)][ccc], f_d, t_d)
                        absent_ = note_date(prac_date[ccc][e], uid_2[str(cookie_value)][ccc], f_d, t_d)

            # if ttl_cnt == 0:
            #     return "0"
            # perk = int((cnt / ttl_cnt) * 100)

            return ttl_cnt - cnt, absent_

        return 0

    att_temp = {}
    cc = []
    pc = []
    utc_now = datetime.utcnow()

    # Convert UTC time to Indian Standard Time (IST)
    utc_now = pytz.utc.localize(utc_now)
    ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
    date_temp = ist_now.date()  # .strftime("%d-%m-%Y")
    print_data_request = request.get_json()
    batch = print_data_request["batch"]

    print(batch)
    for b in batch:
        for c in class_code:
            if class_code[c][0] == b:
                cc.append(c)

    for b in batch:
        for c in prac_code:
            if prac_code[c][0] == b:
                pc.append(c)

    print(cc, pc)

    for i in cc:
        for s in class_code[i][3]:
            # ab = get_att(s, i, (date_temp - dt.timedelta(days=1)).strftime("%Y-%m-%d"),
            #              date_temp.strftime("%Y-%m-%d"))
            ab, ab_time = get_att(s, i, date_temp.strftime("%Y-%m-%d"),
                                  (date_temp + dt.timedelta(days=1)).strftime("%Y-%m-%d"))

            if ab > 0:

                if att_temp.get(s):
                    att_temp[s][1][class_code[i][1]] = ab_time

                else:
                    att_temp[s] = [uid[s][0], {class_code[i][1]: ab_time}]

    for i in pc:
        for s in prac_code[i][3]:
            # ab = get_att(s, i, (date_temp - dt.timedelta(days=1)).strftime("%Y-%m-%d"),
            #              date_temp.strftime("%Y-%m-%d"))
            ab, ab_time = get_att(s, i, date_temp.strftime("%Y-%m-%d"),
                                  (date_temp + dt.timedelta(days=1)).strftime("%Y-%m-%d"))

            if ab > 0:

                if att_temp.get(s):
                    att_temp[s][1][prac_code[i][1]] = ab_time

                else:
                    att_temp[s] = [uid[s][0], {prac_code[i][1]: ab_time}]

    print(att_temp)

    return jsonify({'att': att_temp})


@app.route("/Xciell/EVRs/DDEg/commit/det/fiielwq")
def commit():
    global backup_cnt, uid, uid_2, class_code, prac_code, prac_date

    _1, _2, _3, _4, _5, _6 = backup_cnt, uid, uid_2, class_code, prac_code, prac_date

    try:
        print(f"structure backed up ({backup_cnt})")

        with open("./enc/c_dat", "w") as b_file:
            b_file.write("uid_2:dict=" + str(uid_2) + "\nprac_code:dict=" + str(prac_code) +
                         "\nclass_code:dict=" + str(class_code) + "\nuid:dict=" + str(uid) +
                         "\nprac_date:dict=" + str(prac_date))
            backup_cnt = backup_cnt + 1

        return jsonify({'success': f"Structure backed ({backup_cnt})"}), 200

    except BaseException as es:
        backup_cnt, uid, uid_2, class_code, prac_code, prac_date = _1, _2, _3, _4, _5, _6

        return jsonify({'error': "structure not backed successfully"}), 401


@app.route("/update-file-receive")
def upd_x_prep():
    return send_file("/Users/anodic_passion/PycharmProjects/X_Prep/x_prep_institute.py", as_attachment=True)


@app.route("/edit")
def edit_profile():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    cookie_value = request.cookies.get('user_id')

    try:
        name = uid[str(cookie_value)][0]
        roll = uid[str(cookie_value)][1]

        return render_template("update.html", NAME=name, ROLL=roll)

    except:

        return render_template("update.html", NAME="", ROLL="")


@app.route("/about")
def about():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    return render_template("about.html")


@app.route("/developer")
def dev():
    user_agent = request.headers.get('User-Agent').lower()
    if "iphone" not in user_agent and "android" not in user_agent:
        return redirect("/docs")
    return render_template("developer.html")


@app.route("/update-acc", methods=["POST"])
def update_prof():
    global uid

    cookie_value = request.cookies.get('user_id')
    data = request.get_json()

    try:
        name = data['name']
        # roll = data['roll']
        password = data['password']
        n_password = data['password_n']
        prev = uid[cookie_value][2]
        roll = uid[cookie_value][1]

        if password == uid[cookie_value][3]:
            print("changing\n", uid[cookie_value], "\nto\n", data)
            uid[cookie_value] = [str(name), str(roll), str(prev), str(n_password)]

            return jsonify({'success': True})

        else:

            return jsonify(), 401

    except:
        print(f"Cannot update profile {cookie_value} for data {data}")

        return jsonify(), 401


@app.route("/200")
def _200():
    return "200"


@app.errorhandler(500)
def internal_server_error_500(e):
    return render_template('500.html'), 500


@app.errorhandler(405)
def internal_server_error_405(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_server_error_404(e):
    return render_template('500.html'), 500


def lst_save():
    global backup_cnt, prac_date, prac_code, class_code, uid, uid_2

    print(backup_cnt, prac_date, prac_code, class_code, uid, uid_2)
    print(f"structure backed up while exiting.")

    with open("./enc/c_dat", "w") as b_file:
        b_file.write("uid_2:dict=" + str(uid_2) + "\nprac_code:dict=" + str(prac_code) +
                     "\nclass_code:dict=" + str(class_code) + "\nuid:dict=" + str(uid) +
                     "\nprac_date:dict=" + str(prac_date))

    backup_cnt = backup_cnt + 1


# @app.route('/report/<cc>')
# def download(cc):
#     global class_code, uid_2, uid
#     # Change the file name accordingly
#     header = ["Roll Number", "Name"]
#     std_lst = class_code[cc][3]
#     for k in std_lst:
#         for i in uid_2[k][cc]:
#             if i not in header:
#                 header.append(i)
#     with open("dat/report.csv", "w") as x:
#         x.write("")
#     csv_file = open("dat/report.csv", "a")
#     # csv_file.write(str(header)[1:-1])
#     for _, i in enumerate(header):
#         if _ == len(header) - 1:
#             csv_file.write(i + "\n")
#         else:
#             csv_file.write(i + ",")
#     temp_lst = []
#     for z in std_lst:
#         temp_lst = []
#         for _ in range(len(header) - 1):
#             temp_lst.append("")
#         temp_lst.insert(0, uid[z][1])
#         temp_lst.insert(1, uid[z][0])
#         for d in uid_2[z][cc]:
#             temp_lst.insert(header.index(d), 1)
#             print(temp_lst)
#         csv_file.write("\n" + str(temp_lst)[1:-1])
#     csv_file.close()
#     print(header)
#     print(temp_lst)
#     file_path = 'static/progress_w.png'
#
#     return send_file(file_path, as_attachment=True)
