CREATE TABLE GOLDSET (
    Gold_ID INT NOT NULL,
    Name CHAR(50),
    Quantity FLOAT NOT NULL,
    BuyPrice FLOAT NOT NULL,
    BuyDate DATE,
    GoldForm CHAR(50),
    Origin CHAR(50),
    Finess INT,
    PRIMARY KEY (Gold_ID)
);
