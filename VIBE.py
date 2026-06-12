#Duncan J. Knight III
#CIS261
#VIBE Coding

"""
Student Record Management System
Manages student records including test scores and calculates grades.
"""

import json
import os
from datetime import datetime

class Student:
    """Class to represent a student with three test scores."""
    
    def __init__(self, student_id, name):
        """Initialize a student with ID and name.
        
        Attributes:
            student_id (str): The student's ID
            name (str): The student's name
            test_1 (float): First test score
            test_2 (float): Second test score
            test_3 (float): Third test score
            average (float): Calculated average score
            grade (str): Calculated letter grade
        """
        self.student_id = student_id
        self.name = name
        self.test_1 = None
        self.test_2 = None
        self.test_3 = None
    
    def add_test_1(self, score):
        """Add Test 1 score (0-100)."""
        if 0 <= score <= 100:
            self.test_1 = float(score)
            return True
        return False
    
    def add_test_2(self, score):
        """Add Test 2 score (0-100)."""
        if 0 <= score <= 100:
            self.test_2 = float(score)
            return True
        return False
    
    def add_test_3(self, score):
        """Add Test 3 score (0-100)."""
        if 0 <= score <= 100:
            self.test_3 = float(score)
            return True
        return False
    
    @property
    def average(self):
        """Calculate and return the average test score (float).
        
        Returns:
            float: Average of three test scores, or 0 if tests not complete
        """
        if self.test_1 is None or self.test_2 is None or self.test_3 is None:
            return 0
        return (self.test_1 + self.test_2 + self.test_3) / 3
    
    @property
    def grade(self):
        """Calculate letter grade based on average score (string).
        
        Returns:
            str: Letter grade (A, B, C, D, or F)
        """
        avg = self.average
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    
    def all_scores_entered(self):
        """Check if all three test scores have been entered."""
        return self.test_1 is not None and self.test_2 is not None and self.test_3 is not None
    
    def __str__(self):
        """Return string representation of student."""
        if self.all_scores_entered():
            return f"ID: {self.student_id} | Name: {self.name} | Test 1: {self.test_1:.2f} | Test 2: {self.test_2:.2f} | Test 3: {self.test_3:.2f} | Average: {self.average:.2f} | Grade: {self.grade}"
        else:
            completed = sum([self.test_1 is not None, self.test_2 is not None, self.test_3 is not None])
            return f"ID: {self.student_id} | Name: {self.name} | Tests Entered: {completed}/3"


def validate_score(score_input):
    """Validate and convert score input to float.
    
    Args:
        score_input (str): User input for score
    
    Returns:
        tuple: (is_valid, score_value, error_message)
    """
    try:
        score = float(score_input)
        if 0 <= score <= 100:
            return True, score, None
        else:
            return False, None, "Score must be between 0 and 100."
    except ValueError:
        return False, None, "Invalid input. Please enter a valid number."


def get_score_input(test_number):
    """Get and validate a test score from user input.
    
    Args:
        test_number (int): The test number (1, 2, or 3)
    
    Returns:
        float: Validated test score
    """
    while True:
        try:
            score_input = input(f"Enter Test {test_number} score (0-100): ").strip()
            is_valid, score, error_msg = validate_score(score_input)
            if is_valid:
                return score
            else:
                print(f"✗ {error_msg}")
        except Exception as e:
            print(f"✗ Error: {e}")


def add_student_with_scores(system):
    """Add a student and their test scores to the system.
    
    Args:
        system (StudentRecordSystem): The record management system
    
    Returns:
        bool: True if student was added successfully
    """
    try:
        name = input("Enter student name: ").strip()
        if not name:
            print("✗ Student name cannot be empty.")
            return False
        
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("✗ Student ID cannot be empty.")
            return False
        
        if not system.add_student(student_id, name):
            print(f"✗ Student ID '{student_id}' already exists.")
            return False
        
        print(f"\nEntering test scores for {name}...")
        
        for test_num in range(1, 4):
            score = get_score_input(test_num)
            if not system.add_test_score(student_id, test_num, score):
                print(f"✗ Failed to add Test {test_num} score.")
                return False
            print(f"✓ Test {test_num} score {score:.2f} added successfully.")
        
        print(f"✓ Student '{name}' has been successfully added.")
        return True
    
    except Exception as e:
        print(f"✗ Error adding student: {e}")
        return False


