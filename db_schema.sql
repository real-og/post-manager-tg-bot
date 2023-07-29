CREATE TABLE channels (
    channel_id BIGINT PRIMARY KEY,
    name varchar(100)
); 

CREATE TABLE access_codes (
  code VARCHAR(255) PRIMARY KEY,
  usage_count INTEGER DEFAULT 0,
  limit_count INTEGER DEFAULT 0,
  last_reset TIMESTAMP DEFAULT NOW(),
  channel_id BIGINT,
  FOREIGN KEY (channel_id) REFERENCES channels (channel_id) ON DELETE CASCADE
);