import tkinter as tk

def on_key_release(event):
    search_term = entry.get()
    if search_term:
        search_results = [student_id for student_id in student_ids if search_term.lower() in student_id.lower()]
    else:
        search_results = student_ids
    update_listbox(search_results)

def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_student = listbox.get(selected_index)
        entry.delete(0, tk.END)
        entry.insert(0, selected_student)

def update_listbox(results):
    listbox.delete(0, tk.END)
    for student_id in results:
        listbox.insert(tk.END, student_id)

root = tk.Tk()
root.title("Search Student ID")

# Danh sách mã số sinh viên
student_ids = [
    "2021001",
    "2021002",
    "2021003",
    "3021004",
    "5021005",
    # Thêm các mã số sinh viên khác nếu cần
]

# Tạo entry widget
entry = tk.Entry(root, width=30)
entry.pack(padx=10, pady=10)

# Tạo listbox widget để hiển thị gợi ý
listbox = tk.Listbox(root, width=30)
listbox.pack(padx=10, pady=10)

entry.bind("<KeyRelease>", on_key_release)
listbox.bind("<<ListboxSelect>>", on_select)

# Hiển thị toàn bộ danh sách mã số sinh viên khi ban đầu
update_listbox(student_ids)

root.mainloop()
