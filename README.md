# **LiveConfig**

LiveConfig is an in-development python package with the goal of making it easier to develop large scale python programs. LiveConfig will allow a developer to edit variables while a program is running, reducing the need to stop and restart a program.

## **Motivation**

The inspiration for LiveConfig came from a recent computer vision project of mine, where certain values and thresholds needed to be tweaked often, which involved a lot of restarting the program, which took ages each time.

I ended up making a GUI using PyQt for several important thresholds, however this was tedious to do, and adding additional fields was time consuming. Additionally, running PyQt slowed down my program, and it wanted to use the main thread.

I had the idea to make a python package that would allow easy variable editing through an interface of choice. I wanted the setup for the end-user to be as simple as a decorator before a class, or a slight change to a definition.

## **End Goals**

I want LiveConfig to be very simple to use for the end-user, intuitive, and with as little performance overhead as possible.

I will view LiveConfig as "complete" when:

- The user can edit function parameters, variables, and class attributes live.
- The user can choose which interface they wish to use:
  - Web
  - CLI
  - GUI
- The user can save variables to a database or file of choice, which is then loaded on program execution.
- No more than 2 lines of code need to be modified to add/remove a live variable.
- The interface can be disabled easily with a user runtime flag and have little performance impact.
- Sufficient security so others on the network cannot modify variables without permission.
