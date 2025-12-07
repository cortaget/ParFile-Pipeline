def create_task_list():
    """
    Creates task list using closure. Its create one list of tasks with two properties (description, is_complete) and some functions for manipulate it.

    :return: Dictionary with closure functions
    """

    tasks = []

    def add_task(description : str):
        """
        Add new uncompleted task
        :param description: the task text
        """
        if len(description.strip()) < 0:
            raise Exception("Task must contains one char at least.")

        tasks.append({"description" : description, "is_complete" : False})


    def mark_completed(index : int):
        if index < 0 or index >= len(tasks):
            raise Exception("Index out of range.")

        tasks[index]["is_complete"] = True

    def get_uncompleted():
        """
        Select uncompleted tasks and return it
        :return: list of descriptions in str
        """
        uncompleted = []
        for t in tasks:
            if not t["is_complete"]:
                uncompleted.append(t["description"])
        return uncompleted

    def get_completed():
        return [t for t in tasks if t["is_complete"]]


    def print_tasks():
        for i, t in enumerate(tasks):
            status = "✓" if t["is_complete"] else "✗"
            print(f"{i}. [{status}] {t['description']}")

    return {"add_task" : add_task, "get_uncompleted": get_uncompleted, "mark_completed": mark_completed, "get_completed": get_completed, "print_tasks": print_tasks}


peter_todo = create_task_list()
peter_todo["add_task"]("Vynest smeti")
peter_todo["add_task"]("Uklidit si pokojicek")

print(peter_todo["get_uncompleted"]())
peter_todo["mark_completed"](0)
print(peter_todo["get_uncompleted"]())
print(peter_todo["get_completed"]())
peter_todo["print_tasks"]()