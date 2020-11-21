from sqlalchemy.orm import sessionmaker
from model import Task
from datetime import datetime, timedelta


class App:
    EXIT = 0
    ACTIVE = 1
    TODAY_TASKS = 2
    ADD_TASK = 3

    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)()
        self.status = self.ACTIVE

    def run(self):
        while self.status != self.EXIT:
            self.display()
            self.choose_menu()

    @staticmethod
    def display():
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

    def choose_menu(self):
        choice = input()
        print()

        if choice == "0":
            self.status = self.EXIT
        elif choice == "1":
            self.today_tasks()
        elif choice == "2":
            self.week_tasks()
        elif choice == "3":
            self.all_tasks()
        elif choice == "4":
            self.missed_tasks()
        elif choice == "5":
            self.add_task()
        elif choice == "6":
            self.delete_task()
        else:
            print("Invalid input. Try again.")

        print()

    def today_tasks(self):
        self.display_tasks_by_date(datetime.today())

    def week_tasks(self):
        curr_date = datetime.today()
        for i in range(7):
            self.display_tasks_by_date(curr_date, today=False)
            curr_date += timedelta(days=1)
            if i != 6:
                print()

    def all_tasks(self, title="All tasks:"):
        print(title)
        self.display_tasks(self.find_tasks(), with_date=True)

    def missed_tasks(self):
        print("Missed tasks:")
        self.display_tasks(self.find_tasks(missed_by=datetime.today()), with_date=True)

    def add_task(self):
        print("Enter task")
        task = input()
        print("Enter deadline")
        year, month, day = [int(x) for x in input().split("-")]

        self.session.add(Task(task=task, deadline=datetime(year, month, day)))
        self.session.commit()

        print("The task has been added!")

    def delete_task(self):
        self.all_tasks("Choose the number of the task you want to delete:")

        task = self.find_tasks()[int(input()) - 1]
        self.session.delete(task)
        self.session.commit()

        print("The task has been deleted")

    def find_tasks(self, by_date=None, missed_by=None):
        query = self.session.query(Task)

        if by_date:
            query = query.filter(Task.deadline == by_date.date())
        elif missed_by:
            query = query.filter(Task.deadline < missed_by.date())

        return query.order_by(Task.deadline).all()

    def display_tasks_by_date(self, date, today=True):
        weekday = "Today" if today else date.strftime("%A")
        print(f"{weekday} {date.strftime('%d %b')}:")
        self.display_tasks(self.find_tasks(by_date=date))

    @staticmethod
    def display_tasks(tasks, with_date=False):
        if len(tasks) == 0:
            print("Nothing to do!")
            return

        date_info = ""
        for pos, task in enumerate(tasks, start=1):
            if with_date:
                date_info = ". " + task.deadline.strftime("%d %b")
            print(f"{pos}. {task}{date_info}")
