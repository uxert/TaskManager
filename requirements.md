I want to build my own task manager. 
I want it to be self-hosted, without relying on external providers.

# MOSCOW

## MUST
- [x] allow for creation of tasks
- [x] have some command-line editor that will allow user to perform basic CRUD on their tasks
- [x] of course persist the tasks in some database (probably just relational for the time being)
- [x] be able to register many users and login them, so that each user has his own tasks
- [x] have a secure user authentication, so that you cannot see tasks on other accounts
- [x] tasks have to have assignable attributes, AT THE VERY LEAST name, importance, expected length and some custom comment
- [ ] be fully self-hosted
- [x] have GUI at least for login and the most basic task CRUD 


## SHOULD
- [ ] have a fully interactive GUI view, where user could perform all possible CRUD operations on their tasks purely in graphical interface
- [ ] have a pretty, GUI callendar view, where each task takes some space (because it has a defined expected length). When a few tasks are overlapping, it should remain clear which task is which
- [ ] have counter of remaining/inprogress/done tasks for custom time period
- [ ] allow to share (read-only) tasks via shareable urls

## COULD
- [ ] the callendar view could be interactive too and allow user to edit tasks from there
- [ ] allow to collaborate on tasks:
  - allow to share (read and edit) tasks via shareable urls
  - allow to have conversation between users:
      - in general
      - for a task they are collaborating on
- [ ] "split" a task into smaller sub-tasks:
  -  create a new full task inside another task
  -  fast create some basic version of a subtask (like one only with a name, length and a comment)
     
## WON'T (this time)
- [ ] have some fancy magic algorithm that will plan your tasks in correct order for you
