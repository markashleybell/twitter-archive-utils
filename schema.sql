-- Table: tweets

DROP TABLE tweets;

CREATE TABLE tweets
(
  id bigint NOT NULL,
  created_at timestamp with time zone,
  status text,
  CONSTRAINT pk_tweets PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tweets
  OWNER TO postgres;
