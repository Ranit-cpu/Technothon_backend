-- SQL Query to create sponsors table
CREATE TABLE sponsors (
    sponsor_id VARCHAR(255) PRIMARY KEY,
    sponsor_name VARCHAR(255) NOT NULL,
    selling_domain VARCHAR(255) NOT NULL,
    given_amount BIGINT NULL,  -- Optional - can be NULL if providing goods
    goods_services TEXT NULL,  -- Description of goods/services provided
    contribution_type VARCHAR(50) NOT NULL,  -- 'monetary', 'goods', or 'both'
    sponsor_logo LONGBLOB,  -- For binary encoded photos
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Alternative query for SQLite (if using SQLite instead of MySQL)
-- CREATE TABLE sponsors (
--     sponsor_id VARCHAR(255) PRIMARY KEY,
--     sponsor_name VARCHAR(255) NOT NULL,
--     selling_domain VARCHAR(255) NOT NULL,
--     given_amount INTEGER NULL,  -- Optional - can be NULL if providing goods
--     goods_services TEXT NULL,  -- Description of goods/services provided
--     contribution_type VARCHAR(50) NOT NULL,  -- 'monetary', 'goods', or 'both'
--     sponsor_logo BLOB,  -- For binary encoded photos
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
