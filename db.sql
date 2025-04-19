CREATE DATABASE CC15;

/*ADD INDEXES*/

USE CC15;

CREATE TABLE Users(
    userId INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(100) UNIQUE, /* username should be unique */
    HashedPassword varchar(100) /*password is stored with bcrypt hashes */
);

CREATE TABLE TaskStatus(
    statusId INT PRIMARY KEY,
    statusName varchar(50)
);

CREATE TABLE TaskType(
    typeId INT PRIMARY KEY,
    typeName varchar(50)
);

CREATE TABLE TaskPriority(
    priorityId INT PRIMARY KEY,
    priorityName varchar(50)
);

INSERT INTO TaskStatus VALUES 
    (1,"Completed"),
    (2,"Concluding"),
    (3,"In progress"),
    (4,"Pending");

INSERT INTO TaskType VALUES 
    (1,"Personal"),
    (2,"Academic"),
    (3,"Miscellaneous");

INSERT INTO TaskPriority VALUES
    (1,"Urgent"),
    (2,"High"),
    (3,"Average"),
    (4,"Low"),
    (5,"Optional");

CREATE TABLE Tasks(
    taskId INT AUTO_INCREMENT,
    userId INT,
    priorityId INT,
    typeId INT,
    statusId INT,
    taskName varchar(50),
    deadline DATE,

    PRIMARY KEY (taskId,userId),
    FOREIGN KEY (priorityId) REFERENCES TaskPriority(priorityId),
    FOREIGN KEY (typeId) REFERENCES TaskType(typeId),
    FOREIGN KEY (statusId) REFERENCES TaskStatus(statusId)
);