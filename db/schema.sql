--
-- File generated with SQLiteStudio v3.1.1 on So wrz 9 23:15:15 2017
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: sh.CaseSteps
CREATE TABLE [sh.CaseSteps] (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id          INTEGER REFERENCES [sh.TestCase] (id) MATCH [FULL]
                             NOT NULL,
    previous_step_id INTEGER REFERENCES [sh.Step] (id) MATCH [FULL],
    step_id          INTEGER REFERENCES [sh.Step] (id) MATCH [FULL]
                             NOT NULL
);


-- Table: sh.dict.CaseStatus
CREATE TABLE [sh.dict.CaseStatus] (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

INSERT INTO [sh.dict.CaseStatus] (
                                     id,
                                     name
                                 )
                                 VALUES (
                                     1,
                                     'positive'
                                 );

INSERT INTO [sh.dict.CaseStatus] (
                                     id,
                                     name
                                 )
                                 VALUES (
                                     2,
                                     'negative'
                                 );


-- Table: sh.dict.Priority
CREATE TABLE [sh.dict.Priority] (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

INSERT INTO [sh.dict.Priority] (
                                   id,
                                   name
                               )
                               VALUES (
                                   1,
                                   'Low'
                               );

INSERT INTO [sh.dict.Priority] (
                                   id,
                                   name
                               )
                               VALUES (
                                   2,
                                   'Medium'
                               );

INSERT INTO [sh.dict.Priority] (
                                   id,
                                   name
                               )
                               VALUES (
                                   3,
                                   'High'
                               );


-- Table: sh.dict.StepAssembly
CREATE TABLE [sh.dict.StepAssembly] (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

INSERT INTO [sh.dict.StepAssembly] (
                                       id,
                                       name
                                   )
                                   VALUES (
                                       1,
                                       'Arrange'
                                   );

INSERT INTO [sh.dict.StepAssembly] (
                                       id,
                                       name
                                   )
                                   VALUES (
                                       2,
                                       'Act'
                                   );

INSERT INTO [sh.dict.StepAssembly] (
                                       id,
                                       name
                                   )
                                   VALUES (
                                       3,
                                       'Assert'
                                   );


-- Table: sh.dict.StepType
CREATE TABLE [sh.dict.StepType] (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    NOT NULL
);

INSERT INTO [sh.dict.StepType] (
                                   id,
                                   name
                               )
                               VALUES (
                                   1,
                                   'action'
                               );

INSERT INTO [sh.dict.StepType] (
                                   id,
                                   name
                               )
                               VALUES (
                                   2,
                                   'result'
                               );


-- Table: sh.Step
CREATE TABLE [sh.Step] (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    name        TEXT     NOT NULL,
    description TEXT,
    assembly    INTEGER  REFERENCES [sh.dict.StepAssembly] (id) MATCH [FULL],
    type        INTEGER  REFERENCES [sh.dict.StepType] (id) MATCH [FULL],
    applicant   INTEGER  REFERENCES [sh.Users] (id) MATCH [FULL],
    create_time DATETIME,
    modify_time DATETIME,
    modify_by   INTEGER  REFERENCES [sh.Users] (id) MATCH [FULL],
    is_active   INTEGER  NOT NULL
                         DEFAULT (1) 
);


-- Table: sh.TestCase
CREATE TABLE [sh.TestCase] (
    id               INTEGER  PRIMARY KEY,
    name             TEXT     NOT NULL,
    description      TEXT,
    status           INTEGER  REFERENCES [sh.dict.case_status] (id) MATCH [FULL],
    priority         INTEGER  REFERENCES [sh.dict.priority] (id) MATCH [FULL],
    objective        TEXT,
    expected_results TEXT,
    post_conditions  TEXT,
    applicant        INTEGER  REFERENCES [sh.Users] (id) MATCH [FULL]
                              NOT NULL,
    create_time      DATETIME,
    modify_time      DATETIME,
    modify_by        INTEGER  REFERENCES [sh.Users] (id) MATCH [FULL],
    is_active        BOOLEAN  DEFAULT True
);


-- Table: sh.Users
CREATE TABLE [sh.Users] (
    id               INTEGER  PRIMARY KEY ASC AUTOINCREMENT
                              UNIQUE
                              NOT NULL,
    full_name        TEXT,
    login            TEXT     UNIQUE
                              NOT NULL,
    account_type     INTEGER  REFERENCES [sh.dict.AccountType] (id) MATCH [FULL]
                              DEFAULT (1) 
                              NOT NULL,
    notification     INTEGER  NOT NULL
                              DEFAULT (1),
    created_datetime DATETIME NOT NULL
                              DEFAULT ( (datetime('now', 'localtime') ) ),
    is_active        INTEGER  DEFAULT (1) 
                              NOT NULL,
    password         TEXT,
    token            TEXT,
    email            TEXT
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
