from rich import box
from rich.table import Table


from typing import Union
import shutil
import os 
from time import time 

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


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description if self.description else None,
            'priority': self.priority if self.priority else None,
            'created': self.created if self.created else None,
            'due': self.due if self.due else None,
            'completed': self.completed if self.completed else False
        }


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


        for index, task in enumerate(tasks):
            if task.completed:
                task_name = f'[{task_done_style}]{task.name}[/]'
                task_description = f'[{task_done_style}]{task.description}[/]'
                task_status = '[#61E294]✓[/]'
                task_priority = f'[{task_done_style}]{task.priority}[/]'
                task_created = f'[{task_done_style}]{task.created}[/]'
                task_due = f'[{task_done_style}]{task.due}[/]'
                task_id = f'[{task_done_style}]{str(index + 1)}[/]'
            else:
                task_name = f'[{task_pending_style}]{task.name}[/]'
                task_description = f'[{task_pending_style}]{task.description}[/]'
                task_status = '[#f2b3bb]✗[/]'
                task_priority = f'[{task_pending_style}]{task.priority}[/]'
                task_created = f'[{task_pending_style}]{task.created}[/]'
                task_due = f'[{task_pending_style}]{task.due}[/]'
                task_id = f'[{task_pending_style}]{str(index + 1)}[/]'


            task_table.add_row(
                task_id, 
                task_name, 
                task_description, 
                task_status, 
                task_priority, 
                task_created, 
                task_due
            )

        return task_table
    
    
        



    