def view_student_record(system):
    """View a single student's record.
    
    Args:
        system (StudentRecordSystem): The record management system
    """
    try:
        student_id = input("Enter student ID: ").strip()
        student = system.find_student(student_id)
        if student:
            print("\n" + "="*100)
            print(student)
            print("="*100)
        else:
            print(f"✗ Student ID '{student_id}' not found.")
    except Exception as e:
        print(f"✗ Error viewing student record: {e}")


def view_all_records_with_stats(system):
    """View all student records and class statistics.
    
    Args:
        system (StudentRecordSystem): The record management system
    """
    try:
        system.display_all_records()
    except Exception as e:
        print(f"✗ Error displaying records: {e}")


def search_students_by_name(system):
    """Search for students by name.
    
    Args:
        system (StudentRecordSystem): The record management system
    """
    try:
        search_name = input("Enter name to search (case-insensitive): ").strip()
        if not search_name:
            print("✗ Search term cannot be empty.")
            return
        
        results = system.search_by_name(search_name)
        if results:
            print(f"\n✓ Found {len(results)} student(s) matching '{search_name}':")
            print("="*100)
            for student in results:
                print(student)
            print("="*100)
        else:
            print(f"✗ No students found matching '{search_name}'.")
    except Exception as e:
        print(f"✗ Error searching for students: {e}")


def save_records(system):
    """Save records to file with error handling.
    
    Args:
        system (StudentRecordSystem): The record management system
    """
    try:
        system.save_to_file("student_grades.txt")
    except Exception as e:
        print(f"✗ Error saving records: {e}")


def load_records(system):
    """Load records from file with error handling.
    
    Args:
        system (StudentRecordSystem): The record management system
    """
    try:
        if system.load_from_file("student_grades.txt"):
            print("✓ Records loaded successfully!")
        else:
            print("✗ No saved records found or file could not be opened.")
    except Exception as e:
        print(f"✗ Error loading records: {e}")


