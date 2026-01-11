from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory task list
TASKS = [
    {'id': 1, 'title': 'Learn Flask', 'status': 'Completed', 'priority': 'High'},
    {'id': 2, 'title': 'Build To-Do App', 'status': 'In Progress', 'priority': 'Medium'},
    {'id': 3, 'title': 'Push to GitHub', 'status': 'Pending', 'priority': 'Low'},
]

def get_task(task_id):
    return next((t for t in TASKS if t["id"] == task_id), None)

def get_next_id():
    return max((task["id"] for task in TASKS), default=0) + 1

# Home page - list all tasks (+ simple stats)
@app.route("/")
def index():
    total = len(TASKS)
    completed = sum(1 for t in TASKS if t["status"] == "Completed")
    in_progress = sum(1 for t in TASKS if t["status"] == "In Progress")
    pending = sum(1 for t in TASKS if t["status"] == "Pending")
    return render_template(
        "index.html",
        tasks=TASKS,
        total=total,
        completed=completed,
        in_progress=in_progress,
        pending=pending,
    )

# Add task page (GET form + POST submit)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        status = request.form.get("status", "Pending")
        priority = request.form.get("priority", "Medium")

        if title:
            TASKS.append(
                {
                    "id": get_next_id(),
                    "title": title,
                    "status": status,
                    "priority": priority,
                }
            )
        return redirect(url_for("index"))

    return render_template("add.html")

# View single task details
@app.route("/task/<int:id>")
def task_detail(id):
    task = get_task(id)
    if task is None:
        return "Task not found", 404
    return render_template("task.html", task=task)

# Edit task (optional, makes app nicer)
@app.route("/task/<int:id>/edit", methods=["GET", "POST"])
def edit_task(id):
    task = get_task(id)
    if task is None:
        return "Task not found", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        status = request.form.get("status", task["status"])
        priority = request.form.get("priority", task["priority"])
        if title:
            task["title"] = title
        task["status"] = status
        task["priority"] = priority
        return redirect(url_for("task_detail", id=id))

    return render_template("add.html", task=task, is_edit=True)

# Delete task
@app.route("/task/<int:id>/delete", methods=["POST"])
def delete_task(id):
    global TASKS
    TASKS = [t for t in TASKS if t["id"] != id]
    return redirect(url_for("index"))

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# Bonus: filter by priority
@app.route("/priority/<name>")
def filter_priority(name):
    filtered = [t for t in TASKS if t["priority"].lower() == name.lower()]
    return render_template("index.html",
                           tasks=filtered,
                           total=len(filtered),
                           completed=sum(1 for t in filtered if t["status"] == "Completed"),
                           in_progress=sum(1 for t in filtered if t["status"] == "In Progress"),
                           pending=sum(1 for t in filtered if t["status"] == "Pending"),
                           priority_filter=name.capitalize())

if __name__ == "__main__":
    app.run(debug=True)
