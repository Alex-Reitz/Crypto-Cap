-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/ioZ39i
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

CREATE TABLE "User" (
    "UserID" int   NOT NULL,
    "Name" varchar(25)   NOT NULL,
    "Username" string   NOT NULL,
    "Password" string   NOT NULL,
    "Favorites" string   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "UserID"
     ),
    CONSTRAINT "uc_User_Name" UNIQUE (
        "Name"
    ),
    CONSTRAINT "uc_User_Username" UNIQUE (
        "Username"
    )
);

CREATE TABLE "Favorites" (
    "FavoriteID" int   NOT NULL,
    "UserID" int   NOT NULL,
    "CryptoName" string   NOT NULL,
    CONSTRAINT "pk_Favorites" PRIMARY KEY (
        "FavoriteID"
     )
);

CREATE TABLE "Cryptos" (
    "CryptoID" int   NOT NULL,
    "Crypto_Name" string   NOT NULL,
    CONSTRAINT "pk_Cryptos" PRIMARY KEY (
        "CryptoID"
     )
);

ALTER TABLE "Favorites" ADD CONSTRAINT "fk_Favorites_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

ALTER TABLE "Favorites" ADD CONSTRAINT "fk_Favorites_CryptoName" FOREIGN KEY("CryptoName")
REFERENCES "Cryptos" ("CryptoID");

