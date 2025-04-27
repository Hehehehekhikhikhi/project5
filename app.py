from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def generate_usn(branch, num_students):
    return [f"3VY24CS{str(i).zfill(2)}" for i in range(1, num_students + 1)]

def allocate_seats(num_students, num_rooms, rows, benches_per_row):
    usn_list = generate_usn("CS", num_students)
    seating_arrangement = {}

    student_index = 0
    for room_no in range(1, num_rooms + 1):
        if student_index >= num_students:
            break
            
        seating_arrangement[room_no] = np.full((rows, benches_per_row), "Empty", dtype=object)
        
        for bench in range(benches_per_row):
            for row in range(rows):
                if student_index >= num_students:
                    break
                seating_arrangement[room_no][row][bench] = usn_list[student_index]
                student_index += 1
                
    return seating_arrangement

def generate_chart(room_no, seating_arrangement):
    grid = seating_arrangement[room_no]
    rows, benches_per_row = grid.shape

    fig, ax = plt.subplots(figsize=(benches_per_row, rows))
    ax.set_title(f"Room {room_no} Seating Arrangement")

    for row in range(rows):
        for bench in range(benches_per_row):
            seat_text = grid[row][bench]
            ax.text(bench, -row, seat_text, ha='center', va='center', fontsize=8, bbox=dict(boxstyle="round,pad=0.3", edgecolor="black"))

    ax.set_xticks(np.arange(benches_per_row))
    ax.set_yticks(np.arange(-rows, 0))
    ax.set_xticklabels([f"B{i+1}" for i in range(benches_per_row)])
    ax.set_yticklabels([f"R{i+1}" for i in range(rows)])

    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def index():
    seating_arrangement = None
    room_charts = {}

    if request.method == "POST":
        num_students = int(request.form["num_students"])
        num_rooms = int(request.form["num_rooms"])
        rows = int(request.form["rows"])
        benches_per_row = int(request.form["benches_per_row"])

        seating_arrangement = allocate_seats(num_students, num_rooms, rows, benches_per_row)

        for room_no in seating_arrangement.keys():
            room_charts[room_no] = generate_chart(room_no, seating_arrangement)

    return render_template("index.html", seating_arrangement=seating_arrangement, room_charts=room_charts)

if __name__ == "__main__":
    app.run(debug=True)
