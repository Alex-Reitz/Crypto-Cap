-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/ioZ39i
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "User" (
    "UserID" int   NOT NULL,
    "Email" string   NOT NULL,
    "Username" string   NOT NULL,
    "Password" string   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "UserID"
     ),
    CONSTRAINT "uc_User_Email" UNIQUE (
        "Email"
    ),
    CONSTRAINT "uc_User_Username" UNIQUE (
        "Username"
    )
);

ALTER TABLE "Favorites" ADD CONSTRAINT "fk_Favorites_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

