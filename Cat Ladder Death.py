import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
import random   
import time

# ข้อมูลผู้เล่น
players = []  # รายชื่อผู้เล่น
positions = []  # ตำแหน่งผู้เล่น
player_colors = []  # สีของผู้เล่นแต่ละคน
current_player = 0  # ผู้เล่นคนปัจจุบัน
cats = {}  # แมว
ladders = {}  # บันได

def generate_cats_and_ladders():  #เพื่อกำหนดตำแหน่งเริ่มต้นของแมวและบันไดโดยไม่ซ้ำกัน
    global cats, ladders
    cat_starts = random.sample(range(2, 100), 9)  # สุ่มตำแหน่งเริ่มต้นของแมว
    ladder_starts = random.sample([i for i in range(2, 100) if i not in cat_starts], 9)  # สุ่มตำแหน่งเริ่มต้นของบันไดที่ไม่ซ้ำกับแมว
    
    cats = {start: random.randint(1, start - 1) for start in cat_starts}
    ladders = {start: random.randint(start + 1, 100) for start in ladder_starts}

def setup_game(): 
    generate_cats_and_ladders()  # สุ่มแมวและบันไดใหม่ทุกเกม
    num_players = simpledialog.askinteger("ขอทราบชื่อคุณหนูได้มั้ยคะ", "ใส่จำนวนผู้เล่น (1-4):", minvalue=1, maxvalue=4)
    if not num_players:
        root.destroy()
        return

    for i in range(num_players):
        name = simpledialog.askstring("ชื่อผู้เล่น", f"ใส่ชื่อคุณหนูคนที่ {i + 1}:")
        players.append(name if name else f"ผู้เล่น {i + 1}")
        positions.append(1)  # เริ่มที่ช่อง 1 ทุกคน
        
        # ให้ผู้เล่นเลือกสีของตัวเอง
        color = colorchooser.askcolor(title=f"เลือกสีสำหรับคุณหนู {players[-1]}")[1]
        player_colors.append(color if color else "#ffcc99")  # ถ้าไม่เลือกจะเป็นสีเริ่มต้น

    label_status.config(text=f"เริ่มเกม!คุณหนู {players[0]} เริ่มก่อน")
    update_board()

def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    label_dice.config(text=f"😺 เขย่าแมว: {dice1} + {dice2} = {total}")
    move_player(total)

def move_player(steps): #เก็บค่าผลรวมจำนวนช่องการเดินของผู้เล่น
    global current_player
    old_position = positions[current_player]
    new_position = old_position + steps

    if new_position > 100:
        label_status.config(text=f"หว้า!คุณหนู {players[current_player]} ทอยได้เกิน 100! ถอยกลับมาก่อนนะ")
        time.sleep(2)
        new_position = 100 - (new_position - 100) 
    
    for _ in range(abs(new_position - old_position)):
        if positions[current_player] < 100:
            if new_position > old_position:
                positions[current_player] += 1
            else:
                positions[current_player] -= 1
            update_board()
            root.update()
            time.sleep(0.2)

    check_special_position()

    if positions[current_player] == 100:
        messagebox.showinfo("ยินดีด้วยคุณหนู!", f"🎉คุณหนู {players[current_player]} เสียเวลาเล่นตั้งนาน!")
        button_roll.config(state="disabled")
    else:
        current_player = (current_player + 1) % len(players)
        label_status.config(text=f"ถึงตาของคุณหนู {players[current_player]}")

def check_special_position(): 
    pos = positions[current_player]

    if pos in cats:
        new_pos = cats[pos]
        positions[current_player] = new_pos
        label_status.config(
            text=f"โอ้ไม่นะ! คุณหนู {players[current_player]} เจอแมวขี้โมโห! จากช่อง {pos} ไปช่อง {new_pos}"
        )
        update_board()
        root.update()
        time.sleep(3.5)

    elif pos in ladders:
        new_pos = ladders[pos]
        positions[current_player] = new_pos
        label_status.config(
            text=f"สุดยอด! คุณหนู {players[current_player]} เจอบันได! ปีนจากช่อง {pos} ไปช่อง {new_pos}"
        )
        update_board()
        root.update()
        time.sleep(3.5)

    update_board()

def update_board():
    colors = ["#262626", "#333333", "#1a1a1a"]  # สีโทนเข้มสำหรับช่อง (ธีมดำ)
    for i in range(10):
        for j in range(10):
            cell_number = 100 - (i * 10 + (j if i % 2 == 0 else 9 - j))
            label = cells[i][j]
            bg_color = colors[(i + j) % 3]
            text = str(cell_number)

            if cell_number in cats:
                text += " 😾"  # ใช้แมวสำหรับตำแหน่งแมว
            elif cell_number in ladders:
                text += " 🪜"

            label.config(text=text, bg=bg_color, fg="white")

            for idx, pos in enumerate(positions):
                if cell_number == pos:
                    label.config(bg=player_colors[idx], fg="white")  # ใช้สีที่ผู้เล่นเลือก

def reset_game():
    global positions, current_player
    positions = [1] * len(players)
    current_player = 0
    generate_cats_and_ladders()
    label_status.config(text=f"เริ่มเกมใหม่คุณหนู {players[0]} เริ่มก่อน")
    label_dice.config(text="😺 เขย่าแมว: -")
    button_roll.config(state="normal")
    update_board()


# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("เกมบันไดแมวมรณะ")
root.geometry("650x750")
root.config(bg="#1a1a1a")  # พื้นหลังสีดำ

# กระดานเกม
frame_board = tk.Frame(root, bg="#1a1a1a")
frame_board.pack(pady=10)

# สร้างตาราง 10x10
cells = []
for i in range(10):
    row = []
    for j in range(10):
        cell_number = 100 - (i * 10 + (j if i % 2 == 0 else 9 - j))
        label = tk.Label(
            frame_board, text=str(cell_number), width=4, height=2,
            borderwidth=2, relief="solid", font=("Arial", 12, "bold"),
            bg="#262626", fg="white"  # สีช่องเริ่มต้นโทนดำ
        )
        label.grid(row=i, column=j, padx=1, pady=1)
        row.append(label)
    cells.append(row)

# ส่วนแสดงผลลูกเต๋าและสถานะ
label_dice = tk.Label(root, text="😺 เขย่าแมว: -", font=("Arial", 16), bg="#1a1a1a", fg="white")
label_dice.pack()

label_status = tk.Label(root, text="ยินดีต้อนรับสู่บันไดแมวมรณะ! รอการตั้งค่า...", font=("Arial", 16), bg="#1a1a1a", fg="white")
label_status.pack()

# ปุ่มทอยลูกเต๋า
button_roll = tk.Button(root, text="เขย่าแมว", command=roll_dice, font=("Arial", 14), bg="#333333", fg="white")
button_roll.pack(pady=5)

# ปุ่มเริ่มเกมใหม่
button_reset = tk.Button(root, text="เริ่มเกมใหม่", command=reset_game, font=("Arial", 14), bg="#4d4d4d", fg="white")
button_reset.pack(pady=5)

# เริ่มการตั้งค่าเกม
root.after(100, setup_game)

# เริ่ม UI 50 555000
root.mainloop()