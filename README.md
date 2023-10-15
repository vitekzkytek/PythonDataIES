# Data Processing in Python (JEM207)

The course site for the Data Processing in Python from [IES](http://ies.fsv.cuni.cz/). See information on [SIS](https://is.cuni.cz/studium/predmety/index.php?do=predmet&kod=JEM207). The course is taught by [Martin Hronec](mailto:martin.hronec@fsv.cuni.cz), [Jan Šíla](mailto:jan.sila@fsv.cuni.cz) and 
[Alena Pavlovova](mailto:alena.pavlova@fsv.cuni.cz).

## Communication
Please direct all questions at [Alena Pavlova](mailto:alena.pavlova@fsv.cuni.cz) only. 

## FAQ - pre semester

* If you are on **waiting list** there is *nothing* we can do to enroll you. We managed to master somehow `python`, but SIS is something else. We follow the rules. Students usully drop from the course during the first week of the semester so **there is a good chance** you will be able to register.

* The course is held **in-person** and there is by default **no online** option.

* If you are junior to last BSc year/ MSc level, please consider your coding skills. If you just started coding (R or anything else), please consider signing up later on. We will still be here (hopefully) next semester as well.
* You are free to drop the course at any time until 08/10. If you decide to do so after this date, please get in touch with [Alena Pavlova](mailto:alena.pavlova@fsv.cuni.cz). However, please be aware that after 10/11, discontinuation will no longer be an option.
* If you decide to *drop out after the 2-week grace period*, note that if you submit homework, you will be awarded "F" mark following the university guidelines. Please, do consider this as well with regards to staying in the course. There might be others waiting for the spot.

# Schedule

| Week | Date   | L/S | Topic                                      | Lecturer            | Deadline         |
|------|--------|-----|--------------------------------------------|---------------------|------------------|
| 1    | 2.10.  | S   | Seminar 0: Setup (Jupyter, VScode, Git, OS basics) | Martin      |                  |
| 1    | 3.1    | L   | Python basics                              | Martin              |                  |
| 2    | 10.10. | L   | Python basics II                           | Jan                 |                  |
| 3    | 16.10. | S   | Seminar 1: Basics                          | Alena               | HW 1             |
| 3    | 17.10. | L   | Numpy                                      | Jan                 |                  |
| 4    | 24.10. | L   | Pandas I                                   | Martin              |                  |
| 5    | 30.10. | S   | Seminar 2: Numpy & pandas                  | Alena               | HW 2             |
| 5    | 31.10. | L   | Pandas II + Matplotlib                     | Martin              |                  |
| 6    | 7.11.  | L   | Data formats, APIs                         | Jan                 |                  |
| 7    | 13.11. | S   | Seminar 3: Data formats & APIs             | Alena               | HW 3             |
| 7    | 14.11. | L   | Algorithmic problem solving                | Jan                 |                  |
| 8    | 21.11. | -   | MIDTERM                                    | Alena, Jan & Martin |                  |
| 9    | 27.11. | S   | MIDTERM solution                           | Alena               |                  |
| 9    | 28.11. | L   | Data science                               | Martin              | Project proposal |
| 10   | 5.12.  | L   | How to code (avoiding spaghetti code)      | Martin              | Topic approved   |
| 11   | 11.12. | S   | Seminar 5: Data science case-study         | Alena               |                  |
| 11   | 12.12. | L   | Databases                                  | Jan                 |                  |
| 12   | 19.12. | L   | Guest lecture (TBA) + Python Beer          | Alena, Jan & Martin |                  |
| 2.1. | -      | -   | WiP: Project consultations                 | Alena, Jan & Martin |                  |
| 9.1. | -      | -   | WiP: Project consultations                 | Alena, Jan & Martin |                  |


# Course requirements
The requirements for passing the course are homeworks (5pts), the midterm (25pts), work in-progress-presentation (10pts), and the final project - including the final delivery presentation (60pts).
At least 50% from the homeworks assignments and work-in-progress presentation is required for passing the course.

## Final project (60%)
* Students in teams by 2
* Deadline for topic approval: 5th of December 2023
* Deadline: 9th of February 2024

### Projects' Evaluation critera
* Use of git by both - 5pts
    * meaningful commit messages
* pythonic code principles - 5 pts
    * code is more often read than written, EAFP
* runability - 15 pts
    * by far the most important one! Project needs to run from scratch after installing versioned requirements.
        * provide requirements.txt file with specific versions of packages (use pip freeze to get it), and specify your precise Python version. 
* code structure - 15 pts
    * functions (classes), properly named variables
* README, documentation - 5 pts
* analysis, visualization - 15 pts
    * highlight key poins of your projet

## Project work - presentation (10%)
* Presentation of work-in-progress related to the final project.
* Prepare questions, understand the goals of your project

## Midterm exam (25%)
Live coding (80 minutes), "open browser", no collaboration between the students. More details during the lecture week before

## Homework Assignments (5%)

* Create leetcode.com account
* You are expected to submit in a specified Google form: https://forms.gle/jkoRpZ7yZoQYSYjY7
    * link to the problem
    * Print page showing your solution and submission statistics 
        *Like this: [Path Sum III - Submission Detail - LeetCode.pdf](https://github.com/vitekzkytek/PythonDataIES/files/12743340/Path.Sum.III.-.Submission.Detail.-.LeetCode.pdf)


    * Plain text of your script (in python 3!)
* Rules:
    * Do not just copy the public solutions or what ChatGPT tells you. We will make an effort to find out and you will be penalized as per academic integrity guidelines. Do not try to get easy points by cheating, it is not the purpose of the HW tasks.
    * Have fun and try to beat the world!
    * Your submission will ideally be accepted by leetcode, but send us your best attempt regardless, you can still get the points. If anything, try to optimize run time, do not worry about memory.
    * You will struggle, but if you solve many of those, your next stop is Google cafeteria as an employee!
    * If you cannot decide, there is a shuffle button which will pick something for you.

* HW 1 (1 pts):
    * Choose one of the easy problems. Have fun and send us how far you have got!
        * Example: [Two Sum](https://leetcode.com/problems/two-sum/)
* HW 2 (2 pts):
    * One easy or one Medium problem
        * Example: Medium: [Parentheses](https://leetcode.com/problems/generate-parentheses/)
* HW 3 (2 pts):
    * One easy or one Medium problem
    * Must be from [Pandas set of problems](https://leetcode.com/problemset/pandas/)


# Prerequisities

The course is designed for students who have at least some basic coding experience. It does not need to be very advanced, but they should be aware of concepts such as ` for ` loop ,`if` and `else`,`variable` or `function`.

No knowledge of Python is required to enter the course.

# Credits
Passing the course is rewarded with 5 ECTS credits.
