#include <stdio.h>
#include <mysql.h>
#include "db.h"

MYSQL *connectDB()
{
    MYSQL *conn;

    conn = mysql_init(NULL);

    if(conn == NULL)
    {
        printf("MySQL Initialization Failed\n");
        return NULL;
    }

    if(!mysql_real_connect(
        conn,
        "localhost",
        "root",
        "",
        "complaint_portal",
        0,
        NULL,
        0))
    {
        printf("Database Connection Failed\n");
        return NULL;
    }

    return conn;
}
