CREATE TABLE IF NOT EXISTS Company(
	symbol VARCHAR(100) UNIQUE,
	logo VARCHAR(100),
	exchange VARCHAR(100),
	name VARCHAR(100) not NULL,
	cik VARCHAR(100),
	bloomberg VARCHAR(100),
	lei VARCHAR(100),
	sic INTEGER,
	country VARCHAR(100),
	industry VARCHAR(100),
	sector VARCHAR(100),
	marketcap VARCHAR(100),
	employees VARCHAR(100),
	phone VARCHAR(100),
	ceo VARCHAR(100),
	url VARCHAR(100),
	description VARCHAR(100)
);
