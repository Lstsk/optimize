from flask import Flask, render_template, request, jsonify

app = Flask("app")
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_SORT_KEYS"] = False


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "GET":
        return render_template("page.html")
    if request.method == "POST":
        length = request.form["length"]
        width = request.form["width"]
        volumes, dev_str = optimize(float(length), float(width))
        maximum_volume = max(volumes)

        data = {
            "length": length,
            "width": width,
            "volumes": volumes,
            "max_volume": maximum_volume,
            "derivative": dev_str,
        }

        return render_template("page.html", dataout=data)


# calculation
from cmath import sqrt


def optimize(l: int, w: int) -> int:
    outer = l * w
    middle = l * -2 + w * -2
    first = 2 * 2

    dev, dev_str = get_derivative([first, middle, outer])
    print(dev[0])  # in order, first, middle , outer

    a = get_quad(first, middle, outer)
    print(a)

    quadratic_plus = (-dev[1] + sqrt(((dev[1]) ** 2) - 4 * dev[0] * dev[2]).real) / (
        2 * dev[0]
    )
    quadratic_minus = (-dev[1] - sqrt(((dev[1]) ** 2) - 4 * dev[0] * dev[2]).real) / (
        2 * dev[0]
    )

    print(quadratic_plus, quadratic_minus)

    volume = get_volume(quadratic_minus, quadratic_plus)

    return volume, dev_str


def get_quad(first: int, middle: int, outer: int) -> int:
    return f"{first}x^2 {pos_neg(middle)} {middle}x {pos_neg(outer)} {outer}"


def pos_neg(number: int) -> int:
    if number >= 0:
        return "+"
    return ""


def get_derivative(coe: list) -> list:
    dev_list = []
    derivative = ""
    for i in range(len(coe)):
        if i == 0:
            dev_list.append(coe[i] * 3)
            derivative += str(coe[i] * 3) + "x^2"
        elif i == 1:
            dev_list.append(coe[i] * 2)
            if (coe[i] * 2) >= 0:
                derivative += "+" + str(coe[i] * 2) + "x"
            else:
                derivative += str(coe[i] * 2) + "x"

    dev_list.append(coe[2])
    if (coe[2]) >= 0:
        derivative += "+" + str(coe[i])
    else:
        derivative += str(coe[i])

    return dev_list, derivative


def get_volume(x_1, x_2):
    return sorted(
        [x_1 * (8.5 - 2 * x_1) * (11 - 2 * x_1), x_2 * (8.5 - 2 * x_2) * (11 - 2 * x_2)]
    )


app.run(host="0.0.0.0", port=8080)
