CREATE TABLE Swipes (
	[SwipeId] int IDENTITY(1,1) PRIMARY KEY,
	[IsSwipeIn] bit,
	[UserId] int,
	[SwipeTimeStamp] DateTime,
	FOREIGN KEY ([UserId]) REFERENCES Users([UserId])
)

CREATE TABLE Users(
	[UserId] int IDENTITY(1,1) PRIMARY KEY,
	[UserTypeId] int,
	[IdNumber] nvarchar(14),
	[AccessId] int,
	[IsSwipedIn] bit,
	FOREIGN KEY ([UserTypeId]) REFERENCES UserTypes([UserTypeId]),
    FOREIGN KEY ([AccessId]) REFERENCES Accesses([AccessId])
)

CREATE TABLE Accesses(
	[AccessId] int IDENTITY(1,1) PRIMARY KEY,
	[AccessType] nvarchar(30)
)

CREATE TABLE UserTypes(
	[UserTypeId] int IDENTITY(1,1) PRIMARY KEY,
	[UserType] nvarchar(30)
)

CREATE TABLE Logins(
	[LoginId] int IDENTITY(1,1) PRIMARY KEY,
	[Username] nvarchar(63),
	[Password] nvarchar(21)
)

CREATE OR ALTER VIEW vwSwipes AS
SELECT
    s.SwipeId,
    s.IsSwipeIn,
    s.SwipeTimeStamp,
    ut.UserType,
    ac.AccessType,
    u.IdNumber
FROM 
    Swipes AS s 
    LEFT OUTER JOIN Users AS u ON u.UserId = s.UserId
    LEFT OUTER JOIN Accesses AS ac ON ac.AccessId = u.AccessId
    LEFT OUTER JOIN UserTypes AS ut ON ut.UserTypeId = u.UserTypeId;


CREATE PROCEDURE DeleteOldSwipes
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @FiveYearsAgo DateTime;
    SET @FiveYearsAgo = DATEADD(YEAR, -5, GETDATE());
    DELETE FROM Swipes
    WHERE SwipeTimeStamp < @FiveYearsAgo;
END;

INSERT INTO Accesses VALUES('Active'),('Suspended'),('Deactivated')
INSERT INTO UserTypes VALUES('Student'),('Faculty'),('Staff'),('Janitor')
-----------Users-------------
--Students
INSERT INTO Users VALUES(1, '986532147', 1, 0), (1, '986532987', 1, 0), (1, '986452147', 1, 0), (1, '123786789', 1, 0),(1, '473456789', 1, 0),(1, '123456789', 1, 0),(1, '123786789', 1, 0),(1, '123456747', 1, 0),(1, '123456700', 1, 0),(1, '123456789', 1, 0)
--Faculty
INSERT INTO Users VALUES(2, '31242', 1, 0)
--Staff
INSERT INTO Users VALUES(3, '54363', 1, 0)
--Janitors
INSERT INTO Users VALUES(4, '87546', 1, 0)


-----------Swipes------------
INSERT INTO Swipes VALUES(1, 1, GETDATE()),(0, 1, DATEADD(HOUR, 1, GETDATE())),(1,2,DATEADD(MINUTE, 34, GETDATE())), (0,2,DATEADD(HOUR, 2, GETDATE())), (1,4,DATEADD(HOUR, 10, GETDATE())), (0,4,DATEADD(HOUR, 12, GETDATE())),
(1,11,DATEADD(MINUTE, 20, GETDATE())), (0,11,DATEADD(MINUTE, 40, GETDATE())), (1,10,DATEADD(DAY, 2, GETDATE())), (0,10,DATEADD(DAY, 2, GETDATE())), (1,1,DATEADD(DAY, 3, GETDATE())), (0,1,DATEADD(DAY, 3, GETDATE())),
(1,13,DATEADD(HOUR, 20, GETDATE())), (0,13,DATEADD(HOUR, 23, GETDATE())), (1,12,DATEADD(HOUR, 39, GETDATE())), (0,12,DATEADD(HOUR, 40, GETDATE()))

INSERT INTO Logins Values('Mwwenger', 'Password1!')

select * from Swipes
select * from Users
SELECT * FROM vwSwipes ORDER BY SwipeTimeStamp DESC;
select * from Logins

--CREATE TABLE CombinedSwipesTable(
--	[SwipeId] int IDENTITY(1,1) PRIMARY KEY,
--	[IsSwipeIn] bit,
--	[UserId] int,
--	[TimeStamp] DateTime
--)