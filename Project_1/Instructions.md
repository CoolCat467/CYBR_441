# Project 1
**Course:** CYBR 441
**Instructor:** Nathan Roth
---
This project serves as a light review of some basic data structure concepts.

### Submission Instructions

Create a folder named:
Project1-[Your Name]

Within this folder, create a separate folder for each problem:

- Problem1
- Problem2
- Problem3

Place all files related to a given problem in its corresponding folder.

When complete, submit the Github link as your submission. Ensure that
the project is shared with me so I can view it. If I am unable to view
it, you will not receive credit or a credit penalty.

If you have issues with Github, you may replicate this file structure
locally and submit a zip file of this directory instead.

---

### Style and Documentation Requirements

For this and future projects, be sure to include good style and
documentation. Follow the guildelines of the style guide. If there are
any conflicts between this assignment and the style guide, prioritize
the requirements of the assignment page.

---
### AI Usage

You may use an AI tool only in the creation of the `Student` class as
outlined in the first paragraph of [Problem 1][p1] and the `Node` class
as outlined in the first paragraph of [Problem 2][p2]. All other uses
are prohibited.

## Grading Rubric
I have created test modules that will test your functionality. So,
ensure that you are using the correct syntax so that these modules can
run. Failure to be able to test results in a 25% penalty.

### Problem 1 (9 Points Total)
- Linked list/deque class created: 1 point
- Student class modified: 1 point
- Push front/back, pop front/back, remove, search: 5 points
- Style/documentation: 2 points

### Problem 2 (9 Points Total)
- Node class created as specified: 1 point
- BST class created: 1 point
- Insertion, deletion, and search: 3 points
- Traversals: 2 points
- Style/documentation: 2 point

### Problem 3 (2 Points Total)
- Reflection questions answered: 2 points
---

## Problem 1
### Step 1: Create a Student Class

Create a `Student` class. Each instance of this class should have a
name, age, and gpa field. Ensure that you create and use the appropriate
accessor, mutator, and helper functions.

### Step 2: Implement a Deque
Implement a deque using a linked list of Student objects.
Your deque should support the following operations:
- Push to the front: `addFront()`
- Push to the back: `addBack()`
- Pop from the front: `removeFront()`
- Pop from the back: `removeBack()`
- Search: `search(name) -> returns boolean`
- Remove: `remove(name) -> returns boolean`
Also implement driver code to test your linked list implementation.
---
## Problem 2
Create a binary search tree (BST).
### Step 1: Create a Node Class
Each Node should contain:
- A payload (an integer is fine)
- A left child (optionally empty)
- A right child (optionally empty)
- Applicable methods
### Step 2: Create a Binary Search Tree Class
Implement the following operations:
- Insertion
- Deletion
- Search
### Step 3: Implement Traversals
Include the following tree traversals:
- Inorder
- Preorder
- Postorder
Note: You do not need to implement balancing features, but you are welcome to
include them if desired.
---
## Problem 3
Create a new Python file and answer the following questions using comments only.
### Questions
a. How much time did you spend on these two problems?
b. How would you rate the difficulty of these two problems?
[p1]: #problem-1
[p2]: #problem-2
