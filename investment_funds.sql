CREATE TABLE IF NOT EXISTS investment_funds (
    fund_id TEXT PRIMARY KEY,
    fund_name VARCHAR(255) NOT NULL,
    fund_manager_name VARCHAR(100) NOT NULL,
    fund_desc TEXT,
    fund_nav DECIMAL(15, 2),
    creation_date DATE,
    performance DECIMAL(5, 2)
);