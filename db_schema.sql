CREATE TABLE channels (
    channel_id BIGINT PRIMARY KEY,
    name varchar(100)
); 

CREATE TABLE access_codes (
  code VARCHAR(255) PRIMARY KEY,
  usage_count INTEGER DEFAULT 0,
  tg_link_usage_count INTEGER DEFAULT 0,
  limit_count_all INTEGER DEFAULT 0,
  limit_count_tg_link INTEGER DEFAULT 0,
  limit_days INTEGER DEFAULT 0,
  creation_datetime TIMESTAMP DEFAULT NOW(),
  channel_id BIGINT,
  FOREIGN KEY (channel_id) REFERENCES channels (channel_id) ON DELETE CASCADE
);