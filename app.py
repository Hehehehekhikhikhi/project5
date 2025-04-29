import matplotlib.pyplot as plt
import math

def generate_usn(student_id):
    return f"3VY24CS{str(student_id).zfill(3)}"

def create_seating_arrangement(num_students, num_rooms, room_capacity, rows, benches_per_row):
    seating_chart = {}
    students_per_room = math.ceil(num_students / num_rooms)  # Ensures equal distribution

    student_id = 1
    for room in range(1, num_rooms + 1):
        seating_chart[room] = []
        for col in range(benches_per_row):  # Benches (Columns)
            for row in range(rows):  # Rows
                if student_id > num_students:
                    break
                usn = generate_usn(student_id)
                seat_number = f"R{room}-S{student_id}"
                seating_chart[room].append((row + 1, col + 1, seat_number, usn))
                student_id += 1
                if student_id > (students_per_room * room):
                    break  # Stops when the room has reached its equal share of students

    return seating_chart

def plot_seating_chart(seating_chart):
    for room, seats in seating_chart.items():
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_title(f"Room {room} Seating Arrangement", fontsize=12)

        for row, col, seat_num, usn in seats:
            ax.text(col, row, f"{seat_num}\n{usn}", ha='center', va='center', fontsize=8,
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.3'))

        ax.set_xlim(0, max([col for _, col, _, _ in seats]) + 1)
        ax.set_ylim(0, max([row for row, _, _, _ in seats]) + 1)
        ax.set_xticks(range(1, max([col for _, col, _, _ in seats]) + 1))
        ax.set_yticks(range(1, max([row for row, _, _, _ in seats]) + 1))
        ax.grid(True)
        
        plt.gca().invert_yaxis()  # Aligns top-to-bottom like seating layout
        plt.show()

# Get user inputs
num_students = int(input("Enter total number of students: "))
num_rooms = int(input("Enter total number of rooms: "))

room_capacity = 25  # Fixed room capacity
rows = 4
benches_per_row = 7

# Generate and display seating arrangement
seating_chart = create_seating_arrangement(num_students, num_rooms, room_capacity, rows, benches_per_row)
plot_seating_chart(seating_chart)
