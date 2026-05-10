#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql.h>
#include "db.h"

void studentRegister();
void lecturerRegister();

void studentLogin();
void lecturerLogin();

void adminLogin();

void submitStudentComplaint(int studentId);
void submitLecturerComplaint(int lecturerId);

void trackStudentComplaint(int studentId);
void trackLecturerComplaint(int lecturerId);

void adminDashboard();

int main()
{
    int choice;

    while(1)
    {
        printf("\n=====================================\n");
        printf(" COLLEGE COMPLAINT MANAGEMENT SYSTEM\n");
        printf("=====================================\n");

        printf("1. Student Register\n");
        printf("2. Lecturer Register\n");
        printf("3. Student Login\n");
        printf("4. Lecturer Login\n");
        printf("5. Admin Login\n");
        printf("6. Exit\n");

        printf("Enter Choice: ");
        scanf("%d", &choice);

        switch(choice)
        {
            case 1:
                studentRegister();
                break;

            case 2:
                lecturerRegister();
                break;

            case 3:
                studentLogin();
                break;

            case 4:
                lecturerLogin();
                break;

            case 5:
                adminLogin();
                break;

            case 6:
                exit(0);

            default:
                printf("Invalid Choice\n");
        }
    }

    return 0;
}

void studentRegister()
{
    MYSQL *conn = connectDB();

    char name[100];
    char usn[50];
    char email[100];
    char password[100];
    int departmentId;

    printf("\n===== STUDENT REGISTER =====\n");

    printf("Enter Name: ");
    scanf(" %[^\n]", name);

    printf("Enter USN: ");
    scanf("%s", usn);

    printf("Enter Email: ");
    scanf("%s", email);

    printf("Enter Password: ");
    scanf("%s", password);

    printf("Department ID: ");
    scanf("%d", &departmentId);

    char query[1000];

    sprintf(query,
    "INSERT INTO students(student_name,usn,email,password,department_id) VALUES('%s','%s','%s','%s',%d)",
    name,usn,email,password,departmentId);

    if(mysql_query(conn, query))
    {
        printf("Registration Failed\n");
    }
    else
    {
        printf("Student Registered Successfully\n");
    }

    mysql_close(conn);
}

void lecturerRegister()
{
    MYSQL *conn = connectDB();

    char name[100];
    char employeeId[50];
    char email[100];
    char password[100];
    int departmentId;

    printf("\n===== LECTURER REGISTER =====\n");

    printf("Enter Name: ");
    scanf(" %[^\n]", name);

    printf("Employee ID: ");
    scanf("%s", employeeId);

    printf("Email: ");
    scanf("%s", email);

    printf("Password: ");
    scanf("%s", password);

    printf("Department ID: ");
    scanf("%d", &departmentId);

    char query[1000];

    sprintf(query,
    "INSERT INTO lecturers(lecturer_name,employee_id,email,password,department_id) VALUES('%s','%s','%s','%s',%d)",
    name,employeeId,email,password,departmentId);

    if(mysql_query(conn, query))
    {
        printf("Registration Failed\n");
    }
    else
    {
        printf("Lecturer Registered Successfully\n");
    }

    mysql_close(conn);
}

void studentLogin()
{
    MYSQL *conn = connectDB();

    char email[100];
    char password[100];

    printf("\n===== STUDENT LOGIN =====\n");

    printf("Email: ");
    scanf("%s", email);

    printf("Password: ");
    scanf("%s", password);

    char query[1000];

    sprintf(query,
    "SELECT student_id FROM students WHERE email='%s' AND password='%s'",
    email,password);

    mysql_query(conn, query);

    MYSQL_RES *result = mysql_store_result(conn);

    MYSQL_ROW row = mysql_fetch_row(result);

    if(row)
    {
        int studentId = atoi(row[0]);

        printf("Login Successful\n");

        int choice;

        while(1)
        {
            printf("\n1. Submit Complaint\n");
            printf("2. Track Complaint\n");
            printf("3. Logout\n");

            printf("Enter Choice: ");
            scanf("%d", &choice);

            if(choice == 1)
            {
                submitStudentComplaint(studentId);
            }
            else if(choice == 2)
            {
                trackStudentComplaint(studentId);
            }
            else
            {
                break;
            }
        }
    }
    else
    {
        printf("Invalid Login\n");
    }

    mysql_free_result(result);
    mysql_close(conn);
}

void submitStudentComplaint(int studentId)
{
    MYSQL *conn = connectDB();

    char title[255];
    char description[500];
    int departmentId;

    printf("\n===== SUBMIT COMPLAINT =====\n");

    printf("Title: ");
    scanf(" %[^\n]", title);

    printf("Description: ");
    scanf(" %[^\n]", description);

    printf("Department ID: ");
    scanf("%d", &departmentId);

    char query[2000];

    sprintf(query,
    "INSERT INTO complaints(complaint_by,student_id,department_id,title,description) VALUES('student',%d,%d,'%s','%s')",
    studentId,departmentId,title,description);

    if(mysql_query(conn, query))
    {
        printf("Complaint Submission Failed\n");
    }
    else
    {
        printf("Complaint Submitted Successfully\n");
    }

    mysql_close(conn);
}