class StudentRecordSystem:
    """System to manage student records."""
    
    def __init__(self):
        """Initialize the student record system."""
        self.students = {}
    
    def add_student(self, student_id, name):
        """Add a new student to the system."""
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
            return True
        return False
    
    def find_student(self, student_id):
        """Find and return a student by ID."""
        return self.students.get(student_id)
    
    def add_test_score(self, student_id, test_number, score):
        """Add a specific test score to a student.
        
        Args:
            student_id (str): The student's ID
            test_number (int): Test number (1, 2, or 3)
            score (float): Test score
        
        Returns:
            bool: True if successful, False otherwise
        """
        student = self.find_student(student_id)
        if not student:
            return False
        
        if test_number == 1:
            return student.add_test_1(score)
        elif test_number == 2:
            return student.add_test_2(score)
        elif test_number == 3:
            return student.add_test_3(score)
        return False
    
    def get_all_students(self):
        """Return all students in the system."""
        return list(self.students.values())
    
    def get_class_average(self):
        """Calculate the average grade for all students with complete scores."""
        students_with_scores = [s for s in self.students.values() if s.all_scores_entered()]
        if not students_with_scores:
            return 0
        total_avg = sum(s.average for s in students_with_scores)
        return total_avg / len(students_with_scores)
    
    def calculate_statistics(self):
        """Calculate and return class statistics.
        
        Returns:
            dict: Contains highest_avg, lowest_avg, class_avg, total_students
        """
        students_with_scores = [s for s in self.students.values() if s.all_scores_entered()]
        
        if not students_with_scores:
            return {
                'highest_avg': 0,
                'lowest_avg': 0,
                'class_avg': 0,
                'total_students': 0,
                'students_with_scores': 0
            }
        
        averages = [s.average for s in students_with_scores]
        
        return {
            'highest_avg': max(averages),
            'lowest_avg': min(averages),
            'class_avg': sum(averages) / len(averages),
            'total_students': len(self.students),
            'students_with_scores': len(students_with_scores)
        }
    
    def search_by_name(self, name):
        """Search for students by name (case-insensitive).
        
        Args:
            name (str): The name to search for
        
        Returns:
            list: List of Student objects matching the search
        """
        search_term = name.lower()
        results = [s for s in self.students.values() if search_term in s.name.lower()]
        return results
    
    def save_to_file(self, filename="student_grades.txt"):
        """Save all student records to a file in pipe-delimited format.
        
        Format: name|id|test1|test2|test3|average|grade
        
        Args:
            filename (str): The filename to save to
        
        Raises:
            IOError: If file cannot be written
        """
        try:
            with open(filename, 'w') as f:
                # Write header
                f.write("name|id|test1|test2|test3|average|grade\n")
                
                # Write each student's record
                for student in self.students.values():
                    if student.all_scores_entered():
                        line = f"{student.name}|{student.student_id}|{student.test_1:.2f}|{student.test_2:.2f}|{student.test_3:.2f}|{student.average:.2f}|{student.grade}\n"
                        f.write(line)
                    else:
                        # Save incomplete records with empty values
                        test1 = f"{student.test_1:.2f}" if student.test_1 is not None else ""
                        test2 = f"{student.test_2:.2f}" if student.test_2 is not None else ""
                        test3 = f"{student.test_3:.2f}" if student.test_3 is not None else ""
                        avg = f"{student.average:.2f}" if student.all_scores_entered() else ""
                        grade = student.grade if student.all_scores_entered() else ""
                        line = f"{student.name}|{student.student_id}|{test1}|{test2}|{test3}|{avg}|{grade}\n"
                        f.write(line)
            
            print(f"✓ Successfully saved {len(self.students)} student record(s) to '{filename}'")
            return True
        except IOError as e:
            print(f"✗ File I/O Error: Unable to save to '{filename}' - {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error saving to file: {e}")
            return False
    
    def load_from_file(self, filename="student_grades.txt"):
        """Load student records from a pipe-delimited file.
        
        Format: name|id|test1|test2|test3|average|grade
        
        Args:
            filename (str): The filename to load from
        
        Returns:
            bool: True if successfully loaded, False otherwise
        
        Raises:
            IOError: If file cannot be read
        """
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            if not lines:
                print(f"✗ File '{filename}' is empty.")
                return False
            
            loaded_count = 0
            
            # Skip header line
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    parts = line.split('|')
                    if len(parts) < 7:
                        continue
                    
                    name = parts[0]
                    student_id = parts[1]
                    
                    if not name or not student_id:
                        continue
                    
                    if student_id not in self.students:
                        self.add_student(student_id, name)
                    
                    student = self.students[student_id]
                    
                    # Load test scores if they exist
                    if parts[2]:
                        try:
                            student.add_test_1(float(parts[2]))
                        except ValueError:
                            pass
                    
                    if parts[3]:
                        try:
                            student.add_test_2(float(parts[3]))
                        except ValueError:
                            pass
                    
                    if parts[4]:
                        try:
                            student.add_test_3(float(parts[4]))
                        except ValueError:
                            pass
                    
                    loaded_count += 1
                
                except Exception as line_error:
                    print(f"⚠ Warning: Could not parse line: {line} - {line_error}")
                    continue
            
            if loaded_count > 0:
                print(f"✓ Successfully loaded {loaded_count} student record(s) from '{filename}'")
            
            return True
        
        except IOError as e:
            print(f"✗ File I/O Error: Unable to read '{filename}' - {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error loading from file: {e}")
            return False
    
    def display_all_records(self):
        """Display all student records in a formatted table."""
        if not self.students:
            print("\nNo students in the system.")
            return
        
        print("\n" + "="*135)
        print("STUDENT RECORDS - FORMATTED TABLE")
        print("="*135)
        print(f"{'ID':<10} {'Name':<20} {'Test 1':<12} {'Test 2':<12} {'Test 3':<12} {'Average':<12} {'Grade':<8} {'Status':<20}")
        print("-"*135)
        
        for student in self.students.values():
            if student.all_scores_entered():
                status = "Complete"
                print(f"{student.student_id:<10} {student.name:<20} {student.test_1:<12.2f} {student.test_2:<12.2f} {student.test_3:<12.2f} {student.average:<12.2f} {student.grade:<8} {status:<20}")
            else:
                completed = sum([student.test_1 is not None, student.test_2 is not None, student.test_3 is not None])
                status = f"Incomplete ({completed}/3)"
                print(f"{student.student_id:<10} {student.name:<20} {'---':<12} {'---':<12} {'---':<12} {'---':<12} {'---':<8} {status:<20}")
        
        print("="*135)



