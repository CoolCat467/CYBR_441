# Project 2: Uninformed Search

**Course:** CYBR 441

**Instructor:** Nathan Roth

---

This project serves as an implementation of breadth-first and
depth-first search in an artificial intelligence context.  You will be
solving the Vacuum World problem.

### Submission Instructions

Create a folder named:

Project2-[Your Name]

Within this folder, create a separate folder for each problem:
- Problem1
- Problem2

Place all files related to a given problem in its corresponding folder.

When complete, submit the Github link as your submissions. Ensure that
the project is shared with me so I can view it. If I am unable to view
it, you will not receive credit or a credit penalty.

If you have issues with Github, you may replicate this file structure
locally and submit a zip file of this directory instead.

---

### Style and Documentation Requirements

For this and future projects, be sure to include good style and
documentation. Follow the guildelines of the style guide.  If there are
any conflicts between this assignment and the style guide, prioritize
the requirements of the assignment page.

### AI Usage
You may not use any AI tools in this project.

## Grading Rubric

There are no automated testing modules for this.  I will run each of
your programs individually.  Because of the nature of grading a large
number of programs in an appropriate time, I will not spend time
debugging your program if it does not work.

### Problem 1 (28 points total)

- `Node` design and state representation: 2 points
- `Graph` design and implementation: 2 points
- `World` class correctly sets up the state space: 4 points
- BFS function works correctly: 6 points
- DFS function works correctly: 6 points
- GUI displays the correct path (actions and states): 2 points
- Style/documentation/misc: 4 points
- Extension to 3 cells: 2 points

### Problem 2: 2 points total

- Reflection questions answered: 2 points

---

## Problem 1

Vacuum World is a toy search problem that demonstrates the basics of
problem-solving by searching.  You are going to implement this in code.
In this assignment, you will design and implement a software solution
that models the Vacuum World environment and applies search algorithms
to identify a path from an initial state to a goal state.

The application should allow a user to enter a starting state ID, select
a search algorithm, and view the resulting solution path.  The initial
implementation will focus on a 2-cell Vacuum World.

You are provided with a code skeleton that has the core classes and a
partially implemented GUI.  Your task is to extend the existing codebase
to correctly model the problem and implement the problem-solving
(search) capability.

As written, the `Interface` file contains the main functionality.  When
run, a GUI will appear with several options for you.  The controls and
event handlers are already provided, so if you follow the function
signatures as provided in that file, few or no changes to the GUI should
be necessary.

### Step 1: Create the Search Space
I recommend you complete this portion on paper.  You need to list all
possible states of this problem, and the actions that will lead from one
to another.  Then, use a digital tool to create visuals of each state.
Take a screenshot of each so you can display the image in the program.

### Step 2: Update the `Node` and `Graph` Classes
A basic skeleton is given to you in the `Node` and `Graph` classes.
Evaluate what information is necessary to accurately represent a state
within the Vacuum World environment. Update these classes to include
these additional characteristics.  Especially pay attention to the
`Node` class, as this essentially represents each state.  What
information should be stored in each state?

### Step 3: Update a `World` Class
You are given a class called `World`.  In here, you need to actually
create the states, load them with applicable properties, link them
together with the correct actions, and place them in a `Graph` object.
Essentially, you are implementing what you drew in Step 1.

### Step 4: Implement BFS and DFS
In your `Graph` class, create and implement functions that perform
breadth-first and depth-first search.  For each of these, the return
value should be the sequence of states that are visited, if a solution
exists.  Pay attention to the `Interface` class as this will determine
your syntax for these classes.

### Step 5: Document
Create a readme file that explains how to run your application.  You
should list all of the possible states as well as their individual ID's
so the user can select which one they want to start at.

### Step 6: Extend
As an optional extension, allow the user to run a 3-cell Vacuum World.
All other steps should be the same.  Note that not doing this will only
result in a small deduction.


---

## Problem 2

Create a new Python file and answer the following questions using
comments only.

### Questions

a. How much time did you spend on these two problems?

b. How would you rate the difficulty of these two problems?