void trackStudentComplaint(int studentId)
{
    MYSQL *conn = connectDB();

    char query[1000];

    sprintf(query,
    "SELECT complaint_id,title,status FROM complaints WHERE student_id=%d",
    studentId);

    mysql_query(conn, query);

    MYSQL_RES *result = mysql_store_result(conn);

    MYSQL_ROW row;

    printf("\n===== MY COMPLAINTS =====\n");

    while((row = mysql_fetch_row(result)))
    {
        printf("\nComplaint ID : %s\n", row[0]);
        printf("Title        : %s\n", row[1]);
        printf("Status       : %s\n", row[2]);
    }

    mysql_free_result(result);

    mysql_close(conn);
}

void lecturerLogin()
{
    MYSQL *conn = connectDB();

    char email[100];
    char password[100];

    printf("\n===== LECTURER LOGIN =====\n");

    printf("Email: ");
    scanf("%s", email);

    printf("Password: ");
    scanf("%s", password);

    char query[1000];

    sprintf(query,
    "SELECT lecturer_id FROM lecturers WHERE email='%s' AND password='%s'",
    email,password);

    mysql_query(conn, query);

    MYSQL_RES *result = mysql_store_result(conn);

    MYSQL_ROW row = mysql_fetch_row(result);

    if(row)
    {
        int lecturerId = atoi(row[0]);

        printf("Login Successful\n");

        int choice;

        while(1)
        {
            printf("\n1. Submit Complaint\n");
            printf("2. Track Complaint\n");
            printf("3. Logout\n");

            printf("Enter Choice: ");
            scanf("%d", &choice);

            if(choice == 1)
            {
                submitLecturerComplaint(lecturerId);
            }
            else if(choice == 2)
            {
                trackLecturerComplaint(lecturerId);
            }
            else
            {
                break;
            }
        }
    }
    else
    {
        printf("Invalid Login\n");
    }

    mysql_free_result(result);
    mysql_close(conn);
}

void submitLecturerComplaint(int lecturerId)
{
    MYSQL *conn = connectDB();

    char title[255];
    char description[500];
    int departmentId;

    printf("\n===== SUBMIT COMPLAINT =====\n");

    printf("Title: ");
    scanf(" %[^\n]", title);

    printf("Description: ");
    scanf(" %[^\n]", description);

    printf("Department ID: ");
    scanf("%d", &departmentId);

    char query[2000];

    sprintf(query,
    "INSERT INTO complaints(complaint_by,lecturer_id,department_id,title,description) VALUES('lecturer',%d,%d,'%s','%s')",
    lecturerId,departmentId,title,description);

    if(mysql_query(conn, query))
    {
        printf("Complaint Submission Failed\n");
    }
    else
    {
        printf("Complaint Submitted Successfully\n");
    }

    mysql_close(conn);
}

void trackLecturerComplaint(int lecturerId)
{
    MYSQL *conn = connectDB();

    char query[1000];

    sprintf(query,
    "SELECT complaint_id,title,status FROM complaints WHERE lecturer_id=%d",
    lecturerId);

    mysql_query(conn, query);

    MYSQL_RES *result = mysql_store_result(conn);

    MYSQL_ROW row;

    printf("\n===== MY COMPLAINTS =====\n");

    while((row = mysql_fetch_row(result)))
    {
        printf("\nComplaint ID : %s\n", row[0]);
        printf("Title        : %s\n", row[1]);
        printf("Status       : %s\n", row[2]);
    }

    mysql_free_result(result);

    mysql_close(conn);
}

void adminLogin()
{
    MYSQL *conn = connectDB();

    char email[100];
    char password[100];

    printf("\n===== ADMIN LOGIN =====\n");

    printf("Email: ");
    scanf("%s", email);

    printf("Password: ");
    scanf("%s", password);

    char query[1000];

    sprintf(query,
    "SELECT * FROM admin WHERE email='%s' AND password='%s'",
    email,password);

    mysql_query(conn, query);

    MYSQL_RES *result = mysql_store_result(conn);

    MYSQL_ROW row = mysql_fetch_row(result);

    if(row)
    {
        printf("Admin Login Successful\n");

        adminDashboard();
    }
    else
    {
        printf("Invalid Admin Login\n");
    }

    mysql_free_result(result);

    mysql_close(conn);
}

void adminDashboard()
{
    MYSQL *conn = connectDB();

    char query[] =
    "SELECT complaint_id, complaint_by, title, status FROM complaints";

    mysql_query(conn, query);

    MYSQL_RES *result = mysql_store_result(conn);

    MYSQL_ROW row;

    printf("\n===== ADMIN DASHBOARD =====\n");

    while((row = mysql_fetch_row(result)))
    {
        printf("\nComplaint ID : %s\n", row[0]);
        printf("Complaint By : %s\n", row[1]);
        printf("Title        : %s\n", row[2]);
        printf("Status       : %s\n", row[3]);
    }

    mysql_free_result(result);

    mysql_close(conn);
}