def display_menu():
    """Display the main menu."""
    print("\n" + "="*40)
    print("STUDENT RECORD MANAGEMENT SYSTEM")
    print("="*40)
    print("1. Add Student")
    print("2. View Student Record")
    print("3. Display All Students (Table)")
    print("4. Class Statistics")
    print("5. Search Student by Name")
    print("6. Save Records")
    print("7. Exit")
    print("="*40)


def main():
    """Main program loop."""
    system = StudentRecordSystem()
    
    print("\n" + "="*50)
    print("STUDENT RECORD MANAGEMENT SYSTEM")
    print("="*50)
    
    # Load records from file at startup
    if system.load_from_file("student_grades.txt"):
        pass  # Success message already printed by load function
    
    while True:
        display_menu()
        try:
            choice = input("Select an option (1-7) or press ESC to exit: ").strip()
            
            # Check for ESC key or exit commands
            if choice == '\x1b' or choice.upper() == 'ESC' or choice == '7':
                print("\n" + "="*50)
                print("Saving records before exit...")
                system.save_to_file("student_grades.txt")
                print("Thank you for using the Student Record Management System.")
                print("="*50)
                break
            
            if choice == '1':
                # Add Student and Test Scores
                print("\n--- Add Student ---")
                add_student_with_scores(system)
            
            elif choice == '2':
                # View Individual Student Record
                print("\n--- View Student Record ---")
                view_student_record(system)
            
            elif choice == '3':
                # Display All Students (Table)
                print("\n--- Display All Students (Table) ---")
                view_all_records_with_stats(system)
            
            elif choice == '4':
                # Class Statistics
                print("\n--- Class Statistics ---")
                stats = system.calculate_statistics()
                if stats['students_with_scores'] > 0:
                    print("\nClass Statistics")
                    print("="*30)
                    print(f"Total Students: {stats['total_students']}")
                    print(f"Students with Complete Scores: {stats['students_with_scores']}")
                    print(f"Highest Average: {stats['highest_avg']:.2f}")
                    print(f"Lowest Average: {stats['lowest_avg']:.2f}")
                    print(f"Class Average: {stats['class_avg']:.2f}")
                    print("="*30)
                else:
                    print("✗ No complete student scores available to calculate statistics.")
            
            elif choice == '5':
                # Search Student by Name
                print("\n--- Search Student by Name ---")
                search_students_by_name(system)
            
            elif choice == '6':
                # Save Records
                print("\n--- Save Records ---")
                save_records(system)
            
            else:
                print("✗ Invalid option. Please select 1-7.")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*50)
            print("Program interrupted. Saving records...")
            system.save_to_file("student_grades.txt")
            print("Thank you for using the Student Record Management System.")
            print("="*50)
            break
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")
            print("Please try again or contact support.")


if __name__ == "__main__":
    main()