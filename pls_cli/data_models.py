from rich import box
from rich.table import Table


from typing import Union
import shutil
import os 
import time
from enum import Enum

msg_pending_style = os.getenv('PLS_MSG_PENDING_STYLE', '#61E294')
table_header_style = os.getenv('PLS_TABLE_HEADER_STYLE', '#d77dd8')
task_done_style = os.getenv('PLS_TASK_DONE_STYLE', '#a0a0a0')
task_pending_style = os.getenv('PLS_TASK_PENDING_STYLE', '#bb93f2')
header_greetings_style = os.getenv('PLS_HEADER_GREETINGS_STYLE', '#FFBF00')
quote_style = os.getenv('PLS_QUOTE_STYLE', '#a0a0a0')
author_style = os.getenv('PLS_AUTHOR_STYLE', '#a0a0a0')


class Priority(Enum): 
    LOW = 1 
    MEDIUM = 2
    HIGH = 3
    SUPER_HIGH = 4



class Task: 
    def __init__(self, 
                 task_id: int, 
                 task_name: str, 
                 task_description: str = None, 
                 task_priority: int = None, 
                 task_created: str = None, 
                 task_due: str = None, 
                 task_completed: bool = False):
        
        self.id = task_id
        self.name = task_name
        self.description = task_description
        self.priority = task_priority
        self.created = task_created if task_created else str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.due = task_due
        self.completed = task_completed
        self.subtasks = [] 
        self.parent = None


    def edit(self, 
             task_name: str = None, 
             task_description: str = None, 
             task_priority: int = None, 
             task_due: str = None, 
             task_completed: bool = None):
        
        if task_name:
            self.name = task_name
        if task_description:
            self.description = task_description
        if task_priority:
            self.priority = task_priority
        if task_due:
            self.due = task_due
        if task_completed:
            self.completed = task_completed


    def addSubtask(self, subtask):
        subtask.parent = self.id 
        self.subtasks.append(subtask.id)


    def removeSubtask(self, subtask_id):
        self.subtasks.remove(subtask_id)



    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description if self.description else None,
            'priority': self.priority if self.priority else None,
            'created': self.created if self.created else None,
            'due': self.due if self.due else None,
            'completed': self.completed if self.completed else False, 
            'subtasks': self.subtasks if self.subtasks else [],
            'parent': self.parent if self.parent else None
        }
    
    @classmethod
    def from_dict(cls, task_dict: dict):
        id = task_dict['id']
        name = task_dict['name']
        description = task_dict.get('description', None)
        priority = task_dict.get('priority', None)
        created = task_dict.get('created', None)
        due = task_dict.get('due', None)
        completed = task_dict.get('completed', False)
        subtasks = [subtask_id for subtask_id in task_dict.get('subtasks', [])] 
        parent = task_dict.get('parent', None)
        
        task = cls(id, name, description, priority, created, due, completed)
        
        task.subtasks = subtasks
        task.parent = parent 

        return task  

class TaskTable: 
    def __init__(self, tasks: list[Task]): 
        self.task_table = self._build_table(tasks) 


    def _build_table(self, tasks: list[Task]): 
        task_table = Table(
            header_style=table_header_style,
            style=table_header_style,
            box=box.SIMPLE_HEAVY,
        )

        task_table.add_column('ID', justify='center')
        task_table.add_column('Name', justify='center')
        task_table.add_column('Description', justify='center')
        task_table.add_column('Status', justify='center')
        task_table.add_column('Priority', justify='center')
        task_table.add_column('Created', justify='center')
        task_table.add_column('Due', justify='center')
        task_table.add_column('Subtasks', justify='center')
        task_table.add_column('Parent', justify='center')


        for index, task in enumerate(tasks):
            self._add_task(task, task_table, tasks)


        return task_table
    
    def _add_task(self, task: Task, table, tasks: list[Task]): 
        if task.completed:
            task_name = f'[{task_done_style}]{task.name}[/]'
            task_description = f'[{task_done_style}]{task.description}[/]'
            task_status = '[#61E294]✓[/]'
            task_priority = f'[{task_done_style}]{task.priority}[/]'
            task_created = f'[{task_done_style}]{task.created}[/]'
            task_due = f'[{task_done_style}]{task.due}[/]'
            task_id = f'[{task_done_style}]{str(task.id)}[/]'
            task_subtasks_counter = f'[{task_done_style}]{len(task.subtasks)}/{len(task.subtasks)}[/]'
            task_parent = f'[{task_done_style}]{task.parent}[/]' if task.parent else '[#a0a0a0]None[/]'
        else:
            task_name = f'[{task_pending_style}]{task.name}[/]'
            task_description = f'[{task_pending_style}]{task.description}[/]'
            task_status = '[#f2b3bb]✗[/]'
            task_priority = f'[{task_pending_style}]{task.priority}[/]'
            task_created = f'[{task_pending_style}]{task.created}[/]'
            task_due = f'[{task_pending_style}]{task.due}[/]'
            task_id = f'[{task_pending_style}]{str(task.id)}[/]'

            num_done_subtasks = len([subtask for subtask in tasks if subtask.completed and subtask.parent == task.id])
            task_subtasks_counter = f'[{task_pending_style}]{num_done_subtasks}/{len(task.subtasks)}[/]'
            task_parent = f'[{task_pending_style}]{task.parent}[/]' if task.parent else '[#a0a0a0]None[/]'
            
        table.add_row(
                task_id, 
                task_name, 
                task_description, 
                task_status, 
                task_priority, 
                task_created, 
                task_due, 
                task_subtasks_counter,
                task_parent
            )


    

def get_subtasks(task: Task, tasks: list[Task]) -> list[Task]:
    subtask_ids = task.subtasks
    subtasks = list(filter(lambda t: t.id in subtask_ids, tasks))
    return subtasks


from rich.rule import Rule
from rich.console import Console
from rich.align import Align

console = Console()


def get_terminal_full_width() -> int:
    return shutil.get_terminal_size().columns


def get_terminal_center_width() -> int:
    return shutil.get_terminal_size().columns // 2



def center_print(
    text, style: Union[str, None] = None, wrap: bool = False
) -> None:
    """Print text with center alignment.
    Args:
        text (Union[str, Rule, Table]): object to center align
        style (str, optional): styling of the object. Defaults to None.
    """

    width = get_terminal_full_width() if wrap else get_terminal_full_width()

    if isinstance(text, Rule):
        console.print(text, style=style, width=width)
    else:
        console.print(Align.center(text, style=style, width=width))
    
    
    
        
if __name__ == "__main__":
    task1 = Task(1, 'Task 1', 'This is task 1', 'HIGH', '2021-09-01', '2021-09-02', False)
    task2 = Task(2, 'Task 2', 'This is task 2', 'HIGH', '2021-09-01', '2021-09-02', False)
    task3 = Task(3, 'Task 3', 'This is task 3', 'HIGH', '2021-09-01', '2021-09-02', True)
    task4 = Task(4, 'Task 4', 'This is task 4', 'HIGH', '2021-09-01', '2021-09-02', True)
    task5 = Task(5, 'Task 5', 'This is task 5', 'HIGH', '2021-09-01', '2021-09-02', False)
    
    task1.addSubtask(task2)
    task1.addSubtask(task3)
    task2.addSubtask(task4)
    tasks = [task1, task2, task3, task4, task5]
    task_table = TaskTable(tasks)


    print(task1.to_dict())
    
    center_print(task_table.task_table)
