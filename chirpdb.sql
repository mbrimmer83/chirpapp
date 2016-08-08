--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: follow; Type: TABLE; Schema: public; Owner: Matthew
--

CREATE TABLE follow (
    id integer NOT NULL,
    follower integer,
    followee integer
);


ALTER TABLE follow OWNER TO "Matthew";

--
-- Name: follow_id_seq; Type: SEQUENCE; Schema: public; Owner: Matthew
--

CREATE SEQUENCE follow_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE follow_id_seq OWNER TO "Matthew";

--
-- Name: follow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Matthew
--

ALTER SEQUENCE follow_id_seq OWNED BY follow.id;


--
-- Name: tweets; Type: TABLE; Schema: public; Owner: Matthew
--

CREATE TABLE tweets (
    tweetid integer NOT NULL,
    user_id integer,
    tweet_date_time timestamp without time zone DEFAULT now(),
    tweet_content character varying(141),
    likes integer,
    retweet_num integer,
    retweet_user_name character varying
);


ALTER TABLE tweets OWNER TO "Matthew";

--
-- Name: tweets_tweetid_seq; Type: SEQUENCE; Schema: public; Owner: Matthew
--

CREATE SEQUENCE tweets_tweetid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tweets_tweetid_seq OWNER TO "Matthew";

--
-- Name: tweets_tweetid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Matthew
--

ALTER SEQUENCE tweets_tweetid_seq OWNED BY tweets.tweetid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: Matthew
--

CREATE TABLE users (
    id integer NOT NULL,
    name character varying,
    email character varying,
    username character varying,
    password character varying
);


ALTER TABLE users OWNER TO "Matthew";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: Matthew
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO "Matthew";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Matthew
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY follow ALTER COLUMN id SET DEFAULT nextval('follow_id_seq'::regclass);


--
-- Name: tweetid; Type: DEFAULT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY tweets ALTER COLUMN tweetid SET DEFAULT nextval('tweets_tweetid_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: follow; Type: TABLE DATA; Schema: public; Owner: Matthew
--

COPY follow (id, follower, followee) FROM stdin;
1	1	2
2	2	1
4	4	5
9	3	1
10	3	2
11	4	1
12	1	4
13	5	1
14	2	4
15	5	4
16	5	2
\.


--
-- Name: follow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Matthew
--

SELECT pg_catalog.setval('follow_id_seq', 16, true);


--
-- Data for Name: tweets; Type: TABLE DATA; Schema: public; Owner: Matthew
--

COPY tweets (tweetid, user_id, tweet_date_time, tweet_content, likes, retweet_num, retweet_user_name) FROM stdin;
1	1	2016-07-29 13:55:33.941534	This is my first chirp!	0	0	\N
2	1	2016-07-29 13:56:13.107803	I am almost done building this application!	0	0	\N
7	5	2016-07-29 13:58:53.776634	Kyle in the house!	0	0	\N
8	5	2016-07-29 13:59:13.908908	Javascript or Python?	0	0	\N
5	4	2016-07-29 13:57:50.954031	Yo fools, I'm Carolyn!	0	1	\N
12	1	2016-07-29 14:15:40.61756	Hi, I am Toby.	0	0	tobyho123
3	2	2016-07-29 13:57:05.367382	Hi, I am Toby.	1	2	\N
13	1	2016-07-29 14:47:35.380856	Python rocks!	0	0	carolyndaniel123
14	2	2016-07-29 14:49:11.735893	Python rocks!	0	0	carolyndaniel123
15	5	2016-07-29 14:54:20.639605	Python rocks!	0	0	carolyndaniel123
6	4	2016-07-29 13:58:19.902366	Python rocks!	2	4	\N
16	5	2016-07-29 14:54:32.430808	I love to chirp!	0	0	tobyho123
17	5	2016-07-29 15:03:25.68657	I love to chirp!	0	0	tobyho123
4	2	2016-07-29 13:57:16.278567	I love to chirp!	1	4	\N
18	5	2016-07-29 15:04:13.310914	Chirping rocks!	0	0	\N
\.


--
-- Name: tweets_tweetid_seq; Type: SEQUENCE SET; Schema: public; Owner: Matthew
--

SELECT pg_catalog.setval('tweets_tweetid_seq', 18, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: Matthew
--

COPY users (id, name, email, username, password) FROM stdin;
1	Matthew Brimmer	mbrimmer1@gmail.com	mbrimmer1	$2b$10$kqxET1kOJ7gMrj/tGrPUl.m86rlWeD5.4Iq7PLpmA8rR8ZJdDR13u
2	Toby Ho	tobyho@yahoo.com	tobyho123	$2b$10$U82/mSMtstyoE7CTPwN5GecIWQU9ubmI5f/TX6EcAJlDD2DSRDcsO
3	John Doe	jdoe@yahoo.com	johndoe123	$2b$10$1v/OpATz.RMpo.fPsXS64OAbGYWY7/AsqUUOjf8DYCTa7hTYJgkHW
4	Carolyn Daniel	cdaniel@yhoo.com	carolyndaniel123	$2b$10$rgQxP7Z6knt0BNz6emYjFeE0.QQmsxcI/Fat9ZLY.nyT9ZdhnknNi
5	Kyle Luck	kluck@yahoo.com	kyleluck123	$2b$10$mdjj5HZ/sjCTtmhBZy9DKuWXBflAbnORHRr0.q3TRhYRuEgHOg0Vu
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Matthew
--

SELECT pg_catalog.setval('users_id_seq', 5, true);


--
-- Name: follow_pkey; Type: CONSTRAINT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY follow
    ADD CONSTRAINT follow_pkey PRIMARY KEY (id);


--
-- Name: tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (tweetid);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: follow_followee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY follow
    ADD CONSTRAINT follow_followee_fkey FOREIGN KEY (followee) REFERENCES users(id);


--
-- Name: follow_follower_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY follow
    ADD CONSTRAINT follow_follower_fkey FOREIGN KEY (follower) REFERENCES users(id);


--
-- Name: tweets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Matthew
--

ALTER TABLE ONLY tweets
    ADD CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

